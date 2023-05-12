from __future__ import annotations

import codecs
import os
import os.path
from glob import glob
from secrets import token_bytes

import pkg_resources
from tutor import hooks

from .__about__ import __version__

########################################
# CONFIGURATION
########################################

hooks.Filters.CONFIG_DEFAULTS.add_items(
    [
        ("JUPYTER_VERSION", __version__),
        (
            "JUPYTER_DOCKER_IMAGE_HUB",
            "{{ DOCKER_REGISTRY }}overhangio/jupyterhub:{{ JUPYTER_VERSION }}",
        ),
        (
            "JUPYTER_DOCKER_IMAGE_LAB",
            "{{ DOCKER_REGISTRY }}overhangio/jupyterlab:{{ JUPYTER_VERSION }}",
        ),
        ("JUPYTER_HOST", "jupyter.{{ LMS_HOST }}"),
        ("JUPYTER_DEFAULT_PASSPORT_ID", "jupyterhub"),
        ("JUPYTER_LTI_CLIENT_KEY", "openedx"),
        ("JUPYTER_HUB_MYSQL_DATABASE", "jupyterhub"),
        ("JUPYTER_HUB_MYSQL_USERNAME", "jupyterhub"),
        ("JUPYTER_LAB_CPU_LIMIT", None),
        ("JUPYTER_LAB_MEMORY_LIMIT", "200M"),
    ]
)

hooks.Filters.CONFIG_UNIQUE.add_items(
    [
        ("JUPYTER_HUB_COOKIE_SECRET", "{{ 32|jupyterhub_crypt_key }}"),
        ("JUPYTER_HUB_CRYPT_KEY", "{{ 32|jupyterhub_crypt_key }}"),
        ("JUPYTER_HUB_MYSQL_PASSWORD", "{{ 24|random_string }}"),
        ("JUPYTER_LTI_CLIENT_SECRET", "{{ 24|random_string }}"),
    ]
)


def jupyterhub_crypt_key(size: int) -> str:
    """
    Return a random hex-encoded bytes string of fixed size. This is equivalent to `openssl rand -hex 32`.
    https://jupyterhub.readthedocs.io/en/stable/reference/authenticators.html#authentication-state
    """
    return codecs.encode(token_bytes(size), "hex").decode()


hooks.Filters.ENV_TEMPLATE_FILTERS.add_item(
    ("jupyterhub_crypt_key", jupyterhub_crypt_key)
)

########################################
# INITIALIZATION TASKS
########################################

MY_INIT_TASKS: list[tuple[str, tuple[str, ...]]] = [
    ("mysql", ("jupyter", "jobs", "init", "mysql.sh")),
    ("jupyterhub", ("jupyter", "jobs", "init", "jupyterhub.sh")),
]

for service, template_path in MY_INIT_TASKS:
    full_path: str = pkg_resources.resource_filename(
        "tutorjupyter", os.path.join("templates", *template_path)
    )
    with open(full_path, encoding="utf-8") as init_task_file:
        init_task: str = init_task_file.read()
    hooks.Filters.CLI_DO_INIT_TASKS.add_item((service, init_task))


########################################
# DOCKER IMAGE MANAGEMENT
########################################


hooks.Filters.IMAGES_BUILD.add_items(
    [
        (
            "jupyterhub",
            ("plugins", "jupyter", "build", "hub"),
            "{{ JUPYTER_DOCKER_IMAGE_HUB }}",
            (),
        ),
        (
            "jupyterlab",
            ("plugins", "jupyter", "build", "lab"),
            "{{ JUPYTER_DOCKER_IMAGE_LAB }}",
            (),
        ),
    ]
)
hooks.Filters.IMAGES_PULL.add_items(
    [
        ("jupyterhub", "{{ JUPYTER_DOCKER_IMAGE_HUB }}"),
        ("jupyterlab", "{{ JUPYTER_DOCKER_IMAGE_LAB }}"),
    ]
)
hooks.Filters.IMAGES_PUSH.add_items(
    [
        ("jupyterhub", "{{ JUPYTER_DOCKER_IMAGE_HUB }}"),
        ("jupyterlab", "{{ JUPYTER_DOCKER_IMAGE_LAB }}"),
    ]
)


########################################
# TEMPLATE RENDERING
########################################

hooks.Filters.ENV_TEMPLATE_ROOTS.add_items(
    # Root paths for template files, relative to the project root.
    [
        pkg_resources.resource_filename("tutorjupyter", "templates"),
    ]
)

hooks.Filters.ENV_TEMPLATE_TARGETS.add_items(
    [
        ("jupyter/build", "plugins"),
        ("jupyter/apps", "plugins"),
    ],
)


########################################
# PATCH LOADING
########################################

# For each file in tutorjupyter/patches,
# apply a patch based on the file's name and contents.
for path in glob(
    os.path.join(
        pkg_resources.resource_filename("tutorjupyter", "patches"),
        "*",
    )
):
    with open(path, encoding="utf-8") as patch_file:
        hooks.Filters.ENV_PATCHES.add_item((os.path.basename(path), patch_file.read()))

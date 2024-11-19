from __future__ import annotations

import codecs
import os
import os.path
import typing as t
from glob import glob
from secrets import token_bytes

import importlib_resources
from tutor import hooks
from tutor.__about__ import __version_suffix__

from .__about__ import __version__

# Handle version suffix in main mode, just like tutor core
if __version_suffix__:
    __version__ += "-" + __version_suffix__

########################################
# CONFIGURATION
########################################

config: t.Dict[str, t.Dict[str, t.Any]] = {
    "defaults": {
        "VERSION": __version__,
        "DOCKER_IMAGE_HUB": "{{ DOCKER_REGISTRY }}overhangio/jupyterhub:{{ JUPYTER_VERSION }}",
        "DOCKER_IMAGE_LAB": "{{ DOCKER_REGISTRY }}overhangio/jupyterlab:{{ JUPYTER_VERSION }}",
        "HOST": "jupyter.{{ LMS_HOST }}",
        "DEFAULT_PASSPORT_ID": "jupyterhub",
        "LTI_CLIENT_KEY": "openedx",
        "HUB_MYSQL_DATABASE": "jupyterhub",
        "HUB_MYSQL_USERNAME": "jupyterhub",
        "LAB_CPU_LIMIT": None,
        "LAB_MEMORY_LIMIT": "200M",
    },
    "unique": {
        "HUB_COOKIE_SECRET": "{{ 32|jupyterhub_crypt_key }}",
        "HUB_CRYPT_KEY": "{{ 32|jupyterhub_crypt_key }}",
        "HUB_MYSQL_PASSWORD": "{{ 24|random_string }}",
        "LTI_CLIENT_SECRET": "{{ 24|random_string }}",
    },
}
hooks.Filters.CONFIG_DEFAULTS.add_items(
    [(f"JUPYTER_{key}", value) for key, value in config.get("defaults", {}).items()]
)
hooks.Filters.CONFIG_UNIQUE.add_items(
    [(f"JUPYTER_{key}", value) for key, value in config.get("unique", {}).items()]
)
hooks.Filters.CONFIG_OVERRIDES.add_items(list(config.get("overrides", {}).items()))


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

for service in ["mysql", "jupyterhub"]:
    full_path: str = str(
        importlib_resources.files("tutorjupyter")
        / "templates"
        / "jupyter"
        / "tasks"
        / service
        / "init"
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

hooks.Filters.ENV_TEMPLATE_ROOTS.add_item(
    # Root path for template files, relative to the project root.
    str(importlib_resources.files("tutorjupyter") / "templates")
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
for path in glob(str(importlib_resources.files("tutorjupyter") / "patches" / "*")):
    with open(path, encoding="utf-8") as patch_file:
        hooks.Filters.ENV_PATCHES.add_item((os.path.basename(path), patch_file.read()))

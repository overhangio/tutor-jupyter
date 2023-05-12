Jupyter Notebook plugin for `Tutor <https://docs.tutor.overhang.io>`__
======================================================================

This is a plugin for Tutor that makes it easy to integrate `Jupyter <https://jupyter.org/>`__ notebooks in `Open edX <https://openedx.org>`__. It achieves the following:

1. Install the official `jupyter-xblock <https://github.com/overhangio/jupyter-xblock/>`__ in the Open edX LMS and Studio.
2. Run a Docker-based `JupyterHub <https://jupyterhub.readthedocs.io/en/stable/>`__ instance with a `Docker spawner <https://jupyterhub-dockerspawner.readthedocs.io/en/latest/>`__.

In pratice, it means that students will be allocated Docker containers with limited CPU and memory to run their custom notebooks.

⚠️ This plugin is not compatible with Kubernetes. If you wish to run JupyterHub on Kubernetes, you are encouraged to check the documentation of the `Zero to JupyterHub with Kubernetes <https://z2jh.jupyter.org/en/stable/resources/reference.html>`__ project.

Installation
------------

::

    pip install tutor-jupyter

Usage
-----

Launch a local platform ::

    tutor plugins enable jupyter mfe
    tutor config save
    tutor images build openedx
    tutor local launch

TODO Create LTI passport in Open edX::

    echo "$(tutor config printvalue JUPYTER_DEFAULT_PASSPORT_ID):$(tutor config printvalue JUPYTER_LTI_CLIENT_KEY):$(tutor config printvalue JUPYTER_LTI_CLIENT_SECRET)"

Configuration
-------------

Settings
~~~~~~~~

TODO

- JUPYTER_DOCKER_IMAGE_HUB (default: ``"{{ DOCKER_REGISTRY }}overhangio/jupyterhub:{{ JUPYTER_VERSION }}"``)
- JUPYTER_DOCKER_IMAGE_LAB (default: ``"{{ DOCKER_REGISTRY }}overhangio/jupyterlab:{{ JUPYTER_VERSION }}"``)
- JUPYTER_HOST (default: ``"jupyter.{{ LMS_HOST }}"``)
- JUPYTER_DEFAULT_PASSPORT_ID (default: ``"jupyterhub"``)
- JUPYTER_LTI_CLIENT_KEY (default: ``"openedx"``)
- JUPYTER_HUB_MYSQL_DATABASE (default: ``"jupyterhub"``)
- JUPYTER_HUB_MYSQL_USERNAME (default: ``"jupyterhub"``)
- JUPYTER_LAB_CPU_LIMIT", None
- JUPYTER_LAB_MEMORY_LIMIT (default: ``"200M"``)

- JUPYTER_HUB_COOKIE_SECRET (default: ``"{{ 32|jupyterhub_crypt_key }}"``)
- JUPYTER_HUB_CRYPT_KEY (default: ``"{{ 32|jupyterhub_crypt_key }}"``)
- JUPYTER_HUB_MYSQL_PASSWORD (default: ``"{{ 24|random_string }}"``)
- JUPYTER_LTI_CLIENT_SECRET (default: ``"{{ 24|random_string }}"``)

Modifying the default lab environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

TODO implement "jupyter-lab-dockerfile" patch::

    from tutor import hooks

    hooks.Filters.ENV_PATCHES.add_item(
        (
            "jupyter-lab-dockerfile",
            """
    # Install extra Python packages
    RUN pip install matplotlib scipy seaborn
    """
        )
    )

Then build the lab image again::

    tutor config save
    tutor images build jupyterlab

License
-------

This software is licensed under the terms of the `AGPLv3 <https://www.gnu.org/licenses/agpl-3.0.en.html>`__.

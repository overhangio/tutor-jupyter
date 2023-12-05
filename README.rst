Jupyter Notebook plugin for `Tutor <https://docs.tutor.edly.io>`__
======================================================================

This is a plugin for Tutor that makes it easy to integrate `Jupyter <https://jupyter.org/>`__ notebooks in `Open edX <https://openedx.org>`__. It achieves the following:

1. Install the official `jupyter-xblock <https://github.com/overhangio/jupyter-xblock/>`__ in the Open edX LMS and Studio.
2. Run a Docker-based `JupyterHub <https://jupyterhub.readthedocs.io/en/stable/>`__ instance with a `Docker spawner <https://jupyterhub-dockerspawner.readthedocs.io/en/latest/>`__.

In pratice, it means that students will be allocated Docker containers with limited CPU and memory to run their custom notebooks.

⚠️ Compatibility with Kubernetes was not battle-tested. Please report any issue you face. For a more production-ready Kubernetes environment, you are encouraged to check the documentation of the `Zero to JupyterHub with Kubernetes <https://z2jh.jupyter.org/en/stable/resources/reference.html>`__ project.

Installation
------------

::

    tutor plugins install jupyter

Usage
-----

Enable the plugin::

    tutor plugins enable jupyter

Re-build the "openedx" Docker image to install the Jupyter XBlock::

    tutor images build openedx

Launch your platform again::

    tutor local launch

Print the default passport ID::

    echo "$(tutor config printvalue JUPYTER_DEFAULT_PASSPORT_ID):$(tutor config printvalue JUPYTER_LTI_CLIENT_KEY):$(tutor config printvalue JUPYTER_LTI_CLIENT_SECRET)"

Make a note of the printed value. Go to the Studio Tools ➡️ Advanced Settings ➡️ LTI Passports. Insert the passport value:

.. image:: https://raw.githubusercontent.com/overhangio/jupyter-xblock/main/static/screenshots/studio-advanced-settings-lti.png
     :alt: Studio advanced settings


In "Advanced Module List" add "jupyter" (with quotes):

.. image:: https://raw.githubusercontent.com/overhangio/jupyter-xblock/main/static/screenshots/studio-advanced-settings.png
     :alt: Studio advanced settings

You should then be able to create an advanced Jupyter XBlock in the Studio:

> Add New Component ➡️ Advanced ➡️ Jupyter notebook

The default `"hello" <https://github.com/overhangio/jupyter-xblock/blob/main/static/notebooks/hello.ipynb>`__  notebook will be pulled from the jupyter-block repository and displayed in the studio.


Configuration
-------------

Settings
~~~~~~~~

This plugin has the following Tutor settings. Each setting can be printed with ``tutor config printvalue JUPYTER_SETTING_NAME`` and modified with ``tutor config save --set JUPYTER_SETTING_NAME=value``.

Default settings:

- JUPYTER_DOCKER_IMAGE_HUB (default: ``"{{ DOCKER_REGISTRY }}overhangio/jupyterhub:{{ JUPYTER_VERSION }}"``)
- JUPYTER_DOCKER_IMAGE_LAB (default: ``"{{ DOCKER_REGISTRY }}overhangio/jupyterlab:{{ JUPYTER_VERSION }}"``)
- JUPYTER_HOST (default: ``"jupyter.{{ LMS_HOST }}"``)
- JUPYTER_DEFAULT_PASSPORT_ID (default: ``"jupyterhub"``)
- JUPYTER_LTI_CLIENT_KEY (default: ``"openedx"``)
- JUPYTER_HUB_MYSQL_DATABASE (default: ``"jupyterhub"``)
- JUPYTER_HUB_MYSQL_USERNAME (default: ``"jupyterhub"``)
- JUPYTER_LAB_CPU_LIMIT (default: ``None``)
- JUPYTER_LAB_MEMORY_LIMIT (default: ``"200M"``)

Unique, user-specific settings:

- JUPYTER_HUB_COOKIE_SECRET (default: ``"{{ 32|jupyterhub_crypt_key }}"``)
- JUPYTER_HUB_CRYPT_KEY (default: ``"{{ 32|jupyterhub_crypt_key }}"``)
- JUPYTER_HUB_MYSQL_PASSWORD (default: ``"{{ 24|random_string }}"``)
- JUPYTER_LTI_CLIENT_SECRET (default: ``"{{ 24|random_string }}"``)

JupyterHub
~~~~~~~~~~

The configuration template for the JupyterHub instance is stored in `jupyterhub_config.py <./tutorjupyter/templates/jupyter/apps/jupyterhub_config.py>`__. This template file includes a ``{{ patch("jupyterhub-config") }}`` statement, which means that its contents can be overridden by creating an ad-hoc Tutor plugin. For instance, to add custom LTI keys to your JupyterHub instance::

    from tutor import hooks

    hooks.Filters.ENV_PATCHES.add_item(
        (
            "jupyterhub-config",
            """
    # Add LTI keys to the authenticator
    c.LTI11Authenticator.consumers["my-lti-key"] = "my-lti-secret"
    """
        )
    )

Lab environment
~~~~~~~~~~~~~~~

By default, Jupyter lab notebooks will be spawned that do not include extra Python packages or dependencies. To modify the "jupyterlab" Docker image and add extra Python packages (for example), you should create a Tutor plugin that implements the "jupyter-lab-dockerfile" patch::

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

You should now be able to run ``import matplotlib`` statements within your Jupyter notebooks.

Troubleshooting
---------------

This Tutor plugin is maintained by Muhammad Hassan Siddiqi from `Edly <https://edly.io>`__. Community support is available from the official `Open edX forum <https://discuss.openedx.org>`__. Do you need help with this plugin? See the `troubleshooting <https://docs.tutor.edly.io/troubleshooting.html>`__ section from the Tutor documentation.

License
-------

This software is licensed under the terms of the `AGPLv3 <https://www.gnu.org/licenses/agpl-3.0.en.html>`__.

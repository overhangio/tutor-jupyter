# https://hub.docker.com/r/jupyterhub/singleuser/tags
FROM docker.io/jupyterhub/singleuser:4

# Install git for nbgitpuller
USER root
RUN apt update && apt install -y git

USER jovyan

# Download git repos
# https://github.com/jupyterhub/nbgitpuller
# https://hub.jupyter.org/nbgitpuller/
# https://pypi.org/project/nbgitpuller/
RUN pip install nbgitpuller==1.2.0

# https://pypi.org/project/jupyterlab/
RUN pip install jupyterlab==4.0.9

{{ patch("jupyter-lab-dockerfile") }}

# Disable obnoxious jupyterlab announcements
# https://jupyterlab.readthedocs.io/en/stable/user/announcements.html
RUN jupyter labextension disable "@jupyterlab/apputils-extension:announcements"


# Load custom config
COPY --chown=jovyan:jovyan ./config.py /tmp/
RUN cat /tmp/config.py >> /etc/jupyter/jupyter_notebook_config.py \
    && rm /tmp/config.py

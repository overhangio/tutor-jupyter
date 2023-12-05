# https://hub.docker.com/r/jupyterhub/jupyterhub/tags
# Base: https://github.com/jupyterhub/jupyterhub/blob/main/Dockerfile
FROM docker.io/jupyterhub/jupyterhub:4

# https://pypi.org/project/dockerspawner/
# https://pypi.org/project/jupyterhub-kubespawner/
# https://pypi.org/project/jupyterhub-ltiauthenticator/
# https://pypi.org/project/pymysql/
RUN pip install \
    dockerspawner==13.0.0 \
    jupyterhub-kubespawner==6.2.0 \
    jupyterhub-ltiauthenticator==1.6.1 \
    pymysql==1.1.0

CMD ["jupyterhub"]

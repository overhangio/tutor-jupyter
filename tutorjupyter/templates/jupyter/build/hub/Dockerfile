# https://hub.docker.com/r/jupyterhub/jupyterhub/tags
# Base: https://github.com/jupyterhub/jupyterhub/blob/main/Dockerfile
FROM docker.io/jupyterhub/jupyterhub:4.0.0

# https://pypi.org/project/dockerspawner/
# https://pypi.org/project/jupyterhub-ltiauthenticator/
# https://pypi.org/project/pymysql/
RUN pip install dockerspawner==12.1.0 jupyterhub-ltiauthenticator==1.5.1 pymysql==1.0.3

CMD ["jupyterhub"]

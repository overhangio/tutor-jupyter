# https://hub.docker.com/r/jupyterhub/jupyterhub/tags
# Base: https://github.com/jupyterhub/jupyterhub/blob/main/Dockerfile
# Upgrade to 4.0.0 once this is fixed in LTIAuthenticator:
# https://github.com/jupyterhub/ltiauthenticator/issues/157
# FROM docker.io/jupyterhub/jupyterhub:4.0.0
FROM docker.io/jupyterhub/jupyterhub:3.1.1

# https://pypi.org/project/dockerspawner/
RUN pip install dockerspawner==12.1.0
# https://pypi.org/project/jupyterhub-ltiauthenticator/
RUN pip install jupyterhub-ltiauthenticator==1.3.0
# https://pypi.org/project/pymysql/
RUN pip install pymysql==1.0.3

CMD ["jupyterhub"]

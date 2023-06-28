# Configuration file for jupyterhub.
# Reference: https://jupyterhub.readthedocs.io/en/latest/reference/config-reference.html
# Heavily inspired by: https://github.com/jupyterhub/jupyterhub-deploy-docker/blob/master/jupyterhub_config.py
import os

c = get_config()  # pylint: disable=undefined-variable

# Logging
c.Application.log_level = "DEBUG"
c.JupyterHub.log_level = "DEBUG"
# Public IP and port
c.JupyterHub.ip = "0.0.0.0"
c.JupyterHub.port = 9045
# Internal IP and port that spawners connect to
c.JupyterHub.hub_ip = "0.0.0.0"
c.JupyterHub.hub_port = 8081
# Database
c.JupyterHub.db_url = "mysql+pymysql://{{ JUPYTER_HUB_MYSQL_USERNAME }}:{{ JUPYTER_HUB_MYSQL_PASSWORD }}@{{ MYSQL_HOST }}:{{ MYSQL_PORT }}/{{ JUPYTER_HUB_MYSQL_DATABASE }}"
c.JupyterHub.cookie_secret = "{{ JUPYTER_HUB_COOKIE_SECRET }}"
# Don't write pid file to current folder, where we may not have write access
c.ConfigurableHTTPProxy.pid_file = "/tmp/jupyter-proxy.pid"

# Authorise embedding in some iframes.
# Add "*" to allow embedding in all iframes (though it's dangerous and you probably
# shouldn't do it).
# https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy/frame-ancestors
frame_ancestors = [
    "{% if ENABLE_HTTPS %}https{% else %}http{% endif %}://{{ LMS_HOST }}",
    "{% if ENABLE_HTTPS %}https{% else %}http{% endif %}://{{ LMS_HOST }}:8000",
    "{% if ENABLE_HTTPS %}https{% else %}http{% endif %}://{{ CMS_HOST }}",
    "{% if ENABLE_HTTPS %}https{% else %}http{% endif %}://{{ CMS_HOST }}:8001",
    "{% if ENABLE_HTTPS %}https{% else %}http{% endif %}://{{ PREVIEW_LMS_HOST }}",
    "{% if ENABLE_HTTPS %}https{% else %}http{% endif %}://{{ PREVIEW_LMS_HOST }}:8000",
]
{% if MFE_HOST is defined %}
frame_ancestors += [
    "{% if ENABLE_HTTPS %}https{% else %}http{% endif %}://{{ MFE_HOST }}",
    "{% if ENABLE_HTTPS %}https{% else %}http{% endif %}://{{ MFE_HOST }}:2000",
]
{% endif %}
content_security_policy = "frame-ancestors 'self' " + " ".join(frame_ancestors) + ";"
c.JupyterHub.tornado_settings = {
    "headers": {"Content-Security-Policy": content_security_policy}
}

# Authenticator
# note that the JUPYTERHUB_CRYPT_KEY env var must be defined
c.Authenticator.enable_auth_state = True

# LTI authenticator
# https://github.com/jupyterhub/ltiauthenticator

# LTI 1.1
# https://github.com/jupyterhub/ltiauthenticator/blob/main/examples/jupyterhub_config_lti11.py
c.JupyterHub.authenticator_class = "ltiauthenticator.LTIAuthenticator"
c.LTI11Authenticator.consumers = {
    "{{ JUPYTER_LTI_CLIENT_KEY }}": "{{ JUPYTER_LTI_CLIENT_SECRET }}"
}
c.LTI11Authenticator.username_key = "lis_person_sourcedid"

# # LTI 1.3
# # https://github.com/jupyterhub/ltiauthenticator/blob/main/examples/jupyterhub_config_lti13.py
# c.JupyterHub.authenticator_class = "ltiauthenticator.lti13.auth.LTI13Authenticator"
# c.LTI13Authenticator.username_key: "given_name"
# c.LTI13Authenticator.authorize_url: "https://canvas.instructure.com/api/lti/authorize_redirect"
# c.LTI13Authenticator.client_id: "125900000000000329"
# c.LTI13Authenticator.endpoint: "http://localhost:8000/hub/oauth_callback"
# c.LTI13Authenticator.token_url: "https://canvas.instructure.com/login/oauth2/token"

# nbgitpuller
c.ServerApp.nbserver_extensions = {"nbgitpuller": True}

# Spawner
# Limit spawner cpu and memory
{% if JUPYTER_LAB_CPU_LIMIT %}
c.Spawner.cpu_limit = {{ JUPYTER_LAB_CPU_LIMIT }}
{% endif %}
c.Spawner.mem_limit = "{{ JUPYTER_LAB_MEMORY_LIMIT }}"

if os.environ.get("SPAWNER") == "docker":
    # Run as Docker containers
    # https://jupyterhub-dockerspawner.readthedocs.io/en/latest/api/index.html
    c.JupyterHub.spawner_class = "dockerspawner.DockerSpawner"
    c.DockerSpawner.image = "{{ JUPYTER_DOCKER_IMAGE_LAB }}"
    c.DockerSpawner.debug = True
    c.DockerSpawner.remove = True
    c.DockerSpawner.use_internal_ip = True
    c.DockerSpawner.network_name = os.environ.get("NETWORK_NAME")
    c.DockerSpawner.environment = {"CONTENT_SECURITY_POLICY": content_security_policy}
    # Persist user data: this will create a new "jupyterhub-user-{username}" named volume on
    # the host for every Docker container.
    # https://jupyterhub-dockerspawner.readthedocs.io/en/latest/data-persistence.html
    c.DockerSpawner.notebook_dir = "/home/jovyan/work"
    c.DockerSpawner.volumes = {"jupyterhub-user-{username}": c.DockerSpawner.notebook_dir}
elif os.environ.get("SPAWNER") == "kubernetes":
    # Run as kubernetes pods
    # https://jupyterhub-kubespawner.readthedocs.io/en/latest/spawner.html
    # https://z2jh.jupyter.org/en/stable/resources/reference.html#helm-chart-configuration-reference
    # spoiler: you're in for one hell of a ride...
    c.JupyterHub.spawner_class = "kubespawner.KubeSpawner"
    c.KubeSpawner.debug = True
    c.KubeSpawner.hub_connect_url = "http://jupyterhub:8081"
    # c.KubeSpawner.port = 8081
    c.KubeSpawner.service_account = "jupyterhub"
    c.KubeSpawner.image = "{{ JUPYTER_DOCKER_IMAGE_LAB }}"
    c.KubeSpawner.environment = {"CONTENT_SECURITY_POLICY": content_security_policy}

{{ patch("jupyterhub-config") }}

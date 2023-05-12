# Custom notebook configuration
import os

# Authorise embedding in some iframes.
content_security_policy = os.environ.get("CONTENT_SECURITY_POLICY")
if content_security_policy:
    c.NotebookApp.tornado_settings = {
        "headers": {"Content-Security-Policy": content_security_policy}
    }

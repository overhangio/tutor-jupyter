# Changelog

This file includes a history of past releases. Changes that were not yet added to a release are in the [changelog.d/](./changelog.d) folder.

<!--
⚠️ DO NOT ADD YOUR CHANGES TO THIS FILE! (unless you want to modify existing changelog entries in this file)
Changelog entries are managed by scriv. After you have made some changes to this plugin, create a changelog entry with:

    scriv create

Edit and commit the newly-created file in changelog.d.

If you need to create a new release, create a separate commit just for that. It is important to respect these
instructions, because git commits are used to generate release notes:
  - Modify the version number in `__about__.py`.
  - Collect changelog entries with `scriv collect`
  - The title of the commit should be the same as the new version: "vX.Y.Z".
-->

<!-- scriv-insert-here -->

<a id='changelog-16.0.1'></a>
## v16.0.1 (2023-06-29)

- [Feature] Run JupyterHub on Kubernetes. This is an alpha feature. Feedback is welcome! (by @regisb)

<a id='changelog-16.0.0'></a>
## v16.0.0 (2023-06-15)

- 💥[Feature] Upgrade to Quince. (by @regisb)

<a id='changelog-15.0.2'></a>
## v15.0.2 (2023-05-24)

- [Improvement] Upgrade JupyterHub to 4.0.0. This is possible now that [this ltiauthenticator issue](https://github.com/jupyterhub/ltiauthenticator/issues/157) is resolved. (by @regisb)

<a id='changelog-15.0.1'></a>
## v15.0.1 (2023-05-22)

- [Improvement] Add a scriv-compliant changelog. (by @regisb)
- [Feature] upgrade jupyter-xblock to 15.0.3. (by @regisb)


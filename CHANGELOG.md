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

<a id='changelog-20.0.0'></a>
## v20.0.0 (2025-04-06)

- 💥[Feature] Renamed the `jupyter-lab-dockerfile` to `jupyterlab-dockerfile` for consistency across the Tutor ecosystem and added the `jupyterhub-dockerfile` patch to the JupyterHub Dockerfile for customization. If you were previously using the patch with the old name, update your configuration to reflect the new name to ensure compatibility. (by @Abdul-Muqadim-Arbisoft)

- [Improvement] Migrate packaging from setup.py/setuptools to pyproject.toml/hatch. (by @Abdul-Muqadim-Arbisoft)
  - For more details view tutor core PR: https://github.com/overhangio/tutor/pull/1163

- [Improvement] Add hatch_build.py in sdist target to fix the installation issues (by @dawoudsheraz)

- 💥[Feature] Upgrade to teak. (by @Abdul-Muqadim-Arbisoft)

<a id='changelog-19.0.0'></a>
## v19.0.0 (2024-12-16)

- 💥[Feature] Upgrade to Sumac (by @Abdul-Muqadim-Arbisoft)

<a id='changelog-18.1.1'></a>
## v18.1.1 (2024-12-16)

- 💥 [Deprecation] Drop support for python 3.8 and set Python 3.9 as the minimum supported python version. (by @Abdul-Muqadim-Arbisoft)

- 💥[Improvement] Rename Tutor's two branches (by @DawoudSheraz):
  * Rename **master** to **release**, as this branch runs the latest official Open edX release tag.
  * Rename **nightly** to **main**, as this branch runs the Open edX master branches, which are the basis for the next Open edX release.

- [Bugfix] Fix the LTI_DEFAULT_JUPYTER_HUB_URL which had an extra '%' in the HTTPS URL. (by @Danyal-Faheem)

<a id='changelog-18.1.0'></a>
## v18.1.0 (2024-09-15)

- 💥[Feature] Make the plugin work in development mode by adding `openedx-development-settings`. (by @Abdul-Muqadim-Arbisoft)

<a id='changelog-18.0.0'></a>
## v18.0.0 (2024-06-20)

- 💥[Feature] Upgrade to Redwood (by @Abdul-Muqadim-Arbisoft)
- [Improvement] Makefile updated and test added to the repository and formatted code with Black and isort. (by @CodeWithEmad)
- [Bugfix] Make plugin compatible with Python 3.12 by removing dependency on `pkg_resources`. (by @regisb)

<a id='changelog-17.0.0'></a>
## v17.0.0 (2023-12-06)

- 💥[Feature] Upgrade to Quince. (by @mhsiddiqui)

<a id='changelog-16.0.1'></a>
## v16.0.1 (2023-06-29)

- [Feature] Run JupyterHub on Kubernetes. This is an alpha feature. Feedback is welcome! (by @regisb)

<a id='changelog-16.0.0'></a>
## v16.0.0 (2023-06-15)

- 💥[Feature] Upgrade to Palm. (by @regisb)

<a id='changelog-15.0.2'></a>
## v15.0.2 (2023-05-24)

- [Improvement] Upgrade JupyterHub to 4.0.0. This is possible now that [this ltiauthenticator issue](https://github.com/jupyterhub/ltiauthenticator/issues/157) is resolved. (by @regisb)

<a id='changelog-15.0.1'></a>
## v15.0.1 (2023-05-22)

- [Improvement] Add a scriv-compliant changelog. (by @regisb)
- [Feature] upgrade jupyter-xblock to 15.0.3. (by @regisb)


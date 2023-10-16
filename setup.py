import io
import os
from setuptools import setup, find_packages

HERE = os.path.abspath(os.path.dirname(__file__))


def load_readme():
    with io.open(os.path.join(HERE, "README.rst"), "rt", encoding="utf8") as f:
        return f.read()


def load_about():
    about = {}
    with io.open(
        os.path.join(HERE, "tutorjupyter", "__about__.py"),
        "rt",
        encoding="utf-8",
    ) as f:
        exec(f.read(), about)  # pylint: disable=exec-used
    return about


ABOUT = load_about()


setup(
    name="tutor-jupyter",
    version=ABOUT["__package_version__"],
    url="https://github.com/overhangio/tutor-jupyter",
    project_urls={
        "Code": "https://github.com/overhangio/tutor-jupyter",
        "Issue tracker": "https://github.com/overhangio/tutor-jupyter/issues",
    },
    license="AGPLv3",
    author="Overhang.IO",
    maintainer="Edly",
    maintainer_email="mhassan.eeng@gmail.com",
    description="Jupyter Notebook plugin for Tutor",
    long_description=load_readme(),
    packages=find_packages(exclude=["tests*"]),
    include_package_data=True,
    python_requires=">=3.8",
    install_requires=["tutor>=16.0.0,<17.0.0", "tutor-mfe>=16.0.0,<17.0.0"],
    entry_points={
        "tutor.plugin.v1": [
            "jupyter = tutorjupyter.plugin"
        ]
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)

#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

requirements = [
    "ruamel.yaml==0.17.20",
    "prettytable==3.0.0",
    "Jinja2==3.0.3",
    "fire==0.4.0",
]

test_requirements = [
    "pytest>=3",
]

setup(
    author="Gabriel Bacallado",
    author_email="gabriel.bacallado@gmail.com",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    description="Python package to automatically build the AWS Control Tower Manifest given Cloud Formation templates as input.",
    entry_points={
        "console_scripts": [
            "aws_control_tower_manifest_builder=aws_control_tower_manifest_builder.cli:main",
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    keywords="aws_control_tower_manifest_builder",
    name="aws_control_tower_manifest_builder",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/gabrielbac/aws_control_tower_manifest_builder",
    version="0.3.1",
    zip_safe=False,
)

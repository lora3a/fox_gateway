"""Setuptools File."""

from pathlib import Path

from setuptools import setup

setup(
    name="fox_gateway",
    version="0.0.1",
    author="Michele Forese",
    author_email="michele.forese.personal@gmail.com",
    description="This is a simple Fox Gateway for the H10.",
    long_description=Path("README.md").read_text(),
    license="GPL-3",
    packages=["gateway"],
    install_requires=Path("requirements.txt").read_text().splitlines(),
    entry_points={"console_scripts": ["gateway=gateway:cli"]},
)

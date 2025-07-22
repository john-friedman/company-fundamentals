from setuptools import setup, find_packages

with open("readme.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="company-fundamentals",
    version="0.0.1",
    description="A package to standardize XBRL into fundamentals data",
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT"
)
from setuptools import setup, find_packages

with open("README.md") as f:
    readme = f.read()

setup(
    name="computor",
    version="0.2",
    description=readme,
    author="mgena",
    author_email="mgena@student.42.fr",
    url="https://github.com/kosyan62/computor",
    license="MIT",
    packages=find_packages(),
    entry_points={"console_scripts": ["computor=computor:main"]},
)

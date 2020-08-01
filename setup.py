import pathlib

from setuptools import setup, find_packages

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / "README.md").read_text(encoding="utf-8")

# Load requirements.
with open("requirements.txt") as f:
    required = f.read().splitlines()


setup(
    name="bluff",
    version="1.0.0",
    description="A Pythonic Poker framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/matheusccouto/bluff",
    author="Matheus Couto",
    author_email="matheusccouto@gmail.com",
    keywords="poker",
    package_dir={"": "bluff"},
    packages=find_packages(where="bluff"),
    python_requires=">=3.6",
    install_requires=required,
    include_package_data=True,
)

from setuptools import find_packages, setup

setup(
    name="alchemyst",
    packages=find_packages(where="."),
    include_package_data=True,
    package_dir={"": "."},
)

from setuptools import setup, find_packages

setup(
    name="Ghostbuster", 
    version="1.0", 
    packages=find_packages(), 
    install_requires=open("requirements.txt", "r", encoding="utf-8").read().splitlines(),
    include_package_data=True,
)

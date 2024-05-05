from setuptools import setup

setup(
    name="Ghostbuster", 
    version="1.0", 
    install_requires=open("requirements.txt", "r", encoding="utf-8").read().splitlines(),
    packages=['ghostbuster','ghostbuster.utils', 'ghostbuster.model'],
    package_data={'ghostbuster.model': ['*']},
    include_package_data=True,
)

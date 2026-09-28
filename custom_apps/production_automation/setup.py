from setuptools import setup, find_packages

with open("requirements.txt") as f:
    install_requires = f.read().strip().split("\n")

setup(
    name="production_automation",
    version="0.0.1",
    description="Custom production flow automation",
    author="Pavindhiran",
    author_email="you@example.com",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=install_requires,
)
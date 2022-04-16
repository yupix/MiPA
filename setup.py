import pathlib

from setuptools import setup

description = "A Python wrapper for the Misskey API"
readme_file = pathlib.Path(__file__).parent / "README.md"
with readme_file.open(encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as f:
    requirements = f.read().splitlines()





extras_require = {
    'dev': [
        'pysen[lint]'
    ]
}

packages = [
    'mipac',
    'mipac.abc',
    'mipac.actions',
    'mipac.core',
    'mipac.core.models',
    'mipac.manager',
    'mipac.manager.admin',
    'mipac.models',
    'mipac.types'

]

setup(
    name="mipac",
    version="0.0.1",
    install_requires=requirements,
    url="https://github.com/yupix/mi.py",
    author="yupix",
    author_email="yupi0982@outlook.jp",
    license="MIT",
    python_requires=">=3.10, <4.0",
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=packages,
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python :: 3.10",
        "Natural Language :: Japanese",
        "License :: OSI Approved :: MIT License",
    ],
    extras_require=extras_require,
)

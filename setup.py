import pathlib

from setuptools import setup
import versioneer

description = 'Python Misskey Bot Framework'
readme_file = pathlib.Path(__file__).parent / 'README.md'
with readme_file.open(encoding='utf-8') as fh:
    long_description = fh.read()

with open('requirements.txt', 'r') as f:
    requirements = f.read().splitlines()

extras_require = {
    'dev': ['ruff', 'isort', 'mypy', 'flake8'],
    'ci': ['flake8', 'mypy'],
}

packages = ['mipa', 'mipa.ext', 'mipa.ext.commands', 'mipa.ext.tasks', 'mipa.ext.timelines']

setup(
    name='mipa',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    install_requires=requirements,
    url='https://github.com/yupix/MiPA',
    author='yupix',
    author_email='yupi0982@outlook.jp',
    license='MIT',
    python_requires='>=3.12, <4.0',
    description=description,
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=packages,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python :: 3.12',
        'Natural Language :: Japanese',
        'License :: OSI Approved :: MIT License',
    ],
    extras_require=extras_require,
)

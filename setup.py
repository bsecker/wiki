from setuptools import setup, find_packages

# read the contents of your README file
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="seckerwiki",
    version="0.1.1",
    packages=find_packages(),
    author="Benjamin Secker",
    author_email="Benjamin.secker@gmail.com",
    description="Markdown wiki CLI and scripts",
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords="Markdown,wiki,scripts,cli,mdwiki",
    url="https://github.com/bsecker/wiki",
    license='MIT',
    python_requires=">=3.6",
    install_requires=[
        'PyInquirer',
        'pyyaml',
        'pdf2image==1.5.4',
        'Pillow==6.0.0',
        'requests'
    ],
    entry_points={
        "console_scripts": [
            'wiki = seckerwiki.wiki:main',
        ]
    }
)

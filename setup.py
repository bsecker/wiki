from setuptools import setup, find_packages
setup(
    name="WikiCLI",
    version="0.1",
    packages=find_packages(),
    author="Benjamin Secker",
    author_email="Benjamin.secker@gmail.com",
    description="Markdown wiki CLI and scripts",
    keywords="Markdown,wiki,scripts,cli,mdwiki",
    url="https://github.com/bsecker/wiki",
    scripts=[
        'wiki/wiki.py',
    ],
    python_requires=">=3.6",
    install_requires=[
        'PyInquirer',
        'pyyaml',
        'pdf2image==1.5.4',
        'Pillow==6.0.0',
        'requests'
    ]
)
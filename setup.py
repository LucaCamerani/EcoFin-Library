from setuptools import setup

def parser(path: str):
    with open(path) as f:
        lines = f.read().splitlines()

    return lines

README = open(r"README.md", "r").read()
REQ = parser(r"requirements.txt")

setup(
    name='EcoFin',
    version='1.3',
    packages=['EcoFin', 'EcoFin.math', 'EcoFin.math.stochasticProcess', 'EcoFin.stat',
              'EcoFin.utils', 'EcoFin.equity', 'EcoFin.forward', 'EcoFin.options', 'EcoFin.dataDownload',
              'EcoFin.assetAllocation'],
    url='https://github.com/LucaCamerani/EcoFin-Library',
    license='BSD Open Source License',
    author='Luca Camerani',
    author_email='l.camerani@campus.unimib.it',
    description='EcoFin is a quantitative economic library',
    long_description=README,
    long_description_content_type="text/markdown",
    include_package_data=True,
    install_requires=REQ
)

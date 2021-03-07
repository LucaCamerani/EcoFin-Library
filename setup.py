from setuptools import setup
import requirements

README = open(r"README.md", "r").read()
REQ = []

with open(r"requirements.txt", 'r') as fd:
    for req in requirements.parse(fd):
        REQ.append("{}{}{}".format(req.name, req.specs[0][0], req.specs[0][1]))

setup(
    name='EcoFin',
    version='1.2',
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

import pathlib
from setuptools import setup
import requirements

HERE = pathlib.Path(__file__).parents[1]
README = (HERE / "README.md").read_text()
REQUIREMENTS = (HERE / "requirements.txt")

REQ = []
with open(REQUIREMENTS, 'r') as fd:
    for req in requirements.parse(fd):
        REQ.append("{}{}{}".format(req.name, req.specs[0][0], req.specs[0][1]))

setup(
    name='EcoFin',
    version='1.0.1',
    packages=['math', 'math.stochasticProcess', 'stat',
              'utils', 'equity', 'forward', 'options', 'dataDownload',
              'assetAllocation'],
    url='https://github.com/LucaCamerani/EcoFin-Library',
    license='BSD Open Source License',
    author='Luca Camerani',
    author_email='l.camerani@campus.unimib.it',
    description='EcoFin is a quantitative economic library',
    long_description=README,
    long_description_content_type="text/markdown",
    include_package_data=True,
    requires=REQ
)

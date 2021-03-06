import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

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
    include_package_data=True
)

from setuptools import setup

setup(
    name='EcoFin',
    version='1.0.0',
    packages=['math', 'math.stochasticProcess', 'stat',
              'utils', 'equity', 'forward', 'options', 'dataDownload',
              'assetAllocation'],
    url='https://github.com/LucaCamerani/EcoFin-Library',
    license='BSD Open Source License',
    author='Luca Camerani',
    author_email='l.camerani@campus.unimib.it',
    description='EcoFin is a quantitative economic library'
)

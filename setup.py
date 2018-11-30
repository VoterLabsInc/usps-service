from distutils.core import setup


def readme():
    with open("README.md") as readme:
        return readme.read()


setup(
    name='USPSService',
    version='0.1.0',
    description='A library to make requests to the USPS shipping API',
    long_description=readme(),
    classifiers=[
        'License :: MIT License',
        'Programming Language :: Python 3.6',
    ],
    url='https://github.com/VoterLabsInc/usps-service',
    author='VoterLabsInc',
    author_email='briar.harrison@voterlabs.com',
    license='MIT',
    packages=['usps_service'],
    install_requires=[
        'xmltodict',
        'requests'
    ]
)

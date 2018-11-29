from distutils.core import setup

setup(
    name='USPSService',
    version='0.1.0',
    packages=['usps_service'],
    install_requires=[
    	'xmltodict',
    	'requests'
    ]
)

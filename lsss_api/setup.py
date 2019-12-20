from setuptools import setup



with open("README.md", "r") as fh:
    long_description = fh.read()


#
#    import urllib.request
#    import xmltodict
#    import pandas as pd

setup(name='lsss_api',
      version='1.0',
      description='This package provides functionality for downloading acoustic data from nmd server, and to process data in the lsss software',
      url='https://github.com/sindrevatnehol/lsss_api',
      author='Sindre Vatnehol',
      author_email='sindre.vatnehol@hi.no',
      license='GPL3',
      packages=['NMDdata','API'],
      install_requires=["numpy","requests",'xmltodict','pandas'],
      zip_safe=False)


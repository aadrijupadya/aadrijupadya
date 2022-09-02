from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.1'
DESCRIPTION = 'Cricket sports analytics package'
LONG_DESCRIPTION = 'A novel cricket package specializing in data accessibility and visualization.'

# Setting up
setup(
    name="CricCatapult",
    version=VERSION,
    author="Aadrij Upadya, Pradyum Chitlu",
    author_email="<adrij2005@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['pandas', 'numpy', 'matplotlib',
                      'requests', 'bs4', 'geocoder', 'folium', 'seaborn', 'geopandas', 'pygame', 'ssl'],
    keywords=['python', 'cricket', 'sports analytics',
              'data packaging', 'visualization', 'web scraping'],
    classifiers=[
        "Development Status :: 2 - Production",
        "Intended Audience :: Sports Analysts",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)

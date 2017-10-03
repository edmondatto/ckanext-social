[![PyPI version](https://badge.fury.io/py/ckanext-social.svg)](https://badge.fury.io/py/ckanext-social)
[![GitHub issues](https://img.shields.io/github/issues/codeforafricalabs/ckanext-social.svg?style=flat-square)](https://github.com/codeforafricalabs/ckanext-social/issues)
[![GitHub forks](https://img.shields.io/github/forks/codeforafricalabs/ckanext-social.svg?style=flat-square)](https://github.com/codeforafricalabs/ckanext-social/network)
[![GitHub stars](https://img.shields.io/github/stars/codeforafricalabs/ckanext-social.svg?style=flat-square)](https://github.com/codeforafricalabs/ckanext-social/stargazers)
[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square)](https://raw.githubusercontent.com/codeforafricalabs/ckanext-social/master/LICENSE)
[![Twitter](https://img.shields.io/twitter/url/https/github.com/codeforafricalabs/ckanext-social/.svg?style=social&style=flat-square)](https://twitter.com/intent/tweet?text=Wow:&url=%5Bobject%20Object%5D)
# CKAN social

_An extension to improve social sharing in CKAN._

With the extension installed and activated:

- when a user clicks the social share button, the page title is included in the text that pops up.

<!-- Include with / without photo -->

- includes open graph tags in the head to facilitate the use of summary cards when sharing to social

<!-- Include with / without photo -->


## Requirements
This extension has been tested with versions of CKAN from 2.6.3 onwards
and works well on these versions.


## Installation

Installing this extension in your CKAN instance is as easy as installing any other CKAN extension.

Activate your CKAN virtual environment, for example

`. /usr/local/lib/ckan/default/bin/activate`


#### Option 1: Install the extension using `python setup.py`

```commandline
$ git clone https://github.com/CodeForAfricaLabs/ckanext-social.git
$ cd ckanext-social
$ python setup.py install
```

Modify your configuration file (generally in `/etc/ckan/default/production.ini`) and add `social` in the `ckan.plugins` property.

`ckan.plugins = social <OTHER_PLUGINS>`

#### Option 2: Install the extension using `pip install ckanext-social`
1. Install the ckanext-social Python package into your virtual environment:

     pip install ckanext-social

2. Add ``social`` to the ``ckan.plugins`` setting in your CKAN
   config file (by default the config file is located at
   ``/etc/ckan/default/production.ini``).

3. Restart CKAN. For example if you've deployed CKAN with Apache on Ubuntu:
```commandline
sudo service apache2 reload
```

### Development Installation
To install ckanext-social for development, activate your CKAN virtualenv and
run the following commands
```commandline
git clone https://github.com/edmondatto/ckanext-social.git
cd ckanext-social
python setup.py develop
pip install -r dev-requirements.txt
```
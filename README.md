# CKAN social

_An extension to improve social sharing in CKAN._

With the extension installed and activated:

- when a user clicks the social share button, the page title is included in the text that pops up.

<!-- Include with / without photo -->

- includes open graph tags in the head to facilitate the use of summary cards when sharing to social

<!-- Include with / without photo -->


# Installation

Installing this extension in your CKAN instance is as easy as installing any other CKAN extension.

Activate your virtual environment

`. /usr/local/lib/ckan/default/bin/activate`


## Install the extension

```commandline
$ git clone https://github.com/CodeForAfricaLabs/ckanext-social.git
$ cd ckanext-social
$ python setup.py develop
```

Modify your configuration file (generally in /etc/ckan/default/production.ini) and add social in the ckan.plugins property.

`ckan.plugins = social <OTHER_PLUGINS>`

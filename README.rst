.. You should enable this project on travis-ci.org and coveralls.io to make
   these badges work. The necessary Travis and Coverage config files have been
   generated for you.

.. image:: https://travis-ci.org/jiankaiwang/ckanext-cdcmainlib.svg?branch=master
    :target: https://travis-ci.org/jiankaiwang/ckanext-cdcmainlib

=============
ckanext-cdcmainlib
=============

The extension is the base library for all ckanexts on TCDC open data portal.

------------
Requirements
------------

* Developed on CKAN 2.5.x
* Require external packages
	* psycopg2 : https://pypi.python.org/pypi/psycopg2
	* py2psql : https://github.com/jiankaiwang/seed/blob/master/python/py2psql.py

------------
Installation
------------

To install ckanext-cdcmainlib:

1. Activate your CKAN virtual environment, for example::

     . /usr/lib/ckan/default/bin/activate

2. Clone the ckanext-cdcmainlib from github, for example::
 
     cd /usr/lib/ckan/default/src/

     git clone https://github.com/jiankaiwang/ckanext-cdcmainlib.git

3. Install the ckanext-cdcmainlib Python package into your virtual environment::

     pip install .

4. Add ``cdcmainlib`` to the ``ckan.plugins`` setting in your CKAN
   config file (by default the config file is located at
   ``/etc/ckan/default/production.ini``).

5. Restart CKAN. For example if you've deployed CKAN with Apache on Ubuntu::

     sudo service apache2 reload

   If you've deployed CKAN with uwsgi::

     uwsgi --ini-paste /etc/ckan/default/production.ini

   If you've create a ckan.service::
 
     sudo systemctl restart ckan.service


---------------
Config Settings
---------------

Document any optional config settings here. For example::

    ckan.plugins = cdcmainlib

postgresql database to record downloading information::

    ckan.cdcmainlib.psqlUrl = postgresql://(dbuser):(dbpass)@(dbhost)/(dbname)

------------------------
Development Installation
------------------------

To install ckanext-cdcmainlib for development, activate your CKAN virtualenv and
do::

    git clone https://github.com/jiankaiwang/ckanext-cdcmainlib.git
    cd ckanext-cdcmainlib
    python setup.py develop
    pip install -r dev-requirements.txt


----------------------------------------
Releasing a New Version of ckanext-cdcmainlib
----------------------------------------

1. Update the version number in the ``setup.py`` file.
   See `PEP 440 <http://legacy.python.org/dev/peps/pep-0440/#public-version-identifiers>`_
   for how to choose version numbers.

2. Create a source distribution of the new version::

     python setup.py sdist

3. Upload the source distribution to PyPI::

     python setup.py sdist upload

4. Tag the new release of the project on GitHub with the version number from
   the ``setup.py`` file. For example if the version number in ``setup.py`` is
   0.0.2 then do::

       git tag 0.0.2
       git push --tags

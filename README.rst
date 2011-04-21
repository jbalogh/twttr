Installation
------------

#. Make a virtualenv
#. Get gcc and mysql-devel
#. git clone git://github.com/jbalogh/twttr.git camelot
#. cd camelot
#. pip install -r reqs.txt
#. service mysqld start
#. mysql -u root -p
#. mysql> create database camelot;
#. mysql> grant all on camelot.* to ''@'%';

#. ./manage.py syncdb
#. ./manage.py seed_db
#. while true; do ./manage.py get_users; done

#. ./manage.py run_gunicorn

#
# Regular cron jobs for the django-library package
#
0 4	* * *	root	[ -x /usr/bin/django-library_maintenance ] && /usr/bin/django-library_maintenance

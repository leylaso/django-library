
<VirtualHost *:80>
	ServerAdmin webmaster@##HOSTNAME##
        ServerName ##HOSTNAME##
        ServerAlias www.##HOSTNAME##
	DocumentRoot ##HTMLPAYLOAD## 
	<Directory ##HTMLPAYLOAD##>
		Options Indexes FollowSymLinks MultiViews
		AllowOverride All
		Order allow,deny
		allow from all
	</Directory>

        Alias /static ##HTMLPAYLOAD##/static
        <Directory ##HTMLPAYLOAD##/static>
                Options Indexes FollowSymLinks MultiViews
                Order allow,deny
                allow from all
        </Directory>

        WSGIScriptAlias / ##HTMLPAYLOAD##/django.wsgi

        ErrorLog error.log

	# Possible values include: debug, info, notice, warn, error, crit,
	# alert, emerg.
	LogLevel warn

	CustomLog access.log combined

</VirtualHost>

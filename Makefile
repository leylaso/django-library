
APACHE2_SITES_AVAILABLE=$(DESTDIR)/etc/apache2/sites-available/
HTML=$(DESTDIR)/var/www/
APACHE2_RESTART=apache2ctl restart
APACHE2_ENABLE_SITE=a2ensite

SITE_NAME=django-library
HTMLPAYLOAD=$(HTML)$(SITE_NAME)

HOSTNAME=local2.bibliodira.org

install: 
	if [ -f "$(APACHE2_SITES_AVAILABLE)$(HOSTNAME)" ]; then \
	  echo "Error: can't recreate the django-library"; exit 2; \
	else \
          cat django-library.apache2 | sed 's|##HTMLPAYLOAD##|$(HTMLPAYLOAD)|' | sed 's|##HOSTNAME##|$(HOSTNAME)|' > $(APACHE2_SITES_AVAILABLE)$(HOSTNAME) ; \
          $(APACHE2_ENABLE_SITE) $(HOSTNAME) ; \
          $(APACHE2_RESTART) ; \
	fi ; 

uninstall: 
	if [ -f "$(APACHE2_SITES_AVAILABLE)$(HOSTNAME)" ]; then \
           rm $(APACHE2_SITES_AVAILABLE)$(HOSTNAME) ; \
        fi ;  
	  

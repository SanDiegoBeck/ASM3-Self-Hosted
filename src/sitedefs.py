# ASM3 site definitions

# The base URL to the ASM installation as seen by the client
BASE_URL = "http://localhost:5000"

# The language to use before a locale has been configured 
# in the database
LOCALE = "en"

# The timezone offset to use before one has been configured
# in the database (+/- server clock offset, NOT UTC)
TIMEZONE = 0

# Where ASM directs log output to, one of:
# stderr  - the standard error stream
# syslog  - the UNIX syslogger (with USER facility)
# ntevent - the Windows event logger
# <file>  - The path to a file to log to
LOG_LOCATION = "syslog"

# Include debug messages when logging - set to False
# to disable debug messages
LOG_DEBUG = True

# Deployment type, wsgi or fcgi
DEPLOYMENT_TYPE = "wsgi"

# URLs for ASM services
URL_NEWS = "http://sheltermanager.com/repo/asm_news.html"
URL_REPORTS = "http://sheltermanager.com/repo/reports.txt"

# Default database info
ASM3_DBTYPE = "MYSQL" # MYSQL, POSTGRESQL, SQLITE
ASM3_DBHOST = "localhost"
ASM3_DBPORT = 3306
ASM3_DBUSERNAME = "root"
ASM3_DBPASSWORD = "root"
ASM3_DBNAME = "asm"

# If you want to maintain compatibility with an ASM2 client
# in the database, update the primarykey table
ASM3_HAS_ASM2_PK_TABLE = False

# The strategy for generating table primary keys. If you have
# ASM3_HAS_ASM2_PK_TABLE it will override this value and set
# it to max as it's the only compatible approach between
# ASM2 and ASM3
#
# max:      Use MAX(ID)+1
# memcache: Store IDs in memcache and use memcache.incr (requires memcache)
# pseq:     Use PostgreSQL sequences (only valid for PostgreSQL database)
ASM3_PK_STRATEGY = "max"

# The storage location for HTTP sessions. If set to "database"
# it will use the database info specified above and create a
# "sessions" table in it. 
# The app can only have a single session store, so it will still 
# use the above database even if MULTIPLE_DATABASES is on below.
SESSION_STORE = "database" # database or memcached

# The host/port that memcached is running on if it is to be used
#MEMCACHED_SERVER = "127.0.0.1:11211"
MEMCACHED_SERVER = ""

# Cache results of the most common, less important queries for
# a short period (60 seconds) to help performance. These queries
# include shelterview animals and main screen links) 
#- requires MEMCACHED_SERVER
CACHE_COMMON_QUERIES = False

# Cache service call responses on the server side according
# to their max-age headers - requires MEMCACHED_SERVER
CACHE_SERVICE_RESPONSES = False

# If EMAIL_ERRORS is set to True, all errors from the site
# are emailed to ADMIN_EMAIL and the user is given a generic
# error page. If set to False, debug information is output.
EMAIL_ERRORS = False
ADMIN_EMAIL = "you@youraddress.com"

# If MINIFY_JS is set to True, minified versions of the javascript
# files will be generated at build/deploy time and the handler
# in html.py will reference them instead
MINIFY_JS = False

# Only allow hotlinks to the animal_image and extra_image
# service calls from this domain (blank for any domain)
IMAGE_HOTLINKING_ONLY_FROM_DOMAIN = ""

# If you have a facebook app for page/wall posting, the id and secret
FACEBOOK_CLIENT_ID = ""
FACEBOOK_CLIENT_SECRET = ""

# Shell commands to use to test if Ghostscript is installed and
# to scale down PDFs if it is available
SCALE_PDF = False
GHOSTSCRIPT_TEST_INSTALLED = "gs -v"
GHOSTSCRIPT_SCALE_PDF = "gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/screen -dNOPAUSE -dQUIET -dBATCH -sOutputFile=%(output)s %(input)s"

# Target for viewing an address on a map, {0} is the address
MAP_LINK = "http://www.openstreetmap.org/search?query={0}"

# Client geocode provider, can be "mapquest", "nominatim" or "google"
GEO_PROVIDER = "nominatim"
GEO_PROVIDER_KEY = ""

# Map provider for rendering maps on the client, can be "osm" or "google"
MAP_PROVIDER = "osm"
OSM_MAP_TILES = "http://{s}.tile.osm.org/{z}/{x}/{y}.png" # (can be switched for cloudmade.com or other OSM slippy tiles)

# Bulk geocode provider for server side geocoding of
# historical data, can be "nominatim" or "cloudmade"
BULK_GEO_PROVIDER = "nominatim"
BULK_GEO_PROVIDER_KEY = ""

# Enable the database field on login and allow login to multiple databases
MULTIPLE_DATABASES = False
MULTIPLE_DATABASES_TYPE = "map"
MULTIPLE_DATABASES_MAP = {
    #"alias": { "dbtype": "MYSQL", "host": "localhost", "port": 3306, "username": "root", "password": "root", "database": "asm" }
}

# Override the html publishDir with a fixed value and forbid
# editing in the UI.
# {alias} will be substituted for the current database alias 
# {database} the current database name
# {username} the current database username.
# MULTIPLE_DATABASES_PUBLISH_DIR = "/home/somewhere/{alias}"
MULTIPLE_DATABASES_PUBLISH_DIR = ""

# The URL to show in the UI when publish dir is overridden
# MULTIPLE_DATABASES_PUBLISH_URL = "http://yoursite.com/{alias}"
MULTIPLE_DATABASES_PUBLISH_URL = ""

# Override the HTML/FTP upload credentials. Setting this
# turns on FTP upload and hides those configuration fields in the UI
#MULTIPLE_DATABASES_PUBLISH_FTP = { "host": "ftp.host.com", "user": "user", "pass": "pass", "port": 21, "chdir": "/home/{alias}", "passive": True }
MULTIPLE_DATABASES_PUBLISH_FTP = None

# What to do when a user requests database dumps in various
# formats. Leave blank to enable the system to handle it. 
# Set to "disabled" to prevent that item and remove it from the UI
# altogether. Or, use a URL to redirect the user to another location 
# where the dump can be downloaded. Valid tags are:
# {alias} {database} {username} {password} {md5pass}
DUMP_OVERRIDES = {
    "dumpsql": "",
    "dumpsqlnomedia": "",
    "dumpsqlasm2": "",
    "dumpsqlasm2nomedia": ""
}

# If you want a forgotten password link on the login page,
# the URL it should link to
FORGOTTEN_PASSWORD = ""

# Override the SMTP settings and remove the controls from the options screen
# SMTP_SERVER = { "host": "mail.yourdomain.com", "port": 25, "username": "userifauth", "password": "passifauth", "usetls": False }
SMTP_SERVER = None

# CDN script and css references for dependencies
JQUERY_UI_CSS = '<link rel="stylesheet" href="//ajax.googleapis.com/ajax/libs/jqueryui/1.10.3/themes/%(theme)s/jquery-ui.css" type="text/css" media="all" id="jqt" />'
JQUERY_UI_JS = '<script src="//ajax.googleapis.com/ajax/libs/jqueryui/1.10.3/jquery-ui.min.js" type="text/javascript"></script>'
JQUERY_JS = '<script src="//ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js" type="text/javascript"></script>'
JQUERY_MOBILE_CSS = '<link rel="stylesheet" href="//cdnjs.cloudflare.com/ajax/libs/jquery-mobile/1.3.0/jquery.mobile.min.css" />'
JQUERY_MOBILE_JS = '<script src="//cdnjs.cloudflare.com/ajax/libs/jquery-mobile/1.3.0/jquery.mobile.min.js"></script>'
TINYMCE_4_JS = '<script src="//tinymce.cachefly.net/4.0/tinymce.min.js"></script>'
LEAFLET_CSS = '//cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.1/leaflet.css'
LEAFLET_JS = '//cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.1/leaflet.js'

SMCOM_PAYMENT_LINK = ""


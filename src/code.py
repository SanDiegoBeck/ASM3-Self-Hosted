#!/usr/bin/python

import os, sys

# The path to the folder containing the ASM3 modules
PATH = os.path.dirname(os.path.abspath(__file__)) + os.sep

# Put the rest of our modules on the path
sys.path.append(PATH)
sys.path.append(PATH + "locale")

import al
import additional as extadditional
import animal as extanimal
import cache
import configuration
import csvimport as extcsvimport
import db, dbfs, dbupdate
import diary as extdiary
import financial
import html
from i18n import _, translate, ntranslate, get_version, get_display_date_format, get_currency_prefix, get_currency_symbol, get_currency_dp, python2display, subtract_days, subtract_months, first_of_month, last_of_month, monday_of_week, sunday_of_week, first_of_year, last_of_year, now, format_currency, i18nstringsjs
import log as extlog
import lookups as extlookups
import lostfound as extlostfound
import media as extmedia
import medical as extmedical
import mimetypes
import mobile as extmobile
import movement as extmovement
import onlineform as extonlineform
import person as extperson
import publish as extpublish
import reports as extreports
import search as extsearch
import service as extservice
import smcom
import social
import users
import utils
import waitinglist as extwaitinglist
import web
import wordprocessor
from sitedefs import BASE_URL, DEPLOYMENT_TYPE, DUMP_OVERRIDES, FORGOTTEN_PASSWORD, LOCALE, FACEBOOK_CLIENT_ID, GEO_PROVIDER, GEO_PROVIDER_KEY, LEAFLET_CSS, LEAFLET_JS, MULTIPLE_DATABASES, MULTIPLE_DATABASES_TYPE, MULTIPLE_DATABASES_PUBLISH_URL, MULTIPLE_DATABASES_PUBLISH_FTP, ADMIN_EMAIL, EMAIL_ERRORS, MAP_LINK, MAP_PROVIDER, OSM_MAP_TILES, SESSION_STORE, SMTP_SERVER, SMCOM_PAYMENT_LINK

# URL to class mappings
urls = (
    "/", "index",
    "/accounts", "accounts", 
    "/accounts_trx", "accounts_trx", 
    "/additional", "additional",
    "/animal", "animal",
    "/animal_costs", "animal_costs", 
    "/animal_diary", "animal_diary", 
    "/animal_diet", "animal_diet", 
    "/animal_donations", "animal_donations",
    "/animal_embed", "animal_embed",
    "/animal_facebook", "animal_facebook",
    "/animal_find", "animal_find",
    "/animal_find_results", "animal_find_results",
    "/animal_log", "animal_log",
    "/animal_media", "animal_media",
    "/animal_medical", "animal_medical",
    "/animal_movements", "animal_movements",
    "/animal_new", "animal_new",
    "/animal_test", "animal_test",
    "/animal_vaccination", "animal_vaccination", 
    "/change_password", "change_password",
    "/change_user_settings", "change_user_settings",
    "/config.js", "configjs",
    "/css", "css",
    "/csvimport", "csvimport",
    "/database", "database",
    "/diary_edit", "diary_edit",
    "/diary_edit_my", "diary_edit_my",
    "/diarytask", "diarytask",
    "/diarytasks", "diarytasks",
    "/document_gen", "document_gen",
    "/document_edit", "document_edit",
    "/document_media_edit", "document_media_edit",
    "/document_repository", "document_repository",
    "/document_templates", "document_templates",
    "/donation", "donation",
    "/donation_receive", "donation_receive",
    "/foundanimal", "foundanimal",
    "/foundanimal_diary", "foundanimal_diary",
    "/foundanimal_find", "foundanimal_find",
    "/foundanimal_find_results", "foundanimal_find_results",
    "/foundanimal_log", "foundanimal_log",
    "/foundanimal_media", "foundanimal_media",
    "/foundanimal_new", "foundanimal_new",
    "/giftaid_hmrc_spreadsheet", "giftaid_hmrc_spreadsheet",
    "/htmltemplates", "htmltemplates",
    "/i18n.js", "i18njs",
    "/js", "js",
    "/image", "image",
    "/litters", "litters", 
    "/log_new", "log_new",
    "/lookups", "lookups",
    "/lostanimal", "lostanimal",
    "/lostanimal_find", "lostanimal_find",
    "/lostanimal_find_results", "lostanimal_find_results",
    "/lostanimal_diary", "lostanimal_diary",
    "/lostanimal_log", "lostanimal_log",
    "/lostfound_match", "lostfound_match", 
    "/lostanimal_media", "lostanimal_media",
    "/lostanimal_new", "lostanimal_new",
    "/mailmerge", "mailmerge",
    "/media", "media",
    "/medicalprofile", "medicalprofile",
    "/mobile", "mobile",
    "/move_adopt", "move_adopt",
    "/move_book_foster", "move_book_foster",
    "/move_book_reservation", "move_book_reservation",
    "/move_book_retailer", "move_book_retailer",
    "/move_book_recent_adoption", "move_book_recent_adoption",
    "/move_book_recent_other", "move_book_recent_other",
    "/move_book_recent_transfer", "move_book_recent_transfer",
    "/move_book_trial_adoption", "move_book_trial_adoption",
    "/move_book_unneutered", "move_book_unneutered",
    "/move_deceased", "move_deceased",
    "/move_foster", "move_foster",
    "/move_reserve", "move_reserve",
    "/move_retailer", "move_retailer",
    "/move_transfer", "move_transfer",
    "/mobile_login", "mobile_login",
    "/mobile_logout", "mobile_logout",
    "/mobile_post", "mobile_post",
    "/mobile_report", "mobile_report",
    "/main", "main",
    "/login", "login",
    "/login_splash", "login_splash",
    "/logout", "logout",
    "/medical", "medical",
    "/onlineform", "onlineform",
    "/onlineform_incoming", "onlineform_incoming",
    "/onlineforms", "onlineforms",
    "/options", "options",
    "/person", "person",
    "/person_diary", "person_diary",
    "/person_donations", "person_donations",
    "/person_embed", "person_embed",
    "/person_find", "person_find",
    "/person_find_results", "person_find_results",
    "/person_investigation", "person_investigation",
    "/person_links", "person_links",
    "/person_log", "person_log",
    "/person_lookingfor", "person_lookingfor",
    "/person_media", "person_media",
    "/person_movements", "person_movements",
    "/person_new", "person_new",
    "/person_vouchers", "person_vouchers",
    "/publish", "publish",
    "/publish_logs", "publish_logs",
    "/publish_options", "publish_options",
    "/report", "report",
    "/report_images", "report_images",
    "/reports", "reports",
    "/roles", "roles",
    "/search", "search",
    "/service", "service",
    "/shelterview", "shelterview",
    "/spellcheck", "spellcheck",
    "/sql", "sql",
    "/systemusers", "systemusers",
    "/test", "test",
    "/vaccination", "vaccination",
    "/waitinglist", "waitinglist",
    "/waitinglist_diary", "waitinglist_diary",
    "/waitinglist_log", "waitinglist_log",
    "/waitinglist_media", "waitinglist_media",
    "/waitinglist_new", "waitinglist_new",
    "/waitinglist_results", "waitinglist_results",
    "/welcome", "welcome"
)

class MemCacheStore(web.session.Store):
    """ 
    A session manager that uses the local memcache install
    If anything goes wrong reading or writing a value, the client
    reconnects so as not to leave the store in a broken state.
    """
    def __contains__(self, key):
        return cache.get(key) is not None
    def __getitem__(self, key):
        return cache.get(key)
    def __setitem__(self, key, value):
        return cache.put(key, value, web.config.session_parameters["timeout"])
    def __delitem__(self, key):
        cache.delete(key)
    def cleanup(self, timeout):
        pass # Not needed, we assign values to memcache with timeout

def remote_ip():
    """
    Gets the IP address of the requester, taking account of
    reverse proxies
    """
    remoteip = web.ctx['ip']
    if web.ctx.env.has_key("HTTP_X_FORWARDED_FOR"):
        xf = web.ctx.env["HTTP_X_FORWARDED_FOR"]
        if xf is not None and str(xf).strip() != "":
            remoteip = xf
    return remoteip

def session_manager():
    """
    Sort out our session manager. We use a global in the utils module
    to hold the session to make sure if the app is reloaded it
    always gets the same session manager.
    """
    # Set session parameters, 24 hour timeout
    web.config.session_parameters["cookie_name"] = "asm_session_id"
    web.config.session_parameters["cookie_path"] = "/"
    web.config.session_parameters["timeout"] = 3600 * 24
    web.config.session_parameters["ignore_expiry"] = True
    web.config.session_parameters["ignore_change_ip"] = True
    sess = None
    if utils.websession is None:
        # Disable noisy logging from session db
        web.config.debug_sql = False
        if SESSION_STORE == "memcached":
            store = MemCacheStore()
        else:
            # Otherwise we're using the main database for session storage
            dbs = db.DatabaseInfo()
            dbn = dbs.dbtype.lower()
            if dbn == "postgresql": dbn = "postgres"
            if dbn == "mysql" or dbn == "postgres":
                if dbs.password != "":
                    wdb = web.database(dbn=dbn, host=dbs.host, port=dbs.port, db=dbs.database, user=dbs.username, pw=dbs.password)
                else:
                    wdb = web.database(dbn=dbn, host=dbs.host, port=dbs.port, db=dbs.database, user=dbs.username)
            elif dbn == "sqlite":
                wdb = web.database(dbn=dbn, db=dbs.database)
            try:
                wdb.printing = False
                wdb.query("create table sessions (" \
                    "session_id char(128) UNIQUE NOT NULL," \
                    "atime timestamp NOT NULL default current_timestamp," \
                    "data text)")
            except:
                pass
            store = web.session.DBStore(wdb, 'sessions')
        sess = web.session.Session(app, store, initializer={"user" : None, "dbo" : None, "locale" : None, "searches" : [] })
        utils.websession = sess
    else:
        sess = utils.websession
    return sess

def asm_404():
    """
    Custom 404 page
    """
    s = """
        <html>
        <head>
        <title>404</title>
        </head>
        <body style="background-color: #999">
        <div style="position: absolute; left: 20%; width: 60%; padding: 20px; background-color: white">

        <img src="static/images/logo/icon-64.png" align="right" />
        <h2>Error 404</h2>

        <p>Sorry, but the record you tried to access was not found.</p>

        <p><a href="javascript:history.back()">Go Back</a></p>

        </div>
        </body>
        </html>
    """
    return web.notfound(s)

def asm_500_email():
    """
    Custom 500 error page that sends emails to the site admin
    """
    web.emailerrors(ADMIN_EMAIL, web.webapi._InternalError)()
    s = """
        <html>
        <head>
        <title>500</title>
        </head>
        <body style="background-color: #999">
        <div style="position: absolute; left: 20%; width: 60%; padding: 20px; background-color: white">

        <img src="static/images/logo/icon-64.png" align="right" />
        <h2>Error 500</h2>

        <p>An error occurred trying to process your request.</p>

        <p>The system administrator has been notified to fix the problem.</p>

        <p>Sometimes, a database update needs to have been run. Return
        to the <a href="main">main screen</a> to run any outstanding
        database updates.</p>

        <p><a href="javascript:history.back()">Go Back</a></p>

        </div>
        </body>
        </html>
    """
    return web.internalerror(s)

# Setup the WSGI application object and session with mappings
app = web.application(urls, globals())
app.notfound = asm_404
if EMAIL_ERRORS:
    app.internalerror = asm_500_email
session = session_manager()

# Choose startup mode
if DEPLOYMENT_TYPE == "wsgi":
    application = app.wsgifunc()
elif DEPLOYMENT_TYPE == "fcgi":
    web.wsgi.runwsgi = lambda func, addr=None: web.wsgi.runfcgi(func, addr)
    web.runwsgi = web.runfcgi

class index:
    def GET(self):
        # If there's no database structure, create it before 
        # redirecting to the login page.
        if not MULTIPLE_DATABASES:
            dbo = db.DatabaseInfo()
            if not db.has_structure(dbo):
                raise web.seeother("/database")
        raise web.seeother("/main")

class database:
    def GET(self):
        dbo = db.DatabaseInfo()
        if MULTIPLE_DATABASES:
            if smcom.active():
                raise utils.ASMPermissionError("N/A for sm.com")
            else:
                # We can't create the database as we have multiple, so
                # output the SQL creation script with default data
                # for whatever our dbtype is instead
                s = "-- Creation script for %s\n\n" % dbo.dbtype
                s += dbupdate.sql_structure(dbo)
                s += dbupdate.sql_default_data(dbo).replace("|=", ";")
                web.header("Content-Type", "text/plain")
                web.header("Content-Disposition", "attachment; filename=\"setup.sql\"")
                return s
        if db.has_structure(dbo):
            raise utils.ASMPermissionError("Database already created")
        s = html.bare_header("Create your database")
        s += """
            <h2>Create your new ASM database</h2>
            <form id="cdbf" method="post" action="database">
            <p>Please select your locale: 
            <select name="locale" class="asm-selectbox">
            %s
            </select>
            </p>
            <button id="createdb">Create Database</button>
            <div id="info" class="ui-state-highlight ui-corner-all" style="margin-top: 20px; padding: 0 .7em; display: none">
            <p><span class="ui-icon ui-icon-info" style="float: left; margin-right: .3em;"></span>
            Please be patient, this can take upto a few minutes.
            </p>
            </div>
            </form>
            <script type="text/javascript">
            $("#createdb").button().click(function() {
                $("#createdb").button("disable");
                $("#info").fadeIn();
                $("#cdbf").submit();
            });
            </script>
            """ % html.options_locales()
        s += html.footer()
        web.header("Content-Type", "text/html")
        return s

    def POST(self):
        post = utils.PostedData(web.input(locale = LOCALE), LOCALE)
        dbo = db.DatabaseInfo()
        dbo.locale = post["locale"]
        dbo.installpath = PATH
        dbupdate.install(dbo)
        raise web.seeother("/login")

class image:
    def GET(self):
        utils.check_loggedin(session, web)
        post = utils.PostedData(web.input(mode = "animal", id = "0", seq = -1), session.locale)
        try:
            lastmod, imagedata = extmedia.get_image_file_data(session.dbo, post["mode"], post["id"], post.integer("seq"), False)
        except Exception,err:
            al.error("%s" % str(err), "code.image", session.dbo)
            return ""
        if imagedata != "NOPIC":
            web.header("Content-Type", "image/jpeg")
            web.header("Cache-Control", "max-age=86400")
            return imagedata
        else:
            web.header("Content-Type", "image/jpeg")
            web.header("Cache-Control", "no-cache")
            raise web.seeother("image?mode=dbfs&id=/reports/nopic.jpg")

class configjs:
    def GET(self):
        # db is the database name and ts is the date/time the config was
        # last read upto. The ts value (config_ts) is set during login and
        # updated whenever the user posts to publish_options or options.
        # Both values are used purely to cache the config in the browser, but
        # aren't actually used by the controller here.
        # data = web.input(db = "", ts = "")
        if utils.is_loggedin(session) and session.dbo is not None:
            dbo = session.dbo
            web.header("Content-Type", "text/javascript")
            web.header("Cache-Control", "max-age=86400")
            realname = ""
            emailaddress = ""
            expirydate = ""
            expirydatedisplay = ""
            if smcom.active():
                expirydate = smcom.get_expiry_date(dbo)
                if expirydate is not None: 
                    expirydatedisplay = python2display(session.locale, expirydate)
                    expirydate = expirydate.isoformat()
            us = users.get_users(dbo, session.user)
            if len(us) > 0:
                emailaddress = utils.nulltostr(us[0]["EMAILADDRESS"])
                realname = utils.nulltostr(us[0]["REALNAME"])
            s = "asm={baseurl:'%s'," % BASE_URL
            s += "locale:'%s'," % session.locale
            s += "theme:'%s'," % session.theme
            s += "user:'%s'," % session.user.replace("'", "\\'")
            s += "useremail:'%s'," % emailaddress
            s += "userreal:'%s'," % realname.replace("'", "\\'")
            s += "useraccount:'%s'," % dbo.database
            s += "useraccountalias: '%s'," % dbo.alias
            s += "dateformat:'%s'," % get_display_date_format(session.locale)
            s += "currencysymbol:'%s'," % get_currency_symbol(session.locale)
            s += "currencydp:%d," % get_currency_dp(session.locale)
            s += "currencyprefix:'%s'," % get_currency_prefix(session.locale)
            s += "securitymap:'%s'," % session.securitymap
            s += "superuser:%s," % (session.superuser and "true" or "false")
            s += "locationfilter:'%s'," % session.locationfilter
            s += "roles:'%s'," % (session.roles.replace("'", "\\'"))
            s += "roleids:'%s'," % (session.roleids)
            s += "smcom:%s," % (smcom.active() and "true" or "false")
            s += "smcomexpiry:'%s'," % expirydate
            s += "smcomexpirydisplay:'%s'," % expirydatedisplay
            s += "smcompaymentlink:'%s'," % (SMCOM_PAYMENT_LINK.replace("{alias}", dbo.alias).replace("{database}", dbo.database))
            s += "geoprovider:'%s'," % (GEO_PROVIDER)
            s += "geoproviderkey:'%s'," % (GEO_PROVIDER_KEY)
            s += "leafletcss:'%s'," % (LEAFLET_CSS)
            s += "leafletjs:'%s'," % (LEAFLET_JS)
            s += "maplink:'%s'," % (MAP_LINK)
            s += "mapprovider:'%s'," % (MAP_PROVIDER)
            s += "osmmaptiles:'%s'," % (OSM_MAP_TILES)
            s += "hascustomlogo:%s," % (dbfs.file_exists(dbo, "logo.jpg") and "true" or "false")
            s += "config:" + html.json([configuration.get_map(dbo),]) + ", "
            s += "menustructure:" + html.json_menu(session.locale, 
                extreports.get_reports_menu(dbo, session.roleids, session.superuser), 
                extreports.get_mailmerges_menu(dbo, session.roleids, session.superuser))
            s += "};"
            return s
        else:
            # Not logged in
            web.header("Content-Type", "text/javascript")
            web.header("Cache-Control", "no-cache")
            return ""

class css:
    def GET(self):
        post = utils.PostedData(web.input(v = "", k = ""), LOCALE) # k is ignored here, but versions css within browser cache
        v = post["v"]
        csspath = PATH + "static/css/" + v
        if v.find("..") != -1: raise web.notfound() # prevent escaping our PATH
        if not os.path.exists(csspath): raise web.notfound()
        if v == "": raise web.notfound()
        f = open(csspath, "r")
        content = f.read()
        f.close()
        web.header("Content-Type", "text/css")
        web.header("Cache-Control", "max-age=8640000") # Don't refresh this version for 100 days
        return content

class i18njs:
    def GET(self):
        post = utils.PostedData(web.input(l = LOCALE, k = ""), LOCALE) # k is ignored here, but versions locale within cache
        l = post["l"]
        web.header("Content-Type", "text/javascript")
        web.header("Cache-Control", "max-age=8640000")
        return i18nstringsjs(l)

class js:
    def GET(self):
        post = utils.PostedData(web.input(v = "", k = ""), LOCALE) # k is ignored here, but versions js within browser cache
        v = post["v"]
        jspath = PATH + "static/js/" + v
        if v.find("..") != -1: raise web.notfound() # prevent escaping our PATH
        if not os.path.exists(jspath): raise web.notfound()
        if v == "": raise web.notfound()
        f = open(jspath, "r")
        content = f.read()
        f.close()
        web.header("Content-Type", "text/javascript")
        web.header("Cache-Control", "max-age=8640000") # Don't refresh this version for 100 days
        return content

class media:
    def GET(self):
        utils.check_loggedin(session, web)
        post = utils.PostedData(web.input(id = "0"), LOCALE)
        lastmod, medianame, mimetype, filedata = extmedia.get_media_file_data(session.dbo, post.integer("id"))
        web.header("Content-Type", mimetype)
        web.header("Cache-Control", "max-age=86400")
        web.header("Content-Disposition", "inline; filename=\"%s\"" % medianame)
        return filedata

class mobile:
    def GET(self):
        utils.check_loggedin(session, web, "/mobile_login")
        web.header("Content-Type", "text/html")
        return extmobile.page(session.dbo, session, session.user)

class mobile_login:
    def GET(self):
        l = LOCALE
        if not MULTIPLE_DATABASES:
            dbo = db.DatabaseInfo()
            l = configuration.locale(dbo)
        web.header("Content-Type", "text/html")
        return extmobile.page_login(l)

    def POST(self):
        post = utils.PostedData(web.input( database="", username="", password="" ), LOCALE)
        raise web.seeother( extmobile.login(post, session, remote_ip(), PATH) )

class mobile_logout:
    def GET(self):
        users.logout(session.dbo, session.user)
        session.user = None
        raise web.seeother("mobile_login")

class mobile_post:
    def handle(self):
        utils.check_loggedin(session, web, "/mobile_login")
        post = utils.PostedData(web.input(posttype = "", id = "0", animalid = "0", medicalid = "0", logtypeid = "0", logtext = "", filechooser = {}, success = ""), session.locale)
        s = extmobile.handler(session.dbo, session.user, post)
        if s is None:
            raise utils.ASMValidationError("mobile handler failed.")
        elif s.startswith("GO "):
            raise web.seeother(s[3:])
        else:
            web.header("Content-Type", "text/html")
            return s
    def GET(self):
        return self.handle()
    def POST(self):
        return self.handle()

class mobile_report:
    def GET(self):
        utils.check_loggedin(session, web, "/mobile_login")
        post = utils.PostedData(web.input(id = "0"), session.locale)
        crid = post.integer("id")
        web.header("Content-Type", "text/html")
        return extmobile.report(session.dbo, crid, session.user)

class main:
    def GET(self):
        utils.check_loggedin(session, web)
        l = session.locale
        dbo = session.dbo
        title = _("Animal Shelter Manager", l)
        title += " - " + configuration.organisation(dbo)
        # Do we need to request a password change?
        if session.passchange:
            raise web.seeother("/change_password?suggest=1")
        s = html.header(title, session, "main.js")
        # Database update checks
        dbmessage = ""
        if dbupdate.check_for_updates(dbo):
            newversion = dbupdate.perform_updates(dbo)
            if newversion != "":
                dbmessage = _("Updated database to version {0}", l).format(str(newversion))
                session.configuration = configuration.get_map(dbo)
        if dbupdate.check_for_view_seq_changes(dbo):
            dbupdate.install_db_views(dbo)
            dbupdate.install_db_sequences(dbo)
        # News
        news = dbfs.get_asm_news(dbo)
        # Welcome dialog
        showwelcome = False
        if configuration.show_first_time_screen(dbo) and session.superuser == 1:
            showwelcome = True
        # Messages
        mess = extlookups.get_messages(dbo, session.user, session.roles, session.superuser)
        # Animal links
        linkmode = configuration.main_screen_animal_link_mode(dbo)
        linkmax = configuration.main_screen_animal_link_max(dbo)
        animallinks = []
        linkname = ""
        if linkmode == "recentlychanged":
            linkname = _("Recently Changed", l)
            animallinks = extanimal.get_links_recently_changed(dbo, linkmax, session.locationfilter)
        elif linkmode == "recentlyentered":
            linkname = _("Recently Entered Shelter", l)
            animallinks = extanimal.get_links_recently_entered(dbo, linkmax, session.locationfilter)
        elif linkmode == "recentlyadopted":
            linkname = _("Recently Adopted", l)
            animallinks = extanimal.get_links_recently_adopted(dbo, linkmax, session.locationfilter)
        elif linkmode == "recentlyfostered":
            linkname = _("Recently Fostered", l)
            animallinks = extanimal.get_links_recently_fostered(dbo, linkmax, session.locationfilter)
        elif linkmode == "longestonshelter":
            linkname = _("Longest On Shelter", l)
            animallinks = extanimal.get_links_longest_on_shelter(dbo, linkmax, session.locationfilter)
        elif linkmode == "adoptable":
            linkname = _("Up for adoption", l)
            pc = extpublish.PublishCriteria(configuration.publisher_presets(dbo))
            pc.limit = linkmax
            animallinks = extpublish.get_animal_data(dbo, pc)
        # Users and roles, active users
        usersandroles = users.get_users_and_roles(dbo)
        activeusers = users.get_activeusers(dbo)
        # Alerts
        alerts = extanimal.get_alerts(dbo, session.locationfilter)
        if len(alerts) > 0: alerts[0]["LOOKFOR"] = configuration.lookingfor_last_match_count(dbo)
        # Diary Notes
        dm = None
        if configuration.all_diary_home_page(dbo): 
            dm = extdiary.get_uncompleted_upto_today(dbo)
        else:
            dm = extdiary.get_uncompleted_upto_today(dbo, session.user)
        # Create controller
        c = html.controller_bool("showwelcome", showwelcome)
        c += html.controller_str("news", news)
        c += html.controller_str("dbmessage", dbmessage)
        c += html.controller_str("version", get_version())
        c += html.controller_str("linkname", linkname)
        c += html.controller_json("usersandroles", usersandroles)
        c += html.controller_json("alerts", alerts)
        c += html.controller_json("stats", extanimal.get_stats(dbo))
        c += html.controller_json("activeusers", activeusers)
        c += html.controller_json("animallinks", extanimal.get_animals_brief(animallinks))
        c += html.controller_json("diary", dm)
        c += html.controller_json("mess", mess)
        s += html.controller(c)
        s += html.footer()
        al.debug("main for '%s', %d diary notes, %d messages" % (session.user, len(dm), len(mess)), "code.main", dbo)
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        post = utils.PostedData(web.input( mode = "", id = 0 ), session.locale)
        dbo = session.dbo
        mode = post["mode"]
        if mode == "addmessage":
            extlookups.add_message(dbo, session.user, post.boolean("email"), post["message"], post["forname"], post.integer("priority"), post.date("expires"))
        elif mode == "delmessage":
            extlookups.delete_message(dbo, post.integer("id"))
        elif mode == "showfirsttimescreen":
            configuration.show_first_time_screen(dbo, True, False)

class login:
    def GET(self):
        l = LOCALE
        has_animals = True
        custom_splash = False
        post = utils.PostedData(web.input(smaccount = "", username = "", password = "", target = "", nologconnection = ""), l)
        # Figure out how to get the default locale and any overridden splash screen
        # Single database
        if not MULTIPLE_DATABASES:
            dbo = db.DatabaseInfo()
            l = configuration.locale(dbo)
            has_animals = extanimal.get_has_animals(dbo)
            custom_splash = dbfs.file_exists(dbo, "splash.jpg")
        # Multiple databases, no account given
        elif MULTIPLE_DATABASES and MULTIPLE_DATABASES_TYPE == "map" and post["smaccount"] == "":
            try:
                dbo = db.DatabaseInfo()
                l = configuration.locale(dbo)
            except:
                l = LOCALE
                pass
        # Multiple databases, account given
        elif MULTIPLE_DATABASES and MULTIPLE_DATABASES_TYPE == "map" and post["smaccount"] != "":
            dbo = db.get_multiple_database_info(post["smaccount"])
            if dbo.database != "FAIL" and dbo.database != "DISABLED":
                custom_splash = dbfs.file_exists(dbo, "splash.jpg")
                l = configuration.locale(dbo)
        # Sheltermanager.com
        elif MULTIPLE_DATABASES and MULTIPLE_DATABASES_TYPE == "smcom" and post["smaccount"] != "":
            dbo = smcom.get_database_info(post["smaccount"])
            if dbo.database != "FAIL" and dbo.database != "DISABLED":
                custom_splash = dbfs.file_exists(dbo, "splash.jpg")
                l = configuration.locale(dbo)
        title = _("Animal Shelter Manager Login", l)
        s = html.bare_header(title, "login.js", locale = l)
        c = html.controller_bool("smcom", smcom.active())
        c += html.controller_bool("multipledatabases", MULTIPLE_DATABASES)
        c += html.controller_str("locale", l)
        c += html.controller_bool("hasanimals", has_animals)
        c += html.controller_bool("customsplash", custom_splash)
        c += html.controller_str("forgottenpassword", FORGOTTEN_PASSWORD)
        c += html.controller_str("smaccount", post["smaccount"])
        c += html.controller_str("husername", post["username"])
        c += html.controller_str("hpassword", post["password"]) 
        c += html.controller_str("nologconnection", post["nologconnection"])
        c += html.controller_str("target", post["target"])
        s += html.controller(c)
        s += "<noscript>" + _("Sorry. ASM will not work without Javascript.", l) + "</noscript>\n"
        s += html.footer()
        web.header("Content-Type", "text/html")
        return s

    def POST(self):
        post = utils.PostedData(web.input( database = "", username = "", password = "", nologconnection = "" ), LOCALE)
        return users.web_login(post, session, remote_ip(), PATH)

class login_splash:
    def GET(self):
        post = utils.PostedData(web.input(smaccount = ""), LOCALE)
        try:
            dbo = db.DatabaseInfo()
            if MULTIPLE_DATABASES:
                if post["smaccount"] != "":
                    if MULTIPLE_DATABASES_TYPE == "smcom":
                        dbo = smcom.get_database_info(post["smaccount"])
                    else:
                        dbo = db.get_multiple_database_info(post["smaccount"])
            web.header("Content-Type", "image/jpeg")
            web.header("Cache-Control", "max-age=86400")
            return dbfs.get_string_filepath(dbo, "/reports/splash.jpg")
        except Exception,err:
            al.error("%s" % str(err), "code.login_splash", session.dbo)
            return ""

class logout:
    def GET(self):
        url = "login"
        if MULTIPLE_DATABASES and session.dbo is not None and session.dbo.alias != None:
            url = "login?smaccount=" + session.dbo.alias
        users.logout(session.dbo, session.user)
        session.user = None
        session.kill()
        raise web.seeother(url)

class accounts:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_ACCOUNT)
        l = session.locale
        dbo = session.dbo
        accounts = financial.get_accounts(dbo)
        al.debug("got %d accounts" % len(accounts), "code.accounts", dbo)
        title = _("Accounts", l)
        s = html.header(title, session, "accounts.js")
        c = html.controller_json("accounttypes", extlookups.get_account_types(dbo))
        c += html.controller_json("donationtypes", extlookups.get_donation_types(dbo))
        c += html.controller_json("roles", users.get_roles(dbo))
        c += html.controller_json("rows", accounts)
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        post = utils.PostedData(web.input(mode="create"), session.locale)
        mode = post.string("mode")
        if mode == "create":
            users.check_permission(session, users.ADD_ACCOUNT)
            return financial.insert_account_from_form(session.dbo, session.user, post)
        elif mode == "update":
            users.check_permission(session, users.CHANGE_ACCOUNT)
            financial.update_account_from_form(session.dbo, session.user, post)
        elif mode == "delete":
            users.check_permission(session, users.DELETE_ACCOUNT)
            for aid in post.integer_list("ids"):
                financial.delete_account(session.dbo, session.user, aid)

class accounts_trx:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_ACCOUNT)
        l = session.locale
        dbo = session.dbo
        post = utils.PostedData(web.input(accountid = 0, fromdate = "", todate = "", recfilter = 0), l)
        defview = configuration.default_account_view_period(dbo)
        fromdate = post["fromdate"]
        todate = post["todate"]
        if fromdate != "" and todate != "":
            fromdate = post.date("fromdate")
            todate = post.date("todate")
        elif defview == financial.THIS_MONTH:
            fromdate = first_of_month(now())
            todate = last_of_month(now())
        elif defview == financial.THIS_WEEK:
            fromdate = monday_of_week(now())
            todate = sunday_of_week(now())
        elif defview == financial.THIS_YEAR:
            fromdate = first_of_year(now())
            todate = last_of_year(now())
        elif defview == financial.LAST_MONTH:
            fromdate = first_of_month(subtract_months(now(), 1))
            todate = last_of_month(subtract_months(now(), 1))
        elif defview == financial.LAST_WEEK:
            fromdate = monday_of_week(subtract_days(now(), 7))
            todate = sunday_of_week(subtract_days(now(), 7))
        transactions = financial.get_transactions(dbo, post.integer("accountid"), fromdate, todate, post.integer("recfilter"))
        accountcode = financial.get_account_code(dbo, post.integer("accountid"))
        accounteditroles = financial.get_account_edit_roles(dbo, post.integer("accountid"))
        title = accountcode
        al.debug("got %d trx for %s <-> %s" % (len(transactions), str(fromdate), str(todate)), "code.accounts_trx", dbo)
        s = html.header(title, session, "accounts_trx.js")
        c = html.controller_json("rows", transactions)
        c += html.controller_json("codes", "|".join(financial.get_account_codes(dbo)))
        c += html.controller_int("accountid", post.integer("accountid"))
        c += html.controller_str("accountcode", accountcode);
        c += html.controller_str("accounteditroles", "|".join(accounteditroles));
        c += html.controller_str("fromdate", python2display(l, fromdate))
        c += html.controller_str("todate", python2display(l, todate))
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        post = utils.PostedData(web.input(mode="create"), session.locale)
        mode = post["mode"]
        if mode == "create":
            users.check_permission(session, users.CHANGE_TRANSACTIONS)
            financial.insert_trx_from_form(session.dbo, session.user, post)
        elif mode == "update":
            users.check_permission(session, users.CHANGE_TRANSACTIONS)
            financial.update_trx_from_form(session.dbo, session.user, post)
        elif mode == "delete":
            users.check_permission(session, users.CHANGE_TRANSACTIONS)
            for tid in post.integer_list("ids"):
                financial.delete_trx(session.dbo, session.user, tid)
        elif mode == "reconcile":
            users.check_permission(session, users.CHANGE_TRANSACTIONS)
            for tid in post.integer_list("ids"):
                financial.mark_reconciled(session.dbo, tid)

class additional:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.MODIFY_LOOKUPS)
        l = session.locale
        dbo = session.dbo
        fields = extadditional.get_fields(dbo)
        title = _("Additional Fields", l)
        al.debug("got %d additional field definitions" % len(fields), "code.additional", dbo)
        s = html.header(title, session, "additional.js")
        c = html.controller_json("rows", fields)
        c += html.controller_json("fieldtypes", extlookups.get_additionalfield_types(dbo))
        c += html.controller_json("linktypes", extlookups.get_additionalfield_links(dbo))
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        post = utils.PostedData(web.input(mode="create"), session.locale)
        mode = post["mode"]
        if mode == "create":
            users.check_permission(session, users.MODIFY_LOOKUPS)
            extadditional.insert_field_from_form(session.dbo, session.user, post)
        elif mode == "update":
            users.check_permission(session, users.MODIFY_LOOKUPS)
            extadditional.update_field_from_form(session.dbo, session.user, post)
        elif mode == "delete":
            users.check_permission(session, users.MODIFY_LOOKUPS)
            for fid in post.integer_list("ids"):
                extadditional.delete_field(session.dbo, session.user, fid)

class animal:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_ANIMAL)
        dbo = session.dbo
        data = web.input(id = 0)
        l = dbo.locale
        a = extanimal.get_animal(dbo, utils.df_ki(data, "id"))
        if a is None: raise web.notfound()
        # If a location filter is set, prevent the user opening this animal if it's
        # not in their location.
        if session.locationfilter != "":
            if str(a["SHELTERLOCATION"]) not in session.locationfilter.split(","):
                raise utils.ASMPermissionError("animal not in location filter")
        al.debug("opened animal %s %s" % (a["CODE"], a["ANIMALNAME"]), "code.animal", dbo)
        title = _("{0} - {1} ({2} {3} aged {4})", l).format(a["ANIMALNAME"], a["CODE"], a["SEXNAME"], a["SPECIESNAME"], a["ANIMALAGE"])
        s = html.header(title, session, "animal.js")
        c = html.controller_json("animal", a)
        c += html.controller_plain("activelitters", html.json_autocomplete_litters(dbo))
        c += html.controller_json("additional", extadditional.get_additional_fields(dbo, a["ID"], "animal"))
        c += html.controller_json("animaltypes", extlookups.get_animal_types(dbo))
        c += html.controller_json("species", extlookups.get_species(dbo))
        c += html.controller_json("breeds", extlookups.get_breeds_by_species(dbo))
        c += html.controller_json("coattypes", extlookups.get_coattypes(dbo))
        c += html.controller_json("colours", extlookups.get_basecolours(dbo))
        c += html.controller_json("deathreasons", extlookups.get_deathreasons(dbo))
        c += html.controller_json("diarytasks", extdiary.get_animal_tasks(dbo))
        c += html.controller_json("entryreasons", extlookups.get_entryreasons(dbo))
        c += html.controller_str("facebookclientid", FACEBOOK_CLIENT_ID)
        c += html.controller_bool("hasfacebook", FACEBOOK_CLIENT_ID != "")
        c += html.controller_json("internallocations", extlookups.get_internal_locations(dbo, session.locationfilter))
        c += html.controller_json("posneg", extlookups.get_posneg(dbo))
        c += html.controller_json("sexes", extlookups.get_sexes(dbo))
        c += html.controller_json("sizes", extlookups.get_sizes(dbo))
        c += html.controller_json("tabcounts", extanimal.get_satellite_counts(dbo, a["ID"])[0])
        c += html.controller_json("templates", dbfs.get_html_templates(dbo))
        c += html.controller_json("ynun", extlookups.get_ynun(dbo))
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        l = session.locale
        dbo = session.dbo
        data = web.input(mode="save")
        mode = utils.df_ks(data, "mode")
        if mode == "save":
            users.check_permission(session, users.CHANGE_ANIMAL)
            extanimal.update_animal_from_form(dbo, data, session.user)
        elif mode == "delete":
            users.check_permission(session, users.DELETE_ANIMAL)
            extanimal.delete_animal(dbo, session.user, utils.df_ki(data, "animalid"))
        elif mode == "gencode":
            animaltypeid = utils.df_ki(data, "animaltypeid")
            datebroughtin = utils.df_kd(data, "datebroughtin", l)
            sheltercode, shortcode, unique, year = extanimal.calc_shelter_code(dbo, animaltypeid, datebroughtin)
            return sheltercode + "||" + shortcode + "||" + str(unique) + "||" + str(year)
        elif mode == "randomname":
            return extanimal.get_random_name(dbo, utils.df_ki(data, "sex"))
        elif mode == "clone":
            users.check_permission(session, users.CLONE_ANIMAL)
            utils.check_locked_db(session)
            nid = extanimal.clone_animal(dbo, session.user, utils.df_ki(data, "animalid"))
            return str(nid)
        elif mode == "webnotes":
            users.check_permission(session, users.CHANGE_MEDIA)
            extanimal.update_preferred_web_media_notes(dbo, session.user, utils.df_ki(data, "id"), utils.df_ks(data, "comments"))

class animal_costs:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_COST)
        dbo = session.dbo
        data = web.input(id = 0)
        a = extanimal.get_animal(dbo, utils.df_ki(data, "id"))
        if a is None: raise web.notfound()
        cost = extanimal.get_costs(dbo, utils.df_ki(data, "id"))
        costtypes = extlookups.get_costtypes(dbo)
        costtotals = extanimal.get_cost_totals(dbo, utils.df_ki(data, "id"))
        title = _("{0} - {1} ({2} {3} aged {4})").format(a["ANIMALNAME"], a["CODE"], a["SEXNAME"], a["SPECIESNAME"], a["ANIMALAGE"])
        al.debug("got %d costs for animal %s %s" % (len(cost), a["CODE"], a["ANIMALNAME"]), "code.animal_costs", dbo)
        s = html.header(title, session, "animal_costs.js")
        c = html.controller_json("rows", cost)
        c += html.controller_json("animal", a)
        c += html.controller_json("costtypes", costtypes)
        c += html.controller_json("costtotals", costtotals)
        c += html.controller_json("tabcounts", extanimal.get_satellite_counts(dbo, a["ID"])[0])
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        dbo = session.dbo
        l = session.locale
        username = session.user
        data = web.input(mode="create")
        mode = utils.df_ks(data, "mode")
        if mode == "create":
            users.check_permission(session, users.ADD_COST)
            return extanimal.insert_cost_from_form(dbo, username, data)
        elif mode == "update":
            users.check_permission(session, users.CHANGE_COST)
            extanimal.update_cost_from_form(dbo, username, data)
        elif mode == "dailyboardingcost":
            users.check_permission(session, users.CHANGE_ANIMAL)
            animalid = utils.df_ki(data, "animalid")
            cost = utils.df_m(data, "dailyboardingcost", l)
            extanimal.update_daily_boarding_cost(dbo, username, animalid, cost)
        elif mode == "delete":
            users.check_permission(session, users.DELETE_COST)
            for cid in utils.df_kl(data, "ids"):
                extanimal.delete_cost(session.dbo, session.user, cid)

class animal_diary:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_DIARY)
        dbo = session.dbo
        data = web.input(id = 0)
        a = extanimal.get_animal(dbo, utils.df_ki(data, "id"))
        if a is None: raise web.notfound()
        diaries = extdiary.get_diaries(dbo, extdiary.ANIMAL, utils.df_ki(data, "id"))
        title = _("{0} - {1} ({2} {3} aged {4})").format(a["ANIMALNAME"], a["CODE"], a["SEXNAME"], a["SPECIESNAME"], a["ANIMALAGE"])
        al.debug("got %d notes for animal %s %s" % (len(diaries), a["CODE"], a["ANIMALNAME"]), "code.animal_diary", dbo)
        s = html.header(title, session, "diary.js")
        c = html.controller_json("rows", diaries)
        c += html.controller_json("animal", a)
        c += html.controller_json("tabcounts", extanimal.get_satellite_counts(dbo, a["ID"])[0])
        c += html.controller_str("name", "animal_diary")
        c += html.controller_int("linkid", a["ID"])
        c += html.controller_json("forlist", users.get_users_and_roles(dbo))
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        data = web.input(mode="create")
        mode = utils.df_ks(data, "mode")
        if mode == "create":
            users.check_permission(session, users.ADD_DIARY)
            return extdiary.insert_diary_from_form(session.dbo, session.user, extdiary.ANIMAL, utils.df_ki(data, "linkid"), data)
        elif mode == "update":
            users.check_permission(session, users.EDIT_ALL_DIARY_NOTES)
            extdiary.update_diary_from_form(session.dbo, session.user, data)
        elif mode == "delete":
            users.check_permission(session, users.DELETE_DIARY)
            for did in utils.df_kl(data, "ids"):
                extdiary.delete_diary(session.dbo, session.user, did)
        elif mode == "complete":
            users.check_permission(session, users.BULK_COMPLETE_NOTES)
            for did in utils.df_kl(data, "ids"):
                extdiary.complete_diary_note(session.dbo, session.user, did)

class animal_diet:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_DIET)
        dbo = session.dbo
        data = web.input(id = 0)
        a = extanimal.get_animal(dbo, utils.df_ki(data, "id"))
        if a is None: raise web.notfound()
        diet = extanimal.get_diets(dbo, utils.df_ki(data, "id"))
        diettypes = extlookups.get_diets(dbo)
        title = _("{0} - {1} ({2} {3} aged {4})").format(a["ANIMALNAME"], a["CODE"], a["SEXNAME"], a["SPECIESNAME"], a["ANIMALAGE"])
        al.debug("got %d diets for animal %s %s" % (len(diet), a["CODE"], a["ANIMALNAME"]), "code.animal_diet", dbo)
        s = html.header(title, session, "animal_diet.js")
        c = html.controller_json("rows", diet)
        c += html.controller_json("animal", a)
        c += html.controller_json("tabcounts", extanimal.get_satellite_counts(dbo, a["ID"])[0])
        c += html.controller_json("diettypes", diettypes)
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        data = web.input(mode="create")
        mode = utils.df_ks(data, "mode")
        if mode == "create":
            users.check_permission(session, users.ADD_DIET)
            return str(extanimal.insert_diet_from_form(session.dbo, session.user, data))
        elif mode == "update":
            users.check_permission(session, users.CHANGE_DIET)
            extanimal.update_diet_from_form(session.dbo, session.user, data)
        elif mode == "delete":
            users.check_permission(session, users.DELETE_DIET)
            for did in utils.df_kl(data, "ids"):
                extanimal.delete_diet(session.dbo, session.user, did)

class animal_donations:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_DONATION)
        l = session.locale
        dbo = session.dbo
        data = web.input(id = 0)
        a = extanimal.get_animal(dbo, utils.df_ki(data, "id"))
        if a is None: raise web.notfound()
        donations = financial.get_animal_donations(dbo, utils.df_ki(data, "id"))
        title = _("{0} - {1} ({2} {3} aged {4})", l).format(a["ANIMALNAME"], a["CODE"], a["SEXNAME"], a["SPECIESNAME"], a["ANIMALAGE"])
        al.debug("got %d donations for animal %s %s" % (len(donations), a["CODE"], a["ANIMALNAME"]), "code.animal_donations", dbo)
        s = html.header(title, session, "donations.js")
        c = html.controller_json("animal", a)
        c += html.controller_json("tabcounts", extanimal.get_satellite_counts(dbo, a["ID"])[0])
        c += html.controller_str("name", "animal_donations")
        c += html.controller_json("donationtypes", extlookups.get_donation_types(dbo))
        c += html.controller_json("paymenttypes", extlookups.get_payment_types(dbo))
        c += html.controller_json("frequencies", extlookups.get_donation_frequencies(dbo))
        c += html.controller_json("templates", dbfs.get_html_templates(dbo))
        c += html.controller_json("rows", donations)
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        data = web.input(mode="create")
        dbo = session.dbo
        mode = utils.df_ks(data, "mode")
        if mode == "create":
            users.check_permission(session, users.ADD_DONATION)
            return financial.insert_donation_from_form(dbo, session.user, data)
        elif mode == "update":
            users.check_permission(session, users.CHANGE_DONATION)
            financial.update_donation_from_form(dbo, session.user, data)
        elif mode == "delete":
            users.check_permission(session, users.DELETE_DONATION)
            for did in utils.df_kl(data, "ids"):
                financial.delete_donation(dbo, session.user, did)
        elif mode == "receive":
            users.check_permission(session, users.CHANGE_DONATION)
            for did in utils.df_kl(data, "ids"):
                financial.receive_donation(dbo, session.user, did)
        elif mode == "personmovements":
            users.check_permission(session, users.VIEW_MOVEMENT)
            web.header("Content-Type", "application/json")
            return html.json(extmovement.get_person_movements(dbo, utils.df_ki(data, "personid")))

class animal_embed:
    def POST(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_ANIMAL)
        dbo = session.dbo
        data = web.input(mode = "find")
        web.header("Content-Type", "application/json")
        mode = utils.df_ks(data, "mode")
        if mode == "find":
            q = utils.df_ks(data, "q")
            rows = extanimal.get_animal_find_simple(dbo, q, utils.df_ks(data, "filter"), 100, False, session.locationfilter)
            al.debug("got %d results for '%s'" % (len(rows), str(web.ctx.query)), "code.animal_embed", dbo)
            return html.json(rows)
        elif mode == "id":
            a = extanimal.get_animal(dbo, utils.df_ki(data, "id"))
            if a is None:
                al.error("get animal by id %d found no records." % (utils.df_ki(data, "id")), "code.animal_embed", dbo)
                raise web.notfound()
            else:
                al.debug("got animal %s %s by id" % (a["CODE"], a["ANIMALNAME"]), "code.animal_embed", dbo)
                return html.json((a,))

class animal_facebook:
    def GET(self):
        """
        This controller is redirected to from Facebook. 
        The link to Facebook is done in animal.js when the Facebook button is pressed.
        
        Facebook include code and state query parameters when redirecting to this controller.
        
        code: a token that we can use in our server side HTTP request to Facebook to get a 
              real access_token from them for the logged in user.
        state: we passed this in the original link to Facebook and it's the 
               ID of the animal we would like to post.
        """
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_ANIMAL)
        data = web.input(code = "", state = "")
        oauth_code = utils.df_ks(data, "code")
        oauth_state = utils.df_ks(data, "state")
        if utils.df_ks(data, "error_reason") != "":
            raise utils.ASMValidationError(utils.df_ks(data, "error_description"))
        # Post the requested animal to facebook
        social.post_animal_facebook(session.dbo, session.user, oauth_code, oauth_state)
        # Redirect back to the animal record and tell the user it worked
        raise web.seeother("animal?facebook=true&id=" + oauth_state[1:])

class animal_find:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_ANIMAL)
        l = session.locale
        dbo = session.dbo
        title = _("Find Animal", l)
        s = html.header(title, session, "animal_find.js")
        c = html.controller_json("agegroups", configuration.age_groups(dbo))
        c += html.controller_json("animaltypes", extlookups.get_animal_types(dbo))
        c += html.controller_json("species", extlookups.get_species(dbo))
        c += html.controller_json("breeds", extlookups.get_breeds_by_species(dbo))
        c += html.controller_json("sexes", extlookups.get_sexes(dbo))
        c += html.controller_json("internallocations", extlookups.get_internal_locations(dbo, session.locationfilter))
        c += html.controller_json("sizes", extlookups.get_sizes(dbo))
        c += html.controller_json("colours", extlookups.get_basecolours(dbo))
        s += html.controller(c)
        al.debug("loaded lookups for find animal", "code.animal_find", dbo)
        s += html.footer()
        web.header("Content-Type", "text/html")
        return s

class animal_find_results:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_ANIMAL)
        dbo = session.dbo
        l = session.locale
        data = web.input(q = "", mode = "")
        q = utils.df_ks(data, "q")
        mode = utils.df_ks(data, "mode")
        if mode == "SIMPLE":
            results = extanimal.get_animal_find_simple(dbo, q, "all", configuration.record_search_limit(dbo), False, session.locationfilter)
        else:
            results = extanimal.get_animal_find_advanced(dbo, data, configuration.record_search_limit(dbo), session.locationfilter)
        add = None
        if len(results) > 0: 
            add = extadditional.get_additional_fields_ids(dbo, results, "animal")
        al.debug("found %d results for %s" % (len(results), str(web.ctx.query)), "code.animal_find_results", dbo)
        wasonshelter = False
        if q == "" and mode == "SIMPLE":
            wasonshelter = True
        s = html.header(_("Results", l), session, "animal_find_results.js")
        c = html.controller_json("rows", results)
        c += html.controller_str("resultsmessage", _("Search returned {0} results.", l).format(len(results)))
        c += html.controller_json("additional", add)
        c += html.controller_bool("wasonshelter", wasonshelter)
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

class animal_log:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_LOG)
        dbo = session.dbo
        data = web.input(id = 0, filter = -2)
        logfilter = utils.df_ki(data, "filter")
        if logfilter == -2: logfilter = configuration.default_log_filter(dbo)
        a = extanimal.get_animal(dbo, utils.df_ki(data, "id"))
        if a is None: raise web.notfound()
        logs = extlog.get_logs(dbo, extlog.ANIMAL, utils.df_ki(data, "id"), logfilter)
        title = _("{0} - {1} ({2} {3} aged {4})").format(a["ANIMALNAME"], a["CODE"], a["SEXNAME"], a["SPECIESNAME"], a["ANIMALAGE"])
        al.debug("got %d logs for animal %s %s" % (len(logs), a["CODE"], a["ANIMALNAME"]), "code.animal_log", dbo)
        s = html.header(title, session, "log.js")
        c = html.controller_str("name", "animal_log")
        c += html.controller_int("linkid", utils.df_ki(data, "id"))
        c += html.controller_int("filter", logfilter)
        c += html.controller_json("rows", logs)
        c += html.controller_json("animal", a)
        c += html.controller_json("tabcounts", extanimal.get_satellite_counts(dbo, a["ID"])[0])
        c += html.controller_json("logtypes", extlookups.get_log_types(dbo))
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        data = web.input(mode="create")
        mode = utils.df_ks(data, "mode")
        if mode == "create":
            users.check_permission(session, users.ADD_LOG)
            return extlog.insert_log_from_form(session.dbo, session.user, extlog.ANIMAL, utils.df_ki(data, "linkid"), data)
        elif mode == "update":
            users.check_permission(session, users.CHANGE_LOG)
            extlog.update_log_from_form(session.dbo, session.user, data)
        elif mode == "delete":
            users.check_permission(session, users.DELETE_LOG)
            for lid in utils.df_kl(data, "ids"):
                extlog.delete_log(session.dbo, session.user, lid)

class animal_media:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_MEDIA)
        dbo = session.dbo
        data = web.input(id = 0, newmedia=0)
        a = extanimal.get_animal(dbo, utils.df_ki(data, "id"))
        if a is None: raise web.notfound()
        m = extmedia.get_media(dbo, extmedia.ANIMAL, utils.df_ki(data, "id"))
        title = _("{0} - {1} ({2} {3} aged {4})").format(a["ANIMALNAME"], a["CODE"], a["SEXNAME"], a["SPECIESNAME"], a["ANIMALAGE"])
        al.debug("got %d media entries for animal %s %s" % (len(m), a["CODE"], a["ANIMALNAME"]), "code.animal_media", dbo)
        s = html.header(title, session, "media.js")
        c = html.controller_json("media", m)
        c += html.controller_json("animal", a)
        c += html.controller_json("tabcounts", extanimal.get_satellite_counts(dbo, a["ID"])[0])
        c += html.controller_bool("showPreferred", True)
        c += html.controller_int("linkid", utils.df_ki(data, "id"))
        c += html.controller_int("linktypeid", extmedia.ANIMAL)
        c += html.controller_str("name", self.__class__.__name__)
        c += html.controller_bool("newmedia", utils.df_ki(data, "newmedia") == 1)
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        data = web.input(mode="create", filechooser={}, linkid="0", base64image = "", _unicode=False)
        mode = utils.df_ks(data, "mode")
        dbo = session.dbo
        l = session.locale
        linkid = utils.df_ki(data, "linkid")
        if mode == "create":
            users.check_permission(session, users.ADD_MEDIA)
            extmedia.attach_file_from_form(session.dbo, session.user, extmedia.ANIMAL, linkid, data)
            raise web.seeother("animal_media?id=%d" % linkid)
        elif mode == "createdoc":
            users.check_permission(session, users.ADD_MEDIA)
            mediaid = extmedia.create_blank_document_media(session.dbo, session.user, extmedia.ANIMAL, linkid)
            raise web.seeother("document_media_edit?id=%d&redirecturl=animal_media?id=%d" % (mediaid, linkid))
        elif mode == "createlink":
            users.check_permission(session, users.ADD_MEDIA)
            mediaid = extmedia.attach_link_from_form(session.dbo, session.user, extmedia.ANIMAL, linkid, data)
            raise web.seeother("animal_media?id=%d" % linkid)
        elif mode == "update":
            users.check_permission(session, users.CHANGE_MEDIA)
            extmedia.update_media_notes(session.dbo, session.user, utils.df_ki(data, "mediaid"), utils.df_ks(data, "comments"))
        elif mode == "delete":
            users.check_permission(session, users.DELETE_MEDIA)
            for mid in utils.df_kl(data, "ids"):
                extmedia.delete_media(session.dbo, session.user, mid)
        elif mode == "email":
            users.check_permission(session, users.MAIL_MERGE)
            emailadd = utils.df_ks(data, "email")
            if emailadd == "" or emailadd.find("@") == -1:
                raise utils.ASMValidationError(_("Invalid email address", l))
            for mid in utils.df_kl(data, "ids"):
                m = extmedia.get_media_by_id(dbo, mid)
                if len(m) == 0: raise web.notfound()
                m = m[0]
                content = dbfs.get_string(dbo, m["MEDIANAME"])
                content = utils.fix_relative_document_uris(content, BASE_URL, MULTIPLE_DATABASES and dbo.database or "")
                utils.send_email(dbo, configuration.email(dbo), emailadd, "", m["MEDIANOTES"], content, "html")
                return emailadd
        elif mode == "rotateclock":
            users.check_permission(session, users.CHANGE_MEDIA)
            for mid in utils.df_kl(data, "ids"):
                extmedia.rotate_media(session.dbo, session.user, mid, True)
        elif mode == "rotateanti":
            users.check_permission(session, users.CHANGE_MEDIA)
            for mid in utils.df_kl(data, "ids"):
                extmedia.rotate_media(session.dbo, session.user, mid, False)
        elif mode == "web":
            users.check_permission(session, users.CHANGE_MEDIA)
            mid = utils.df_kl(data, "ids")[0]
            extmedia.set_web_preferred(session.dbo, session.user, mid)
        elif mode == "video":
            users.check_permission(session, users.CHANGE_MEDIA)
            mid = utils.df_kl(data, "ids")[0]
            extmedia.set_video_preferred(session.dbo, session.user, mid)
        elif mode == "doc":
            users.check_permission(session, users.CHANGE_MEDIA)
            mid = utils.df_kl(data, "ids")[0]
            extmedia.set_doc_preferred(session.dbo, session.user, mid)
        elif mode == "exclude":
            users.check_permission(session, users.CHANGE_MEDIA)
            extmedia.set_excluded(session.dbo, session.user, utils.df_ki(data, "mediaid"), utils.df_ki(data, "exclude"))

class animal_medical:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_MEDICAL)
        dbo = session.dbo
        data = web.input(id = 0)
        a = extanimal.get_animal(dbo, utils.df_ki(data, "id"))
        if a is None: raise web.notfound()
        med = extmedical.get_regimens_treatments(dbo, utils.df_ki(data, "id"))
        profiles = extmedical.get_profiles(dbo)
        title = _("{0} - {1} ({2} {3} aged {4})").format(a["ANIMALNAME"], a["CODE"], a["SEXNAME"], a["SPECIESNAME"], a["ANIMALAGE"])
        al.debug("got %d medical entries for animal %s %s" % (len(med), a["CODE"], a["ANIMALNAME"]), "code.animal_medical", dbo)
        s = html.header(title, session, "medical.js")
        c = html.controller_json("profiles", profiles)
        c += html.controller_json("rows", med)
        c += html.controller_str("name", "animal_medical")
        c += html.controller_json("tabcounts", extanimal.get_satellite_counts(dbo, a["ID"])[0])
        c += html.controller_json("animal", a)
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        data = web.input(mode="create")
        mode = utils.df_ks(data, "mode")
        if mode == "create":
            users.check_permission(session, users.ADD_MEDICAL)
            extmedical.insert_regimen_from_form(session.dbo, session.user, data)
        elif mode == "update":
            users.check_permission(session, users.CHANGE_MEDICAL)
            extmedical.update_regimen_from_form(session.dbo, session.user, data)
        elif mode == "delete_regimen":
            users.check_permission(session, users.DELETE_MEDICAL)
            for mid in utils.df_kl(data, "ids"):
                extmedical.delete_regimen(session.dbo, session.user, mid)
        elif mode == "delete_treatment":
            users.check_permission(session, users.DELETE_MEDICAL)
            for mid in utils.df_kl(data, "ids"):
                extmedical.delete_treatment(session.dbo, session.user, mid)
        elif mode == "get_profile":
            return html.json([extmedical.get_profile(session.dbo, utils.df_ki(data, "profileid"))])
        elif mode == "complete":
            users.check_permission(session, users.BULK_COMPLETE_MEDICAL)
            for mid in utils.df_kl(data, "ids"):
                extmedical.update_treatment_today(session.dbo, session.user, mid)
        elif mode == "given":
            users.check_permission(session, users.BULK_COMPLETE_MEDICAL)
            newdate = utils.df_kd(data, "newdate", session.dbo.locale)
            for mid in utils.df_kl(data, "ids"):
                extmedical.update_treatment_given(session.dbo, session.user, mid, newdate)
        elif mode == "required":
            users.check_permission(session, users.BULK_COMPLETE_MEDICAL)
            newdate = utils.df_kd(data, "newdate", session.dbo.locale)
            for mid in utils.df_kl(data, "ids"):
                extmedical.update_treatment_required(session.dbo, session.user, mid, newdate)

class animal_movements:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_MOVEMENT)
        dbo = session.dbo
        data = web.input(id = 0)
        a = extanimal.get_animal(dbo, utils.df_ki(data, "id"))
        if a is None: raise web.notfound()
        movements = extmovement.get_animal_movements(dbo, utils.df_ki(data, "id"))
        title = _("{0} - {1} ({2} {3} aged {4})").format(a["ANIMALNAME"], a["CODE"], a["SEXNAME"], a["SPECIESNAME"], a["ANIMALAGE"])
        al.debug("got %d movements for animal %s %s" % (len(movements), a["CODE"], a["ANIMALNAME"]), "code.animal_movements", dbo)
        s = html.header(title, session, "movements.js")
        c = html.controller_json("rows", movements)
        c += html.controller_json("animal", a)
        c += html.controller_json("tabcounts", extanimal.get_satellite_counts(dbo, a["ID"])[0])
        c += html.controller_json("movementtypes", extlookups.get_movement_types(dbo))
        c += html.controller_json("returncategories", extlookups.get_entryreasons(dbo))
        c += html.controller_str("name", self.__class__.__name__)
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        data = web.input(mode="create")
        mode = utils.df_ks(data, "mode")
        if mode == "create":
            users.check_permission(session, users.ADD_MOVEMENT)
            return extmovement.insert_movement_from_form(session.dbo, session.user, data)
        elif mode == "update":
            users.check_permission(session, users.CHANGE_MOVEMENT)
            extmovement.update_movement_from_form(session.dbo, session.user, data)
        elif mode == "delete":
            users.check_permission(session, users.DELETE_MOVEMENT)
            for mid in utils.df_kl(data, "ids"):
                extmovement.delete_movement(session.dbo, session.user, mid)
        elif mode == "insurance":
            return extmovement.generate_insurance_number(session.dbo)

class animal_new:
    def GET(self):
        utils.check_loggedin(session, web)
        l = session.locale
        dbo = session.dbo
        title = _("Add a new animal", l)
        s = html.header(title, session, "animal_new.js")
        c = html.controller_plain("autolitters", html.json_autocomplete_litters(dbo))
        c += html.controller_json("animaltypes", extlookups.get_animal_types(dbo))
        c += html.controller_json("species", extlookups.get_species(dbo))
        c += html.controller_json("breeds", extlookups.get_breeds_by_species(dbo))
        c += html.controller_json("colours", extlookups.get_basecolours(dbo))
        c += html.controller_json("sexes", extlookups.get_sexes(dbo))
        c += html.controller_json("internallocations", extlookups.get_internal_locations(dbo, session.locationfilter))
        c += html.controller_json("sizes", extlookups.get_sizes(dbo))
        al.debug("loaded lookups for new animal", "code.animal_new", dbo)
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.ADD_ANIMAL)
        utils.check_locked_db(session)
        data = web.input(mode = "save")
        mode = utils.df_ks(data, "mode")
        if mode == "save":
            animalid, code = extanimal.insert_animal_from_form(session.dbo, data, session.user)
            return str(animalid) + " " + str(code)
        elif mode == "recentnamecheck":
            rows = extanimal.get_recent_with_name(session.dbo, utils.df_ks(data, "animalname"))
            al.debug("recent names found %d rows for '%s'" % (len(rows), utils.df_ks(data, "animalname")), "code.animal_new.recentnamecheck", session.dbo)
            if len(rows) > 0:
                return "|".join((str(rows[0]["ANIMALID"]), rows[0]["SHELTERCODE"], rows[0]["ANIMALNAME"]))

class animal_test:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_TEST)
        l = session.locale
        dbo = session.dbo
        data = web.input(id = 0)
        a = extanimal.get_animal(dbo, utils.df_ki(data, "id"))
        if a is None: raise web.notfound()
        test = extmedical.get_tests(dbo, utils.df_ki(data, "id"))
        al.debug("got %d tests" % len(test), "code.animal_test", dbo)
        title = _("{0} - {1} ({2} {3} aged {4})", l).format(a["ANIMALNAME"], a["CODE"], a["SEXNAME"], a["SPECIESNAME"], a["ANIMALAGE"])
        s = html.header(title, session, "test.js")
        c = html.controller_str("name", "animal_test")
        c += html.controller_json("animal", a)
        c += html.controller_json("tabcounts", extanimal.get_satellite_counts(dbo, a["ID"])[0])
        c += html.controller_json("rows", test)
        c += html.controller_json("testtypes", extlookups.get_test_types(dbo))
        c += html.controller_json("testresults", extlookups.get_test_results(dbo))
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        data = web.input(mode = "create", ids = "")
        mode = utils.df_ks(data, "mode")
        if mode == "create":
            users.check_permission(session, users.ADD_TEST)
            return extmedical.insert_test_from_form(session.dbo, session.user, data)
        elif mode == "update":
            users.check_permission(session, users.CHANGE_TEST)
            extmedical.update_test_from_form(session.dbo, session.user, data)
        elif mode == "delete":
            users.check_permission(session, users.DELETE_TEST)
            for vid in utils.df_kl(data, "ids"):
                extmedical.delete_test(session.dbo, session.user, vid)

class animal_vaccination:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_VACCINATION)
        l = session.locale
        dbo = session.dbo
        data = web.input(id = 0)
        a = extanimal.get_animal(dbo, utils.df_ki(data, "id"))
        if a is None: raise web.notfound()
        schedules = [ 
            "7|%s" % ntranslate(1, [ _("{plural0} week", l), _("{plural1} weeks", l), _("{plural2} weeks", l), _("{plural3} weeks", l) ], l),
            "14|%s" % ntranslate(2, [ _("{plural0} week", l), _("{plural1} weeks", l), _("{plural2} weeks", l), _("{plural3} weeks", l) ], l),
            "21|%s" % ntranslate(3, [ _("{plural0} week", l), _("{plural1} weeks", l), _("{plural2} weeks", l), _("{plural3} weeks", l) ], l),
            "28|%s" % ntranslate(4, [ _("{plural0} week", l), _("{plural1} weeks", l), _("{plural2} weeks", l), _("{plural3} weeks", l) ], l),
            "182|%s" % ntranslate(6, [ _("{plural0} month", l), _("{plural1} months", l), _("{plural2} months", l), _("{plural3} months", l) ], l),
            "365|%s" % ntranslate(1, [ _("{plural0} year", l), _("{plural1} year", l), _("{plural2} year", l), _("{plural3} year", l) ], l),
            "730|%s" % ntranslate(2, [ _("{plural0} year", l), _("{plural1} year", l), _("{plural2} year", l), _("{plural3} year", l) ], l),
            "1095|%s" % ntranslate(3, [ _("{plural0} year", l), _("{plural1} year", l), _("{plural2} year", l), _("{plural3} year", l) ], l)
        ]
        vacc = extmedical.get_vaccinations(dbo, utils.df_ki(data, "id"))
        al.debug("got %d vaccinations" % len(vacc), "code.vaccination", dbo)
        title = _("{0} - {1} ({2} {3} aged {4})", l).format(a["ANIMALNAME"], a["CODE"], a["SEXNAME"], a["SPECIESNAME"], a["ANIMALAGE"])
        s = html.header(title, session, "vaccination.js")
        c = html.controller_str("name", "animal_vaccination")
        c += html.controller_json("animal", a)
        c += html.controller_json("tabcounts", extanimal.get_satellite_counts(dbo, a["ID"])[0])
        c += html.controller_json("schedules", schedules)
        c += html.controller_json("rows", vacc)
        c += html.controller_json("vaccinationtypes", extlookups.get_vaccination_types(dbo))
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        data = web.input(mode = "create", ids = "", duration = 0)
        mode = utils.df_ks(data, "mode")
        if mode == "create":
            users.check_permission(session, users.ADD_VACCINATION)
            return extmedical.insert_vaccination_from_form(session.dbo, session.user, data)
        elif mode == "update":
            users.check_permission(session, users.CHANGE_VACCINATION)
            extmedical.update_vaccination_from_form(session.dbo, session.user, data)
        elif mode == "delete":
            users.check_permission(session, users.DELETE_VACCINATION)
            for vid in utils.df_kl(data, "ids"):
                extmedical.delete_vaccination(session.dbo, session.user, vid)
        elif mode == "complete":
            users.check_permission(session, users.BULK_COMPLETE_VACCINATION)
            for vid in utils.df_kl(data, "ids"):
                extmedical.complete_vaccination(session.dbo, session.user, vid)
        elif mode == "reschedule":
            users.check_permission(session, users.BULK_COMPLETE_VACCINATION)
            for vid in utils.df_kl(data, "ids"):
                extmedical.reschedule_vaccination(session.dbo, session.user, vid, utils.df_ki(data, "duration"))
        elif mode == "required":
            users.check_permission(session, users.BULK_COMPLETE_VACCINATION)
            newdate = utils.df_kd(data, "newdate", session.dbo.locale)
            for vid in utils.df_kl(data, "ids"):
                extmedical.update_vaccination_required(session.dbo, session.user, vid, newdate)

class change_password:
    def GET(self):
        utils.check_loggedin(session, web)
        l = session.locale
        dbo = session.dbo
        data = web.input()
        title = _("Change Password", l)
        al.debug("%s change password screen" % session.user, "code.change_password", dbo)
        s = html.header(title, session, "change_password.js")
        c = html.controller_bool("ismaster", smcom.active() and dbo.database == session.user)
        c += html.controller_bool("issuggest", utils.df_ki(data, "suggest") == 1)
        c += html.controller_str("username", session.user)
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        dbo = session.dbo
        data = web.input(oldpassword = "", newpassword = "")
        oldpass = utils.df_ks(data, "oldpassword")
        newpass = utils.df_ks(data, "newpassword")
        al.debug("%s changed password %s -> %s" % (session.user, oldpass, newpass), "code.change_password", dbo)
        users.change_password(dbo, session.user, oldpass, newpass)

class change_user_settings:
    def GET(self):
        utils.check_loggedin(session, web)
        l = session.locale
        dbo = session.dbo
        title = _("Change User Settings", l)
        al.debug("%s change user settings screen" % session.user, "code.change_user_settings", dbo)
        s = html.header(title, session, "change_user_settings.js")
        c = html.controller_json("user", users.get_users(dbo, session.user))
        c += html.controller_json("locales", extlookups.LOCALES)
        c += html.controller_json("themes", extlookups.VISUAL_THEMES)
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        dbo = session.dbo
        data = web.input(theme = "", locale = "", realname = "", email = "")
        theme = utils.df_ks(data, "theme")
        locale = utils.df_ks(data, "locale")
        realname = utils.df_ks(data, "realname")
        email = utils.df_ks(data, "email")
        al.debug("%s changed settings: theme=%s, locale=%s, realname=%s, email=%s" % (session.user, theme, locale, realname, email), "code.change_password", dbo)
        users.update_user_settings(dbo, session.user, email, realname, locale, theme)
        users.update_session(session)

class csvimport:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.USE_SQL_INTERFACE)
        l = session.locale
        title = _("Import a CSV file", l)
        s = html.header(title, session, "csvimport.js")
        s += html.controller("")
        s += html.footer()
        web.header("Content-Type", "text/html")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        utils.check_locked_db(session)
        dbo = session.dbo
        l = session.locale
        data = web.input(createmissinglookups = "", cleartables = "", filechooser={})
        users.check_permission(session, users.USE_SQL_INTERFACE)
        web.header("Content-Type", "text/html")
        try:
            errors = extcsvimport.csvimport(dbo, data.filechooser.value, utils.df_kc(data, "createmissinglookups") == 1, utils.df_kc(data, "cleartables") == 1)
            title = _("Import a CSV file", l)
            s = html.header(title, session, "csvimport.js")
            c = html.controller_json("errors", errors)
            s += html.controller(c)
            s += html.footer()
            return s
        except Exception,err:
            if str(err).find("no attribute 'value'") != -1:
                err = "No CSV file was uploaded"
            title = _("Import a CSV file", l)
            s = html.header(title, session, "csvimport.js")
            c = html.controller_str("error", str(err))
            s += html.controller(c)
            s += html.footer()
            return s

class diary_edit:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.EDIT_ALL_DIARY_NOTES)
        l = session.locale
        dbo = session.dbo
        data = web.input(id = 0, filter="uncompleted", newnote="0")
        dfilter = utils.df_ks(data, "filter")
        if dfilter == "uncompleted":
            diaries = extdiary.get_uncompleted_upto_today(dbo)
        elif dfilter == "completed":
            diaries = extdiary.get_completed_upto_today(dbo)
        elif dfilter == "future":
            diaries = extdiary.get_future(dbo)
        elif dfilter == "all":
            diaries = extdiary.get_all_upto_today(dbo)
        title = _("Edit diary notes", l)
        al.debug("got %d diaries, filter was %s" % (len(diaries), dfilter), "code.diary_edit", dbo)
        s = html.header(title, session, "diary.js")
        c = html.controller_json("rows", diaries)
        c += html.controller_bool("newnote", utils.df_ki(data, "newnote") == 1)
        c += html.controller_str("name", "diary_edit")
        c += html.controller_json("forlist", users.get_users_and_roles(dbo))
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        data = web.input(mode="create")
        mode = utils.df_ks(data, "mode")
        if mode == "create":
            users.check_permission(session, users.ADD_DIARY)
            return extdiary.insert_diary_from_form(session.dbo, session.user, extdiary.NO_LINK, 0, data)
        elif mode == "update":
            users.check_permission(session, users.EDIT_ALL_DIARY_NOTES)
            extdiary.update_diary_from_form(session.dbo, session.user, data)
        elif mode == "delete":
            users.check_permission(session, users.DELETE_DIARY)
            for did in utils.df_kl(data, "ids"):
                extdiary.delete_diary(session.dbo, session.user, did)
        elif mode == "complete":
            users.check_permission(session, users.BULK_COMPLETE_NOTES)
            for did in utils.df_kl(data, "ids"):
                extdiary.complete_diary_note(session.dbo, session.user, did)

class diary_edit_my:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.EDIT_MY_DIARY_NOTES)
        l = session.locale
        dbo = session.dbo
        data = web.input(id = 0, filter="uncompleted", newnote="0")
        userfilter = session.user.strip()
        dfilter = utils.df_ks(data, "filter")
        if dfilter == "uncompleted":
            diaries = extdiary.get_uncompleted_upto_today(dbo, userfilter)
        elif dfilter == "completed":
            diaries = extdiary.get_completed_upto_today(dbo, userfilter)
        elif dfilter == "future":
            diaries = extdiary.get_future(dbo, userfilter)
        elif dfilter == "all":
            diaries = extdiary.get_all_upto_today(dbo, userfilter)
        title = _("Edit my diary notes", l)
        al.debug("got %d diaries (%s), filter was %s" % (len(diaries), userfilter, dfilter), "code.diary_edit_my", dbo)
        s = html.header(title, session, "diary.js")
        c = html.controller_json("rows", diaries)
        c += html.controller_bool("newnote", utils.df_ki(data, "newnote") == 1)
        c += html.controller_str("name", "diary_edit_my")
        c += html.controller_json("forlist", users.get_users_and_roles(dbo))
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        data = web.input(mode="create")
        mode = utils.df_ks(data, "mode")
        if mode == "create":
            users.check_permission(session, users.ADD_DIARY)
            extdiary.insert_diary_from_form(session.dbo, session.user, extdiary.NO_LINK, 0, data)
        elif mode == "update":
            users.check_permission(session, users.EDIT_ALL_DIARY_NOTES)
            extdiary.update_diary_from_form(session.dbo, session.user, data)
        elif mode == "delete":
            users.check_permission(session, users.DELETE_DIARY)
            for did in utils.df_kl(data, "ids"):
                extdiary.delete_diary(session.dbo, session.user, did)
        elif mode == "complete":
            users.check_permission(session, users.BULK_COMPLETE_NOTES)
            for did in utils.df_kl(data, "ids"):
                extdiary.complete_diary_note(session.dbo, session.user, did)

class diarytask:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.EDIT_DIARY_TASKS)
        l = session.locale
        dbo = session.dbo
        data = web.input(taskid = 0)
        taskid = utils.df_ki(data, "taskid")
        taskname = extdiary.get_diarytask_name(dbo, taskid)
        diarytaskdetail = extdiary.get_diarytask_details(dbo, taskid)
        title = _("Diary task: {0}", l).format(taskname)
        al.debug("got %d diary task details" % len(diarytaskdetail), "code.diarytask", dbo)
        s = html.header(title, session, "diarytask.js")
        c = html.controller_json("rows", diarytaskdetail)
        c += html.controller_int("taskid", taskid)
        c += html.controller_str("taskname", taskname)
        c += html.controller_json("forlist", users.get_users_and_roles(dbo))
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        l = session.locale
        dbo = session.dbo
        data = web.input(mode="create", tasktype="ANIMAL", taskid="0", id="0", seldate="")
        mode = utils.df_ks(data, "mode")
        if mode == "create":
            users.check_permission(session, users.EDIT_DIARY_TASKS)
            return extdiary.insert_diarytaskdetail_from_form(session.dbo, session.user, data)
        elif mode == "update":
            users.check_permission(session, users.EDIT_DIARY_TASKS)
            extdiary.update_diarytaskdetail_from_form(session.dbo, session.user, data)
        elif mode == "delete":
            users.check_permission(session, users.EDIT_DIARY_TASKS)
            for did in utils.df_kl(data, "ids"):
                extdiary.delete_diarytaskdetail(session.dbo, session.user, did)
        elif mode == "exec":
            users.check_permission(session, users.ADD_DIARY)
            extdiary.execute_diary_task(dbo, session.user, utils.df_ks(data, "tasktype"), utils.df_ki(data, "taskid"), utils.df_ki(data, "id"), utils.df_kd(data, "seldate", l))

class diarytasks:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.EDIT_DIARY_TASKS)
        l = session.locale
        dbo = session.dbo
        diarytaskhead = extdiary.get_diarytasks(dbo)
        title = _("Diary Tasks", l)
        al.debug("got %d diary tasks" % len(diarytaskhead), "code.diarytasks", dbo)
        s = html.header(title, session, "diarytasks.js")
        c = html.controller_json("rows", diarytaskhead)
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        data = web.input(mode="create")
        mode = utils.df_ks(data, "mode")
        if mode == "create":
            users.check_permission(session, users.EDIT_DIARY_TASKS)
            return extdiary.insert_diarytaskhead_from_form(session.dbo, session.user, data)
        elif mode == "update":
            users.check_permission(session, users.EDIT_DIARY_TASKS)
            extdiary.update_diarytaskhead_from_form(session.dbo, session.user, data)
        elif mode == "delete":
            users.check_permission(session, users.EDIT_DIARY_TASKS)
            for did in utils.df_kl(data, "ids"):
                extdiary.delete_diarytask(session.dbo, session.user, did)

class document_gen:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.GENERATE_DOCUMENTS)
        dbo = session.dbo
        data = web.input(mode = "ANIMAL", id = 0, template = 0)
        mode = utils.df_ks(data, "mode")
        template = utils.df_ki(data, "template")
        templatename = dbfs.get_name_for_id(dbo, template)
        title = templatename
        loglinktype = extlog.ANIMAL
        al.debug("generating %s document for %d" % (mode, utils.df_ki(data, "id")), "code.document_gen", dbo)
        logid = utils.df_ki(data, "id")
        if mode == "ANIMAL":
            loglinktype = extlog.ANIMAL
            content = wordprocessor.generate_animal_doc(dbo, template, utils.df_ki(data, "id"), session.user)
        elif mode == "PERSON":
            loglinktype = extlog.PERSON
            content = wordprocessor.generate_person_doc(dbo, template, utils.df_ki(data, "id"), session.user)
        elif mode == "DONATION":
            loglinktype = extlog.PERSON
            logid = financial.get_donation(dbo, utils.df_ki(data, "id"))["OWNERID"]
            content = wordprocessor.generate_donation_doc(dbo, template, utils.df_ki(data, "id"), session.user)
        if configuration.generate_document_log(dbo) and configuration.generate_document_log_type(dbo) > 0:
            extlog.add_log(dbo, session.user, loglinktype, logid, configuration.generate_document_log_type(dbo), _("Generated document '{0}'").format(templatename))
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return html.tinymce_header(title, "document_edit.js") + \
            html.tinymce_main(dbo.locale, "document_gen", recid=utils.df_ks(data, "id"), mode=utils.df_ks(data, "mode"), \
                template=utils.df_ks(data, "template"), content=utils.escape_tinymce(content))

    def POST(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.GENERATE_DOCUMENTS)
        dbo = session.dbo
        data = web.input(recid = 0, mode = "ANIMAL", template = 0, document = "", savemode="save")
        mode = utils.df_ks(data, "mode")
        template = utils.df_ki(data, "template")
        tempname = dbfs.get_name_for_id(dbo, template)
        if utils.df_ks(data, "savemode") == "save":
            recid = utils.df_ki(data, "recid")
            if mode == "ANIMAL":
                tempname += " - " + extanimal.get_animal_namecode(dbo, recid)
                extmedia.create_document_media(dbo, session.user, extmedia.ANIMAL, recid, tempname, utils.df_ks(data, "document"))
                raise web.seeother("animal_media?id=%d" % recid)
            elif mode == "PERSON":
                tempname += " - " + extperson.get_person_name(dbo, recid)
                extmedia.create_document_media(dbo, session.user, extmedia.PERSON, recid, tempname, utils.df_ks(data, "document"))
                raise web.seeother("person_media?id=%d" % recid)
            elif mode == "DONATION":
                d = financial.get_donation(dbo, recid)
                tempname += " - " + extperson.get_person_name(dbo, d["OWNERID"])
                extmedia.create_document_media(dbo, session.user, extmedia.PERSON, d["OWNERID"], tempname, utils.df_ks(data, "document"))
                raise web.seeother("person_media?id=%d" % recid)
            else:
                raise web.seeother("main")
        elif utils.df_ks(data, "savemode") == "pdf":
            web.header("Content-Type", "application/pdf")
            disposition = configuration.pdf_inline(dbo) and "inline; filename=\"doc.pdf\"" or "attachment; filename=\"doc.pdf\""
            web.header("Content-Disposition", disposition)
            return utils.html_to_pdf(utils.df_ks(data, "document"), BASE_URL, MULTIPLE_DATABASES and dbo.database or "")

class document_edit:
    def GET(self):
        utils.check_loggedin(session, web)
        dbo = session.dbo
        data = web.input(template = 0)
        template = utils.df_ki(data, "template")
        templatename = dbfs.get_name_for_id(dbo, template)
        if templatename == "": raise web.notfound()
        title = templatename
        al.debug("editing %s" % templatename, "code.document_edit", dbo)
        content = utils.escape_tinymce(dbfs.get_string_id(dbo, template))
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return html.tinymce_header(title, "document_edit.js") + html.tinymce_main(dbo.locale, "document_edit", template=template, content=content)

    def POST(self):
        utils.check_loggedin(session, web)
        dbo = session.dbo
        data = web.input(template = "", document = "", savemode = "save")
        if utils.df_ks(data, "savemode") == "save":
            dbfs.put_string_id(dbo, utils.df_ki(data, "template"), utils.df_ks(data, "document"))
            raise web.seeother("document_templates")
        elif utils.df_ks(data, "savemode") == "pdf":
            web.header("Content-Type", "application/pdf")
            disposition = configuration.pdf_inline(dbo) and "inline; filename=\"doc.pdf\"" or "attachment; filename=\"doc.pdf\""
            web.header("Content-Disposition", disposition)
            return utils.html_to_pdf(utils.df_ks(data, "document"), BASE_URL, MULTIPLE_DATABASES and dbo.database or "")

class document_media_edit:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_MEDIA)
        dbo = session.dbo
        data = web.input(id = 0, redirecturl = "/main")
        lastmod, medianame, mimetype, filedata = extmedia.get_media_file_data(session.dbo, utils.df_ki(data, "id"))
        al.debug("editing media %d" % utils.df_ki(data, "id"), "code.document_media_edit", dbo)
        title = medianame
        web.header("Content-Type", "text/html")
        return html.tinymce_header(title, "document_edit.js") + \
            html.tinymce_main(dbo.locale, "document_media_edit", mediaid=utils.df_ks(data, "id"), redirecturl=utils.df_ks(data, "redirecturl"), \
                content=utils.escape_tinymce(filedata))

    def POST(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.CHANGE_MEDIA)
        dbo = session.dbo
        data = web.input(mediaid = 0, redirecturl = "main", document = "", savemode = "save")
        if utils.df_ks(data, "savemode") == "save":
            extmedia.update_file_content(dbo, session.user, utils.df_ki(data, "mediaid"), utils.df_ks(data, "document"))
            raise web.seeother(utils.df_ks(data, "redirecturl"))
        elif utils.df_ks(data, "savemode") == "pdf":
            web.header("Content-Type", "application/pdf")
            disposition = configuration.pdf_inline(dbo) and "inline; filename=\"doc.pdf\"" or "attachment; filename=\"doc.pdf\""
            web.header("Content-Disposition", disposition)
            return utils.html_to_pdf(utils.df_ks(data, "document"), BASE_URL, MULTIPLE_DATABASES and dbo.database or "")

class document_repository:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_REPO_DOCUMENT)
        dbo = session.dbo
        l = session.locale
        data = web.input(dbfsid = 0)
        if utils.df_ki(data, "dbfsid") != 0:
            name = dbfs.get_name_for_id(dbo, utils.df_ki(data, "dbfsid"))
            mimetype, encoding = mimetypes.guess_type("file://" + name, strict=False)
            web.header("Content-Type", mimetype)
            web.header("Content-Disposition", "attachment; filename=\"%s\"" % name)
            return dbfs.get_string_id(dbo, utils.df_ki(data, "dbfsid"))
        else:
            title = _("Document Repository", l)
            documents = dbfs.get_document_repository(dbo)
            al.debug("got %d documents in repository" % len(documents), "code.document_repository", dbo)
            s = html.header(title, session, "document_repository.js")
            c = html.controller_json("rows", documents)
            s += html.controller(c)
            s += html.footer()
            web.header("Content-Type", "text/html")
            web.header("Cache-Control", "no-cache")
            return s

    def POST(self):
        utils.check_loggedin(session, web)
        dbo = session.dbo
        data = web.input(mode="create", filechooser={})
        mode = utils.df_ks(data, "mode")
        if mode == "create":
            users.check_permission(session, users.ADD_REPO_DOCUMENT)
            dbfs.upload_document_repository(dbo, data.filechooser)
            raise web.seeother("document_repository")
        if mode == "delete":
            users.check_permission(session, users.DELETE_REPO_DOCUMENT)
            for i in utils.df_kl(data, "ids"):
                dbfs.delete_id(dbo, i)

class document_templates:
    def GET(self):
        utils.check_loggedin(session, web)
        dbo = session.dbo
        l = session.locale
        title = _("Document Templates", l)
        templates = dbfs.get_html_templates(dbo)
        al.debug("got %d document templates" % len(templates), "code.document_templates", dbo)
        s = html.header(title, session, "document_templates.js")
        c = html.controller_json("rows", templates)
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        dbo = session.dbo
        data = web.input(mode="create", template="")
        mode = utils.df_ks(data, "mode")
        if mode == "create":
            return dbfs.create_html_template(dbo, utils.df_ks(data, "template"))
        if mode == "clone":
            for t in utils.df_kl(data, "ids"):
                return dbfs.clone_html_template(dbo, t, utils.df_ks(data, "template"))
        if mode == "delete":
            for t in utils.df_kl(data, "ids"):
                dbfs.delete_id(dbo, t)

class donation:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_DONATION)
        l = session.locale
        dbo = session.dbo
        data = web.input(id = 0, offset = "m7")
        donations = financial.get_donations(dbo, utils.df_ks(data, "offset"))
        title = _("Donation book", l)
        al.debug("got %d donations" % (len(donations)), "code.donation", dbo)
        s = html.header(title, session, "donations.js")
        c = html.controller_str("name", "donation")
        c += html.controller_json("donationtypes", extlookups.get_donation_types(dbo))
        c += html.controller_json("paymenttypes", extlookups.get_payment_types(dbo))
        c += html.controller_json("frequencies", extlookups.get_donation_frequencies(dbo))
        c += html.controller_json("templates", dbfs.get_html_templates(dbo))
        c += html.controller_json("rows", donations)
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        data = web.input(mode="create")
        mode = utils.df_ks(data, "mode")
        dbo = session.dbo
        if mode == "create":
            users.check_permission(session, users.ADD_DONATION)
            return financial.insert_donation_from_form(dbo, session.user, data)
        elif mode == "update":
            users.check_permission(session, users.CHANGE_DONATION)
            financial.update_donation_from_form(dbo, session.user, data)
        elif mode == "delete":
            users.check_permission(session, users.DELETE_DONATION)
            for did in utils.df_kl(data, "ids"):
                financial.delete_donation(dbo, session.user, did)
        elif mode == "receive":
            users.check_permission(session, users.CHANGE_DONATION)
            for did in utils.df_kl(data, "ids"):
                financial.receive_donation(dbo, session.user, did)
        elif mode == "personmovements":
            users.check_permission(session, users.VIEW_MOVEMENT)
            web.header("Content-Type", "application/json")
            return html.json(extmovement.get_person_movements(dbo, utils.df_ki(data, "personid")))

class donation_receive:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.ADD_DONATION)
        l = session.locale
        dbo = session.dbo
        title = _("Receive a donation", l)
        s = html.header(title, session, "donation_receive.js")
        al.debug("receiving donation", "code.donation_receive", dbo)
        c = html.controller_json("donationtypes", extlookups.get_donation_types(dbo))
        c += html.controller_json("paymenttypes", extlookups.get_payment_types(dbo))
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        data = web.input(mode="create")
        mode = utils.df_ks(data, "mode")
        if mode == "create":
            users.check_permission(session, users.ADD_DONATION)
            return str(financial.insert_donation_from_form(session.dbo, session.user, data))

class foundanimal:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_FOUND_ANIMAL)
        l = session.locale
        dbo = session.dbo
        data = web.input(id = 0)
        a = extlostfound.get_foundanimal(dbo, utils.df_ki(data, "id"))
        if a is None: raise web.notfound()
        title = _("Found animal - {0} {1} [{2}]", l).format(a["AGEGROUP"], a["SPECIESNAME"], a["OWNERNAME"])
        al.debug("open found animal %s %s %s" % (a["AGEGROUP"], a["SPECIESNAME"], a["OWNERNAME"]), "code.foundanimal", dbo)
        s = html.header(title, session, "lostfound.js")
        c = html.controller_json("animal", a)
        c += html.controller_str("name", "foundanimal")
        c += html.controller_json("additional", extadditional.get_additional_fields(dbo, a["ID"], "foundanimal"))
        c += html.controller_json("agegroups", configuration.age_groups(dbo))
        c += html.controller_json("breeds", extlookups.get_breeds_by_species(dbo))
        c += html.controller_json("colours", extlookups.get_basecolours(dbo))
        c += html.controller_json("sexes", extlookups.get_sexes(dbo))
        c += html.controller_json("species", extlookups.get_species(dbo))
        c += html.controller_json("tabcounts", extlostfound.get_foundanimal_satellite_counts(dbo, a["LFID"])[0])
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        dbo = session.dbo
        data = web.input(mode="save")
        mode = utils.df_ks(data, "mode")
        if mode == "save":
            users.check_permission(session, users.CHANGE_FOUND_ANIMAL)
            extlostfound.update_foundanimal_from_form(dbo, data, session.user)
        elif mode == "delete":
            users.check_permission(session, users.DELETE_FOUND_ANIMAL)
            extlostfound.delete_foundanimal(dbo, session.user, utils.df_ki(data, "id"))
        elif mode == "toanimal":
            users.check_permission(session, users.ADD_ANIMAL)
            return str(extlostfound.create_animal_from_found(dbo, session.user, utils.df_ki(data, "id")))
        elif mode == "towaitinglist":
            users.check_permission(session, users.ADD_WAITING_LIST)
            return str(extlostfound.create_waitinglist_from_found(dbo, session.user, utils.df_ki(data, "id")))

class foundanimal_diary:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_DIARY)
        l = session.locale
        dbo = session.dbo
        data = web.input(id = 0)
        a = extlostfound.get_foundanimal(dbo, utils.df_ki(data, "id"))
        if a is None: raise web.notfound()
        title = _("Found animal - {0} {1} [{2}]", l).format(a["AGEGROUP"], a["SPECIESNAME"], a["OWNERNAME"])
        diaries = extdiary.get_diaries(dbo, extdiary.FOUNDANIMAL, utils.df_ki(data, "id"))
        al.debug("got %d diaries for found animal %s %s %s" % (len(diaries), a["AGEGROUP"], a["SPECIESNAME"], a["OWNERNAME"]), "code.foundanimal_diary", dbo)
        s = html.header(title, session, "diary.js")
        c = html.controller_json("rows", diaries)
        c += html.controller_json("animal", a)
        c += html.controller_json("tabcounts", extlostfound.get_foundanimal_satellite_counts(dbo, a["LFID"])[0])
        c += html.controller_str("name", "foundanimal_diary")
        c += html.controller_int("linkid", a["LFID"])
        c += html.controller_json("forlist", users.get_users_and_roles(dbo))
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        data = web.input(mode="create")
        mode = utils.df_ks(data, "mode")
        if mode == "create":
            users.check_permission(session, users.ADD_DIARY)
            return extdiary.insert_diary_from_form(session.dbo, session.user, extdiary.FOUNDANIMAL, utils.df_ki(data, "linkid"), data)
        elif mode == "update":
            users.check_permission(session, users.EDIT_ALL_DIARY_NOTES)
            extdiary.update_diary_from_form(session.dbo, session.user, data)
        elif mode == "delete":
            users.check_permission(session, users.DELETE_DIARY)
            for did in utils.df_kl(data, "ids"):
                extdiary.delete_diary(session.dbo, session.user, did)
        elif mode == "complete":
            users.check_permission(session, users.BULK_COMPLETE_NOTES)
            for did in utils.df_kl(data, "ids"):
                extdiary.complete_diary_note(session.dbo, session.user, did)

class foundanimal_find:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_FOUND_ANIMAL)
        l = session.locale
        dbo = session.dbo
        title = _("Find Found Animal", l)
        s = html.header(title, session, "lostfound_find.js")
        c = html.controller_json("agegroups", configuration.age_groups(dbo))
        c += html.controller_json("colours", extlookups.get_basecolours(dbo))
        c += html.controller_json("species", extlookups.get_species(dbo))
        c += html.controller_json("breeds", extlookups.get_breeds_by_species(dbo))
        c += html.controller_json("sexes", extlookups.get_sexes(dbo))
        c += html.controller_str("mode", "found")
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        return s

class foundanimal_find_results:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_FOUND_ANIMAL)
        dbo = session.dbo
        l = session.locale
        data = web.input(mode = "")
        results = extlostfound.get_foundanimal_find_advanced(dbo, data, configuration.record_search_limit(dbo))
        title = _("Results", l)
        resultsmessage = _("Find found animal returned {0} results.", l).format(len(results))
        al.debug("found %d results for %s" % (len(results), str(web.ctx.query)), "code.foundanimal_find_results", dbo)
        s = html.header(title, session, "lostfound_find_results.js")
        c = html.controller_json("rows", results)
        c += html.controller_str("name", "foundanimal_find_results")
        c += html.controller_str("resultsmessage", resultsmessage)
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

class foundanimal_log:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_LOG)
        l = session.locale
        dbo = session.dbo
        data = web.input(id = 0, filter = -2)
        logfilter = utils.df_ki(data, "filter")
        if logfilter == -2: logfilter = configuration.default_log_filter(dbo)
        a = extlostfound.get_foundanimal(dbo, utils.df_ki(data, "id"))
        if a is None: raise web.notfound()
        title = _("Found animal - {0} {1} [{2}]", l).format(a["AGEGROUP"], a["SPECIESNAME"], a["OWNERNAME"])
        logs = extlog.get_logs(dbo, extlog.FOUNDANIMAL, utils.df_ki(data, "id"), logfilter)
        s = html.header(title, session, "log.js")
        c = html.controller_str("name", "foundanimal_log")
        c += html.controller_int("linkid", utils.df_ki(data, "id"))
        c += html.controller_int("filter", logfilter)
        c += html.controller_json("rows", logs)
        c += html.controller_json("animal", a)
        c += html.controller_json("tabcounts", extlostfound.get_foundanimal_satellite_counts(dbo, a["LFID"])[0])
        c += html.controller_json("logtypes", extlookups.get_log_types(dbo))
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        data = web.input(mode="create")
        mode = utils.df_ks(data, "mode")
        if mode == "create":
            users.check_permission(session, users.ADD_LOG)
            return extlog.insert_log_from_form(session.dbo, session.user, extlog.FOUNDANIMAL, utils.df_ki(data, "linkid"), data)
        elif mode == "update":
            users.check_permission(session, users.CHANGE_LOG)
            extlog.update_log_from_form(session.dbo, session.user, data)
        elif mode == "delete":
            users.check_permission(session, users.DELETE_LOG)
            for lid in utils.df_kl(data, "ids"):
                extlog.delete_log(session.dbo, session.user, lid)

class foundanimal_media:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_MEDIA)
        l = session.locale
        dbo = session.dbo
        data = web.input(id = 0)
        a = extlostfound.get_foundanimal(dbo, utils.df_ki(data, "id"))
        if a is None: raise web.notfound()
        title = _("Found animal - {0} {1} [{2}]", l).format(a["AGEGROUP"], a["SPECIESNAME"], a["OWNERNAME"])
        m = extmedia.get_media(dbo, extmedia.FOUNDANIMAL, utils.df_ki(data, "id"))
        al.debug("got %d media for found animal %s %s %s" % (len(m), a["AGEGROUP"], a["SPECIESNAME"], a["OWNERNAME"]), "code.foundanimal_media", dbo)
        s = html.header(title, session, "media.js")
        c = html.controller_json("media", m)
        c += html.controller_json("animal", a)
        c += html.controller_json("tabcounts", extlostfound.get_foundanimal_satellite_counts(dbo, a["LFID"])[0])
        c += html.controller_bool("showPreferred", False)
        c += html.controller_int("linkid", utils.df_ki(data, "id"))
        c += html.controller_int("linktypeid", extmedia.FOUNDANIMAL)
        c += html.controller_str("name", self.__class__.__name__)
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        data = web.input(mode="create", filechooser={}, linkid="0", base64image = "", _unicode=False)
        mode = utils.df_ks(data, "mode")
        dbo = session.dbo
        l = session.locale
        linkid = utils.df_ki(data, "linkid")
        if mode == "create":
            users.check_permission(session, users.ADD_MEDIA)
            extmedia.attach_file_from_form(session.dbo, session.user, extmedia.FOUNDANIMAL, linkid, data)
            raise web.seeother("foundanimal_media?id=%d" % linkid)
        elif mode == "createdoc":
            users.check_permission(session, users.ADD_MEDIA)
            mediaid = extmedia.create_blank_document_media(session.dbo, session.user, extmedia.FOUNDANIMAL, linkid)
            raise web.seeother("document_media_edit?id=%d&redirecturl=foundanimal_media?id=%d" % (mediaid, linkid))
        elif mode == "createlink":
            users.check_permission(session, users.ADD_MEDIA)
            mediaid = extmedia.attach_link_from_form(session.dbo, session.user, extmedia.FOUNDANIMAL, linkid, data)
            raise web.seeother("foundanimal_media?id=%d" % linkid)
        elif mode == "update":
            users.check_permission(session, users.CHANGE_MEDIA)
            extmedia.update_media_notes(session.dbo, session.user, utils.df_ki(data, "mediaid"), utils.df_ks(data, "comments"))
        elif mode == "delete":
            users.check_permission(session, users.DELETE_MEDIA)
            for mid in utils.df_kl(data, "ids"):
                extmedia.delete_media(session.dbo, session.user, mid)
        elif mode == "email":
            users.check_permission(session, users.MAIL_MERGE)
            emailadd = utils.df_ks(data, "email")
            if emailadd == "" or emailadd.find("@") == -1:
                raise utils.ASMValidationError(_("Invalid email address", l))
            for mid in utils.df_kl(data, "ids"):
                m = extmedia.get_media_by_id(dbo, mid)
                if len(m) == 0: raise web.notfound()
                m = m[0]
                content = dbfs.get_string(dbo, m["MEDIANAME"])
                content = utils.fix_relative_document_uris(content, BASE_URL, MULTIPLE_DATABASES and dbo.database or "")
                utils.send_email(dbo, configuration.email(dbo), emailadd, "", m["MEDIANOTES"], content, "html")
                return emailadd
        elif mode == "rotateclock":
            users.check_permission(session, users.CHANGE_MEDIA)
            for mid in utils.df_kl(data, "ids"):
                extmedia.rotate_media(session.dbo, session.user, mid, True)
        elif mode == "rotateanti":
            users.check_permission(session, users.CHANGE_MEDIA)
            for mid in utils.df_kl(data, "ids"):
                extmedia.rotate_media(session.dbo, session.user, mid, False)
        elif mode == "web":
            users.check_permission(session, users.CHANGE_MEDIA)
            mid = utils.df_kl(data, "ids")[0]
            extmedia.set_web_preferred(session.dbo, session.user, mid)
        elif mode == "video":
            users.check_permission(session, users.CHANGE_MEDIA)
            mid = utils.df_kl(data, "ids")[0]
            extmedia.set_video_preferred(session.dbo, session.user, mid)
        elif mode == "doc":
            users.check_permission(session, users.CHANGE_MEDIA)
            mid = utils.df_kl(data, "ids")[0]
            extmedia.set_doc_preferred(session.dbo, session.user, mid)

class foundanimal_new:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.ADD_FOUND_ANIMAL)
        l = session.locale
        dbo = session.dbo
        title = _("Add found animal", l)
        s = html.header(title, session, "lostfound_new.js")
        c = html.controller_json("agegroups", configuration.age_groups(dbo))
        c += html.controller_json("colours", extlookups.get_basecolours(dbo))
        c += html.controller_json("species", extlookups.get_species(dbo))
        c += html.controller_json("breeds", extlookups.get_breeds_by_species(dbo))
        c += html.controller_json("sexes", extlookups.get_sexes(dbo))
        c += html.controller_str("name", "foundanimal_new")
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.ADD_FOUND_ANIMAL)
        utils.check_locked_db(session)
        dbo = session.dbo
        data = web.input()
        return str(extlostfound.insert_foundanimal_from_form(dbo, data, session.user))

class giftaid_hmrc_spreadsheet:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_DONATION)
        dbo = session.dbo
        l = session.locale
        data = web.input(fromdate = "", todate = "")
        fromdate = utils.df_ks(data, "fromdate")
        todate = utils.df_ks(data, "todate")
        if fromdate == "":
            title = "HMRC Gift Aid Spreadsheet"
            s = html.header(title, session, "giftaid_hmrc_spreadsheet.js")
            s += html.footer()
            web.header("Content-Type", "text/html")
            return s
        else:
            al.debug("generating HMRC giftaid spreadsheet for %s -> %s" % (fromdate, todate), "code.giftaid_hmrc_spreadsheet", dbo)
            web.header("Content-Type", "application/vnd.oasis.opendocument.spreadsheet")
            web.header("Cache-Control", "no-cache")
            web.header("Content-Disposition", "attachment; filename=\"giftaid.ods\"")
            return financial.giftaid_spreadsheet(dbo, PATH, utils.df_kd(data, "fromdate", l), utils.df_kd(data, "todate", l))

class htmltemplates:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.SYSTEM_OPTIONS)
        l = session.locale
        dbo = session.dbo
        title = _("HTML Publishing Templates", l)
        templates = dbfs.get_html_publisher_templates_files(dbo)
        al.debug("editing %d html templates" % len(templates), "code.htmltemplates", dbo)
        s = html.header(title, session, "htmltemplates.js")
        c = html.controller_json("rows", templates)
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        data = web.input(mode="create", templatename = "", header = "", body = "", footer = "")
        mode = utils.df_ks(data, "mode")
        dbo = session.dbo
        if mode == "create":
            users.check_permission(session, users.SYSTEM_OPTIONS)
            dbfs.update_html_publisher_template(dbo, session.user, utils.df_ks(data, "templatename"), utils.df_ks(data, "header"), utils.df_ks(data, "body"), utils.df_ks(data, "footer"))
        elif mode == "update":
            users.check_permission(session, users.SYSTEM_OPTIONS)
            dbfs.update_html_publisher_template(dbo, session.user, utils.df_ks(data, "templatename"), utils.df_ks(data, "header"), utils.df_ks(data, "body"), utils.df_ks(data, "footer"))
        elif mode == "delete":
            users.check_permission(session, users.SYSTEM_OPTIONS)
            for name in utils.df_ks(data, "names").split(","):
                if name != "": dbfs.delete_html_publisher_template(dbo, session.user, name)

class litters:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_LITTER)
        l = session.locale
        dbo = session.dbo
        litters = extanimal.get_litters(dbo)
        title = _("Litters", l)
        al.debug("got %d litters" % len(litters), "code.litters", dbo)
        s = html.header(title, session, "litters.js")
        c = html.controller_json("rows", litters)
        c += html.controller_json("species", extlookups.get_species(dbo))
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        data = web.input(mode="create")
        mode = utils.df_ks(data, "mode")
        dbo = session.dbo
        if mode == "create":
            users.check_permission(session, users.ADD_LITTER)
            return extanimal.insert_litter_from_form(session.dbo, session.user, data)
        elif mode == "nextlitterid":
            nextid = db.query_int(dbo, "SELECT MAX(ID) FROM animallitter") + 1
            return utils.padleft(nextid, 6)
        elif mode == "update":
            users.check_permission(session, users.CHANGE_LITTER)
            extanimal.update_litter_from_form(session.dbo, session.user, data)
        elif mode == "delete":
            users.check_permission(session, users.DELETE_LITTER)
            for lid in utils.df_kl(data, "ids"):
                extanimal.delete_litter(session.dbo, session.user, lid)

class log_new:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.CHANGE_ANIMAL)
        l = session.locale
        dbo = session.dbo
        data = web.input(mode = "animal")
        title = _("Add a new log", l)
        s = html.header(title, session, "log_new.js")
        c = html.controller_json("logtypes", extlookups.get_log_types(dbo))
        c += html.controller_str("mode", utils.df_ks(data, "mode"))
        al.debug("loaded lookups for new log", "code.log_new", dbo)
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        dbo = session.dbo
        data = web.input(mode="create")
        mode = utils.df_ks(data, "mode")
        users.check_permission(session, users.ADD_LOG)
        if mode == "animal":
            extlog.insert_log_from_form(dbo, session.user, extlog.ANIMAL, utils.df_ki(data, "animal"), data)
        elif mode == "person":
            extlog.insert_log_from_form(dbo, session.user, extlog.PERSON, utils.df_ki(data, "person"), data)

class lookups:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.MODIFY_LOOKUPS)
        l = session.locale
        dbo = session.dbo
        data = web.input(tablename="animaltype")
        tablename = utils.df_ks(data, "tablename");
        table = list(extlookups.LOOKUP_TABLES[tablename])
        table[0] = translate(table[0], l)
        table[2] = translate(table[2], l)
        rows = extlookups.get_lookup(dbo, tablename, table[1])
        al.debug("edit lookups for %s, got %d rows" % (tablename, len(rows)), "code.lookups", dbo)
        title = _("Edit Lookups", l)
        s = html.header(title, session, "lookups.js")
        c = html.controller_json("rows", rows)
        c += html.controller_json("petfinderspecies", extlookups.PETFINDER_SPECIES)
        c += html.controller_json("petfinderbreeds", extlookups.PETFINDER_BREEDS)
        c += html.controller_str("tablename", tablename)
        c += html.controller_str("tablelabel", table[0])
        c += html.controller_str("namefield", table[1].upper())
        c += html.controller_str("namelabel", table[2])
        c += html.controller_str("descfield", table[3].upper())
        c += html.controller_bool("hasspecies", table[4] == 1)
        c += html.controller_bool("haspfspecies", table[5] == 1)
        c += html.controller_bool("haspfbreed", table[6] == 1)
        c += html.controller_bool("hasdefaultcost", table[7] == 1)
        c += html.controller_bool("canadd", table[8] == 1)
        c += html.controller_bool("candelete", table[9] == 1)
        c += html.controller_json("species", extlookups.get_species(dbo))
        c += html.controller_json("tables", html.json_lookup_tables(l))
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        dbo = session.dbo
        l = session.locale
        data = web.input(mode="create", id=0, lookup="", lookupname="", lookupdesc="", species=0, pfbreed="", pfspecies="", defaultcost="", adoptionfee="")
        mode = utils.df_ks(data, "mode")
        if mode == "create":
            users.check_permission(session, users.MODIFY_LOOKUPS)
            return extlookups.insert_lookup(dbo, utils.df_ks(data, "lookup"), utils.df_ks(data, "lookupname"), utils.df_ks(data, "lookupdesc"), \
                utils.df_ki(data, "species"), utils.df_ks(data, "pfbreed"), utils.df_ks(data, "pfspecies"), utils.df_km(data, "defaultcost", l))
        elif mode == "update":
            users.check_permission(session, users.MODIFY_LOOKUPS)
            extlookups.update_lookup(dbo, utils.df_ki(data, "id"), utils.df_ks(data, "lookup"), utils.df_ks(data, "lookupname"), utils.df_ks(data, "lookupdesc"), \
                utils.df_ki(data, "species"), utils.df_ks(data, "pfbreed"), utils.df_ks(data, "pfspecies"), utils.df_km(data, "defaultcost", l))
        elif mode == "delete":
            users.check_permission(session, users.MODIFY_LOOKUPS)
            for lid in utils.df_kl(data, "ids"):
                extlookups.delete_lookup(dbo, utils.df_ks(data, "lookup"), lid)

class lostanimal:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_LOST_ANIMAL)
        l = session.locale
        dbo = session.dbo
        data = web.input(id = 0)
        a = extlostfound.get_lostanimal(dbo, utils.df_ki(data, "id"))
        if a is None: raise web.notfound()
        al.debug("open lost animal %s %s %s" % (a["AGEGROUP"], a["SPECIESNAME"], a["OWNERNAME"]), "code.foundanimal", dbo)
        title = _("Lost animal - {0} {1} [{2}]", l).format(a["AGEGROUP"], a["SPECIESNAME"], a["OWNERNAME"])
        s = html.header(title, session, "lostfound.js")
        c = html.controller_json("animal", a)
        c += html.controller_str("name", "lostanimal")
        c += html.controller_json("additional", extadditional.get_additional_fields(dbo, a["ID"], "lostanimal"))
        c += html.controller_json("agegroups", configuration.age_groups(dbo))
        c += html.controller_json("breeds", extlookups.get_breeds_by_species(dbo))
        c += html.controller_json("colours", extlookups.get_basecolours(dbo))
        c += html.controller_json("sexes", extlookups.get_sexes(dbo))
        c += html.controller_json("species", extlookups.get_species(dbo))
        c += html.controller_json("tabcounts", extlostfound.get_lostanimal_satellite_counts(dbo, a["LFID"])[0])
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        dbo = session.dbo
        data = web.input(mode="save")
        mode = utils.df_ks(data, "mode")
        if mode == "save":
            users.check_permission(session, users.CHANGE_LOST_ANIMAL)
            extlostfound.update_lostanimal_from_form(dbo, data, session.user)
        elif mode == "delete":
            users.check_permission(session, users.DELETE_LOST_ANIMAL)
            extlostfound.delete_lostanimal(dbo, session.user, utils.df_ki(data, "id"))

class lostanimal_diary:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_DIARY)
        l = session.locale
        dbo = session.dbo
        data = web.input(id = 0)
        a = extlostfound.get_lostanimal(dbo, utils.df_ki(data, "id"))
        if a is None: raise web.notfound()
        title = _("Lost animal - {0} {1} [{2}]", l).format(a["AGEGROUP"], a["SPECIESNAME"], a["OWNERNAME"])
        diaries = extdiary.get_diaries(dbo, extdiary.LOSTANIMAL, utils.df_ki(data, "id"))
        al.debug("got %d diaries for lost animal %s %s %s" % (len(diaries), a["AGEGROUP"], a["SPECIESNAME"], a["OWNERNAME"]), "code.foundanimal_diary", dbo)
        s = html.header(title, session, "diary.js")
        c = html.controller_json("rows", diaries)
        c += html.controller_json("animal", a)
        c += html.controller_json("tabcounts", extlostfound.get_lostanimal_satellite_counts(dbo, a["LFID"])[0])
        c += html.controller_str("name", "lostanimal_diary")
        c += html.controller_int("linkid", a["LFID"])
        c += html.controller_json("forlist", users.get_users_and_roles(dbo))
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        data = web.input(mode="create")
        mode = utils.df_ks(data, "mode")
        if mode == "create":
            users.check_permission(session, users.ADD_DIARY)
            return extdiary.insert_diary_from_form(session.dbo, session.user, extdiary.LOSTANIMAL, utils.df_ki(data, "linkid"), data)
        elif mode == "update":
            users.check_permission(session, users.EDIT_ALL_DIARY_NOTES)
            extdiary.update_diary_from_form(session.dbo, session.user, data)
        elif mode == "delete":
            users.check_permission(session, users.DELETE_DIARY)
            for did in utils.df_kl(data, "ids"):
                extdiary.delete_diary(session.dbo, session.user, did)
        elif mode == "complete":
            users.check_permission(session, users.BULK_COMPLETE_NOTES)
            for did in utils.df_kl(data, "ids"):
                extdiary.complete_diary_note(session.dbo, session.user, did)

class lostanimal_find:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_LOST_ANIMAL)
        l = session.locale
        dbo = session.dbo
        title = _("Find Lost Animal", l)
        s = html.header(title, session, "lostfound_find.js")
        c = html.controller_json("agegroups", configuration.age_groups(dbo))
        c += html.controller_json("colours", extlookups.get_basecolours(dbo))
        c += html.controller_json("species", extlookups.get_species(dbo))
        c += html.controller_json("breeds", extlookups.get_breeds_by_species(dbo))
        c += html.controller_json("sexes", extlookups.get_sexes(dbo))
        c += html.controller_str("mode", "lost")
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        return s

class lostanimal_find_results:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_LOST_ANIMAL)
        dbo = session.dbo
        l = session.locale
        data = web.input(mode = "")
        results = extlostfound.get_lostanimal_find_advanced(dbo, data, configuration.record_search_limit(dbo))
        title = _("Results", l)
        resultsmessage = _("Find lost animal returned {0} results.", l).format(len(results))
        al.debug("found %d results for %s" % (len(results), str(web.ctx.query)), "code.lostanimal_find_results", dbo)
        s = html.header(title, session, "lostfound_find_results.js")
        c = html.controller_json("rows", results)
        c += html.controller_str("name", "lostanimal_find_results")
        c += html.controller_str("resultsmessage", resultsmessage)
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

class lostanimal_log:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_LOG)
        l = session.locale
        dbo = session.dbo
        data = web.input(id = 0, filter = -2)
        logfilter = utils.df_ki(data, "filter")
        if logfilter == -2: logfilter = configuration.default_log_filter(dbo)
        a = extlostfound.get_lostanimal(dbo, utils.df_ki(data, "id"))
        if a is None: raise web.notfound()
        title = _("Lost animal - {0} {1} [{2}]", l).format(a["AGEGROUP"], a["SPECIESNAME"], a["OWNERNAME"])
        logs = extlog.get_logs(dbo, extlog.LOSTANIMAL, utils.df_ki(data, "id"), logfilter)
        s = html.header(title, session, "log.js")
        c = html.controller_str("name", "lostanimal_log")
        c += html.controller_int("linkid", utils.df_ki(data, "id"))
        c += html.controller_int("filter", logfilter)
        c += html.controller_json("rows", logs)
        c += html.controller_json("animal", a)
        c += html.controller_json("tabcounts", extlostfound.get_lostanimal_satellite_counts(dbo, a["LFID"])[0])
        c += html.controller_json("logtypes", extlookups.get_log_types(dbo))
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        data = web.input(mode="create")
        mode = utils.df_ks(data, "mode")
        if mode == "create":
            users.check_permission(session, users.ADD_LOG)
            return extlog.insert_log_from_form(session.dbo, session.user, extlog.LOSTANIMAL, utils.df_ki(data, "linkid"), data)
        elif mode == "update":
            users.check_permission(session, users.CHANGE_LOG)
            extlog.update_log_from_form(session.dbo, session.user, data)
        elif mode == "delete":
            users.check_permission(session, users.DELETE_LOG)
            for lid in utils.df_kl(data, "ids"):
                extlog.delete_log(session.dbo, session.user, lid)

class lostanimal_media:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_MEDIA)
        l = session.locale
        dbo = session.dbo
        data = web.input(id = 0)
        a = extlostfound.get_lostanimal(dbo, utils.df_ki(data, "id"))
        if a is None: raise web.notfound()
        title = _("Lost animal - {0} {1} [{2}]", l).format(a["AGEGROUP"], a["SPECIESNAME"], a["OWNERNAME"])
        m = extmedia.get_media(dbo, extmedia.LOSTANIMAL, utils.df_ki(data, "id"))
        al.debug("got %d media for lost animal %s %s %s" % (len(m), a["AGEGROUP"], a["SPECIESNAME"], a["OWNERNAME"]), "code.foundanimal_media", dbo)
        s = html.header(title, session, "media.js")
        c = html.controller_json("media", m)
        c += html.controller_json("animal", a)
        c += html.controller_json("tabcounts", extlostfound.get_lostanimal_satellite_counts(dbo, a["LFID"])[0])
        c += html.controller_bool("showPreferred", False)
        c += html.controller_int("linkid", utils.df_ki(data, "id"))
        c += html.controller_int("linktypeid", extmedia.LOSTANIMAL)
        c += html.controller_str("name", self.__class__.__name__)
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        data = web.input(mode="create", filechooser={}, linkid="0", base64image = "", _unicode=False)
        mode = utils.df_ks(data, "mode")
        dbo = session.dbo
        l = session.locale
        linkid = utils.df_ki(data, "linkid")
        if mode == "create":
            users.check_permission(session, users.ADD_MEDIA)
            extmedia.attach_file_from_form(session.dbo, session.user, extmedia.LOSTANIMAL, linkid, data)
            raise web.seeother("lostanimal_media?id=%d" % linkid)
        elif mode == "createdoc":
            users.check_permission(session, users.ADD_MEDIA)
            mediaid = extmedia.create_blank_document_media(session.dbo, session.user, extmedia.LOSTANIMAL, linkid)
            raise web.seeother("document_media_edit?id=%d&redirecturl=lostanimal_media?id=%d" % (mediaid, linkid))
        elif mode == "createlink":
            users.check_permission(session, users.ADD_MEDIA)
            mediaid = extmedia.attach_link_from_form(session.dbo, session.user, extmedia.LOSTANIMAL, linkid, data)
            raise web.seeother("lostanimal_media?id=%d" % linkid)
        elif mode == "update":
            users.check_permission(session, users.CHANGE_MEDIA)
            extmedia.update_media_notes(session.dbo, session.user, utils.df_ki(data, "mediaid"), utils.df_ks(data, "comments"))
        elif mode == "delete":
            users.check_permission(session, users.DELETE_MEDIA)
            for mid in utils.df_kl(data, "ids"):
                extmedia.delete_media(session.dbo, session.user, mid)
        elif mode == "email":
            users.check_permission(session, users.MAIL_MERGE)
            emailadd = utils.df_ks(data, "email")
            if emailadd == "" or emailadd.find("@") == -1:
                raise utils.ASMValidationError(_("Invalid email address", l))
            for mid in utils.df_kl(data, "ids"):
                m = extmedia.get_media_by_id(dbo, mid)
                if len(m) == 0: raise web.notfound()
                m = m[0]
                content = dbfs.get_string(dbo, m["MEDIANAME"])
                content = utils.fix_relative_document_uris(content, BASE_URL, MULTIPLE_DATABASES and dbo.database or "")
                utils.send_email(dbo, configuration.email(dbo), emailadd, "", m["MEDIANOTES"], content, "html")
                return emailadd
        elif mode == "rotateclock":
            users.check_permission(session, users.CHANGE_MEDIA)
            for mid in utils.df_kl(data, "ids"):
                extmedia.rotate_media(session.dbo, session.user, mid, True)
        elif mode == "rotateanti":
            users.check_permission(session, users.CHANGE_MEDIA)
            for mid in utils.df_kl(data, "ids"):
                extmedia.rotate_media(session.dbo, session.user, mid, False)
        elif mode == "web":
            users.check_permission(session, users.CHANGE_MEDIA)
            mid = utils.df_kl(data, "ids")[0]
            extmedia.set_web_preferred(session.dbo, session.user, mid)
        elif mode == "video":
            users.check_permission(session, users.CHANGE_MEDIA)
            mid = utils.df_kl(data, "ids")[0]
            extmedia.set_video_preferred(session.dbo, session.user, mid)
        elif mode == "doc":
            users.check_permission(session, users.CHANGE_MEDIA)
            mid = utils.df_kl(data, "ids")[0]
            extmedia.set_doc_preferred(session.dbo, session.user, mid)

class lostanimal_new:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.ADD_LOST_ANIMAL)
        l = session.locale
        dbo = session.dbo
        title = _("Add lost animal", l)
        s = html.header(title, session, "lostfound_new.js")
        c = html.controller_json("agegroups", configuration.age_groups(dbo))
        c += html.controller_json("colours", extlookups.get_basecolours(dbo))
        c += html.controller_json("species", extlookups.get_species(dbo))
        c += html.controller_json("breeds", extlookups.get_breeds_by_species(dbo))
        c += html.controller_json("sexes", extlookups.get_sexes(dbo))
        c += html.controller_str("name", "lostanimal_new")
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.ADD_LOST_ANIMAL)
        utils.check_locked_db(session)
        dbo = session.dbo
        data = web.input()
        return str(extlostfound.insert_lostanimal_from_form(dbo, data, session.user))

class lostfound_match:
    def GET(self):
        utils.check_loggedin(session, web)
        dbo = session.dbo
        data = web.input(lostanimalid = 0, foundanimalid = 0, animalid = 0)
        lostanimalid = utils.df_ki(data, "lostanimalid")
        foundanimalid = utils.df_ki(data, "foundanimalid")
        animalid = utils.df_ki(data, "animalid")
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        # If no parameters have been given, use the cached daily copy of the match report
        if lostanimalid == 0 and foundanimalid == 0 and animalid == 0:
            al.debug("no parameters given, using cached report at /reports/daily/lost_found_match.html", "code.lostfound_match", dbo)
            return dbfs.get_string_filepath(dbo, "/reports/daily/lost_found_match.html")
        else:
            al.debug("match lost=%d, found=%d, animal=%d" % (lostanimalid, foundanimalid, animalid), "code.lostfound_match", dbo)
            return extlostfound.match_report(dbo, session.user, lostanimalid, foundanimalid, animalid)

class mailmerge:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.MAIL_MERGE)
        data = web.input(id = "0", mode = "criteria")
        mode = utils.df_ks(data, "mode")
        dbo = session.dbo
        l = session.locale
        user = session.user
        crit = extreports.get_criteria_controls(session.dbo, utils.df_ki(data, "id"))
        title = extreports.get_title(dbo, utils.df_ki(data, "id"))
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        # If the mail merge doesn't take criteria, go to the merge selection screen instead
        if crit == "":
            al.debug("mailmerge %d has no criteria, moving to merge selection" % utils.df_ki(data, "id"), "code.mailmerge", dbo)
            mode = "selection"
        # If we're in criteria mode (and there are some to get here), ask for them
        if mode == "criteria":
            al.debug("building report criteria form for mailmerge %d %s" % (utils.df_ki(data, "id"), title), "code.mailmerge", dbo)
            s = html.header(title, session, "mailmerge.js")
            s += html.controller(html.controller_bool("criteria", True))
            s += html.heading(title)
            s += "<div id=\"criteriaform\">"
            s += "<input data-post=\"id\" type=\"hidden\" value=\"%d\" />" % utils.df_ki(data, "id")
            s += "<input data-post=\"mode\" type=\"hidden\" value=\"selection\" />"
            s += crit
            s += "</div>"
            s += html.footing()
            s += html.footer()
            return s
        elif mode == "selection":
            al.debug("entering mail merge selection mode for %d" % utils.df_ki(data, "id"), "code.mailmerge", dbo)
            p = extreports.get_criteria_params(dbo, utils.df_ki(data, "id"), data)
            session.mergeparams = p
            session.mergereport = utils.df_ki(data, "id")
            rows, cols = extreports.execute_query(dbo, utils.df_ki(data, "id"), user, p)
            if rows is None: rows = []
            al.debug("got merge rows (%d items)" % len(rows), "code.mailmerge", dbo)
            session.mergetitle = title.replace(" ", "_").replace("\"", "").replace("'", "").lower()
            # construct a list of field tokens for the email helper
            fields = []
            if len(rows) >  0:
                for fname in sorted(rows[0].iterkeys()):
                    fields.append(fname)
            # send the selection form
            title = _("Mail Merge - {0}", l).format(title)
            s = html.header(title, session, "mailmerge.js")
            c = html.controller_json("fields", fields)
            c += html.controller_int("numrows", len(rows))
            s += html.controller(c)
            s += html.footer()
            return s

    def POST(self):
        utils.check_loggedin(session, web)
        dbo = session.dbo
        data = web.input(mode="csv")
        mode = utils.df_ks(data, "mode")
        rows, cols = extreports.execute_query(dbo, session.mergereport, session.user, session.mergeparams)
        al.debug("got merge rows (%d items)" % len(rows), "code.mailmerge", dbo)
        if mode == "email":
            fromadd = utils.df_ks(data, "from")
            subject = utils.df_ks(data, "subject")
            body = utils.df_ks(data, "body")
            contenttype = utils.df_kc(data, "html") == 1 and "html" or "plain"
            utils.send_bulk_email(dbo, fromadd, subject, body, rows, contenttype)
        elif mode == "document":
            pass
        elif mode == "labels":
            web.header("Content-Type", "application/pdf")
            disposition = configuration.pdf_inline(dbo) and "inline; filename=%s" or "attachment; filename=%s"
            web.header("Content-Disposition", disposition % session.mergetitle + ".pdf")
            return utils.generate_label_pdf(dbo, session.locale, rows, utils.df_ks(data, "papersize"), utils.df_ks(data, "units"), 
                utils.df_kf(data, "hpitch"), utils.df_kf(data, "vpitch"), utils.df_kf(data, "width"),
                utils.df_kf(data, "height"), utils.df_kf(data, "lmargin"), utils.df_kf(data, "tmargin"),
                utils.df_ki(data, "cols"), utils.df_ki(data, "rows"))
        elif mode == "csv":
            web.header("Content-Type", "text/csv")
            web.header("Content-Disposition", u"attachment; filename=" + utils.decode_html(session.mergetitle) + u".csv")
            includeheader = 1 == utils.df_kc(data, "includeheader")
            return utils.csv(rows, cols, includeheader)

class medical:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_MEDICAL)
        l = session.locale
        dbo = session.dbo
        data = web.input(newmed = "0", offset = "m31")
        med = extmedical.get_treatments_outstanding(dbo, utils.df_ks(data, "offset"), session.locationfilter)
        profiles = extmedical.get_profiles(dbo)
        title = _("Medical Book", l)
        al.debug("got %d medical treatments" % len(med), "code.medical", dbo)
        s = html.header(title, session, "medical.js")
        c = html.controller_json("profiles", profiles)
        c += html.controller_json("rows", med)
        c += html.controller_bool("newmed", utils.df_ki(data, "newmed") == 1)
        c += html.controller_str("name", "medical")
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        data = web.input(mode="create")
        mode = utils.df_ks(data, "mode")
        if mode == "create":
            users.check_permission(session, users.ADD_MEDICAL)
            extmedical.insert_regimen_from_form(session.dbo, session.user, data)
        elif mode == "update":
            users.check_permission(session, users.CHANGE_MEDICAL)
            extmedical.update_regimen_from_form(session.dbo, session.user, data)
        elif mode == "delete_regimen":
            users.check_permission(session, users.DELETE_MEDICAL)
            for mid in utils.df_kl(data, "ids"):
                extmedical.delete_regimen(session.dbo, session.user, mid)
        elif mode == "delete_treatment":
            users.check_permission(session, users.DELETE_MEDICAL)
            for mid in utils.df_kl(data, "ids"):
                extmedical.delete_treatment(session.dbo, session.user, mid)
        elif mode == "get_profile":
            return html.json([extmedical.get_profile(session.dbo, utils.df_ki(data, "profileid"))])
        elif mode == "complete":
            users.check_permission(session, users.BULK_COMPLETE_MEDICAL)
            for mid in utils.df_kl(data, "ids"):
                extmedical.update_treatment_today(session.dbo, session.user, mid)
        elif mode == "given":
            users.check_permission(session, users.BULK_COMPLETE_MEDICAL)
            newdate = utils.df_kd(data, "newdate", session.dbo.locale)
            for mid in utils.df_kl(data, "ids"):
                extmedical.update_treatment_given(session.dbo, session.user, mid, newdate)
        elif mode == "required":
            users.check_permission(session, users.BULK_COMPLETE_MEDICAL)
            newdate = utils.df_kd(data, "newdate", session.dbo.locale)
            for mid in utils.df_kl(data, "ids"):
                extmedical.update_treatment_required(session.dbo, session.user, mid, newdate)

class medicalprofile:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_MEDICAL)
        l = session.locale
        dbo = session.dbo
        med = extmedical.get_profiles(dbo)
        title = _("Medical Profiles", l)
        al.debug("got %d medical profiles" % len(med), "code.medical_profile", dbo)
        s = html.header(title, session, "medicalprofile.js")
        c = html.controller_json("rows", med)
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        data = web.input(mode="create")
        mode = utils.df_ks(data, "mode")
        if mode == "create":
            users.check_permission(session, users.ADD_MEDICAL)
            extmedical.insert_profile_from_form(session.dbo, session.user, data)
        elif mode == "update":
            users.check_permission(session, users.CHANGE_MEDICAL)
            extmedical.update_profile_from_form(session.dbo, session.user, data)
        elif mode == "delete":
            users.check_permission(session, users.DELETE_MEDICAL)
            for mid in utils.df_kl(data, "ids"):
                extmedical.delete_profile(session.dbo, session.user, mid)

class move_adopt:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.ADD_MOVEMENT)
        l = session.locale
        dbo = session.dbo
        title = _("Adopt an animal", l)
        s = html.header(title, session, "move_adopt.js")
        c = html.controller_json("donationtypes", extlookups.get_donation_types(dbo))
        c += html.controller_json("paymenttypes", extlookups.get_payment_types(dbo))
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        dbo = session.dbo
        l = dbo.locale
        data = web.input(mode="create")
        mode = utils.df_ks(data, "mode")
        if mode == "create":
            users.check_permission(session, users.ADD_MOVEMENT)
            return str(extmovement.insert_adoption_from_form(session.dbo, session.user, data))
        elif mode == "cost":
            users.check_permission(session, users.VIEW_COST)
            dailyboardcost = extanimal.get_daily_boarding_cost(dbo, utils.df_ki(data, "id"))
            dailyboardcostdisplay = format_currency(l, dailyboardcost)
            daysonshelter = extanimal.get_days_on_shelter(dbo, utils.df_ki(data, "id"))
            totaldisplay = format_currency(l, dailyboardcost * daysonshelter)
            return totaldisplay + "||" + _("On shelter for {0} days, daily cost {1}, cost record total <b>{2}</b>", l).format(daysonshelter, dailyboardcostdisplay, totaldisplay)
        elif mode == "templates":
            return html.template_selection(dbfs.get_html_templates(dbo), "document_gen?mode=ANIMAL&id=%d" % utils.df_ki(data, "id"))
        elif mode == "donationdefault":
            return extlookups.get_donation_default(dbo, utils.df_ki(data, "donationtype"))

class move_book_foster:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_MOVEMENT)
        l = session.locale
        dbo = session.dbo
        movements = extmovement.get_movements(dbo, extmovement.FOSTER)
        al.debug("got %d movements" % len(movements), "code.move_book_foster", dbo)
        title = _("Foster Book", l)
        s = html.header(title, session, "movements.js")
        c = html.controller_json("rows", movements)
        c += html.controller_json("movementtypes", extlookups.get_movement_types(dbo))
        c += html.controller_json("returncategories", extlookups.get_entryreasons(dbo))
        c += html.controller_str("name", self.__class__.__name__)
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        data = web.input(mode="create")
        mode = utils.df_ks(data, "mode")
        if mode == "create":
            users.check_permission(session, users.ADD_MOVEMENT)
            return extmovement.insert_movement_from_form(session.dbo, session.user, data)
        elif mode == "update":
            users.check_permission(session, users.CHANGE_MOVEMENT)
            extmovement.update_movement_from_form(session.dbo, session.user, data)
        elif mode == "delete":
            users.check_permission(session, users.DELETE_MOVEMENT)
            for mid in utils.df_kl(data, "ids"):
                extmovement.delete_movement(session.dbo, session.user, mid)

class move_book_recent_adoption:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_MOVEMENT)
        l = session.locale
        dbo = session.dbo
        movements = extmovement.get_recent_adoptions(dbo)
        al.debug("got %d movements" % len(movements), "code.move_book_recent_adoption", dbo)
        title = _("Return an animal from adoption", l)
        s = html.header(title, session, "movements.js")
        c = html.controller_json("rows", movements)
        c += html.controller_json("movementtypes", extlookups.get_movement_types(dbo))
        c += html.controller_json("returncategories", extlookups.get_entryreasons(dbo))
        c += html.controller_str("name", self.__class__.__name__)
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        data = web.input(mode="create")
        mode = utils.df_ks(data, "mode")
        if mode == "create":
            users.check_permission(session, users.ADD_MOVEMENT)
            return extmovement.insert_movement_from_form(session.dbo, session.user, data)
        elif mode == "update":
            users.check_permission(session, users.CHANGE_MOVEMENT)
            extmovement.update_movement_from_form(session.dbo, session.user, data)
        elif mode == "delete":
            users.check_permission(session, users.DELETE_MOVEMENT)
            for mid in utils.df_kl(data, "ids"):
                extmovement.delete_movement(session.dbo, session.user, mid)

class move_book_recent_other:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_MOVEMENT)
        l = session.locale
        dbo = session.dbo
        movements = extmovement.get_recent_nonfosteradoption(dbo)
        al.debug("got %d movements" % len(movements), "code.move_book_recent_other", dbo)
        title = _("Return an animal from another movement", l)
        s = html.header(title, session, "movements.js")
        c = html.controller_json("rows", movements)
        c += html.controller_json("movementtypes", extlookups.get_movement_types(dbo))
        c += html.controller_json("returncategories", extlookups.get_entryreasons(dbo))
        c += html.controller_str("name", self.__class__.__name__)
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        data = web.input(mode="create")
        mode = utils.df_ks(data, "mode")
        if mode == "create":
            users.check_permission(session, users.ADD_MOVEMENT)
            return extmovement.insert_movement_from_form(session.dbo, session.user, data)
        elif mode == "update":
            users.check_permission(session, users.CHANGE_MOVEMENT)
            extmovement.update_movement_from_form(session.dbo, session.user, data)
        elif mode == "delete":
            users.check_permission(session, users.DELETE_MOVEMENT)
            for mid in utils.df_kl(data, "ids"):
                extmovement.delete_movement(session.dbo, session.user, mid)

class move_book_recent_transfer:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_MOVEMENT)
        l = session.locale
        dbo = session.dbo
        movements = extmovement.get_recent_transfers(dbo)
        al.debug("got %d movements" % len(movements), "code.move_book_recent_transfer", dbo)
        title = _("Return an animal from transfer", l)
        s = html.header(title, session, "movements.js")
        c = html.controller_json("rows", movements)
        c += html.controller_json("movementtypes", extlookups.get_movement_types(dbo))
        c += html.controller_json("returncategories", extlookups.get_entryreasons(dbo))
        c += html.controller_str("name", self.__class__.__name__)
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        data = web.input(mode="create")
        mode = utils.df_ks(data, "mode")
        if mode == "create":
            users.check_permission(session, users.ADD_MOVEMENT)
            return extmovement.insert_movement_from_form(session.dbo, session.user, data)
        elif mode == "update":
            users.check_permission(session, users.CHANGE_MOVEMENT)
            extmovement.update_movement_from_form(session.dbo, session.user, data)
        elif mode == "delete":
            users.check_permission(session, users.DELETE_MOVEMENT)
            for mid in utils.df_kl(data, "ids"):
                extmovement.delete_movement(session.dbo, session.user, mid)

class move_book_reservation:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_MOVEMENT)
        l = session.locale
        dbo = session.dbo
        movements = extmovement.get_active_reservations(dbo)
        al.debug("got %d movements" % len(movements), "code.move_book_reservation", dbo)
        title = _("Reservation Book", l)
        s = html.header(title, session, "movements.js")
        c = html.controller_json("rows", movements)
        c += html.controller_json("movementtypes", extlookups.get_movement_types(dbo))
        c += html.controller_json("returncategories", extlookups.get_entryreasons(dbo))
        c += html.controller_str("name", self.__class__.__name__)
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        data = web.input(mode="create")
        mode = utils.df_ks(data, "mode")
        if mode == "create":
            users.check_permission(session, users.ADD_MOVEMENT)
            return extmovement.insert_movement_from_form(session.dbo, session.user, data)
        elif mode == "update":
            users.check_permission(session, users.CHANGE_MOVEMENT)
            extmovement.update_movement_from_form(session.dbo, session.user, data)
        elif mode == "delete":
            users.check_permission(session, users.DELETE_MOVEMENT)
            for mid in utils.df_kl(data, "ids"):
                extmovement.delete_movement(session.dbo, session.user, mid)

class move_book_retailer:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_MOVEMENT)
        l = session.locale
        dbo = session.dbo
        movements = extmovement.get_movements(dbo, extmovement.RETAILER)
        al.debug("got %d movements" % len(movements), "code.move_book_retailer", dbo)
        title = _("Retailer Book", l)
        s = html.header(title, session, "movements.js")
        c = html.controller_json("rows", movements)
        c += html.controller_json("movementtypes", extlookups.get_movement_types(dbo))
        c += html.controller_json("returncategories", extlookups.get_entryreasons(dbo))
        c += html.controller_str("name", self.__class__.__name__)
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        data = web.input(mode="create")
        mode = utils.df_ks(data, "mode")
        if mode == "create":
            users.check_permission(session, users.ADD_MOVEMENT)
            return extmovement.insert_movement_from_form(session.dbo, session.user, data)
        elif mode == "update":
            users.check_permission(session, users.CHANGE_MOVEMENT)
            extmovement.update_movement_from_form(session.dbo, session.user, data)
        elif mode == "delete":
            users.check_permission(session, users.DELETE_MOVEMENT)
            for mid in utils.df_kl(data, "ids"):
                extmovement.delete_movement(session.dbo, session.user, mid)

class move_book_trial_adoption:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_MOVEMENT)
        l = session.locale
        dbo = session.dbo
        movements = extmovement.get_trial_adoptions(dbo)
        al.debug("got %d movements" % len(movements), "code.move_book_trial_adoption", dbo)
        title = _("Trial adoption book", l)
        s = html.header(title, session, "movements.js")
        c = html.controller_json("rows", movements)
        c += html.controller_json("movementtypes", extlookups.get_movement_types(dbo))
        c += html.controller_json("returncategories", extlookups.get_entryreasons(dbo))
        c += html.controller_str("name", self.__class__.__name__)
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        data = web.input(mode="create")
        mode = utils.df_ks(data, "mode")
        if mode == "create":
            users.check_permission(session, users.ADD_MOVEMENT)
            return extmovement.insert_movement_from_form(session.dbo, session.user, data)
        elif mode == "update":
            users.check_permission(session, users.CHANGE_MOVEMENT)
            extmovement.update_movement_from_form(session.dbo, session.user, data)
        elif mode == "delete":
            users.check_permission(session, users.DELETE_MOVEMENT)
            for mid in utils.df_kl(data, "ids"):
                extmovement.delete_movement(session.dbo, session.user, mid)

class move_book_unneutered:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_MOVEMENT)
        l = session.locale
        dbo = session.dbo
        movements = extmovement.get_recent_unneutered_adoptions(dbo)
        al.debug("got %d movements" % len(movements), "code.move_book_unneutered", dbo)
        title = _("Unaltered Adopted Animals", l)
        s = html.header(title, session, "movements.js")
        c = html.controller_json("rows", movements)
        c += html.controller_json("movementtypes", extlookups.get_movement_types(dbo))
        c += html.controller_json("returncategories", extlookups.get_entryreasons(dbo))
        c += html.controller_str("name", self.__class__.__name__)
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        data = web.input(mode="create")
        mode = utils.df_ks(data, "mode")
        if mode == "create":
            users.check_permission(session, users.ADD_MOVEMENT)
            return extmovement.insert_movement_from_form(session.dbo, session.user, data)
        elif mode == "update":
            users.check_permission(session, users.CHANGE_MOVEMENT)
            extmovement.update_movement_from_form(session.dbo, session.user, data)
        elif mode == "delete":
            users.check_permission(session, users.DELETE_MOVEMENT)
            for mid in utils.df_kl(data, "ids"):
                extmovement.delete_movement(session.dbo, session.user, mid)

class move_deceased:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.CHANGE_ANIMAL)
        l = session.locale
        dbo = session.dbo
        title = _("Mark an animal deceased", l)
        s = html.header(title, session, "move_deceased.js")
        c = html.controller_json("deathreasons", extlookups.get_deathreasons(dbo))
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        dbo = session.dbo
        data = web.input(mode="create")
        mode = utils.df_ks(data, "mode")
        if mode == "create":
            users.check_permission(session, users.CHANGE_ANIMAL)
            extanimal.update_deceased_from_form(dbo, session.user, data)

class move_foster:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.ADD_MOVEMENT)
        l = session.locale
        title = _("Foster an animal", l)
        s = html.header(title, session, "move_foster.js")
        s += html.footer()
        web.header("Content-Type", "text/html")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        dbo = session.dbo
        data = web.input(mode="create")
        mode = utils.df_ks(data, "mode")
        if mode == "create":
            users.check_permission(session, users.ADD_MOVEMENT)
            return str(extmovement.insert_foster_from_form(session.dbo, session.user, data))
        if mode == "templates":
            return html.template_selection(dbfs.get_html_templates(dbo), "document_gen?mode=ANIMAL&id=%d" % utils.df_ki(data, "id"))

class move_reserve:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.ADD_MOVEMENT)
        l = session.locale
        dbo = session.dbo
        title = _("Reserve an animal", l)
        s = html.header(title, session, "move_reserve.js")
        c = html.controller_json("donationtypes", extlookups.get_donation_types(dbo))
        c += html.controller_json("paymenttypes", extlookups.get_payment_types(dbo))
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        dbo = session.dbo
        data = web.input(mode="create")
        mode = utils.df_ks(data, "mode")
        if mode == "create":
            users.check_permission(session, users.ADD_MOVEMENT)
            return str(extmovement.insert_reserve_from_form(session.dbo, session.user, data))
        if mode == "templates":
            return html.template_selection(dbfs.get_html_templates(dbo), "document_gen?mode=ANIMAL&id=%d" % utils.df_ki(data, "id"))

class move_retailer:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.ADD_MOVEMENT)
        l = session.locale
        title = _("Move an animal to a retailer", l)
        s = html.header(title, session, "move_retailer.js")
        s += html.footer()
        web.header("Content-Type", "text/html")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        dbo = session.dbo
        data = web.input(mode="create")
        mode = utils.df_ks(data, "mode")
        if mode == "create":
            users.check_permission(session, users.ADD_MOVEMENT)
            return str(extmovement.insert_retailer_from_form(session.dbo, session.user, data))
        if mode == "templates":
            return html.template_selection(dbfs.get_html_templates(dbo), "document_gen?mode=ANIMAL&id=%d" % utils.df_ki(data, "id"))

class move_transfer:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.ADD_MOVEMENT)
        l = session.locale
        title = _("Transfer an animal", l)
        s = html.header(title, session, "move_transfer.js")
        s += html.footer()
        web.header("Content-Type", "text/html")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        dbo = session.dbo
        data = web.input(mode="create")
        mode = utils.df_ks(data, "mode")
        if mode == "create":
            users.check_permission(session, users.ADD_MOVEMENT)
            return str(extmovement.insert_transfer_from_form(session.dbo, session.user, data))
        if mode == "templates":
            return html.template_selection(dbfs.get_html_templates(dbo), "document_gen?mode=ANIMAL&id=%d" % utils.df_ki(data, "id"))

class onlineform_incoming:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_INCOMING_FORMS)
        l = session.locale
        dbo = session.dbo
        headers = extonlineform.get_onlineformincoming_headers(dbo)
        title = _("Incoming Forms", l)
        al.debug("got %d submitted headers" % len(headers), "code.onlineform_incoming", dbo)
        s = html.header(title, session, "onlineform_incoming.js")
        c = html.controller_json("rows", headers)
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        dbo = session.dbo
        data = web.input(mode="view")
        mode = utils.df_ks(data, "mode")
        personid = utils.df_ki(data, "personid")
        collationid = utils.df_ki(data, "collationid")
        web.header("Content-Type", "text/plain")
        if mode == "view":
            users.check_permission(session, users.VIEW_INCOMING_FORMS)
            return extonlineform.get_onlineformincoming_html(dbo, collationid)
        elif mode == "delete":
            users.check_permission(session, users.DELETE_INCOMING_FORMS)
            for did in utils.df_kl(data, "ids"):
                extonlineform.delete_onlineformincoming(session.dbo, session.user, did)
        elif mode == "attach":
            formname = extonlineform.get_onlineformincoming_name(dbo, collationid)
            formhtml = extonlineform.get_onlineformincoming_html(dbo, collationid)
            extmedia.create_document_media(dbo, session.user, extmedia.PERSON, personid, formname, formhtml )
            return personid 
        elif mode == "person":
            users.check_permission(session, users.ADD_PERSON)
            rv = []
            for pid in utils.df_kl(data, "ids"):
                collationid, personid, personname = extonlineform.create_person(session.dbo, session.user, pid)
                rv.append("%d|%d|%s" % (collationid, personid, personname))
            return "^$".join(rv)
        elif mode == "lostanimal":
            users.check_permission(session, users.ADD_LOST_ANIMAL)
            rv = []
            for pid in utils.df_kl(data, "ids"):
                collationid, lostanimalid, personname = extonlineform.create_lostanimal(session.dbo, session.user, pid)
                rv.append("%d|%d|%s" % (collationid, lostanimalid, personname))
            return "^$".join(rv)
        elif mode == "foundanimal":
            users.check_permission(session, users.ADD_FOUND_ANIMAL)
            rv = []
            for pid in utils.df_kl(data, "ids"):
                collationid, foundanimalid, personname = extonlineform.create_foundanimal(session.dbo, session.user, pid)
                rv.append("%d|%d|%s" % (collationid, foundanimalid, personname))
            return "^$".join(rv)
        elif mode == "waitinglist":
            users.check_permission(session, users.ADD_WAITING_LIST)
            rv = []
            for pid in utils.df_kl(data, "ids"):
                collationid, wlid, personname = extonlineform.create_waitinglist(session.dbo, session.user, pid)
                rv.append("%d|%d|%s" % (collationid, wlid, personname))
            return "^$".join(rv)

class onlineform:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.EDIT_ONLINE_FORMS)
        l = session.locale
        dbo = session.dbo
        data = web.input(formid = 0)
        formid = utils.df_ki(data, "formid")
        formname = extonlineform.get_onlineform_name(dbo, formid)
        fields = extonlineform.get_onlineformfields(dbo, formid)
        title = _("Online Form: {0}", l).format(formname)
        al.debug("got %d online form fields" % len(fields), "code.onlineform", dbo)
        s = html.header(title, session, "onlineform.js")
        c = html.controller_json("rows", fields)
        c += html.controller_int("formid", formid)
        c += html.controller_str("formname", formname)
        c += html.controller_json("formfields", extonlineform.FORM_FIELDS)
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        data = web.input(mode="create")
        mode = utils.df_ks(data, "mode")
        if mode == "create":
            users.check_permission(session, users.EDIT_ONLINE_FORMS)
            return extonlineform.insert_onlineformfield_from_form(session.dbo, session.user, data)
        elif mode == "update":
            users.check_permission(session, users.EDIT_ONLINE_FORMS)
            extonlineform.update_onlineformfield_from_form(session.dbo, session.user, data)
        elif mode == "delete":
            users.check_permission(session, users.EDIT_ONLINE_FORMS)
            for did in utils.df_kl(data, "ids"):
                extonlineform.delete_onlineformfield(session.dbo, session.user, did)

class onlineforms:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.EDIT_ONLINE_FORMS)
        l = session.locale
        dbo = session.dbo
        onlineforms = extonlineform.get_onlineforms(dbo)
        title = _("Online Forms", l)
        al.debug("got %d online forms" % len(onlineforms), "code.onlineforms", dbo)
        s = html.header(title, session, "onlineforms.js")
        c = html.controller_json("rows", onlineforms)
        c += html.controller_json("flags", extlookups.get_person_flags(dbo))
        c += html.controller_str("baseurl", BASE_URL)
        c += html.controller_json("header", html.escape_angle(extonlineform.get_onlineform_header(dbo)))
        c += html.controller_json("footer", html.escape_angle(extonlineform.get_onlineform_footer(dbo)))
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        data = web.input(mode="create")
        mode = utils.df_ks(data, "mode")
        if mode == "create":
            users.check_permission(session, users.EDIT_ONLINE_FORMS)
            return extonlineform.insert_onlineform_from_form(session.dbo, session.user, data)
        elif mode == "update":
            users.check_permission(session, users.EDIT_ONLINE_FORMS)
            extonlineform.update_onlineform_from_form(session.dbo, session.user, data)
        elif mode == "delete":
            users.check_permission(session, users.EDIT_ONLINE_FORMS)
            for did in utils.df_kl(data, "ids"):
                extonlineform.delete_onlineform(session.dbo, session.user, did)
        elif mode == "headfoot":
            users.check_permission(session, users.EDIT_ONLINE_FORMS)
            dbfs.put_string_filepath(session.dbo, "/onlineform/head.html", utils.df_ks(data, "header"))
            dbfs.put_string_filepath(session.dbo, "/onlineform/foot.html", utils.df_ks(data, "footer"))

class options:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.SYSTEM_OPTIONS)
        l = session.locale
        dbo = session.dbo
        title = _("Options", l)
        session.configuration = configuration.get_map(dbo)
        s = html.header(title, session, "options.js")
        c = html.controller_json("accounts", financial.get_accounts(dbo))
        c += html.controller_bool("hassmtpoverride", SMTP_SERVER is not None)
        c += html.controller_plain("animalfindcolumns", html.json_animalfindcolumns(dbo))
        c += html.controller_json("breeds", extlookups.get_breeds(dbo))
        c += html.controller_json("coattypes", extlookups.get_coattypes(dbo))
        c += html.controller_json("colours", extlookups.get_basecolours(dbo))
        c += html.controller_json("costtypes", extlookups.get_costtypes(dbo))
        c += html.controller_json("deathreasons", extlookups.get_deathreasons(dbo))
        c += html.controller_json("donationtypes", extlookups.get_donation_types(dbo))
        c += html.controller_json("entryreasons", extlookups.get_entryreasons(dbo))
        c += html.controller_json("locales", extlookups.LOCALES)
        c += html.controller_json("locations", extlookups.get_internal_locations(dbo))
        c += html.controller_json("logtypes", extlookups.get_log_types(dbo))
        c += html.controller_plain("personfindcolumns", html.json_personfindcolumns(dbo))
        c += html.controller_plain("quicklinks", html.json_quicklinks(dbo))
        c += html.controller_json("sizes", extlookups.get_sizes(dbo))
        c += html.controller_json("species", extlookups.get_species(dbo))
        c += html.controller_json("themes", extlookups.VISUAL_THEMES)
        c += html.controller_json("testtypes", extlookups.get_test_types(dbo))
        c += html.controller_json("types", extlookups.get_animal_types(dbo))
        c += html.controller_json("urgencies", extlookups.get_urgencies(dbo))
        c += html.controller_json("vaccinationtypes", extlookups.get_vaccination_types(dbo))
        c += html.controller_plain("waitinglistcolumns", html.json_waitinglistcolumns(dbo))
        al.debug("lookups loaded", "code.options", dbo)
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        data = web.input(mode="save")
        mode = utils.df_ks(data, "mode")
        if mode == "save":
            users.check_permission(session, users.SYSTEM_OPTIONS)
            configuration.csave(session.dbo, session.user, data)
            users.update_session(session)

class person:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_PERSON)
        dbo = session.dbo
        data = web.input(id = 0)
        p = extperson.get_person(dbo, utils.df_ki(data, "id"))
        if p is None: raise web.notfound()
        if p["ISSTAFF"] == 1:
            users.check_permission(session, users.VIEW_STAFF)
        title = p["OWNERNAME"]
        al.debug("opened person '%s'" % p["OWNERNAME"], "code.person", dbo)
        s = html.header(title, session, "person.js")
        c = html.controller_json("additional", extadditional.get_additional_fields(dbo, p["ID"], "person"))
        c += html.controller_json("animaltypes", extlookups.get_animal_types(dbo))
        c += html.controller_json("species", extlookups.get_species(dbo))
        c += html.controller_json("breeds", extlookups.get_breeds_by_species(dbo))
        c += html.controller_json("colours", extlookups.get_basecolours(dbo))
        c += html.controller_json("diarytasks", extdiary.get_person_tasks(dbo))
        c += html.controller_json("flags", extlookups.get_person_flags(dbo))
        c += html.controller_json("ynun", extlookups.get_ynun(dbo))
        c += html.controller_json("homecheckhistory", extperson.get_homechecked(dbo, utils.df_ki(data, "id")))
        c += html.controller_json("logtypes", extlookups.get_log_types(dbo))
        c += html.controller_json("sexes", extlookups.get_sexes(dbo))
        c += html.controller_json("sizes", extlookups.get_sizes(dbo))
        c += html.controller_str("towns", "|".join(extperson.get_towns(dbo)))
        c += html.controller_str("counties", "|".join(extperson.get_counties(dbo)))
        c += html.controller_str("towncounties", "|".join(extperson.get_town_to_county(dbo)))
        c += html.controller_json("tabcounts", extperson.get_satellite_counts(dbo, p["ID"])[0])
        c += html.controller_json("templates", dbfs.get_html_templates(dbo))
        c += html.controller_json("person", p)
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        dbo = session.dbo
        data = web.input(mode="save")
        mode = utils.df_ks(data, "mode")
        if mode == "save":
            users.check_permission(session, users.CHANGE_PERSON)
            extperson.update_person_from_form(dbo, data, session.user)
        elif mode == "delete":
            users.check_permission(session, users.DELETE_PERSON)
            extperson.delete_person(dbo, session.user, utils.df_ki(data, "personid"))
        elif mode == "email":
            users.check_permission(session, users.VIEW_PERSON)
            extperson.send_email_from_form(dbo, session.user, data)
        elif mode == "latlong":
            users.check_permission(session, users.CHANGE_PERSON)
            extperson.update_latlong(dbo, utils.df_ki(data, "personid"), utils.df_ks(data, "latlong"))
        elif mode == "merge":
            users.check_permission(session, users.CHANGE_PERSON)
            users.check_permission(session, users.DELETE_PERSON)
            extperson.merge_person(dbo, session.user, utils.df_ki(data, "personid"), utils.df_ki(data, "mergepersonid"))

class person_diary:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_DIARY)
        dbo = session.dbo
        data = web.input(id = 0)
        p = extperson.get_person(dbo, utils.df_ki(data, "id"))
        if p is None: raise web.notfound()
        title = p["OWNERNAME"]
        diaries = extdiary.get_diaries(dbo, extdiary.PERSON, utils.df_ki(data, "id"))
        al.debug("got %d diaries" % len(diaries), "code.person_diary", dbo)
        s = html.header(title, session, "diary.js")
        c = html.controller_json("rows", diaries)
        c += html.controller_json("person", p)
        c += html.controller_json("tabcounts", extperson.get_satellite_counts(dbo, p["ID"])[0])
        c += html.controller_str("name", "person_diary")
        c += html.controller_int("linkid", p["ID"])
        c += html.controller_json("forlist", users.get_users_and_roles(dbo))
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        data = web.input(mode="create")
        mode = utils.df_ks(data, "mode")
        if mode == "create":
            users.check_permission(session, users.ADD_DIARY)
            return extdiary.insert_diary_from_form(session.dbo, session.user, extdiary.PERSON, utils.df_ki(data, "linkid"), data)
        elif mode == "update":
            users.check_permission(session, users.EDIT_ALL_DIARY_NOTES)
            extdiary.update_diary_from_form(session.dbo, session.user, data)
        elif mode == "delete":
            users.check_permission(session, users.DELETE_DIARY)
            for did in utils.df_kl(data, "ids"):
                extdiary.delete_diary(session.dbo, session.user, did)
        elif mode == "complete":
            users.check_permission(session, users.BULK_COMPLETE_NOTES)
            for did in utils.df_kl(data, "ids"):
                extdiary.complete_diary_note(session.dbo, session.user, did)

class person_donations:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_DONATION)
        dbo = session.dbo
        data = web.input(id = 0)
        p = extperson.get_person(dbo, utils.df_ki(data, "id"))
        if p is None: raise web.notfound()
        title = p["OWNERNAME"]
        donations = financial.get_person_donations(dbo, utils.df_ki(data, "id"))
        s = html.header(title, session, "donations.js")
        c = html.controller_json("person", p)
        c += html.controller_json("tabcounts", extperson.get_satellite_counts(dbo, p["ID"])[0])
        c += html.controller_str("name", "person_donations")
        c += html.controller_json("donationtypes", extlookups.get_donation_types(dbo))
        c += html.controller_json("paymenttypes", extlookups.get_payment_types(dbo))
        c += html.controller_json("frequencies", extlookups.get_donation_frequencies(dbo))
        c += html.controller_json("templates", dbfs.get_html_templates(dbo))
        c += html.controller_json("rows", donations)
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        data = web.input(mode="create")
        mode = utils.df_ks(data, "mode")
        dbo = session.dbo
        if mode == "create":
            users.check_permission(session, users.ADD_DONATION)
            return financial.insert_donation_from_form(dbo, session.user, data)
        elif mode == "update":
            users.check_permission(session, users.CHANGE_DONATION)
            financial.update_donation_from_form(dbo, session.user, data)
        elif mode == "delete":
            users.check_permission(session, users.DELETE_DONATION)
            for did in utils.df_kl(data, "ids"):
                financial.delete_donation(dbo, session.user, did)
        elif mode == "receive":
            users.check_permission(session, users.CHANGE_DONATION)
            for did in utils.df_kl(data, "ids"):
                financial.receive_donation(dbo, session.user, did)
        elif mode == "personmovements":
            users.check_permission(session, users.VIEW_MOVEMENT)
            return html.json(extmovement.get_person_movements(dbo, utils.df_ki(data, "personid")))

class person_embed:
    def GET(self):
        utils.check_loggedin(session, web)
        dbo = session.dbo
        data = web.input(mode = "lookup")
        mode = utils.df_ks(data, "mode")
        if mode == "lookup":
            rv = {}
            rv["towns"] = "|".join(extperson.get_towns(dbo))
            rv["counties"] = "|".join(extperson.get_counties(dbo))
            rv["towncounties"] = "|".join(extperson.get_town_to_county(dbo))
            rv["flags"] = extlookups.get_person_flags(dbo)
            web.header("Content-Type", "application/json")
            web.header("Cache-Control", "max-age=60")
            return html.json(rv)

    def POST(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_PERSON)
        dbo = session.dbo
        data = web.input(mode = "find", filter = "all", id = 0)
        mode = utils.df_ks(data, "mode")
        q = utils.df_ks(data, "q")
        web.header("Content-Type", "application/json")
        if mode == "find":
            rows = extperson.get_person_find_simple(dbo, q, utils.df_ks(data, "filter"), users.check_permission_bool(session, users.VIEW_STAFF), 100)
            al.debug("find '%s' got %d rows" % (str(web.ctx.query), len(rows)), "code.person_embed", dbo)
            return html.json(rows)
        elif mode == "id":
            p = extperson.get_person(dbo, utils.df_ki(data, "id"))
            if p is None:
                al.error("get person by id %d found no records." % (utils.df_ki(data, "id")), "code.person_embed", dbo)
                raise web.notfound()
            else:
                al.debug("get person by id %d got '%s'" % (utils.df_ki(data, "id"), p["OWNERNAME"]), "code.person_embed", dbo)
                return html.json((p,))
        elif mode == "similar":
            surname = utils.df_ks(data, "surname")
            forenames = utils.df_ks(data, "forenames")
            address = utils.df_ks(data, "address")
            p = extperson.get_person_similar(dbo, surname, forenames, address)
            if len(p) == 0:
                al.debug("No similar people found for %s, %s, %s" % (surname, forenames, address), "code.person_embed", dbo)
            else:
                al.debug("found similar people for %s, %s, %s: got %d records" % (surname, forenames, address, len(p)), "code.person_embed", dbo)
            return html.json(p)
        elif mode == "add":
            users.check_permission(session, users.ADD_PERSON)
            al.debug("add new person", "code.person_embed", dbo)
            pid = extperson.insert_person_from_form(dbo, data, session.user)
            p = extperson.get_person(dbo, pid)
            return html.json((p,))

class person_find:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_PERSON)
        l = session.locale
        dbo = session.dbo
        title = _("Find Person", l)
        flags = extlookups.get_person_flags(dbo)
        al.debug("lookups loaded", "code.person_find", dbo)
        s = html.header(title, session, "person_find.js")
        c = html.controller_json("flags", flags)
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        return s

class person_find_results:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_PERSON)
        dbo = session.dbo
        l = session.locale
        data = web.input(mode = "", q = "")
        mode = utils.df_ks(data, "mode")
        q = utils.df_ks(data, "q")
        if mode == "SIMPLE":
            results = extperson.get_person_find_simple(dbo, q, "all", users.check_permission_bool(session, users.VIEW_STAFF), configuration.record_search_limit(dbo))
        else:
            results = extperson.get_person_find_advanced(dbo, data, users.check_permission_bool(session, users.VIEW_STAFF), configuration.record_search_limit(dbo))
        add = None
        if len(results) > 0: 
            add = extadditional.get_additional_fields_ids(dbo, results, "person")
        title = _("Results", l)
        al.debug("found %d results for %s" % (len(results), str(web.ctx.query)), "code.person_find_results", dbo)
        s = html.header(title, session, "person_find_results.js")
        c = html.controller_json("rows", results)
        c += html.controller_json("additional", add)
        c += html.controller_str("resultsmessage", _("Search returned {0} results.", l).format(len(results)))
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

class person_investigation:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_INVESTIGATION)
        dbo = session.dbo
        data = web.input(id = 0)
        p = extperson.get_person(dbo, utils.df_ki(data, "id"))
        if p is None: raise web.notfound()
        title = p["OWNERNAME"]
        investigation = extperson.get_investigation(dbo, utils.df_ki(data, "id"))
        al.debug("got %d investigation records for person %s" % (len(investigation), p["OWNERNAME"]), "code.person_investigation", dbo)
        s = html.header(title, session, "person_investigation.js")
        c = html.controller_json("rows", investigation)
        c += html.controller_json("person", p)
        c += html.controller_json("tabcounts", extperson.get_satellite_counts(dbo, p["ID"])[0])
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        data = web.input(mode="create")
        mode = utils.df_ks(data, "mode")
        if mode == "create":
            users.check_permission(session, users.ADD_INVESTIGATION)
            return str(extperson.insert_investigation_from_form(session.dbo, session.user, data))
        elif mode == "update":
            users.check_permission(session, users.CHANGE_INVESTIGATION)
            extperson.update_investigation_from_form(session.dbo, session.user, data)
        elif mode == "delete":
            users.check_permission(session, users.DELETE_INVESTIGATION)
            for did in utils.df_kl(data, "ids"):
                extperson.delete_investigation(session.dbo, session.user, did)

class person_log:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_LOG)
        dbo = session.dbo
        data = web.input(id = 0, filter = -2)
        logfilter = utils.df_ki(data, "filter")
        if logfilter == -2: logfilter = configuration.default_log_filter(dbo)
        p = extperson.get_person(dbo, utils.df_ki(data, "id"))
        if p is None: raise web.notfound()
        title = p["OWNERNAME"]
        logs = extlog.get_logs(dbo, extlog.PERSON, utils.df_ki(data, "id"), logfilter)
        s = html.header(title, session, "log.js")
        c = html.controller_str("name", "person_log")
        c += html.controller_int("linkid", utils.df_ki(data, "id"))
        c += html.controller_int("filter", logfilter)
        c += html.controller_json("rows", logs)
        c += html.controller_json("person", p)
        c += html.controller_json("tabcounts", extperson.get_satellite_counts(dbo, p["ID"])[0])
        c += html.controller_json("logtypes", extlookups.get_log_types(dbo))
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        data = web.input(mode="create")
        mode = utils.df_ks(data, "mode")
        if mode == "create":
            users.check_permission(session, users.ADD_LOG)
            return extlog.insert_log_from_form(session.dbo, session.user, extlog.PERSON, utils.df_ki(data, "linkid"), data)
        elif mode == "update":
            users.check_permission(session, users.CHANGE_LOG)
            extlog.update_log_from_form(session.dbo, session.user, data)
        elif mode == "delete":
            users.check_permission(session, users.DELETE_LOG)
            for lid in utils.df_kl(data, "ids"):
                extlog.delete_log(session.dbo, session.user, lid)

class person_lookingfor:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_PERSON)
        dbo = session.dbo
        web.header("Content-Type", "text/html")
        return dbfs.get_string_filepath(dbo, "/reports/daily/lookingfor.html")

class person_links:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_PERSON_LINKS)
        dbo = session.dbo
        data = web.input(id = 0)
        links = extperson.get_links(dbo, utils.df_ki(data, "id"))
        p = extperson.get_person(dbo, utils.df_ki(data, "id"))
        if p is None: raise web.notfound()
        title = p["OWNERNAME"]
        s = html.header(title, session, "person_links.js")
        al.debug("got %d person links" % len(links), "code.person_links", dbo)
        c = html.controller_json("links", links)
        c += html.controller_json("person", p)
        c += html.controller_json("tabcounts", extperson.get_satellite_counts(dbo, p["ID"])[0])
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

class person_media:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_MEDIA)
        dbo = session.dbo
        data = web.input(id = 0)
        p = extperson.get_person(dbo, utils.df_ki(data, "id"))
        if p is None: raise web.notfound()
        title = p["OWNERNAME"]
        m = extmedia.get_media(dbo, extmedia.PERSON, utils.df_ki(data, "id"))
        al.debug("got %d media" % len(m), "code.person_media", dbo)
        s = html.header(title, session, "media.js")
        c = html.controller_json("media", m)
        c += html.controller_json("person", p)
        c += html.controller_json("tabcounts", extperson.get_satellite_counts(dbo, p["ID"])[0])
        c += html.controller_bool("showPreferred", True)
        c += html.controller_int("linkid", utils.df_ki(data, "id"))
        c += html.controller_int("linktypeid", extmedia.PERSON)
        c += html.controller_str("name", self.__class__.__name__)
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        data = web.input(mode="create", filechooser={}, linkid="0", base64image = "", _unicode=False)
        mode = utils.df_ks(data, "mode")
        dbo = session.dbo
        l = session.locale
        linkid = utils.df_ki(data, "linkid")
        if mode == "create":
            users.check_permission(session, users.ADD_MEDIA)
            extmedia.attach_file_from_form(dbo, session.user, extmedia.PERSON, linkid, data)
            raise web.seeother("person_media?id=%d" % linkid)
        elif mode == "createdoc":
            users.check_permission(session, users.ADD_MEDIA)
            mediaid = extmedia.create_blank_document_media(dbo, session.user, extmedia.PERSON, linkid)
            raise web.seeother("document_media_edit?id=%d&redirecturl=person_media?id=%d" % (mediaid, linkid))
        elif mode == "createlink":
            users.check_permission(session, users.ADD_MEDIA)
            mediaid = extmedia.attach_link_from_form(session.dbo, session.user, extmedia.PERSON, linkid, data)
            raise web.seeother("person_media?id=%d" % linkid)
        elif mode == "update":
            users.check_permission(session, users.CHANGE_MEDIA)
            extmedia.update_media_notes(dbo, session.user, utils.df_ki(data, "mediaid"), utils.df_ks(data, "comments"))
        elif mode == "delete":
            users.check_permission(session, users.DELETE_MEDIA)
            for mid in utils.df_kl(data, "ids"):
                extmedia.delete_media(dbo, session.user, mid)
        elif mode == "email":
            users.check_permission(session, users.MAIL_MERGE)
            emailadd = utils.df_ks(data, "email")
            if emailadd == "" or emailadd.find("@") == -1:
                raise utils.ASMValidationError(_("Invalid email address", l))
            for mid in utils.df_kl(data, "ids"):
                m = extmedia.get_media_by_id(dbo, mid)
                if len(m) == 0: raise web.notfound()
                m = m[0]
                content = dbfs.get_string(dbo, m["MEDIANAME"])
                content = utils.fix_relative_document_uris(content, BASE_URL, MULTIPLE_DATABASES and dbo.database or "")
                utils.send_email(dbo, configuration.email(dbo), emailadd, "", m["MEDIANOTES"], content, "html")
                return emailadd
        elif mode == "rotateclock":
            users.check_permission(session, users.CHANGE_MEDIA)
            for mid in utils.df_kl(data, "ids"):
                extmedia.rotate_media(dbo, session.user, mid, True)
        elif mode == "rotateanti":
            users.check_permission(session, users.CHANGE_MEDIA)
            for mid in utils.df_kl(data, "ids"):
                extmedia.rotate_media(dbo, session.user, mid, False)
        elif mode == "web":
            users.check_permission(session, users.CHANGE_MEDIA)
            mid = utils.df_kl(data, "ids")[0]
            extmedia.set_web_preferred(dbo, session.user, mid)
        elif mode == "video":
            users.check_permission(session, users.CHANGE_MEDIA)
            mid = utils.df_kl(data, "ids")[0]
            extmedia.set_video_preferred(session.dbo, session.user, mid)
        elif mode == "doc":
            users.check_permission(session, users.CHANGE_MEDIA)
            mid = utils.df_kl(data, "ids")[0]
            extmedia.set_doc_preferred(dbo, session.user, mid)

class person_movements:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_MOVEMENT)
        dbo = session.dbo
        data = web.input(id = 0)
        p = extperson.get_person(dbo, utils.df_ki(data, "id"))
        if p is None: raise web.notfound()
        title = p["OWNERNAME"]
        movements = extmovement.get_person_movements(dbo, utils.df_ki(data, "id"))
        al.debug("got %d movements" % len(movements), "code.person_movements", dbo)
        s = html.header(title, session, "movements.js")
        c = html.controller_json("rows", movements)
        c += html.controller_json("person", p)
        c += html.controller_json("tabcounts", extperson.get_satellite_counts(dbo, p["ID"])[0])
        c += html.controller_json("movementtypes", extlookups.get_movement_types(dbo))
        c += html.controller_json("returncategories", extlookups.get_entryreasons(dbo))
        c += html.controller_str("name", self.__class__.__name__)
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        data = web.input(mode="create")
        mode = utils.df_ks(data, "mode")
        if mode == "create":
            users.check_permission(session, users.ADD_MOVEMENT)
            return extmovement.insert_movement_from_form(session.dbo, session.user, data)
        elif mode == "update":
            users.check_permission(session, users.CHANGE_MOVEMENT)
            extmovement.update_movement_from_form(session.dbo, session.user, data)
        elif mode == "delete":
            users.check_permission(session, users.DELETE_MOVEMENT)
            for mid in utils.df_kl(data, "ids"):
                extmovement.delete_movement(session.dbo, session.user, mid)
        elif mode == "insurance":
            return extmovement.generate_insurance_number(session.dbo)

class person_new:
    def GET(self):
        utils.check_loggedin(session, web)
        l = session.locale
        dbo = session.dbo
        title = _("Add a new person", l)
        s = html.header(title, session, "person_new.js")
        c = html.controller_str("towns", "|".join(extperson.get_towns(dbo)))
        c += html.controller_str("counties", "|".join(extperson.get_counties(dbo)))
        c += html.controller_str("towncounties", "|".join(extperson.get_town_to_county(dbo)))
        c += html.controller_json("flags", extlookups.get_person_flags(dbo))
        s += html.controller(c)
        s += html.footer()
        al.debug("add person", "code.person_new", dbo)
        web.header("Content-Type", "text/html")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.ADD_PERSON)
        utils.check_locked_db(session)
        data = web.input()
        personid = extperson.insert_person_from_form(session.dbo, data, session.user)
        return str(personid)

class person_vouchers:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_VOUCHER)
        dbo = session.dbo
        data = web.input(id = 0)
        p = extperson.get_person(dbo, utils.df_ki(data, "id"))
        if p is None: raise web.notfound()
        title = p["OWNERNAME"]
        vouchers = financial.get_vouchers(dbo, utils.df_ki(data, "id"))
        al.debug("got %d vouchers" % len(vouchers), "code.person_vouchers", dbo)
        s = html.header(title, session, "person_vouchers.js")
        c = html.controller_json("vouchertypes", extlookups.get_voucher_types(dbo))
        c += html.controller_json("rows", vouchers)
        c += html.controller_json("person", p)
        c += html.controller_json("tabcounts", extperson.get_satellite_counts(dbo, p["ID"])[0])
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        data = web.input(mode="create")
        mode = utils.df_ks(data, "mode")
        if mode == "create":
            users.check_permission(session, users.ADD_VOUCHER)
            return financial.insert_voucher_from_form(session.dbo, session.user, data)
        elif mode == "update":
            users.check_permission(session, users.CHANGE_VOUCHER)
            financial.update_voucher_from_form(session.dbo, session.user, data)
        elif mode == "delete":
            users.check_permission(session, users.DELETE_VOUCHER)
            for vid in utils.df_kl(data, "ids"):
                financial.delete_voucher(session.dbo, session.user, vid)

class publish:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.USE_INTERNET_PUBLISHER)
        l = session.locale
        dbo = session.dbo
        data = web.input(mode="page")
        mode = utils.df_ks(data, "mode")
        failed = False
        al.debug("publish started for mode %s" % mode, "code.publish", dbo)
        # If a publisher is already running and we have a mode, mark
        # a failure starting
        execstr = configuration.publisher_executing(dbo)
        failed = not execstr.startswith("NONE") and not execstr.endswith("100")
        if failed:
            al.debug("publish already running, not starting new publish", "code.publish", dbo)
        else:
            # If a publishing mode is requested, start that publisher
            # running on a background thread
            pc = extpublish.PublishCriteria(configuration.publisher_presets(dbo))
            if mode == "ftp":
                h = extpublish.HTMLPublisher(dbo, pc, session.user)
                h.start()
            if mode == "pf": 
                pf = extpublish.PetFinderPublisher(dbo, pc)
                pf.start()
            if mode == "ap": 
                ap = extpublish.AdoptAPetPublisher(dbo, pc)
                ap.start()
            if mode == "rg": 
                rg = extpublish.RescueGroupsPublisher(dbo, pc)
                rg.start()
            if mode == "mp": 
                mp = extpublish.MeetAPetPublisher(dbo, pc)
                mp.start()
            if mode == "hlp": 
                mp = extpublish.HelpingLostPetsPublisher(dbo, pc)
                mp.start()
            if mode == "pl": 
                mp = extpublish.PetLinkPublisher(dbo, pc)
                mp.start()
            if mode == "p9": 
                pn = extpublish.Pets911Publisher(dbo, pc)
                pn.start()
            if mode == "st": 
                st = extpublish.SmartTagPublisher(dbo, pc)
                st.start()
        s = html.header(_("Publishing", l), session, "publish.js")
        c = html.controller_bool("failed", failed)
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        data = web.input(mode="poll")
        mode = utils.df_ks(data, "mode")
        dbo = session.dbo
        if mode == "poll":
            users.check_permission(session, users.USE_INTERNET_PUBLISHER)
            return configuration.publisher_executing(dbo) + "|" + configuration.publisher_last_error(dbo)
        elif mode == "stop":
            configuration.publisher_stop(dbo, "Yes")
            configuration.publisher_executing(dbo, "NONE", 0)

class publish_logs:
    def GET(self):
        utils.check_loggedin(session, web)
        dbo = session.dbo
        l = session.locale
        data = web.input(view = "")
        if utils.df_ks(data, "view") == "":
            title = _("Publisher Logs", l)
            s = html.header(title, session, "publish_logs.js")
            logs = dbfs.get_publish_logs(dbo)
            al.debug("viewing %d publishing logs" % len(logs), "code.publish_logs", dbo)
            c = html.controller_json("rows", logs)
            s += html.controller(c)
            s += html.footer()
            web.header("Content-Type", "text/html")
            web.header("Cache-Control", "no-cache")
            return s
        else:
            al.debug("viewing log file %s" % utils.df_ks(data, "view"), "code.publish_logs", dbo)
            web.header("Content-Type", "text/plain")
            web.header("Cache-Control", "max-age=10000000")
            web.header("Content-Disposition", "inline; filename=\"%s\"" % utils.df_ks(data, "view"))
            return dbfs.get_string_filepath(dbo, utils.df_ks(data, "view"))

class publish_options:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.SYSTEM_OPTIONS)
        l = session.locale
        dbo = session.dbo
        title = _("Publishing Options", l)
        s = html.header(title, session, "publish_options.js")
        c = html.controller_json("locations", extlookups.get_internal_locations(dbo))
        c += html.controller_str("publishurl", MULTIPLE_DATABASES_PUBLISH_URL)
        c += html.controller_bool("hasftpoverride", MULTIPLE_DATABASES_PUBLISH_FTP is not None and not configuration.publisher_ignore_ftp_override(dbo))
        c += html.controller_bool("hasfacebook", FACEBOOK_CLIENT_ID != "")
        c += html.controller_json("logtypes", extlookups.get_log_types(dbo))
        c += html.controller_json("styles", dbfs.get_html_publisher_templates(dbo))
        s += html.controller(c)
        al.debug("loaded lookups", "code.publish_options", dbo)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        data = web.input(mode="save")
        mode = utils.df_ks(data, "mode")
        if mode == "save":
            users.check_permission(session, users.SYSTEM_OPTIONS)
            configuration.csave(session.dbo, session.user, data)
            users.update_session(session)

class report:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_REPORT)
        data = web.input(id = "0", mode = "criteria")
        mode = utils.df_ks(data, "mode")
        dbo = session.dbo
        user = session.user
        crid = utils.df_ki(data, "id")
        # Make sure this user has a role that can view the report
        extreports.check_view_permission(session, crid)
        crit = extreports.get_criteria_controls(session.dbo, crid, locationfilter = session.locationfilter) 
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        # If the report doesn't take criteria, just show it
        if crit == "":
            al.debug("report %d has no criteria, displaying" % crid, "code.report", dbo)
            return extreports.execute(dbo, crid, user)
        # If we're in criteria mode (and there are some to get here), ask for them
        elif mode == "criteria":
            title = extreports.get_title(dbo, crid)
            al.debug("building criteria form for report %d %s" % (crid, title), "code.report", dbo)
            s = html.header(title, session, "report.js")
            s += html.heading(title)
            s += "<div id=\"criteriaform\">"
            s += "<input data-post=\"id\" type=\"hidden\" value=\"%d\" />" % crid
            s += "<input data-post=\"mode\" type=\"hidden\" value=\"exec\" />"
            s += crit
            s += "</div>"
            s += html.footing()
            s += html.footer()
            return s
        # The user has entered the criteria and we're in exec mode, unpack
        # the criteria and run the report
        elif mode == "exec":
            al.debug("got criteria (%s), executing report %d" % (str(data), crid), "code.report", dbo)
            p = extreports.get_criteria_params(dbo, crid, data)
            return extreports.execute(dbo, crid, user, p)

class report_images:
    def GET(self):
        utils.check_loggedin(session, web)
        dbo = session.dbo
        l = session.locale
        title = _("Extra images", l)
        images = dbfs.get_report_images(dbo)
        al.debug("got %d extra images" % len(images), "code.report_images", dbo)
        s = html.header(title, session, "report_images.js")
        c = html.controller_json("rows", images)
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        dbo = session.dbo
        data = web.input(mode="create", filechooser={})
        mode = utils.df_ks(data, "mode")
        if mode == "create":
            dbfs.upload_report_image(dbo, data.filechooser)
            users.update_session(session)
            raise web.seeother("report_images")
        if mode == "delete":
            for i in utils.df_kl(data, "ids"):
                if i != "" and not i.endswith("nopic.jpg"): dbfs.delete_filepath(dbo, "/reports/" + i)
            users.update_session(session)

class reports:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_REPORT)
        l = session.locale
        dbo = session.dbo
        reports = extreports.get_reports(dbo)
        # Sanitise the HTMLBODY for sending to the front end
        for r in reports:
            r["HTMLBODY"] = html.escape_angle(r["HTMLBODY"])
        header = dbfs.get_string(dbo, "head.html", "/reports")
        if header == "": header = dbfs.get_string(dbo, "head.dat", "/reports")
        footer = dbfs.get_string(dbo, "foot.html", "/reports")
        if footer == "": footer = dbfs.get_string(dbo, "foot.dat", "/reports")
        title = _("Edit Reports", l)
        al.debug("editing %d reports" % len(reports), "code.reports", dbo)
        s = html.header(title, session, "reports.js")
        c = html.controller_json("categories", "|".join(extreports.get_categories(dbo)))
        c += html.controller_json("header", html.escape_angle(header))
        c += html.controller_json("footer", html.escape_angle(footer))
        c += html.controller_json("roles", users.get_roles(dbo))
        c += html.controller_json("rows", reports)
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        data = web.input(mode="create")
        mode = utils.df_ks(data, "mode")
        dbo = session.dbo
        l = dbo.locale
        if mode == "create":
            users.check_permission(session, users.ADD_REPORT)
            rid = extreports.insert_report_from_form(dbo, session.user, data)
            users.update_session(session)
            return rid
        elif mode == "update":
            users.check_permission(session, users.CHANGE_REPORT)
            extreports.update_report_from_form(dbo, session.user, data)
            users.update_session(session)
        elif mode == "delete":
            users.check_permission(session, users.DELETE_REPORT)
            for rid in utils.df_kl(data, "ids"):
                extreports.delete_report(dbo, session.user, rid)
            users.update_session(session)
        elif mode == "sql":
            users.check_permission(session, users.USE_SQL_INTERFACE)
            extreports.check_sql(dbo, session.user, utils.df_ks(data, "sql"))
        elif mode == "genhtml":
            users.check_permission(session, users.USE_SQL_INTERFACE)
            return extreports.generate_html(dbo, session.user, utils.df_ks(data, "sql"))
        elif mode == "headfoot":
            users.check_permission(session, users.CHANGE_REPORT)
            dbfs.put_string_filepath(dbo, "/reports/head.html", utils.df_ks(data, "header"))
            dbfs.put_string_filepath(dbo, "/reports/foot.html", utils.df_ks(data, "footer"))
        elif mode == "smcomlist":
            return html.smcom_report_list_table(l, extreports.get_smcom_reports(dbo))
        elif mode == "smcominstall":
            users.check_permission(session, users.ADD_REPORT)
            extreports.install_smcom_reports(dbo, session.user, utils.df_kl(data, "ids"))
            users.update_session(session)

class roles:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.EDIT_USER)
        dbo = session.dbo
        l = session.locale
        roles = users.get_roles(dbo)
        title = _("Edit roles", l)
        al.debug("editing %d roles" % len(roles), "code.roles", dbo)
        s = html.header(title, session, "roles.js")
        c = html.controller_json("rows", roles)
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        data = web.input(mode="create")
        mode = utils.df_ks(data, "mode")
        if mode == "create":
            users.check_permission(session, users.EDIT_USER)
            users.insert_role_from_form(session.dbo, session.user, data)
        elif mode == "update":
            users.check_permission(session, users.EDIT_USER)
            users.update_role_from_form(session.dbo, session.user, data)
        elif mode == "delete":
            users.check_permission(session, users.EDIT_USER)
            for rid in utils.df_kl(data, "ids"):
                users.delete_role(session.dbo, session.user, rid)

class search:
    def GET(self):
        utils.check_loggedin(session, web)
        dbo = session.dbo
        l = session.locale
        data = web.input()
        q = utils.df_ks(data, "q")
        title = _("Search Results for '{0}'", l).format(q)
        results, timetaken, explain, sortname = extsearch.search(dbo, session, q)
        is_large_db = ""
        if dbo.is_large_db: is_large_db = " (indexed only)"
        al.debug("searched for '%s', got %d results in %s, sorted %s %s" % (q, len(results), timetaken, sortname, is_large_db), "code.search", dbo)
        s = html.header(title, session, "search.js")
        c = html.controller_json("results", results)
        c += html.controller_str("timetaken", str(round(timetaken, 2)))
        c += html.controller_str("explain", explain)
        c += html.controller_str("sortname", sortname)
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

class service:
    def handle(self):
        data = web.input(filechooser = {})
        contenttype, maxage, response = extservice.handler(data, remote_ip(),  web.ctx.env.get("HTTP_REFERER", ""))
        if contenttype == "redirect":
            raise web.seeother(response)
        else:
            web.header("Content-Type", contenttype)
            web.header("Cache-Control", "max-age=%d" % maxage)
            return response
    def POST(self):
        return self.handle()
    def GET(self):
        return self.handle()

class shelterview:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_ANIMAL)
        l = session.locale
        dbo = session.dbo
        animals = extanimal.get_shelterview_animals(dbo, session.locationfilter)
        perrow = configuration.main_screen_animal_link_max(dbo)
        title = _("Shelter view", l)
        al.debug("got %d animals for shelterview" % (len(animals)), "code.shelterview", dbo)
        s = html.header(title, session, "shelterview.js")
        c = html.controller_json("animals", extanimal.get_animals_brief(animals))
        c += html.controller_int("perrow", perrow)
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        data = web.input(mode="move")
        mode = utils.df_ks(data, "mode")
        if mode == "move":
            users.check_permission(session, users.CHANGE_ANIMAL)
            extanimal.update_location(session.dbo, utils.df_ki(data, "animalid"), utils.df_ki(data, "locationid"))

class spellcheck:
    def POST(self):
        utils.check_loggedin(session, web)
        dbo = session.dbo
        data = web.data()
        try:
            jreq = html.json_parse(data)
            al.debug("spell check request: " + str(jreq), "code.spellcheck", dbo)
            cid = jreq["id"]
            method = jreq["method"]
            params = jreq["params"]
            if method == "checkWords":
                # TinyMCE 3.x
                lang = params[0]
                badwords = []
                for word in params[1]:
                    word = word.encode("ascii", "xmlcharrefreplace")
                    aresp = os.popen("echo \"%s\" | aspell -a -l %s" % (word, lang)).readlines()
                    for ap in aresp:
                        if ap.startswith("&"):
                            badwords.append(ap.split(" ")[1])
                sresp =  "{'id': '%s', 'result': %s, 'error': null}" % (cid, badwords)
                al.debug("spell check response: %s" % sresp, "code.spellcheck", dbo)
                return sresp
            elif method == "getSuggestions":
                # TinyMCE 3.x
                lang = params[0]
                word = params[1]
                word = word.encode("ascii", "xmlcharrefreplace")
                aresp = os.popen("echo \"%s\" | aspell -a -l %s" % (word, lang)).readlines()
                suggestions = []
                for ap in aresp:
                    if ap.startswith("&"):
                        suggestions = ap[ap.find(":")+1:].split(",")
                sresp =  "{'id': '%s', 'result': %s, 'error': null}" % (cid, suggestions)
                al.debug("spell check response: %s" % sresp, "code.spellcheck", dbo)
                return sresp
            elif method == "spellcheck":
                # TinyMCE 4.x does wordchecks and suggestions with a single call,
                # the response is an object using mispelled words as the key with
                # suggestions
                lang = params["lang"]
                badwords = {}
                for word in params["words"]:
                    word = word.encode("ascii", "xmlcharrefreplace")
                    aresp = os.popen("echo \"%s\" | aspell -a -l %s" % (word, lang)).readlines()
                    for ap in aresp:
                        if ap.startswith("&"):
                            badwords[word] = ap[ap.find(":")+2:].split(", ")
                sresp =  "{'id': '%s', 'result': %s, 'error': null}" % (cid, badwords)
                al.debug("spell check response: %s" % sresp, "code.spellcheck", dbo)
                return sresp
        except Exception,err:
            al.error("failed serving tinymce spellcheck request: %s" % str(err), "code.spellcheck", dbo, sys.exc_info())
            raise utils.ASMValidationError("failed parsing tinymce spellcheck request.")

class sql:
    def check_disabled(self, dbo, dumptype):
        if DUMP_OVERRIDES[dumptype] == "disabled":
            al.error("attempted %s and it is disabled" % dumptype, "code.sql", dbo)
            raise utils.ASMPermissionError("%s is disabled" % dumptype)

    def check_url(self, dbo, dumptype):
        url = DUMP_OVERRIDES[dumptype]
        if not url.startswith("http"): return
        url = url.replace("{alias}", dbo.alias).replace("{database}", dbo.database)
        url = url.replace("{username}", dbo.username).replace("{password}", dbo.password)
        url = url.replace("{md5pass}", users.hash_password(dbo.password))
        raise web.seeother(url)

    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.USE_SQL_INTERFACE)
        l = session.locale
        dbo = session.dbo
        data = web.input(mode="iface")
        mode = utils.df_ks(data, "mode")
        if mode == "iface":
            title = _("SQL Interface", l)
            al.debug("%s opened SQL interface" % str(session.user), "code.sql", dbo)
            s = html.header(title, session, "sql.js")
            c = html.controller_json("tables", dbupdate.TABLES + dbupdate.VIEWS)
            c += html.controller_json("dumpoverrides", DUMP_OVERRIDES)
            s += html.controller(c)
            s += html.footer()
            web.header("Content-Type", "text/html")
            return s
        elif mode == "dumpsql":
            self.check_disabled(dbo, "dumpsql")
            self.check_url(dbo, "dumpsql")
            al.info("%s executed SQL database dump" % str(session.user), "code.sql", dbo)
            web.header("Content-Type", "text/plain")
            web.header("Content-Disposition", "attachment; filename=\"dump.sql\"")
            return dbupdate.dump(dbo)
        elif mode == "dumpsqlnomedia":
            self.check_disabled(dbo, "dumpsqlnomedia")
            self.check_url(dbo, "dumpsqlnomedia")
            al.info("%s executed SQL database dump (without media)" % str(session.user), "code.sql", dbo)
            web.header("Content-Type", "text/plain")
            web.header("Content-Disposition", "attachment; filename=\"dump.sql\"")
            return dbupdate.dump(dbo, includeDBFS = False)
        elif mode == "dumpsqlasm2":
            self.check_disabled(dbo, "dumpsqlasm2")
            self.check_url(dbo, "dumpsqlasm2")
            # ASM2_COMPATIBILITY
            al.info("%s executed SQL database dump (ASM2 HSQLDB)" % str(session.user), "code.sql", dbo)
            web.header("Content-Type", "text/plain")
            web.header("Content-Disposition", "attachment; filename=\"asm2.sql\"")
            return dbupdate.dump_hsqldb(dbo)
        elif mode == "dumpsqlasm2nomedia":
            self.check_disabled(dbo, "dumpsqlasm2nomedia")
            self.check_url(dbo, "dumpsqlasm2nomedia")
            # ASM2_COMPATIBILITY
            al.info("%s executed SQL database dump (ASM2 HSQLDB, without media)" % str(session.user), "code.sql", dbo)
            web.header("Content-Type", "text/plain")
            web.header("Content-Disposition", "attachment; filename=\"asm2.sql\"")
            return dbupdate.dump_hsqldb(dbo, includeDBFS = False)
        elif mode == "animalcsv":
            al.debug("%s executed CSV animal dump" % str(session.user), "code.sql", dbo)
            web.header("Content-Type", "text/plain")
            web.header("Content-Disposition", "attachment; filename=\"animal.csv\"")
            return utils.csv(extanimal.get_animal_find_advanced(dbo, { "logicallocation" : "all", "includedeceased": "true", "includenonshelter": "true" }))
        elif mode == "personcsv":
            al.debug("%s executed CSV person dump" % str(session.user), "code.sql", dbo)
            web.header("Content-Type", "text/plain")
            web.header("Content-Disposition", "attachment; filename=\"person.csv\"")
            return utils.csv(extperson.get_person_find_simple(dbo, "", "all", True, 0))

    def POST(self):
        utils.check_loggedin(session, web)
        data = web.input(mode="exec", sql = "", sqlfile = "", table = "")
        mode = utils.df_ks(data, "mode")
        dbo = session.dbo
        if mode == "cols":
            try:
                if utils.df_ks(data, "table").strip() == "": return ""
                rows = db.query(dbo, "SELECT * FROM %s LIMIT 1" % utils.df_ks(data, "table"))
                if len(rows) == 0: return ""
                return "|".join(sorted(rows[0].iterkeys()))
            except Exception,err:
                al.error("%s" % str(err), "code.sql", dbo)
                utils.ASMValidationError(str(err))
        elif mode == "exec":
            users.check_permission(session, users.USE_SQL_INTERFACE)
            utils.check_locked_db(session)
            sql = utils.df_ks(data, "sql").strip()
            return self.exec_sql(dbo, sql)
        elif mode == "execfile":
            users.check_permission(session, users.USE_SQL_INTERFACE)
            utils.check_locked_db(session)
            sql = utils.df_ks(data, "sqlfile").strip()
            web.header("Content-Type", "text/plain")
            return self.exec_sql(dbo, sql)

    def exec_sql(self, dbo, sql):
        l = dbo.locale
        if sql.endswith(";"): sql = sql[0:len(sql)-1]
        # Use semi-colons (that aren't inside literals) as terminators
        # for multiple queries.
        queries = []
        inliteral = False
        lastchunk = 0
        for c in xrange(0, len(sql)):
            if sql[c:c+1] == "'": 
                inliteral = not inliteral
            if sql[c:c+1] == ";" and not inliteral:
                queries.append(sql[lastchunk:c])
                lastchunk = c
        queries.append(sql[lastchunk:len(sql)])
        rowsaffected = 0
        try:
            for q in queries:
                if q.strip() == "": continue
                al.info("%s query: %s" % (session.user, q), "code.sql", dbo)
                if q.lower().startswith("select") or q.lower().startswith("show"):
                    return html.table(db.query(dbo, q))
                else:
                    rowsaffected += db.execute(dbo, q)
            return _("{0} rows affected.", l).format(rowsaffected)
        except Exception,err:
            al.error("%s" % str(err), "code.sql", dbo)
            utils.ASMValidationError(str(err))

class systemusers:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.EDIT_USER)
        l = session.locale
        dbo = session.dbo
        title = _("Edit system users", l)
        user = users.get_users(dbo)
        roles = users.get_roles(dbo)
        al.debug("editing %d system users" % len(user), "code.systemusers", dbo)
        s = html.header(title, session, "users.js")
        c = html.controller_json("rows", user)
        c += html.controller_json("roles", roles)
        c += html.controller_json("internallocations", extlookups.get_internal_locations(dbo))
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        data = web.input(mode="create")
        mode = utils.df_ks(data, "mode")
        if mode == "create":
            users.check_permission(session, users.ADD_USER)
            return users.insert_user_from_form(session.dbo, session.user, data)
        elif mode == "update":
            users.check_permission(session, users.EDIT_USER)
            users.update_user_from_form(session.dbo, session.user, data)
        elif mode == "delete":
            users.check_permission(session, users.EDIT_USER)
            for uid in utils.df_kl(data, "ids"):
                users.delete_user(session.dbo, session.user, uid)
        elif mode == "reset":
            users.check_permission(session, users.EDIT_USER)
            for uid in utils.df_kl(data, "ids"):
                users.reset_password(session.dbo, uid)

class test:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_TEST)
        l = session.locale
        dbo = session.dbo
        data = web.input(newtest = "0", offset = "m31")
        test = extmedical.get_tests_outstanding(dbo, utils.df_ks(data, "offset"), session.locationfilter)
        al.debug("got %d tests" % len(test), "code.test", dbo)
        title = _("Test Book", l)
        s = html.header(title, session, "test.js")
        c = html.controller_str("name", "test")
        c += html.controller_bool("newtest", utils.df_ki(data, "newtest") == 1)
        c += html.controller_json("rows", test)
        c += html.controller_json("testtypes", extlookups.get_test_types(dbo))
        c += html.controller_json("testresults", extlookups.get_test_results(dbo))
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        data = web.input(mode = "create", ids = "")
        mode = utils.df_ks(data, "mode")
        if mode == "create":
            users.check_permission(session, users.ADD_TEST)
            return extmedical.insert_test_from_form(session.dbo, session.user, data)
        elif mode == "update":
            users.check_permission(session, users.CHANGE_TEST)
            extmedical.update_test_from_form(session.dbo, session.user, data)
        elif mode == "delete":
            users.check_permission(session, users.DELETE_TEST)
            for vid in utils.df_kl(data, "ids"):
                extmedical.delete_test(session.dbo, session.user, vid)

class vaccination:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_VACCINATION)
        l = session.locale
        dbo = session.dbo
        data = web.input(newvacc = "0", offset = "m31")
        vacc = extmedical.get_vaccinations_outstanding(dbo, utils.df_ks(data, "offset"), session.locationfilter)
        schedules = [ 
            "7|%s" % ntranslate(1, [ _("{plural0} week", l), _("{plural1} weeks", l), _("{plural2} weeks", l), _("{plural3} weeks", l) ], l),
            "14|%s" % ntranslate(2, [ _("{plural0} week", l), _("{plural1} weeks", l), _("{plural2} weeks", l), _("{plural3} weeks", l) ], l),
            "21|%s" % ntranslate(3, [ _("{plural0} week", l), _("{plural1} weeks", l), _("{plural2} weeks", l), _("{plural3} weeks", l) ], l),
            "28|%s" % ntranslate(4, [ _("{plural0} week", l), _("{plural1} weeks", l), _("{plural2} weeks", l), _("{plural3} weeks", l) ], l),
            "182|%s" % ntranslate(6, [ _("{plural0} month", l), _("{plural1} months", l), _("{plural2} months", l), _("{plural3} months", l) ], l),
            "365|%s" % ntranslate(1, [ _("{plural0} year", l), _("{plural1} year", l), _("{plural2} year", l), _("{plural3} year", l) ], l),
            "730|%s" % ntranslate(2, [ _("{plural0} year", l), _("{plural1} year", l), _("{plural2} year", l), _("{plural3} year", l) ], l),
            "1095|%s" % ntranslate(3, [ _("{plural0} year", l), _("{plural1} year", l), _("{plural2} year", l), _("{plural3} year", l) ], l)
        ]
        al.debug("got %d vaccinations" % len(vacc), "code.vaccination", dbo)
        title = _("Vaccination Book", l)
        s = html.header(title, session, "vaccination.js")
        c = html.controller_str("name", "vaccination")
        c += html.controller_json("schedules", schedules)
        c += html.controller_bool("newvacc", utils.df_ki(data, "newvacc") == 1)
        c += html.controller_json("rows", vacc)
        c += html.controller_json("vaccinationtypes", extlookups.get_vaccination_types(dbo))
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        data = web.input(mode = "create", ids = "", duration = 0)
        mode = utils.df_ks(data, "mode")
        if mode == "create":
            users.check_permission(session, users.ADD_VACCINATION)
            return extmedical.insert_vaccination_from_form(session.dbo, session.user, data)
        elif mode == "update":
            users.check_permission(session, users.CHANGE_VACCINATION)
            extmedical.update_vaccination_from_form(session.dbo, session.user, data)
        elif mode == "delete":
            users.check_permission(session, users.DELETE_VACCINATION)
            for vid in utils.df_kl(data, "ids"):
                extmedical.delete_vaccination(session.dbo, session.user, vid)
        elif mode == "complete":
            users.check_permission(session, users.BULK_COMPLETE_VACCINATION)
            for vid in utils.df_kl(data, "ids"):
                extmedical.complete_vaccination(session.dbo, session.user, vid)
        elif mode == "reschedule":
            users.check_permission(session, users.BULK_COMPLETE_VACCINATION)
            for vid in utils.df_kl(data, "ids"):
                extmedical.reschedule_vaccination(session.dbo, session.user, vid, utils.df_ki(data, "duration"))
        elif mode == "required":
            users.check_permission(session, users.BULK_COMPLETE_VACCINATION)
            newdate = utils.df_kd(data, "newdate", session.dbo.locale)
            for vid in utils.df_kl(data, "ids"):
                extmedical.update_vaccination_required(session.dbo, session.user, vid, newdate)

class waitinglist:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_WAITING_LIST)
        l = session.locale
        dbo = session.dbo
        data = web.input(id = 0)
        a = extwaitinglist.get_waitinglist_by_id(dbo, utils.df_ki(data, "id"))
        if a is None: raise web.notfound()
        title = _("Waiting list entry for {0} ({1})", l).format(a["OWNERNAME"], a["SPECIESNAME"])
        al.debug("opened waiting list %s %s" % (a["OWNERNAME"], a["SPECIESNAME"]), "code.waitinglist", dbo)
        s = html.header(title, session, "waitinglist.js")
        c = html.controller_json("animal", a)
        c += html.controller_json("additional", extadditional.get_additional_fields(dbo, a["ID"], "waitinglist"))
        c += html.controller_json("species", extlookups.get_species(dbo))
        c += html.controller_json("urgencies", extlookups.get_urgencies(dbo))
        c += html.controller_json("tabcounts", extwaitinglist.get_satellite_counts(dbo, a["ID"])[0])
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        dbo = session.dbo
        data = web.input(mode="save")
        mode = utils.df_ks(data, "mode")
        if mode == "save":
            users.check_permission(session, users.CHANGE_WAITING_LIST)
            extwaitinglist.update_waitinglist_from_form(dbo, data, session.user)
        elif mode == "delete":
            users.check_permission(session, users.DELETE_WAITING_LIST)
            extwaitinglist.delete_waitinglist(dbo, session.user, utils.df_ki(data, "id"))
        elif mode == "toanimal":
            users.check_permission(session, users.ADD_ANIMAL)
            return str(extwaitinglist.create_animal(dbo, session.user, utils.df_ki(data, "id")))

class waitinglist_diary:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_DIARY)
        l = session.locale
        dbo = session.dbo
        data = web.input(id = 0)
        a = extwaitinglist.get_waitinglist_by_id(dbo, utils.df_ki(data, "id"))
        if a is None: raise web.notfound()
        title = _("Waiting list entry for {0} ({1})", l).format(a["OWNERNAME"], a["SPECIESNAME"])
        diaries = extdiary.get_diaries(dbo, extdiary.WAITINGLIST, utils.df_ki(data, "id"))
        al.debug("got %d diaries" % len(diaries), "code.waitinglist_diary", dbo)
        s = html.header(title, session, "diary.js")
        c = html.controller_json("rows", diaries)
        c += html.controller_json("animal", a)
        c += html.controller_json("tabcounts", extwaitinglist.get_satellite_counts(dbo, a["WLID"])[0])
        c += html.controller_str("name", "waitinglist_diary")
        c += html.controller_int("linkid", a["WLID"])
        c += html.controller_json("forlist", users.get_users_and_roles(dbo))
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        data = web.input(mode="create")
        mode = utils.df_ks(data, "mode")
        if mode == "create":
            users.check_permission(session, users.ADD_DIARY)
            return extdiary.insert_diary_from_form(session.dbo, session.user, extdiary.WAITINGLIST, utils.df_ki(data, "linkid"), data)
        elif mode == "update":
            users.check_permission(session, users.EDIT_ALL_DIARY_NOTES)
            extdiary.update_diary_from_form(session.dbo, session.user, data)
        elif mode == "delete":
            users.check_permission(session, users.DELETE_DIARY)
            for did in utils.df_kl(data, "ids"):
                extdiary.delete_diary(session.dbo, session.user, did)
        elif mode == "complete":
            users.check_permission(session, users.BULK_COMPLETE_NOTES)
            for did in utils.df_kl(data, "ids"):
                extdiary.complete_diary_note(session.dbo, session.user, did)

class waitinglist_log:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_LOG)
        l = session.locale
        dbo = session.dbo
        data = web.input(id = 0, filter = -2)
        logfilter = utils.df_ki(data, "filter")
        if logfilter == -2: logfilter = configuration.default_log_filter(dbo)
        a = extwaitinglist.get_waitinglist_by_id(dbo, utils.df_ki(data, "id"))
        if a is None: raise web.notfound()
        title = _("Waiting list entry for {0} ({1})", l).format(a["OWNERNAME"], a["SPECIESNAME"])
        logs = extlog.get_logs(dbo, extlog.WAITINGLIST, utils.df_ki(data, "id"), logfilter)
        al.debug("got %d logs" % len(logs), "code.waitinglist_diary", dbo)
        s = html.header(title, session, "log.js")
        c = html.controller_str("name", "waitinglist_log")
        c += html.controller_int("linkid", utils.df_ki(data, "id"))
        c += html.controller_int("filter", logfilter)
        c += html.controller_json("rows", logs)
        c += html.controller_json("animal", a)
        c += html.controller_json("tabcounts", extwaitinglist.get_satellite_counts(dbo, a["WLID"])[0])
        c += html.controller_json("logtypes", extlookups.get_log_types(dbo))
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        data = web.input(mode="create")
        mode = utils.df_ks(data, "mode")
        if mode == "create":
            users.check_permission(session, users.ADD_LOG)
            return extlog.insert_log_from_form(session.dbo, session.user, extlog.WAITINGLIST, utils.df_ki(data, "linkid"), data)
        elif mode == "update":
            users.check_permission(session, users.CHANGE_LOG)
            extlog.update_log_from_form(session.dbo, session.user, data)
        elif mode == "delete":
            users.check_permission(session, users.DELETE_LOG)
            for lid in utils.df_kl(data, "ids"):
                extlog.delete_log(session.dbo, session.user, lid)

class waitinglist_media:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_MEDIA)
        l = session.locale
        dbo = session.dbo
        data = web.input(id = 0)
        a = extwaitinglist.get_waitinglist_by_id(dbo, utils.df_ki(data, "id"))
        if a is None: raise web.notfound()
        title = _("Waiting list entry for {0} ({1})", l).format(a["OWNERNAME"], a["SPECIESNAME"])
        m = extmedia.get_media(dbo, extmedia.WAITINGLIST, utils.df_ki(data, "id"))
        al.debug("got %d media" % len(m), "code.waitinglist_media", dbo)
        s = html.header(title, session, "media.js")
        c = html.controller_json("media", m)
        c += html.controller_json("animal", a)
        c += html.controller_json("tabcounts", extwaitinglist.get_satellite_counts(dbo, a["WLID"])[0])
        c += html.controller_bool("showPreferred", False)
        c += html.controller_int("linkid", utils.df_ki(data, "id"))
        c += html.controller_int("linktypeid", extmedia.WAITINGLIST)
        c += html.controller_str("name", self.__class__.__name__)
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        data = web.input(mode="create", filechooser={}, linkid="0", base64image = "", _unicode=False)
        mode = utils.df_ks(data, "mode")
        dbo = session.dbo
        l = session.locale
        linkid = utils.df_ki(data, "linkid")
        if mode == "create":
            users.check_permission(session, users.ADD_MEDIA)
            extmedia.attach_file_from_form(session.dbo, session.user, extmedia.WAITINGLIST, linkid, data)
            raise web.seeother("waitinglist_media?id=%d" % utils.df_ki(data, "linkid"))
        elif mode == "createdoc":
            users.check_permission(session, users.ADD_MEDIA)
            mediaid = extmedia.create_blank_document_media(session.dbo, session.user, extmedia.WAITINGLIST, linkid)
            raise web.seeother("document_media_edit?id=%d&redirecturl=waitinglist_media?id=%d" % (mediaid, linkid))
        elif mode == "createlink":
            users.check_permission(session, users.ADD_MEDIA)
            mediaid = extmedia.attach_link_from_form(session.dbo, session.user, extmedia.WAITINGLIST, linkid, data)
            raise web.seeother("waitinglist_media?id=%d" % linkid)
        elif mode == "update":
            users.check_permission(session, users.CHANGE_MEDIA)
            extmedia.update_media_notes(session.dbo, session.user, utils.df_ki(data, "mediaid"), utils.df_ks(data, "comments"))
        elif mode == "delete":
            users.check_permission(session, users.DELETE_MEDIA)
            for mid in utils.df_kl(data, "ids"):
                extmedia.delete_media(session.dbo, session.user, mid)
        elif mode == "email":
            users.check_permission(session, users.MAIL_MERGE)
            emailadd = utils.df_ks(data, "email")
            if emailadd == "" or emailadd.find("@") == -1:
                raise utils.ASMValidationError(_("Invalid email address", l))
            for mid in utils.df_kl(data, "ids"):
                m = extmedia.get_media_by_id(dbo, mid)
                if len(m) == 0: raise web.notfound()
                m = m[0]
                content = dbfs.get_string(dbo, m["MEDIANAME"])
                content = utils.fix_relative_document_uris(content, BASE_URL, MULTIPLE_DATABASES and dbo.database or "")
                utils.send_email(dbo, configuration.email(dbo), emailadd, "", m["MEDIANOTES"], content, "html")
                return emailadd
        elif mode == "rotateclock":
            users.check_permission(session, users.CHANGE_MEDIA)
            for mid in utils.df_kl(data, "ids"):
                extmedia.rotate_media(session.dbo, session.user, mid, True)
        elif mode == "rotateanti":
            users.check_permission(session, users.CHANGE_MEDIA)
            for mid in utils.df_kl(data, "ids"):
                extmedia.rotate_media(session.dbo, session.user, mid, False)
        elif mode == "web":
            users.check_permission(session, users.CHANGE_MEDIA)
            mid = utils.df_kl(data, "ids")[0]
            extmedia.set_web_preferred(session.dbo, session.user, mid)
        elif mode == "video":
            users.check_permission(session, users.CHANGE_MEDIA)
            mid = utils.df_kl(data, "ids")[0]
            extmedia.set_video_preferred(session.dbo, session.user, mid)
        elif mode == "doc":
            users.check_permission(session, users.CHANGE_MEDIA)
            mid = utils.df_kl(data, "ids")[0]
            extmedia.set_doc_preferred(session.dbo, session.user, mid)

class waitinglist_new:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.ADD_WAITING_LIST)
        l = session.locale
        dbo = session.dbo
        title = _("Add waiting list", l)
        s = html.header(title, session, "waitinglist_new.js")
        c = html.controller_json("species", extlookups.get_species(dbo))
        c += html.controller_json("urgencies", extlookups.get_urgencies(dbo))
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.ADD_WAITING_LIST)
        dbo = session.dbo
        data = web.input()
        return str(extwaitinglist.insert_waitinglist_from_form(dbo, data, session.user))

class waitinglist_results:
    def GET(self):
        utils.check_loggedin(session, web)
        users.check_permission(session, users.VIEW_WAITING_LIST)
        l = session.locale
        dbo = session.dbo
        urgencies = extlookups.get_urgencies(dbo)
        lowest_priority = len(urgencies)
        data = web.input(priorityfloor = lowest_priority, includeremoved = 0, species = -1, namecontains = "", 
            addresscontains = "", descriptioncontains = "")
        rows = extwaitinglist.get_waitinglist(dbo, utils.df_ki(data, "priorityfloor"), utils.df_ki(data, "species"), utils.df_ks(data, "addresscontains"),
            utils.df_ki(data, "includeremoved"), utils.df_ks(data, "namecontains"), utils.df_ks(data, "descriptioncontains"))
        title = _("Waiting List", l)
        al.debug("found %d results" % (len(rows)), "code.waitinglist_results", dbo)
        s = html.header(title, session, "waitinglist_results.js")
        c = html.controller_json("rows", rows)
        c += html.controller_str("seladdresscontains", utils.df_ks(data, "addresscontains"))
        c += html.controller_str("seldescriptioncontains", utils.df_ks(data, "descriptioncontains"))
        c += html.controller_int("selincluderemoved", utils.df_ki(data, "includeremoved"))
        c += html.controller_str("selnamecontains", utils.df_ks(data, "namecontains"))
        c += html.controller_int("selpriorityfloor", utils.df_ki(data, "priorityfloor"))
        c += html.controller_int("selspecies", utils.df_ki(data, "species"))
        c += html.controller_json("species", extlookups.get_species(dbo))
        c += html.controller_json("urgencies", urgencies)
        c += html.controller_json("yesno", extlookups.get_yesno(dbo))
        s += html.controller(c)
        s += html.footer()
        web.header("Content-Type", "text/html")
        web.header("Cache-Control", "no-cache")
        return s

    def POST(self):
        utils.check_loggedin(session, web)
        data = web.input(mode="create")
        mode = utils.df_ks(data, "mode")
        if mode == "delete":
            users.check_permission(session, users.DELETE_WAITING_LIST)
            for wid in utils.df_kl(data, "ids"):
                extwaitinglist.delete_waitinglist(session.dbo, session.user, wid)
        elif mode == "complete":
            users.check_permission(session, users.CHANGE_WAITING_LIST)
            for wid in utils.df_kl(data, "ids"):
                extwaitinglist.update_waitinglist_remove(session.dbo, session.user, wid)
        elif mode == "highlight":
            users.check_permission(session, users.CHANGE_WAITING_LIST)
            for wid in utils.df_kl(data, "ids"):
                extwaitinglist.update_waitinglist_highlight(session.dbo, wid, utils.df_ks(data, "himode"))


if __name__ == "__main__":
    app.run()

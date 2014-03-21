#!/usr/bin/python

import al
import audit
import configuration
import datetime, time
import db
import dbupdate
import hashlib
import i18n
import smcom
import sys
import utils
from sitedefs import MULTIPLE_DATABASES, MULTIPLE_DATABASES_TYPE

# Security flags
ADD_ANIMAL                      = "aa"
CHANGE_ANIMAL                   = "ca"
VIEW_ANIMAL                     = "va"
VIEW_ANIMAL_VET                 = "vavet"
DELETE_ANIMAL                   = "da"
CLONE_ANIMAL                    = "cloa"

GENERATE_DOCUMENTS              = "gaf"
MODIFY_NAME_DATABASE            = "mand"
MAIL_MERGE                      = "mmeo"

ADD_REPO_DOCUMENT               = "ard"
DELETE_REPO_DOCUMENT            = "drd"
VIEW_REPO_DOCUMENT              = "vrd"

ADD_VACCINATION                 = "aav"
VIEW_VACCINATION                = "vav"
CHANGE_VACCINATION              = "cav"
DELETE_VACCINATION              = "dav"
BULK_COMPLETE_VACCINATION       = "bcav"

ADD_TEST                        = "aat"
VIEW_TEST                       = "vat"
CHANGE_TEST                     = "cat"
DELETE_TEST                     = "dat"

ADD_MEDICAL                     = "maam"
CHANGE_MEDICAL                  = "mcam"
VIEW_MEDICAL                    = "mvam"
DELETE_MEDICAL                  = "mdam"
BULK_COMPLETE_MEDICAL           = "bcam"

ADD_MEDIA                       = "aam"
CHANGE_MEDIA                    = "cam"
VIEW_MEDIA                      = "vam"
DELETE_MEDIA                    = "dam"

ADD_DIET                        = "daad"
CHANGE_DIET                     = "dcad"
DELETE_DIET                     = "ddad"
VIEW_DIET                       = "dvad"

ADD_COST                        = "caad"
CHANGE_COST                     = "ccad"
DELETE_COST                     = "cdad"
VIEW_COST                       = "cvad"

ADD_MOVEMENT                    = "aamv"
CHANGE_MOVEMENT                 = "camv"
VIEW_MOVEMENT                   = "vamv"
DELETE_MOVEMENT                 = "damv"

ADD_ACCOUNT                     = "aac"
VIEW_ACCOUNT                    = "vac"
CHANGE_ACCOUNT                  = "cac"
CHANGE_TRANSACTIONS             = "ctrx"
DELETE_ACCOUNT                  = "dac"

ADD_PERSON                      = "ao"
CHANGE_PERSON                   = "co"
VIEW_PERSON                     = "vo"
VIEW_STAFF                      = "vso"
DELETE_PERSON                   = "do"
MERGE_PERSON                    = "mo"
VIEW_PERSON_LINKS               = "volk"

ADD_INVESTIGATION               = "aoi"
CHANGE_INVESTIGATION            = "coi"
DELETE_INVESTIGATION            = "doi"
VIEW_INVESTIGATION              = "voi"

ADD_VOUCHER                     = "vaov"
CHANGE_VOUCHER                  = "vcov"
DELETE_VOUCHER                  = "vdov"
VIEW_VOUCHER                    = "vvov"

ADD_DONATION                    = "oaod"
CHANGE_DONATION                 = "ocod"
DELETE_DONATION                 = "odod"
VIEW_DONATION                   = "ovod"

ADD_LOG                         = "ale"
CHANGE_LOG                      = "cle"
DELETE_LOG                      = "dle"
VIEW_LOG                        = "vle"

EDIT_ONLINE_FORMS               = "eof"
VIEW_INCOMING_FORMS             = "vif"
DELETE_INCOMING_FORMS           = "dif"

SYSTEM_MENU                     = "asm"
SYSTEM_OPTIONS                  = "cso"
MODIFY_LOOKUPS                  = "ml"
ADD_USER                        = "asu"
EDIT_USER                       = "esu"
EDIT_DIARY_TASKS                = "edt"
RUN_DB_UPDATE                   = "rdbu"
RUN_DB_DIAGNOSTIC               = "rdbd"
USE_SQL_INTERFACE               = "usi"
USE_INTERNET_PUBLISHER          = "uipb"

ADD_REPORT                      = "ccr"
VIEW_REPORT                     = "vcr"
CHANGE_REPORT                   = "hcr"
DELETE_REPORT                   = "dcr"

ADD_DIARY                       = "adn"
VIEW_DIARY                      = "vdn"
EDIT_ALL_DIARY_NOTES            = "eadn"
EDIT_MY_DIARY_NOTES             = "emdn"
EDIT_COMPLETED_NOTES            = "ecdn"
BULK_COMPLETE_NOTES             = "bcn"
DELETE_DIARY                    = "ddn"
PRINT_DIARY                     = "pdn"
PRINT_VACCINATION_DIARY         = "pvd"

ADD_LOST_ANIMAL                 = "ala"
ADD_FOUND_ANIMAL                = "afa"
CHANGE_LOST_ANIMAL              = "cla"
CHANGE_FOUND_ANIMAL             = "cfa"
DELETE_LOST_ANIMAL              = "dla"
DELETE_FOUND_ANIMAL             = "dfa"
VIEW_LOST_ANIMAL                = "vla"
VIEW_FOUND_ANIMAL               = "vfa"
MATCH_LOST_FOUND                = "mlaf"

VIEW_WAITING_LIST               = "vwl"
ADD_WAITING_LIST                = "awl"
DELETE_WAITING_LIST             = "dwl"
CHANGE_WAITING_LIST             = "cwl"
BULK_COMPLETE_WAITING_LIST      = "bcwl"

ADD_LITTER                      = "all"
VIEW_LITTER                     = "vll"
DELETE_LITTER                   = "dll"
CHANGE_LITTER                   = "cll"

def check_permission(session, flag, message = ""):
    """
    Throws an ASMPermissionError if the flag is not in the map
    """
    l = session.locale
    if session.superuser == 1: return
    if not has_security_flag(session.securitymap, flag):
        if message == "":
            message = i18n._("Forbidden", l)
        raise utils.ASMPermissionError(message)

def check_permission_bool(session, flag):
    """
    Returns True if a user has permission to do something
    """
    if session.superuser == 1: return True
    if has_security_flag(session.securitymap, flag): return True
    return False

def has_security_flag(securitymap, flag):
    """
    Returns true if the given flag is in the given map
    """
    return securitymap.find(flag + " ") != -1

def add_security_flag(securitymap, flag):
    """
    Adds a security flag to a map and returns the new map
    """
    if not has_security_flag(securitymap, flag):
        securitymap += flag + " *"
    return securitymap

def login(dbo, username):
    """
    Marks the given user as logged in
    """
    logout(dbo, username)
    db.execute(dbo, "DELETE FROM activeuser WHERE UPPER(UserName) LIKE '%s'" % str(username.upper()))
    db.execute(dbo, db.make_insert_sql("activeuser", (
        ( "UserName", db.ds(username)),
        ( "Since", db.ddt(i18n.now())),
        ( "Messages", db.ds("asm3"))
        )))
    al.info("%s logged in" % username, "users.login", dbo)

def logout(dbo, username):
    """
    Marks the given user as logged out
    """
    if dbo is None: return
    db.execute(dbo, "DELETE FROM activeuser WHERE username LIKE '%s'" % username)
    al.info("%s logged out" % username, "users.logout", dbo)

def auto_logout(dbo):
    """
    Marks all users logged out who have been logged in for longer than 
    8 hours to account for people not logging out manually.
    """
    cutoff = i18n.now() - datetime.timedelta(hours = -8)
    db.execute(dbo, "DELETE FROM activeuser WHERE Since <= %s" % db.dd(cutoff))

def authenticate(dbo, username, password):
    """
    Authenticates whether a username and password are valid.
    Returns None if authentication failed, or a user row
    """
    username = db.escape(username).replace("\\", "")
    pypassword = hash_password(password)
    javapassword = hash_password(password, True)

    users = db.query(dbo, "SELECT * FROM users WHERE UPPER(UserName) LIKE UPPER(" + db.ds(username) + ")")
    for u in users:
        dbpass = u["PASSWORD"].strip()
        if dbpass == pypassword or dbpass == javapassword:
            return u
    return None

def authenticate_ip(user, remoteip):
    """
    Tests whether the user's remoteip fits into any IP restriction
    set on the user object.
    If IP restriction is not present or blank, we let them through.
    Returns true for successful authentication.
    user: A row from the user table
    remoteip: The user's remote ip address
    """
    if not user.has_key("IPRESTRICTION"):
        return True
    if user["IPRESTRICTION"] is None or user["IPRESTRICTION"] == "":
        return True
    # Restriction is a space separated list of addresses in CIDR
    # notation.
    restrictions = user["IPRESTRICTION"].split(" ")
    for r in restrictions:
        # We have to have a slash for CIDR notation
        if r.count("/") != 1:
            continue
        address, size = r.split("/")
        # We should have 4 numbers for the dotted quads
        if address.count(".") != 3:
            continue
        q1, q2, q3, q4 = address.split(".")
        # Depending on the size selected, we check a smaller or
        # larger chunk of the remote ip for a match.
        if size == "32" and remoteip == address:
            return True
        if size == "24" and remoteip.startswith("%s.%s.%s." % (q1, q2, q3)):
            return True
        if size == "16" and remoteip.startswith("%s.%s." % (q1, q2)):
            return True
        if size == "8" and remoteip.startswith("%s." % q1):
            return True
    return False

def hash_password(password, javaCompatible = False):
    """
    Returns an md5 hash of a password string
    javaCompatible: Return an MD5 hash compatible with Java MD5
    """
    m = hashlib.md5()
    m.update(password)
    s = m.hexdigest()
    if javaCompatible and s.startswith("0"): s = s[1:]
    return s

def change_password(dbo, username, oldpassword, newpassword):
    """
    Changes the password for a user
    """
    l = dbo.locale
    if None == authenticate(dbo, username, oldpassword):
        raise utils.ASMValidationError(i18n._("Password is incorrect.", l))
    db.execute(dbo, "UPDATE users SET Password = '%s' WHERE UserName Like '%s'" % (hash_password(newpassword, True), username))

def get_locale_override(dbo, username):
    """
    Returns a user's locale override, or empty string if it doesn't have one
    """
    try:
        return db.query_string(dbo, "SELECT LocaleOverride FROM users WHERE UserName Like '%s'" % username)
    except:
        return ""

def get_theme_override(dbo, username):
    """
    Returns a user's theme override, or empty string if it doesn't have one
    """
    try:
        return db.query_string(dbo, "SELECT ThemeOverride FROM users WHERE UserName Like '%s'" % username)
    except:
        return ""

def get_real_name(dbo, username):
    """
    Returns a user's real name
    """
    return db.query_string(dbo, "SELECT RealName FROM users WHERE UserName Like '%s'" % username)

def get_roles(dbo):
    """
    Returns a list of all system roles
    """
    return db.query(dbo, "SELECT * FROM role ORDER BY Rolename")

def get_roles_for_user(dbo, user):
    """
    Returns a list of roles a user is in
    """
    rows = db.query(dbo, "SELECT r.Rolename FROM role r " \
        "INNER JOIN userrole ur ON ur.RoleID = r.ID " \
        "INNER JOIN users u ON u.ID = ur.UserID " \
        "WHERE u.UserName Like '%s' " \
        "ORDER BY r.Rolename" % user)
    roles = []
    for r in rows:
        roles.append(r["ROLENAME"])
    return roles

def get_security_map(dbo, username):
    """
    Returns the security map for a user, which is an aggregate of all
    the roles they have.
    """
    rv = ""
    maps = db.query(dbo, "SELECT role.SecurityMap FROM role " \
        "INNER JOIN userrole ON role.ID = userrole.RoleID " \
        "INNER JOIN users ON users.ID = userrole.UserID " \
        "WHERE users.UserName Like '%s'" % username)
    for m in maps:
        rv += str(m["SECURITYMAP"])
    return rv

def get_users_and_roles(dbo):
    """
    Returns a single list of all users and roles together,
    with one column - USERNAME
    """
    return db.query(dbo, "SELECT UserName FROM users " \
        "UNION SELECT Rolename AS UserName FROM role ORDER BY UserName")

def get_users(dbo, user='%'):
    """
    Returns a list of all (or selected) system users with a pipe
    separated list of their roles
    """
    users = db.query(dbo, "SELECT * FROM users WHERE UserName Like '%s' ORDER BY UserName" % user)
    roles = db.query(dbo, "SELECT ur.*, r.RoleName FROM userrole ur INNER JOIN role r ON ur.RoleID = r.ID")
    for u in users:
        roleids = []
        rolenames = []
        for r in roles:
            if r["USERID"] == u["ID"]:
                roleids.append(str(r["ROLEID"]))
                rolenames.append(str(r["ROLENAME"]))
        u["ROLEIDS"] = "|".join(roleids)
        u["ROLES"] = "|".join(rolenames)
    return users

def get_activeusers(dbo):
    """
    Returns a list of active users on the system
    USERNAME, SINCE, MESSAGES
    """
    return db.query(dbo, "SELECT * FROM activeuser")

def get_personid(dbo, user):
    """
    Returns the personid for a user or 0 if it doesn't have one
    """
    return db.query_int(dbo, "SELECT OwnerID FROM users WHERE UserName Like '%s'" % user)

def get_location_filter(dbo, user):
    """
    Returns the location filter (comma separated list of IDs) 
    for a user, or "" if it doesn't have one.
    """
    return db.query_string(dbo, "SELECT LocationFilter FROM users WHERE UserName LIKE '%s'" % user)

def insert_user_from_form(dbo, username, data):
    """
    Creates a user record from posted form data. Uses
    the roles key (which should be a comma separated list of
    role ids) to create userrole records.
    """
    nuserid = db.get_id(dbo, "users")
    sql = db.make_insert_sql("users", ( 
        ( "ID", db.di(nuserid)),
        ( "UserName", utils.df_t(data, "username")),
        ( "RealName", utils.df_t(data, "realname")),
        ( "EmailAddress", utils.df_t(data, "email")),
        ( "Password", db.ds(hash_password(utils.df_ks(data, "password"), True))),
        ( "SuperUser", utils.df_s(data, "superuser")),
        ( "RecordVersion", db.di(0)),
        ( "SecurityMap", db.ds("dummy")),
        ( "OwnerID", utils.df_s(data, "person")),
        ( "LocationFilter", utils.df_t(data, "locationfilter")),
        ( "IPRestriction", utils.df_t(data, "iprestriction"))
        ))
    db.execute(dbo, sql)
    audit.create(dbo, username, "users", str(nuserid))
    roles = utils.df_ks(data, "roles").strip()
    if roles != "":
        for rid in roles.split(","):
            if rid.strip() != "":
                db.execute(dbo, "INSERT INTO userrole VALUES (%d, %d)" % (nuserid, int(rid)))
    return nuserid

def update_user_settings(dbo, username, email = "", realname = "", locale = "", theme = ""):
    userid = db.query_int(dbo, "SELECT ID FROM users WHERE Username = '%s'" % username)
    sql = db.make_update_sql("users", "ID=%d" % userid, (
        ( "RealName", db.ds(realname) ),
        ( "EmailAddress", db.ds(email) ),
        ( "ThemeOverride", db.ds(theme) ),
        ( "LocaleOverride", db.ds(locale) )
    ))
    preaudit = db.query(dbo, "SELECT * FROM users WHERE ID = %d" % int(userid))[0]
    db.execute(dbo, sql)
    postaudit = db.query(dbo, "SELECT * FROM users WHERE ID = %d" % int(userid))[0]
    audit.edit(dbo, username, "users", audit.map_diff(preaudit, postaudit, [ "USERNAME", ]))

def update_user_from_form(dbo, username, data):
    """
    Updates a user record from posted form data
    Uses the roles key (which should be a comma separated list of
    role ids) to create userrole records.
    """
    userid = utils.df_ki(data, "userid")
    sql = db.make_update_sql("users", "ID=%d" % userid, ( 
        ( "RealName", utils.df_t(data, "realname")),
        ( "EmailAddress", utils.df_t(data, "email")),
        ( "SuperUser", utils.df_s(data, "superuser")),
        ( "OwnerID", utils.df_s(data, "person")),
        ( "LocationFilter", utils.df_t(data, "locationfilter")),
        ( "IPRestriction", utils.df_t(data, "iprestriction"))
        ))
    preaudit = db.query(dbo, "SELECT * FROM users WHERE ID = %d" % userid)
    db.execute(dbo, sql)
    postaudit = db.query(dbo, "SELECT * FROM users WHERE ID = %d" % userid)
    audit.edit(dbo, username, "users", audit.map_diff(preaudit, postaudit, [ "USERNAME", ]))
    db.execute(dbo, "DELETE FROM userrole WHERE UserID = %d" % userid)
    if utils.df_ki(data, "issuperuser") == 0:
        roles = utils.df_ks(data, "roles").strip()
        if roles != "":
            for rid in roles.split(","):
                if rid.strip() != "":
                    db.execute(dbo, "INSERT INTO userrole VALUES (%d, %d)" % (userid, int(rid)))

def delete_user(dbo, username, uid):
    """
    Deletes the selected user
    """
    audit.delete(dbo, username, "users", str(db.query(dbo, "SELECT * FROM users WHERE ID=%d" % int(uid))))
    db.execute(dbo, "DELETE FROM users WHERE ID = %d" % int(uid))
    db.execute(dbo, "DELETE FROM userrole WHERE UserID = %d" % int(uid))

def insert_role_from_form(dbo, username, data):
    """
    Creates a role record from posted form data. 
    """
    nroleid = db.get_id(dbo, "role")
    sql = db.make_insert_sql("role", ( 
        ( "ID", db.di(nroleid)),
        ( "Rolename", utils.df_t(data, "rolename")),
        ( "SecurityMap", utils.df_t(data, "securitymap"))
        ))
    db.execute(dbo, sql)
    audit.create(dbo, username, "role", str(nroleid))

def update_role_from_form(dbo, username, data):
    """
    Updates a role record from posted form data
    """
    roleid = utils.df_ki(data, "roleid")
    sql = db.make_update_sql("role", "ID=%d" % roleid, ( 
        ( "Rolename", utils.df_t(data, "rolename")),
        ( "SecurityMap", utils.df_t(data, "securitymap"))
        ))
    preaudit = db.query(dbo, "SELECT * FROM role WHERE ID = %d" % roleid)
    db.execute(dbo, sql)
    postaudit = db.query(dbo, "SELECT * FROM role WHERE ID = %d" % roleid)
    audit.edit(dbo, username, "role", audit.map_diff(preaudit, postaudit, [ "ROLENAME", ]))

def delete_role(dbo, username, rid):
    """
    Deletes the selected role. If it's in use, throws an ASMValidationError
    """
    l = dbo.locale
    if db.query_int(dbo, "SELECT COUNT(*) FROM userrole WHERE RoleID = %d" % int(rid)) > 0:
        raise utils.ASMValidationError(i18n._("Role is in use and cannot be deleted.", l))
    audit.delete(dbo, username, "role", str(db.query(dbo, "SELECT * FROM role WHERE ID=%d" % int(rid))))
    db.execute(dbo, "DELETE FROM accountsrole WHERE RoleID = %d" % int(rid))
    db.execute(dbo, "DELETE FROM customreportrole WHERE RoleID = %d" % int(rid))
    db.execute(dbo, "DELETE FROM role WHERE ID = %d" % int(rid))

def reset_password(dbo, userid):
    """
    Resets the password for the given user to "password"
    """
    db.execute(dbo, "UPDATE users SET Password = '%s' WHERE ID = %d" % ( hash_password("password", True), int(userid)))

def update_session(session):
    """
    Updates and reloads stored session data
    """
    dbo = session.dbo
    locale = configuration.locale(dbo)
    theme = configuration.system_theme(dbo)
    loverride = get_locale_override(dbo, session.user)
    if loverride != "": 
        al.debug("user %s has locale override of %s set, switching." % (session.user, loverride), "users.update_session", dbo)
        locale = loverride
    toverride = get_theme_override(dbo, session.user)
    if toverride != "":
        al.debug("user %s has theme override of %s set, switching." % (session.user, toverride), "users.update_session", dbo)
        theme = toverride
    dbo.locale = locale
    dbo.is_large_db = db.query_int(dbo, "SELECT COUNT(*) FROM animal") > 10000
    session.locale = locale
    session.theme = theme
    session.config_ts = time.strftime("%Y%m%d%H%M%S", datetime.datetime.today().timetuple())

def web_login(post, session, remoteip, path):
    """
    Performs a login and sets up the user's session.
    Returns the username on successful login, or:
        FAIL     - problem with user/pass/account/ip
        DISABLED - The database is disabled
    """
    dbo = db.DatabaseInfo()
    database = post["database"]
    username = post["username"]
    password = post["password"]
    nologconnection = post["nologconnection"]
    # Do we have multiple databases?
    if MULTIPLE_DATABASES:
        if MULTIPLE_DATABASES_TYPE == "smcom":
            # Is this sheltermanager.com? If so, we need to get the 
            # database connection info (dbo) before we can login.
            # If a database hasn't been supplied, let's bail out now
            # since we can't do anything
            if str(database).strip() == "":
                return "FAIL"
            else:
                dbo = smcom.get_database_info(database)
                # Bail out if there was a problem with the database
                if dbo.database == "FAIL" or dbo.database == "DISABLED":
                    return dbo.database
        else:
            # Look up the database info from our map
            dbo  = db.get_multiple_database_info(database)
            if dbo.database == "FAIL":
                return dbo.database
    # Connect to the database and authenticate the username and password
    user = authenticate(dbo, username, password)
    if user is not None and not authenticate_ip(user, remoteip):
        al.error("user %s with ip %s failed ip restriction check '%s'" % (username, remoteip, user["IPRESTRICTION"]), "users.web_login", dbo)
        return "FAIL"
    if user is not None:
        al.info("%s successfully authenticated from %s" % (username, remoteip), "users.web_login", dbo)
        try:
            dbo.locked = configuration.smdb_locked(dbo)
            dbo.timezone = configuration.timezone(dbo)
            dbo.installpath = path
            session.locale = configuration.locale(dbo)
            dbo.locale = session.locale
            session.dbo = dbo
            session.user = user["USERNAME"]
            session.superuser = user["SUPERUSER"]
            session.passchange = (password == "password")
            update_session(session)
        except:
            al.error("failed setting up session: %s" % str(sys.exc_info()[0]), "users.web_login", dbo, sys.exc_info())
            return "FAIL"
        try:
            session.securitymap = get_security_map(dbo, user["USERNAME"])
        except:
            # This is a pre-3002 login where the securitymap is with 
            # the user (the error occurs because there's no role table)
            al.debug("role table does not exist, using securitymap from user", "users.web_login", dbo)
            session.securitymap = user["SECURITYMAP"]
        try:
            ur = get_users(dbo, user["USERNAME"])[0]
            session.roles = ur["ROLES"]
            session.roleids = ur["ROLEIDS"]
            session.locationfilter = utils.nulltostr(user["LOCATIONFILTER"])
        except:
            # Users coming from v2 won't have the
            # IPRestriction or EmailAddress fields necessary for get_users - we can't
            # help them right now so just give them an empty set of
            # roles and locationfilter until they login again after the db update
            session.roles = ""
            session.roleids = ""
            session.locationfilter = ""
        try:
            # If it's a sheltermanager.com database, try and update the
            # last time the user connected to today
            if smcom.active() and database != "" and nologconnection == "":
                smcom.set_last_connected(dbo)
        except:
            pass
        try:
            # Check to see if any updates need performing on this database
            if dbupdate.check_for_updates(dbo):
                dbupdate.perform_updates(dbo)
                # We did some updates, better reload just in case config/reports/etc changed
                update_session(session)
            # Check to see if our views and sequences are out of date and need reloading
            if dbupdate.check_for_view_seq_changes(dbo):
                dbupdate.install_db_views(dbo)
                dbupdate.install_db_sequences(dbo)
        except:
            al.error("failed updating database: %s" % str(sys.exc_info()[0]), "users.web_login", dbo, sys.exc_info())
        try:
            # Log out any old users that have been hanging around
            auto_logout(dbo)
            # Let this user through
            login(dbo, user["USERNAME"])
        except:
            al.error("failed updating activeuser table: %s" % str(sys.exc_info()[0]), "users.web_login", dbo, sys.exc_info())
            return "FAIL"
    else:
        al.error("database:%s username:%s password:%s failed authentication from %s" % (database, username, password, remoteip), "users.web_login", dbo)
        return "FAIL"

    return user["USERNAME"]


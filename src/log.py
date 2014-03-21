#!/usr/bin/python

import audit
import db
import i18n
import utils

# Log links
ANIMAL = 0
PERSON = 1
LOSTANIMAL = 2
FOUNDANIMAL = 3
WAITINGLIST = 4
MOVEMENT = 5

ASCENDING = 0
DESCENDING = 1

def add_log(dbo, username, linktype, linkid, logtypeid, logtext):
    logid = db.get_id(dbo, "log")
    sql = db.make_insert_user_sql(dbo, "log", username, (
        ( "ID", db.di(logid) ),
        ( "LogTypeID", db.di(logtypeid) ),
        ( "LinkID", db.di(linkid) ),
        ( "LinkType", db.di(linktype) ),
        ( "Date", db.dd(i18n.now(dbo.timezone)) ),
        ( "Comments", db.ds(logtext) )
        ))
    db.execute(dbo, sql)
    audit.create(dbo, username, "log", str(logid))

def get_logs(dbo, linktypeid, linkid, logtype = 0, sort = DESCENDING):
    """
    Gets a list of logs. <= 0 = all types.
    """
    sql = "SELECT l.*, lt.LogTypeName FROM log l " \
        "INNER JOIN logtype lt ON lt.ID = l.LogTypeID " \
        "WHERE LinkType = %d AND LinkID = %d " % (int(linktypeid), int(linkid))
    if logtype > 0:
        sql += "AND l.LogTypeID = %d " % int(logtype)
    if sort == ASCENDING:
        sql += "ORDER BY l.Date"
    if sort == DESCENDING:
        sql += "ORDER BY l.Date DESC"
    return db.query(dbo, sql)

def insert_log_from_form(dbo, username, linktypeid, linkid, data):
    """
    Creates a log from the form data
    username: User creating the diary
    linktypeid, linkid: The link
    data: The web.py form object
    """
    l = dbo.locale
    if utils.df_kd(data, "logdate", l) is None:
        raise utils.ASMValidationError(i18n._("Log date must be a valid date", l))
    logid = db.get_id(dbo, "log")
    sql = db.make_insert_user_sql(dbo, "log", username, (
        ( "ID", db.di(logid)),
        ( "LogTypeID", utils.df_s(data, "type")),
        ( "LinkID", db.di(linkid) ),
        ( "LinkType", db.di(linktypeid) ),
        ( "Date", utils.df_d(data, "logdate", l) ),
        ( "Comments", utils.df_t(data, "entry") )
        ))
    db.execute(dbo, sql)
    audit.create(dbo, username, "log", str(logid))
    return logid

def update_log_from_form(dbo, username, data):
    """
    Updates a log from form data
    """
    l = dbo.locale
    logid = utils.df_ki(data, "logid")
    if utils.df_kd(data, "logdate", l) is None:
        raise utils.ASMValidationError(i18n._("Log date must be a valid date", l))
    sql = db.make_update_user_sql(dbo, "log", username, "ID=%d" % logid, (
        ( "LogTypeID", utils.df_s(data, "type")),
        ( "Date", utils.df_d(data, "logdate", l) ),
        ( "Comments", utils.df_t(data, "entry") )
        ))
    preaudit = db.query(dbo, "SELECT * FROM log WHERE ID=%d" % logid)
    db.execute(dbo, sql)
    postaudit = db.query(dbo, "SELECT * FROM log WHERE ID=%d" % logid)
    audit.edit(dbo, username, "log", audit.map_diff(preaudit, postaudit))

def delete_log(dbo, username, logid):
    """
    Deletes a log
    """
    audit.delete(dbo, username, "log", str(db.query(dbo, "SELECT * FROM log WHERE ID = %d" % int(logid))))
    db.execute(dbo, "DELETE FROM log WHERE ID = %d" % int(logid))


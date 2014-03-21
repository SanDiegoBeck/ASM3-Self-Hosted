#!/usr/bin/python

import additional
import al
import animal
import audit
import configuration
import db
import diary
import log
import media
import utils
from i18n import _, after, now, python2display, subtract_years, add_days, date_diff

def get_waitinglist_query():
    """
    Returns the SELECT and JOIN commands necessary for selecting
    waiting list rows with resolved lookups.
    """
    return "SELECT * FROM v_animalwaitinglist a"

def get_waitinglist_by_id(dbo, wid):
    """
    Returns a single waitinglist record for the ID given
    """
    l = dbo.locale
    sql = get_waitinglist_query() + " WHERE a.ID = %d" % int(wid)
    rows = db.query(dbo, sql)
    if len(rows) == 0: return None
    r = rows[0]
    ranks = get_waitinglist_ranks(dbo)
    if ranks.has_key(r["WLID"]):
        r["RANK"] = ranks[r["WLID"]]
    else:
        r["RANK"] = ""
    r["TIMEONLIST"] = date_diff(l, r["DATEPUTONLIST"], now(dbo.timezone))
    return r

def get_person_name(dbo, wid):
    """
    Returns the contact name for the waitinglist with id
    """
    return db.query_string(dbo, "SELECT o.OwnerName FROM animalwaitinglist a INNER JOIN owner o ON a.OwnerID = o.ID WHERE a.ID = %d" % int(wid))

def get_waitinglist_ranks(dbo):
    """
    Returns a dictionary of waiting list IDs with their current ranks.
    """
    byspecies = configuration.waiting_list_rank_by_species(dbo)
    if not byspecies:
        rows = db.query(dbo, "SELECT a.ID, a.SpeciesID FROM animalwaitinglist a " \
            "INNER JOIN owner o ON a.OwnerID = o.ID " \
            "WHERE a.DateRemovedFromList Is Null " \
            "ORDER BY a.Urgency, a.DatePutOnList")
    else:
        rows = db.query(dbo, "SELECT a.ID, a.SpeciesID FROM animalwaitinglist a " \
            "INNER JOIN owner o ON a.OwnerID = o.ID " \
            "WHERE a.DateRemovedFromList Is Null " \
            "ORDER BY a.SpeciesID, a.Urgency, a.DatePutOnList")
    ranks = {}
    lastspecies = 0
    rank = 1
    for r in rows:
        if byspecies:
            if not lastspecies == r["SPECIESID"]:
                lastspecies = r["SPECIESID"]
                rank = 1
        ranks[r["ID"]] = rank
        rank += 1
    return ranks

def get_waitinglist(dbo, priorityfloor = 5, species = -1, addresscontains = "", includeremoved = 0, namecontains = "", descriptioncontains = ""):
    """
    Retrieves the waiting list
    priorityfloor: The lowest urgency to show (1 = urgent, 5 = lowest)
    species: A species filter or -1 for all
    addresscontains: A partial address
    includeremoved: Whether or not to include removed entries
    namecontains: A partial name
    descriptioncontains: A partial description
    """
    l = dbo.locale
    ranks = get_waitinglist_ranks(dbo)
    sql = get_waitinglist_query() + " WHERE a.Urgency <= " + str(priorityfloor)
    if includeremoved == 0: sql += " AND a.DateRemovedFromList Is Null"
    if species != -1: sql += " AND a.SpeciesID = " + str(species)
    if addresscontains != "": sql += " AND UPPER(OwnerAddress) Like '%" + str(addresscontains).upper().replace("'", "`") + "%'"
    if namecontains != "": sql += " AND UPPER(OwnerName) Like '%" + str(namecontains).upper().replace("'", "`") + "%'"
    if descriptioncontains != "": sql += " AND UPPER(AnimalDescription) Like '%" + str(descriptioncontains).upper().replace("'", "`") + "%'"
    sql += " ORDER BY a.Urgency, a.DatePutOnList"
    rows = db.query(dbo, sql)
    wlh = configuration.waiting_list_highlights(dbo).split(" ")
    for r in rows:
        r["HIGHLIGHT"] = ""
        for hi in wlh:
            if hi != "":
                if hi.find("|") == -1:
                    wid = hi
                    h = "1"
                else:
                    wid, h = hi.split("|")
                if wid == str(r["WLID"]).strip():
                    r["HIGHLIGHT"] = h
                    break
        if ranks.has_key(r["WLID"]):
            r["RANK"] = ranks[r["WLID"]]
        else:
            r["RANK"] = ""
        r["TIMEONLIST"] = date_diff(l, r["DATEPUTONLIST"], now(dbo.timezone))
    return rows

def get_waitinglist_find_simple(dbo, query = "", limit = 0, onlyindexed = False):
    """
    Returns rows for simple waiting list searches.
    query: The search criteria
    """
    # If no query has been given, do a current waitinglist search
    if query == "":
        return get_waitinglist(dbo)

    ors = []
    add = lambda f: "LOWER(%s) LIKE '%%%s%%'" % (f, query.lower())
    if utils.is_numeric(query):
        ors.append("a.ID = " + str(utils.cint(query)))
    ors.append(add("a.OwnerName"))
    ors.append(add("a.AnimalDescription"))
    if not onlyindexed:
        ors.append(add("a.ReasonForWantingToPart"))
        ors.append(add("a.ReasonForRemoval"))
    sql = get_waitinglist_query() + " WHERE " + " OR ".join(ors)
    if limit > 0: sql += " LIMIT " + str(limit)
    return db.query(dbo, sql)

def get_satellite_counts(dbo, wlid):
    """
    Returns a resultset containing the number of each type of satellite
    record that a waitinglist entry has.
    """
    sql = "SELECT a.ID, " \
        "(SELECT COUNT(*) FROM media me WHERE me.LinkID = a.ID AND me.LinkTypeID = %d) AS media, " \
        "(SELECT COUNT(*) FROM diary di WHERE di.LinkID = a.ID AND di.LinkType = %d) AS diary, " \
        "(SELECT COUNT(*) FROM log WHERE log.LinkID = a.ID AND log.LinkType = %d) AS logs " \
        "FROM animalwaitinglist a WHERE a.ID = %d" \
        % (media.WAITINGLIST, diary.WAITINGLIST, log.WAITINGLIST, int(wlid))
    return db.query(dbo, sql)

def delete_waitinglist(dbo, username, wid):
    """
    Deletes a waiting list record
    """
    audit.delete(dbo, username, "animalwaitinglist", str(db.query(dbo, "SELECT * FROM animalwaitinglist WHERE ID=%d" % wid)))
    db.execute(dbo, "DELETE FROM animalwaitinglist WHERE ID = %d" % wid)

def update_waitinglist_remove(dbo, username, wid):
    """
    Marks a waiting list record as removed
    """
    db.execute(dbo, "UPDATE animalwaitinglist SET DateRemovedFromList = %s WHERE ID = %d" % ( db.dd(now(dbo.timezone)), int(wid) ))
    audit.edit(dbo, username, "animalwaitinglist", "%s: DateRemovedFromList ==> %s" % ( str(wid), python2display(dbo.locale, now(dbo.timezone))))

def update_waitinglist_highlight(dbo, wlid, himode):
    """
    Toggles a waiting list ID record as highlighted.
    wlid: The waiting list id to toggle
    himode: a highlight value from 1 to 5 for a colour
    """
    hl = list(configuration.waiting_list_highlights(dbo).split(" "))
    wlid = str(wlid).strip()
    # Create a new highlight list that doesn't have our id in it
    nl = []
    removed = False
    for hi in hl:
        if hi != "":
            if hi.find("|") != -1:
                wid, h = hi.split("|")
            else:
                wid = hi
                h = "1"
            if wlid == wid:
                removed = True
            else:
                nl.append(wid + "|" + h)
    # If our id wasn't present in the list, add it (so we're
    # effectively toggling the id on and off)
    if not removed:
        nl.append(wlid + "|" + himode)
    configuration.waiting_list_highlights(dbo, " ".join(nl))

def auto_remove_waitinglist(dbo):
    """
    Finds and automatically marks entries removed that have gone past
    the last contact date + weeks.
    """
    l = dbo.locale
    rows = db.query(dbo, "SELECT a.ID, a.DateOfLastOwnerContact, " \
        "a.AutoRemovePolicy " \
        "FROM animalwaitinglist a WHERE a.DateRemovedFromList Is Null " \
        "AND AutoRemovePolicy > 0 AND DateOfLastOwnerContact Is Not Null")
    updates = []
    for r in rows:
        xdate = add_days(r["DATEOFLASTOWNERCONTACT"], 7 * r["AUTOREMOVEPOLICY"])
        if after(now(dbo.timezone), xdate):
            al.debug("auto removing waitinglist entry %d due to policy" % int(r["ID"]), "waitinglist.auto_remove_waitinglist", dbo)
            updates.append((now(dbo.timezone), _("Auto removed due to lack of owner contact.", l), r["ID"]))
    if len(updates) > 0:
        db.execute_many(dbo, "UPDATE animalwaitinglist SET DateRemovedFromList = %s, " \
            "ReasonForRemoval=%s WHERE ID=%s", updates)
        
def auto_update_urgencies(dbo):
    """
    Finds all animals where the next UrgencyUpdateDate field is greater
    than or equal to today and the urgency is larger than High (so we
    can never reach Urgent).
    """
    update_period_days = configuration.waiting_list_urgency_update_period(dbo)
    if update_period_days == 0:
        al.debug("urgency update period is 0, not updating waiting list entries", "waitinglist.auto_update_urgencies", dbo)
        return
    rows = db.query(dbo, "SELECT a.* " \
        "FROM animalwaitinglist a WHERE UrgencyUpdateDate <= %s " \
        "AND Urgency > 2" % db.dd(now(dbo.timezone)))
    updates = []
    for r in rows:
        al.debug("increasing urgency of waitinglist entry %d" % int(r["ID"]), "waitinglist.auto_update_urgencies", dbo)
        updates.append((now(dbo.timezone), add_days(r["URGENCYUPDATEDATE"], update_period_days), r["URGENCY"] - 1, r["ID"]))
    if len(updates) > 0:
        db.execute_many(dbo, "UPDATE animalwaitinglist SET " \
            "UrgencyLastUpdatedDate=%s, " \
            "UrgencyUpdateDate=%s, " \
            "Urgency=%s " \
            "WHERE ID=%s ", updates)
            
def update_waitinglist_from_form(dbo, data, username):
    """
    Updates a waiting list record from the screen
    data: The webpy data object containing form parameters
    """
    l = dbo.locale
    wlid = utils.df_ki(data, "id")
    if utils.df_ks(data, "description") == "":
        raise utils.ASMValidationError(_("Description cannot be blank", l))
    if utils.df_ki(data, "owner") == "0":
        raise utils.ASMValidationError(_("Waiting list entries must have a contact", l))
    if utils.df_ks(data, "dateputon") == "":
        raise utils.ASMValidationError(_("Date put on cannot be blank", l))

    preaudit = db.query(dbo, "SELECT * FROM animalwaitinglist WHERE ID = %d" % wlid)
    db.execute(dbo, db.make_update_user_sql(dbo, "animalwaitinglist", username, "ID=%d" % wlid, (
        ( "SpeciesID", utils.df_s(data, "species")),
        ( "DatePutOnList", utils.df_d(data, "dateputon", l)),
        ( "OwnerID", utils.df_s(data, "owner")),
        ( "AnimalDescription", utils.df_t(data, "description")),
        ( "ReasonForWantingToPart", utils.df_t(data, "reasonforwantingtopart")),
        ( "CanAffordDonation", utils.df_c(data, "canafforddonation")), 
        ( "Urgency", utils.df_s(data, "urgency")),
        ( "DateRemovedFromList", utils.df_d(data, "dateremoved", l)),
        ( "AutoRemovePolicy", utils.df_s(data, "autoremovepolicy")),
        ( "DateOfLastOwnerContact", utils.df_d(data, "dateoflastownercontact", l)),
        ( "ReasonForRemoval", utils.df_t(data, "reasonforremoval")),
        ( "Comments", utils.df_t(data, "comments"))
        )))
    additional.save_values_for_link(dbo, data, wlid, "waitinglist")
    postaudit = db.query(dbo, "SELECT * FROM animalwaitinglist WHERE ID = %d" % wlid)
    audit.edit(dbo, username, "animalwaitinglist", audit.map_diff(preaudit, postaudit))

def insert_waitinglist_from_form(dbo, data, username):
    """
    Creates a waiting list record from the screen
    data: The webpy data object containing form parameters
    """
    l = dbo.locale
    if utils.df_ks(data, "description") == "":
        raise utils.ASMValidationError(_("Description cannot be blank", l))
    if utils.df_ki(data, "owner") == "0":
        raise utils.ASMValidationError(_("Waiting list entries must have a contact", l))
    if utils.df_ks(data, "dateputon") == "":
        raise utils.ASMValidationError(_("Date put on cannot be blank", l))
    nwlid = db.get_id(dbo, "animalwaitinglist")
    db.execute(dbo, db.make_insert_user_sql(dbo, "animalwaitinglist", username, (
        ( "ID", db.di(nwlid)),
        ( "SpeciesID", utils.df_s(data, "species")),
        ( "DatePutOnList", utils.df_d(data, "dateputon", l)),
        ( "OwnerID", utils.df_s(data, "owner")),
        ( "AnimalDescription", utils.df_t(data, "description")),
        ( "ReasonForWantingToPart", utils.df_t(data, "reasonforwantingtopart")),
        ( "CanAffordDonation", utils.df_c(data, "canafforddonation")), 
        ( "Urgency", utils.df_s(data, "urgency")),
        ( "DateRemovedFromList", utils.df_d(data, "dateremoved", l)),
        ( "AutoRemovePolicy", utils.df_s(data, "autoremovepolicy")),
        ( "DateOfLastOwnerContact", db.dd(now(dbo.timezone))), 
        ( "ReasonForRemoval", utils.df_t(data, "reasonforremoval")),
        ( "Comments", utils.df_t(data, "comments")),
        ( "UrgencyLastUpdatedDate", db.dd(now(dbo.timezone))),
        ( "UrgencyUpdateDate", db.dd(add_days(now(dbo.timezone), configuration.waiting_list_urgency_update_period(dbo))))
        )))
    audit.create(dbo, username, "animalwaitinglist", str(nwlid))
    return nwlid

def create_animal(dbo, username, wlid):
    """
    Creates an animal record from a waiting list entry with the id given
    """
    a = db.query(dbo, "SELECT * FROM animalwaitinglist WHERE ID = %d" % wlid)[0]
    l = dbo.locale
    data = {
        "animalname":           _("Waiting List {0}", l).format(wlid),
        "markings":             str(a["ANIMALDESCRIPTION"]),
        "reasonforentry":       str(a["REASONFORWANTINGTOPART"]),
        "species":              str(a["SPECIESID"]),
        "comments":             str(a["COMMENTS"]),
        "broughtinby":          str(a["OWNERID"]),
        "originalowner":        str(a["OWNERID"]),
        "animaltype":           configuration.default_type(dbo),
        "breed1":               configuration.default_breed(dbo),
        "breed2":               configuration.default_breed(dbo),
        "basecolour":           configuration.default_colour(dbo),
        "size":                 configuration.default_size(dbo),
        "internallocation":     configuration.default_location(dbo),
        "dateofbirth":          python2display(l, subtract_years(now(dbo.timezone))),
        "estimateddob":         "1"
    }
    # If we're creating shelter codes manually, we need to put something unique
    # in there for now. Use the id
    if configuration.manual_codes(dbo):
        data["sheltercode"] = "WL" + str(wlid)
        data["shortcode"] = "WL" + str(wlid)
    nextid, code = animal.insert_animal_from_form(dbo, data, username)
    # Now that we've created our animal, we should remove this entry from the waiting list
    db.execute(dbo, "UPDATE animalwaitinglist SET DateRemovedFromList = %s, ReasonForRemoval = %s " \
        "WHERE ID = %d" % ( 
        db.dd(now(dbo.timezone)), 
        db.ds(_("Moved to animal record {0}", l).format(code)),
        wlid))
    return nextid
   


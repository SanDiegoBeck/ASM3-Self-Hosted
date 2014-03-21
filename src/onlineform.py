#!/usr/bin/python

import al
import audit
import configuration
import db
import dbfs
import i18n
import html
import lostfound
import media
import person
import utils
import waitinglist
from sitedefs import BASE_URL

FIELDTYPE_YESNO = 0
FIELDTYPE_TEXT = 1
FIELDTYPE_NOTES = 2
FIELDTYPE_LOOKUP = 3

# Online field names that we recognise and will attempt to map to
# owner fields when importing from submitted forms
FORM_FIELDS = [
    "title", "initials", "firstname", "forenames", "surname", "lastname", "address",
    "town", "city", "county", "state", "postcode", "zipcode", "hometelephone", 
    "worktelephone", "mobiletelephone", "celltelephone", "emailaddress",
    "description", "reason", "species", "breed", "agegroup", "color", "colour", 
    "arealost", "areafound", "areapostcode", "areazipcode"
]

def get_onlineforms(dbo):
    """ Return all online forms """
    return db.query(dbo, "SELECT *, (SELECT COUNT(*) FROM onlineformfield WHERE OnlineFormID = onlineform.ID) AS NumberOfFields FROM onlineform ORDER BY Name")

def get_onlineform_html(dbo, formid, completedocument = True):
    """ Get the selected online form as HTML """
    h = []
    l = dbo.locale
    form = db.query(dbo, "SELECT * FROM onlineform WHERE ID = %d" % formid)[0]
    if completedocument:
        header = get_onlineform_header(dbo)
        h.append(header.replace("$$TITLE$$", form["NAME"]))
        h.append('<h2 class="asm-onlineform-title">%s</h2>' % form["NAME"])
        h.append('<p class="asm-onlineform-description">%s</p>' % form["DESCRIPTION"])
    h.append('<form action="%s/service" method="post">' % BASE_URL)
    h.append('<input type="hidden" name="method" value="online_form_post" />')
    h.append('<input type="hidden" name="account" value="%s" />' % dbo.alias)
    h.append('<input type="hidden" name="redirect" value="%s" />' % form["REDIRECTURLAFTERPOST"])
    h.append('<input type="hidden" name="flags" value="%s" />' % form["SETOWNERFLAGS"])
    h.append('<input type="hidden" name="formname" value="%s" />' % html.escape(form["NAME"]))
    h.append('<table width="100%" class="asm-onlineform-table">')
    for f in get_onlineformfields(dbo, formid):
        fname = f["FIELDNAME"] + "_" + str(f["ID"])
        h.append('<tr class="asm-onlineform-tr">')
        h.append('<td class="asm-onlineform-td">')
        h.append('<label for="f%d">%s</label>' % ( f["ID"], f["LABEL"] ))
        h.append('</td>')
        h.append('<td class="asm-onlineform-td">')
        if f["FIELDTYPE"] == FIELDTYPE_YESNO:
            h.append('<select name="%s" title="%s"><option>%s</option><option>%s</option></select>' % \
                ( html.escape(fname), utils.nulltostr(f["TOOLTIP"]), i18n._("No", l), i18n._("Yes", l)))
        elif f["FIELDTYPE"] == FIELDTYPE_TEXT:
            h.append('<input type="text" name="%s" title="%s" />' % ( html.escape(fname), utils.nulltostr(f["TOOLTIP"])))
        elif f["FIELDTYPE"] == FIELDTYPE_NOTES:
            h.append('<textarea name="%s" title="%s"></textarea>' % ( html.escape(fname), utils.nulltostr(f["TOOLTIP"])))
        elif f["FIELDTYPE"] == FIELDTYPE_LOOKUP:
            h.append('<select name="%s" title="%s">' % ( html.escape(fname), utils.nulltostr(f["TOOLTIP"])))
            for lv in utils.nulltostr(f["LOOKUPS"]).split("|"):
                h.append('<option>%s</option>' % lv)
            h.append('</select>')
        h.append('</td>')
        h.append('</tr>')
    h.append('</table>')
    h.append('<p style="text-align: center"><input type="submit" value="Submit" /></p>')
    h.append('</form>')
    if completedocument:
        footer = get_onlineform_footer(dbo)
        h.append(footer.replace("$$TITLE$$", form["NAME"]))
    return "\n".join(h)

def get_onlineform_header(dbo):
    header = dbfs.get_string_filepath(dbo, "/onlineform/head.html")
    if header == "": header = "<html>\n<head>\n<title>$$TITLE$$</title>\n</head>\n<body>"
    return header

def get_onlineform_footer(dbo):
    footer = dbfs.get_string_filepath(dbo, "/onlineform/foot.html")
    if footer == "": footer = "</body>\n</html>"
    return footer

def get_onlineform_name(dbo, formid):
    """ Returns the name of a form """
    return db.query_string(dbo, "SELECT Name FROM onlineform WHERE ID = %d" % int(formid))

def get_onlineformfields(dbo, formid):
    """ Return all fields for a form """
    return db.query(dbo, "SELECT * FROM onlineformfield WHERE OnlineFormID=%d ORDER BY DisplayIndex" % formid)

def get_onlineformincoming_headers(dbo):
    """ Returns all incoming form posts """
    return db.query(dbo, "SELECT DISTINCT f.CollationID, f.FormName, f.PostedDate, f.Host, f.Preview " \
        "FROM onlineformincoming f ORDER BY f.PostedDate")

def get_onlineformincoming_detail(dbo, collationid):
    """ Returns the detail lines for an incoming post """
    return db.query(dbo, "SELECT * FROM onlineformincoming WHERE CollationID = %d ORDER BY DisplayIndex" % int(collationid))

def get_onlineformincoming_html(dbo, collationid):
    """ Returns an HTML fragment of the incoming form data """
    h = []
    h.append('<table width="100%">')
    for f in get_onlineformincoming_detail(dbo, collationid):
        label = f["LABEL"]
        if label is None or label == "": label = f["FIELDNAME"]
        h.append('<tr>')
        h.append('<td>%s</td>' % label )
        h.append('<td>%s</td>' % f["VALUE"])
        h.append('</tr>')
    h.append('</table>')
    return "\n".join(h)

def get_onlineformincoming_name(dbo, collationid):
    """ Returns the form name for a collation id """
    return db.query_string(dbo, "SELECT FormName FROM onlineformincoming WHERE CollationID = %d LIMIT 1" % int(collationid))

def insert_onlineform_from_form(dbo, username, data):
    """
    Create an onlineform record from posted data
    """
    formid = db.get_id(dbo, "onlineform")
    sql = db.make_insert_sql("onlineform", ( 
        ( "ID", db.di(formid)),
        ( "Name", db.ds(utils.df_ks(data, "name"))),
        ( "RedirectUrlAfterPOST", db.ds(utils.df_ks(data, "redirect"))),
        ( "SetOwnerFlags", db.ds(utils.df_ks(data, "flags"))),
        ( "Description", db.ds(utils.df_ks(data, "description")))
        ))
    db.execute(dbo, sql)
    audit.create(dbo, username, "onlineform", str(formid))
    return formid

def update_onlineform_from_form(dbo, username, data):
    """
    Update an onlineform record from posted data
    """
    formid = utils.df_ki(data, "formid")
    sql = db.make_update_sql("onlineform", "ID=%d" % formid, ( 
        ( "Name", db.ds(utils.df_ks(data, "name"))),
        ( "RedirectUrlAfterPOST", db.ds(utils.df_ks(data, "redirect"))),
        ( "SetOwnerFlags", db.ds(utils.df_ks(data, "flags"))),
        ( "Description", db.ds(utils.df_ks(data, "description")))
        ))
    preaudit = db.query(dbo, "SELECT * FROM onlineform WHERE ID = %d" % formid)
    db.execute(dbo, sql)
    postaudit = db.query(dbo, "SELECT * FROM onlineform WHERE ID = %d" % formid)
    audit.edit(dbo, username, "onlineform", audit.map_diff(preaudit, postaudit))

def delete_onlineform(dbo, username, formid):
    """
    Deletes the specified onlineform and fields
    """
    audit.delete(dbo, username, "onlineform", str(db.query(dbo, "SELECT * FROM onlineform WHERE ID=%d" % int(formid))))
    db.execute(dbo, "DELETE FROM onlineformfield WHERE OnlineFormID = %d" % int(formid))
    db.execute(dbo, "DELETE FROM onlineform WHERE ID = %d" % int(formid))

def insert_onlineformfield_from_form(dbo, username, data):
    """
    Create an onlineformfield record from posted data
    """
    formfieldid = db.get_id(dbo, "onlineformfield")
    sql = db.make_insert_sql("onlineformfield", ( 
        ( "ID", db.di(formfieldid)),
        ( "OnlineFormID", db.di(utils.df_ki(data, "formid"))),
        ( "FieldName", db.ds(utils.df_ks(data, "fieldname"))),
        ( "FieldType", db.di(utils.df_ki(data, "fieldtype"))),
        ( "Label", db.ds(utils.df_ks(data, "label"))),
        ( "DisplayIndex", db.di(utils.df_ki(data, "displayindex"))),
        ( "Lookups", db.ds(utils.df_ks(data, "lookups"))),
        ( "Tooltip", db.ds(utils.df_ks(data, "tooltip")))
        ))
    db.execute(dbo, sql)
    audit.create(dbo, username, "onlineformfield", str(formfieldid))
    return formfieldid

def update_onlineformfield_from_form(dbo, username, data):
    """
    Update an onlineformfield record from posted data
    """
    formfieldid = utils.df_ki(data, "formfieldid")
    sql = db.make_update_sql("onlineformfield", "ID=%d" % formfieldid, ( 
        ( "FieldName", db.ds(utils.df_ks(data, "fieldname"))),
        ( "FieldType", db.di(utils.df_ki(data, "fieldtype"))),
        ( "Label", db.ds(utils.df_ks(data, "label"))),
        ( "DisplayIndex", db.di(utils.df_ki(data, "displayindex"))),
        ( "Lookups", db.ds(utils.df_ks(data, "lookups"))),
        ( "Tooltip", db.ds(utils.df_ks(data, "tooltip")))
        ))
    preaudit = db.query(dbo, "SELECT * FROM onlineformfield WHERE ID = %d" % formfieldid)
    db.execute(dbo, sql)
    postaudit = db.query(dbo, "SELECT * FROM onlineformfield WHERE ID = %d" % formfieldid)
    audit.edit(dbo, username, "onlineformfield", audit.map_diff(preaudit, postaudit))

def delete_onlineformfield(dbo, username, fieldid):
    """
    Deletes the specified onlineformfield
    """
    audit.delete(dbo, username, "onlineformfield", str(db.query(dbo, "SELECT * FROM onlineformfield WHERE ID=%d" % int(fieldid))))
    db.execute(dbo, "DELETE FROM onlineformfield WHERE ID = %d" % int(fieldid))

def insert_onlineformincoming_from_form(dbo, data, remoteip):
    """
    Create onlineformincoming records from posted data. We 
    create a row for every key/value pair in the posted data
    with a unique collation ID.
    """
    IGNORE_FIELDS = [ "formname", "flags", "redirect", "account", "filechooser", "method" ]
    collationid = db.query_int(dbo, "SELECT MAX(CollationID) FROM onlineformincoming") + 1
    formname = utils.df_ks(data, "formname")
    posteddate = i18n.now(dbo.timezone)
    flags = utils.df_ks(data, "flags")
    for k, v in data.iteritems():
        if k not in IGNORE_FIELDS:
            label = ""
            displayindex = 0
            fieldname = k
            # Form fields should have a _ONLINEFORMFIELD.ID suffix we can use to get the
            # original label and display position
            if k.find("_") != -1:
                fid = utils.cint(k[k.rfind("_")+1:])
                fieldname = k[0:k.rfind("_")]
                if fid != 0:
                    fld = db.query(dbo, "SELECT Label, DisplayIndex FROM onlineformfield WHERE ID = %d" % fid)
                    if len(fld) > 0:
                        label = fld[0]["LABEL"]
                        displayindex = fld[0]["DISPLAYINDEX"]

            sql = db.make_insert_sql("onlineformincoming", ( 
                ( "CollationID", db.di(collationid)),
                ( "FormName", db.ds(formname)),
                ( "PostedDate", db.ddt(posteddate)),
                ( "Flags", db.ds(flags)),
                ( "FieldName", db.ds(fieldname)),
                ( "Label", db.ds(label)),
                ( "DisplayIndex", db.di(displayindex)),
                ( "Host", db.ds(remoteip)),
                ( "Value", db.ds(v))
                ))
            db.execute(dbo, sql)
    # Sort out the preview of the first few fields
    fieldssofar = 0
    preview = []
    for fld in get_onlineformincoming_detail(dbo, collationid):
        if fieldssofar < 3:
            fieldssofar += 1
            preview.append( fld["LABEL"] + ": " + fld["VALUE"] )
    db.execute(dbo, "UPDATE onlineformincoming SET Preview = %s WHERE CollationID = %s" % ( db.ds(", ".join(preview)), db.di(collationid) ))
    return collationid

def delete_onlineformincoming(dbo, username, collationid):
    """
    Deletes the specified onlineformincoming set
    """
    audit.delete(dbo, username, "onlineformincoming", str(db.query(dbo, "SELECT * FROM onlineformincoming WHERE CollationID=%d" % int(collationid))))
    db.execute(dbo, "DELETE FROM onlineformincoming WHERE CollationID = %d" % int(collationid))

def guess_agegroup(dbo, s):
    """ Guesses an agegroup, returns the default if no match is found """
    s = str(s).lower()
    guess = db.query_string(dbo, "SELECT ItemValue FROM configuration WHERE ItemName LIKE 'AgeGroup%Name' AND LOWER(ItemValue) LIKE '%" + db.escape(s) + "%'")
    if guess != "": return guess
    return db.query_string(dbo, "SELECT ItemValue FROM configuration WHERE ItemName LIKE 'AgeGroup2Name'")

def guess_breed(dbo, s):
    """ Guesses a breed, returns the default if no match is found """
    s = str(s).lower()
    guess = db.query_int(dbo, "SELECT ID FROM breed WHERE LOWER(BreedName) LIKE '%" + db.escape(s) + "%'")
    if guess != 0: return guess
    return configuration.default_breed(dbo)

def guess_colour(dbo, s):
    """ Guesses a colour, returns the default if no match is found """
    s = str(s).lower()
    guess = db.query_int(dbo, "SELECT ID FROM basecolour WHERE LOWER(BaseColour) LIKE '%" + db.escape(s) + "%'")
    if guess != 0: return guess
    return configuration.default_colour(dbo)

def guess_sex(dummy, s):
    """ Guesses a sex """
    if s.lower().startswith("M"):
        return 1
    return 0

def guess_species(dbo, s):
    """ Guesses a species, returns the default if no match is found """
    s = str(s).lower()
    guess = db.query_int(dbo, "SELECT ID FROM species WHERE LOWER(SpeciesName) LIKE '%" + db.escape(s) + "%'")
    if guess != 0: return guess
    return configuration.default_species(dbo)

def create_person(dbo, username, collationid):
    """
    Creates a person record from the incoming form data with collationid.
    Also, attaches the form to the person as media.
    The return value is tuple of collationid, personid, personname
    """
    l = dbo.locale
    fields = get_onlineformincoming_detail(dbo, collationid)
    d = {}
    flags = None
    for f in fields:
        if flags is None: flags = f["FLAGS"]
        if f["FIELDNAME"] == "title": d["title"] = f["VALUE"]
        if f["FIELDNAME"] == "forenames": d["forenames"] = f["VALUE"]
        if f["FIELDNAME"] == "firstname": d["forenames"] = f["VALUE"]
        if f["FIELDNAME"] == "surname": d["surname"] = f["VALUE"]
        if f["FIELDNAME"] == "lastname": d["surname"] = f["VALUE"]
        if f["FIELDNAME"] == "address": d["address"] = f["VALUE"]
        if f["FIELDNAME"] == "town": d["town"] = f["VALUE"]
        if f["FIELDNAME"] == "city": d["town"] = f["VALUE"]
        if f["FIELDNAME"] == "county": d["county"] = f["VALUE"]
        if f["FIELDNAME"] == "state": d["county"] = f["VALUE"]
        if f["FIELDNAME"] == "postcode": d["postcode"] = f["VALUE"]
        if f["FIELDNAME"] == "zipcode": d["postcode"] = f["VALUE"]
        if f["FIELDNAME"] == "hometelephone": d["hometelephone"] = f["VALUE"]
        if f["FIELDNAME"] == "worktelephone": d["worktelephone"] = f["VALUE"]
        if f["FIELDNAME"] == "mobiletelephone": d["mobiletelephone"] = f["VALUE"]
        if f["FIELDNAME"] == "celltelephone": d["mobiletelephone"] = f["VALUE"]
        if f["FIELDNAME"] == "emailaddress": d["emailaddress"] = f["VALUE"]
    d["flags"] = flags
    # Have we got enough info to create the person record? We just need a surname
    if not d.has_key("surname"):
        raise utils.ASMValidationError(i18n._("There is not enough information in the form to create a person record (need a surname).", l))
    # Create the person record
    personid = person.insert_person_from_form(dbo, d, username)
    personname = person.get_person_name_code(dbo, personid)
    # Attach the form to the person
    formname = get_onlineformincoming_name(dbo, collationid)
    formhtml = get_onlineformincoming_html(dbo, collationid)
    media.create_document_media(dbo, username, media.PERSON, personid, formname, formhtml )
    return (collationid, personid, personname)

def create_lostanimal(dbo, username, collationid):
    """
    Creates a lost animal record from the incoming form data with collationid.
    Also, attaches the form to the lost animal as media.
    """
    l = dbo.locale
    fields = get_onlineformincoming_detail(dbo, collationid)
    d = {}
    d["datelost"] = i18n.python2display(l, i18n.now(dbo.timezone))
    d["datereported"] = i18n.python2display(l, i18n.now(dbo.timezone))
    for f in fields:
        if f["FIELDNAME"] == "species": d["species"] = guess_species(dbo, f["VALUE"])
        if f["FIELDNAME"] == "sex": d["sex"] = guess_sex(dbo, f["VALUE"])
        if f["FIELDNAME"] == "breed": d["breed"] = guess_breed(dbo, f["VALUE"])
        if f["FIELDNAME"] == "agegroup": d["agegroup"] = guess_agegroup(dbo, f["VALUE"])
        if f["FIELDNAME"] == "color": d["colour"] = guess_colour(dbo, f["VALUE"])
        if f["FIELDNAME"] == "colour": d["colour"] = guess_colour(dbo, f["VALUE"])
        if f["FIELDNAME"] == "description": d["markings"] = f["VALUE"]
        if f["FIELDNAME"] == "arealost": d["arealost"] = f["VALUE"]
        if f["FIELDNAME"] == "areapostcode": d["areapostcode"] = f["VALUE"]
        if f["FIELDNAME"] == "areazipcode": d["areazipcode"] = f["VALUE"]
    if not d.has_key("species"): d["species"] = guess_species(dbo, "")
    if not d.has_key("sex"): d["sex"] = guess_sex(dbo, "")
    if not d.has_key("breed"): d["breed"] = guess_breed(dbo, "")
    if not d.has_key("agegroup"): d["agegroup"] = guess_agegroup(dbo, "")
    if not d.has_key("colour"): d["colour"] = guess_colour(dbo, "")
    # Have we got enough info to create the lost animal record? We need a description and arealost
    if not d.has_key("markings") or not d.has_key("arealost"):
        raise utils.ASMValidationError(i18n._("There is not enough information in the form to create a lost animal record (need a description and area lost).", l))
    # We need the person record before we create the lost animal
    collationid, personid, personname = create_person(dbo, username, collationid)
    d["owner"] = personid
    # Create the lost animal
    lostanimalid = lostfound.insert_lostanimal_from_form(dbo, d, username)
    # Attach the form to the lost animal
    formname = get_onlineformincoming_name(dbo, collationid)
    formhtml = get_onlineformincoming_html(dbo, collationid)
    media.create_document_media(dbo, username, media.LOSTANIMAL, lostanimalid, formname, formhtml )
    return (collationid, lostanimalid, utils.padleft(lostanimalid, 6) + " - " + personname)
  
def create_foundanimal(dbo, username, collationid):
    """
    Creates a found animal record from the incoming form data with collationid.
    Also, attaches the form to the found animal as media.
    """
    l = dbo.locale
    fields = get_onlineformincoming_detail(dbo, collationid)
    d = {}
    d["datefound"] = i18n.python2display(l, i18n.now(dbo.timezone))
    d["datereported"] = i18n.python2display(l, i18n.now(dbo.timezone))
    for f in fields:
        if f["FIELDNAME"] == "species": d["species"] = guess_species(dbo, f["VALUE"])
        if f["FIELDNAME"] == "sex": d["sex"] = guess_sex(dbo, f["VALUE"])
        if f["FIELDNAME"] == "breed": d["breed"] = guess_breed(dbo, f["VALUE"])
        if f["FIELDNAME"] == "agegroup": d["agegroup"] = guess_agegroup(dbo, f["VALUE"])
        if f["FIELDNAME"] == "color": d["colour"] = guess_colour(dbo, f["VALUE"])
        if f["FIELDNAME"] == "colour": d["colour"] = guess_colour(dbo, f["VALUE"])
        if f["FIELDNAME"] == "description": d["markings"] = f["VALUE"]
        if f["FIELDNAME"] == "areafound": d["areafound"] = f["VALUE"]
        if f["FIELDNAME"] == "areapostcode": d["areapostcode"] = f["VALUE"]
        if f["FIELDNAME"] == "areazipcode": d["areazipcode"] = f["VALUE"]
    if not d.has_key("species"): d["species"] = guess_species(dbo, "")
    if not d.has_key("sex"): d["sex"] = guess_sex(dbo, "")
    if not d.has_key("breed"): d["breed"] = guess_breed(dbo, "")
    if not d.has_key("agegroup"): d["agegroup"] = guess_agegroup(dbo, "")
    if not d.has_key("colour"): d["colour"] = guess_colour(dbo, "")
    # Have we got enough info to create the found animal record? We need a description and areafound
    if not d.has_key("markings") or not d.has_key("areafound"):
        raise utils.ASMValidationError(i18n._("There is not enough information in the form to create a found animal record (need a description and area found).", l))
    # We need the person record before we create the found animal
    collationid, personid, personname = create_person(dbo, username, collationid)
    d["owner"] = personid
    # Create the found animal
    foundanimalid = lostfound.insert_foundanimal_from_form(dbo, d, username)
    # Attach the form to the found animal
    formname = get_onlineformincoming_name(dbo, collationid)
    formhtml = get_onlineformincoming_html(dbo, collationid)
    media.create_document_media(dbo, username, media.FOUNDANIMAL, foundanimalid, formname, formhtml )
    return (collationid, foundanimalid, utils.padleft(foundanimalid, 6) + " - " + personname)
  
def create_waitinglist(dbo, username, collationid):
    """
    Creates a waitinglist record from the incoming form data with collationid.
    Also, attaches the form to the waiting list as media.
    """
    l = dbo.locale
    fields = get_onlineformincoming_detail(dbo, collationid)
    d = {}
    d["dateputon"] = i18n.python2display(l, i18n.now(dbo.timezone))
    d["urgency"] = "5"
    for f in fields:
        if f["FIELDNAME"] == "species": d["species"] = guess_species(dbo, f["VALUE"])
        if f["FIELDNAME"] == "description": d["description"] = f["VALUE"]
        if f["FIELDNAME"] == "reason": d["reasonforwantingtopart"] = f["VALUE"]
    if not d.has_key("species"): d["species"] = guess_species(dbo, "")
    # Have we got enough info to create the waiting list record? We need a description
    if not d.has_key("description"):
        raise utils.ASMValidationError(i18n._("There is not enough information in the form to create a waiting list record (need a description).", l))
    # We need the person record before we create the waiting list
    collationid, personid, personname = create_person(dbo, username, collationid)
    d["owner"] = personid
    # Create the waiting list
    wlid = waitinglist.insert_waitinglist_from_form(dbo, d, username)
    # Attach the form to the waiting list
    formname = get_onlineformincoming_name(dbo, collationid)
    formhtml = get_onlineformincoming_html(dbo, collationid)
    media.create_document_media(dbo, username, media.WAITINGLIST, wlid, formname, formhtml )
    return (collationid, wlid, utils.padleft(wlid, 6) + " - " + personname)
  

def auto_remove_old_incoming_forms(dbo):
    """
    Automatically removes incoming forms older than the daily amount set
    """
    removeafter = configuration.auto_remove_incoming_forms_days(dbo)
    if removeafter <= 0:
        al.debug("auto remove incoming forms is off.", "onlineform.auto_remove_old_incoming_forms")
        return
    removecutoff = i18n.subtract_days(i18n.now(dbo.timezone), removeafter)
    al.debug("remove date: incoming forms < %s" % db.dd(removecutoff), "onlineform.auto_remove_old_incoming_forms")
    sql = "DELETE FROM onlineformincoming WHERE PostedDate < %s" % db.dd(removecutoff)
    count = db.execute(dbo, sql)
    al.debug("removed %d incoming forms older than %d days" % (count, int(removeafter)), "onlineform.auto_remove_old_incoming_forms", dbo)


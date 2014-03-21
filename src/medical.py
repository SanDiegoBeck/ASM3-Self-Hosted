#!/usr/bin/python

import audit
import datetime
import db
import utils
from i18n import _, now, add_days, subtract_days

# Medical treatment rules
FIXED_LENGTH = 0
UNSPECIFIED_LENGTH = 1

# Medical statuses
ACTIVE = 0
HELD = 1
COMPLETED = 2

# Medical frequencies
ONEOFF = 0
DAILY = 0
WEEKLY = 1
MONTHLY = 2
YEARLY = 3

# Sort ordering
ASCENDING_REQUIRED = 0
ASCENDING_NAME = 0
DESCENDING_NAME = 1
DESCENDING_REQUIRED = 1
DESCENDING_GIVEN = 2

def get_vaccinations(dbo, animalid, onlygiven = False, sort = ASCENDING_REQUIRED):
    """
    Returns a recordset of vaccinations for an animal:
    VACCINATIONTYPE, DATEREQUIRED, DATEOFVACCINATION, COMMENTS, COST
    """
    dg = ""
    if onlygiven:
        dg = "DateOfVaccination Is Not Null AND "
    sql = "SELECT * FROM v_animalvaccination " \
        "WHERE %sAnimalID = %d" % (dg, animalid)
    if sort == ASCENDING_REQUIRED:
        sql += " ORDER BY DateRequired"
    elif sort == DESCENDING_REQUIRED:
        sql += " ORDER BY DateRequired DESC"
    return db.query(dbo, sql)

def get_vaccinated(dbo, animalid):
    """
    Returns true if the animal has had at least one vaccination given
    """
    return 0 < db.query_int(dbo, "SELECT COUNT(ID) FROM animalvaccination " \
        "WHERE AnimalID = %d AND DateOfVaccination Is Not Null" % animalid)

def get_regimens(dbo, animalid, onlycomplete = False, sort = ASCENDING_REQUIRED):
    """
    Returns a recordset of medical regimens for an animal:
    TREATMENTNAME, COST, COMMENTS, NAMEDFREQUENCY, NAMEDNUMBEROFTREATMENTS,
    NAMEDSTATUS, DOSAGE, STARTDATE, TREATMENTSGIVEN, TREATMENTSREMAINING,
    TIMINGRULE, TIMINGRULEFREQUENCY, TIMINGRULENOFREQUENCIES, TREATMENTRULE
    TOTALNUMBEROFTREATMENTS
    """
    l = dbo.locale
    sc = ""
    if onlycomplete:
        sc = "am.Status = 2 AND "
    sql = "SELECT am.* FROM animalmedical am WHERE %sam.AnimalID = %d" % (sc, animalid)
    if sort == ASCENDING_REQUIRED:
        sql += " ORDER BY ID"
    elif sort == DESCENDING_REQUIRED:
        sql += " ORDER BY ID DESC"
    rows = db.query(dbo, sql)
    # Now add our extra named fields
    return embellish_regimen(l, rows)

def get_regimens_treatments(dbo, animalid, sort = DESCENDING_REQUIRED):
    """
    Returns a recordset of medical regimens and treatments for an animal:
    TREATMENTNAME, COST, COMMENTS, NAMEDFREQUENCY, NAMEDNUMBEROFTREATMENTS,
    NAMEDSTATUS, DOSAGE, STARTDATE, TREATMENTSGIVEN, TREATMENTSREMAINING,
    TIMINGRULE, TIMINGRULEFREQUENCY, TIMINGRULENOFREQUENCIES, TREATMENTRULE
    TOTALNUMBEROFTREATMENTS, DATEREQUIRED, DATEGIVEN, TREATMENTCOMMENTS,
    TREATMENTNUMBER, TOTALTREATMENTS, GIVENBY, REGIMENID, TREATMENTID
    """
    l = dbo.locale
    sql = "SELECT * FROM v_animalmedicaltreatment " \
        "WHERE AnimalID = %d" % animalid
    if sort == ASCENDING_REQUIRED:
        sql += " ORDER BY DateRequired"
    elif sort == DESCENDING_REQUIRED:
        sql += " ORDER BY DateRequired DESC"
    elif sort == DESCENDING_GIVEN:
        sql += " ORDER BY DateGiven DESC"

    rows = db.query(dbo, sql)
    # Now add our extra named fields
    return embellish_regimen(l, rows)

def get_profile(dbo, pfid):
    """
    Returns a single medical profile by id.
    TREATMENTNAME, COST, COMMENTS, NAMEDFREQUENCY, NAMEDNUMBEROFTREATMENTS, DOSAGE,
    TIMINGRULE, TIMINGRULEFREQUENCY, TIMINGRULENOFREQUENCIES, TREATMENTRULE, TOTALNUMBEROFTREATMENTS
    """
    l = dbo.locale
    sql = "SELECT m.* FROM medicalprofile m WHERE m.ID = %d" % int(pfid)
    rows = db.query(dbo, sql)
    rows = embellish_regimen(l, rows)
    return rows[0]

def get_profiles(dbo, sort = ASCENDING_NAME):
    """
    Returns a recordset of medical profiles:
    TREATMENTNAME, COST, COMMENTS, NAMEDFREQUENCY, NAMEDNUMBEROFTREATMENTS, DOSAGE,
    TIMINGRULE, TIMINGRULEFREQUENCY, TIMINGRULENOFREQUENCIES, TREATMENTRULE, TOTALNUMBEROFTREATMENTS
    """
    l = dbo.locale
    sql = "SELECT m.* FROM medicalprofile m"
    if sort == ASCENDING_NAME:
        sql += " ORDER BY ProfileName"
    elif sort == DESCENDING_NAME:
        sql += " ORDER BY ProfileName DESC"
    rows = db.query(dbo, sql)
    # Now add our extra named fields
    return embellish_regimen(l, rows)

def embellish_regimen(l, rows):
    """
    Adds the following fields to a resultset containing
    regimen rows:
    NAMEDFREQUENCY, NAMEDNUMBEROFTREATMENTS, NAMEDSTATUS, COMPOSITEID
    """
    for r in rows:
        st = 0
        if r.has_key("REGIMENID"): r["COMPOSITEID"] = "%d_%d" % (r["REGIMENID"], r["TREATMENTID"])
        if r.has_key("STATUS"): st = int(r["STATUS"])
        tr = int(r["TIMINGRULE"])
        trr = int(r["TREATMENTRULE"])
        trf = int(r["TIMINGRULEFREQUENCY"])
        trnf = int(r["TIMINGRULENOFREQUENCIES"])
        tnt = int(r["TOTALNUMBEROFTREATMENTS"])
        # NAMEDFREQUENCY - pulls together timing rule
        # information to produce a string, like "One Off"
        # or "1 treatment every 5 weeks"
        tp = _("days", l)
        if tr == ONEOFF:
            r["NAMEDFREQUENCY"] = _("One Off", l)
        else:
            if trf == DAILY:
                r["NAMEDFREQUENCY"] = str(_("{0} treatments every {1} days", l)).format(tr, trnf)
                tp = _("days", l)
            elif trf == WEEKLY:
                r["NAMEDFREQUENCY"] = str(_("{0} treatments every {1} weeks", l)).format(tr, trnf)
                tp = _("weeks", l)
            elif trf == MONTHLY:
                r["NAMEDFREQUENCY"] = str(_("{0} treatments every {1} months", l)).format(tr, trnf)
                tp = _("months", l)
            elif trf == YEARLY:
                r["NAMEDFREQUENCY"] = str(_("{0} treatments every {1} years", l)).format(tr, trnf)
                tp = _("years", l)
        # NAMEDNUMBEROFTREATMENTS - pulls together the treatment
        # rule information to return a string like "Unspecified" or
        # "21 treatment periods (52 treatments)" or "1 treatment" for one-offs
        if tr == ONEOFF:
            r["NAMEDNUMBEROFTREATMENTS"] = _("1 treatment", l)
        elif trr == UNSPECIFIED_LENGTH:
            r["NAMEDNUMBEROFTREATMENTS"] = _("Unspecified", l)
        else:
            r["NAMEDNUMBEROFTREATMENTS"] = str(_("{0} {1} ({2} treatments)", l)).format(tnt, tp, tr * tnt)
        # NAMEDSTATUS
        if st == ACTIVE:
            r["NAMEDSTATUS"] = _("Active", l)
        elif st == COMPLETED:
            r["NAMEDSTATUS"] = _("Completed", l)
        elif st == HELD:
            r["NAMEDSTATUS"] = _("Held", l)
    return rows

def get_tests(dbo, animalid, onlygiven = False, sort = ASCENDING_REQUIRED):
    """
    Returns a recordset of tests for an animal:
    TESTNAME, RESULTNAME, DATEREQUIRED, DATEOFTEST, COMMENTS, COST
    """
    dg = ""
    if onlygiven:
        dg = "DateOfTest Is Not Null AND "
    sql = "SELECT * FROM v_animaltest " \
        "WHERE %sAnimalID = %d" % (dg, animalid)
    if sort == ASCENDING_REQUIRED:
        sql += " ORDER BY DateRequired"
    elif sort == DESCENDING_REQUIRED:
        sql += " ORDER BY DateRequired DESC"
    return db.query(dbo, sql)

def get_vaccinations_outstanding(dbo, offset = "m31", locationfilter = ""):
    """
    Returns a recordset of animals awaiting vaccinations:
    offset is m to go backwards, or p to go forwards with a number of days.
    locationfilter is a comma separated list of internal locations to include animals in
    ID, ANIMALID, SHELTERCODE, ANIMALNAME, LOCATIONNAME, WEBSITEMEDIANAME, DATEREQUIRED, DATEOFVACCINATION, COMMENTS, VACCINATIONTYPE, VACCINATIONID
    """
    ec = ""
    offsetdays = utils.cint(offset[1:])
    if offset.startswith("m"):
        ec = " AND DateRequired >= %s AND DateRequired <= %s" % (db.dd( subtract_days(now(dbo.timezone), offsetdays)), db.dd(now(dbo.timezone)))
    if offset.startswith("p"):
        ec = " AND DateRequired >= %s AND DateRequired <= %s" % (db.dd(now(dbo.timezone)), db.dd( add_days(now(dbo.timezone), offsetdays)))
    if locationfilter != "":
        locationfilter = " AND ShelterLocation IN (%s)" % locationfilter
    return db.query(dbo, "SELECT * FROM v_animalvaccination " \
        "WHERE DateRequired Is Not Null AND DateOfVaccination Is Null " \
        "AND DeceasedDate Is Null AND (Archived = 0 OR ActiveMovementType = 2) %s %s " \
        "ORDER BY DateRequired, AnimalName" % (ec, locationfilter))

def get_tests_outstanding(dbo, offset = "m31", locationfilter = ""):
    """
    Returns a recordset of animals awaiting tests:
    offset is m to go backwards, or p to go forwards with a number of days.
    ID, ANIMALID, SHELTERCODE, ANIMALNAME, LOCATIONNAME, WEBSITEMEDIANAME, DATEREQUIRED, DATEOFTEST, COMMENTS, TESTNAME, RESULTNAME, TESTTYPEID
    """
    ec = ""
    offsetdays = utils.cint(offset[1:])
    if offset.startswith("m"):
        ec = " AND DateRequired >= %s AND DateRequired <= %s" % (db.dd( subtract_days(now(dbo.timezone), offsetdays)), db.dd(now(dbo.timezone)))
    if offset.startswith("p"):
        ec = " AND DateRequired >= %s AND DateRequired <= %s" % (db.dd(now(dbo.timezone)), db.dd( add_days(now(dbo.timezone), offsetdays)))
    if locationfilter != "":
        locationfilter = " AND ShelterLocation IN (%s)" % locationfilter
    return db.query(dbo, "SELECT * FROM v_animaltest " \
        "WHERE DateRequired Is Not Null AND DateOfTest Is Null " \
        "AND DeceasedDate Is Null AND (Archived = 0 OR ActiveMovementType = 2) %s %s " \
        "ORDER BY DateRequired, AnimalName" % (ec, locationfilter))

def get_treatments_outstanding(dbo, offset = "m31", locationfilter = ""):
    """
    Returns a recordset of shelter animals awaiting medical treatments:
    offset is m to go backwards, or p to go forwards with a number of days.
    ANIMALID, SHELTERCODE, ANIMALNAME, LOCATIONNAME, WEBSITEMEDIANAME,
    TREATMENTNAME, COST, COMMENTS, NAMEDFREQUENCY, NAMEDNUMBEROFTREATMENTS,
    NAMEDSTATUS, DOSAGE, STARTDATE, TREATMENTSGIVEN, TREATMENTSREMAINING,
    TIMINGRULE, TIMINGRULEFREQUENCY, TIMINGRULENOFREQUENCIES, TREATMENTRULE
    TOTALNUMBEROFTREATMENTS, DATEREQUIRED, DATEGIVEN, TREATMENTCOMMENTS,
    TREATMENTNUMBER, TOTALTREATMENTS, GIVENBY, REGIMENID, TREATMENTID
    """
    ec = ""
    offsetdays = utils.cint(offset[1:])
    if offset.startswith("m"):
        ec = " AND DateRequired >= %s AND DateRequired <= %s" % (db.dd( subtract_days(now(dbo.timezone), offsetdays)), db.dd(now(dbo.timezone)))
    if offset.startswith("p"):
        ec = " AND DateRequired >= %s AND DateRequired <= %s" % (db.dd(now(dbo.timezone)), db.dd( add_days(now(dbo.timezone), offsetdays)))
    if locationfilter != "":
        locationfilter = " AND ShelterLocation IN (%s)" % locationfilter
    return embellish_regimen(dbo.locale, db.query(dbo, "SELECT * FROM v_animalmedicaltreatment " \
        "WHERE DateRequired Is Not Null AND DateGiven Is Null " \
        "AND Status = 0 " \
        "AND DeceasedDate Is Null AND (Archived = 0 OR ActiveMovementType = 2) %s %s " \
        "ORDER BY DateRequired, AnimalName" % (ec, locationfilter)))

def update_test_today(dbo, username, testid, resultid):
    """
    Marks a test record as performed today. 
    """
    db.execute(dbo, db.make_update_user_sql(dbo, "animaltest", username, "ID = %d" % testid, (
        ( "DateOfTest", db.dd(now(dbo.timezone)) ), 
        ( "TestResultID", db.di(resultid) )
        )))

def update_vaccination_today(dbo, username, vaccid):
    """
    Marks a vaccination record as given today. 
    """
    db.execute(dbo, db.make_update_user_sql(dbo, "animalvaccination", username, "ID = %d" % vaccid, (
        ( "DateOfVaccination", db.dd(now(dbo.timezone)) ), 
        None )
        ))

def calculate_given_remaining(dbo, amid):
    """
    Calculates the number of treatments given and remaining
    """
    given = db.query_int(dbo, "SELECT COUNT(*) FROM animalmedicaltreatment " +
        "WHERE AnimalMedicalID = %d AND DateGiven Is Not Null" % amid)
    db.execute(dbo, "UPDATE animalmedical SET " \
        "TreatmentsGiven = %d, TreatmentsRemaining = " \
        "((TotalNumberOfTreatments * TimingRule) - %d) WHERE ID = %d" % (given, given, amid))

def complete_vaccination(dbo, username, vaccinationid):
    """
    Marks a vaccination completed today
    """
    db.execute(dbo, "UPDATE animalvaccination SET DateOfVaccination = %s WHERE ID = %d" % ( db.dd(now(dbo.timezone)), int(vaccinationid)))
    audit.edit(dbo, username, "animalvaccination", str(vaccinationid) + " => given")

def reschedule_vaccination(dbo, username, vaccinationid, newdays):
    """
    Marks a vaccination completed today (if it's not already completed) 
    and reschedules it for given + newdays onwards.
    """
    av = db.query(dbo, "SELECT * FROM animalvaccination WHERE ID = %d" % int(vaccinationid))[0]
    given = av["DATEOFVACCINATION"]
    if given is None:
        given = now(dbo.timezone)
        db.execute(dbo, "UPDATE animalvaccination SET DateOfVaccination = %s WHERE ID = %d" % ( db.dd(now(dbo.timezone)), int(vaccinationid)))
        audit.edit(dbo, username, "animalvaccination", str(vaccinationid) + " => given")

    nvaccid = db.get_id(dbo, "animalvaccination")
    db.execute(dbo, db.make_insert_user_sql(dbo, "animalvaccination", username, (
        ( "ID", db.di(nvaccid)),
        ( "AnimalID", db.di(av["ANIMALID"])),
        ( "VaccinationID", db.di(av["VACCINATIONID"])),
        ( "DateOfVaccination", db.dd(None)),
        ( "DateRequired", db.dd(add_days(given, int(newdays)))),
        ( "Cost", db.di(av["COST"])),
        ( "Comments", db.ds(av["COMMENTS"])))))

    audit.create(dbo, username, "animalvaccination", str(nvaccid))

def update_medical_treatments(dbo, username, amid):
    """
    Called on creation of an animalmedical record and after the saving
    of a treatment record. This handles creating the next treatment
    in the sequence.

    1. Check if the record is still active, but has all treatments
       given, mark it complete if true
    2. Ignore completed records
    3. If the record has no treatments, generate one from the master
    4. If the record has no outstanding treatment records, generate
       one from the last administered record
    5. If we generated a record, increment the tally of given and
       reduce the tally of remaining. If TreatmentRule is unspecified,
       ignore this step
    """
    am = db.query(dbo, "SELECT * FROM animalmedical WHERE ID = %d" % amid)
    if len(am) == 0: return
    am = am[0]
    amt = db.query(dbo, "SELECT * FROM animalmedicaltreatment " +
        "WHERE AnimalMedicalID = %d ORDER BY DateRequired DESC" % amid)

    # Drop out if it's inactive
    if am["STATUS"] != ACTIVE:
        return

    # If it's a one-off treatment and we've given it, mark complete
    if am["TIMINGRULE"] == ONEOFF:
        if len(amt) > 0:
            if amt[0]["DATEGIVEN"] != None:
                db.execute(dbo, "UPDATE animalmedical SET Status = %d WHERE ID = %d" % ( COMPLETED, amid ))
                return

    # If it's a fixed length treatment, check to see if it's 
    # complete
    if am["TREATMENTRULE"] == FIXED_LENGTH:
        
        # Do we have any outstanding treatments? 
        # Drop out if we do
        ost = db.query_int(dbo, "SELECT COUNT(ID) FROM animalmedicaltreatment " \
            "WHERE AnimalMedicalID = %d AND DateGiven Is Null" % amid)
        if ost > 0:
            return

        # Does the number of treatments given match the total? 
        # Mark the record complete if so and we're done
        if am["TIMINGRULE"] == ONEOFF:
            if am["TREATMENTSGIVEN"] == 1:
                db.execute(dbo, "UPDATE animalmedical SET Status = %d WHERE ID = %d" % ( COMPLETED, amid ))
                return
        else:
            if am["TREATMENTSGIVEN"] >= (am["TOTALNUMBEROFTREATMENTS"] * am["TIMINGRULE"]):
                db.execute(dbo, "UPDATE animalmedical SET Status = %d WHERE ID = %d" % ( COMPLETED, amid ))
                return

    # If there aren't any treatment records at all, create
    # one now
    if len(amt) == 0:
        insert_treatments(dbo, username, amid, am["STARTDATE"], True)
    else:
        # We've got some treatments, use the latest given
        # date (desc order). If it doesn't have a given date then there's
        # still an outstanding treatment and we can bail
        if amt[0]["DATEGIVEN"] is None:
            return

        insert_treatments(dbo, username, amid, amt[0]["DATEGIVEN"], False)

def insert_treatments(dbo, username, amid, requireddate, isstart = True):
    """
    Creates new treatment records for the given medical record
    with the required date given. isstart says that the date passed
    is the real start date, so don't look at the timing rule to 
    calculate the next date.
    """
    am = db.query(dbo, "SELECT * FROM animalmedical WHERE ID = %d" % amid)[0]
    nofreq = int(am["TIMINGRULENOFREQUENCIES"])
    if not isstart:
        if am["TIMINGRULEFREQUENCY"] == DAILY:
            requireddate += datetime.timedelta(days=nofreq)
        if am["TIMINGRULEFREQUENCY"] == WEEKLY:
            requireddate += datetime.timedelta(days=nofreq*7)
        if am["TIMINGRULEFREQUENCY"] == MONTHLY:
            requireddate += datetime.timedelta(days=nofreq*31)
        if am["TIMINGRULEFREQUENCY"] == YEARLY:
            requireddate += datetime.timedelta(days=nofreq*365)

    # Create correct number of records
    norecs = am["TIMINGRULE"]
    if norecs == 0: norecs = 1

    for x in range(1, norecs+1):
        sql = db.make_insert_user_sql(dbo, "animalmedicaltreatment", username, (
            ( "ID", db.di(db.get_id(dbo, "animalmedicaltreatment"))),
            ( "AnimalID", db.di(am["ANIMALID"]) ),
            ( "AnimalMedicalID", db.di(amid)),
            ( "DateRequired", db.dd(requireddate)),
            ( "DateGiven", db.dd(None)),
            ( "GivenBy", db.ds("")),
            ( "TreatmentNumber", db.di(x)),
            ( "TotalTreatments", db.di(norecs)),
            ( "Comments", db.ds(""))
        ))
        db.execute(dbo, sql)

    # Update the number of treatments given and remaining
    calculate_given_remaining(dbo, amid)

def insert_regimen_from_form(dbo, username, data):
    """
    Creates a regimen record from posted form data
    """
    l = dbo.locale
    if utils.df_kd(data, "startdate", l) is None:
        raise utils.ASMValidationError(_("Start date must be a valid date", l))
    if utils.df_ks(data, "treatmentname") == "":
        raise utils.ASMValidationError(_("Treatment name cannot be blank", l))

    l = dbo.locale
    nregid = db.get_id(dbo, "animalmedical")
    timingrule = utils.df_ki(data, "timingrule")
    timingrulenofrequencies = utils.df_ki(data, "timingrulenofrequencies")
    timingrulefrequency = utils.df_ki(data, "timingrulefrequency")
    totalnumberoftreatments = utils.df_ki(data, "totalnumberoftreatments")
    treatmentsremaining = int(totalnumberoftreatments) * int(timingrule)
    treatmentrule = utils.df_ki(data, "treatmentrule")
    singlemulti = utils.df_ki(data, "singlemulti")
    if singlemulti == 0:
        timingrule = 0
        timingrulenofrequencies = 0
        timingrulefrequency = 0
        treatmentsremaining = 1
    if treatmentrule != 0:
        totalnumberoftreatments = 0
        treatmentsremaining = 0

    sql = db.make_insert_user_sql(dbo, "animalmedical", username, ( 
        ( "ID", db.di(nregid)),
        ( "AnimalID", db.di(utils.df_ki(data, "animal"))),
        ( "MedicalProfileID", utils.df_s(data, "profileid")),
        ( "TreatmentName", utils.df_t(data, "treatmentname")),
        ( "Dosage", utils.df_t(data, "dosage")),
        ( "StartDate", utils.df_d(data, "startdate", l)),
        ( "Status", db.di(0)),
        ( "Cost", utils.df_m(data, "cost", l)),
        ( "TimingRule", db.di(timingrule)),
        ( "TimingRuleFrequency", db.di(timingrulefrequency)),
        ( "TimingRuleNoFrequencies", db.di(timingrulenofrequencies)),
        ( "TreatmentRule", utils.df_s(data, "treatmentrule")),
        ( "TotalNumberOfTreatments", db.di(totalnumberoftreatments)),
        ( "TreatmentsGiven", db.di(0)),
        ( "TreatmentsRemaining", db.di(treatmentsremaining)),
        ( "Comments", utils.df_t(data, "comments"))
        ))
    db.execute(dbo, sql)
    audit.create(dbo, username, "animalmedical", str(nregid) + ": " + utils.df_ks(data, "treatmentname") + " " + utils.df_ks(data, "dosage"))
    update_medical_treatments(dbo, username, nregid)

def update_regimen_from_form(dbo, username, data):
    """
    Updates a regimen record from posted form data
    """
    l = dbo.locale
    regimenid = utils.df_ki(data, "regimenid")
    if utils.df_ks(data, "treatmentname") == "":
        raise utils.ASMValidationError(_("Treatment name cannot be blank", l))

    sql = db.make_update_user_sql(dbo, "animalmedical", username, "ID=%d" % regimenid, ( 
        ( "TreatmentName", utils.df_t(data, "treatmentname")),
        ( "Dosage", utils.df_t(data, "dosage")),
        ( "Status", utils.df_s(data, "status")),
        ( "Cost", utils.df_m(data, "cost", l)),
        ( "Comments", utils.df_t(data, "comments"))
        ))
    preaudit = db.query(dbo, "SELECT * FROM animalmedical WHERE ID=%d" % regimenid)
    db.execute(dbo, sql)
    postaudit = db.query(dbo, "SELECT * FROM animalmedical WHERE ID=%d" % regimenid)
    audit.edit(dbo, username, "animalmedical", audit.map_diff(preaudit, postaudit, [ "TREATMENTNAME", "DOSAGE" ]))
    update_medical_treatments(dbo, username, utils.df_ki(data, "regimenid"))

def insert_vaccination_from_form(dbo, username, data):
    """
    Creates a vaccination record from posted form data
    """
    l = dbo.locale
    if utils.df_kd(data, "required", l) is None:
        raise utils.ASMValidationError(_("Required date must be a valid date", l))

    nvaccid = db.get_id(dbo, "animalvaccination")
    sql = db.make_insert_user_sql(dbo, "animalvaccination", username, ( 
        ( "ID", db.di(nvaccid)),
        ( "AnimalID", db.di(utils.df_ki(data, "animal"))),
        ( "VaccinationID", utils.df_s(data, "type")),
        ( "DateOfVaccination", utils.df_d(data, "given", l)),
        ( "DateRequired", utils.df_d(data, "required", l)),
        ( "Cost", utils.df_m(data, "cost", l)),
        ( "Comments", utils.df_t(data, "comments"))
        ))
    db.execute(dbo, sql)
    audit.create(dbo, username, "animalvaccination", str(nvaccid))
    return nvaccid

def update_vaccination_from_form(dbo, username, data):
    """
    Updates a vaccination record from posted form data
    """
    l = dbo.locale
    vaccid = utils.df_ki(data, "vaccid")
    if utils.df_kd(data, "required", l) is None:
        raise utils.ASMValidationError(_("Required date must be a valid date", l))

    sql = db.make_update_user_sql(dbo, "animalvaccination", username, "ID=%d" % vaccid, ( 
        ( "AnimalID", db.di(utils.df_ki(data, "animal"))),
        ( "VaccinationID", utils.df_s(data, "type")),
        ( "DateOfVaccination", utils.df_d(data, "given", l)),
        ( "DateRequired", utils.df_d(data, "required", l)),
        ( "Cost", utils.df_m(data, "cost", l)),
        ( "Comments", utils.df_t(data, "comments"))
        ))
    preaudit = db.query(dbo, "SELECT * FROM animalvaccination WHERE ID = %d" % vaccid)
    db.execute(dbo, sql)
    postaudit = db.query(dbo, "SELECT * FROM animalvaccination WHERE ID = %d" % vaccid)
    audit.edit(dbo, username, "animalvaccination", audit.map_diff(preaudit, postaudit))

def insert_test_from_form(dbo, username, data):
    """
    Creates a test record from posted form data
    """
    l = dbo.locale
    if utils.df_kd(data, "required", l) is None:
        raise utils.ASMValidationError(_("Required date must be a valid date", l))

    ntestid = db.get_id(dbo, "animaltest")
    sql = db.make_insert_user_sql(dbo, "animaltest", username, ( 
        ( "ID", db.di(ntestid)),
        ( "AnimalID", db.di(utils.df_ki(data, "animal"))),
        ( "TestTypeID", utils.df_s(data, "type")),
        ( "TestResultID", utils.df_s(data, "result")),
        ( "DateOfTest", utils.df_d(data, "given", l)),
        ( "DateRequired", utils.df_d(data, "required", l)),
        ( "Cost", utils.df_m(data, "cost", l)),
        ( "Comments", utils.df_t(data, "comments"))
        ))
    db.execute(dbo, sql)
    audit.create(dbo, username, "animaltest", str(ntestid))
    # ASM2_COMPATIBILITY
    update_asm2_tests(dbo, ntestid)
    return ntestid

def update_test_from_form(dbo, username, data):
    """
    Updates a test record from posted form data
    """
    l = dbo.locale
    testid = utils.df_ki(data, "testid")
    if utils.df_kd(data, "required", l) is None:
        raise utils.ASMValidationError(_("Required date must be a valid date", l))

    sql = db.make_update_user_sql(dbo, "animaltest", username, "ID=%d" % testid, ( 
        ( "AnimalID", db.di(utils.df_ki(data, "animal"))),
        ( "TestTypeID", utils.df_s(data, "type")),
        ( "TestResultID", utils.df_s(data, "result")),
        ( "DateOfTest", utils.df_d(data, "given", l)),
        ( "DateRequired", utils.df_d(data, "required", l)),
        ( "Cost", utils.df_m(data, "cost", l)),
        ( "Comments", utils.df_t(data, "comments"))
        ))
    preaudit = db.query(dbo, "SELECT * FROM animaltest WHERE ID = %d" % testid)
    db.execute(dbo, sql)
    postaudit = db.query(dbo, "SELECT * FROM animaltest WHERE ID = %d" % testid)
    audit.edit(dbo, username, "animaltest", audit.map_diff(preaudit, postaudit))
    # ASM2_COMPATIBILITY
    update_asm2_tests(dbo, testid)

def update_asm2_tests(dbo, testid):
    """
    Used for asm2 compatibility, checks the test with testid and if it's
    a FIV, FLV or Heartworm test updates the old ASM2 fields for them.
    """
    # ASM2_COMPATIBILITY
    testid = int(testid)
    t = db.query(dbo, "SELECT AnimalID, TestName, DateOfTest, ResultName FROM animaltest " \
        "INNER JOIN testtype ON testtype.ID = animaltest.TestTypeID " \
        "INNER JOIN testresult ON testresult.ID = animaltest.TestResultID " \
        "WHERE animaltest.ID=%d" % testid)[0]
    # If there's no date, forget it
    if t["DATEOFTEST"] is None: return
    # Get an old style result
    result = 0
    if t["RESULTNAME"].find("egativ") != -1: result = 1
    if t["RESULTNAME"].find("ositiv") != -1: result = 2
    # Update for the correct test if it's one we know about
    if t["TESTNAME"].find("FIV") != -1: 
        db.execute(dbo, "UPDATE animal SET CombiTested = 1, CombiTestDate = %s, CombiTestResult = %d WHERE ID = %d" % \
            (db.dd(t["DATEOFTEST"]), result, t["ANIMALID"]))
    if t["TESTNAME"].find("FLV") != -1: 
        db.execute(dbo, "UPDATE animal SET CombiTested = 1, CombiTestDate = %s, FLVResult = %d WHERE ID = %d" % \
            (db.dd(t["DATEOFTEST"]), result, t["ANIMALID"]))
    if t["TESTNAME"].find("eartworm") != -1: 
        db.execute(dbo, "UPDATE animal SET HeartwormTested = 1, HeartwormTestDate = %s, HeartwormTestResult = %d WHERE ID = %d" % \
            (db.dd(t["DATEOFTEST"]), result, t["ANIMALID"]))

def delete_regimen(dbo, username, amid):
    """
    Deletes a regimen
    """
    audit.delete(dbo, username, "animalmedical", str(db.query(dbo, "SELECT * FROM animalmedical WHERE ID = %d" % int(amid))))
    db.execute(dbo, "DELETE FROM animalmedicaltreatment WHERE AnimalMedicalID = %d" % amid)
    db.execute(dbo, "DELETE FROM animalmedical WHERE ID = %d" % amid)

def delete_treatment(dbo, username, amtid):
    """
    Deletes a treatment record
    """
    audit.delete(dbo, username, "animalmedicaltreatment", str(db.query(dbo, "SELECT * FROM animalmedicaltreatment WHERE ID = %d" % int(amtid))))
    amid = db.query_int(dbo, "SELECT AnimalMedicalID FROM animalmedicaltreatment WHERE ID = %d" % int(amtid))
    db.execute(dbo, "DELETE FROM animalmedicaltreatment WHERE ID = %d" % amtid)
    calculate_given_remaining(dbo, amid)
    update_medical_treatments(dbo, username, amid)

def delete_test(dbo, username, testid):
    """
    Deletes a test record
    """
    audit.delete(dbo, username, "animaltest", str(db.query(dbo, "SELECT * FROM animaltest WHERE ID = %d" % int(testid))))
    db.execute(dbo, "DELETE FROM animaltest WHERE ID = %d" % testid)

def delete_vaccination(dbo, username, vaccinationid):
    """
    Deletes a vaccination record
    """
    audit.delete(dbo, username, "animalvaccination", str(db.query(dbo, "SELECT * FROM animalvaccination WHERE ID = %d" % int(vaccinationid))))
    db.execute(dbo, "DELETE FROM animalvaccination WHERE ID = %d" % vaccinationid)

def insert_profile_from_form(dbo, username, data):
    """
    Creates a profile record from posted form data
    """
    l = dbo.locale
    if utils.df_ks(data, "treatmentname") == "":
        raise utils.ASMValidationError(_("Treatment name cannot be blank", l))
    if utils.df_ks(data, "profilename") == "":
        raise utils.ASMValidationError(_("Profile name cannot be blank", l))

    nprofid = db.get_id(dbo, "medicalprofile")
    timingrule = utils.df_ki(data, "timingrule")
    timingrulenofrequencies = utils.df_ki(data, "timingrulenofrequencies")
    timingrulefrequency = utils.df_ki(data, "timingrulefrequency")
    totalnumberoftreatments = utils.df_ki(data, "totalnumberoftreatments")
    treatmentrule = utils.df_ki(data, "treatmentrule")
    singlemulti = utils.df_ki(data, "singlemulti")
    if singlemulti == 0:
        timingrule = 0
        timingrulenofrequencies = 0
        timingrulefrequency = 0
    if treatmentrule != 0:
        totalnumberoftreatments = 0
    sql = db.make_insert_user_sql(dbo, "medicalprofile", username, ( 
        ( "ID", db.di(nprofid)),
        ( "ProfileName", utils.df_t(data, "profilename")),
        ( "TreatmentName", utils.df_t(data, "treatmentname")),
        ( "Dosage", utils.df_t(data, "dosage")),
        ( "Cost", utils.df_m(data, "cost", l)),
        ( "TimingRule", db.di(timingrule)),
        ( "TimingRuleFrequency", db.di(timingrulefrequency)),
        ( "TimingRuleNoFrequencies", db.di(timingrulenofrequencies)),
        ( "TreatmentRule", utils.df_s(data, "treatmentrule")),
        ( "TotalNumberOfTreatments", db.di(totalnumberoftreatments)),
        ( "Comments", utils.df_t(data, "comments"))
        ))
    db.execute(dbo, sql)
    audit.create(dbo, username, "medicalprofile", str(nprofid) + ": " + utils.df_ks(data, "treatmentname") + " " + utils.df_ks(data, "dosage"))

def update_profile_from_form(dbo, username, data):
    """
    Updates a profile record from posted form data
    """
    l = dbo.locale
    profileid = utils.df_ki(data, "profileid")
    if utils.df_ks(data, "treatmentname") == "":
        raise utils.ASMValidationError(_("Treatment name cannot be blank", l))
    if utils.df_ks(data, "profilename") == "":
        raise utils.ASMValidationError(_("Profile name cannot be blank", l))

    timingrule = utils.df_ki(data, "timingrule")
    timingrulenofrequencies = utils.df_ki(data, "timingrulenofrequencies")
    timingrulefrequency = utils.df_ki(data, "timingrulefrequency")
    totalnumberoftreatments = utils.df_ki(data, "totalnumberoftreatments")
    treatmentrule = utils.df_ki(data, "treatmentrule")
    singlemulti = utils.df_ki(data, "singlemulti")
    if singlemulti == 0:
        timingrule = 0
        timingrulenofrequencies = 0
        timingrulefrequency = 0
    if treatmentrule != 0:
        totalnumberoftreatments = 0
    sql = db.make_update_user_sql(dbo, "medicalprofile", username, "ID=%d" % profileid, ( 
        ( "ProfileName", utils.df_t(data, "profilename")),
        ( "TreatmentName", utils.df_t(data, "treatmentname")),
        ( "Dosage", utils.df_t(data, "dosage")),
        ( "Cost", utils.df_m(data, "cost", l)),
        ( "TimingRule", db.di(timingrule)),
        ( "TimingRuleFrequency", db.di(timingrulefrequency)),
        ( "TimingRuleNoFrequencies", db.di(timingrulenofrequencies)),
        ( "TreatmentRule", utils.df_s(data, "treatmentrule")),
        ( "TotalNumberOfTreatments", db.di(totalnumberoftreatments)),
        ( "Comments", utils.df_t(data, "comments"))
        ))
    preaudit = db.query(dbo, "SELECT * FROM medicalprofile WHERE ID=%d" % profileid)
    db.execute(dbo, sql)
    postaudit = db.query(dbo, "SELECT * FROM medicalprofile WHERE ID=%d" % profileid)
    audit.edit(dbo, username, "medicalprofile", audit.map_diff(preaudit, postaudit, [ "TREATMENTNAME", "DOSAGE" ]))

def delete_profile(dbo, username, pfid):
    """
    Deletes a profile
    """
    audit.delete(dbo, username, "medicalprofile", str(db.query(dbo, "SELECT * FROM medicalprofile WHERE ID = %d" % pfid)))
    db.execute(dbo, "DELETE FROM medicalprofile WHERE ID = %d" % pfid)

def update_treatment_today(dbo, username, amtid):
    """
    Marks a treatment record as given today. 
    """
    amid = db.query_int(dbo, "SELECT AnimalMedicalID FROM animalmedicaltreatment WHERE ID = %d" % amtid)
    db.execute(dbo, db.make_update_user_sql(dbo, "animalmedicaltreatment", username, "ID = %d" % amtid, (
        ( "DateGiven", db.dd(now(dbo.timezone)) ), 
        ( "GivenBy", db.ds(username))
        )))
    audit.edit(dbo, username, "animalmedicaltreatment", "%d => given" % amtid)

    # Update number of treatments given and remaining
    calculate_given_remaining(dbo, amid)

    # Generate next treatments in sequence or complete the
    # medical record appropriately
    update_medical_treatments(dbo, username, amid)

def update_treatment_given(dbo, username, amtid, newdate):
    """
    Marks a treatment record as given on newdate, assuming
    that newdate is valid.
    """
    amid = db.query_int(dbo, "SELECT AnimalMedicalID FROM animalmedicaltreatment WHERE ID = %d" % amtid)
    db.execute(dbo, db.make_update_user_sql(dbo, "animalmedicaltreatment", username, "ID = %d" % amtid, (
        ( "DateGiven", db.dd(newdate) ), 
        ( "GivenBy", db.ds(username))
        )))
    audit.edit(dbo, username, "animalmedicaltreatment", "%d given => %s" % (amtid, str(newdate)))

    # Update number of treatments given and remaining
    calculate_given_remaining(dbo, amid)

    # Generate next treatments in sequence or complete the
    # medical record appropriately
    update_medical_treatments(dbo, username, amid)

def update_treatment_required(dbo, username, amtid, newdate):
    """
    Marks a treatment record as required on newdate, assuming
    that newdate is valid.
    """
    db.execute(dbo, "UPDATE animalmedicaltreatment SET DateRequired = %s WHERE ID = %d" % (db.dd(newdate), amtid))
    audit.edit(dbo, username, "animalmedicaltreatment", "%d required => %s" % (amtid, str(newdate)))


def update_vaccination_required(dbo, username, vaccid, newdate):
    """
    Gives a vaccination record a required date of newdate, assuming
    that newdate is valid.
    """
    db.execute(dbo, db.make_update_user_sql(dbo, "animalvaccination", username, "ID = %d" % vaccid, (
        ( "DateRequired", db.dd(newdate) ), 
        )))
    audit.edit(dbo, username, "animalvaccination", "%d required => %s" % (vaccid, str(newdate)))


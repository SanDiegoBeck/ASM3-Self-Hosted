#!/usr/bin/python

import al
import animal
import audit
import configuration
import db
import financial
import i18n
import utils

NO_MOVEMENT = 0
ADOPTION = 1
FOSTER = 2
TRANSFER = 3
ESCAPED = 4
RECLAIMED = 5
STOLEN = 6
RELEASED = 7
RETAILER = 8
RESERVATION = 9
CANCELLED_RESERVATION = 10
TRIAL_ADOPTION = 11

def get_movements(dbo, movementtype):
    """
    Gets the list of movements of a particular type 
    (unreturned or returned after today and for animals who aren't deceased)
    """
    return db.query(dbo, "SELECT * FROM v_adoption " \
        "WHERE MovementType = %d AND " \
        "(ReturnDate Is Null OR ReturnDate > %s) " \
        "AND DeceasedDate Is Null " \
        "ORDER BY MovementDate DESC" % (int(movementtype), db.dd(i18n.now(dbo.timezone))))

def get_active_reservations(dbo, age = 0):
    """
    Gets the list of uncancelled reservation movements.
    age: The age of the reservation in days, or 0 for all
    """
    where = ""
    if age > 0:
        where = "AND ReservationDate <= %s" % db.dd(i18n.subtract_days(i18n.now(dbo.timezone), age))
    return db.query(dbo, "SELECT * FROM v_adoption " \
        "WHERE ReservationDate Is Not Null AND MovementDate Is Null AND MovementType = 0 AND ReturnDate Is Null " \
        "AND ReservationCancelledDate Is Null %s ORDER BY ReservationDate" % where)

def get_recent_adoptions(dbo, months = 1):
    """
    Returns a list of adoptions in the last "months" months.
    """
    return db.query(dbo, "SELECT * FROM v_adoption " \
        "WHERE MovementType = 1 AND MovementDate Is Not Null AND ReturnDate Is Null " \
        "AND MovementDate > %s " \
        "ORDER BY MovementDate DESC" % db.dd(i18n.subtract_days(i18n.now(dbo.timezone), months * 31)))

def get_recent_nonfosteradoption(dbo, months = 1):
    """
    Returns a list of active movements that aren't reserves,
    fosters, adoptions or transfers in the last "months" months.
    """
    return db.query(dbo, "SELECT * FROM v_adoption " \
        "WHERE MovementType > 3 AND MovementDate Is Not Null AND ReturnDate Is Null " \
        "AND MovementDate > %s " \
        "ORDER BY MovementDate DESC" % db.dd(i18n.subtract_days(i18n.now(dbo.timezone), months * 31)))

def get_recent_transfers(dbo, months = 1):
    """
    Returns a list of transfers in the last "months" months.
    """
    return db.query(dbo, "SELECT * FROM v_adoption " \
        "WHERE MovementType = 3 AND MovementDate Is Not Null AND ReturnDate Is Null " \
        "AND MovementDate > %s " \
        "ORDER BY MovementDate DESC" % db.dd(i18n.subtract_days(i18n.now(dbo.timezone), months * 31)))

def get_recent_unneutered_adoptions(dbo, months = 1):
    """
    Returns a list of adoptions in the last "months" months where the
    animal remains unneutered.
    """
    return db.query(dbo, "SELECT * FROM v_adoption " \
        "WHERE MovementType = 1 AND MovementDate Is Not Null AND ReturnDate Is Null " \
        "AND MovementDate > %s AND Neutered = 0 " \
        "ORDER BY MovementDate DESC" % db.dd(i18n.subtract_days(i18n.now(dbo.timezone), months * 31)))

def get_trial_adoptions(dbo, mode = "ALL"):
    """
    Returns a list of trial adoption movements. 
    If mode is EXPIRING, shows trials that end today or before.
    If mode is ACTIVE, shows trials that end after today.
    If mode is ALL, returns all trials.
    """
    where = ""
    if mode == "ALL":
        where = ""
    elif mode == "EXPIRING":
        where = "AND TrialEndDate <= %s " % db.dd(i18n.now(dbo.timezone))
    elif mode == "ACTIVE":
        where = "AND TrialEndDate > %s " % db.dd(i18n.now(dbo.timezone))
    return db.query(dbo, "SELECT * FROM v_adoption " \
        "WHERE IsTrial = 1 AND MovementType = 1 AND (ReturnDate Is Null OR ReturnDate > %s) %s" \
        "ORDER BY TrialEndDate" % (db.dd(i18n.now(dbo.timezone)), where))

def get_animal_movements(dbo, aid):
    """
    Gets the list of movements for a particular animal
    """
    return db.query(dbo, "SELECT * FROM v_adoption " \
        "WHERE AnimalID = %d ORDER BY MovementDate DESC" % int(aid))

def get_person_movements(dbo, pid):
    """
    Gets the list of movements for a particular person
    """
    return db.query(dbo, "SELECT * FROM v_adoption " \
        "WHERE OwnerID = %d ORDER BY MovementDate DESC" % int(pid))

def validate_movement_form_data(dbo, data):
    """
    Verifies that form data is valid for a movement
    """
    l = dbo.locale
    movementid = utils.df_ki(data, "movementid")
    movement = None
    if movementid != 0: movement = db.query(dbo, "SELECT * FROM adoption WHERE ID = %d" % movementid)[0]
    adoptionno = utils.df_ks(data, "adoptionno")
    movementtype = utils.df_ki(data, "type")
    movementdate = utils.df_kd(data, "movementdate", l)
    returndate = utils.df_kd(data, "returndate", l)
    reservationdate = utils.df_kd(data, "reservationdate", l)
    reservationcancelled = utils.df_kd(data, "reservationcancelled", l)
    personid = utils.df_ki(data, "person")
    animalid = utils.df_ki(data, "animal")
    retailerid = utils.df_ki(data, "retailer")
    al.debug("validating saved movement %d for animal %d" % (movementid, animalid), "movement.validate_movement_form_data", dbo)
    # If we have a date but no type, get rid of it
    if movementdate is None and movementtype == 0:
        data["movementdate"] = ""
        al.debug("blank date and type", "movement.validate_movement_form_data", dbo)
    # If we've got a type, but no date, default today
    if movementtype > 0 and movementdate is None:
        movementdate = i18n.now()
        data["movementdate"] = i18n.python2display(l, movementdate)
        al.debug("type set and no date, defaulting today", "movement.validate_movement_form_data", dbo)
    # If we've got a reserve cancellation without a reserve, remove it
    if reservationdate is None and reservationcancelled is not None:
        data["reservationdate"] = ""
        al.debug("movement has no reserve or cancelled date", "movement.validate_movement_form_data", dbo)
    # Animals are always required
    if animalid == 0:
        al.debug("movement has no animal", "movement.validate_movement_form_data", dbo)
        raise utils.ASMValidationError(i18n._("Movements require an animal", l))
    # Owners are required unless type is escaped, stolen or released
    if personid == 0 and movementtype != ESCAPED and movementtype != STOLEN and movementtype != RELEASED:
        al.debug("movement has no person and is not ESCAPED|STOLEN|RELEASED", "movement.validate_movement_form_data", dbo)
        raise utils.ASMValidationError(i18n._("A person is required for this movement type.", l))
    # Is the movement number unique?
    if 0 != db.query_int(dbo, "SELECT COUNT(*) FROM adoption WHERE AdoptionNumber LIKE '%s' AND ID <> %d" % (adoptionno, movementid)):
        raise utils.ASMValidationError(i18n._("Movement numbers must be unique.", l))
    # If we're updating an existing record, we only need to continue validation
    # if one of the important fields has changed (movement date/type, return date, reservation, animal)
    if movement is not None:
        if movementtype == movement["MOVEMENTTYPE"] and movementdate == movement["MOVEMENTDATE"] and returndate == movement["RETURNDATE"] and reservationdate == movement["RESERVATIONDATE"] and animalid == movement["ANIMALID"]:
            al.debug("movement type, dates and animalid have not changed. Abandoning further validation", "movement.validate_movement_form_data", dbo)
            return
    # If the animal is held in case of reclaim, it can't be adopted
    if movementtype == ADOPTION:
        if 1 == db.query_int(dbo, "SELECT IsHold FROM animal WHERE ID = %d" % animalid):
            al.debug("movement is adoption and the animal is on hold", "movement.validate_movement_form_data", dbo)
            raise utils.ASMValidationError(i18n._("This animal is currently held and cannot be adopted.", l))
    # If it's a foster movement, make sure the owner is a fosterer
    if movementtype == FOSTER:
        if 0 == db.query_int(dbo, "SELECT IsFosterer FROM owner WHERE ID = %d" % personid):
            al.debug("movement is a foster and the person is not a fosterer.", "movement.validate_movement_form_data", dbo)
            raise utils.ASMValidationError(i18n._("This person is not flagged as a fosterer and cannot foster animals.", l))
    # If it's a retailer movement, make sure the owner is a retailer
    if movementtype == RETAILER:
        if 0 == db.query_int(dbo, "SELECT IsRetailer FROM owner WHERE ID = %d" % personid):
            al.debug("movement is a retailer and the person is not a retailer.", "movement.validate_movement_form_data", dbo)
            raise utils.ASMValidationError(i18n._("This person is not flagged as a retailer and cannot handle retailer movements.", l))
    # If a retailer is selected, make sure it's an adoption
    if retailerid != 0 and movementtype != ADOPTION:
        al.debug("movement has a retailerid set and this is not an adoption.", "movement.validate_movement_form_data", dbo)
        raise utils.ASMValidationError(i18n._("From retailer is only valid on adoption movements.", l))
    # If a retailer is selected, make sure there's been a retailer movement in this animal's history
    if retailerid != 0:
        if 0 == db.query_int(dbo, "SELECT COUNT(*) FROM adoption WHERE AnimalID = %d AND MovementType = %d" % ( animalid, RETAILER )):
            al.debug("movement has a retailerid set but has never been to a retailer.", "movement.validate_movement_form_data", dbo)
            raise utils.ASMValidationError(i18n._("This movement cannot be from a retailer when the animal has no prior retailer movements.", l))
    # You can't have a return without a movement
    if movementdate is None and returndate is not None:
        al.debug("movement is returned without a movement date.", "movement.validate_movement_form_data", dbo)
        raise utils.ASMValidationError(i18n._("You can't have a return without a movement.", l))
    # Return should be after or same day as movement
    if movementdate is not None and returndate != None and movementdate > returndate:
        al.debug("movement return date is before the movement date.", "movement.validate_movement_form_data", dbo)
        raise utils.ASMValidationError(i18n._("Return date cannot be before the movement date.", l))
    # Can't have multiple open movements
    if movementdate is not None:
        existingopen = db.query_int(dbo, "SELECT COUNT(*) FROM adoption WHERE MovementDate Is Not Null AND " \
            "ReturnDate Is Null AND AnimalID = %d AND ID <> %d" % (animalid, movementid))
        if existingopen > 0:
            al.debug("movement is open and animal already has another open movement.", "movement.validate_movement_form_data", dbo)
            raise utils.ASMValidationError(i18n._("An animal cannot have multiple open movements.", l))
    # If we have a movement and return, is there another movement with a 
    # movementdate between the movement and return date on this one?
    if movementdate is not None and returndate != None:
        clash = db.query_int(dbo, "SELECT COUNT(*) FROM adoption WHERE " \
        "AnimalID = %d AND ID <> %d AND ((ReturnDate > %s AND ReturnDate < %s) " \
        "OR (MovementDate < %s AND MovementDate > %s))" % ( animalid, movementid, 
        db.dd(movementdate), db.dd(returndate), db.dd(returndate), db.dd(movementdate) ))
        if clash > 0:
            al.debug("movement dates overlap an existing movement.", "movement.validate_movement_form_data", dbo)
            raise utils.ASMValidationError(i18n._("Movement dates clash with an existing movement.", l))
    # Does this movement date fall within the date range of an already
    # returned movement for the same animal?
    if movementdate is not None and returndate is None:
        clash = db.query_int(dbo, "SELECT COUNT(*) FROM adoption WHERE AnimalID = %d AND ID <> %d AND " \
        "MovementDate Is Not Null AND ReturnDate Is Not Null AND " \
        "%s > MovementDate AND %s < ReturnDate" % ( animalid, movementid, db.dd(movementdate), db.dd(movementdate)))
        if clash > 0:
            al.debug("movement dates overlap an existing movement.", "movement.validate_movement_form_data", dbo)
            raise utils.ASMValidationError(i18n._("Movement dates clash with an existing movement.", l))
    # If there's a cancelled reservation, make sure it's after the reserve date
    if reservationdate is not None and reservationcancelled != None and reservationcancelled < reservationdate:
        al.debug("reserve date is after cancelled date.", "movement.validate_movement_form_data", dbo)
        raise utils.ASMValidationError(i18n._("Reservation date cannot be after cancellation date.", l))
    # If this is a new reservation, make sure there's no open movement (fosters do not count)
    if movementid == 0 and movementtype == 0 and movementdate is None and reservationdate is not None:
        om = db.query_int(dbo, "SELECT COUNT(*) FROM adoption WHERE AnimalID = %d AND " \
            "MovementDate Is Not Null AND ReturnDate Is Null AND MovementType <> 2" % animalid)
        if om > 0:
            al.debug("movement is a reservation but animal has active movement.", "movement.validate_movement_form_data", dbo)
            raise utils.ASMValidationError(i18n._("Can't reserve an animal that has an active movement.", l))
    # Make sure the adoption number is unique
    an = db.query_int(dbo, "SELECT COUNT(*) FROM adoption WHERE ID <> %d AND " \
        "AdoptionNumber LIKE %s" % ( movementid, utils.df_t(data, "adoptionno" )))
    if an > 0:
        al.debug("movement number is not unique.", "movement.validate_movement_form_data", dbo)
        raise utils.ASMValidationError(i18n._("The movement number '{0}' is not unique.", l).format(utils.df_ks(data, "adoptionno")))
    # If this is an adoption and the owner had some criteria, expire them
    if movementtype == ADOPTION and personid > 0:
        al.debug("movement is an adoption, expiring person criteria.", "movement.validate_movement_form_data", dbo)
        sql = "UPDATE owner SET MatchActive = 0, MatchExpires = %s WHERE ID = %d" % ( db.dd(i18n.now(dbo.timezone)), int(personid) )
        db.execute(dbo, sql)
    # If the option to cancel reserves on adoption is set, cancel any outstanding reserves for the animal
    if movementtype == ADOPTION and configuration.cancel_reserves_on_adoption(dbo):
        al.debug("movement is an adoption, cancelling outstanding reserves.", "movement.validate_movement_form_data", dbo)
        sql = "UPDATE adoption SET ReservationCancelledDate = %s " \
            "WHERE ReservationCancelledDate Is Null AND MovementDate Is Null " \
            "AND AnimalID = %d AND ID <> %d" % ( db.dd(i18n.now(dbo.timezone)), animalid, int(movementid) )
        db.execute(dbo, sql)

def insert_movement_from_form(dbo, username, data):
    """
    Creates a movement record from posted form data 
    """
    movementid = db.get_id(dbo, "adoption")
    adoptionno = utils.df_ks(data, "adoptionno")
    animalid = utils.df_ki(data, "animal")
    if adoptionno == "": 
        # No adoption number was supplied, generate a
        # unique number from the movementid
        idx = movementid
        while True:
            adoptionno = utils.padleft(idx, 6)
            data["adoptionno"] = adoptionno
            if 0 == db.query_int(dbo, "SELECT COUNT(*) FROM adoption WHERE AdoptionNumber LIKE '%s'" % adoptionno):
                break
            else:
                idx += 1

    validate_movement_form_data(dbo, data)
    l = dbo.locale
    sql = db.make_insert_user_sql(dbo, "adoption", username, ( 
        ( "ID", db.di(movementid)),
        ( "AdoptionNumber", db.ds(adoptionno)),
        ( "OwnerID", db.di(utils.df_ki(data, "person"))),
        ( "RetailerID", db.di(utils.df_ki(data, "retailer"))),
        ( "AnimalID", db.di(utils.df_ki(data, "animal"))),
        ( "OriginalRetailerMovementID", db.di(utils.df_ki(data, "originalretailermovement"))),
        ( "MovementDate", utils.df_d(data, "movementdate", l)),
        ( "MovementType", utils.df_s(data, "type")),
        ( "ReturnDate", utils.df_d(data, "returndate", l)),
        ( "ReturnedReasonID", utils.df_s(data, "returncategory")),
        ( "Donation", utils.df_m(data, "donation", l)),
        ( "InsuranceNumber", utils.df_t(data, "insurance")),
        ( "ReasonForReturn", utils.df_t(data, "reason")),
        ( "ReservationDate", utils.df_d(data, "reservationdate", l)),
        ( "ReservationCancelledDate", utils.df_d(data, "reservationcancelled", l)),
        ( "IsTrial", utils.df_c(data, "trial")),
        ( "IsPermanentFoster", utils.df_c(data, "permanentfoster")),
        ( "TrialEndDate", utils.df_d(data, "trialenddate", l)),
        ( "Comments", utils.df_t(data, "comments"))
        ))
    db.execute(dbo, sql)
    audit.create(dbo, username, "adoption", str(movementid))
    animal.update_animal_status(dbo, animalid)
    animal.update_variable_animal_data(dbo, animalid)
    update_movement_donation(dbo, movementid)
    return movementid

def update_movement_from_form(dbo, username, data):
    """
    Updates a movement record from posted form data
    """
    validate_movement_form_data(dbo, data)
    l = dbo.locale
    movementid = utils.df_ki(data, "movementid")
    sql = db.make_update_user_sql(dbo, "adoption", username, "ID=%d" % movementid, ( 
        ( "AdoptionNumber", utils.df_t(data, "adoptionno")),
        ( "OwnerID", db.di(utils.df_ki(data, "person"))),
        ( "RetailerID", db.di(utils.df_ki(data, "retailer"))),
        ( "AnimalID", db.di(utils.df_ki(data, "animal"))),
        ( "OriginalRetailerMovementID", db.di(utils.df_ki(data, "originalretailermovement"))),
        ( "MovementDate", utils.df_d(data, "movementdate", l)),
        ( "MovementType", utils.df_s(data, "type")),
        ( "ReturnDate", utils.df_d(data, "returndate", l)),
        ( "ReturnedReasonID", utils.df_s(data, "returncategory")),
        ( "Donation", utils.df_m(data, "donation", l)),
        ( "InsuranceNumber", utils.df_t(data, "insurance")),
        ( "ReasonForReturn", utils.df_t(data, "reason")),
        ( "ReservationDate", utils.df_d(data, "reservationdate", l)),
        ( "ReservationCancelledDate", utils.df_d(data, "reservationcancelled", l)),
        ( "IsTrial", utils.df_c(data, "trial")),
        ( "IsPermanentFoster", utils.df_c(data, "permanentfoster")),
        ( "TrialEndDate", utils.df_d(data, "trialenddate", l)),
        ( "Comments", utils.df_t(data, "comments"))
        ))
    preaudit = db.query(dbo, "SELECT * FROM adoption WHERE ID = %d" % movementid)
    db.execute(dbo, sql)
    postaudit = db.query(dbo, "SELECT * FROM adoption WHERE ID = %d" % movementid)
    audit.edit(dbo, username, "adoption", audit.map_diff(preaudit, postaudit))
    animal.update_animal_status(dbo, utils.df_ki(data, "animal"))
    animal.update_variable_animal_data(dbo, utils.df_ki(data, "animal"))
    update_movement_donation(dbo, movementid)

def delete_movement(dbo, username, mid):
    """
    Deletes a movement record
    """
    animalid = db.query_int(dbo, "SELECT AnimalID FROM adoption WHERE ID = %d" % int(mid))
    if animalid == 0:
        raise utils.ASMError("Trying to delete a movement that does not exist")
    db.execute(dbo, "UPDATE ownerdonation SET MovementID = 0 WHERE MovementID = %d" % int(mid))
    audit.delete(dbo, username, "adoption", str(db.query(dbo, "SELECT * FROM adoption WHERE ID=%d" % int(mid))))
    db.execute(dbo, "DELETE FROM adoption WHERE ID = %d" % int(mid))
    animal.update_animal_status(dbo, animalid)
    animal.update_variable_animal_data(dbo, animalid)

def return_movement(dbo, movementid, animalid, returndate):
    """
    Returns a movement with the date given
    """
    db.execute(dbo, "UPDATE adoption SET ReturnDate = %s WHERE ID = %d" % (db.dd(returndate), int(movementid)))
    animal.update_animal_status(dbo, int(animalid))

def insert_adoption_from_form(dbo, username, data, creating = []):
    """
    Inserts a movement from the workflow adopt an animal screen.
    Returns the new movement id
    creating is an ongoing list of animals we're already going to
    create adoptions for. It prevents a never ending recursive loop
    of animal1 being bonded to animal2 that's bonded to animal1, etc.
    """
    l = dbo.locale
    # Validate that we have a movement date before doing anthing
    if None == utils.df_kd(data, "movementdate", l):
        raise utils.ASMValidationError(i18n._("Adoption movements must have a valid adoption date.", l))
    # Get the animal record for this adoption
    a = animal.get_animal(dbo, utils.df_ki(data, "animal"))
    if a is None:
        raise utils.ASMValidationError("Adoption POST has an invalid animal ID: %d" % utils.df_ki(data, "animal"))
    al.debug("Creating adoption for %d (%s - %s)" % (a["ID"], a["SHELTERCODE"], a["ANIMALNAME"]), "movement.insert_adoption_from_form", dbo)
    creating.append(a["ID"])
    # If the animal is bonded to other animals, we call this function
    # again with a copy of the data and the bonded animal substituted
    # so we can create their adoption records too.
    if a["BONDEDANIMALID"] is not None and a["BONDEDANIMALID"] != 0 and a["BONDEDANIMALID"] not in creating:
        al.debug("Found bond to animal %d, creating adoption..." % a["BONDEDANIMALID"], "movement.insert_adoption_from_form", dbo)
        newdata = dict(data)
        newdata["animal"] = str(a["BONDEDANIMALID"])
        insert_adoption_from_form(dbo, username, newdata, creating)
    if a["BONDEDANIMAL2ID"] is not None and a["BONDEDANIMAL2ID"] != 0 and a["BONDEDANIMAL2ID"] not in creating:
        al.debug("Found bond to animal %d, creating adoption..." % a["BONDEDANIMAL2ID"], "movement.insert_adoption_from_form", dbo)
        newdata = dict(data)
        newdata["animal"] = str(a["BONDEDANIMAL2ID"])
        insert_adoption_from_form(dbo, username, newdata, creating)
    cancel_reserves = configuration.cancel_reserves_on_adoption(dbo)
    # Prepare a dictionary of data for the movement table via insert_movement_from_form
    move_dict = {
        "person"                : utils.df_ks(data, "person"),
        "animal"                : utils.df_ks(data, "animal"),
        "adoptionno"            : utils.df_ks(data, "movementnumber"),
        "movementdate"          : utils.df_ks(data, "movementdate"),
        "type"                  : str(ADOPTION),
        "donation"              : utils.df_ks(data, "amount"),
        "insurance"             : utils.df_ks(data, "insurance"),
        "returncategory"        : configuration.default_return_reason(dbo),
        "trial"                 : utils.df_ks(data, "trial"),
        "trialenddate"          : utils.df_ks(data, "trialenddate")
    }
    # Is this animal currently on foster? If so, return the foster
    fm = get_animal_movements(dbo, utils.df_ki(data, "animal"))
    for m in fm:
        if m["MOVEMENTTYPE"] == FOSTER and m["RETURNDATE"] is None:
            return_movement(dbo, m["ID"], utils.df_ki(data, "animal"), utils.df_kd(data, "movementdate", l))
    # Is this animal current at a retailer? If so, return it from the
    # retailer and set the originalretailermovement and retailerid fields
    # on our new adoption movement so it can be linked back
    for m in fm:
        if m["MOVEMENTTYPE"] == RETAILER and m["RETURNDATE"] is None:
            return_movement(dbo, m["ID"], utils.df_ki(data, "animal"), utils.df_kd(data, "movementdate", l))
            move_dict["originalretailermovement"] = str(m["ID"])
            move_dict["retailer"] = str(m["OWNERID"])
    # Did we say we'd like to flag the owner as homechecked?
    if utils.df_kc(data, "homechecked") == 1:
        db.execute(dbo, "UPDATE owner SET IDCheck = 1, DateLastHomeChecked = %s WHERE ID = %d" % \
            ( db.dd(i18n.now(dbo.timezone)), utils.df_ki(data, "person")))
    # If the animal was flagged as not available for adoption, then it
    # shouldn't be since we've just adopted it.
    db.execute(dbo, "UPDATE animal SET IsNotAvailableForAdoption = 0 WHERE ID = %s" % utils.df_ks(data, "animal"))
    # Is the animal reserved to the person adopting? 
    movementid = 0
    for m in fm:
        if m["MOVEMENTTYPE"] == NO_MOVEMENT and m["RESERVATIONDATE"] is not None \
            and m["RESERVATIONCANCELLEDDATE"] is None and m["ANIMALID"] == utils.df_ki(data, "animal") \
            and m["OWNERID"] == utils.df_ki(data, "person"):
            # yes - update the existing movement
            movementid = m["ID"]
            move_dict["movementid"] = str(movementid)
            move_dict["adoptionno"] = utils.padleft(movementid, 6)
            move_dict["reservationdate"] = str(i18n.python2display(l, m["RESERVATIONDATE"]))
            move_dict["comments"] = utils.nulltostr(m["COMMENTS"])
            break
        elif cancel_reserves and m["MOVEMENTTYPE"] == NO_MOVEMENT and m["RESERVATIONDATE"] is not None \
            and m["RESERVATIONCANCELLEDDATE"] is None:
            # no, but it's reserved to someone else and we're cancelling
            # reserves on adoption
            db.execute(dbo, "UPDATE adoption SET ReservationCancelledDate = %s WHERE ID = %d" % \
                ( utils.df_d(data, "movementdate", l), m["ID"] ))
    if movementid != 0:
        update_movement_from_form(dbo, username, move_dict)
    else:
        movementid = insert_movement_from_form(dbo, username, move_dict)
    # Create the donation if there is one
    donation_amount = int(utils.df_m(data, "amount", l))
    if donation_amount > 0:
        due = ""
        received = utils.df_ks(data, "movementdate")
        if configuration.movement_donations_default_due(dbo):
            due = utils.df_ks(data, "movementdate")
            received = ""
        don_dict = {
            "person"                : utils.df_ks(data, "person"),
            "animal"                : utils.df_ks(data, "animal"),
            "movement"              : str(movementid),
            "type"                  : utils.df_ks(data, "donationtype"),
            "payment"               : utils.df_ks(data, "payment"),
            "frequency"             : "0",
            "amount"                : utils.df_ks(data, "amount"),
            "due"                   : due,
            "received"              : received,
            "giftaid"               : utils.df_ks(data, "giftaid")
        }
        financial.insert_donation_from_form(dbo, username, don_dict)
    # And a second donation if there is one
    donation_amount = int(utils.df_m(data, "amount2", l))
    if donation_amount > 0:
        due = ""
        received = utils.df_ks(data, "movementdate")
        if configuration.movement_donations_default_due(dbo):
            due = utils.df_ks(data, "movementdate")
            received = ""
        don_dict = {
            "person"                : utils.df_ks(data, "person"),
            "animal"                : utils.df_ks(data, "animal"),
            "movement"              : str(movementid),
            "type"                  : utils.df_ks(data, "donationtype2"),
            "payment"               : utils.df_ks(data, "payment2"),
            "frequency"             : "0",
            "amount"                : utils.df_ks(data, "amount2"),
            "due"                   : due,
            "received"              : received,
            "giftaid"               : utils.df_ks(data, "giftaid")
        }
        financial.insert_donation_from_form(dbo, username, don_dict)
    # Then any boarding cost record
    cost_amount = int(utils.df_m(data, "costamount", l))
    cost_type = utils.df_ks(data, "costtype")
    cost_create = utils.df_ki(data, "costcreate")
    if cost_amount > 0 and cost_type != "" and cost_create == 1:
        boc_dict = {
            "animalid"          : utils.df_ks(data, "animal"),
            "type"              : cost_type,
            "costdate"          : utils.df_ks(data, "movementdate"),
            "cost"              : utils.df_ks(data, "costamount")
        }
        animal.insert_cost_from_form(dbo, username, boc_dict)
    return movementid

def insert_foster_from_form(dbo, username, data):
    """
    Inserts a movement from the workflow foster an animal screen.
    Returns the new movement id
    """
    # Validate that we have a movement date before doing anthing
    l = dbo.locale
    if None == utils.df_kd(data, "fosterdate", l):
        raise utils.ASMValidationError(i18n._("Foster movements must have a valid foster date.", l))

    # Is this animal already on foster? If so, return that foster first
    fm = get_animal_movements(dbo, utils.df_ki(data, "animal"))
    for m in fm:
        if m["MOVEMENTTYPE"] == FOSTER and m["RETURNDATE"] is None:
            return_movement(dbo, m["ID"], utils.df_ki(data, "animal"), utils.df_kd(data, "fosterdate", l))
    # Create the foster movement
    move_dict = {
        "person"                : utils.df_ks(data, "person"),
        "animal"                : utils.df_ks(data, "animal"),
        "movementdate"          : utils.df_ks(data, "fosterdate"),
        "permanentfoster"       : utils.df_ks(data, "permanentfoster"),
        "adoptionno"            : utils.df_ks(data, "movementnumber"),
        "returndate"            : utils.df_ks(data, "returndate"),
        "type"                  : str(FOSTER),
        "donation"              : utils.df_ks(data, "amount"),
        "returncategory"        : configuration.default_return_reason(dbo)
    }
    movementid = insert_movement_from_form(dbo, username, move_dict)
    return movementid

def insert_transfer_from_form(dbo, username, data):
    """
    Inserts a movement from the workflow transfer an animal screen.
    Returns the new movement id
    """
    # Validate that we have a movement date before doing anthing
    l = dbo.locale
    if None == utils.df_kd(data, "transferdate", l):
        raise utils.ASMValidationError(i18n._("Transfers must have a valid transfer date.", l))

    # Is this animal already on foster? If so, return that foster first
    fm = get_animal_movements(dbo, utils.df_ki(data, "animal"))
    for m in fm:
        if m["MOVEMENTTYPE"] == FOSTER and m["RETURNDATE"] is None:
            return_movement(dbo, m["ID"], utils.df_ki(data, "animal"), utils.df_kd(data, "transferdate", l))
    # Create the transfer movement
    move_dict = {
        "person"                : utils.df_ks(data, "person"),
        "animal"                : utils.df_ks(data, "animal"),
        "adoptionno"            : utils.df_ks(data, "movementnumber"),
        "movementdate"          : utils.df_ks(data, "transferdate"),
        "type"                  : str(TRANSFER),
        "donation"              : utils.df_ks(data, "amount"),
        "returncategory"        : configuration.default_return_reason(dbo)
    }
    movementid = insert_movement_from_form(dbo, username, move_dict)
    return movementid

def insert_reserve_from_form(dbo, username, data):
    """
    Inserts a movement from the workflow reserve an animal screen.
    Returns the new movement id
    """
    # Validate that we have a date before doing anthing
    l = dbo.locale
    if None == utils.df_kd(data, "reservationdate", l):
        raise utils.ASMValidationError(i18n._("Reservations must have a valid reservation date.", l))

    # Do the movement itself first
    move_dict = {
        "person"                : utils.df_ks(data, "person"),
        "animal"                : utils.df_ks(data, "animal"),
        "reservationdate"       : utils.df_ks(data, "reservationdate"),
        "adoptionno"            : utils.df_ks(data, "movementnumber"),
        "movementdate"          : "",
        "type"                  : str(NO_MOVEMENT),
        "donation"              : utils.df_ks(data, "amount"),
        "returncategory"        : configuration.default_return_reason(dbo)
    }
    movementid = insert_movement_from_form(dbo, username, move_dict)
    # Then the donation if we have one
    donation_amount = int(utils.df_m(data, "amount", l))
    if donation_amount > 0:
        due = ""
        received = utils.df_ks(data, "reservationdate")
        if configuration.movement_donations_default_due(dbo):
            due = utils.df_ks(data, "reservationdate")
            received = ""
        don_dict = {
            "person"                : utils.df_ks(data, "person"),
            "animal"                : utils.df_ks(data, "animal"),
            "movement"              : str(movementid),
            "type"                  : utils.df_ks(data, "donationtype"),
            "payment"               : utils.df_ks(data, "payment"),
            "frequency"             : "0",
            "amount"                : utils.df_ks(data, "amount"),
            "due"                   : due,
            "received"              : received,
            "giftaid"               : utils.df_ks(data, "giftaid")
        }
        financial.insert_donation_from_form(dbo, username, don_dict)
    # And a second donation if there is one
    donation_amount = int(utils.df_m(data, "amount2", l))
    if donation_amount > 0:
        due = ""
        received = utils.df_ks(data, "movementdate")
        if configuration.movement_donations_default_due(dbo):
            due = utils.df_ks(data, "movementdate")
            received = ""
        don_dict = {
            "person"                : utils.df_ks(data, "person"),
            "animal"                : utils.df_ks(data, "animal"),
            "movement"              : str(movementid),
            "type"                  : utils.df_ks(data, "donationtype2"),
            "payment"               : utils.df_ks(data, "payment2"),
            "frequency"             : "0",
            "amount"                : utils.df_ks(data, "amount2"),
            "due"                   : due,
            "received"              : received,
            "giftaid"               : utils.df_ks(data, "giftaid")
        }
        financial.insert_donation_from_form(dbo, username, don_dict)
    return movementid

def insert_retailer_from_form(dbo, username, data):
    """
    Inserts a retailer from the workflow move to retailer screen.
    Returns the new movement id
    """
    # Validate that we have a movement date before doing anthing
    l = dbo.locale
    if None == utils.df_kd(data, "retailerdate", l):
        raise utils.ASMValidationError(i18n._("Retailer movements must have a valid movement date.", l))

    # Is this animal already at a foster? If so, return that foster first
    fm = get_animal_movements(dbo, utils.df_ki(data, "animal"))
    for m in fm:
        if m["MOVEMENTTYPE"] == FOSTER and m["RETURNDATE"] is None:
            return_movement(dbo, m["ID"], utils.df_ki(data, "animal"), utils.df_kd(data, "retailerdate", l))
    # Create the retailer movement
    move_dict = {
        "person"                : utils.df_ks(data, "person"),
        "animal"                : utils.df_ks(data, "animal"),
        "movementdate"          : utils.df_ks(data, "retailerdate"),
        "adoptionno"            : utils.df_ks(data, "movementnumber"),
        "type"                  : str(RETAILER),
        "donation"              : utils.df_ks(data, "amount"),
        "returncategory"        : configuration.default_return_reason(dbo)
    }
    movementid = insert_movement_from_form(dbo, username, move_dict)
    return movementid

def update_movement_donation(dbo, movementid):
    """
    Goes through all donations attached to a particular movement and updates
    the denormalised movement total.
    """
    if utils.cint(movementid) == 0: return
    db.execute(dbo, "UPDATE adoption SET Donation = " \
        "(SELECT SUM(Donation) FROM ownerdonation WHERE MovementID = %d) WHERE ID = %d" % \
        (int(movementid), int(movementid)))

def generate_insurance_number(dbo):
    """
    Returns the next insurance number in the sequence
    """
    ins = configuration.auto_insurance_next(dbo)
    nextins = ins + 1
    configuration.auto_insurance_next(dbo, nextins)
    return ins

def auto_cancel_reservations(dbo):
    """
    Automatically cancels reservations after the daily amount set
    """
    cancelafter = configuration.auto_cancel_reserves_days(dbo)
    if cancelafter <= 0:
        al.debug("auto reserve cancel is off.", "movement.auto_cancel_reservations")
        return
    cancelcutoff = i18n.subtract_days(i18n.now(dbo.timezone), cancelafter)
    al.debug("cutoff date: reservations < %s" % db.dd(cancelcutoff), "movement.auto_cancel_reservations")
    sql = "UPDATE adoption SET ReservationCancelledDate = %s " \
        "WHERE MovementDate Is Null AND ReservationCancelledDate Is Null AND " \
        "MovementType = 0 AND ReservationDate < %s" % ( db.dd(i18n.now(dbo.timezone)), db.dd(cancelcutoff))
    count = db.execute(dbo, sql)
    al.debug("cancelled %d reservations older than %d days" % (count, int(cancelafter)), "movement.auto_cancel_reservations", dbo)

    

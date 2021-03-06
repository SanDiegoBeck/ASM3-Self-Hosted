#!/usr/bin/python

import al
import audit
import configuration
import db
import i18n
import movement
import utils
import zipfile, sys
from cStringIO import StringIO

BANK = 1
CREDITCARD = 2
LOAN = 3
EXPENSE = 4
INCOME = 5
PENSION = 6
SHARES = 7
ASSET = 8
LIABILITY = 9

BOTH = 0
RECONCILED = 1
NONRECONCILED = 2

THIS_MONTH = 0
THIS_WEEK = 1
THIS_YEAR = 2
LAST_MONTH = 3
LAST_WEEK = 4

ASCENDING = 0
DESCENDING = 1


def get_account_code(dbo, accountid):
    """
    Returns the code for an accountid
    """
    return db.query_string(dbo, "SELECT Code FROM accounts WHERE ID = %d" % int(accountid))

def get_account_codes(dbo):
    """
    Returns a list of all account codes in order
    """
    l = []
    for a in get_accounts(dbo):
        l.append(a["CODE"])
    return l

def get_account_edit_roles(dbo, accountid):
    """
    Returns a list of edit roles for this account
    """
    roles = []
    rows = db.query(dbo, "SELECT r.RoleName FROM accountsrole ar INNER JOIN role r ON r.ID = ar.RoleID WHERE ar.AccountID = %d AND ar.CanEdit = 1" % int(accountid))
    for r in rows:
        roles.append(r["ROLENAME"])
    return roles

def get_account_id(dbo, code):
    """
    Returns the id for an account code
    """
    return db.query_int(dbo, "SELECT ID FROM accounts WHERE Code = '%s'" % str(code))
    
def get_accounts(dbo):
    """
    Returns all of the accounts with reconciled/balance figures
    ID, CODE, DESCRIPTION, ACCOUNTTYPE, DONATIONTYPEID, RECONCILED, BALANCE, VIEWROLEIDS, VIEWROLES, EDITROLEIDS, EDITROLES
    If an accounting period has been set, balances are calculated from that point
    """
    l = dbo.locale
    pfilter = ""
    aperiod = configuration.accounting_period(dbo)
    if aperiod != "":
        pfilter = " AND TrxDate >= " + db.dd(i18n.display2python(l, aperiod))
    roles = db.query(dbo, "SELECT ar.*, r.RoleName FROM accountsrole ar INNER JOIN role r ON ar.RoleID = r.ID")
    accounts = db.query(dbo, "SELECT a.*, at.AccountType AS AccountTypeName, " \
        "dt.DonationName, " \
        "(SELECT SUM(Amount) FROM accountstrx WHERE DestinationAccountID = a.ID%s) AS dest," \
        "(SELECT SUM(Amount) FROM accountstrx WHERE SourceAccountID = a.ID%s) AS src," \
        "(SELECT SUM(Amount) FROM accountstrx WHERE Reconciled = 1 AND DestinationAccountID = a.ID%s) AS recdest," \
        "(SELECT SUM(Amount) FROM accountstrx WHERE Reconciled = 1 AND SourceAccountID = a.ID%s) AS recsrc " \
        "FROM accounts a " \
        "INNER JOIN lksaccounttype at ON at.ID = a.AccountType " \
        "LEFT OUTER JOIN donationtype dt ON dt.ID = a.DonationTypeID " \
        "ORDER BY a.AccountType, a.Code" % (pfilter, pfilter, pfilter, pfilter))
    for a in accounts:
        dest = a["DEST"]
        src = a["SRC"]
        recdest = a["RECDEST"]
        recsrc = a["RECSRC"]
        if dest is None: dest = 0
        if src is None: src = 0
        if recdest is None: recdest = 0
        if recsrc is None: recsrc = 0
        
        a["BALANCE"] = dest - src
        a["RECONCILED"] = recdest - recsrc
        if a["ACCOUNTTYPE"] == INCOME or a["ACCOUNTTYPE"] == EXPENSE:
            a["BALANCE"] = abs(a["BALANCE"])
            a["RECONCILED"] = abs(a["RECONCILED"])
        viewroleids = []
        viewrolenames = []
        editroleids = []
        editrolenames = []
        for r in roles:
            if r["ACCOUNTID"] == a["ID"] and r["CANVIEW"] == 1:
                viewroleids.append(str(r["ROLEID"]))
                viewrolenames.append(str(r["ROLENAME"]))
            if r["ACCOUNTID"] == a["ID"] and r["CANEDIT"] == 1:
                editroleids.append(str(r["ROLEID"]))
                editrolenames.append(str(r["ROLENAME"]))
        a["VIEWROLEIDS"] = "|".join(viewroleids)
        a["VIEWROLES"] = "|".join(viewrolenames)
        a["EDITROLEIDS"] = "|".join(editroleids)
        a["EDITROLES"] = "|".join(editrolenames)
    return accounts

def get_balance_to_date(dbo, accountid, todate):
    """
    Returns the balance of accountid to todate.
    """
    aid = int(accountid)
    rows = db.query(dbo, "SELECT a.AccountType, " \
        "(SELECT SUM(Amount) FROM accountstrx WHERE SourceAccountID = a.ID AND TrxDate < %s) AS withdrawal," \
        "(SELECT SUM(Amount) FROM accountstrx WHERE DestinationAccountID = a.ID AND TrxDate < %s) AS deposit " \
        "FROM accounts a " \
        "WHERE a.ID = %d" % ( db.dd(todate), db.dd(todate), aid ))
    r = rows[0]
    deposit = r["DEPOSIT"]
    withdrawal = r["WITHDRAWAL"]
    if deposit is None: deposit = 0
    if withdrawal is None: withdrawal = 0
    balance = deposit - withdrawal
    if r["ACCOUNTTYPE"] == INCOME or r["ACCOUNTTYPE"] == EXPENSE:
        balance = abs(balance)
    return balance

def get_balance_fromto_date(dbo, accountid, fromdate, todate):
    """
    Returns the balance of accountid from fromdate to todate.
    """
    aid = int(accountid)
    rows = db.query(dbo, "SELECT a.AccountType, " \
        "(SELECT SUM(Amount) FROM accountstrx WHERE SourceAccountID = a.ID AND TrxDate >= %s AND TrxDate < %s) AS withdrawal," \
        "(SELECT SUM(Amount) FROM accountstrx WHERE DestinationAccountID = a.ID AND TrxDate >= %s AND TrxDate < %s) AS deposit " \
        "FROM accounts a " \
        "WHERE a.ID = %d" % ( db.dd(fromdate), db.dd(todate), db.dd(fromdate), db.dd(todate), aid ))
    r = rows[0]
    deposit = r["DEPOSIT"]
    withdrawal = r["WITHDRAWAL"]
    if deposit is None: deposit = 0
    if withdrawal is None: withdrawal = 0
    balance = deposit - withdrawal
    if r["ACCOUNTTYPE"] == INCOME or r["ACCOUNTTYPE"] == EXPENSE:
        balance = abs(balance)
    return balance

def mark_reconciled(dbo, trxid):
    """
    Marks a transaction reconciled.
    """
    db.execute(dbo, "UPDATE accountstrx SET Reconciled = 1 WHERE ID = %d" % int(trxid))

def get_transactions(dbo, accountid, datefrom, dateto, reconciled):
    """
    Gets a list of transactions for the account given, between
    two python dates. PERSONID and PERSONNAME are returned for
    linked donations.
    accountid: Account ID as integer
    datefrom: Python from date
    dateto: Python to date
    reconciled: one of RECONCILED, NONRECONCILED or BOTH to filter
    It creates extra columns, THISACCOUNT and OTHERACCOUNT
    for use by the UI when displaying transactions. It also adds 
    THISACCOUNTCODE and OTHERACCOUNTCODE for display purposes, 
    the BALANCE column and WITHDRAWAL and DEPOSIT.
    """
    l = dbo.locale
    period = configuration.accounting_period(dbo)
    if not configuration.account_period_totals(dbo):
        period = ""
    # If we have an accounting period set and it's after the from date,
    # use that instead
    if period != "" and i18n.after(i18n.display2python(l, period), datefrom):
        datefrom = i18n.display2python(l, period)
    recfilter = ""
    if reconciled == RECONCILED:
        recfilter = " AND Reconciled = 1"
    elif reconciled == NONRECONCILED:
        recfilter = " AND Reconciled = 0"
    rows = db.query(dbo, "SELECT t.*, srcac.Code AS SrcCode, destac.Code AS DestCode, " \
        "o.OwnerName AS PersonName, o.ID AS PersonID, a.ID AS AnimalID, " \
        "a.AnimalName AS AnimalName, " \
        "CASE " \
        "WHEN 'Yes' = (SELECT ItemValue FROM configuration WHERE ItemName Like 'UseShortShelterCodes') " \
        "THEN a.ShelterCode ELSE a.ShortCode END AS AnimalCode " \
        "FROM accountstrx t " \
        "INNER JOIN accounts srcac ON srcac.ID = t.SourceAccountID " \
        "INNER JOIN accounts destac ON destac.ID = t.DestinationAccountID " \
        "LEFT OUTER JOIN ownerdonation od ON od.ID = t.OwnerDonationID " \
        "LEFT OUTER JOIN owner o ON o.ID = od.OwnerID " \
        "LEFT OUTER JOIN animal a ON a.ID = od.AnimalID " \
        "WHERE t.TrxDate >= %s AND t.TrxDate <= %s%s " \
        "AND (t.SourceAccountID = %d OR t.DestinationAccountID = %d) " \
        "ORDER BY t.TrxDate" % ( db.dd(datefrom), db.dd(dateto), recfilter, int(accountid), int(accountid)))
    balance = 0
    if period != "":
        balance = get_balance_fromto_date(dbo, accountid, i18n.display2python(l, period), datefrom)
    else:
        balance = get_balance_to_date(dbo, accountid, datefrom)
    for r in rows:
        # Error scenario - this account is both source and destination
        if r["SOURCEACCOUNTID"] == accountid and r["DESTINATIONACCOUNTID"] == accountid:
            r["WITHDRAWAL"] = 0
            r["DEPOSIT"] = 0
            r["THISACCOUNT"] = accountid
            r["THISACCOUNTCODE"] = r["SRCCODE"]
            r["OTHERACCOUNT"] = accountid
            r["OTHERACCOUNTCODE"] = "<-->"
            r["BALANCE"] = balance
        # This account is the source - it's a withdrawal
        elif r["SOURCEACCOUNTID"] == accountid:
            r["WITHDRAWAL"] = r["AMOUNT"]
            r["DEPOSIT"] = 0
            r["OTHERACCOUNT"] = r["DESTINATIONACCOUNTID"]
            r["OTHERACCOUNTCODE"] = r["DESTCODE"]
            r["THISACCOUNT"] = accountid
            r["THISACCOUNTCODE"] = r["SRCCODE"]
            balance -= r["AMOUNT"]
            r["BALANCE"] = balance
        # This account is the destination - it's a deposit
        else:
            r["WITHDRAWAL"] = 0
            r["DEPOSIT"] = r["AMOUNT"]
            r["OTHERACCOUNT"] = r["SOURCEACCOUNTID"]
            r["OTHERACCOUNTCODE"] = r["SRCCODE"]
            r["THISACCOUNT"] = accountid
            r["THISACCOUNTCODE"] = r["DESTCODE"]
            balance += r["AMOUNT"]
            r["BALANCE"] = balance
    return rows
       
def get_donation(dbo, did):
    """
    Returns a single donation by id
    """
    return db.query(dbo, "SELECT od.*, dt.DonationName, lk.Name AS IsGiftAidName " \
        "FROM ownerdonation od " \
        "INNER JOIN donationtype dt ON dt.ID = od.DonationTypeID " \
        "LEFT OUTER JOIN lksyesno lk ON od.IsGiftAid = lk.ID " \
        "WHERE od.ID = %d" % int(did))[0]

def get_donations(dbo, offset = "m31"):
    """
    Returns a recordset of donations
    offset is m to go backwards, or p to go forwards with a number of days.
    ID, DONATIONTYPEID, DONATIONNAME, DATE, DATEDUE, DONATION,
    ISGIFTAID, FREQUENCY, FREQUENCYNAME, NEXTCREATED, COMMENTS, OWNERNAME, 
    ANIMALNAME, SHELTERCODE, OWNERID, ANIMALID
    """
    ec = ""
    order = ""
    offsetdays = utils.cint(offset[1:])
    if offset.startswith("m"):
        ec = "Date >= %s AND Date <= %s" % (db.dd( i18n.subtract_days(i18n.now(dbo.timezone), offsetdays)), db.dd(i18n.now(dbo.timezone)))
        order = "Date DESC"
    elif offset.startswith("p"):
        ec = "Date Is Null AND DateDue >= %s AND DateDue <= %s" % (db.dd(i18n.now(dbo.timezone)), db.dd(i18n.add_days(i18n.now(dbo.timezone), offsetdays)))
        order = "DateDue DESC"
    elif offset.startswith("d"):
        ec = "Date Is Null AND DateDue <= %s" % (db.dd(i18n.now(dbo.timezone)))
        order = "DateDue"
    return db.query(dbo, "SELECT * FROM v_ownerdonation " \
        "WHERE %s "
        "ORDER BY %s" % (ec, order))

def get_animal_donations(dbo, aid, sort = ASCENDING):
    """
    Returns all of the owner donation records for an animal, along with
    some owner and animal info.
    ID, DONATIONTYPEID, DONATIONNAME, DATE, DATEDUE, DONATION,
    ISGIFTAID, FREQUENCY, FREQUENCYNAME, NEXTCREATED, COMMENTS, OWNERNAME, 
    ANIMALNAME, SHELTERCODE, OWNERID, ANIMALID
    """
    order = "Date DESC"
    if sort == ASCENDING:
        order = "Date"
    return db.query(dbo, "SELECT * FROM v_ownerdonation " \
        "WHERE AnimalID = %d " \
        "ORDER BY %s" % (int(aid), order))

def get_person_donations(dbo, oid, sort = ASCENDING):
    """
    Returns all of the owner donation records for an owner, along with some animal info
    ID, DONATIONTYPEID, DONATIONNAME, DATE, DATEDUE, DONATION,
    ISGIFTAID, FREQUENCY, FREQUENCYNAME, NEXTCREATED, COMMENTS, OWNERNAME, 
    ANIMALNAME, SHELTERCODE, OWNERID, ANIMALID
    """
    order = "Date DESC"
    if sort == ASCENDING:
        order = "Date"
    return db.query(dbo, "SELECT * FROM v_ownerdonation " \
        "WHERE OwnerID = %d " \
        "ORDER BY %s" % (int(oid), order))

def get_vouchers(dbo, personid):
    """
    Returns a list of vouchers for an owner
    ID, VOUCHERNAME, VOUCHERID, DATEISSUED, DATEEXPIRED,
    VALUE, COMMENTS
    """
    return db.query(dbo, "SELECT * FROM v_ownervoucher " \
        "WHERE OwnerID = %d ORDER BY DateIssued" % int(personid))

def insert_donation_from_form(dbo, username, data):
    """
    Creates a donation record from posted form data 
    """
    l = dbo.locale
    donationid = db.get_id(dbo, "ownerdonation")
    sql = db.make_insert_user_sql(dbo, "ownerdonation", username, ( 
        ( "ID", db.di(donationid)),
        ( "OwnerID", db.di(utils.df_ki(data, "person"))),
        ( "AnimalID", db.di(utils.df_ki(data, "animal"))),
        ( "MovementID", db.di(utils.df_ki(data, "movement"))),
        ( "DonationTypeID", utils.df_s(data, "type")),
        ( "DonationPaymentID", utils.df_s(data, "payment")),
        ( "Frequency", utils.df_s(data, "frequency")),
        ( "Donation", utils.df_m(data, "amount", l)),
        ( "DateDue", utils.df_d(data, "due", l)),
        ( "Date", utils.df_d(data, "received", l)),
        ( "NextCreated", db.di(0)),
        ( "IsGiftAid", utils.df_s(data, "giftaid")),
        ( "Comments", utils.df_t(data, "comments"))
        ))
    db.execute(dbo, sql)
    audit.create(dbo, username, "ownerdonation", str(donationid))
    update_matching_transaction(dbo, username, donationid)
    check_create_next_donation(dbo, username, donationid)
    movement.update_movement_donation(dbo, utils.df_ki(data, "movement"))
    return donationid

def update_donation_from_form(dbo, username, data):
    """
    Updates a donation record from posted form data
    """
    l = dbo.locale
    donationid = utils.df_ki(data, "donationid")
    sql = db.make_update_user_sql(dbo, "ownerdonation", username, "ID=%d" % donationid, ( 
        ( "OwnerID", db.di(utils.df_ki(data, "person"))),
        ( "AnimalID", db.di(utils.df_ki(data, "animal"))),
        ( "MovementID", db.di(utils.df_ki(data, "movement"))),
        ( "DonationTypeID", utils.df_s(data, "type")),
        ( "DonationPaymentID", utils.df_s(data, "payment")),
        ( "Frequency", utils.df_s(data, "frequency")),
        ( "Donation", utils.df_m(data, "amount", l)),
        ( "DateDue", utils.df_d(data, "due", l)),
        ( "Date", utils.df_d(data, "received", l)),
        ( "IsGiftAid", utils.df_s(data, "giftaid")),
        ( "Comments", utils.df_t(data, "comments"))
        ))
    preaudit = db.query(dbo, "SELECT * FROM ownerdonation WHERE ID = %d" % donationid)
    db.execute(dbo, sql)
    postaudit = db.query(dbo, "SELECT * FROM ownerdonation WHERE ID = %d" % donationid)
    audit.edit(dbo, username, "ownerdonation", audit.map_diff(preaudit, postaudit))
    update_matching_transaction(dbo, username, donationid)
    check_create_next_donation(dbo, username, donationid)
    movement.update_movement_donation(dbo, utils.df_ki(data, "movement"))

def delete_donation(dbo, username, did):
    """
    Deletes a donation record
    """
    audit.delete(dbo, username, "ownerdonation", str(db.query(dbo, "SELECT * FROM ownerdonation WHERE ID=%d" % int(did))))
    movementid = db.query_int(dbo, "SELECT MovementID FROM ownerdonation WHERE ID = %d" % int(did))
    db.execute(dbo, "DELETE FROM ownerdonation WHERE ID = %d" % int(did))
    # Delete any existing transaction for this donation if there is one
    db.execute(dbo, "DELETE FROM accountstrx WHERE OwnerDonationID = %d" % int(did))
    movement.update_movement_donation(dbo, movementid)

def receive_donation(dbo, username, did):
    """
    Marks a donation received
    """
    if id is None or did == "": return
    db.execute(dbo, "UPDATE ownerdonation SET Date = %s WHERE ID = %d" % ( db.dd(i18n.now(dbo.timezone)), int(did)))
    audit.edit(dbo, username, "ownerdonation", str(did) + ": received")
    update_matching_transaction(dbo, username, int(did))
    check_create_next_donation(dbo, username, did)

def check_create_next_donation(dbo, username, odid):
    """
    Checks to see if a donation is now received and the next in 
    a sequence needs to be created for donations with a frequency 
    """
    al.debug("Create next donation %d" % int(odid), "financial.check_create_next_donation", dbo)
    d = db.query(dbo, "SELECT * FROM ownerdonation WHERE ID = %d" % int(odid))
    if d is None or len(d) == 0: 
        al.error("No donation found for %d" % int(odid), "financial.check_create_next_donation", dbo)
        return
    d = d[0]
    # If we have a frequency > 0, the nextcreated flag isn't set
    # and there's a datereceived and due then we need to create the
    # next donation in the sequence
    if d["DATEDUE"] != None and d["DATE"] != None and d["FREQUENCY"] > 0 and d["NEXTCREATED"] == 0:
        nextdue = d["DATEDUE"]
        if d["FREQUENCY"] == 1:
            nextdue = i18n.add_days(nextdue, 7)
        if d["FREQUENCY"] == 2:
            nextdue = i18n.add_months(nextdue, 1)
        if d["FREQUENCY"] == 3:
            nextdue = i18n.add_months(nextdue, 3)
        if d["FREQUENCY"] == 4:
            nextdue = i18n.add_years(nextdue, 1)
        al.debug("Next donation due %s" % str(nextdue), "financial.check_create_next_donation", dbo)
        # Update nextcreated flag for this donation
        db.execute(dbo, "UPDATE ownerdonation SET NextCreated = 1 WHERE ID = %d" % int(odid))
        # Create the new donation due record
        did = db.get_id(dbo, "ownerdonation")
        sql = db.make_insert_user_sql(dbo, "ownerdonation", username, (
            ( "ID", db.di(did)),
            ( "AnimalID", db.di(d["ANIMALID"])),
            ( "OwnerID", db.di(d["OWNERID"])),
            ( "MovementID", db.di(d["MOVEMENTID"])),
            ( "DonationTypeID", db.di(d["DONATIONTYPEID"])),
            ( "DateDue", db.dd(nextdue)),
            ( "Date", db.dd(None)),
            ( "Donation", db.di(d["DONATION"])),
            ( "IsGiftAid", db.di(d["ISGIFTAID"])),
            ( "DonationPaymentID", db.di(d["DONATIONPAYMENTID"])),
            ( "Frequency", db.di(d["FREQUENCY"])),
            ( "NextCreated", db.di(0)),
            ( "Comments", db.ds(d["COMMENTS"]))
        ))
        db.execute(dbo, sql)

def update_matching_transaction(dbo, username, odid):
    """
    Creates a matching account transaction for a donation or updates
    an existing trx if it already exists
    """
    # Don't do anything if we aren't creating matching transactions
    if not configuration.create_donation_trx(dbo): 
        al.debug("Create donation trx is off, not creating trx.", "financial.update_matching_transaction", dbo)
        return

    dr = db.query(dbo, "SELECT * FROM ownerdonation WHERE ID = %d" % int(odid))
    if dr is None or len(dr) == 0:
        al.error("No matching transaction for %d found in database, bailing" % int(odid), "financial.update_matching_transaction", dbo)
        return

    d = dr[0]

    # If the donation hasn't been received, don't do anything
    if d["DATE"] is None: 
        al.debug("Donation not received, not creating trx.", "financial.update_matching_transaction", dbo)
        return
    # Do we already have an existing transaction for this donation?
    # If we do, we only need to check the amounts as it's now the
    # users problem if they picked the wrong donationtype/account
    trxid = db.query_int(dbo, "SELECT ID FROM accountstrx WHERE OwnerDonationID = %d" % int(odid))
    if trxid != 0:
        al.debug("Already have an existing transaction, updating amount to %d" % d["DONATION"], "financial.update_matching_transaction", dbo)
        db.execute(dbo, "UPDATE accountstrx SET Amount = %d WHERE ID = %d" % (d["DONATION"], trxid))
        return
    # ========== NOT USED - we used to force regeneration
    #                       instead of checking for the existing transaction
    # Delete any existing transaction for this donation if there is one
    # al.debug("Removing any existing trx for this donation.", "financial.update_matching_transaction", dbo)
    # db.execute(dbo, "DELETE FROM accountstrx WHERE OwnerDonationID = %d" % int(odid))
    # ========== NOT USED
    # Get the source account for this type of donation, use the first income account on file for that type
    source = db.query_int(dbo, "SELECT ID FROM accounts WHERE AccountType = %d AND DonationTypeID = %d ORDER BY ID" % (INCOME, int(d["DONATIONTYPEID"])))
    if source == 0:
        # This shouldn't happen, but we can't go ahead without an account
        raise utils.ASMValidationError("No source account found for donation type, can't create trx")
    # Get the target account
    target = configuration.donation_target_account(dbo)
    al.debug("Target account in config is: %s" % target, "financial.update_matching_transaction", dbo)
    # If no target is configured, use the first bank account on file
    if target == 0:
        target = db.query_int(dbo, "SELECT ID FROM accounts WHERE AccountType = 1")
        al.debug("Got blank target, getting first bank account: %s" % target, "financial.update_matching_transaction", dbo)
        if target == 0:
            # Shouldn't happen, but we have no bank accounts on file
            al.error("No target available for trx. Bailing.", "financial.update_matching_transaction", dbo)
            raise utils.ASMValidationError("No bank accounts on file, can't set target for donation trx")
    # Has a mapping been created by the user for this donation type
    # to a destination other than the default?
    maps = configuration.donation_account_mappings(dbo)
    if maps.has_key(str(d["DONATIONTYPEID"])):
        target = maps[str(d["DONATIONTYPEID"])]
        al.debug("Found override for donationtype %s, got new target account %s" % (str(d["DONATIONTYPEID"]), str(target)), "financial.update_matching_transaction", dbo)
    # Is the donation for a negative amount? If so, flip the accounts
    # round as this is a refund donation and make the amount positive.
    amount = d["DONATION"]
    if amount < 0:
        oldtarget = target
        target = source
        source = oldtarget
        amount = abs(amount)
    # Create the transaction
    tid = db.get_id(dbo, "accountstrx")
    sql = db.make_insert_user_sql(dbo, "accountstrx", username, (
        ( "ID", db.di(tid) ),
        ( "TrxDate", db.dd(d["DATE"])),
        ( "Description", db.ds(d["COMMENTS"])),
        ( "Reconciled", db.di(0)),
        ( "Amount", db.di(amount)),
        ( "SourceAccountID", db.di(source)),
        ( "DestinationAccountID", db.di(target)),
        ( "OwnerDonationID", db.di(int(odid)))
        ))
    db.execute(dbo, sql)
    al.debug("Trx created with ID %d" % int(tid), "financial.update_matching_transaction", dbo)

def insert_account_from_donationtype(dbo, dtid, name, desc):
    """
    Creates an account from a donation type record
    """
    l = dbo.locale
    aid = db.get_id(dbo, "accounts")
    acode = i18n._("Income::", l) + name.replace(" ", "")
    sql = db.make_insert_user_sql(dbo, "accounts", "system", ( 
        ( "ID", db.di(aid)),
        ( "Code", db.ds(acode)),
        ( "AccountType", db.di(INCOME)),
        ( "DonationTypeID", db.di(dtid)),
        ( "Description", db.ds(desc))
        ))
    db.execute(dbo, sql)
    audit.create(dbo, "system", "accounts", str(aid))

def insert_account_from_form(dbo, username, post):
    """
    Creates an account from posted form data 
    """
    l = dbo.locale
    if post["code"] == "":
        raise utils.ASMValidationError(i18n._("Account code cannot be blank.", l))
    if 0 != db.query_int(dbo, "SELECT COUNT(*) FROM accounts WHERE Code Like '%s'" % post["code"]):
        raise utils.ASMValidationError(i18n._("Account code '{0}' has already been used.", l).format(post["code"]))

    aid = db.get_id(dbo, "accounts")
    sql = db.make_insert_user_sql(dbo, "accounts", username, ( 
        ( "ID", db.di(aid)),
        ( "Code", post.db_string("code")),
        ( "AccountType", post.db_integer("type")),
        ( "DonationTypeID", post.db_integer("donationtype")),
        ( "Description", post.db_string("description"))
        ))
    db.execute(dbo, sql)
    audit.create(dbo, username, "accounts", str(aid))
    accountid = post.integer("accountid")
    for rid in post.integer_list("viewroles"):
        db.execute(dbo, "INSERT INTO accountsrole (AccountID, RoleID, CanView, CanEdit) VALUES (%d, %d, 1, 0)" % (accountid, rid))
    for rid in post.integer_list("editroles"):
        if rid in post.integer_list("viewroles"):
            db.execute(dbo, "UPDATE accountsrole SET CanEdit = 1 WHERE AccountID = %d AND RoleID = %d" % (accountid, rid))
        else:
            db.execute(dbo, "INSERT INTO accountsrole (AccountID, RoleID, CanView, CanEdit) VALUES (%d, %d, 0, 1)" % (accountid, rid))
    return aid

def update_account_from_form(dbo, username, post):
    """
    Updates an account from posted form data
    """
    l = dbo.locale
    accountid = post.integer("accountid")
    if post["code"] == "":
        raise utils.ASMValidationError(i18n._("Account code cannot be blank.", l))
    if 0 != db.query_int(dbo, "SELECT COUNT(*) FROM accounts WHERE Code Like '%s' AND ID <> %d" % (post["code"], accountid)):
        raise utils.ASMValidationError(i18n._("Account code '{0}' has already been used.", l).format(post["code"]))

    sql = db.make_update_user_sql(dbo, "accounts", username, "ID=%d" % accountid, ( 
        ( "Code", post.db_string("code")),
        ( "AccountType", post.db_integer("type")),
        ( "DonationTypeID", post.db_integer("donationtype")),
        ( "Description", post.db_string("description"))
        ))
    preaudit = db.query(dbo, "SELECT * FROM accounts WHERE ID = %d" % accountid)
    db.execute(dbo, sql)
    postaudit = db.query(dbo, "SELECT * FROM accounts WHERE ID = %d" % accountid)
    audit.edit(dbo, username, "accounts", audit.map_diff(preaudit, postaudit))
    db.execute(dbo, "DELETE FROM accountsrole WHERE AccountID = %d" % accountid)
    for rid in post.integer_list("viewroles"):
        db.execute(dbo, "INSERT INTO accountsrole (AccountID, RoleID, CanView, CanEdit) VALUES (%d, %d, 1, 0)" % (accountid, rid))
    for rid in post.integer_list("editroles"):
        if rid in post.integer_list("viewroles"):
            db.execute(dbo, "UPDATE accountsrole SET CanEdit = 1 WHERE AccountID = %d AND RoleID = %d" % (accountid, rid))
        else:
            db.execute(dbo, "INSERT INTO accountsrole (AccountID, RoleID, CanView, CanEdit) VALUES (%d, %d, 0, 1)" % (accountid, rid))

def delete_account(dbo, username, aid):
    """
    Deletes an account
    """
    audit.delete(dbo, username, "accounts", str(db.query(dbo, "SELECT * FROM accounts WHERE ID=%d" % int(aid))))
    db.execute(dbo, "DELETE FROM accountstrx WHERE SourceAccountID = %d OR DestinationAccountID = %d" % ( int(aid), int(aid) ))
    db.execute(dbo, "DELETE FROM accountsrole WHERE AccountID = %d" % int(aid))
    db.execute(dbo, "DELETE FROM accounts WHERE ID = %d" % int(aid))

def insert_trx_from_form(dbo, username, post):
    """
    Creates a transaction from posted form data
    """
    l = dbo.locale
    amount = 0
    source = 0
    target = 0
    deposit = post.money("deposit")
    withdrawal = post.money("withdrawal")
    account = post.integer("accountid")
    other = get_account_id(dbo, post["otheraccount"])
    if other == 0:
        raise utils.ASMValidationError(i18n._("Account code '{0}' is not valid.", l).format(post["otheraccount"]))
    if deposit > 0:
        amount = deposit
        source = other
        target = account
    else:
        amount = withdrawal
        source = account
        target = other
    tid = db.get_id(dbo, "accountstrx")
    sql = db.make_insert_user_sql(dbo, "accountstrx", username, (
        ( "ID", db.di(tid) ),
        ( "TrxDate", post.db_date("trxdate")),
        ( "Description", post.db_string("description")),
        ( "Reconciled", post.db_boolean("reconciled")),
        ( "Amount", db.di(amount)),
        ( "SourceAccountID", db.di(source)),
        ( "DestinationAccountID", db.di(target)),
        ( "OwnerDonationID", db.di(0))
        ))
    db.execute(dbo, sql)
    audit.create(dbo, username, "accountstrx", str(tid) + ": " + post["description"])

def update_trx_from_form(dbo, username, post):
    """
    Updates a transaction from posted form data
    """
    l = dbo.locale
    amount = 0
    source = 0
    target = 0
    deposit = post.money("deposit")
    withdrawal = post.money("withdrawal")
    account = post.integer("accountid")
    trxid = post.integer("trxid")
    other = get_account_id(dbo, post["otheraccount"])
    if other == 0:
        raise utils.ASMValidationError(i18n._("Account code '{0}' is not valid.", l).format(post["otheraccount"]))
    if deposit > 0:
        amount = deposit
        source = other
        target = account
    else:
        amount = withdrawal
        source = account
        target = other
    sql = db.make_update_user_sql(dbo, "accountstrx", username, "ID=%d" % trxid, (
        ( "TrxDate", post.db_date("trxdate")),
        ( "Description", post.db_string("description")),
        ( "Reconciled", post.db_integer("reconciled")),
        ( "Amount", db.di(amount)),
        ( "SourceAccountID", db.di(source)),
        ( "DestinationAccountID", db.di(target))
        ))
    preaudit = db.query(dbo, "SELECT * FROM accountstrx WHERE ID = %d" % trxid)
    db.execute(dbo, sql)
    postaudit = db.query(dbo, "SELECT * FROM accountstrx WHERE ID = %d" % trxid)
    audit.edit(dbo, username, "accountstrx", audit.map_diff(preaudit, postaudit))

def delete_trx(dbo, username, tid):
    """
    Deletes a transaction
    """
    audit.delete(dbo, username, "accountstrx", str(db.query(dbo, "SELECT * FROM accountstrx WHERE ID=%d" % int(tid))))
    db.execute(dbo, "DELETE FROM accountstrx WHERE ID = %d" % int(tid))

def insert_voucher_from_form(dbo, username, data):
    """
    Creates a voucher record from posted form data 
    """
    l = dbo.locale
    voucherid = db.get_id(dbo, "ownervoucher")
    sql = db.make_insert_user_sql(dbo, "ownervoucher", username, ( 
        ( "ID", db.di(voucherid)),
        ( "OwnerID", db.di(utils.df_ki(data, "personid"))),
        ( "VoucherID", utils.df_s(data, "type")),
        ( "DateIssued", utils.df_d(data, "issued", l)),
        ( "DateExpired", utils.df_d(data, "expires", l)),
        ( "Value", utils.df_m(data, "amount", l)),
        ( "Comments", utils.df_t(data, "comments"))
        ))
    db.execute(dbo, sql)
    audit.create(dbo, username, "ownervoucher", str(voucherid))
    return voucherid

def update_voucher_from_form(dbo, username, data):
    """
    Updates a voucher record from posted form data
    """
    l = dbo.locale
    voucherid = utils.df_ki(data, "voucherid")
    sql = db.make_update_user_sql(dbo, "ownervoucher", username, "ID=%d" % voucherid, ( 
        ( "VoucherID", utils.df_s(data, "type")),
        ( "DateIssued", utils.df_d(data, "issued", l)),
        ( "DateExpired", utils.df_d(data, "expires", l)),
        ( "Value", utils.df_m(data, "amount", l)),
        ( "Comments", utils.df_t(data, "comments"))
    ))
    preaudit = db.query(dbo, "SELECT * FROM ownervoucher WHERE ID = %d" % voucherid)
    db.execute(dbo, sql)
    postaudit = db.query(dbo, "SELECT * FROM ownervoucher WHERE ID = %d" % voucherid)
    audit.edit(dbo, username, "ownervoucher", audit.map_diff(preaudit, postaudit))

def delete_voucher(dbo, username, vid):
    """
    Deletes a voucher record
    """
    audit.delete(dbo, username, "ownervoucher", str(db.query(dbo, "SELECT * FROM ownervoucher WHERE ID=%d" % int(vid))))
    db.execute(dbo, "DELETE FROM ownervoucher WHERE ID = %d" % int(vid))

def giftaid_spreadsheet(dbo, path, fromdate, todate):
    """
    Generates an HMRC giftaid spreadsheet in their ODS format. The template
    is stored in src/static/docs/giftaid.ods
    path: The path to the ASM installation
    fromdate: Python date, the date to include donations from
    todate: Python date, the date to include donations to
    """
    def housenumber(s):
        # Return the full address if the first word is not numeric
        bits = s.strip().split(" ")
        houseno = s
        if len(bits) > 0 and utils.cint(bits[0]) > 0:
            houseno = bits[0]
        return houseno

    # Get the zip file containing our tax year template and load
    # it into an in-memory file
    try:
        ods = open(path + "static/docs/giftaid.ods", "r")
        zf = zipfile.ZipFile(ods, "r")
        # Load the content.xml file
        content = zf.open("content.xml").read()
        dons = db.query(dbo, "SELECT od.Date AS DonationDate, od.Donation AS DonationAmount, o.* " \
            "FROM ownerdonation od " \
            "INNER JOIN owner o ON od.OwnerID = o.ID " \
            "WHERE od.IsGiftAid = 1 AND od.Date Is Not Null AND " \
            "od.Date >= %s AND od.Date <= %s ORDER BY od.Date" % (db.dd(fromdate), db.dd(todate)))
        al.debug("got %d giftaid donations for %s -> %s" % (len(dons), str(fromdate), str(todate)), "financial.giftaid_spreadsheet", dbo)
        # Insert them into the content.xml
        # We just replace the first occurrence each time
        subearly = False
        for d in dons:
            if not subearly:
                subearly = True
                content = content.replace("DONEARLIESTDONATION", i18n.format_date("%d/%m/%y", d["DONATIONDATE"]))
            content = content.replace("DONTITLE", d["OWNERTITLE"], 1)
            content = content.replace("DONFIRSTNAME", d["OWNERFORENAMES"], 1)
            content = content.replace("DONLASTNAME", d["OWNERSURNAME"], 1)
            content = content.replace("DONHOUSENUMBER", housenumber(d["OWNERADDRESS"]), 1)
            content = content.replace("DONPOSTCODE", d["OWNERPOSTCODE"], 1)
            content = content.replace("DONAGGREGATE", "", 1)
            content = content.replace("DONSPONSOR", "", 1)
            # Switch the string date format to a real date with the correct value
            content = content.replace("table:style-name=\"ce36\" office:value-type=\"string\">", 
                "table:style-name=\"ce36\" office:value-type=\"date\" office:date-value=\"%s\">" % \
                i18n.format_date("%Y-%m-%d", d["DONATIONDATE"]), 1)
            content = content.replace("DONDATE", i18n.format_date("%d/%m/%y", d["DONATIONDATE"]), 1)
            donamt = str(float(d["DONATIONAMOUNT"]) / 100)
            content = content.replace("<text:p>54,321.00</text:p>", "<text:p>" + donamt + "</text:p>", 1)
            content = content.replace("office:value=\"54321\"", "office:value=\"" + donamt + "\"", 1)
        # Clear out anything remaining
        content = content.replace("DONTITLE", "")
        content = content.replace("DONFIRSTNAME", "")
        content = content.replace("DONLASTNAME", "")
        content = content.replace("DONHOUSENUMBER", "")
        content = content.replace("DONPOSTCODE", "")
        content = content.replace("DONAGGREGATE", "")
        content = content.replace("DONSPONSOR", "")
        content = content.replace("DONDATE", "")
        content = content.replace("<text:p>54,321.00</text:p>", "<text:p></text:p>")
        content = content.replace("office:value=\"54321\"", "office:value=\"\"")
        # Write the replacement file
        zo = StringIO()
        zfo = zipfile.ZipFile(zo, "w")
        for f in zf.namelist():
            if f == "content.xml":
                zfo.writestr("content.xml", content)
            else:
                zfo.writestr(f, zf.open(f).read())
        zf.close()
        zfo.close()
        # Return the zip data
        return zo.getvalue()
    except Exception,zderr:
        al.error("failed generating spreadsheet: %s" % str(zderr), "financial.giftaid_spreadsheet", dbo, sys.exc_info())
        raise utils.ASMError("Failed generating spreadsheet: %s" % str(zderr))


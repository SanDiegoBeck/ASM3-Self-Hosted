#!/usr/bin/python

import al
import configuration, db, dbfs
import sys
from i18n import _, BUILD
from sitedefs import ASM3_PK_STRATEGY


LATEST_VERSION = 33106
VERSIONS = ( 
    2870, 3000, 3001, 3002, 3003, 3004, 3005, 3006, 3007, 3008, 3009, 3010, 3050,
    3051, 3081, 3091, 3092, 3093, 3094, 3110, 3111, 3120, 3121, 3122, 3123, 3200,
    3201, 3202, 3203, 3204, 3210, 3211, 3212, 3213, 3214, 3215, 3216, 3217, 3218,
    3220, 3221, 3222, 3223, 3224, 3225, 3300, 3301, 3302, 3303, 3304, 3305, 3306,
    3307, 3308, 3309, 33010, 33011, 33012, 33013, 33014, 33015, 33016, 33017, 33018,
    33019, 33101, 33102, 33104, 33105, 33106
)

# All ASM3 tables
TABLES = ( "accounts", "accountsrole", "accountstrx", "activeuser", "additional", "additionalfield",
    "adoption", "animal", "animalcost", "animaldiet", "animalfigures", "animalfiguresannual", 
    "animalfiguresasilomar", "animalfound", "animallitter", "animallost", "animalmedical", 
    "animalmedicaltreatment", "animalname", "animaltype", "animaltest", "animalvaccination", 
    "animalwaitinglist", "audittrail", "basecolour", "breed", "configuration", "costtype", 
    "customreport", "customreportrole", "dbfs", "deathreason", "diary", "diarytaskdetail", "diarytaskhead", 
    "diet", "donationpayment", "donationtype", "entryreason", "internallocation", "lkcoattype", "lkownerflags", 
    "lksaccounttype", "lksdiarylink", "lksdonationfreq", "lksex", "lksfieldlink", "lksfieldtype", "lksize", 
    "lksloglink", "lksmedialink", "lksmediatype", "lksmovementtype", "lksposneg", "lksyesno", "lksynun", 
    "lkurgency", "log", "logtype", "media", "medicalprofile", "messages", "onlineform", "onlineformfield", 
    "onlineformincoming", "owner", "ownerdonation", "ownerinvestigation", "ownervoucher", "role", "species", 
    "testtype", "testresult", "userrole", "users", "vaccinationtype", "voucher" )

# ASM2_COMPATIBILITY This is used for dumping tables in ASM2/HSQLDB format. 
# These are the tables present in ASM2.
TABLES_ASM2 = ( "accounts", "accountsrole", "accountstrx", "activeuser", "additional", "additionalfield",
    "adoption", "animal", "animalcost", "animaldiet", "animalfound", "animallitter", "animallost", 
    "animalmedical", "animalmedicaltreatment", "animalname", "animaltype", "animaltest", "animalvaccination", 
    "animalwaitinglist", "audittrail", "basecolour", "breed", "configuration", "costtype", 
    "customreport", "dbfs", "deathreason", "diary", "diarytaskdetail", "diarytaskhead", "diet", 
    "donationtype", "entryreason", "internallocation", "lkcoattype", "lksaccounttype", "lksdiarylink", 
    "lksdonationfreq", "lksex", "lksfieldlink", "lksfieldtype", "lksize", "lksloglink", "lksmedialink", 
    "lksmediatype", "lksmovementtype", "lksposneg", "lksyesno", "lksynun", "lkurgency", "log", 
    "logtype", "media", "medicalprofile", "owner", "ownerdonation", "ownervoucher", "primarykey", 
    "species", "users", "vaccinationtype", "voucher" )

# Tables that don't have an ID column (we don't create PostgreSQL sequences for them for pseq pk)
TABLES_NO_ID_COLUMN = ( "accountsrole", "activeuser", "additional", "audittrail", "configuration", 
    "customreportrole", "onlineformincoming", "userrole" )

VIEWS = ( "v_adoption", "v_animal", "v_animalfound", "v_animallost", "v_animalmedicaltreatment", 
    "v_animaltest", "v_animalvaccination", "v_animalwaitinglist", "v_owner", "v_ownerdonation", 
    "v_ownervoucher" )

def sql_structure(dbo):
    """
    Returns the SQL necessary to create the database for the type specified
    """
    SHORTTEXT = "VARCHAR(1024)"
    LONGTEXT = "TEXT"
    CLOB = "TEXT"
    DATETIME = "TIMESTAMP"
    INTEGER = "INTEGER"
    FLOAT = "REAL"
    if dbo.dbtype == "MYSQL":
        CLOB = "LONGTEXT"
        SHORTTEXT = "VARCHAR(255)" # MySQL max key length is 767 bytes for multi-byte charsets
        LONGTEXT = "LONGTEXT"
        DATETIME = "DATETIME"
        FLOAT = "DOUBLE"
    if dbo.dbtype == "HSQLDB":
        LONGTEXT = "VARCHAR(2000000)"
        CLOB = LONGTEXT
        FLOAT = "DOUBLE"
    def table(name, fields, includechange = True):
        createtable = "CREATE TABLE "
        if dbo.dbtype == "HSQLDB":
            createtable = "DROP TABLE %s IF EXISTS;\nCREATE MEMORY TABLE " % name
        if includechange:
            cf = (fint("RecordVersion", True),
                fstr("CreatedBy", True),
                fdate("CreatedDate", True),
                fstr("LastChangedBy", True),
                fdate("LastChangedDate", True))
            return "%s%s (%s);\n" % (createtable, name, ",".join(fields + cf))
        return "%s%s (%s);\n" % (createtable, name, ",".join(fields) )
    def index(name, table, fieldlist, unique = False):
        uniquestr = ""
        if unique: uniquestr = "UNIQUE "
        return "CREATE %sINDEX %s ON %s (%s);\n" % ( uniquestr, name, table, fieldlist)
    def field(name, ftype = INTEGER, nullable = True, pk = False):
        nullstr = "NOT NULL"
        if nullable: nullstr = "NULL"
        pkstr = ""
        if pk: pkstr = " PRIMARY KEY"
        if dbo.dbtype == "HSQLDB": name = name.upper()
        return "%s %s %s%s" % ( name, ftype, nullstr, pkstr )
    def fid():
        return field("ID", INTEGER, False, True)
    def fint(name, nullable = False):
        return field(name, INTEGER, nullable, False)
    def ffloat(name, nullable = False):
        return field(name, FLOAT, nullable, False)
    def fdate(name, nullable = False):
        return field(name, DATETIME, nullable, False)
    def fstr(name, nullable = False):
        return field(name, SHORTTEXT, nullable, False)
    def flongstr(name, nullable = True):
        return field(name, LONGTEXT, nullable, False)
    def fclob(name, nullable = True):
        return field(name, CLOB, nullable, False)

    sql = ""
    sql += table("accounts", (
        fid(),
        fstr("Code"),
        fstr("Description"),
        fint("AccountType"),
        fint("DonationTypeID") ))
    sql += index("accounts_Code", "accounts", "Code", True)
 
    sql += table("accountsrole", (
        fint("AccountID"),
        fint("RoleID"),
        fint("CanView"),
        fint("CanEdit") ))
    sql += index("accountsrole_AccountIDRoleID", "accountsrole", "AccountID, RoleID")

    sql += table("accountstrx", (
        fid(),
        fdate("TrxDate"),
        fstr("Description"),
        fint("Reconciled"),
        fint("Amount"),
        fint("SourceAccountID"),
        fint("DestinationAccountID"),
        fint("OwnerDonationID") ))
    sql += index("accountstrx_TrxDate", "accountstrx", "TrxDate")
    sql += index("accountstrx_Source", "accountstrx", "SourceAccountID")
    sql += index("accountstrx_Dest", "accountstrx", "DestinationAccountID")

    sql += table("activeuser", (
        field("UserName", SHORTTEXT, False, True),
        fdate("Since"),
        flongstr("Messages", True) ), False)

    sql += table("additionalfield", (
        fid(),
        fint("LinkType"),
        fstr("FieldName"),
        fstr("FieldLabel"),
        fstr("ToolTip"),
        flongstr("LookupValues"),
        fint("FieldType"),
        fint("DisplayIndex"),
        fint("Mandatory") ), False)
    sql += index("additionalfield_LinkType", "additionalfield", "LinkType")

    sql += table("additional", (
        fint("LinkType"),
        fint("LinkID"),
        fint("AdditionalFieldID"),
        flongstr("Value") ), False)
    sql += index("additional_LinkTypeIDAdd", "additional", "LinkType, LinkID, AdditionalFieldID", True)
    sql += index("additional_LinkTypeID", "additional", "LinkType, LinkID")

    sql += table("adoption", (
        fid(),
        fstr("AdoptionNumber"),
        fint("AnimalID"),
        fint("OwnerID", True),
        fint("RetailerID", True),
        fint("OriginalRetailerMovementID", True),
        fdate("MovementDate", True),
        fint("MovementType"),
        fdate("ReturnDate", True),
        fint("ReturnedReasonID"),
        fstr("InsuranceNumber", True),
        flongstr("ReasonForReturn"),
        fdate("ReservationDate", True),
        fdate("ReservationCancelledDate", True),
        fint("Donation", True),
        fint("IsTrial", True),
        fint("IsPermanentFoster", True),
        fdate("TrialEndDate", True),
        flongstr("Comments") ))
    sql += index("adoption_AdoptionNumber", "adoption", "AdoptionNumber", True)
    sql += index("adoption_AnimalID", "adoption", "AnimalID")
    sql += index("adoption_CreatedBy", "adoption", "CreatedBy")
    sql += index("adoption_IsPermanentFoster", "adoption", "IsPermanentFoster")
    sql += index("adoption_IsTrial", "adoption", "IsTrial")
    sql += index("adoption_OwnerID", "adoption", "OwnerID")
    sql += index("adoption_RetailerID", "adoption", "RetailerID")
    sql += index("adoption_MovementDate", "adoption", "MovementDate")
    sql += index("adoption_MovementType", "adoption", "MovementType")
    sql += index("adoption_ReservationDate", "adoption", "ReservationDate")
    sql += index("adoption_ReservationCancelledDate", "adoption", "ReservationCancelledDate")
    sql += index("adoption_ReturnDate", "adoption", "ReturnDate")
    sql += index("adoption_ReturnedReasonID", "adoption", "ReturnedReasonID")
    sql += index("adoption_TrialEndDate", "adoption", "TrialEndDate")

    sql += table("animal", (
        fid(),
        fint("AnimalTypeID"),
        fstr("AnimalName"),
        fint("NonShelterAnimal"),
        fint("CrueltyCase"),
        fint("BondedAnimalID"),
        fint("BondedAnimal2ID"),
        fint("BaseColourID"),
        fint("SpeciesID"),
        fint("BreedID"),
        fint("Breed2ID"),
        fstr("BreedName", True),
        fint("CrossBreed"),
        fint("CoatType"),
        flongstr("Markings"),
        fstr("ShelterCode"),
        fstr("ShortCode"),
        fint("UniqueCodeID"),
        fint("YearCodeID"),
        fstr("AcceptanceNumber"),
        fdate("DateOfBirth"),
        fint("EstimatedDOB"),
        fstr("AgeGroup", True),
        fdate("DeceasedDate", True),
        fint("Sex"),
        fint("Identichipped"),
        fstr("IdentichipNumber"),
        fdate("IdentichipDate", True),
        fint("Tattoo"),
        fstr("TattooNumber"),
        fdate("TattooDate", True),
        fint("SmartTag"),
        fstr("SmartTagNumber", True),
        fdate("SmartTagDate", True),
        fdate("SmartTagSentDate", True),
        fint("SmartTagType"),
        fdate("PetLinkSentDate", True),
        fint("Neutered"),
        fdate("NeuteredDate", True),
        fint("CombiTested"),
        fdate("CombiTestDate", True),
        fint("CombiTestResult"),
        fint("HeartwormTested"),
        fdate("HeartwormTestDate", True),
        fint("HeartwormTestResult"),
        fint("FLVResult"),
        fint("Declawed"),
        flongstr("HiddenAnimalDetails"),
        flongstr("AnimalComments"),
        fint("OwnersVetID"),
        fint("CurrentVetID"),
        fint("OriginalOwnerID"),
        fint("BroughtInByOwnerID"),
        flongstr("ReasonForEntry"),
        flongstr("ReasonNO"),
        fdate("DateBroughtIn"),
        fint("EntryReasonID"),
        fint("AsilomarIsTransferExternal", True),
        fint("AsilomarIntakeCategory", True),
        fint("AsilomarOwnerRequestedEuthanasia", True),
        flongstr("HealthProblems"),
        fint("PutToSleep"),
        flongstr("PTSReason"),
        fint("PTSReasonID"),
        fint("IsDOA"),
        fint("IsTransfer"),
        fint("IsGoodWithCats"),
        fint("IsGoodWithDogs"),
        fint("IsGoodWithChildren"),
        fint("IsHouseTrained"),
        fint("IsNotAvailableForAdoption"),
        fint("IsHold", True),
        fdate("HoldUntilDate", True),
        fint("IsQuarantine", True),
        fint("HasSpecialNeeds"),
        fint("ShelterLocation"),
        fstr("ShelterLocationUnit", True),
        fint("DiedOffShelter"),
        fint("Size"),
        fstr("RabiesTag", True),
        fint("Archived"),
        fint("ActiveMovementID"),
        fint("ActiveMovementType", True),
        fdate("ActiveMovementDate", True),
        fdate("ActiveMovementReturn", True),
        fint("HasActiveReserve", True),
        fint("HasTrialAdoption", True),
        fint("HasPermanentFoster", True),
        fstr("DisplayLocation", True),
        fdate("MostRecentEntryDate"),
        fstr("TimeOnShelter", True),
        fint("DaysOnShelter", True),
        fint("DailyBoardingCost", True),
        fstr("AnimalAge", True) ))
    sql += index("animal_AnimalShelterCode", "animal", "ShelterCode", True)
    sql += index("animal_AnimalTypeID", "animal", "AnimalTypeID")
    sql += index("animal_AnimalName", "animal", "AnimalName")
    sql += index("animal_AnimalSpecies", "animal", "SpeciesID")
    sql += index("animal_Archived", "animal", "Archived")
    sql += index("animal_ActiveMovementID", "animal", "ActiveMovementID")
    sql += index("animal_ActiveMovementDate", "animal", "ActiveMovementDate")
    sql += index("animal_ActiveMovementReturn", "animal", "ActiveMovementReturn")
    sql += index("animal_AcceptanceNumber", "animal", "AcceptanceNumber")
    sql += index("animal_ActiveMovementType", "animal", "ActiveMovementType")
    sql += index("animal_AgeGroup", "animal", "AgeGroup")
    sql += index("animal_BaseColourID", "animal", "BaseColourID")
    sql += index("animal_BondedAnimalID", "animal", "BondedAnimalID")
    sql += index("animal_BondedAnimal2ID", "animal", "BondedAnimal2ID")
    sql += index("animal_BreedID", "animal", "BreedID")
    sql += index("animal_Breed2ID", "animal", "Breed2ID")
    sql += index("animal_BreedName", "animal", "BreedName")
    sql += index("animal_BroughtInByOwnerID", "animal", "BroughtInByOwnerID")
    sql += index("animal_CoatType", "animal", "CoatType")
    sql += index("animal_CurrentVetID", "animal", "CurrentVetID")
    sql += index("animal_DateBroughtIn", "animal", "DateBroughtIn")
    sql += index("animal_DeceasedDate", "animal", "DeceasedDate")
    sql += index("animal_EntryReasonID", "animal", "EntryReasonID")
    sql += index("animal_IdentichipNumber", "animal", "IdentichipNumber")
    sql += index("animal_MostRecentEntryDate", "animal", "MostRecentEntryDate")
    sql += index("animal_OriginalOwnerID", "animal", "OriginalOwnerID")
    sql += index("animal_OwnersVetID", "animal", "OwnersVetID")
    sql += index("animal_PutToSleep", "animal", "PutToSleep")
    sql += index("animal_PTSReasonID", "animal", "PTSReasonID")
    sql += index("animal_RabiesTag", "animal", "RabiesTag")
    sql += index("animal_Sex", "animal", "Sex")
    sql += index("animal_Size", "animal", "Size")
    sql += index("animal_ShelterLocation", "animal", "ShelterLocation")
    sql += index("animal_ShelterLocationUnit", "animal", "ShelterLocationUnit")
    sql += index("animal_ShortCode", "animal", "ShortCode")
    sql += index("animal_TattooNumber", "animal", "TattooNumber")
    sql += index("animal_UniqueCodeID", "animal", "UniqueCodeID")
    sql += index("animal_YearCodeID", "animal", "YearCodeID")

    sql += table("animalcost", (
        fid(),
        fint("AnimalID"),
        fint("CostTypeID"),
        fdate("CostDate"),
        fint("CostAmount"),
        flongstr("Description", False) ))
    sql += index("animalcost_AnimalID", "animalcost", "AnimalID")
    sql += index("animalcost_CostTypeID", "animalcost", "CostTypeID")
    sql += index("animalcost_CostDate", "animalcost", "CostDate")

    sql += table("animaldiet", (
        fid(),
        fint("AnimalID"),
        fint("DietID"),
        fdate("DateStarted"),
        flongstr("Comments") ))
    sql += index("animaldiet_AnimalID", "animaldiet", "AnimalID")
    sql += index("animaldiet_DietID", "animaldiet", "DietID")

    sql += table("animalfigures", (
        fid(),
        fint("Month"),
        fint("Year"),
        fint("OrderIndex"),
        fstr("Code"),
        fint("AnimalTypeID"),
        fint("SpeciesID"),
        fint("MaxDaysInMonth"),
        fstr("Heading"),
        fint("Bold"),
        fint("D1"), fint("D2"), fint("D3"), fint("D4"), fint("D5"), fint("D6"), fint("D7"), fint("D8"),
        fint("D9"), fint("D10"), fint("D11"), fint("D12"), fint("D13"), fint("D14"), fint("D15"),
        fint("D16"), fint("D17"), fint("D18"), fint("D19"), fint("D20"), fint("D21"), fint("D22"),
        fint("D23"), fint("D24"), fint("D25"), fint("D26"), fint("D27"), fint("D28"), fint("D29"),
        fint("D30"), fint("D31"), fstr("TOTAL"), ffloat("AVERAGE")), False)
    sql += index("animalfigures_AnimalTypeID", "animalfigures", "AnimalTypeID")
    sql += index("animalfigures_SpeciesID", "animalfigures", "SpeciesID")
    sql += index("animalfigures_Month", "animalfigures", "Month")
    sql += index("animalfigures_Year", "animalfigures", "Year")

    sql += table("animalfiguresannual", (
        fid(),
        fint("Year"),
        fint("OrderIndex"),
        fstr("Code"),
        fint("AnimalTypeID"),
        fint("SpeciesID"),
        fstr("GroupHeading"),
        fstr("Heading"),
        fint("Bold"),
        fint("M1"), fint("M2"), fint("M3"), fint("M4"), fint("M5"), fint("M6"),
        fint("M7"), fint("M8"), fint("M9"), fint("M10"), fint("M11"), fint("M12"),
        fint("Total")), False)
    sql += index("animalfiguresannual_AnimalTypeID", "animalfiguresannual", "AnimalTypeID")
    sql += index("animalfiguresannual_SpeciesID", "animalfiguresannual", "SpeciesID")
    sql += index("animalfiguresannual_Year", "animalfiguresannual", "Year")

    sql += table("animalfiguresasilomar", (
        fid(),
        fint("Year"),
        fint("OrderIndex"),
        fstr("Code"),
        fstr("Heading"),
        fint("Bold"),
        fint("Cat"),
        fint("Dog"),
        fint("Total")), False)
    sql += index("animalfiguresasilomar_Year", "animalfiguresasilomar", "Year")

    sql += table("animalfound", (
        fid(),
        fint("AnimalTypeID"),
        fdate("DateReported"),
        fdate("DateFound"),
        fint("Sex"),
        fint("BreedID"),
        fstr("AgeGroup", True),
        fint("BaseColourID"),
        flongstr("DistFeat", False),
        fstr("AreaFound"),
        fstr("AreaPostcode"),
        fint("OwnerID"),
        fdate("ReturnToOwnerDate", True),
        flongstr("Comments") ))
    sql += index("animalfound_ReturnToOwnerDate", "animalfound", "ReturnToOwnerDate")
    sql += index("animalfound_AnimalTypeID", "animalfound", "AnimalTypeID")
    sql += index("animalfound_AreaFound", "animalfound", "AreaFound")
    sql += index("animalfound_AreaPostcode", "animalfound", "AreaPostcode")

    sql += table("animallitter", (
        fid(),
        fint("ParentAnimalID"),
        fint("SpeciesID"),
        fdate("Date"),
        fstr("AcceptanceNumber", True),
        fint("CachedAnimalsLeft"),
        fdate("InvalidDate", True),
        fint("NumberInLitter"),
        flongstr("Comments") ))

    sql += table("animallost", (
        fid(),
        fint("AnimalTypeID"),
        fdate("DateReported"),
        fdate("DateLost"),
        fdate("DateFound", True),
        fint("Sex"),
        fint("BreedID"),
        fstr("AgeGroup", True),
        fint("BaseColourID"),
        flongstr("DistFeat", False),
        fstr("AreaLost"),
        fstr("AreaPostcode"),
        fint("OwnerID"),
        flongstr("Comments") ))
    sql += index("animallost_DateFound", "animallost", "DateFound")
    sql += index("animallost_AnimalTypeID", "animallost", "AnimalTypeID")
    sql += index("animallost_AreaLost", "animallost", "AreaLost")
    sql += index("animallost_AreaPostcode", "animallost", "AreaPostcode")

    sql += table("animalmedical", (
        fid(),
        fint("AnimalID"),
        fint("MedicalProfileID"),
        fstr("TreatmentName"),
        fdate("StartDate"),
        fstr("Dosage", True),
        fint("Cost"),
        fint("TimingRule"),
        fint("TimingRuleFrequency"),
        fint("TimingRuleNoFrequencies"),
        fint("TreatmentRule"),
        fint("TotalNumberOfTreatments"),
        fint("TreatmentsGiven"),
        fint("TreatmentsRemaining"),
        fint("Status"),
        flongstr("Comments") ))
    sql += index("animalmedical_AnimalID", "animalmedical", "AnimalID")
    sql += index("animalmedical_MedicalProfileID", "animalmedical", "MedicalProfileID")

    sql += table("animalmedicaltreatment", (
        fid(),
        fint("AnimalID"),
        fint("AnimalMedicalID"),
        fdate("DateRequired"),
        fdate("DateGiven", True),
        fint("TreatmentNumber"),
        fint("TotalTreatments"),
        fstr("GivenBy"),
        flongstr("Comments") ))
    sql += index("animalmedicaltreatment_AnimalID", "animalmedicaltreatment", "AnimalID")
    sql += index("animalmedicaltreatment_AnimalMedicalID", "animalmedicaltreatment", "AnimalMedicalID")
    sql += index("animalmedicaltreatment_DateRequired", "animalmedicaltreatment", "DateRequired")

    sql += table("animalname", (
        fid(),
        fstr("Name"),
        fint("Sex") ), False)

    sql += table("animaltype", (
        fid(),
        fstr("AnimalType"),
        fstr("AnimalDescription", True) ), False)

    sql += table("animaltest", (
        fid(),
        fint("AnimalID"),
        fint("TestTypeID"),
        fint("TestResultID"),
        fdate("DateOfTest", True),
        fdate("DateRequired"),
        fint("Cost"),
        flongstr("Comments") ))
    sql += index("animaltest_AnimalID", "animaltest", "AnimalID")

    sql += table("animalvaccination", (
        fid(),
        fint("AnimalID"),
        fint("VaccinationID"),
        fdate("DateOfVaccination", True),
        fdate("DateRequired"),
        fint("Cost"),
        flongstr("Comments") ))
    sql += index("animalvaccination_AnimalID", "animalvaccination", "AnimalID")

    sql += table("animalwaitinglist", (
        fid(),
        fint("SpeciesID"),
        fdate("DatePutOnList"),
        fint("OwnerID"),
        fstr("AnimalDescription"),
        flongstr("ReasonForWantingToPart"),
        fint("CanAffordDonation"),
        fint("Urgency"),
        fdate("DateRemovedFromList", True),
        fint("AutoRemovePolicy"),
        fdate("DateOfLastOwnerContact", True),
        flongstr("ReasonForRemoval"),
        flongstr("Comments"),
        fdate("UrgencyUpdateDate", True),
        fdate("UrgencyLastUpdatedDate", True) ))
    sql += index("animalwaitinglist_AnimalDescription", "animalwaitinglist", "AnimalDescription")
    sql += index("animalwaitinglist_OwnerID", "animalwaitinglist", "OwnerID")
    sql += index("animalwaitinglist_SpeciesID", "animalwaitinglist", "SpeciesID")
    sql += index("animalwaitinglist_Urgency", "animalwaitinglist", "Urgency")
    sql += index("animalwaitinglist_DatePutOnList", "animalwaitinglist", "DatePutOnList")

    sql += table("audittrail", (
        fint("Action"),
        fdate("AuditDate"),
        fstr("UserName"),
        fstr("TableName"),
        flongstr("Description", False) ), False)
    sql += index("audittrail_Action", "audittrail", "Action")
    sql += index("audittrail_AuditDate", "audittrail", "AuditDate")
    sql += index("audittrail_UserName", "audittrail", "UserName")
    sql += index("audittrail_TableName", "audittrail", "TableName")

    sql += table("basecolour", (
        fid(),
        fstr("BaseColour"),
        fstr("BaseColourDescription", True) ), False)

    sql += table("breed", (
        fid(),
        fstr("BreedName"),
        fstr("BreedDescription", True),
        fstr("PetFinderBreed", True),
        fint("SpeciesID", True) ), False)

    sql += table("configuration", (
        fstr("ItemName"),
        flongstr("ItemValue", False) ), False)
    sql += index("configuration_ItemName", "configuration", "ItemName")

    sql += table("costtype", (
        fid(),
        fstr("CostTypeName"),
        fstr("CostTypeDescription"),
        fint("DefaultCost", True)), False)

    sql += table("customreport", (
        fid(),
        fstr("Title"),
        fstr("Category"),
        flongstr("SQLCommand", False),
        flongstr("HTMLBody", False),
        flongstr("Description"),
        fint("OmitHeaderFooter"),
        fint("OmitCriteria") ))
    sql += index("customreport_Title", "customreport", "Title")

    sql += table("customreportrole", (
        fint("ReportID"),
        fint("RoleID"),
        fint("CanView") ))
    sql += index("customreportrole_ReportIDRoleID", "customreportrole", "ReportID, RoleID")

    sql += table("dbfs", (
        fid(),
        fstr("Path"),
        fstr("Name"),
        fclob("Content", True) ), False)
    sql += index("dbfs_Path", "dbfs", "Path")
    sql += index("dbfs_Name", "dbfs", "Name")

    sql += table("deathreason", (
        fid(),
        fstr("ReasonName"),
        fstr("ReasonDescription", True) ), False)

    sql += table("diary", (
        fid(),
        fint("LinkID"),
        fint("LinkType"),
        fdate("DiaryDateTime"),
        fstr("DiaryForName"),
        flongstr("Subject"),
        flongstr("Note"),
        flongstr("Comments", True),
        fdate("DateCompleted", True),
        fstr("LinkInfo", True) ))
    sql += index("diary_DiaryForName", "diary", "DiaryForName")

    sql += table("diarytaskdetail", (
        fid(),
        fint("DiaryTaskHeadID"),
        fint("DayPivot"),
        fstr("WhoFor"),
        flongstr("Subject"),
        flongstr("Note"),
        fint("RecordVersion", True) ), False)
    sql += index("diarytaskdetail_DiaryTaskHeadID", "diarytaskdetail", "DiaryTaskHeadID")

    sql += table("diarytaskhead", (
        fid(),
        fstr("Name"),
        fint("RecordType"),
        fint("RecordVersion", True)), False)

    sql += table("diet", (
        fid(),
        fstr("DietName"),
        fstr("DietDescription", True) ), False)

    sql += table("donationtype", (
        fid(),
        fstr("DonationName"),
        fstr("DonationDescription", True),
        fint("DefaultCost", True)), False)

    sql += table("donationpayment", (
        fid(),
        fstr("PaymentName"),
        fstr("PaymentDescription", True) ), False)

    sql += table("entryreason", (
        fid(),
        fstr("ReasonName"),
        fstr("ReasonDescription", True) ), False)

    sql += table("internallocation", (
        fid(),
        fstr("LocationName"),
        fstr("LocationDescription", True) ), False)

    sql += table("lksaccounttype", (
        fid(), fstr("AccountType") ), False)

    sql += table("lkownerflags", (
        fid(), fstr("Flag") ), False)

    sql += table("lkcoattype", (
        fid(), fstr("CoatType") ), False)

    sql += table("lksex", (
        fid(), fstr("Sex") ), False)

    sql += table("lksize", (
        fid(), fstr("Size") ), False)

    sql += table("lksmovementtype", (
        fid(), fstr("MovementType") ), False)

    sql += table("lksfieldlink", (
        fid(), fstr("LinkType") ), False)

    sql += table("lksfieldtype", (
        fid(), fstr("FieldType") ), False)

    sql += table("lksmedialink", (
        fid(), fstr("LinkType") ), False)

    sql += table("lksmediatype", (
        fid(), fstr("MediaType") ), False)

    sql += table("lksdiarylink", (
        fid(), fstr("LinkType") ), False)

    sql += table("lksdonationfreq", (
        fid(), fstr("Frequency") ), False)

    sql += table("lksloglink", (
        fid(), fstr("LinkType") ), False)

    sql += table("lkurgency", ( 
        fid(), fstr("Urgency") ), False)

    sql += table("lksyesno", (
        fid(), fstr("Name") ), False)

    sql += table("lksynun", (
        fid(), fstr("Name") ), False)

    sql += table("lksposneg", (
        fid(), fstr("Name") ), False)

    sql += table("log", (
        fid(),
        fint("LogTypeID"),
        fint("LinkID"),
        fint("LinkType"),
        fdate("Date"),
        flongstr("Comments") ))
    sql += index("log_LogTypeID", "log", "LogTypeID")
    sql += index("log_LinkID", "log", "LinkID")

    sql += table("logtype", (
        fid(),
        fstr("LogTypeName"),
        fstr("LogTypeDescription", True) ), False)

    sql += table("media", (
        fid(),
        fint("MediaType", True),
        fstr("MediaName"),
        flongstr("MediaNotes"),
        fint("WebsitePhoto"),
        fint("WebsiteVideo", True),
        fint("DocPhoto"),
        fint("NewSinceLastPublish"),
        fint("UpdatedSinceLastPublish"),
        fint("ExcludeFromPublish", True),
        fdate("LastPublished", True),
        fdate("LastPublishedPF", True),
        fdate("LastPublishedAP", True),
        fdate("LastPublishedP911", True),
        fdate("LastPublishedRG", True),
        fdate("LastPublishedMP", True),
        fdate("LastPublishedHLP", True),
        fint("LinkID"),
        fint("LinkTypeID"),
        fint("RecordVersion", True),
        fdate("Date") ), False)
    sql += index("media_LinkID", "media", "LinkID")
    sql += index("media_LinkTypeID", "media", "LinkTypeID")
    sql += index("media_WebsitePhoto", "media", "WebsitePhoto")
    sql += index("media_WebsiteVideo", "media", "WebsiteVideo")
    sql += index("media_DocPhoto", "media", "DocPhoto")

    sql += table("medicalprofile", (
        fid(),
        fstr("ProfileName"),
        fstr("TreatmentName"),
        fstr("Dosage"),
        fint("Cost"),
        fint("TimingRule"),
        fint("TimingRuleFrequency"),
        fint("TimingRuleNoFrequencies"),
        fint("TreatmentRule"),
        fint("TotalNumberOfTreatments"),
        flongstr("Comments") ))

    sql += table("messages", (
        fid(),
        fdate("Added"),
        fdate("Expires"),
        fstr("CreatedBy"),
        fstr("ForName"),
        fint("Priority"),
        flongstr("Message")), False)
    sql += index("messages_Expires", "messages", "Expires")

    sql += table("onlineform", (
        fid(),
        fstr("Name"),
        fstr("RedirectUrlAfterPOST", True),
        fstr("SetOwnerFlags", True),
        flongstr("Description", True)), False)
    sql += index("onlineform_Name", "onlineform", "Name")

    sql += table("onlineformfield", (
        fid(),
        fint("OnlineFormID"),
        fstr("FieldName"),
        fint("FieldType"),
        fint("DisplayIndex", True),
        fstr("Label"),
        flongstr("Lookups", True),
        fstr("Tooltip", True)), False)
    sql += index("onlineformfield_OnlineFormID", "onlineformfield", "OnlineFormID")

    sql += table("onlineformincoming", (
        fint("CollationID"),
        fstr("FormName"),
        fdate("PostedDate"),
        fstr("Flags", True),
        fstr("FieldName"),
        fstr("Label", True),
        fstr("DisplayIndex", True),
        fstr("Host", True),
        flongstr("Preview", True),
        flongstr("Value", True)), False)
    sql += index("onlineformincoming_CollationID", "onlineformincoming", "CollationID")

    sql += table("owner", (
        fid(),
        fstr("OwnerTitle"),
        fstr("OwnerInitials"),
        fstr("OwnerForeNames"),
        fstr("OwnerSurname"),
        fstr("OwnerName"),
        fstr("OwnerAddress"),
        fstr("OwnerTown", True),
        fstr("OwnerCounty", True),
        fstr("OwnerPostcode", True),
        fstr("LatLong", True),
        fstr("HomeTelephone", True),
        fstr("WorkTelephone", True),
        fstr("MobileTelephone", True),
        fstr("EmailAddress", True),
        fint("IDCheck"),
        flongstr("Comments"),
        fint("IsBanned"),
        fint("IsVolunteer"),
        fint("IsHomeChecker"),
        fint("IsMember"),
        fdate("MembershipExpiryDate", True),
        fstr("MembershipNumber", True),
        fint("IsDonor"),
        fint("IsShelter"),
        fint("IsACO"), 
        fint("IsStaff"),
        fint("IsFosterer"),
        fint("IsRetailer"),
        fint("IsVet"),
        fint("IsGiftAid"),
        flongstr("AdditionalFlags"),
        flongstr("HomeCheckAreas"),
        fdate("DateLastHomeChecked", True),
        fint("HomeCheckedBy"),
        fdate("MatchAdded", True),
        fdate("MatchExpires", True),
        fint("MatchActive", True),
        fint("MatchSex", True),
        fint("MatchSize", True),
        fint("MatchColour", True),
        ffloat("MatchAgeFrom", True),
        ffloat("MatchAgeTo", True),
        fint("MatchAnimalType", True),
        fint("MatchSpecies", True),
        fint("MatchBreed", True),
        fint("MatchBreed2", True),
        fint("MatchGoodWithCats", True),
        fint("MatchGoodWithDogs", True),
        fint("MatchGoodWithChildren", True),
        fint("MatchHouseTrained", True),
        fstr("MatchCommentsContain", True) ))
    sql += index("owner_MembershipNumber", "owner", "MembershipNumber")
    sql += index("owner_OwnerName", "owner", "OwnerName")
    sql += index("owner_OwnerAddress", "owner", "OwnerAddress")
    sql += index("owner_OwnerCounty", "owner", "OwnerCounty")
    sql += index("owner_EmailAddress", "owner", "EmailAddress")
    sql += index("owner_OwnerForeNames", "owner", "OwnerForeNames")
    sql += index("owner_HomeTelephone", "owner", "HomeTelephone")
    sql += index("owner_MobileTelephone", "owner", "MobileTelephone")
    sql += index("owner_WorkTelephone", "owner", "WorkTelephone")
    sql += index("owner_OwnerInitials", "owner", "OwnerInitials")
    sql += index("owner_OwnerPostcode", "owner", "OwnerPostcode")
    sql += index("owner_OwnerSurname", "owner", "OwnerSurname")
    sql += index("owner_OwnerTitle", "owner", "OwnerTitle")
    sql += index("owner_OwnerTown", "owner", "OwnerTown")

    sql += table("ownerdonation", (
        fid(),
        fint("AnimalID", True),
        fint("OwnerID"),
        fint("MovementID", True),
        fint("DonationTypeID"),
        fint("DonationPaymentID", True),
        fdate("Date", True),
        fdate("DateDue", True),
        fint("Donation"),
        fint("IsGiftAid"),
        fint("Frequency"),
        fint("NextCreated", True),
        flongstr("Comments") ))
    sql += index("ownerdonation_OwnerID", "ownerdonation", "OwnerID")
    sql += index("ownerdonation_Date", "ownerdonation", "Date")

    sql += table("ownerinvestigation", (
        fid(),
        fint("OwnerID"),
        fdate("Date"),
        flongstr("Notes") ))
    sql += index("ownerinvestigation_OwnerID", "ownerinvestigation", "OwnerID")

    sql += table("ownervoucher", (
        fid(),
        fint("OwnerID"),
        fint("VoucherID"),
        fdate("DateIssued"),
        fdate("DateExpired"),
        fint("Value"),
        flongstr("Comments", True) ))
    sql += index("ownervoucher_OwnerID", "ownervoucher", "OwnerID")
    sql += index("ownervoucher_VoucherID", "ownervoucher", "VoucherID")
    sql += index("ownervoucher_DateExpired", "ownervoucher", "DateExpired")

    sql += table("primarykey", (
        fstr("TableName"),
        fint("NextID") ), False)
    sql += index("primarykey_TableName", "primarykey", "TableName")

    sql += table("role", (
        fid(),
        fstr("Rolename"),
        flongstr("SecurityMap")), False)
    sql += index("role_Rolename", "role", "Rolename")

    sql += table("species", (
        fid(),
        fstr("SpeciesName"),
        fstr("SpeciesDescription", True),
        fstr("PetFinderSpecies", True)
        ), False)

    sql += table("testtype", (
        fid(),
        fstr("TestName"),
        fstr("TestDescription", True),
        fint("DefaultCost", True) ), False)

    sql += table("testresult", (
        fid(),
        fstr("ResultName"),
        fstr("ResultDescription", True)
        ), False)

    sql += table("users", (
        fid(),
        fstr("UserName"),
        fstr("RealName", True),
        fstr("EmailAddress", True),
        fstr("Password"),
        fint("SuperUser"),
        fint("OwnerID", True),
        flongstr("SecurityMap", True),
        flongstr("IPRestriction", True),
        fstr("LocaleOverride", True),
        fstr("ThemeOverride", True),
        fstr("LocationFilter", True),
        fint("RecordVersion", True)), False)
    sql += index("users_UserName", "users", "UserName")

    sql += table("userrole", (
        fint("UserID"),
        fint("RoleID")), False)
    sql += index("userrole_UserIDRoleID", "userrole", "UserID, RoleID", True)

    sql += table("voucher", (
        fid(),
        fstr("VoucherName"),
        fstr("VoucherDescription", True),
        fint("DefaultCost", True)), False)

    sql += table("vaccinationtype", (
        fid(),
        fstr("VaccinationType"),
        fstr("VaccinationDescription", True),
        fint("DefaultCost", True) ), False)
    return sql

def sql_default_data(dbo, skip_config = False):
    """
    Returns the SQL for the default data set
    """
    def config(key, value):
        return "INSERT INTO configuration VALUES ('%s', '%s')|=\n" % ( db.escape(key), db.escape(value) )
    def lookup1(tablename, tid, name):
        return "INSERT INTO %s VALUES (%s, '%s')|=\n" % ( tablename, str(tid), db.escape(name) )
    def lookup2(tablename, tid, name):
        return "INSERT INTO %s VALUES (%s, '%s', '%s')|=\n" % ( tablename, str(tid), db.escape(name), "")
    def lookup2money(tablename, tid, name, money = 0):
        return "INSERT INTO %s VALUES (%s, '%s', '%s', %d)|=\n" % ( tablename, str(tid), db.escape(name), "", money)
    def account(tid, code, desc, atype, dtype):
        return "INSERT INTO accounts VALUES (%s, '%s', '%s', %s, %s, 0, '%s', %s, '%s', %s)|=\n" % ( str(tid), db.escape(code), db.escape(desc), str(atype), str(dtype), 'default', db.todaysql(), 'default', db.todaysql())
    def breed(tid, name, petfinder, speciesid):
        return "INSERT INTO breed VALUES (%s, '%s', '', '%s', %s)|=\n" % ( str(tid), db.escape(name), petfinder, str(speciesid) )
    def species(tid, name, petfinder):
        return "INSERT INTO species VALUES (%s, '%s', '', '%s')|=\n" % ( str(tid), db.escape(name), petfinder )

    l = dbo.locale
    sql = ""
    if not skip_config:
        sql += "INSERT INTO users VALUES (1,'user','Default system user', '', 'd107d09f5bbe40cade3de5c71e9e9b7', 1, 0,'', '', '', '', '', 0)|=\n"
        sql += "INSERT INTO users VALUES (2,'guest','Default guest user', '', '84e0343a0486ff05530df6c705c8bb4', 0, 0,'', '', '', '', '', 0)|=\n"
        sql += "INSERT INTO role VALUES (1, '" + _("Other Organisation", l) + "', 'vac *va *vavet *vav *mvam *dvad *cvad *vamv *vo *volk *vle *vvov *vdn *vla *vfa *vwl *vcr *vll *')|=\n"
        sql += "INSERT INTO role VALUES (2, '" + _("Staff", l) + "', 'aa *ca *va *vavet *da *cloa *gaf *aam *cam *dam *vam *mand *aav *vav *cav *dav *bcav *maam *mcam *mdam *mvam *bcam *daad *dcad *ddad *dvad *caad *cdad *cvad *aamv *camv *vamv *damv *ao *co *vo *do *mo *volk *ale *cle *dle *vle *vaov *vcov *vvov *oaod *ocod *odod *ovod *vdn *edt *adn *eadn *emdn *ecdn *bcn *ddn *pdn *pvd *ala *cla *dla *vla *afa *cfa *dfa *vfa *mlaf *vwl *awl *cwl *dwl *bcwl *all *cll *vll *dll *vcr *')|=\n"
        sql += "INSERT INTO role VALUES (3, '" + _("Accountant", l) + "', 'aac *vac *cac *ctrx *dac *vaov *vcov *vdov *vvov *oaod *ocod *odod *ovod *')|=\n"
        sql += "INSERT INTO role VALUES (4, '" + _("Vet", l) + "', 'va *vavet *aav *vav *cav *dav *bcav *maam *mcam *mdam *mvam *bcam *daad *dcad *ddad *dvad * ')|=\n"
        sql += "INSERT INTO role VALUES (5, '" + _("Publisher", l) + "', 'uipb *')|=\n"
        sql += "INSERT INTO role VALUES (6, '" + _("System Admin", l) + "', 'asm *cso *ml *usi *rdbu *rdbd *asu *esu *ccr *vcr *hcr *dcr *')|=\n"
        sql += "INSERT INTO role VALUES (7, '" + _("Marketer", l) + "', 'uipb *mmeo *mmea *')|=\n"
        sql += "INSERT INTO role VALUES (8, '" + _("Investigator", l) + "', 'aoi *coi *doi *voi *')|=\n"
        sql += "INSERT INTO userrole VALUES (2, 1)|=\n"
        sql += config("DBV", str(LATEST_VERSION))
        sql += config("DatabaseVersion", str(LATEST_VERSION))
        sql += config("Organisation", _("Organisation", l))
        sql += config("OrganisationAddress", _("Address", l))
        sql += config("OrganisationTelephone", _("Telephone", l))
        sql += config("CodingFormat", "TYYYYNNN")
        sql += config("ShortCodingFormat", "NNNT")
        sql += config("UseShortShelterCodes", "Yes")
        sql += config("AutoDefaultShelterCode", "Yes")
        sql += config("IncomingMediaScaling", "640x640")
        sql += config("MaxMediaFileSize", "1000")
        sql += config("RecordSearchLimit", "1000")
        sql += config("SearchSort", "3")
        sql += config("AgeGroup1", "0.5")
        sql += config("AgeGroup1Name", _("Baby", l))
        sql += config("AgeGroup2", "2")
        sql += config("AgeGroup2Name", _("Young Adult", l))
        sql += config("AgeGroup3", "7")
        sql += config("AgeGroup3Name", _("Adult", l))
        sql += config("AgeGroup4", "50")
        sql += config("AgeGroup4Name", _("Senior", l))
    sql += account(1, _("Income::Donation", l), _("Incoming donations (misc)", l), 5, 1)
    sql += account(2, _("Income::Adoption", l), _("Adoption fee donations", l), 5, 2)
    sql += account(3, _("Income::WaitingList", l), _("Waiting list donations", l), 5, 3)
    sql += account(4, _("Income::EntryDonation", l), _("Donations for animals entering the shelter", l), 5, 4)
    sql += account(5, _("Income::Sponsorship", l), _("Sponsorship donations", l), 5, 5)
    sql += account(6, _("Income::Shop", l), _("Income from an on-site shop", l), 5, 0)
    sql += account(7, _("Income::Interest", l), _("Bank account interest", l), 5, 0)
    sql += account(8, _("Income::OpeningBalances", l), _("Opening balances", l), 5, 0)
    sql += account(9, _("Bank::Current", l), _("Bank current account", l), 1, 0)
    sql += account(10, _("Bank::Deposit", l), _("Bank deposit account", l), 1, 0)
    sql += account(11, _("Bank::Savings", l), _("Bank savings account", l), 1, 0)
    sql += account(12, _("Asset::Premises", l), _("Premises", l), 8, 0)
    sql += account(13, _("Expenses::Phone", l), _("Telephone Bills", l), 4, 0)
    sql += account(14, _("Expenses::Electricity", l), _("Electricity Bills", l), 4, 0)
    sql += account(15, _("Expenses::Water", l), _("Water Bills", l), 4, 0)
    sql += account(16, _("Expenses::Gas", l), _("Gas Bills", l), 4, 0)
    sql += account(17, _("Expenses::Postage", l), _("Postage costs", l), 4, 0)
    sql += account(18, _("Expenses::Stationary", l), _("Stationary costs", l), 4, 0)
    sql += account(19, _("Expenses::Food", l), _("Animal food costs"), 4, 0)
    sql += lookup2("animaltype", 2, _("D (Dog)", l))
    sql += lookup2("animaltype", 10, _("F (Stray Dog)", l))
    sql += lookup2("animaltype", 11, _("U (Unwanted Cat)", l))
    sql += lookup2("animaltype", 12, _("S (Stray Cat)", l))
    sql += lookup2("animaltype", 13, _("M (Miscellaneous)", l))
    sql += lookup2("animaltype", 40, _("N (Non Shelter Animal)", l))
    sql += lookup2("basecolour", 1, _("Black", l))
    sql += lookup2("basecolour", 2, _("White", l))
    sql += lookup2("basecolour", 3, _("Black and White", l))
    sql += lookup2("basecolour", 4, _("Ginger", l))
    sql += lookup2("basecolour", 5, _("White and Black", l))
    sql += lookup2("basecolour", 6, _("Tortie", l))
    sql += lookup2("basecolour", 7, _("Tabby", l))
    sql += lookup2("basecolour", 8, _("Tan", l))
    sql += lookup2("basecolour", 9, _("Black and Tan", l))
    sql += lookup2("basecolour", 10, _("Tan and Black", l))
    sql += lookup2("basecolour", 11, _("Brown", l))
    sql += lookup2("basecolour", 12, _("Brown and Black", l))
    sql += lookup2("basecolour", 13, _("Black and Brown", l))
    sql += lookup2("basecolour", 14, _("Brindle", l))
    sql += lookup2("basecolour", 15, _("Brindle and Black", l))
    sql += lookup2("basecolour", 16, _("Brindle and White", l))
    sql += lookup2("basecolour", 17, _("Black and Brindle", l))
    sql += lookup2("basecolour", 18, _("White and Brindle", l))
    sql += lookup2("basecolour", 19, _("Tricolour", l))
    sql += lookup2("basecolour", 20, _("Liver", l))
    sql += lookup2("basecolour", 21, _("Liver and White", l))
    sql += lookup2("basecolour", 22, _("White and Liver", l))
    sql += lookup2("basecolour", 23, _("Cream", l))
    sql += lookup2("basecolour", 24, _("Tan and White", l))
    sql += lookup2("basecolour", 26, _("White and Tan", l))
    sql += lookup2("basecolour", 27, _("Tortie and White", l))
    sql += lookup2("basecolour", 28, _("Tabby and White", l))
    sql += lookup2("basecolour", 29, _("Ginger and White", l))
    sql += lookup2("basecolour", 30, _("Grey", l))
    sql += lookup2("basecolour", 31, _("Grey and White", l))
    sql += lookup2("basecolour", 32, _("White and Grey", l))
    sql += lookup2("basecolour", 33, _("White and Torti", l))
    sql += lookup2("basecolour", 35, _("Brown and White", l))
    sql += lookup2("basecolour", 36, _("Blue", l))
    sql += lookup2("basecolour", 37, _("White and Tabby", l))
    sql += lookup2("basecolour", 38, _("Yellow and Grey", l))
    sql += lookup2("basecolour", 39, _("Various", l))
    sql += lookup2("basecolour", 40, _("White and Brown", l))
    sql += lookup2("basecolour", 41, _("Green", l))
    sql += lookup2("basecolour", 42, _("Amber", l))
    sql += lookup2("basecolour", 43, _("Black Tortie", l))
    sql += lookup2("basecolour", 44, _("Blue Tortie", l))
    sql += lookup2("basecolour", 45, _("Chocolate", l))
    sql += lookup2("basecolour", 46, _("Chocolate Tortie", l))
    sql += lookup2("basecolour", 47, _("Cinnamon", l))
    sql += lookup2("basecolour", 48, _("Cinnamon Tortoiseshell", l))
    sql += lookup2("basecolour", 49, _("Fawn", l))
    sql += lookup2("basecolour", 50, _("Fawn Tortoiseshell", l))
    sql += lookup2("basecolour", 51, _("Golden", l))
    sql += lookup2("basecolour", 52, _("Light Amber", l))
    sql += lookup2("basecolour", 53, _("Lilac", l))
    sql += lookup2("basecolour", 54, _("Lilac Tortie", l))
    sql += lookup2("basecolour", 55, _("Ruddy", l))
    sql += lookup2("basecolour", 56, _("Seal", l))
    sql += lookup2("basecolour", 57, _("Silver", l))
    sql += lookup2("basecolour", 58, _("Sorrel", l))
    sql += lookup2("basecolour", 59, _("Sorrel Tortoiseshell", l))
    sql += breed(1, _("Affenpinscher", l), "Affenpinscher", 1)
    sql += breed(2, _("Afghan Hound", l), "Afghan Hound", 1)
    sql += breed(3, _("Airedale Terrier", l), "Airedale Terrier", 1)
    sql += breed(4, _("Akbash", l), "Akbash", 1)
    sql += breed(5, _("Akita", l), "Akita", 1)
    sql += breed(6, _("Alaskan Malamute", l), "Alaskan Malamute", 1)
    sql += breed(7, _("American Bulldog", l), "American Bulldog", 1)
    sql += breed(8, _("American Eskimo Dog", l), "American Eskimo Dog", 1)
    sql += breed(9, _("American Staffordshire Terrier", l), "American Staffordshire Terrier", 1)
    sql += breed(10, _("American Water Spaniel", l), "American Water Spaniel", 1)
    sql += breed(11, _("Anatolian Shepherd", l), "Anatolian Shepherd", 1)
    sql += breed(12, _("Appenzell Mountain Dog", l), "Appenzell Mountain Dog", 1)
    sql += breed(13, _("Australian Cattle Dog/Blue Heeler", l), "Australian Cattle Dog/Blue Heeler", 1)
    sql += breed(14, _("Australian Kelpie", l), "Australian Kelpie", 1)
    sql += breed(15, _("Australian Shepherd", l), "Australian Shepherd", 1)
    sql += breed(16, _("Australian Terrier", l), "Australian Terrier", 1)
    sql += breed(17, _("Basenji", l), "Basenji", 1)
    sql += breed(18, _("Basset Hound", l), "Basset Hound", 1)
    sql += breed(19, _("Beagle", l), "Beagle", 1)
    sql += breed(20, _("Bearded Collie", l), "Bearded Collie", 1)
    sql += breed(21, _("Beauceron", l), "Beauceron", 1)
    sql += breed(22, _("Bedlington Terrier", l), "Bedlington Terrier", 1)
    sql += breed(23, _("Belgian Shepherd Dog Sheepdog", l), "Belgian Shepherd Dog Sheepdog", 1)
    sql += breed(24, _("Belgian Shepherd Laekenois", l), "Belgian Shepherd Laekenois", 1)
    sql += breed(25, _("Belgian Shepherd Malinois", l), "Belgian Shepherd Malinois", 1)
    sql += breed(26, _("Belgian Shepherd Tervuren", l), "Belgian Shepherd Tervuren", 1)
    sql += breed(27, _("Bernese Mountain Dog", l), "Bernese Mountain Dog", 1)
    sql += breed(28, _("Bichon Frise", l), "Bichon Frise", 1)
    sql += breed(29, _("Black and Tan Coonhound", l), "Black and Tan Coonhound", 1)
    sql += breed(30, _("Black Labrador Retriever", l), "Black Labrador Retriever", 1)
    sql += breed(31, _("Black Mouth Cur", l), "Black Mouth Cur", 1)
    sql += breed(32, _("Bloodhound", l), "Bloodhound", 1)
    sql += breed(33, _("Bluetick Coonhound", l), "Bluetick Coonhound", 1)
    sql += breed(34, _("Border Collie", l), "Border Collie", 1)
    sql += breed(35, _("Border Terrier", l), "Border Terrier", 1)
    sql += breed(36, _("Borzoi", l), "Borzoi", 1)
    sql += breed(37, _("Boston Terrier", l), "Boston Terrier", 1)
    sql += breed(38, _("Bouvier des Flanders", l), "Bouvier des Flanders", 1)
    sql += breed(39, _("Boykin Spaniel", l), "Boykin Spaniel", 1)
    sql += breed(40, _("Boxer", l), "Boxer", 1)
    sql += breed(41, _("Briard", l), "Briard", 1)
    sql += breed(42, _("Brittany Spaniel", l), "Brittany Spaniel", 1)
    sql += breed(43, _("Brussels Griffon", l), "Brussels Griffon", 1)
    sql += breed(44, _("Bull Terrier", l), "Bull Terrier", 1)
    sql += breed(45, _("Bullmastiff", l), "Bullmastiff", 1)
    sql += breed(46, _("Cairn Terrier", l), "Cairn Terrier", 1)
    sql += breed(47, _("Canaan Dog", l), "Canaan Dog", 1)
    sql += breed(48, _("Cane Corso Mastiff", l), "Cane Corso Mastiff", 1)
    sql += breed(49, _("Carolina Dog", l), "Carolina Dog", 1)
    sql += breed(50, _("Catahoula Leopard Dog", l), "Catahoula Leopard Dog", 1)
    sql += breed(51, _("Cattle Dog", l), "Cattle Dog", 1)
    sql += breed(52, _("Cavalier King Charles Spaniel", l), "Cavalier King Charles Spaniel", 1)
    sql += breed(53, _("Chesapeake Bay Retriever", l), "Chesapeake Bay Retriever", 1)
    sql += breed(54, _("Chihuahua", l), "Chihuahua", 1)
    sql += breed(55, _("Chinese Crested Dog", l), "Chinese Crested Dog", 1)
    sql += breed(56, _("Chinese Foo Dog", l), "Chinese Foo Dog", 1)
    sql += breed(57, _("Chocolate Labrador Retriever", l), "Chocolate Labrador Retriever", 1)
    sql += breed(58, _("Chow Chow", l), "Chow Chow", 1)
    sql += breed(59, _("Clumber Spaniel", l), "Clumber Spaniel", 1)
    sql += breed(60, _("Cockapoo", l), "Cockapoo", 1)
    sql += breed(61, _("Cocker Spaniel", l), "Cocker Spaniel", 1)
    sql += breed(62, _("Collie", l), "Collie", 1)
    sql += breed(63, _("Coonhound", l), "Coonhound", 1)
    sql += breed(64, _("Corgi", l), "Corgi", 1)
    sql += breed(65, _("Coton de Tulear", l), "Coton de Tulear", 1)
    sql += breed(66, _("Dachshund", l), "Dachshund", 1)
    sql += breed(67, _("Dalmatian", l), "Dalmatian", 1)
    sql += breed(68, _("Dandi Dinmont Terrier", l), "Dandi Dinmont Terrier", 1)
    sql += breed(69, _("Doberman Pinscher", l), "Doberman Pinscher", 1)
    sql += breed(70, _("Dogo Argentino", l), "Dogo Argentino", 1)
    sql += breed(71, _("Dogue de Bordeaux", l), "Dogue de Bordeaux", 1)
    sql += breed(72, _("Dutch Shepherd", l), "Dutch Shepherd", 1)
    sql += breed(73, _("English Bulldog", l), "English Bulldog", 1)
    sql += breed(74, _("English Cocker Spaniel", l), "English Cocker Spaniel", 1)
    sql += breed(75, _("English Coonhound", l), "English Coonhound", 1)
    sql += breed(76, _("English Pointer", l), "English Pointer", 1)
    sql += breed(77, _("English Setter", l), "English Setter", 1)
    sql += breed(78, _("English Shepherd", l), "English Shepherd", 1)
    sql += breed(79, _("English Springer Spaniel", l), "English Springer Spaniel", 1)
    sql += breed(80, _("English Toy Spaniel", l), "English Toy Spaniel", 1)
    sql += breed(81, _("Entlebucher", l), "Entlebucher", 1)
    sql += breed(82, _("Eskimo Dog", l), "Eskimo Dog", 1)
    sql += breed(83, _("Field Spaniel", l), "Field Spaniel", 1)
    sql += breed(84, _("Fila Brasileiro", l), "Fila Brasileiro", 1)
    sql += breed(85, _("Finnish Lapphund", l), "Finnish Lapphund", 1)
    sql += breed(86, _("Finnish Spitz", l), "Finnish Spitz", 1)
    sql += breed(87, _("Flat-coated Retriever", l), "Flat-coated Retriever", 1)
    sql += breed(88, _("Fox Terrier", l), "Fox Terrier", 1)
    sql += breed(89, _("Foxhound", l), "Foxhound", 1)
    sql += breed(90, _("French Bulldog", l), "French Bulldog", 1)
    sql += breed(91, _("German Pinscher", l), "German Pinscher", 1)
    sql += breed(92, _("German Shepherd Dog", l), "German Shepherd Dog", 1)
    sql += breed(93, _("German Shorthaired Pointer", l), "German Shorthaired Pointer", 1)
    sql += breed(94, _("German Wirehaired Pointer", l), "German Wirehaired Pointer", 1)
    sql += breed(95, _("Glen of Imaal Terrier", l), "Glen of Imaal Terrier", 1)
    sql += breed(96, _("Golden Retriever", l), "Golden Retriever", 1)
    sql += breed(97, _("Gordon Setter", l), "Gordon Setter", 1)
    sql += breed(98, _("Great Dane", l), "Great Dane", 1)
    sql += breed(99, _("Great Pyrenees", l), "Great Pyrenees", 1)
    sql += breed(100, _("Greater Swiss Mountain Dog", l), "Greater Swiss Mountain Dog", 1)
    sql += breed(101, _("Greyhound", l), "Greyhound", 1)
    sql += breed(102, _("Havanese", l), "Havanese", 1)
    sql += breed(103, _("Hound", l), "Hound", 1)
    sql += breed(104, _("Hovawart", l), "Hovawart", 1)
    sql += breed(105, _("Husky", l), "Husky", 1)
    sql += breed(106, _("Ibizan Hound", l), "Ibizan Hound", 1)
    sql += breed(107, _("Illyrian Sheepdog", l), "Illyrian Sheepdog", 1)
    sql += breed(108, _("Irish Setter", l), "Irish Setter", 1)
    sql += breed(109, _("Irish Terrier", l), "Irish Terrier", 1)
    sql += breed(110, _("Irish Water Spaniel", l), "Irish Water Spaniel", 1)
    sql += breed(111, _("Irish Wolfhound", l), "Irish Wolfhound", 1)
    sql += breed(112, _("Italian Greyhound", l), "Italian Greyhound", 1)
    sql += breed(113, _("Italian Spinone", l), "Italian Spinone", 1)
    sql += breed(114, _("Jack Russell Terrier", l), "Jack Russell Terrier", 1)
    sql += breed(115, _("Japanese Chin", l), "Japanese Chin", 1)
    sql += breed(116, _("Jindo", l), "Jindo", 1)
    sql += breed(117, _("Kai Dog", l), "Kai Dog", 1)
    sql += breed(118, _("Karelian Bear Dog", l), "Karelian Bear Dog", 1)
    sql += breed(119, _("Keeshond", l), "Keeshond", 1)
    sql += breed(120, _("Kerry Blue Terrier", l), "Kerry Blue Terrier", 1)
    sql += breed(121, _("Kishu", l), "Kishu", 1)
    sql += breed(122, _("Komondor", l), "Komondor", 1)
    sql += breed(123, _("Kuvasz", l), "Kuvasz", 1)
    sql += breed(124, _("Kyi Leo", l), "Kyi Leo", 1)
    sql += breed(125, _("Labrador Retriever", l), "Labrador Retriever", 1)
    sql += breed(126, _("Lakeland Terrier", l), "Lakeland Terrier", 1)
    sql += breed(127, _("Lancashire Heeler", l), "Lancashire Heeler", 1)
    sql += breed(128, _("Lhasa Apso", l), "Lhasa Apso", 1)
    sql += breed(129, _("Leonberger", l), "Leonberger", 1)
    sql += breed(130, _("Lowchen", l), "Lowchen", 1)
    sql += breed(131, _("Maltese", l), "Maltese", 1)
    sql += breed(132, _("Manchester Terrier", l), "Manchester Terrier", 1)
    sql += breed(133, _("Maremma Sheepdog", l), "Maremma Sheepdog", 1)
    sql += breed(134, _("Mastiff", l), "Mastiff", 1)
    sql += breed(135, _("McNab", l), "McNab", 1)
    sql += breed(136, _("Miniature Pinscher", l), "Miniature Pinscher", 1)
    sql += breed(137, _("Mountain Cur", l), "Mountain Cur", 1)
    sql += breed(138, _("Mountain Dog", l), "Mountain Dog", 1)
    sql += breed(139, _("Munsterlander", l), "Munsterlander", 1)
    sql += breed(140, _("Neapolitan Mastiff", l), "Neapolitan Mastiff", 1)
    sql += breed(141, _("New Guinea Singing Dog", l), "New Guinea Singing Dog", 1)
    sql += breed(142, _("Newfoundland Dog", l), "Newfoundland Dog", 1)
    sql += breed(143, _("Norfolk Terrier", l), "Norfolk Terrier", 1)
    sql += breed(144, _("Norwich Terrier", l), "Norwich Terrier", 1)
    sql += breed(145, _("Norwegian Buhund", l), "Norwegian Buhund", 1)
    sql += breed(146, _("Norwegian Elkhound", l), "Norwegian Elkhound", 1)
    sql += breed(147, _("Norwegian Lundehund", l), "Norwegian Lundehund", 1)
    sql += breed(148, _("Nova Scotia Duck-Tolling Retriever", l), "Nova Scotia Duck-Tolling Retriever", 1)
    sql += breed(149, _("Old English Sheepdog", l), "Old English Sheepdog", 1)
    sql += breed(150, _("Otterhound", l), "Otterhound", 1)
    sql += breed(151, _("Papillon", l), "Papillon", 1)
    sql += breed(152, _("Patterdale Terrier (Fell Terrier)", l), "Patterdale Terrier (Fell Terrier)", 1)
    sql += breed(153, _("Pekingese", l), "Pekingese", 1)
    sql += breed(154, _("Peruvian Inca Orchid", l), "Peruvian Inca Orchid", 1)
    sql += breed(155, _("Petit Basset Griffon Vendeen", l), "Petit Basset Griffon Vendeen", 1)
    sql += breed(156, _("Pharaoh Hound", l), "Pharaoh Hound", 1)
    sql += breed(157, _("Pit Bull Terrier", l), "Pit Bull Terrier", 1)
    sql += breed(158, _("Plott Hound", l), "Plott Hound", 1)
    sql += breed(159, _("Portugese Podengo", l), "Podengo Portugueso", 1)
    sql += breed(160, _("Pointer", l), "Pointer", 1)
    sql += breed(161, _("Polish Lowland Sheepdog", l), "Polish Lowland Sheepdog", 1)
    sql += breed(162, _("Pomeranian", l), "Pomeranian", 1)
    sql += breed(163, _("Poodle", l), "Poodle", 1)
    sql += breed(164, _("Portuguese Water Dog", l), "Portuguese Water Dog", 1)
    sql += breed(165, _("Presa Canario", l), "Presa Canario", 1)
    sql += breed(166, _("Pug", l), "Pug", 1)
    sql += breed(167, _("Puli", l), "Puli", 1)
    sql += breed(168, _("Pumi", l), "Pumi", 1)
    sql += breed(169, _("Rat Terrier", l), "Rat Terrier", 1)
    sql += breed(170, _("Redbone Coonhound", l), "Redbone Coonhound", 1)
    sql += breed(171, _("Retriever", l), "Retriever", 1)
    sql += breed(172, _("Rhodesian Ridgeback", l), "Rhodesian Ridgeback", 1)
    sql += breed(173, _("Rottweiler", l), "Rottweiler", 1)
    sql += breed(174, _("Saluki", l), "Saluki", 1)
    sql += breed(175, _("Saint Bernard St. Bernard", l), "Saint Bernard St. Bernard", 1)
    sql += breed(176, _("Samoyed", l), "Samoyed", 1)
    sql += breed(177, _("Schipperke", l), "Schipperke", 1)
    sql += breed(178, _("Schnauzer", l), "Schnauzer", 1)
    sql += breed(179, _("Scottish Deerhound", l), "Scottish Deerhound", 1)
    sql += breed(180, _("Scottish Terrier Scottie", l), "Scottish Terrier Scottie", 1)
    sql += breed(181, _("Sealyham Terrier", l), "Sealyham Terrier", 1)
    sql += breed(182, _("Setter", l), "Setter", 1)
    sql += breed(183, _("Shar Pei", l), "Shar Pei", 1)
    sql += breed(184, _("Sheep Dog", l), "Sheep Dog", 1)
    sql += breed(185, _("Shepherd", l), "Shepherd", 1)
    sql += breed(186, _("Shetland Sheepdog Sheltie", l), "Shetland Sheepdog Sheltie", 1)
    sql += breed(187, _("Shiba Inu", l), "Shiba Inu", 1)
    sql += breed(188, _("Shih Tzu", l), "Shih Tzu", 1)
    sql += breed(189, _("Siberian Husky", l), "Siberian Husky", 1)
    sql += breed(190, _("Silky Terrier", l), "Silky Terrier", 1)
    sql += breed(191, _("Skye Terrier", l), "Skye Terrier", 1)
    sql += breed(192, _("Sloughi", l), "Sloughi", 1)
    sql += breed(193, _("Smooth Fox Terrier", l), "Smooth Fox Terrier", 1)
    sql += breed(194, _("Spaniel", l), "Spaniel", 1)
    sql += breed(195, _("Spitz", l), "Spitz", 1)
    sql += breed(196, _("Staffordshire Bull Terrier", l), "Staffordshire Bull Terrier", 1)
    sql += breed(197, _("South Russian Ovcharka", l), "South Russian Ovcharka", 1)
    sql += breed(198, _("Swedish Vallhund", l), "Swedish Vallhund", 1)
    sql += breed(199, _("Terrier", l), "Terrier", 1)
    sql += breed(200, _("Thai Ridgeback", l), "Thai Ridgeback", 1)
    sql += breed(201, _("Tibetan Mastiff", l), "Tibetan Mastiff", 1)
    sql += breed(202, _("Tibetan Spaniel", l), "Tibetan Spaniel", 1)
    sql += breed(203, _("Tibetan Terrier", l), "Tibetan Terrier", 1)
    sql += breed(204, _("Tosa Inu", l), "Tosa Inu", 1)
    sql += breed(205, _("Toy Fox Terrier", l), "Toy Fox Terrier", 1)
    sql += breed(206, _("Treeing Walker Coonhound", l), "Treeing Walker Coonhound", 1)
    sql += breed(207, _("Vizsla", l), "Vizsla", 1)
    sql += breed(208, _("Weimaraner", l), "Weimaraner", 1)
    sql += breed(209, _("Welsh Corgi", l), "Welsh Corgi", 1)
    sql += breed(210, _("Welsh Terrier", l), "Welsh Terrier", 1)
    sql += breed(211, _("Welsh Springer Spaniel", l), "Welsh Springer Spaniel", 1)
    sql += breed(212, _("West Highland White Terrier Westie", l), "West Highland White Terrier Westie", 1)
    sql += breed(213, _("Wheaten Terrier", l), "Wheaten Terrier", 1)
    sql += breed(214, _("Whippet", l), "Whippet", 1)
    sql += breed(215, _("White German Shepherd", l), "White German Shepherd", 1)
    sql += breed(216, _("Wire-haired Pointing Griffon", l), "Wire-haired Pointing Griffon", 1)
    sql += breed(217, _("Wirehaired Terrier", l), "Wirehaired Terrier", 1)
    sql += breed(218, _("Yellow Labrador Retriever", l), "Yellow Labrador Retriever", 1)
    sql += breed(219, _("Yorkshire Terrier Yorkie", l), "Yorkshire Terrier Yorkie", 1)
    sql += breed(220, _("Xoloitzcuintle/Mexican Hairless", l), "Xoloitzcuintle/Mexican Hairless", 1)
    sql += breed(221, _("Abyssinian", l), "Abyssinian", 2)
    sql += breed(222, _("American Curl", l), "American Curl", 2)
    sql += breed(223, _("American Shorthair", l), "American Shorthair", 2)
    sql += breed(224, _("American Wirehair", l), "American Wirehair", 2)
    sql += breed(225, _("Applehead Siamese", l), "Applehead Siamese", 2)
    sql += breed(226, _("Balinese", l), "Balinese", 2)
    sql += breed(227, _("Bengal", l), "Bengal", 2)
    sql += breed(228, _("Birman", l), "Birman", 2)
    sql += breed(229, _("Bobtail", l), "Bobtail", 2)
    sql += breed(230, _("Bombay", l), "Bombay", 2)
    sql += breed(231, _("British Shorthair", l), "British Shorthair", 2)
    sql += breed(232, _("Burmese", l), "Burmese", 2)
    sql += breed(233, _("Burmilla", l), "Burmilla", 2)
    sql += breed(234, _("Calico", l), "Calico", 2)
    sql += breed(235, _("Canadian Hairless", l), "Canadian Hairless", 2)
    sql += breed(236, _("Chartreux", l), "Chartreux", 2)
    sql += breed(237, _("Chinchilla", l), "Chinchilla", 2)
    sql += breed(238, _("Cornish Rex", l), "Cornish Rex", 2)
    sql += breed(239, _("Cymric", l), "Cymric", 2)
    sql += breed(240, _("Devon Rex", l), "Devon Rex", 2)
    sql += breed(243, _("Domestic Long Hair", l), "Domestic Long Hair", 2)
    sql += breed(252, _("Domestic Medium Hair", l), "Domestic Medium Hair", 2)
    sql += breed(261, _("Domestic Short Hair", l), "Domestic Short Hair", 2)
    sql += breed(271, _("Egyptian Mau", l), "Egyptian Mau", 2)
    sql += breed(272, _("Exotic Shorthair", l), "Exotic Shorthair", 2)
    sql += breed(273, _("Extra-Toes Cat (Hemingway Polydactyl)", l), "Extra-Toes Cat (Hemingway Polydactyl)", 2)
    sql += breed(274, _("Havana", l), "Havana", 2)
    sql += breed(275, _("Himalayan", l), "Himalayan", 2)
    sql += breed(276, _("Japanese Bobtail", l), "Japanese Bobtail", 2)
    sql += breed(277, _("Javanese", l), "Javanese", 2)
    sql += breed(278, _("Korat", l), "Korat", 2)
    sql += breed(279, _("Maine Coon", l), "Maine Coon", 2)
    sql += breed(280, _("Manx", l), "Manx", 2)
    sql += breed(281, _("Munchkin", l), "Munchkin", 2)
    sql += breed(282, _("Norwegian Forest Cat", l), "Norwegian Forest Cat", 2)
    sql += breed(283, _("Ocicat", l), "Ocicat", 2)
    sql += breed(284, _("Oriental Long Hair", l), "Oriental Long Hair", 2)
    sql += breed(285, _("Oriental Short Hair", l), "Oriental Short Hair", 2)
    sql += breed(286, _("Oriental Tabby", l), "Oriental Tabby", 2)
    sql += breed(287, _("Persian", l), "Persian", 2)
    sql += breed(288, _("Pixie-Bob", l), "Pixie-Bob", 2)
    sql += breed(289, _("Ragamuffin", l), "Ragamuffin", 2)
    sql += breed(290, _("Ragdoll", l), "Ragdoll", 2)
    sql += breed(291, _("Russian Blue", l), "Russian Blue", 2)
    sql += breed(292, _("Scottish Fold", l), "Scottish Fold", 2)
    sql += breed(293, _("Selkirk Rex", l), "Selkirk Rex", 2)
    sql += breed(294, _("Siamese", l), "Siamese", 2)
    sql += breed(295, _("Siberian", l), "Siberian", 2)
    sql += breed(296, _("Singapura", l), "Singapura", 2)
    sql += breed(297, _("Snowshoe", l), "Snowshoe", 2)
    sql += breed(298, _("Somali", l), "Somali", 2)
    sql += breed(299, _("Sphynx (hairless cat)", l), "Sphynx (hairless cat)", 2)
    sql += breed(307, _("Tiger", l), "Tiger", 2)
    sql += breed(308, _("Tonkinese", l), "Tonkinese", 2)
    sql += breed(311, _("Turkish Angora", l), "Turkish Angora", 2)
    sql += breed(312, _("Turkish Van", l), "Turkish Van", 2)
    sql += breed(314, _("American", l), "American", 7)
    sql += breed(315, _("American Fuzzy Lop", l), "American Fuzzy Lop", 7)
    sql += breed(316, _("American Sable", l), "American Sable", 7)
    sql += breed(317, _("Angora Rabbit", l), "Angora Rabbit", 7)
    sql += breed(318, _("Belgian Hare", l), "Belgian Hare", 7)
    sql += breed(319, _("Beveren", l), "Beveren", 7)
    sql += breed(320, _("Britannia Petite", l), "Britannia Petite", 7)
    sql += breed(321, _("Bunny Rabbit", l), "Bunny Rabbit", 7)
    sql += breed(322, _("Californian", l), "Californian", 7)
    sql += breed(323, _("Champagne DArgent", l), "Champagne DArgent", 7)
    sql += breed(324, _("Checkered Giant", l), "Checkered Giant", 7)
    sql += breed(325, _("Chinchilla", l), "Chinchilla", 7)
    sql += breed(326, _("Cinnamon", l), "Cinnamon", 7)
    sql += breed(327, _("Creme DArgent", l), "Creme DArgent", 7)
    sql += breed(328, _("Dutch", l), "Dutch", 7)
    sql += breed(329, _("Dwarf", l), "Dwarf", 7)
    sql += breed(330, _("Dwarf Eared", l), "Dwarf Eared", 7)
    sql += breed(331, _("English Lop", l), "English Lop", 7)
    sql += breed(332, _("English Spot", l), "English Spot", 7)
    sql += breed(333, _("Flemish Giant", l), "Flemish Giant", 7)
    sql += breed(334, _("Florida White", l), "Florida White", 7)
    sql += breed(335, _("French-Lop", l), "French-Lop", 7)
    sql += breed(336, _("Harlequin", l), "Harlequin", 7)
    sql += breed(337, _("Havana", l), "Havana", 7)
    sql += breed(338, _("Himalayan", l), "Himalayan", 7)
    sql += breed(339, _("Holland Lop", l), "Holland Lop", 7)
    sql += breed(340, _("Hotot", l), "Hotot", 7)
    sql += breed(341, _("Jersey Wooly", l), "Jersey Wooly", 7)
    sql += breed(342, _("Lilac", l), "Lilac", 7)
    sql += breed(343, _("Lop Eared", l), "Lop Eared", 7)
    sql += breed(344, _("Mini-Lop", l), "Mini-Lop", 7)
    sql += breed(345, _("Mini Rex", l), "Mini Rex", 7)
    sql += breed(346, _("Netherland Dwarf", l), "Netherland Dwarf", 7)
    sql += breed(347, _("New Zealand", l), "New Zealand", 7)
    sql += breed(348, _("Palomino", l), "Palomino", 7)
    sql += breed(349, _("Polish", l), "Polish", 7)
    sql += breed(350, _("Rex", l), "Rex", 7)
    sql += breed(351, _("Rhinelander", l), "Rhinelander", 7)
    sql += breed(352, _("Satin", l), "Satin", 7)
    sql += breed(353, _("Silver", l), "Silver", 7)
    sql += breed(354, _("Silver Fox", l), "Silver Fox", 7)
    sql += breed(355, _("Silver Marten", l), "Silver Marten", 7)
    sql += breed(356, _("Tan", l), "Tan", 7)
    sql += breed(357, _("Appaloosa", l), "Appaloosa", 24)
    sql += breed(358, _("Arabian", l), "Arabian", 24)
    sql += breed(359, _("Clydesdale", l), "Clydesdale", 24)
    sql += breed(360, _("Donkey/Mule", l), "Donkey/Mule", 26)
    sql += breed(361, _("Draft", l), "Draft", 24)
    sql += breed(362, _("Gaited", l), "Gaited", 24)
    sql += breed(363, _("Grade", l), "Grade", 24)
    sql += breed(364, _("Missouri Foxtrotter", l), "Missouri Foxtrotter", 24)
    sql += breed(365, _("Morgan", l), "Morgan", 24)
    sql += breed(366, _("Mustang", l), "Mustang", 24)
    sql += breed(367, _("Paint/Pinto", l), "Paint/Pinto", 24)
    sql += breed(368, _("Palomino", l), "Palomino", 24)
    sql += breed(369, _("Paso Fino", l), "Paso Fino", 24)
    sql += breed(370, _("Percheron", l), "Percheron", 24)
    sql += breed(371, _("Peruvian Paso", l), "Peruvian Paso", 24)
    sql += breed(372, _("Pony", l), "Pony", 25)
    sql += breed(373, _("Quarterhorse", l), "Quarterhorse", 25)
    sql += breed(374, _("Saddlebred", l), "Saddlebred", 24)
    sql += breed(375, _("Standardbred", l), "Standardbred", 24)
    sql += breed(376, _("Thoroughbred", l), "Thoroughbred", 24)
    sql += breed(377, _("Tennessee Walker", l), "Tennessee Walker", 24)
    sql += breed(378, _("Warmblood", l), "Warmblood", 24)
    sql += breed(379, _("Chinchilla", l), "Chinchilla", 10)
    sql += breed(380, _("Ferret", l), "Ferret", 9)
    sql += breed(381, _("Gerbil", l), "Gerbil", 18)
    sql += breed(382, _("Guinea Pig", l), "Guinea Pig", 20)
    sql += breed(383, _("Hamster", l), "Hamster", 22)
    sql += breed(384, _("Hedgehog", l), "Hedgehog", 6)
    sql += breed(385, _("Mouse", l), "Mouse", 4)
    sql += breed(386, _("Prairie Dog", l), "Prairie Dog", 5)
    sql += breed(387, _("Rat", l), "Rat", 5)
    sql += breed(388, _("Skunk", l), "Skunk", 5)
    sql += breed(389, _("Sugar Glider", l), "Sugar Glider", 5)
    sql += breed(390, _("Pot Bellied", l), "Pot Bellied", 28)
    sql += breed(391, _("Vietnamese Pot Bellied", l), "Vietnamese Pot Bellied", 28)
    sql += breed(392, _("Gecko", l), "Gecko", 13)
    sql += breed(393, _("Iguana", l), "Iguana", 13)
    sql += breed(394, _("Lizard", l), "Lizard", 13)
    sql += breed(395, _("Snake", l), "Snake", 13)
    sql += breed(396, _("Turtle", l), "Turtle", 13)
    sql += breed(397, _("Fish", l), "Fish", 21)
    sql += breed(398, _("African Grey", l), "African Grey", 3)
    sql += breed(399, _("Amazon", l), "Amazon", 3)
    sql += breed(400, _("Brotogeris", l), "Brotogeris", 3)
    sql += breed(401, _("Budgie/Budgerigar", l), "Budgie/Budgerigar", 3)
    sql += breed(402, _("Caique", l), "Caique", 3)
    sql += breed(403, _("Canary", l), "Canary", 3)
    sql += breed(404, _("Chicken", l), "Chicken", 3)
    sql += breed(405, _("Cockatiel", l), "Cockatiel", 3)
    sql += breed(406, _("Cockatoo", l), "Cockatoo", 3)
    sql += breed(407, _("Conure", l), "Conure", 3)
    sql += breed(408, _("Dove", l), "Dove", 3)
    sql += breed(409, _("Duck", l), "Duck", 3)
    sql += breed(410, _("Eclectus", l), "Eclectus", 3)
    sql += breed(411, _("Emu", l), "Emu", 3)
    sql += breed(412, _("Finch", l), "Finch", 3)
    sql += breed(413, _("Goose", l), "Goose", 3)
    sql += breed(414, _("Guinea fowl", l), "Guinea fowl", 3)
    sql += breed(415, _("Kakariki", l), "Kakariki", 3)
    sql += breed(416, _("Lory/Lorikeet", l), "Lory/Lorikeet", 3)
    sql += breed(417, _("Lovebird", l), "Lovebird", 3)
    sql += breed(418, _("Macaw", l), "Macaw", 3)
    sql += breed(419, _("Mynah", l), "Mynah", 3)
    sql += breed(420, _("Ostrich", l), "Ostrich", 3)
    sql += breed(421, _("Parakeet (Other)", l), "Parakeet (Other)", 3)
    sql += breed(422, _("Parrot (Other)", l), "Parrot (Other)", 3)
    sql += breed(423, _("Parrotlet", l), "Parrotlet", 3)
    sql += breed(424, _("Peacock/Pea fowl", l), "Peacock/Pea fowl", 3)
    sql += breed(425, _("Pheasant", l), "Pheasant", 3)
    sql += breed(426, _("Pigeon", l), "Pigeon", 3)
    sql += breed(427, _("Pionus", l), "Pionus", 3)
    sql += breed(428, _("Poicephalus/Senegal", l), "Poicephalus/Senegal", 3)
    sql += breed(429, _("Quaker Parakeet", l), "Quaker Parakeet", 3)
    sql += breed(430, _("Rhea", l), "Rhea", 3)
    sql += breed(431, _("Ringneck/Psittacula", l), "Ringneck/Psittacula", 3)
    sql += breed(432, _("Rosella", l), "Rosella", 3)
    sql += breed(433, _("Softbill (Other)", l), "Softbill (Other)", 3)
    sql += breed(434, _("Swan", l), "Swan", 3)
    sql += breed(435, _("Toucan", l), "Toucan", 3)
    sql += breed(436, _("Turkey", l), "Turkey", 3)
    sql += breed(437, _("Cow", l), "Cow", 16)
    sql += breed(438, _("Goat", l), "Goat", 16)
    sql += breed(439, _("Sheep", l), "Sheep", 16)
    sql += breed(440, _("Llama", l), "Llama", 16)
    sql += breed(441, _("Pig (Farm)", l), "Pig (Farm)", 28)
    sql += breed(442, _("Crossbreed", l), "Terrier", 1)
    sql += lookup2money("costtype", 1, _("Board and Food", l))
    sql += lookup2("deathreason", 1, _("Dead On Arrival", l))
    sql += lookup2("deathreason", 2, _("Died", l))
    sql += lookup2("deathreason", 3, _("Healthy", l))
    sql += lookup2("deathreason", 4, _("Sick/Injured", l))
    sql += lookup2("deathreason", 5, _("Requested", l))
    sql += lookup2("deathreason", 6, _("Culling", l))
    sql += lookup2("deathreason", 7, _("Feral", l))
    sql += lookup2("deathreason", 8, _("Biting", l))
    sql += lookup2("diet", 1, _("Standard", l))
    sql += lookup2("donationpayment", 1, _("Cash", l))
    sql += lookup2("donationpayment", 2, _("Cheque", l))
    sql += lookup2("donationpayment", 3, _("Credit Card", l))
    sql += lookup2("donationpayment", 4, _("Debit Card", l))
    sql += lookup2money("donationtype", 1, _("Donation", l))
    sql += lookup2money("donationtype", 2, _("Adoption Fee", l))
    sql += lookup2money("donationtype", 3, _("Waiting List Donation", l))
    sql += lookup2money("donationtype", 4, _("Entry Donation", l))
    sql += lookup2money("donationtype", 5, _("Animal Sponsorship", l))
    sql += lookup2("entryreason", 1, _("Marriage/Relationship split", l))
    sql += lookup2("entryreason", 2, _("Allergies", l))
    sql += lookup2("entryreason", 3, _("Biting", l))
    sql += lookup2("entryreason", 4, _("Unable to Cope", l))
    sql += lookup2("entryreason", 5, _("Unsuitable Accomodation", l))
    sql += lookup2("entryreason", 6, _("Died", l))
    sql += lookup2("entryreason", 7, _("Stray", l))
    sql += lookup2("entryreason", 8, _("Sick/Injured", l))
    sql += lookup2("entryreason", 9, _("Unable to Afford", l))
    sql += lookup2("entryreason", 10, _("Abuse", l))
    sql += lookup2("entryreason", 11, _("Abandoned", l))
    sql += lookup2("internallocation", 1, _("No Locations", l))
    sql += lookup1("lksex", 0, _("Female", l))
    sql += lookup1("lksex", 1, _("Male", l))
    sql += lookup1("lksex", 2, _("Unknown", l))
    sql += lookup1("lksize", 0, _("Very Large", l))
    sql += lookup1("lksize", 1, _("Large", l))
    sql += lookup1("lksize", 2, _("Medium", l))
    sql += lookup1("lksize", 3, _("Small", l))
    sql += lookup1("lkcoattype", 0, _("Short", l))
    sql += lookup1("lkcoattype", 1, _("Long", l))
    sql += lookup1("lkcoattype", 2, _("Rough", l))
    sql += lookup1("lkcoattype", 3, _("Curly", l))
    sql += lookup1("lkcoattype", 4, _("Corded", l))
    sql += lookup1("lkcoattype", 5, _("Hairless", l))
    sql += lookup1("lksaccounttype", 1, _("Bank", l))
    sql += lookup1("lksaccounttype", 2, _("Credit Card", l))
    sql += lookup1("lksaccounttype", 3, _("Loan", l))
    sql += lookup1("lksaccounttype", 4, _("Expense", l))
    sql += lookup1("lksaccounttype", 5, _("Income", l))
    sql += lookup1("lksaccounttype", 6, _("Pension", l))
    sql += lookup1("lksaccounttype", 7, _("Shares", l))
    sql += lookup1("lksaccounttype", 8, _("Asset", l))
    sql += lookup1("lksaccounttype", 9, _("Liability", l))
    sql += lookup1("lksmovementtype", 0, _("None", l))
    sql += lookup1("lksmovementtype", 1, _("Adoption", l))
    sql += lookup1("lksmovementtype", 2, _("Foster", l))
    sql += lookup1("lksmovementtype", 3, _("Transfer", l))
    sql += lookup1("lksmovementtype", 4, _("Escaped", l))
    sql += lookup1("lksmovementtype", 5, _("Reclaimed", l))
    sql += lookup1("lksmovementtype", 6, _("Stolen", l))
    sql += lookup1("lksmovementtype", 7, _("Released To Wild", l))
    sql += lookup1("lksmovementtype", 8, _("Retailer", l))
    sql += lookup1("lksmovementtype", 9, _("Reservation", l))
    sql += lookup1("lksmovementtype", 10, _("Cancelled Reservation", l))
    sql += lookup1("lksmovementtype", 11, _("Trial Adoption", l))
    sql += lookup1("lksmovementtype", 12, _("Permanent Foster", l))
    sql += lookup1("lksmedialink", 0, _("Animal", l))
    sql += lookup1("lksmedialink", 1, _("Lost Animal", l))
    sql += lookup1("lksmedialink", 2, _("Found Animal", l))
    sql += lookup1("lksmedialink", 3, _("Owner", l))
    sql += lookup1("lksmedialink", 4, _("Movement", l))
    sql += lookup1("lksmediatype", 0, _("File", l))
    sql += lookup1("lksmediatype", 1, _("Document Link", l))
    sql += lookup1("lksmediatype", 2, _("Video Link", l))
    sql += lookup1("lksdiarylink", 0, _("None", l))
    sql += lookup1("lksdiarylink", 1, _("Animal", l))
    sql += lookup1("lksdiarylink", 2, _("Owner", l))
    sql += lookup1("lksdiarylink", 3, _("Lost Animal", l))
    sql += lookup1("lksdiarylink", 4, _("Found Animal", l))
    sql += lookup1("lksdiarylink", 5, _("Waiting List", l))
    sql += lookup1("lksdiarylink", 6, _("Movement", l))
    sql += lookup1("lksdonationfreq", 0, _("One-Off", l))
    sql += lookup1("lksdonationfreq", 1, _("Weekly", l))
    sql += lookup1("lksdonationfreq", 2, _("Monthly", l))
    sql += lookup1("lksdonationfreq", 3, _("Quarterly", l))
    sql += lookup1("lksdonationfreq", 4, _("Half-Yearly", l))
    sql += lookup1("lksdonationfreq", 5, _("Annually", l))
    sql += lookup1("lksfieldlink", 0, _("Animal - Additional", l))
    sql += lookup1("lksfieldlink", 2, _("Animal - Details", l))
    sql += lookup1("lksfieldlink", 3, _("Animal - Notes", l))
    sql += lookup1("lksfieldlink", 4, _("Animal - Entry", l))
    sql += lookup1("lksfieldlink", 5, _("Animal - Health and Identification", l))
    sql += lookup1("lksfieldlink", 6, _("Animal - Death", l))
    sql += lookup1("lksfieldlink", 1, _("Person - Additional", l))
    sql += lookup1("lksfieldlink", 7, _("Person - Name and Address", l))
    sql += lookup1("lksfieldlink", 8, _("Person - Type", l))
    sql += lookup1("lksfieldlink", 9, _("Lost Animal - Additional", l))
    sql += lookup1("lksfieldlink", 10, _("Lost Animal - Details", l))
    sql += lookup1("lksfieldlink", 11, _("Found Animal - Additional", l))
    sql += lookup1("lksfieldlink", 12, _("Found Animal - Details", l))
    sql += lookup1("lksfieldlink", 13, _("Waiting List - Additional", l))
    sql += lookup1("lksfieldlink", 14, _("Waiting List - Details", l))
    sql += lookup1("lksfieldlink", 15, _("Waiting List - Removal", l))
    sql += lookup1("lksfieldtype", 0, _("Yes/No", l))
    sql += lookup1("lksfieldtype", 1, _("Text", l))
    sql += lookup1("lksfieldtype", 2, _("Notes", l))
    sql += lookup1("lksfieldtype", 3, _("Number", l))
    sql += lookup1("lksfieldtype", 4, _("Date", l))
    sql += lookup1("lksfieldtype", 5, _("Money", l))
    sql += lookup1("lksfieldtype", 6, _("Lookup", l))
    sql += lookup1("lksfieldtype", 7, _("Multi-Lookup", l))
    sql += lookup1("lksfieldtype", 8, _("Animal", l))
    sql += lookup1("lksfieldtype", 9, _("Person", l))
    sql += lookup1("lksloglink", 0, _("Animal", l))
    sql += lookup1("lksloglink", 1, _("Owner", l))
    sql += lookup1("lksloglink", 2, _("Lost Animal", l))
    sql += lookup1("lksloglink", 3, _("Found Animal", l))
    sql += lookup1("lksloglink", 4, _("Waiting List", l))
    sql += lookup1("lksloglink", 5, _("Movement", l))
    sql += lookup1("lksyesno", 0, _("No", l))
    sql += lookup1("lksyesno", 1, _("Yes", l))
    sql += lookup1("lksynun", 0, _("Yes", l))
    sql += lookup1("lksynun", 1, _("No", l))
    sql += lookup1("lksynun", 2, _("Unknown", l))
    sql += lookup1("lksposneg", 0, _("Unknown", l))
    sql += lookup1("lksposneg", 1, _("Negative", l))
    sql += lookup1("lksposneg", 2, _("Positive", l))
    sql += lookup1("lkurgency", 1, _("Urgent", l))
    sql += lookup1("lkurgency", 2, _("High", l))
    sql += lookup1("lkurgency", 3, _("Medium", l))
    sql += lookup1("lkurgency", 4, _("Low", l))
    sql += lookup1("lkurgency", 5, _("Lowest", l))
    sql += lookup2("logtype", 1, _("Bite", l))
    sql += lookup2("logtype", 2, _("Complaint", l))
    sql += lookup2("logtype", 3, _("History", l))
    sql += lookup2("logtype", 4, _("Weight", l))
    sql += lookup2("logtype", 5, _("Document", l))
    sql += species(1, _("Dog", l), "Dog")
    sql += species(2, _("Cat", l), "Cat")
    sql += species(3, _("Bird", l), "Bird")
    sql += species(4, _("Mouse", l), "Small&Furry")
    sql += species(5, _("Rat", l), "Small&Furry")
    sql += species(6, _("Hedgehog", l), "Small&Furry")
    sql += species(7, _("Rabbit", l), "Rabbit")
    sql += species(8, _("Dove", l), "Bird")
    sql += species(9, _("Ferret", l), "Small&Furry")
    sql += species(10, _("Chinchilla", l), "Small&Furry")
    sql += species(11, _("Snake", l), "Reptile")
    sql += species(12, _("Tortoise", l), "Reptile")
    sql += species(13, _("Terrapin", l), "Reptile")
    sql += species(14, _("Chicken", l), "Barnyard")
    sql += species(15, _("Owl", l), "Bird")
    sql += species(16, _("Goat", l), "Barnyard")
    sql += species(17, _("Goose", l), "Bird")
    sql += species(18, _("Gerbil", l), "Small&Furry")
    sql += species(19, _("Cockatiel", l), "Bird")
    sql += species(20, _("Guinea Pig", l), "Small&Furry")
    sql += species(21, _("Goldfish", l), "Reptile")
    sql += species(22, _("Hamster", l), "Small&Furry")
    sql += species(23, _("Camel", l), "Horse")
    sql += species(24, _("Horse", l), "Horse")
    sql += species(25, _("Pony", l), "Horse")
    sql += species(26, _("Donkey", l), "Horse")
    sql += species(27, _("Llama", l), "Horse")
    sql += species(28, _("Pig", l), "Barnyard")
    sql += lookup2("testresult", 1, _("Unknown", l))
    sql += lookup2("testresult", 2, _("Negative", l))
    sql += lookup2("testresult", 3, _("Positive", l))
    sql += lookup2money("testtype", 1, _("FIV", l))
    sql += lookup2money("testtype", 2, _("FLV", l))
    sql += lookup2money("testtype", 3, _("Heartworm", l))
    sql += lookup2money("voucher", 1, _("Neuter/Spay", l))
    sql += lookup2money("vaccinationtype", 1, _("Temporary Vaccination", l))
    sql += lookup2money("vaccinationtype", 2, _("First Vaccination", l))
    sql += lookup2money("vaccinationtype", 3, _("Second Vaccination", l))
    sql += lookup2money("vaccinationtype", 4, _("Booster", l))
    sql += lookup2money("vaccinationtype", 5, _("Leukaemia", l))
    sql += lookup2money("vaccinationtype", 6, _("Kennel Cough", l))
    sql += lookup2money("vaccinationtype", 7, _("Parvovirus", l))
    return sql

def install_db_structure(dbo):
    """
    Creates the db structure in the target database
    """
    al.info("creating default database schema", "dbupdate.install_default_data", dbo)
    sql = sql_structure(dbo)
    for s in sql.split(";"):
        if (s.strip() != ""):
            print s.strip()
            db.execute_dbupdate(dbo, s.strip())

def install_db_views(dbo):
    """
    Installs all the database views.
    """
    def create_view(viewname, sql):
        db.execute_dbupdate(dbo, "DROP VIEW IF EXISTS %s" % viewname)
        db.execute_dbupdate(dbo, "CREATE VIEW %s AS %s" % (viewname, sql))

    # Set us upto date to stop race condition/other clients trying
    # to install
    configuration.db_view_seq_version(dbo, BUILD)

    create_view("v_adoption", \
        "SELECT m.*, o.OwnerTitle, o.OwnerInitials, o.OwnerSurname, o.OwnerForenames, o.OwnerName, " \
        "o.OwnerAddress, o.HomeTelephone, o.WorkTelephone, o.MobileTelephone, " \
        "a.ShelterCode, a.ShortCode, a.AgeGroup, a.AnimalName, a.Neutered, a.DeceasedDate, a.HasActiveReserve, " \
        "a.HasTrialAdoption, a.IsHold, a.IsQuarantine, a.HoldUntilDate, a.CrueltyCase, a.NonShelterAnimal, " \
        "a.ActiveMovementType, a.Archived, a.IsNotAvailableForAdoption, " \
        "r.OwnerName AS RetailerName, " \
        "ma.MediaName AS WebsiteMediaName, sx.Sex, s.SpeciesName, rr.ReasonName AS ReturnedReasonName, " \
        "CASE WHEN m.MovementType = 2 AND m.IsPermanentFoster = 1 THEN " \
        "(SELECT MovementType FROM lksmovementtype WHERE ID=12) " \
        "WHEN m.MovementType = 1 AND m.IsTrial = 1 THEN " \
        "(SELECT MovementType FROM lksmovementtype WHERE ID=11) " \
        "WHEN m.MovementDate Is Null AND m.ReservationDate Is Not Null AND m.ReservationCancelledDate Is Not Null THEN " \
        "(SELECT MovementType FROM lksmovementtype WHERE ID=10) " \
        "WHEN m.MovementDate Is Null AND m.ReservationDate Is Not Null THEN " \
        "(SELECT MovementType FROM lksmovementtype WHERE ID=9) " \
        "ELSE l.MovementType END AS MovementName " \
        "FROM adoption m " \
        "LEFT OUTER JOIN lksmovementtype l ON l.ID = m.MovementType " \
        "INNER JOIN animal a ON m.AnimalID = a.ID " \
        "LEFT OUTER JOIN media ma ON ma.LinkID = a.ID AND ma.LinkTypeID = 0 AND ma.WebsitePhoto = 1 " \
        "LEFT OUTER JOIN entryreason rr ON m.ReturnedReasonID = rr.ID " \
        "INNER JOIN species s ON a.SpeciesID = s.ID " \
        "INNER JOIN lksex sx ON sx.ID = a.Sex " \
        "LEFT OUTER JOIN owner o ON m.OwnerID = o.ID " \
        "LEFT OUTER JOIN owner r ON m.RetailerID = r.ID ")

    create_view("v_animal", \
        "SELECT DISTINCT a.*, " \
        "at.AnimalType AS AnimalTypeName, " \
        "ba1.AnimalName AS BondedAnimal1Name, " \
        "ba1.ShelterCode AS BondedAnimal1Code, " \
        "ba2.AnimalName AS BondedAnimal2Name, " \
        "ba2.ShelterCode AS BondedAnimal2Code, " \
        "bc.BaseColour AS BaseColourName, " \
        "sp.SpeciesName AS SpeciesName, " \
        "sp.PetFinderSpecies, " \
        "bd.BreedName AS BreedName1, "\
        "bd2.BreedName AS BreedName2, "\
        "bd.PetFinderBreed, " \
        "bd2.PetFinderBreed AS PetFinderBreed2, " \
        "ct.CoatType AS CoatTypeName, " \
        "sx.Sex AS SexName, " \
        "sz.Size AS SizeName, " \
        "ov.OwnerName AS OwnersVetName, " \
        "ov.OwnerAddress AS OwnersVetAddress, " \
        "ov.OwnerTown AS OwnersVetTown, " \
        "ov.OwnerCounty AS OwnersVetCounty, " \
        "ov.OwnerPostcode AS OwnersVetPostcode, " \
        "ov.WorkTelephone AS OwnersVetWorkTelephone, " \
        "cv.OwnerName AS CurrentVetName, " \
        "cv.OwnerAddress AS CurrentVetAddress, " \
        "cv.OwnerTown AS CurrentVetTown, " \
        "cv.OwnerCounty AS CurrentVetCounty, " \
        "cv.OwnerPostcode AS CurrentVetPostcode, " \
        "cv.WorkTelephone AS CurrentVetWorkTelephone, " \
        "oo.OwnerName AS OriginalOwnerName, " \
        "oo.OwnerAddress AS OriginalOwnerAddress, " \
        "oo.OwnerTown AS OriginalOwnerTown, " \
        "oo.OwnerCounty AS OriginalOwnerCounty, " \
        "oo.OwnerPostcode AS OriginalOwnerPostcode, " \
        "oo.HomeTelephone AS OriginalOwnerHomeTelephone, " \
        "oo.WorkTelephone AS OriginalOwnerWorkTelephone, " \
        "oo.MobileTelephone AS OriginalOwnerMobileTelephone, " \
        "oo.EmailAddress AS OriginalOwnerEmailAddress, " \
        "co.ID AS CurrentOwnerID, " \
        "co.OwnerName AS CurrentOwnerName, " \
        "co.OwnerTitle AS CurrentOwnerTitle, " \
        "co.OwnerForeNames AS CurrentOwnerForeNames, " \
        "co.OwnerSurname AS CurrentOwnerSurname, " \
        "co.OwnerAddress AS CurrentOwnerAddress, " \
        "co.OwnerTown AS CurrentOwnerTown, " \
        "co.OwnerCounty AS CurrentOwnerCounty, " \
        "co.OwnerPostcode AS CurrentOwnerPostcode, " \
        "co.HomeTelephone AS CurrentOwnerHomeTelephone, " \
        "co.WorkTelephone AS CurrentOwnerWorkTelephone, " \
        "co.MobileTelephone AS CurrentOwnerMobileTelephone, " \
        "co.EmailAddress AS CurrentOwnerEmailAddress, " \
        "bo.OwnerName AS BroughtInByOwnerName, " \
        "bo.OwnerAddress AS BroughtInByOwnerAddress, " \
        "bo.OwnerTown AS BroughtInByOwnerTown, " \
        "bo.OwnerCounty AS BroughtInByOwnerCounty, " \
        "bo.OwnerPostcode AS BroughtInByOwnerPostcode, " \
        "bo.HomeTelephone AS BroughtInByHomeTelephone, " \
        "bo.WorkTelephone AS BroughtInByWorkTelephone, " \
        "bo.MobileTelephone AS BroughtInByMobileTelephone, " \
        "bo.EmailAddress AS BroughtInByEmailAddress, " \
        "ro.ID AS ReservedOwnerID, " \
        "ro.OwnerName AS ReservedOwnerName, " \
        "ro.OwnerAddress AS ReservedOwnerAddress, " \
        "ro.OwnerTown AS ReservedOwnerTown, " \
        "ro.OwnerCounty AS ReservedOwnerCounty, " \
        "ro.OwnerPostcode AS ReservedOwnerPostcode, " \
        "ro.HomeTelephone AS ReservedOwnerHomeTelephone, " \
        "ro.WorkTelephone AS ReservedOwnerWorkTelephone, " \
        "ro.MobileTelephone AS ReservedOwnerMobileTelephone, " \
        "ro.EmailAddress AS ReservedOwnerEmailAddress, " \
        "er.ReasonName AS EntryReasonName, " \
        "dr.ReasonName AS PTSReasonName, " \
        "il.LocationName AS ShelterLocationName, " \
        "mt.MovementType AS ActiveMovementTypeName, " \
        "am.AdoptionNumber AS ActiveMovementAdoptionNumber, " \
        "am.ReturnDate AS ActiveMovementReturnDate, " \
        "am.InsuranceNumber AS ActiveMovementInsuranceNumber, " \
        "am.ReasonForReturn AS ActiveMovementReasonForReturn, " \
        "am.Comments AS ActiveMovementComments, " \
        "am.ReservationDate AS ActiveMovementReservationDate, " \
        "am.Donation AS ActiveMovementDonation, " \
        "am.CreatedBy AS ActiveMovementCreatedBy, " \
        "au.RealName AS ActiveMovementCreatedByName, " \
        "am.CreatedDate AS ActiveMovementCreatedDate, " \
        "am.LastChangedBy AS ActiveMovementLastChangedBy, " \
        "am.LastChangedDate AS ActiveMovementLastChangedDate, " \
        "CASE " \
        "WHEN EXISTS(SELECT ItemValue FROM configuration WHERE ItemName Like 'UseShortShelterCodes' AND ItemValue = 'Yes') " \
        "THEN a.ShortCode ELSE a.ShelterCode " \
        "END AS Code, " \
        "CASE " \
        "WHEN a.Archived = 0 AND a.ActiveMovementType = 2 AND a.HasPermanentFoster = 1 THEN " \
        "(SELECT MovementType FROM lksmovementtype WHERE ID=12) " \
        "WHEN a.Archived = 0 AND a.ActiveMovementType = 2 THEN " \
        "(SELECT MovementType FROM lksmovementtype WHERE ID=a.ActiveMovementType) " \
        "WHEN a.Archived = 0 AND a.ActiveMovementType = 1 AND a.HasTrialAdoption = 1 THEN " \
        "(SELECT MovementType FROM lksmovementtype WHERE ID=11) " \
        "WHEN a.Archived = 1 AND a.DeceasedDate Is Not Null AND a.ActiveMovementID = 0 THEN " \
        "(SELECT ReasonName FROM deathreason WHERE ID = a.PTSReasonID) " \
        "WHEN a.Archived = 1 AND a.DeceasedDate Is Not Null AND a.ActiveMovementID <> 0 THEN " \
        "(SELECT MovementType FROM lksmovementtype WHERE ID=a.ActiveMovementType) " \
        "WHEN a.Archived = 1 AND a.DeceasedDate Is Null AND a.ActiveMovementID <> 0 THEN " \
        "(SELECT MovementType FROM lksmovementtype WHERE ID=a.ActiveMovementType) " \
        "ELSE " \
        "(SELECT LocationName FROM internallocation WHERE ID=a.ShelterLocation) " \
        "END AS DisplayLocationName, " \
        "CASE " \
        "WHEN a.Archived = 0 AND a.CrueltyCase = 1 THEN 'Cruelty Case' " \
        "WHEN a.Archived = 0 AND a.IsQuarantine = 1 THEN 'Quarantine' " \
        "WHEN a.Archived = 0 AND a.IsHold = 1 THEN 'Hold' " \
        "WHEN a.Archived = 0 AND a.HasActiveReserve = 1 THEN 'Reserved' " \
        "WHEN a.Archived = 0 AND a.HasPermanentFoster = 1 THEN 'Permanent Foster' " \
        "WHEN a.IsNotAvailableForAdoption = 0 AND a.Archived = 0 AND a.HasTrialAdoption = 0 THEN 'Adoptable' " \
        "ELSE 'Not For Adoption' END AS AdoptionStatus, " \
        "web.MediaName AS WebsiteMediaName, " \
        "web.Date AS WebsiteMediaDate, " \
        "web.MediaNotes AS WebsiteMediaNotes, " \
        "(SELECT COUNT(*) FROM media mtc WHERE LOWER(mtc.MediaName) LIKE '%%.jpg' AND mtc.LinkTypeID = 0 AND mtc.LinkID = a.ID) AS WebsiteImageCount, " \
        "doc.MediaName AS DocMediaName, " \
        "vid.MediaName AS WebsiteVideoURL, " \
        "vid.MediaNotes AS WebsiteVideoNotes, " \
        "(SELECT Name FROM lksyesno l WHERE l.ID = a.NonShelterAnimal) AS NonShelterAnimalName, " \
        "(SELECT Name FROM lksyesno l WHERE l.ID = a.CrueltyCase) AS CrueltyCaseName, " \
        "(SELECT Name FROM lksyesno l WHERE l.ID = a.CrossBreed) AS CrossBreedName, " \
        "(SELECT Name FROM lksyesno l WHERE l.ID = a.EstimatedDOB) AS EstimatedDOBName, " \
        "(SELECT Name FROM lksyesno l WHERE l.ID = a.Identichipped) AS IdentichippedName, " \
        "(SELECT Name FROM lksyesno l WHERE l.ID = a.Tattoo) AS TattooName, " \
        "(SELECT Name FROM lksyesno l WHERE l.ID = a.Neutered) AS NeuteredName, " \
        "(SELECT Name FROM lksyesno l WHERE l.ID = a.CombiTested) AS CombiTestedName, " \
        "(SELECT Name FROM lksposneg l WHERE l.ID = a.CombiTestResult) AS CombiTestResultName, " \
        "(SELECT Name FROM lksyesno l WHERE l.ID = a.HeartwormTested) AS HeartwormTestedName, " \
        "(SELECT Name FROM lksposneg l WHERE l.ID = a.HeartwormTestResult) AS HeartwormTestResultName, " \
        "(SELECT Name FROM lksposneg l WHERE l.ID = a.FLVResult) AS FLVResultName, " \
        "(SELECT Name FROM lksyesno l WHERE l.ID = a.Declawed) AS DeclawedName, " \
        "(SELECT Name FROM lksyesno l WHERE l.ID = a.PutToSleep) AS PutToSleepName, " \
        "(SELECT Name FROM lksyesno l WHERE l.ID = a.IsDOA) AS IsDOAName, " \
        "(SELECT Name FROM lksyesno l WHERE l.ID = a.IsTransfer) AS IsTransferName, " \
        "(SELECT Name FROM lksynun l WHERE l.ID = a.IsGoodWithChildren) AS IsGoodWithChildrenName, " \
        "(SELECT Name FROM lksynun l WHERE l.ID = a.IsGoodWithCats) AS IsGoodWithCatsName, " \
        "(SELECT Name FROM lksynun l WHERE l.ID = a.IsGoodWithDogs) AS IsGoodWithDogsName, " \
        "(SELECT Name FROM lksynun l WHERE l.ID = a.IsHouseTrained) AS IsHouseTrainedName, " \
        "(SELECT Name FROM lksyesno l WHERE l.ID = a.IsNotAvailableForAdoption) AS IsNotAvailableForAdoptionName, " \
        "(SELECT Name FROM lksyesno l WHERE l.ID = a.HasSpecialNeeds) AS HasSpecialNeedsName, " \
        "(SELECT Name FROM lksyesno l WHERE l.ID = a.DiedOffShelter) AS DiedOffShelterName, " \
        "(SELECT Name FROM lksyesno l WHERE l.ID = a.HasActiveReserve) AS HasActiveReserveName, " \
        "(SELECT Name FROM lksyesno l WHERE l.ID = a.HasTrialAdoption) AS HasTrialAdoptionName " \
        "FROM animal a " \
        "LEFT OUTER JOIN animal ba1 ON ba1.ID = a.BondedAnimalID " \
        "LEFT OUTER JOIN animal ba2 ON ba2.ID = a.BondedAnimal2ID " \
        "LEFT OUTER JOIN animaltype at ON at.ID = a.AnimalTypeID " \
        "LEFT OUTER JOIN basecolour bc ON bc.ID = a.BaseColourID " \
        "LEFT OUTER JOIN species sp ON sp.ID = a.SpeciesID " \
        "LEFT OUTER JOIN lksex sx ON sx.ID = a.Sex " \
        "LEFT OUTER JOIN lksize sz ON sz.ID = a.Size " \
        "LEFT OUTER JOIN entryreason er ON er.ID = a.EntryReasonID " \
        "LEFT OUTER JOIN internallocation il ON il.ID = a.ShelterLocation " \
        "LEFT OUTER JOIN media web ON web.LinkID = a.ID AND web.LinkTypeID = 0 AND web.WebsitePhoto = 1 " \
        "LEFT OUTER JOIN media vid ON vid.LinkID = a.ID AND vid.LinkTypeID = 0 AND vid.WebsiteVideo = 1 " \
        "LEFT OUTER JOIN media doc ON doc.LinkID = a.ID AND doc.LinkTypeID = 0 AND doc.DocPhoto = 1 " \
        "LEFT OUTER JOIN breed bd ON bd.ID = a.BreedID " \
        "LEFT OUTER JOIN breed bd2 ON bd2.ID = a.Breed2ID " \
        "LEFT OUTER JOIN lkcoattype ct ON ct.ID = a.CoatType " +  \
        "LEFT OUTER JOIN deathreason dr ON dr.ID = a.PTSReasonID " \
        "LEFT OUTER JOIN lksmovementtype mt ON mt.ID = a.ActiveMovementType " \
        "LEFT OUTER JOIN owner ov ON ov.ID = a.OwnersVetID " \
        "LEFT OUTER JOIN owner cv ON cv.ID = a.CurrentVetID " \
        "LEFT OUTER JOIN owner oo ON oo.ID = a.OriginalOwnerID " \
        "LEFT OUTER JOIN owner bo ON bo.ID = a.BroughtInByOwnerID " \
        "LEFT OUTER JOIN adoption am ON am.ID = a.ActiveMovementID " \
        "LEFT OUTER JOIN users au ON au.UserName = am.CreatedBy " \
        "LEFT OUTER JOIN owner co ON co.ID = am.OwnerID " \
        "LEFT OUTER JOIN adoption ar ON ar.AnimalID = a.ID AND ar.MovementType = 0 AND ar.MovementDate Is Null AND ar.ReservationDate Is Not Null AND ar.ReservationCancelledDate Is Null AND ar.ID = (SELECT MAX(sar.ID) FROM adoption sar WHERE sar.AnimalID = a.ID AND sar.MovementType = 0 AND sar.MovementDate Is Null AND sar.ReservationDate Is Not Null AND sar.ReservationCancelledDate Is Null) " \
        "LEFT OUTER JOIN owner ro ON ro.ID = ar.OwnerID")

    create_view("v_animalfound", \
        "SELECT a.*, a.ID AS LFID, s.SpeciesName, b.BreedName, " \
        "c.BaseColour AS BaseColourName, x.Sex AS SexName, " \
        "o.OwnerName, o.HomeTelephone, o.WorkTelephone, o.MobileTelephone " \
        "FROM animalfound a " \
        "LEFT OUTER JOIN breed b ON a.BreedID = b.ID " \
        "INNER JOIN species s ON a.AnimalTypeID = s.ID " \
        "INNER JOIN basecolour c ON a.BaseColourID = c.ID " \
        "INNER JOIN lksex x ON a.Sex = x.ID " \
        "INNER JOIN owner o ON a.OwnerID = o.ID")

    create_view("v_animallost", \
        "SELECT a.*, a.ID AS LFID, s.SpeciesName, b.BreedName, " \
        "c.BaseColour AS BaseColourName, x.Sex AS SexName, " \
        "o.OwnerName, o.HomeTelephone, o.WorkTelephone, o.MobileTelephone " \
        "FROM animallost a " \
        "LEFT OUTER JOIN breed b ON a.BreedID = b.ID " \
        "INNER JOIN species s ON a.AnimalTypeID = s.ID " \
        "INNER JOIN basecolour c ON a.BaseColourID = c.ID " \
        "INNER JOIN lksex x ON a.Sex = x.ID " \
        "INNER JOIN owner o ON a.OwnerID = o.ID")

    create_view("v_animalmedicaltreatment", \
        "SELECT a.ShelterCode, a.AnimalName, a.Archived, a.ActiveMovementType, a.DeceasedDate, " \
        "a.ShelterLocation, am.*, amt.DateRequired, amt.DateGiven, amt.Comments AS TreatmentComments, " \
        "amt.TreatmentNumber, amt.TotalTreatments, ma.MediaName AS WebsiteMediaName, " \
        "am.ID AS RegimenID, amt.ID AS TreatmentID, " \
        "amt.GivenBy, am.Comments AS RegimenComments, " \
        "CASE WHEN a.ActiveMovementType Is Not Null AND a.ActiveMovementType > 0 THEN " \
        "(SELECT mt.MovementType FROM lksmovementtype mt WHERE mt.ID = a.ActiveMovementType) " \
        "ELSE il.LocationName END AS LocationName, " \
        "CASE WHEN a.ActiveMovementType Is Not Null AND a.ActiveMovementType > 0 THEN " \
        "'' ELSE a.ShelterLocationUnit END AS LocationUnit, " \
        "%(compositeid)s AS CompositeID, " \
        "CASE " \
        "WHEN am.TimingRule = 0 THEN 'One Off' " \
        "WHEN am.TimingRuleFrequency = 0 THEN %(daily)s " \
        "WHEN am.TimingRuleFrequency = 1 THEN %(weekly)s " \
        "WHEN am.TimingRuleFrequency = 2 THEN %(monthly)s " \
        "WHEN am.TimingRuleFrequency = 3 THEN %(yearly)s " \
        "END AS NamedFrequency, " \
        "CASE " \
        "WHEN am.TimingRule = 0 THEN '1 treatment' " \
        "WHEN am.TreatmentRule = 1 THEN 'Unspecified' " \
        "ELSE %(numbertreatments)s END AS NamedNumberOfTreatments, " \
        "CASE " \
        "WHEN am.Status = 0 THEN 'Active' " \
        "WHEN am.Status = 1 THEN 'Held' " \
        "WHEN am.Status = 2 THEN 'Completed' END AS NamedStatus " \
        "FROM animal a " \
        "LEFT OUTER JOIN media ma ON ma.LinkID = a.ID AND ma.LinkTypeID = 0 AND ma.WebsitePhoto = 1 " \
        "INNER JOIN animalmedical am ON a.ID = am.AnimalID " \
        "INNER JOIN animalmedicaltreatment amt ON amt.AnimalMedicalID = am.ID " \
        "INNER JOIN internallocation il ON il.ID = a.ShelterLocation " %
            { 
                "compositeid": db.concat(dbo, ["am.ID", "'_'", "amt.ID"]),
                "daily": db.concat(dbo, ["am.TimingRule", "' treatments every '", "am.TimingRuleNoFrequencies", "' days'"]),
                "weekly": db.concat(dbo, ["am.TimingRule", "' treatments every '", "am.TimingRuleNoFrequencies", "' weeks'"]),
                "monthly": db.concat(dbo, ["am.TimingRule", "' treatments every '", "am.TimingRuleNoFrequencies", "' months'"]),
                "yearly": db.concat(dbo, ["am.TimingRule", "' treatments every '", "am.TimingRuleNoFrequencies", "' years'"]),
                "numbertreatments": db.concat(dbo, ["(am.TimingRule * am.TotalNumberOfTreatments)", "' treatments'"])
            })

    create_view("v_animaltest", \
        "SELECT at.*, a.ShelterCode, a.Archived, a.ActiveMovementType, a.DeceasedDate, " \
        "a.AnimalName, ma.MediaName AS WebsiteMediaName, tt.TestName, tt.TestDescription, " \
        "tr.ResultName, " \
        "CASE WHEN a.ActiveMovementType Is Not Null AND a.ActiveMovementType > 0 THEN " \
        "(SELECT mt.MovementType FROM lksmovementtype mt WHERE mt.ID = a.ActiveMovementType) " \
        "ELSE il.LocationName END AS LocationName, " \
        "CASE WHEN a.ActiveMovementType Is Not Null AND a.ActiveMovementType > 0 THEN " \
        "'' ELSE a.ShelterLocationUnit END AS LocationUnit " \
        "FROM animal a " \
        "LEFT OUTER JOIN media ma ON ma.LinkID = a.ID AND ma.LinkTypeID = 0 AND ma.WebsitePhoto = 1 " \
        "INNER JOIN animaltest at ON a.ID = at.AnimalID " \
        "INNER JOIN testtype tt ON tt.ID = at.TestTypeID " \
        "LEFT OUTER JOIN testresult tr ON tr.ID = at.TestResultID " \
        "INNER JOIN internallocation il ON il.ID = a.ShelterLocation ")

    create_view("v_animalvaccination", \
        "SELECT av.*, a.ShelterCode, a.Archived, a.ActiveMovementType, a.DeceasedDate, " \
        "a.AnimalName, ma.MediaName AS WebsiteMediaName, vt.VaccinationType, vt.VaccinationDescription, " \
        "CASE WHEN a.ActiveMovementType Is Not Null AND a.ActiveMovementType > 0 THEN " \
        "(SELECT mt.MovementType FROM lksmovementtype mt WHERE mt.ID = a.ActiveMovementType) " \
        "ELSE il.LocationName END AS LocationName, " \
        "CASE WHEN a.ActiveMovementType Is Not Null AND a.ActiveMovementType > 0 THEN " \
        "'' ELSE a.ShelterLocationUnit END AS LocationUnit " \
        "FROM animal a " \
        "LEFT OUTER JOIN media ma ON ma.LinkID = a.ID AND ma.LinkTypeID = 0 AND ma.WebsitePhoto = 1 " \
        "INNER JOIN animalvaccination av ON a.ID = av.AnimalID " \
        "INNER JOIN vaccinationtype vt ON vt.ID = av.VaccinationID " \
        "INNER JOIN internallocation il ON il.ID = a.ShelterLocation ")

    create_view("v_animalwaitinglist", \
        "SELECT DISTINCT a.*, a.ID AS WLID, " \
        "s.SpeciesName AS SpeciesName, " \
        "o.OwnerName, o.OwnerSurname, o.OwnerForeNames, o.OwnerTitle, o.OwnerInitials, " \
        "o.OwnerAddress, o.OwnerTown, o.OwnerCounty, o.OwnerPostcode, " \
        "o.HomeTelephone, o.WorkTelephone, o.MobileTelephone, o.EmailAddress, " \
        "u.Urgency AS UrgencyName " \
        "FROM animalwaitinglist a " \
        "INNER JOIN species s ON s.ID = a.SpeciesID " \
        "INNER JOIN owner o ON o.ID = a.OwnerID " \
        "INNER JOIN lkurgency u ON u.ID = a.Urgency")

    ownercode = ""
    if dbo.dbtype == "MYSQL": 
        ownercode = "CONCAT(SUBSTR(UPPER(o.OwnerSurname), 1, 2), LPAD(o.ID, 6, '0'))"
    if dbo.dbtype == "POSTGRESQL": 
        ownercode = "SUBSTRING(UPPER((XPATH('/z/text()', ('<z>' || replace(replace(replace(o.OwnerSurname, '&', ''), '<', ''), '>', '') || '</z>')::xml))[1]::text) FROM 0 FOR 3) || TO_CHAR(o.ID, 'FM000000')"
    if dbo.dbtype == "SQLITE": 
        ownercode = "SUBSTR(UPPER(o.OwnerSurname), 1, 2) || o.ID"
    create_view("v_owner", \
        "SELECT DISTINCT o.*, o.ID AS PersonID, " \
        "web.MediaName AS WebsiteMediaName, " \
        "web.Date AS WebsiteMediaDate, " \
        "web.MediaNotes AS WebsiteMediaNotes, " \
        "(SELECT COUNT(oi.ID) FROM ownerinvestigation oi WHERE oi.OwnerID = o.ID) AS Investigation, " \
        "%s AS OwnerCode " \
        "FROM owner o " \
        "LEFT OUTER JOIN media web ON web.LinkID = o.ID AND web.LinkTypeID = 3 AND web.WebsitePhoto = 1" % ownercode)

    create_view("v_ownerdonation", \
        "SELECT od.ID, od.DonationTypeID, od.DonationPaymentID, dt.DonationName, od.Date, od.DateDue, " \
        "od.Donation, p.PaymentName, od.IsGiftAid, od.Frequency, fr.Frequency AS FrequencyName, od.NextCreated, " \
        "od.Comments, o.OwnerTitle, o.OwnerInitials, o.OwnerSurname, o.OwnerForenames, " \
        "o.OwnerName, a.AnimalName, a.ShelterCode, a.ID AS AnimalID, o.ID AS OwnerID, " \
        "od.MovementID, o.OwnerAddress, o.OwnerTown, o.OwnerCounty, o.OwnerPostcode, " \
        "o.HomeTelephone, o.WorkTelephone, o.MobileTelephone, o.EmailAddress, o.AdditionalFlags " \
        "FROM ownerdonation od " \
        "LEFT OUTER JOIN animal a ON a.ID = od.AnimalID " \
        "LEFT OUTER JOIN donationpayment p ON od.DonationPaymentID = p.ID " \
        "INNER JOIN owner o ON o.ID = od.OwnerID " \
        "INNER JOIN donationtype dt ON dt.ID = od.DonationTypeID " \
        "INNER JOIN lksdonationfreq fr ON fr.ID = od.Frequency ")

    create_view("v_ownervoucher", \
        "SELECT ov.*, v.VoucherName, o.OwnerName, " \
        "o.OwnerAddress, o.OwnerTown, o.OwnerCounty, o.OwnerPostcode, " \
        "o.HomeTelephone, o.WorkTelephone, o.MobileTelephone, o.EmailAddress, o.AdditionalFlags " \
        "FROM ownervoucher ov " \
        "INNER JOIN voucher v ON v.ID = ov.VoucherID " \
        "INNER JOIN owner o ON o.ID = ov.OwnerID ")

def install_db_sequences(dbo):
    """
    Installs database sequences and sets their initial values
    (only valid for PostgreSQL and if ASM3_PK_STRATEGY is 'pseq' ).
    """
    if ASM3_PK_STRATEGY != "pseq" or dbo.dbtype != "POSTGRESQL": return
    for table in TABLES:
        if table in TABLES_NO_ID_COLUMN: continue
        initialvalue = db._get_id_max(dbo, table)
        db.execute_dbupdate(dbo, "DROP SEQUENCE IF EXISTS seq_%s" % table)
        db.execute_dbupdate(dbo, "CREATE SEQUENCE seq_%s START %d" % (table, initialvalue))

def install_default_data(dbo, skip_config = False):
    """
    Installs the default dataset into the database.
    skip_config: If true, does not generate config data.
    """
    al.info("creating default data", "dbupdate.install_default_data", dbo)
    sql = sql_default_data(dbo, skip_config)
    for s in sql.split("|="):
        if s.strip() != "":
            print s.strip()
            db.execute_dbupdate(dbo, s.strip())

def reinstall_default_data(dbo):
    """
    Reinstalls all default data for the current locale. It wipes the
    database first, but leaves the configuration and dbfs tables intact.
    """
    for table in TABLES:
        if table != "dbfs" and table != "configuration" and table != "users" and table != "role" and table != "userrole":
            print "DELETE FROM %s" % table
            db.execute_dbupdate(dbo, "DELETE FROM %s" % table)
    install_default_data(dbo, True)

def install_default_media(dbo, removeFirst = False):
    """
    Installs the default media files into the dbfs
    """
    path = dbo.installpath
    if removeFirst:
        al.info("removing /internet, /templates and /report", "dbupdate.install_default_media", dbo)
        db.execute_dbupdate(dbo, "DELETE FROM dbfs WHERE Path Like '/internet%' OR Path Like '/report%' OR Path Like '/template%'")
    al.info("creating default media", "dbupdate.install_default_media", dbo)
    dbfs.create_path(dbo, "/", "internet")
    dbfs.create_path(dbo, "/internet", "littlebox")
    dbfs.put_file(dbo, "body.html", "/internet/littlebox", path + "media/internet/littlebox/body.html")
    dbfs.put_file(dbo, "foot.html", "/internet/littlebox", path + "media/internet/littlebox/foot.html")
    dbfs.put_file(dbo, "head.html", "/internet/littlebox", path + "media/internet/littlebox/head.html")
    dbfs.create_path(dbo, "/internet", "plain")
    dbfs.put_file(dbo, "body.html", "/internet/plain", path + "media/internet/plain/body.html")
    dbfs.put_file(dbo, "foot.html", "/internet/plain", path + "media/internet/plain/foot.html")
    dbfs.put_file(dbo, "heda.html", "/internet/plain", path + "media/internet/plain/head.html")
    dbfs.put_file(dbo, "redirector.html", "/internet/plain", path + "media/internet/plain/redirector.html")
    dbfs.put_file(dbo, "search.html", "/internet/plain", path + "media/internet/plain/search.html")
    dbfs.create_path(dbo, "/internet", "rss")
    dbfs.put_file(dbo, "body.html", "/internet/rss", path + "media/internet/rss/body.html")
    dbfs.put_file(dbo, "foot.html", "/internet/rss", path + "media/internet/rss/foot.html")
    dbfs.put_file(dbo, "head.html", "/internet/rss", path + "media/internet/rss/head.html")
    dbfs.create_path(dbo, "/internet", "sm.com")
    dbfs.put_file(dbo, "body.html", "/internet/sm.com", path + "media/internet/sm.com/body.html")
    dbfs.put_file(dbo, "foot.html", "/internet/sm.com", path + "media/internet/sm.com/foot.html")
    dbfs.put_file(dbo, "head.html", "/internet/sm.com", path + "media/internet/sm.com/head.html")
    dbfs.put_file(dbo, "back1.png", "/internet/sm.com", path + "media/internet/sm.com/back1.png")
    dbfs.put_file(dbo, "cat_no.png", "/internet/sm.com", path + "media/internet/sm.com/cat_no.png")
    dbfs.put_file(dbo, "cat.png", "/internet/sm.com", path + "media/internet/sm.com/cat.png")
    dbfs.put_file(dbo, "dog_no.png", "/internet/sm.com", path + "media/internet/sm.com/dog_no.png")
    dbfs.put_file(dbo, "dog.png", "/internet/sm.com", path + "media/internet/sm.com/dog.png")
    dbfs.put_file(dbo, "housetrained.png", "/internet/sm.com", path + "media/internet/sm.com/housetrained.png")
    dbfs.put_file(dbo, "kids_no.png", "/internet/sm.com", path + "media/internet/sm.com/kids_no.png")
    dbfs.put_file(dbo, "kids.png", "/internet/sm.com", path + "media/internet/sm.com/kids.png")
    dbfs.put_file(dbo, "neutered.png", "/internet/sm.com", path + "media/internet/sm.com/neutered.png")
    dbfs.put_file(dbo, "new.png", "/internet/sm.com", path + "media/internet/sm.com/new.png")
    dbfs.put_file(dbo, "updated.png", "/internet/sm.com", path + "media/internet/sm.com/updated.png")
    dbfs.put_file(dbo, "vaccinated.png", "/internet/sm.com", path + "media/internet/sm.com/vaccinated.png")
    dbfs.create_path(dbo, "/", "reports")
    dbfs.put_file(dbo, "foot.html", "/reports", path + "media/reports/foot.html")
    dbfs.put_file(dbo, "head.html", "/reports", path + "media/reports/head.html")
    dbfs.put_file(dbo, "nopic.jpg", "/reports", path + "media/reports/nopic.jpg")
    dbfs.create_path(dbo, "/", "templates")
    dbfs.put_file(dbo, "adoption_form.html", "/templates", path + "media/templates/adoption_form.html")
    dbfs.put_file(dbo, "cat_assessment_form.html", "/templates", path + "media/templates/cat_assessment_form.html")
    dbfs.put_file(dbo, "cat_cage_card.html", "/templates", path + "media/templates/cat_cage_card.html")
    dbfs.put_file(dbo, "cat_information.html", "/templates", path + "media/templates/cat_information.html")
    dbfs.put_file(dbo, "dog_assessment_form.html", "/templates", path + "media/templates/dog_assessment_form.html")
    dbfs.put_file(dbo, "dog_cage_card.html", "/templates", path + "media/templates/dog_cage_card.html")
    dbfs.put_file(dbo, "dog_information.html", "/templates", path + "media/templates/dog_information.html")
    dbfs.put_file(dbo, "fancy_cage_card.html", "/templates", path + "media/templates/fancy_cage_card.html")
    dbfs.put_file(dbo, "homecheck_form.html", "/templates", path + "media/templates/homecheck_form.html")
    dbfs.put_file(dbo, "invoice.html", "/templates", path + "media/templates/invoice.html")
    dbfs.put_file(dbo, "microchip_form.html", "/templates", path + "media/templates/microchip_form.html")
    dbfs.put_file(dbo, "receipt.html", "/templates", path + "media/templates/receipt.html")
    dbfs.put_file(dbo, "reserved.html", "/templates", path + "media/templates/reserved.html")

def install(dbo):
    """
    Handles the install of the database
    path: The path to the current directory containing the asm source
    """
    install_db_structure(dbo)
    install_db_views(dbo)
    install_default_data(dbo)
    install_db_sequences(dbo)
    install_default_media(dbo)

def dump(dbo, includeConfig = True, includeDBFS = True, includeCustomReport = True, \
        includeNonASM2 = True, includeUsers = True, deleteDBV = False, deleteFirst = True, deleteViewSeq = False, \
        escapeCR = "", uppernames = False):
    """
    Dumps all of the data in the database as DELETE/INSERT statements.
    includeConfig - include the config table
    includeDBFS - include the dbfs table
    includeCustomReport - include the custom report table
    includeUsers - include user and role tables
    deleteDBV - issue DELETE DBV from config after dump to force update/checks
    deleteFirst - issue DELETE FROM statements before INSERTs
    deleteViewSeq - issue DELETE DBViewSeqVersion from config after dump
    escapeCR - A substitute for any \n characters found in values
    """
    s = ""
    for t in TABLES:
        if not includeDBFS and t == "dbfs": continue
        if not includeCustomReport and t == "customreport": continue
        if not includeConfig and t == "configuration": continue
        if not includeUsers and (t == "users" or t == "userrole" or t == "role" or t == "accountsrole" or t == "customreportrole"): continue
        # ASM2_COMPATIBILITY
        if not includeNonASM2 and t not in TABLES_ASM2 : continue
        outtable = t
        if uppernames: outtable = t.upper()
        if deleteFirst: s += "DELETE FROM %s;\n" % outtable
        try:
            sys.stderr.write("dumping %s.., \n" % t)
            s += db.rows_to_insert_sql(outtable, db.query(dbo, "SELECT * FROM %s" % t), escapeCR)
        except:
            em = str(sys.exc_info()[0])
            sys.stderr.write("%s: WARN: %s\n" % (t, em))
    if deleteViewSeq: s += "DELETE FROM configuration WHERE ItemName LIKE 'DBViewSeqVersion';\n"
    if deleteDBV: s += "DELETE FROM configuration WHERE ItemName LIKE 'DBV';\n"
    return s

def dump_dbfs_stdout(dbo):
    """
    Dumps the DBFS table to stdout. For use with very large dbfs tables.
    """
    print "DELETE FROM dbfs;"
    rows = db.query(dbo, "SELECT ID, Name, Path FROM dbfs")
    for r in rows:
        content = db.query_string(dbo, "SELECT Content FROM dbfs WHERE ID=%d" % r["ID"])
        print "INSERT INTO dbfs (ID, Name, Path, Content) VALUES (%d, '%s', '%s', '%s');" % (r["ID"], r["NAME"], r["PATH"], content)
        del content

def dump_hsqldb(dbo, includeDBFS = True):
    """
    Produces a dump in hsqldb format for use with ASM2
    """
    # ASM2_COMPATIBILITY
    hdbo = db.DatabaseInfo()
    hdbo.dbtype = "HSQLDB"
    s = sql_structure(hdbo)
    s += dump(dbo, includeNonASM2 = False, includeDBFS = includeDBFS, escapeCR = " ")
    return s

def dump_smcom(dbo):
    """
    Dumps the database in a convenient format for import to sheltermanager.com
    """
    return dump(dbo, includeConfig = False, includeUsers = False, deleteDBV = True, deleteViewSeq = True)

def diagnostic(dbo):
    """
    Checks for and removes orphaned records and any other useful bits and pieces
    """
    def orphan(table, linktable, leftfield, rightfield):
        count = db.query_int(dbo, "SELECT COUNT(*) FROM %s LEFT OUTER JOIN %s ON %s = %s " \
            "WHERE %s Is Null" % (table, linktable, leftfield, rightfield, rightfield))
        if count > 0:
            db.execute_dbupdate(dbo, "DELETE FROM %s WHERE %s IN " \
                "(SELECT %s FROM %s LEFT OUTER JOIN %s ON %s = %s WHERE %s Is Null)" % (
                table, leftfield, leftfield, table, linktable, leftfield, rightfield, rightfield))
        return count

    return (
        orphan("adoption", "animal", "adoption.AnimalID", "animal.ID"),
        orphan("animalvaccination", "animal", "animalvaccination.AnimalID", "animal.ID"),
        orphan("animaltest", "animal", "animaltest.AnimalID", "animal.ID"),
        orphan("animalmedical", "animal", "animalmedical.AnimalID", "animal.ID"),
        orphan("animalmedicaltreatment", "animal", "animalmedicaltreatment.AnimalID", "animal.ID")
    )

def check_for_updates(dbo):
    """
    Checks to see what version the database is on and whether or
    not it needs to be upgraded. Returns true if it needs
    upgrading.
    """
    dbv = int(configuration.dbv(dbo))
    return dbv < LATEST_VERSION

def check_for_view_seq_changes(dbo):
    """
    Checks to see whether we need to recreate our views and
    sequences by looking to see if BUILD is different. Returns 
    True if we need to update.
    """
    return configuration.db_view_seq_version(dbo) != BUILD

def perform_updates(dbo):
    """
    Performs any updates that need to be performed against the 
    database. Returns the new database version.
    """
    # Lock the database - fail silently if we couldn't lock it
    if not configuration.db_lock(dbo): return ""

    try:
        # Go through our updates to see if any need running
        ver = int(configuration.dbv(dbo))
        for v in VERSIONS:
            if ver < v:
                al.info("updating database to version %d" % v, "dbupdate.perform_updates", dbo)
                # Current db version is below this update, run it
                try:
                    globals()["update_" + str(v)](dbo)
                except:
                    al.error("DB Update Error: %s" % str(sys.exc_info()[0]), "dbupdate.perform_updates", dbo, sys.exc_info())
                # Update the version
                configuration.dbv(dbo, str(v))
                ver = v
        
        # Return the new db version
        configuration.db_unlock(dbo)
        return configuration.dbv(dbo)
    finally:
        # Unlock the database for updates before we leave
        configuration.db_unlock(dbo)

def floattype(dbo):
    if dbo.dbtype == "MYSQL":
        return "DOUBLE"
    else:
        return "REAL"

def datetype(dbo):
    if dbo.dbtype == "MYSQL": 
        return "DATETIME" 
    else:
        return "TIMESTAMP"

def longtext(dbo):
    if dbo.dbtype == "MYSQL":
        return "LONGTEXT"
    else:
        return "TEXT"

def shorttext(dbo):
    if dbo.dbtype == "MYSQL":
        return "VARCHAR(255)"
    else:
        return "VARCHAR(1024)"

def remove_asm2_compatibility(dbo):
    """
    These are fields that we only maintain for compatibility with ASM2.
    One day, we will be able to remove these (note that ASM3 code still
    populates them with values, so that code can be removed too - it's
    all tagged with the ASM2_COMPATIBILITY comment).
    """
    # ASM2_COMPATIBILITY
    db.execute_dbupdate(dbo, "ALTER TABLE users DROP COLUMN SecurityMap")

def update_3000(dbo):
    path = dbo.installpath
    dbfs.put_file(dbo, "adoption_form.html", "/templates", path + "media/templates/adoption_form.html")
    dbfs.put_file(dbo, "cat_assessment_form.html", "/templates", path + "media/templates/cat_assessment_form.html")
    dbfs.put_file(dbo, "cat_cage_card.html", "/templates", path + "media/templates/cat_cage_card.html")
    dbfs.put_file(dbo, "cat_information.html", "/templates", path + "media/templates/cat_information.html")
    dbfs.put_file(dbo, "dog_assessment_form.html", "/templates", path + "media/templates/dog_assessment_form.html")
    dbfs.put_file(dbo, "dog_cage_card.html", "/templates", path + "media/templates/dog_cage_card.html")
    dbfs.put_file(dbo, "dog_information.html", "/templates", path + "media/templates/dog_information.html")
    dbfs.put_file(dbo, "fancy_cage_card.html", "/templates", path + "media/templates/fancy_cage_card.html")
    dbfs.put_file(dbo, "homecheck_form.html", "/templates", path + "media/templates/homecheck_form.html")
    dbfs.put_file(dbo, "invoice.html", "/templates", path + "media/templates/invoice.html")
    dbfs.put_file(dbo, "microchip_form.html", "/templates", path + "media/templates/microchip_form.html")
    dbfs.put_file(dbo, "receipt.html", "/templates", path + "media/templates/receipt.html")
    dbfs.put_file(dbo, "reserved.html", "/templates", path + "media/templates/reserved.html")
    if not dbfs.has_nopic(dbo):
        dbfs.put_file(dbo, "nopic.jpg", "/reports", path + "media/reports/nopic.jpg")
    db.execute_dbupdate(dbo, "CREATE TABLE messages ( ID INTEGER NOT NULL, Added %s NOT NULL, Expires %s NOT NULL, " \
        "CreatedBy %s NOT NULL, Priority INTEGER NOT NULL, Message %s NOT NULL )" % ( datetype(dbo), datetype(dbo), shorttext(dbo), longtext(dbo) ))
    db.execute_dbupdate(dbo, "CREATE UNIQUE INDEX messages_ID ON messages(ID)")
    db.execute_dbupdate(dbo, "CREATE INDEX messages_Expires ON messages(Expires)")

def update_3001(dbo):
    db.execute_dbupdate(dbo, "DELETE FROM configuration WHERE ItemName LIKE 'MappingService%'")
    db.execute_dbupdate(dbo, "INSERT INTO configuration VALUES ('%s', '%s')" % ( "MappingServiceLinkURL", "http://maps.google.com/maps?q={0}" ))
    db.execute_dbupdate(dbo, "INSERT INTO configuration VALUES ('%s', '%s')" % ( "MappingServiceEmbeddedURL", "https://maps.googleapis.com/maps/api/staticmap?center={0}&size=250x250&maptype=roadmap&sensor=false"))
    if 0 == db.query_int(dbo, "SELECT COUNT(ItemName) FROM configuration WHERE ItemName LIKE 'SystemTheme'"):
        db.execute_dbupdate(dbo, "DELETE FROM configuration WHERE ItemName LIKE 'SystemTheme'")
        db.execute_dbupdate(dbo, "INSERT INTO configuration VALUES ('%s', '%s')" % ( "SystemTheme", "smoothness" ))
    if 0 == db.query_int(dbo, "SELECT COUNT(ItemName) FROM configuration WHERE ItemName LIKE 'Timezone'"):
        db.execute_dbupdate(dbo, "DELETE FROM configuration WHERE ItemName LIKE 'Timezone'")
        db.execute_dbupdate(dbo, "INSERT INTO configuration VALUES ('%s', '%s')" % ( "Timezone", "0" ))

def update_3002(dbo):
    db.execute_dbupdate(dbo, "ALTER TABLE users ADD IPRestriction %s NULL" % longtext(dbo))
    db.execute_dbupdate(dbo, "CREATE TABLE role (ID INTEGER NOT NULL PRIMARY KEY, " \
        "Rolename %s NOT NULL, SecurityMap %s NOT NULL)" % (shorttext(dbo), longtext(dbo)))
    db.execute_dbupdate(dbo, "CREATE INDEX role_Rolename ON role(Rolename)")
    db.execute_dbupdate(dbo, "CREATE TABLE userrole (UserID INTEGER NOT NULL, " \
        "RoleID INTEGER NOT NULL)")
    db.execute_dbupdate(dbo, "CREATE INDEX userrole_UserIDRoleID ON " \
        "userrole(UserID, RoleID)")
    # Create default roles
    db.execute_dbupdate(dbo, "INSERT INTO role VALUES (1, 'Other Organisation', 'va *vavet *vav *mvam *dvad *cvad *vamv *vo *volk *vle *vvov *vdn *vla *vfa *vwl *vcr *vll *')")
    db.execute_dbupdate(dbo, "INSERT INTO role VALUES (2, 'Staff', 'aa *ca *va *vavet *da *cloa *gaf *aam *cam *dam *vam *mand *aav *vav *cav *dav *bcav *maam *mcam *mdam *mvam *bcam *daad *dcad *ddad *dvad *caad *cdad *cvad *aamv *camv *vamv *damv *ao *co *vo *do *mo *volk *ale *cle *dle *vle *vaov *vcov *vvov *oaod *ocod *odod *ovod *vdn *edt *adn *eadn *emdn *ecdn *bcn *ddn *pdn *pvd *ala *cla *dla *vla *afa *cfa *dfa *vfa *mlaf *vwl *awl *cwl *dwl *bcwl *all *cll *vll *dll *vcr *')")
    db.execute_dbupdate(dbo, "INSERT INTO role VALUES (3, 'Accountant', 'aac *vac *cac *ctrx *dac *vaov *vcov *vdov *vvov *oaod *ocod *odod *ovod *')")
    db.execute_dbupdate(dbo, "INSERT INTO role VALUES (4, 'Vet', 'va *vavet *aav *vav *cav *dav *bcav *maam *mcam *mdam *mvam *bcam *daad *dcad *ddad *dvad * ')")
    db.execute_dbupdate(dbo, "INSERT INTO role VALUES (5, 'Publisher', 'uipb *')")
    db.execute_dbupdate(dbo, "INSERT INTO role VALUES (6, 'System Admin', 'asm *cso *ml *usi *rdbu *rdbd *asu *esu *ccr *vcr *hcr *dcr *')")
    db.execute_dbupdate(dbo, "INSERT INTO role VALUES (7, 'Marketer', 'uipb *mmeo *mmea *')")
    db.execute_dbupdate(dbo, "INSERT INTO role VALUES (8, 'Investigator', 'aoi *coi *doi *voi *')")
    # Find any existing users that aren't superusers and create a
    # matching role for them
    users = db.query(dbo, "SELECT ID, UserName, SecurityMap FROM users " \
        "WHERE SuperUser = 0")
    for u in users:
        roleid = db._get_id_max(dbo, "role") 
        # If it's the guest user, use the view animals/people role
        if u["USERNAME"] == "guest":
            roleid = 1
        else:
            db.execute_dbupdate(dbo, "INSERT INTO role VALUES (%d, '%s', '%s')" % \
                ( roleid, u["USERNAME"], u["SECURITYMAP"]))
        db.execute_dbupdate(dbo, "INSERT INTO userrole VALUES (%d, %d)" % \
            ( u["ID"], roleid))

def update_3003(dbo):
    if dbo.dbtype == "MYSQL":
        db.execute_dbupdate(dbo, "ALTER TABLE configuration MODIFY ItemValue VARCHAR(16384) NOT NULL")
    elif dbo.dbtype == "POSTGRESQL":
        db.execute_dbupdate(dbo, "ALTER TABLE configuration ALTER ItemValue TYPE VARCHAR(16384)")
        
def update_3004(dbo):
    unused = dbo
    # Broken, disregard.

def update_3005(dbo):
    # 3004 was broken and deleted the mapping service by accident, so we reinstate it
    db.execute_dbupdate(dbo, "DELETE FROM configuration WHERE ItemName LIKE 'MappingService%'")
    db.execute_dbupdate(dbo, "INSERT INTO configuration VALUES ('%s', '%s')" % ( "MappingServiceLinkURL", "http://maps.google.com/maps?q={0}" ))
    db.execute_dbupdate(dbo, "INSERT INTO configuration VALUES ('%s', '%s')" % ( "MappingServiceEmbeddedURL", "https://maps.googleapis.com/maps/api/staticmap?center={0}&size=250x250&maptype=roadmap&sensor=false"))
    # Set default search sort to last changed/relevance
    db.execute_dbupdate(dbo, "DELETE FROM configuration WHERE ItemName LIKE 'RecordSearchLimit' OR ItemName Like 'SearchSort'")
    db.execute_dbupdate(dbo, "INSERT INTO configuration VALUES ('%s', '%s')" % ( "RecordSearchLimit", "1000" ))
    db.execute_dbupdate(dbo, "INSERT INTO configuration VALUES ('%s', '%s')" % ( "SearchSort", "3" ))

def update_3006(dbo):
    # Add ForName field to messages
    try:
        db.execute_dbupdate(dbo, "ALTER TABLE messages ADD ForName %s" % shorttext(dbo))
    except Exception,err:
        al.error("failed creating messages.ForName: %s" % str(err), "dbupdate.update_3006", dbo)
    db.execute_dbupdate(dbo, "UPDATE messages SET ForName = '*'")

def update_3007(dbo):
    # Add default quicklinks
    db.execute_dbupdate(dbo, "DELETE FROM configuration WHERE ItemName Like 'QuicklinksID'")
    db.execute_dbupdate(dbo, "INSERT INTO configuration VALUES ('%s', '%s')" % ( "QuicklinksID", "35,25,33,31,34,19,20"))

def update_3008(dbo):
    # Add facility for users to override the system locale
    db.execute_dbupdate(dbo, "ALTER TABLE users ADD LocaleOverride %s" % shorttext(dbo))

def update_3009(dbo):
    # Create animalfigures table to be updated each night
    sql = "CREATE TABLE animalfigures ( ID INTEGER NOT NULL, " \
        "Month INTEGER NOT NULL, " \
        "Year INTEGER NOT NULL, " \
        "OrderIndex INTEGER NOT NULL, " \
        "Code %s NOT NULL, " \
        "AnimalTypeID INTEGER NOT NULL, " \
        "SpeciesID INTEGER NOT NULL, " \
        "MaxDaysInMonth INTEGER NOT NULL, " \
        "Heading %s NOT NULL, " \
        "Bold INTEGER NOT NULL, " \
        "D1 INTEGER NOT NULL, " \
        "D2 INTEGER NOT NULL, " \
        "D3 INTEGER NOT NULL, " \
        "D4 INTEGER NOT NULL, " \
        "D5 INTEGER NOT NULL, " \
        "D6 INTEGER NOT NULL, " \
        "D7 INTEGER NOT NULL, " \
        "D8 INTEGER NOT NULL, " \
        "D9 INTEGER NOT NULL, " \
        "D10 INTEGER NOT NULL, " \
        "D11 INTEGER NOT NULL, " \
        "D12 INTEGER NOT NULL, " \
        "D13 INTEGER NOT NULL, " \
        "D14 INTEGER NOT NULL, " \
        "D15 INTEGER NOT NULL, " \
        "D16 INTEGER NOT NULL, " \
        "D17 INTEGER NOT NULL, " \
        "D18 INTEGER NOT NULL, " \
        "D19 INTEGER NOT NULL, " \
        "D20 INTEGER NOT NULL, " \
        "D21 INTEGER NOT NULL, " \
        "D22 INTEGER NOT NULL, " \
        "D23 INTEGER NOT NULL, " \
        "D24 INTEGER NOT NULL, " \
        "D25 INTEGER NOT NULL, " \
        "D26 INTEGER NOT NULL, " \
        "D27 INTEGER NOT NULL, " \
        "D28 INTEGER NOT NULL, " \
        "D29 INTEGER NOT NULL, " \
        "D30 INTEGER NOT NULL, " \
        "D31 INTEGER NOT NULL, " \
        "AVG %s NOT NULL)" % (shorttext(dbo), shorttext(dbo), floattype(dbo))
    db.execute_dbupdate(dbo, sql)
    db.execute_dbupdate(dbo, "CREATE UNIQUE INDEX animalfigures_ID ON animalfigures(ID)")
    db.execute_dbupdate(dbo, "CREATE INDEX animalfigures_AnimalTypeID ON animalfigures(AnimalTypeID)")
    db.execute_dbupdate(dbo, "CREATE INDEX animalfigures_SpeciesID ON animalfigures(SpeciesID)")
    db.execute_dbupdate(dbo, "CREATE INDEX animalfigures_Month ON animalfigures(Month)")
    db.execute_dbupdate(dbo, "CREATE INDEX animalfigures_Year ON animalfigures(Year)")

def update_3010(dbo):
    # Create person flags table
    sql = "CREATE TABLE lkownerflags ( ID INTEGER NOT NULL, " \
        "Flag %s NOT NULL)" % shorttext(dbo)
    db.execute_dbupdate(dbo, sql)
    # Add additionalflags field to person
    sql = "ALTER TABLE owner ADD AdditionalFlags %s" % longtext(dbo)
    db.execute_dbupdate(dbo, sql)

def update_3050(dbo):
    # Add default cost for vaccinations
    db.execute_dbupdate(dbo, "ALTER TABLE vaccinationtype ADD DefaultCost INTEGER NULL")
    # Add default adoption fee per species
    db.execute_dbupdate(dbo, "ALTER TABLE species ADD AdoptionFee INTEGER NULL")

def update_3051(dbo):
    # Fix incorrect field name from ASM3 initial install (it was listed
    # as TimingRuleNoFrequency instead of TimingRuleFrequency)
    try:
        db.execute_dbupdate(dbo, "ALTER TABLE medicalprofile ADD TimingRuleFrequency INTEGER NULL")
        db.execute_dbupdate(dbo, "ALTER TABLE medicalprofile DROP TimingRuleNoFrequency")
    except:
        # We don't care if this fails, it's just for broken new ASM3 installs
        pass

def update_3081(dbo):
    # Remove AdoptionFee field - it was a stupid idea
    try:
        db.execute_dbupdate(dbo, "ALTER TABLE species DROP AdoptionFee")
    except:
        # If we can't remove it, doesn't matter it will be ignored
        pass
    # Add DefaultCost to donationtype - much better idea
    db.execute_dbupdate(dbo, "ALTER TABLE donationtype ADD DefaultCost INTEGER NULL")

def update_3091(dbo):
    # Reinstated map url in 3005 did not use SSL for embedded link
    db.execute_dbupdate(dbo, "DELETE FROM configuration WHERE ItemName LIKE 'MappingService%'")
    db.execute_dbupdate(dbo, "INSERT INTO configuration VALUES ('%s', '%s')" % ( "MappingServiceLinkURL", "http://maps.google.com/maps?q={0}" ))
    db.execute_dbupdate(dbo, "INSERT INTO configuration VALUES ('%s', '%s')" % ( "MappingServiceEmbeddedURL", "https://maps.googleapis.com/maps/api/staticmap?center={0}&size=250x250&maptype=roadmap&sensor=false"))
    # Add ExcludeFromPublish field to media
    db.execute_dbupdate(dbo, "ALTER TABLE media ADD ExcludeFromPublish INTEGER")
    db.execute_dbupdate(dbo, "UPDATE media SET ExcludeFromPublish = 0")

def update_3092(dbo):
    # Added last publish date for meetapet.com
    db.execute_dbupdate(dbo, "ALTER TABLE media ADD LastPublishedMP " + datetype(dbo))

def update_3093(dbo):
    # Create animalfiguresannual table to be updated each night
    sql = "CREATE TABLE animalfiguresannual ( ID INTEGER NOT NULL, " \
        "Year INTEGER NOT NULL, " \
        "OrderIndex INTEGER NOT NULL, " \
        "Code %s NOT NULL, " \
        "AnimalTypeID INTEGER NOT NULL, " \
        "SpeciesID INTEGER NOT NULL, " \
        "GroupHeading %s NOT NULL, " \
        "Heading %s NOT NULL, " \
        "Bold INTEGER NOT NULL, " \
        "M1 INTEGER NOT NULL, " \
        "M2 INTEGER NOT NULL, " \
        "M3 INTEGER NOT NULL, " \
        "M4 INTEGER NOT NULL, " \
        "M5 INTEGER NOT NULL, " \
        "M6 INTEGER NOT NULL, " \
        "M7 INTEGER NOT NULL, " \
        "M8 INTEGER NOT NULL, " \
        "M9 INTEGER NOT NULL, " \
        "M10 INTEGER NOT NULL, " \
        "M11 INTEGER NOT NULL, " \
        "M12 INTEGER NOT NULL, " \
        "Total INTEGER NOT NULL)" % (shorttext(dbo), shorttext(dbo), shorttext(dbo))
    db.execute_dbupdate(dbo, sql)
    db.execute_dbupdate(dbo, "CREATE UNIQUE INDEX animalfiguresannual_ID ON animalfiguresannual(ID)")
    db.execute_dbupdate(dbo, "CREATE INDEX animalfiguresannual_AnimalTypeID ON animalfiguresannual(AnimalTypeID)")
    db.execute_dbupdate(dbo, "CREATE INDEX animalfiguresannual_SpeciesID ON animalfiguresannual(SpeciesID)")
    db.execute_dbupdate(dbo, "CREATE INDEX animalfiguresannual_Year ON animalfiguresannual(Year)")

def update_3094(dbo):
    # Added last publish date for helpinglostpets.com
    db.execute_dbupdate(dbo, "ALTER TABLE media ADD LastPublishedHLP " + datetype(dbo))

def update_3110(dbo):
    # Add PetLinkSentDate
    db.execute_dbupdate(dbo, "ALTER TABLE animal ADD PetLinkSentDate " + datetype(dbo)) 

def update_3111(dbo):
    l = dbo.locale
    # New additional field types to indicate location
    db.execute_dbupdate(dbo, "UPDATE lksfieldlink SET LinkType = '%s' WHERE ID = 0" % _("Animal - Additional", l))
    db.execute_dbupdate(dbo, "UPDATE lksfieldlink SET LinkType = '%s' WHERE ID = 1" % _("Person - Additional", l))
    db.execute_dbupdate(dbo, "INSERT INTO lksfieldlink VALUES (2, '%s')" % _("Animal - Details", l))
    db.execute_dbupdate(dbo, "INSERT INTO lksfieldlink VALUES (3, '%s')" % _("Animal - Notes", l))
    db.execute_dbupdate(dbo, "INSERT INTO lksfieldlink VALUES (4, '%s')" % _("Animal - Entry", l))
    db.execute_dbupdate(dbo, "INSERT INTO lksfieldlink VALUES (5, '%s')" % _("Animal - Health and Identification", l))
    db.execute_dbupdate(dbo, "INSERT INTO lksfieldlink VALUES (6, '%s')" % _("Animal - Death", l))
    db.execute_dbupdate(dbo, "INSERT INTO lksfieldlink VALUES (7, '%s')" % _("Person - Name and Address", l))
    db.execute_dbupdate(dbo, "INSERT INTO lksfieldlink VALUES (8, '%s')" % _("Person - Type", l))

def update_3120(dbo):
    # This stuff only applies to MySQL databases - we have to import a lot of these
    # and if they were created by ASM3 they don't quite match our 2870 upgrade schemas
    # as I accidentally had createdby/lastchangedby fields in 3 tables that shouldn't
    # have been there and there was a typo in the lastpublishedp911 field (missing the p)
    if dbo.dbtype != "MYSQL": 
        return
    def column_exists(table, column):
        """ Returns True if the column exists for the table given """
        try:
            db.query(dbo, "SELECT %s FROM %s LIMIT 1" % (column, table))
            return True
        except:
            return False
    if column_exists("diarytaskdetail", "createdby"):
        db.execute_dbupdate(dbo, "ALTER TABLE diarytaskdetail DROP COLUMN createdby")
        db.execute_dbupdate(dbo, "ALTER TABLE diarytaskdetail DROP COLUMN createddate")
        db.execute_dbupdate(dbo, "ALTER TABLE diarytaskdetail DROP COLUMN lastchangedby")
        db.execute_dbupdate(dbo, "ALTER TABLE diarytaskdetail DROP COLUMN lastchangeddate")
    if column_exists("diarytaskhead", "createdby"):
        db.execute_dbupdate(dbo, "ALTER TABLE diarytaskhead DROP COLUMN createdby")
        db.execute_dbupdate(dbo, "ALTER TABLE diarytaskhead DROP COLUMN createddate")
        db.execute_dbupdate(dbo, "ALTER TABLE diarytaskhead DROP COLUMN lastchangedby")
        db.execute_dbupdate(dbo, "ALTER TABLE diarytaskhead DROP COLUMN lastchangeddate")
    if column_exists("media", "createdby"):
        db.execute_dbupdate(dbo, "ALTER TABLE media DROP COLUMN createdby")
        db.execute_dbupdate(dbo, "ALTER TABLE media DROP COLUMN createddate")
        db.execute_dbupdate(dbo, "ALTER TABLE media DROP COLUMN lastchangedby")
        db.execute_dbupdate(dbo, "ALTER TABLE media DROP COLUMN lastchangeddate")
    if column_exists("media", "lastpublished911"):
        db.execute_dbupdate(dbo, "ALTER TABLE media CHANGE COLUMN lastpublished911 lastpublishedp911 DATETIME")

def update_3121(dbo):
    # Added user email address
    db.execute_dbupdate(dbo, "ALTER TABLE users ADD EmailAddress %s" % shorttext(dbo))

def update_3122(dbo):
    # Switch shelter animals quicklink for shelter view
    # This will fail on locked databases, but shouldn't be an issue.
    links = configuration.quicklinks_id(dbo)
    links = links.replace("35", "40")
    configuration.quicklinks_id(dbo, links)

def update_3123(dbo):
    # Add the monthly animal figures total column
    db.execute_dbupdate(dbo, "ALTER TABLE animalfigures ADD Total %s" % shorttext(dbo))

def update_3200(dbo):
    # Add the trial adoption fields to the adoption table
    db.execute_dbupdate(dbo, "ALTER TABLE adoption ADD IsTrial INTEGER")
    db.execute_dbupdate(dbo, "ALTER TABLE adoption ADD TrialEndDate " + datetype(dbo))
    db.execute_dbupdate(dbo, "CREATE INDEX adoption_TrialEndDate ON adoption(TrialEndDate)")

def update_3201(dbo):
    # Add the has trial adoption denormalised field to the animal table and update it
    try:
        db.execute_dbupdate(dbo, "ALTER TABLE animal ADD HasTrialAdoption INTEGER")
    except Exception,err:
        al.error("failed creating animal.HasTrialAdoption: %s" % str(err), "dbupdate.update_3201", dbo)
    db.execute_dbupdate(dbo, "UPDATE animal SET HasTrialAdoption = 0")
    db.execute_dbupdate(dbo, "UPDATE adoption SET IsTrial = 0 WHERE IsTrial Is Null")

def update_3202(dbo):
    # Set default value for HasTrialAdoption
    db.execute_dbupdate(dbo, "UPDATE animal SET HasTrialAdoption = 1 WHERE EXISTS(SELECT ID FROM adoption ad WHERE ad.IsTrial = 1 AND ad.AnimalID = animal.ID)")

def update_3203(dbo):
    l = dbo.locale
    # Add Trial Adoption movement type
    db.execute_dbupdate(dbo, "INSERT INTO lksmovementtype (ID, MovementType) VALUES (11, %s)" % db.ds(_("Trial Adoption", l)))

def update_3204(dbo):
    # Quicklinks format has changed, regenerate them
    links = configuration.quicklinks_id(dbo)
    configuration.quicklinks_id(dbo, links)

def update_3210(dbo):
    # Anyone using MySQL who created their database with the db
    # initialiser here will have some short columns as CLOB
    # wasn't mapped properly
    if dbo.dbtype == "MYSQL":
        db.execute_dbupdate(dbo, "ALTER TABLE dbfs MODIFY Content LONGTEXT")
        db.execute_dbupdate(dbo, "ALTER TABLE media MODIFY MediaNotes LONGTEXT NOT NULL")
        db.execute_dbupdate(dbo, "ALTER TABLE log MODIFY Comments LONGTEXT NOT NULL")

def update_3211(dbo):
    # People who upgraded from ASM2 will find that some of their address fields
    # are a bit short - particularly if they are using unicode chars
    fields = [ "OwnerTitle", "OwnerInitials", "OwnerForeNames", "OwnerSurname", 
        "OwnerName", "OwnerAddress", "OwnerTown", "OwnerCounty", "OwnerPostcode", 
        "HomeTelephone", "WorkTelephone", "MobileTelephone", "EmailAddress" ]
    for f in fields:
        if dbo.dbtype == "MYSQL":
            db.execute_dbupdate(dbo, "ALTER TABLE owner MODIFY %s %s NOT NULL" % (f, shorttext(dbo)))
        elif dbo.dbtype == "POSTGRESQL":
            db.execute_dbupdate(dbo, "ALTER TABLE owner ALTER %s TYPE %s" % (f, shorttext(dbo)))

def update_3212(dbo):
    # Many of our lookup fields are too short for foreign languages
    fields = [ "animaltype.AnimalType", "animaltype.AnimalDescription", "basecolour.BaseColour", "basecolour.BaseColourDescription",
        "breed.BreedName", "breed.BreedDescription", "lkcoattype.CoatType", "costtype.CostTypeName", "costtype.CostTypeDescription",
        "deathreason.ReasonName", "deathreason.ReasonDescription", "diet.DietName", "diet.DietDescription", 
        "donationtype.DonationName", "donationtype.DonationDescription", "entryreason.ReasonName", "entryreason.ReasonDescription",
        "internallocation.LocationName", "internallocation.LocationDescription", "logtype.LogTypeName", "logtype.LogTypeDescription",
        "lksmovementtype.MovementType",  "lkownerflags.Flag", "lksex.Sex", "lksize.Size", "lksyesno.Name", "lksynun.Name", 
        "lksposneg.Name", "species.SpeciesName", "species.SpeciesDescription", "lkurgency.Urgency", 
        "vaccinationtype.VaccinationType", "vaccinationtype.VaccinationDescription", "voucher.VoucherName", "voucher.VoucherDescription",
        "accounts.Code", "accounts.Description", "accountstrx.Description",
        "animal.TimeOnShelter", "animal.AnimalAge", "animalfigures.Heading", "animalfiguresannual.Heading", 
        "animalfiguresannual.GroupHeading", "animalwaitinglist.AnimalDescription",
        "animalmedical.TreatmentName", "animalmedical.Dosage", "diary.Subject", "medicalprofile.TreatmentName", 
        "medicalprofile.Dosage", "medicalprofile.ProfileName" ]
    for f in fields:
        table, field = f.split(".")
        try:
            if dbo.dbtype == "MYSQL":
                db.execute_dbupdate(dbo, "ALTER TABLE %s MODIFY %s %s NOT NULL" % (table, field, shorttext(dbo)))
            elif dbo.dbtype == "POSTGRESQL":
                db.execute_dbupdate(dbo, "ALTER TABLE %s ALTER %s TYPE %s" % (table, field, shorttext(dbo)))
        except Exception,err:
            al.error("failed extending %s: %s" % (f, str(err)), "dbupdate.update_3212", dbo)

def update_3213(dbo):
    try:
        # Make displaylocationname and displaylocationstring denormalised fields
        db.execute_dbupdate(dbo, "ALTER TABLE animal ADD DisplayLocationName %s" % shorttext(dbo))
        db.execute_dbupdate(dbo, "ALTER TABLE animal ADD DisplayLocationString %s" % shorttext(dbo))
    except Exception,err:
        al.error("failed creating animal.DisplayLocationName/String: %s" % str(err), "dbupdate.update_3213", dbo)

    # Default the values for them
    db.execute_dbupdate(dbo, "UPDATE animal SET DisplayLocationName = " \
        "CASE " \
        "WHEN animal.Archived = 0 AND animal.ActiveMovementType = 2 THEN " \
        "(SELECT MovementType FROM lksmovementtype WHERE ID=animal.ActiveMovementType) " \
        "WHEN animal.Archived = 0 AND animal.ActiveMovementType = 1 AND animal.HasTrialAdoption = 1 THEN " \
        "(SELECT MovementType FROM lksmovementtype WHERE ID=11) " \
        "WHEN animal.Archived = 1 AND animal.DeceasedDate Is Not Null AND animal.ActiveMovementID = 0 THEN " \
        "(SELECT ReasonName FROM deathreason WHERE ID = animal.PTSReasonID) " \
        "WHEN animal.Archived = 1 AND animal.DeceasedDate Is Not Null AND animal.ActiveMovementID <> 0 THEN " \
        "(SELECT MovementType FROM lksmovementtype WHERE ID=animal.ActiveMovementType) " \
        "WHEN animal.Archived = 1 AND animal.DeceasedDate Is Null AND animal.ActiveMovementID <> 0 THEN " \
        "(SELECT MovementType FROM lksmovementtype WHERE ID=animal.ActiveMovementType) " \
        "ELSE " \
        "(SELECT LocationName FROM internallocation WHERE ID=animal.ShelterLocation) " \
        "END")
    db.execute_dbupdate(dbo, "UPDATE animal SET DisplayLocationString = DisplayLocationName")

def update_3214(dbo):
    # More short fields
    fields = [ "diarytaskhead.Name", "diarytaskdetail.Subject", "diarytaskdetail.WhoFor", "lksdonationfreq.Frequency",
        "lksloglink.LinkType", "lksdiarylink.LinkType", "lksfieldlink.LinkType", "lksfieldtype.FieldType",
        "lksmedialink.LinkType", "lksdiarylink.LinkType" ]
    for f in fields:
        table, field = f.split(".")
        try:
            if dbo.dbtype == "MYSQL":
                db.execute_dbupdate(dbo, "ALTER TABLE %s MODIFY %s %s NOT NULL" % (table, field, shorttext(dbo)))
            elif dbo.dbtype == "POSTGRESQL":
                db.execute_dbupdate(dbo, "ALTER TABLE %s ALTER %s TYPE %s" % (table, field, shorttext(dbo)))
        except Exception,err:
            al.error("failed extending %s: %s" % (f, str(err)), "dbupdate.update_3214", dbo)

def update_3215(dbo):
    # Rename DisplayLocationString column to just DisplayLocation and ditch DisplayLocationName - it should be calculated
    try:
        db.execute_dbupdate(dbo, "ALTER TABLE animal ADD DisplayLocation %s" % shorttext(dbo))
    except:
        al.error("failed creating animal.DisplayLocation.", "dbupdate.update_3215", dbo)
    try:
        db.execute_dbupdate(dbo, "UPDATE animal SET DisplayLocation = DisplayLocationString")
    except:
        al.error("failed copying DisplayLocationString->DisplayLocation", "dbupdate.update_3215", dbo)
    try:
        db.execute_dbupdate(dbo, "ALTER TABLE animal DROP COLUMN DisplayLocationName")
        db.execute_dbupdate(dbo, "ALTER TABLE animal DROP COLUMN DisplayLocationString")
    except:
        al.error("failed removing DisplayLocationName and DisplayLocationString", "dbupdate.update_3215", dbo)

def update_3216(dbo):
    l = dbo.locale
    # Add the new mediatype field to media and create the link table
    db.execute_dbupdate(dbo, "ALTER TABLE media ADD MediaType INTEGER")
    db.execute_dbupdate(dbo, "ALTER TABLE media ADD WebsiteVideo INTEGER")
    db.execute_dbupdate(dbo, "UPDATE media SET MediaType = 0, WebsiteVideo = 0")
    db.execute_dbupdate(dbo, "CREATE TABLE lksmediatype ( ID INTEGER NOT NULL, MediaType %s NOT NULL )" % ( shorttext(dbo)))
    db.execute_dbupdate(dbo, "CREATE UNIQUE INDEX lksmediatype_ID ON lksmediatype(ID)")
    db.execute_dbupdate(dbo, "INSERT INTO lksmediatype (ID, MediaType) VALUES (%d, '%s')" % (0, _("File", l)))
    db.execute_dbupdate(dbo, "INSERT INTO lksmediatype (ID, MediaType) VALUES (%d, '%s')" % (1, _("Document Link", l)))
    db.execute_dbupdate(dbo, "INSERT INTO lksmediatype (ID, MediaType) VALUES (%d, '%s')" % (2, _("Video Link", l)))

def update_3217(dbo):
    # Add asilomar fields for US users
    db.execute_dbupdate(dbo, "ALTER TABLE animal ADD AsilomarIsTransferExternal INTEGER")
    db.execute_dbupdate(dbo, "ALTER TABLE animal ADD AsilomarIntakeCategory INTEGER")
    db.execute_dbupdate(dbo, "ALTER TABLE animal ADD AsilomarOwnerRequestedEuthanasia INTEGER")
    db.execute_dbupdate(dbo, "UPDATE animal SET AsilomarIsTransferExternal = 0, AsilomarIntakeCategory = 0, AsilomarOwnerRequestedEuthanasia = 0")

def update_3218(dbo):
    # Broken previously by missing field type
    try:
        db.execute_dbupdate(dbo, "ALTER TABLE animal ADD AsilomarOwnerRequestedEuthanasia INTEGER")
    except Exception,err:
        al.error("failed creating animal.AsilomarOwnerRequestedEuthanasia: %s" % str(err), "dbupdate.update_3218", dbo)
    db.execute_dbupdate(dbo, "UPDATE animal SET AsilomarIsTransferExternal = 0, AsilomarIntakeCategory = 0, AsilomarOwnerRequestedEuthanasia = 0")

def update_3220(dbo):
    # Create animalfiguresasilomar table to be updated each night
    # for US shelters with the option on
    sql = "CREATE TABLE animalfiguresasilomar ( ID INTEGER NOT NULL, " \
        "Year INTEGER NOT NULL, " \
        "OrderIndex INTEGER NOT NULL, " \
        "Code %s NOT NULL, " \
        "Heading %s NOT NULL, " \
        "Bold INTEGER NOT NULL, " \
        "Cat INTEGER NOT NULL, " \
        "Dog INTEGER NOT NULL, " \
        "Total INTEGER NOT NULL)" % (shorttext(dbo), shorttext(dbo))
    db.execute_dbupdate(dbo, sql)
    db.execute_dbupdate(dbo, "CREATE UNIQUE INDEX animalfiguresasilomar_ID ON animalfiguresasilomar(ID)")
    db.execute_dbupdate(dbo, "CREATE INDEX animalfiguresasilomar_Year ON animalfiguresasilomar(Year)")

def update_3221(dbo):
    # More short fields
    fields = [ "activeuser.UserName", "customreport.Title", "customreport.Category" ]
    for f in fields:
        table, field = f.split(".")
        try:
            if dbo.dbtype == "MYSQL":
                db.execute_dbupdate(dbo, "ALTER TABLE %s MODIFY %s %s NOT NULL" % (table, field, shorttext(dbo)))
            elif dbo.dbtype == "POSTGRESQL":
                db.execute_dbupdate(dbo, "ALTER TABLE %s ALTER %s TYPE %s" % (table, field, shorttext(dbo)))
        except Exception,err:
            al.error("failed extending %s: %s" % (f, str(err)), "dbupdate.update_3221", dbo)

def update_3222(dbo):
    # Person investigation table
    db.execute_dbupdate(dbo, "CREATE TABLE ownerinvestigation ( ID INTEGER NOT NULL, " \
        "OwnerID INTEGER NOT NULL, Date %s NOT NULL, Notes %s NOT NULL, " \
        "RecordVersion INTEGER, CreatedBy %s, CreatedDate %s, " \
        "LastChangedBy %s, LastChangedDate %s)" % \
        (datetype(dbo), longtext(dbo), shorttext(dbo), datetype(dbo), shorttext(dbo), datetype(dbo)))
    db.execute_dbupdate(dbo, "CREATE UNIQUE INDEX ownerinvestigation_ID ON ownerinvestigation(ID)")
    db.execute_dbupdate(dbo, "CREATE INDEX ownerinvestigation_Date ON ownerinvestigation(Date)")

def update_3223(dbo):
    # PostgreSQL databases have been using VARCHAR(16384) as longtext when
    # they really shouldn't. Let's switch those fields to be TEXT instead.
    if dbo.dbtype != "POSTGRESQL": return
    fields = [ "activeuser.Messages", "additionalfield.LookupValues", "additional.Value", "adoption.ReasonForReturn", "adoption.Comments", "animal.Markings", "animal.HiddenAnimalDetails", "animal.AnimalComments", "animal.ReasonForEntry", "animal.ReasonNO", "animal.HealthProblems", "animal.PTSReason", "animalcost.Description", "animal.AnimalComments", "animalfound.DistFeat", "animalfound.Comments", "animallitter.Comments", "animallost.DistFeat", "animallost.Comments", "animalmedical.Comments", "animalmedicaltreatment.Comments", "animalvaccination.Comments", "animalwaitinglist.ReasonForWantingToPart", "animalwaitinglist.ReasonForRemoval", "animalwaitinglist.Comments", "audittrail.Description", "customreport.Description", "diary.Subject", "diary.Note", "diarytaskdetail.Subject", "diarytaskdetail.Note", "log.Comments", "media.MediaNotes", "medicalprofile.Comments", "messages.Message", "owner.Comments", "owner.AdditionalFlags", "owner.HomeCheckAreas", "ownerdonation.Comments", "ownerinvestigation.Notes", "ownervoucher.Comments", "role.SecurityMap", "users.SecurityMap", "users.IPRestriction", "configuration.ItemValue", "customreport.SQLCommand", "customreport.HTMLBody" ]
    for f in fields:
        table, field = f.split(".")
        try:
            db.execute_dbupdate(dbo, "ALTER TABLE %s ALTER %s TYPE %s" % (table, field, longtext(dbo)))
        except Exception,err:
            al.error("failed switching to TEXT %s: %s" % (f, str(err)), "dbupdate.update_3223", dbo)

def update_3224(dbo):
    # AVG is a reserved keyword in some SQL dialects, change that field
    try:
        if dbo.dbtype == "MYSQL":
            db.execute_dbupdate(dbo, "ALTER TABLE animalfigures CHANGE AVG AVERAGE %s NOT NULL" % floattype(dbo))
        elif dbo.dbtype == "POSTGRESQL":
            db.execute_dbupdate(dbo, "ALTER TABLE animalfigures RENAME COLUMN AVG TO AVERAGE")
        elif dbo.dbtype == "SQLITE":
            db.execute_dbupdate(dbo, "ALTER TABLE animalfigures ADD AVERAGE %s" % floattype(dbo))
    except Exception,err:
        al.error("failed renaming AVG to AVERAGE: %s" % str(err), "dbupdate.update_3224", dbo)

def update_3225(dbo):
    # Make sure the ADOPTIONFEE mistake is really gone
    db.execute_dbupdate(dbo, "ALTER TABLE species DROP COLUMN AdoptionFee")

def update_3300(dbo):
    # Add diary comments field
    db.execute_dbupdate(dbo, "ALTER TABLE diary ADD Comments %s" % longtext(dbo))

def update_3301(dbo):
    # Add the accountsrole table
    db.execute_dbupdate(dbo, "CREATE TABLE accountsrole (AccountID INTEGER NOT NULL, " \
        "RoleID INTEGER NOT NULL, CanView INTEGER NOT NULL, CanEdit INTEGER NOT NULL)")
    db.execute_dbupdate(dbo, "CREATE UNIQUE INDEX accountsrole_AccountIDRoleID ON accountsrole(AccountID, RoleID)")

def update_3302(dbo):
    # Add default cost fields to costtype and voucher
    db.execute_dbupdate(dbo, "ALTER TABLE costtype ADD DefaultCost INTEGER")
    db.execute_dbupdate(dbo, "ALTER TABLE voucher ADD DefaultCost INTEGER")

def update_3303(dbo):
    # Add theme override to users
    db.execute_dbupdate(dbo, "ALTER TABLE users ADD ThemeOverride %s" % shorttext(dbo))

def update_3304(dbo):
    # Add index to configuration ItemName field
    db.execute_dbupdate(dbo, "CREATE INDEX configuration_ItemName ON configuration(ItemName)")

def update_3305(dbo):
    # Add IsHold and IsQuarantine fields
    db.execute_dbupdate(dbo, "ALTER TABLE animal ADD IsHold INTEGER")
    db.execute_dbupdate(dbo, "ALTER TABLE animal ADD IsQuarantine INTEGER")
    db.execute_dbupdate(dbo, "UPDATE animal SET IsHold = 0, IsQuarantine = 0")

def update_3306(dbo):
    # Add HoldUntilDate
    db.execute_dbupdate(dbo, "ALTER TABLE animal ADD HoldUntilDate %s" % datetype(dbo))

def update_3307(dbo):
    # Create new animaltest tables
    sql = "CREATE TABLE animaltest (ID INTEGER NOT NULL PRIMARY KEY, " \
        "AnimalID INTEGER NOT NULL, " \
        "TestTypeID INTEGER NOT NULL, " \
        "TestResultID INTEGER NOT NULL, " \
        "DateOfTest %(date)s, " \
        "DateRequired %(date)s NOT NULL, " \
        "Cost INTEGER, " \
        "Comments %(long)s, " \
        "RecordVersion INTEGER, " \
        "CreatedBy %(short)s, " \
        "CreatedDate %(date)s, " \
        "LastChangedBy %(short)s, " \
        "LastChangedDate %(date)s)" % { "date": datetype(dbo), "long": longtext(dbo), "short": shorttext(dbo)}
    db.execute_dbupdate(dbo, sql)
    sql = "CREATE INDEX animaltest_AnimalID ON animaltest(AnimalID)"
    db.execute_dbupdate(dbo, sql)
    sql = "CREATE TABLE testtype (ID INTEGER NOT NULL PRIMARY KEY, " \
        "TestName %(short)s NOT NULL, " \
        "TestDescription %(long)s, " \
            "DefaultCost INTEGER)" % { "short": shorttext(dbo), "long": longtext(dbo) }
    db.execute_dbupdate(dbo, sql)
    sql = "CREATE TABLE testresult (ID INTEGER NOT NULL PRIMARY KEY, " \
        "ResultName %(short)s NOT NULL, " \
        "ResultDescription %(long)s)" % { "short": shorttext(dbo), "long": longtext(dbo) }
    db.execute_dbupdate(dbo, sql)

def update_3308(dbo):
    # Create intial data for testtype and testresult tables
    l = dbo.locale
    db.execute_dbupdate(dbo, "INSERT INTO testresult (ID, ResultName) VALUES (1, '" + _("Unknown", l) + "')")
    db.execute_dbupdate(dbo, "INSERT INTO testresult (ID, ResultName) VALUES (2, '" + _("Negative", l) + "')")
    db.execute_dbupdate(dbo, "INSERT INTO testresult (ID, ResultName) VALUES (3, '" + _("Positive", l) + "')")
    db.execute_dbupdate(dbo, "INSERT INTO testtype (ID, TestName, DefaultCost) VALUES (1, '" + _("FIV", l) + "', 0)")
    db.execute_dbupdate(dbo, "INSERT INTO testtype (ID, TestName, DefaultCost) VALUES (2, '" + _("FLV", l) + "', 0)")
    db.execute_dbupdate(dbo, "INSERT INTO testtype (ID, TestName, DefaultCost) VALUES (3, '" + _("Heartworm", l) + "', 0)")

def update_3309(dbo):
    fiv = db.query(dbo, "SELECT ID, CombiTestDate, CombiTestResult FROM animal WHERE CombiTested = 1")
    al.debug("found %d fiv results to convert" % len(fiv), "update_3309", dbo)
    for f in fiv:
        ntestid = db._get_id_max(dbo, "animaltest")
        sql = db.make_insert_user_sql(dbo, "animaltest", "update", ( 
            ( "ID", db.di(ntestid)),
            ( "AnimalID", db.di(f["ID"])),
            ( "TestTypeID", db.di(1)),
            ( "TestResultID", db.di(f["COMBITESTRESULT"] + 1)),
            ( "DateOfTest", db.dd(f["COMBITESTDATE"])),
            ( "DateRequired", db.dd(f["COMBITESTDATE"])),
            ( "Cost", db.di(0)),
            ( "Comments", db.ds(""))
            ))
        try:
            db.execute_dbupdate(dbo, sql)
        except Exception,err:
            al.error("fiv: " + str(err), "dbupdate.update_3309", dbo)
    flv = db.query(dbo, "SELECT ID, CombiTestDate, FLVResult FROM animal WHERE CombiTested = 1")
    al.debug("found %d flv results to convert" % len(flv), "update_3309", dbo)
    for f in flv:
        ntestid = db._get_id_max(dbo, "animaltest")
        sql = db.make_insert_user_sql(dbo, "animaltest", "update", ( 
            ( "ID", db.di(ntestid)),
            ( "AnimalID", db.di(f["ID"])),
            ( "TestTypeID", db.di(2)),
            ( "TestResultID", db.di(f["FLVRESULT"] + 1)),
            ( "DateOfTest", db.dd(f["COMBITESTDATE"])),
            ( "DateRequired", db.dd(f["COMBITESTDATE"])),
            ( "Cost", db.di(0)),
            ( "Comments", db.ds(""))
            ))
        try:
            db.execute_dbupdate(dbo, sql)
        except Exception,err:
            al.error("flv: " + str(err), "dbupdate.update_3309", dbo)

    hw = db.query(dbo, "SELECT ID, HeartwormTestDate, HeartwormTestResult FROM animal WHERE HeartwormTested = 1")
    al.debug("found %d heartworm results to convert" % len(hw), "update_3309", dbo)
    for f in hw:
        ntestid = db._get_id_max(dbo, "animaltest")
        sql = db.make_insert_user_sql(dbo, "animaltest", "update", ( 
            ( "ID", db.di(ntestid)),
            ( "AnimalID", db.di(f["ID"])),
            ( "TestTypeID", db.di(3)),
            ( "TestResultID", db.di(f["HEARTWORMTESTRESULT"] + 1)),
            ( "DateOfTest", db.dd(f["HEARTWORMTESTDATE"])),
            ( "DateRequired", db.dd(f["HEARTWORMTESTDATE"])),
            ( "Cost", db.di(0)),
            ( "Comments", db.ds(""))
            ))
        try:
            db.execute_dbupdate(dbo, sql)
        except Exception,err:
            al.error("hw: " + str(err), "dbupdate.update_3309", dbo)

def update_33010(dbo):
    # Add new additional field types and locations
    l = dbo.locale
    db.execute_dbupdate(dbo, "INSERT INTO lksfieldtype (ID, FieldType) VALUES (7, '" + _("Multi-Lookup", l) + "')")
    db.execute_dbupdate(dbo, "INSERT INTO lksfieldtype (ID, FieldType) VALUES (8, '" + _("Animal", l) + "')")
    db.execute_dbupdate(dbo, "INSERT INTO lksfieldtype (ID, FieldType) VALUES (9, '" + _("Person", l) + "')")
    db.execute_dbupdate(dbo, "INSERT INTO lksfieldlink (ID, LinkType) VALUES (9, '" + _("Lost Animal - Additional", l) + "')")
    db.execute_dbupdate(dbo, "INSERT INTO lksfieldlink (ID, LinkType) VALUES (10, '" + _("Lost Animal - Details", l) + "')")
    db.execute_dbupdate(dbo, "INSERT INTO lksfieldlink (ID, LinkType) VALUES (11, '" + _("Found Animal - Additional", l) + "')")
    db.execute_dbupdate(dbo, "INSERT INTO lksfieldlink (ID, LinkType) VALUES (12, '" + _("Found Animal - Details", l) + "')")
    db.execute_dbupdate(dbo, "INSERT INTO lksfieldlink (ID, LinkType) VALUES (13, '" + _("Waiting List - Additional", l) + "')")
    db.execute_dbupdate(dbo, "INSERT INTO lksfieldlink (ID, LinkType) VALUES (14, '" + _("Waiting List - Details", l) + "')")
    db.execute_dbupdate(dbo, "INSERT INTO lksfieldlink (ID, LinkType) VALUES (15, '" + _("Waiting List - Removal", l) + "')")

def update_33011(dbo):
    # Add donationpayment table and data
    l = dbo.locale
    sql = "CREATE TABLE donationpayment (ID INTEGER NOT NULL PRIMARY KEY, " \
        "PaymentName %(short)s NOT NULL, " \
        "PaymentDescription %(long)s ) " % { "short": shorttext(dbo), "long": longtext(dbo) }
    db.execute_dbupdate(dbo, sql)
    db.execute_dbupdate(dbo, "INSERT INTO donationpayment (ID, PaymentName) VALUES (1, '" + _("Cash", l) + "')")
    db.execute_dbupdate(dbo, "INSERT INTO donationpayment (ID, PaymentName) VALUES (2, '" + _("Cheque", l) + "')")
    db.execute_dbupdate(dbo, "INSERT INTO donationpayment (ID, PaymentName) VALUES (3, '" + _("Credit Card", l) + "')")
    db.execute_dbupdate(dbo, "INSERT INTO donationpayment (ID, PaymentName) VALUES (4, '" + _("Debit Card", l) + "')")
    # Add donationpaymentid field to donations
    db.execute_dbupdate(dbo, "ALTER TABLE ownerdonation ADD DonationPaymentID INTEGER")
    db.execute_dbupdate(dbo, "UPDATE ownerdonation SET DonationPaymentID = 1")

def update_33012(dbo):
    # Add ShelterLocationUnit
    db.execute_dbupdate(dbo, "ALTER TABLE animal ADD ShelterLocationUnit %s" % shorttext(dbo))
    db.execute_dbupdate(dbo, "UPDATE animal SET ShelterLocationUnit = ''")

def update_33013(dbo):
    # Add online form tables
    sql = "CREATE TABLE onlineform (ID INTEGER NOT NULL PRIMARY KEY, " \
        "Name %(short)s NOT NULL, " \
        "RedirectUrlAfterPOST %(short)s, " \
        "SetOwnerFlags %(short)s, " \
        "Description %(long)s )" % { "short": shorttext(dbo), "long": longtext(dbo) }
    db.execute_dbupdate(dbo, sql)
    sql = "CREATE INDEX onlineform_Name ON onlineform(Name)"
    db.execute_dbupdate(dbo, sql)
    sql = "CREATE TABLE onlineformfield(ID INTEGER NOT NULL PRIMARY KEY, " \
        "OnlineFormID INTEGER NOT NULL, " \
        "FieldName %(short)s NOT NULL, " \
        "FieldType INTEGER NOT NULL, " \
        "Label %(short)s NOT NULL, " \
        "Lookups %(long)s, " \
        "Tooltip %(long)s )" % { "short": shorttext(dbo), "long": longtext(dbo) }
    db.execute_dbupdate(dbo, sql)
    sql = "CREATE INDEX onlineformfield_OnlineFormID ON onlineformfield(OnlineFormID)"
    db.execute_dbupdate(dbo, sql)
    sql = "CREATE TABLE onlineformincoming(CollationID INTEGER NOT NULL, " \
        "FormName %(short)s NOT NULL, " \
        "PostedDate %(date)s NOT NULL, " \
        "Flags %(short)s, " \
        "FieldName %(short)s NOT NULL, " \
        "Value %(long)s )" % { "date": datetype(dbo), "short": shorttext(dbo), "long": longtext(dbo) }
    db.execute_dbupdate(dbo, sql)
    sql = "CREATE INDEX onlineformincoming_CollationID ON onlineformincoming(CollationID)"
    db.execute_dbupdate(dbo, sql)

def update_33014(dbo):
    # Add a display index field to onlineformfield
    db.execute_dbupdate(dbo, "ALTER TABLE onlineformfield ADD DisplayIndex INTEGER")
    # Add a label field to onlineformincoming
    db.execute_dbupdate(dbo, "ALTER TABLE onlineformincoming ADD Label %s" % shorttext(dbo))

def update_33015(dbo):
    # Add a host field to onlineformincoming
    db.execute_dbupdate(dbo, "ALTER TABLE onlineformincoming ADD Host %s" % shorttext(dbo))

def update_33016(dbo):
    # Add a DisplayIndex and Preview field to onlineformincoming
    db.execute_dbupdate(dbo, "ALTER TABLE onlineformincoming ADD DisplayIndex INTEGER")
    db.execute_dbupdate(dbo, "ALTER TABLE onlineformincoming ADD Preview %s" % longtext(dbo))

def update_33017(dbo):
    # Add the customreportrole table
    db.execute_dbupdate(dbo, "CREATE TABLE customreportrole (ReportID INTEGER NOT NULL, " \
        "RoleID INTEGER NOT NULL, CanView INTEGER NOT NULL)")
    db.execute_dbupdate(dbo, "CREATE UNIQUE INDEX customreportrole_ReportIDRoleID ON customreportrole(ReportID, RoleID)")

def update_33018(dbo):
    l = dbo.locale
    # Add IsPermanentFoster and HasPermanentFoster fields
    db.execute_dbupdate(dbo, "ALTER TABLE adoption ADD IsPermanentFoster INTEGER")
    db.execute_dbupdate(dbo, "ALTER TABLE animal ADD HasPermanentFoster INTEGER")
    # Add Permanent Foster movement type
    db.execute_dbupdate(dbo, "INSERT INTO lksmovementtype (ID, MovementType) VALUES (12, %s)" % db.ds(_("Permanent Foster", l)))

def update_33019(dbo):
    # Set initial value for those flags
    db.execute_dbupdate(dbo, "UPDATE adoption SET IsPermanentFoster = 0 WHERE IsPermanentFoster Is Null")
    db.execute_dbupdate(dbo, "UPDATE animal SET HasPermanentFoster = 0 WHERE HasPermanentFoster Is Null")

def update_33101(dbo):
    # Many indexes we should have
    def do_index(indexname, tablename, fieldname):
        try:
            db.execute_dbupdate(dbo, "CREATE INDEX %s ON %s (%s)" % (indexname, tablename, fieldname))
        except:
            pass
    do_index("owner_OwnerAddress", "owner", "OwnerAddress")
    do_index("owner_OwnerCounty", "owner", "OwnerCounty")
    do_index("owner_EmailAddress", "owner", "EmailAddress")
    do_index("owner_OwnerForeNames", "owner", "OwnerForeNames")
    do_index("owner_HomeTelephone", "owner", "HomeTelephone")
    do_index("owner_MobileTelephone", "owner", "MobileTelephone")
    do_index("owner_WorkTelephone", "owner", "WorkTelephone")
    do_index("owner_OwnerInitials", "owner", "OwnerInitials")
    do_index("owner_OwnerPostcode", "owner", "OwnerPostcode")
    do_index("owner_OwnerSurname", "owner", "OwnerSurname")
    do_index("owner_OwnerTitle", "owner", "OwnerTitle")
    do_index("owner_OwnerTown", "owner", "OwnerTown")
    do_index("animal_AcceptanceNumber", "animal", "AcceptanceNumber")
    do_index("animal_ActiveMovementType", "animal", "ActiveMovementType")
    do_index("animal_AnimalTypeID", "animal", "AnimalTypeID")
    do_index("animal_BaseColourID", "animal", "BaseColourID")
    do_index("animal_BondedAnimalID", "animal", "BondedAnimalID")
    do_index("animal_BondedAnimal2ID", "animal", "BondedAnimal2ID")
    do_index("animal_BreedID", "animal", "BreedID")
    do_index("animal_Breed2ID", "animal", "Breed2ID")
    do_index("animal_BroughtInByOwnerID", "animal", "BroughtInByOwnerID")
    do_index("animal_CoatType", "animal", "CoatType")
    do_index("animal_CurrentVetID", "animal", "CurrentVetID")
    do_index("animal_DeceasedDate", "animal", "DeceasedDate")
    do_index("animal_EntryReasonID", "animal", "EntryReasonID")
    do_index("animal_IdentichipNumber", "animal", "IdentichipNumber")
    do_index("animal_OriginalOwnerID", "animal", "OriginalOwnerID")
    do_index("animal_OwnersVetID", "animal", "OwnersVetID")
    do_index("animal_PutToSleep", "animal", "PutToSleep")
    do_index("animal_PTSReasonID", "animal", "PTSReasonID")
    do_index("animal_Sex", "animal", "Sex")
    do_index("animal_Size", "animal", "Size")
    do_index("animal_ShelterLocation", "animal", "ShelterLocation")
    do_index("animal_ShelterLocationUnit", "animal", "ShelterLocationUnit")
    do_index("animal_ShortCode", "animal", "ShortCode")
    do_index("animal_SpeciesID", "animal", "SpeciesID")
    do_index("adoption_CreatedBy", "adoption", "CreatedBy")
    do_index("adoption_IsPermanentFoster", "adoption", "IsPermanentFoster")
    do_index("adoption_IsTrial", "adoption", "IsTrial")
    do_index("adoption_ReturnedReasonID", "adoption", "ReturnedReasonID")

def update_33102(dbo):
    # More indexes we should have
    def do_index(indexname, tablename, fieldname):
        try:
            db.execute_dbupdate(dbo, "CREATE INDEX %s ON %s (%s)" % (indexname, tablename, fieldname))
        except:
            pass
    do_index("animal_AgeGroup", "animal", "AgeGroup")
    do_index("animal_BreedName", "animal", "BreedName")
    do_index("animal_RabiesTag", "animal", "RabiesTag")
    do_index("animal_TattooNumber", "animal", "TattooNumber")
    do_index("owner_MembershipNumber", "owner", "MembershipNumber")
    do_index("animallost_AreaLost", "animallost", "AreaLost")
    do_index("animallost_AreaPostcode", "animallost", "AreaPostcode")
    do_index("animalfound_AreaFound", "animalfound", "AreaFound")
    do_index("animalfound_AreaPostcode", "animalfound", "AreaPostcode")
    do_index("animalwaitinglist_AnimalDescription", "animalwaitinglist", "AnimalDescription")
    do_index("animalwaitinglist_OwnerID", "animalwaitinglist", "OwnerID")
    do_index("animalfound_AnimalTypeID", "animalfound", "AnimalTypeID")
    do_index("animallost_AnimalTypeID", "animallost", "AnimalTypeID")
    do_index("media_LinkTypeID", "media", "LinkTypeID")
    do_index("media_WebsitePhoto", "media", "WebsitePhoto")
    do_index("media_WebsiteVideo", "media", "WebsiteVideo")
    do_index("media_DocPhoto", "media", "DocPhoto")
    do_index("adoption_MovementType", "adoption", "MovementType")
    do_index("adoption_ReservationDate", "adoption", "ReservationDate")
    do_index("adoption_ReservationCancelledDate", "adoption", "ReservationCancelledDate")

def update_33103(dbo):
    # Mistakes in initial deploy
    def do_index(indexname, tablename, fieldname):
        try:
            db.execute_dbupdate(dbo, "CREATE INDEX %s ON %s (%s)" % (indexname, tablename, fieldname))
        except:
            pass
    do_index("owner_HomeTelephone", "owner", "HomeTelephone")
    do_index("owner_MobileTelephone", "owner", "MobileTelephone")
    do_index("owner_WorkTelephone", "owner", "WorkTelephone")
    do_index("owner_EmailAddress", "owner", "EmailAddress")
    do_index("animal_BroughtInByOwnerID", "animal", "BroughtInByOwnerID")

def update_33104(dbo):
    # Add LatLong
    db.execute_dbupdate(dbo, "ALTER TABLE owner ADD LatLong %s" % shorttext(dbo))

def update_33105(dbo):
    # Add LocationFilter
    db.execute_dbupdate(dbo, "ALTER TABLE users ADD LocationFilter %s" % shorttext(dbo))

def update_33106(dbo):
    # Add MatchColour
    db.execute_dbupdate(dbo, "ALTER TABLE owner ADD MatchColour INTEGER")
    db.execute_dbupdate(dbo, "UPDATE owner SET MatchColour = -1")


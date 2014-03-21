#!/usr/bin/python

import additional
import animal
import configuration
import dbfs
import financial
import html
import log
import medical
import person
import users
import utils
from i18n import _, format_currency_no_symbol, now, python2display, yes_no
from sitedefs import BASE_URL

def org_tags(dbo, username):
    """
    Generates a list of tags from the organisation and user info
    """
    u = users.get_users(dbo, username)
    realname = ""
    email = ""
    if len(u) > 0:
        u = u[0]
        realname = u["REALNAME"]
        email = u["EMAILADDRESS"]
    tags = {
        "ORGANISATION"          : configuration.organisation(dbo),
        "ORGANISATIONADDRESS"   : configuration.organisation_address(dbo),
        "ORGANISATIONTELEPHONE" : configuration.organisation_telephone(dbo),
        "DATE"                  : python2display(dbo.locale, now(dbo.timezone)),
        "USERNAME"              : username,
        "USERREALNAME"          : realname,
        "USEREMAILADDRESS"      : email
    }
    return tags

def additional_yesno(l, af):
    """
    Returns the yes/no value for an additional field. If it has a LOOKUPVALUES
    set, we use the value the user set.
    """
    if af["LOOKUPVALUES"] is not None and af["LOOKUPVALUES"] != "":
        values = af["LOOKUPVALUES"].split("|")
        for v in values:
            if af["VALUE"] is None:
                if v.strip().startswith("0"):
                    return v[v.find("=")+1:]
            else:
                if v.strip().startswith(af["VALUE"]):
                    return v[v.find("=")+1:]
    else:
        return yes_no(l, af["VALUE"])

def animal_tags(dbo, a):
    """
    Generates a list of tags from an animal result (the deep type from
    calling animal.get_animal)
    """
    l = dbo.locale
    displaydob = python2display(l, a["DATEOFBIRTH"])
    displayage = a["ANIMALAGE"]
    estimate = ""
    if a["ESTIMATEDDOB"] == 1: 
        displaydob = a["AGEGROUP"]
        displayage = a["AGEGROUP"]
        estimate = _("estimate", l)

    tags = { 
        "ANIMALNAME"            : a["ANIMALNAME"],
        "ANIMALTYPENAME"        : a["ANIMALTYPENAME"],
        "BASECOLOURNAME"        : a["BASECOLOURNAME"],
        "BASECOLORNAME"         : a["BASECOLOURNAME"],
        "BREEDNAME"             : a["BREEDNAME"],
        "INTERNALLOCATION"      : a["SHELTERLOCATIONNAME"],
        "LOCATIONUNIT"          : a["SHELTERLOCATIONUNIT"],
        "COATTYPE"              : a["COATTYPENAME"],
        "HEALTHPROBLEMS"        : a["HEALTHPROBLEMS"],
        "ANIMALCREATEDBY"       : a["CREATEDBY"],
        "ANIMALCREATEDDATE"     : python2display(l, a["CREATEDDATE"]),
        "DATEBROUGHTIN"         : python2display(l, a["DATEBROUGHTIN"]),
        "DATEOFBIRTH"           : python2display(l, a["DATEOFBIRTH"]),
        "AGEGROUP"              : a["AGEGROUP"],
        "DISPLAYDOB"            : displaydob,
        "DISPLAYAGE"            : displayage,
        "ESTIMATEDDOB"          : estimate,
        "ANIMALID"              : str(a["ID"]),
        "IDENTICHIPNUMBER"      : a["IDENTICHIPNUMBER"],
        "IDENTICHIPPED"         : a["IDENTICHIPPEDNAME"],
        "IDENTICHIPPEDDATE"     : python2display(l, a["IDENTICHIPDATE"]),
        "MICROCHIPNUMBER"       : a["IDENTICHIPNUMBER"],
        "MICROCHIPPED"          : a["IDENTICHIPPEDNAME"],
        "MICROCHIPDATE"         : python2display(l, a["IDENTICHIPDATE"]),
        "TATTOO"                : a["TATTOONAME"],
        "TATTOODATE"            : python2display(l, a["TATTOODATE"]),
        "TATTOONUMBER"          : a["TATTOONUMBER"],
        "COMBITESTED"           : a["COMBITESTEDNAME"],
        "FIVLTESTED"            : a["COMBITESTEDNAME"],
        "COMBITESTDATE"         : python2display(l, a["COMBITESTDATE"]),
        "FIVLTESTDATE"          : python2display(l, a["COMBITESTDATE"]),
        "COMBITESTRESULT"       : a["COMBITESTRESULTNAME"],
        "FIVTESTRESULT"         : a["COMBITESTRESULTNAME"],
        "FIVRESULT"             : a["COMBITESTRESULTNAME"],
        "FLVTESTRESULT"         : a["FLVRESULTNAME"],
        "FLVRESULT"             : a["FLVRESULTNAME"],
        "HEARTWORMTESTED"       : a["HEARTWORMTESTEDNAME"],
        "HEARTWORMTESTDATE"     : python2display(l, a["HEARTWORMTESTDATE"]),
        "HEARTWORMTESTRESULT"   : a["HEARTWORMTESTRESULTNAME"],
        "HIDDENANIMALDETAILS"   : a["HIDDENANIMALDETAILS"],
        "ANIMALLASTCHANGEDBY"   : a["LASTCHANGEDBY"],
        "ANIMALLASTCHANGEDDATE" : python2display(l, a["LASTCHANGEDDATE"]),
        "MARKINGS"              : a["MARKINGS"],
        "DECLAWED"              : a["DECLAWEDNAME"],
        "RABIESTAG"             : a["RABIESTAG"],
        "GOODWITHCATS"          : a["ISGOODWITHCATSNAME"],
        "GOODWITHDOGS"          : a["ISGOODWITHDOGSNAME"],
        "GOODWITHCHILDREN"      : a["ISGOODWITHCHILDRENNAME"],
        "HOUSETRAINED"          : a["ISHOUSETRAINEDNAME"],
        "NAMEOFPERSONBROUGHTANIMALIN" : a["BROUGHTINBYOWNERNAME"],
        "ADDRESSOFPERSONBROUGHTANIMALIN" : a["BROUGHTINBYOWNERADDRESS"],
        "TOWNOFPERSONBROUGHTANIMALIN" : a["BROUGHTINBYOWNERTOWN"],
        "COUNTYOFPERSONBROUGHTANIMALIN": a["BROUGHTINBYOWNERCOUNTY"],
        "POSTCODEOFPERSONBROUGHTIN": a["BROUGHTINBYOWNERPOSTCODE"],
        "CITYOFPERSONBROUGHTANIMALIN" : a["BROUGHTINBYOWNERTOWN"],
        "STATEOFPERSONBROUGHTANIMALIN": a["BROUGHTINBYOWNERCOUNTY"],
        "ZIPCODEOFPERSONBROUGHTIN": a["BROUGHTINBYOWNERPOSTCODE"],
        "BROUGHTINBYNAME"     : a["BROUGHTINBYOWNERNAME"],
        "BROUGHTINBYADDRESS"  : a["BROUGHTINBYOWNERADDRESS"],
        "BROUGHTINBYTOWN"     : a["BROUGHTINBYOWNERTOWN"],
        "BROUGHTINBYCOUNTY"   : a["BROUGHTINBYOWNERCOUNTY"],
        "BROUGHTINBYPOSTCODE" : a["BROUGHTINBYOWNERPOSTCODE"],
        "BROUGHTINBYCITY"     : a["BROUGHTINBYOWNERTOWN"],
        "BROUGHTINBYSTATE"    : a["BROUGHTINBYOWNERCOUNTY"],
        "BROUGHTINBYZIPCODE"  : a["BROUGHTINBYOWNERPOSTCODE"],
        "BROUGHTINBYHOMEPHONE" : a["BROUGHTINBYHOMETELEPHONE"],
        "BROUGHTINBYPHONE"    : a["BROUGHTINBYHOMETELEPHONE"],
        "BROUGHTINBYWORKPHONE" : a["BROUGHTINBYWORKTELEPHONE"],
        "BROUGHTINBYMOBILEPHONE" : a["BROUGHTINBYMOBILETELEPHONE"],
        "BROUGHTINBYCELLPHONE" : a["BROUGHTINBYMOBILETELEPHONE"],
        "BROUGHTINBYEMAIL"    : a["BROUGHTINBYEMAILADDRESS"],
        "NAMEOFOWNERSVET"       : a["OWNERSVETNAME"],
        "NAMEOFCURRENTVET"      : a["CURRENTVETNAME"],
        "HASSPECIALNEEDS"       : a["HASSPECIALNEEDSNAME"],
        "NEUTERED"              : a["NEUTEREDNAME"],
        "FIXED"                 : a["NEUTEREDNAME"],
        "ALTERED"               : a["NEUTEREDNAME"],
        "NEUTEREDDATE"          : python2display(l, a["NEUTEREDDATE"]),
        "FIXEDDATE"             : python2display(l, a["NEUTEREDDATE"]),
        "ALTEREDDATE"           : python2display(l, a["NEUTEREDDATE"]),
        "ORIGINALOWNERNAME"     : a["ORIGINALOWNERNAME"],
        "ORIGINALOWNERADDRESS"  : a["ORIGINALOWNERADDRESS"],
        "ORIGINALOWNERTOWN"     : a["ORIGINALOWNERTOWN"],
        "ORIGINALOWNERCOUNTY"   : a["ORIGINALOWNERCOUNTY"],
        "ORIGINALOWNERPOSTCODE" : a["ORIGINALOWNERPOSTCODE"],
        "ORIGINALOWNERCITY"     : a["ORIGINALOWNERTOWN"],
        "ORIGINALOWNERSTATE"    : a["ORIGINALOWNERCOUNTY"],
        "ORIGINALOWNERZIPCODE"  : a["ORIGINALOWNERPOSTCODE"],
        "ORIGINALOWNERHOMEPHONE" : a["ORIGINALOWNERHOMETELEPHONE"],
        "ORIGINALOWNERPHONE"    : a["ORIGINALOWNERHOMETELEPHONE"],
        "ORIGINALOWNERWORKPHONE" : a["ORIGINALOWNERWORKTELEPHONE"],
        "ORIGINALOWNERMOBILEPHONE" : a["ORIGINALOWNERMOBILETELEPHONE"],
        "ORIGINALOWNERCELLPHONE" : a["ORIGINALOWNERMOBILETELEPHONE"],
        "ORIGINALOWNEREMAIL"    : a["ORIGINALOWNEREMAILADDRESS"],
        "CURRENTOWNERNAME"     : a["CURRENTOWNERNAME"],
        "CURRENTOWNERADDRESS"  : a["CURRENTOWNERADDRESS"],
        "CURRENTOWNERTOWN"     : a["CURRENTOWNERTOWN"],
        "CURRENTOWNERCOUNTY"   : a["CURRENTOWNERCOUNTY"],
        "CURRENTOWNERPOSTCODE" : a["CURRENTOWNERPOSTCODE"],
        "CURRENTOWNERCITY"     : a["CURRENTOWNERTOWN"],
        "CURRENTOWNERSTATE"    : a["CURRENTOWNERCOUNTY"],
        "CURRENTOWNERZIPCODE"  : a["CURRENTOWNERPOSTCODE"],
        "CURRENTOWNERHOMEPHONE" : a["CURRENTOWNERHOMETELEPHONE"],
        "CURRENTOWNERPHONE"    : a["CURRENTOWNERHOMETELEPHONE"],
        "CURRENTOWNERWORKPHONE" : a["CURRENTOWNERWORKTELEPHONE"],
        "CURRENTOWNERMOBILEPHONE" : a["CURRENTOWNERMOBILETELEPHONE"],
        "CURRENTOWNERCELLPHONE" : a["CURRENTOWNERMOBILETELEPHONE"],
        "CURRENTOWNEREMAIL"     : a["CURRENTOWNEREMAILADDRESS"],
        "CURRENTVETNAME"        : a["CURRENTVETNAME"],
        "CURRENTVETADDRESS"     : a["CURRENTVETADDRESS"],
        "CURRENTVETTOWN"        : a["CURRENTVETTOWN"],
        "CURRENTVETCOUNTY"      : a["CURRENTVETCOUNTY"],
        "CURRENTVETPOSTCODE"    : a["CURRENTVETPOSTCODE"],
        "CURRENTVETCITY"        : a["CURRENTVETTOWN"],
        "CURRENTVETSTATE"       : a["CURRENTVETCOUNTY"],
        "CURRENTVETZIPCODE"     : a["CURRENTVETPOSTCODE"],
        "CURRENTVETPHONE"       : a["CURRENTVETWORKTELEPHONE"],
        "OWNERSVETNAME"         : a["OWNERSVETNAME"],
        "OWNERSVETADDRESS"      : a["OWNERSVETADDRESS"],
        "OWNERSVETTOWN"         : a["OWNERSVETTOWN"],
        "OWNERSVETCOUNTY"       : a["OWNERSVETCOUNTY"],
        "OWNERSVETPOSTCODE"     : a["OWNERSVETPOSTCODE"],
        "OWNERSVETCITY"         : a["OWNERSVETTOWN"],
        "OWNERSVETSTATE"        : a["OWNERSVETCOUNTY"],
        "OWNERSVETZIPCODE"      : a["OWNERSVETPOSTCODE"],
        "OWNERSVETPHONE"        : a["OWNERSVETWORKTELEPHONE"],
        "RESERVEDOWNERNAME"     : a["RESERVEDOWNERNAME"],
        "RESERVEDOWNERADDRESS"  : a["RESERVEDOWNERADDRESS"],
        "RESERVEDOWNERTOWN"     : a["RESERVEDOWNERTOWN"],
        "RESERVEDOWNERCOUNTY"   : a["RESERVEDOWNERCOUNTY"],
        "RESERVEDOWNERPOSTCODE" : a["RESERVEDOWNERPOSTCODE"],
        "RESERVEDOWNERCITY"     : a["RESERVEDOWNERTOWN"],
        "RESERVEDOWNERSTATE"    : a["RESERVEDOWNERCOUNTY"],
        "RESERVEDOWNERZIPCODE"  : a["RESERVEDOWNERPOSTCODE"],
        "RESERVEDOWNERHOMEPHONE" : a["RESERVEDOWNERHOMETELEPHONE"],
        "RESERVEDOWNERPHONE"    : a["RESERVEDOWNERHOMETELEPHONE"],
        "RESERVEDOWNERWORKPHONE" : a["RESERVEDOWNERWORKTELEPHONE"],
        "RESERVEDOWNERMOBILEPHONE" : a["RESERVEDOWNERMOBILETELEPHONE"],
        "RESERVEDOWNERCELLPHONE" : a["RESERVEDOWNERMOBILETELEPHONE"],
        "RESERVEDOWNEREMAIL"    : a["RESERVEDOWNEREMAILADDRESS"],
        "ENTRYCATEGORY"         : a["ENTRYREASONNAME"],
        "REASONFORENTRY"        : a["REASONFORENTRY"],
        "REASONNOTBROUGHTBYOWNER" : a["REASONNO"],
        "SEX"                   : a["SEXNAME"],
        "SIZE"                  : a["SIZENAME"],
        "SPECIESNAME"           : a["SPECIESNAME"],
        "ANIMALCOMMENTS"        : a["ANIMALCOMMENTS"],
        "SHELTERCODE"           : a["SHELTERCODE"],
        "AGE"                   : a["ANIMALAGE"],
        "ACCEPTANCENUMBER"      : a["ACCEPTANCENUMBER"],
        "LITTERID"              : a["ACCEPTANCENUMBER"],
        "DECEASEDDATE"          : python2display(l, a["DECEASEDDATE"]),
        "DECEASEDNOTES"         : a["PTSREASON"],
        "DECEASEDCATEGORY"      : a["PTSREASONNAME"],
        "SHORTSHELTERCODE"      : a["SHORTCODE"],
        "MOSTRECENTENTRY"       : python2display(l, a["MOSTRECENTENTRYDATE"]),
        "TIMEONSHELTER"         : a["TIMEONSHELTER"],
        "WEBMEDIAFILENAME"      : a["WEBSITEMEDIANAME"],
        "WEBSITEMEDIANAME"      : a["WEBSITEMEDIANAME"],
        "WEBSITEVIDEOURL"       : a["WEBSITEVIDEOURL"],
        "WEBSITEVIDEONOTES"     : a["WEBSITEVIDEONOTES"],
        "WEBMEDIANOTES"         : a["WEBSITEMEDIANOTES"],
        "WEBSITEMEDIANOTES"     : a["WEBSITEMEDIANOTES"],
        "DOCUMENTIMGLINK"       : "<img height=\"200\" src=\"" + html.img_src(a, "animal") + "\" >",
        "DOCUMENTIMGTHUMBLINK"  : "<img src=\"" + html.thumbnail_img_src(a, "animalthumb") + "\" />",
        "DOCUMENTQRLINK"        : "<img src=\"http://chart.apis.google.com/chart?cht=qr&chl=%s&chs=150x150\" />" % (BASE_URL + "/animal?id=%s" % a["ID"]),
        "ANIMALONSHELTER"       : yes_no(l, a["ARCHIVED"] == 0),
        "ANIMALISRESERVED"      : yes_no(l, a["HASACTIVERESERVE"] == 1),
        "ADOPTIONID"            : a["ACTIVEMOVEMENTADOPTIONNUMBER"],
        "ADOPTIONNUMBER"        : a["ACTIVEMOVEMENTADOPTIONNUMBER"],
        "INSURANCENUMBER"       : a["ACTIVEMOVEMENTINSURANCENUMBER"],
        "RESERVATIONDATE"       : python2display(l, a["ACTIVEMOVEMENTRESERVATIONDATE"]),
        "RETURNDATE"            : python2display(l, a["ACTIVEMOVEMENTRETURNDATE"]),
        "ADOPTIONDATE"          : python2display(l, a["ACTIVEMOVEMENTDATE"]),
        "FOSTEREDDATE"          : python2display(l, a["ACTIVEMOVEMENTDATE"]),
        "TRANSFERDATE"          : python2display(l, a["ACTIVEMOVEMENTDATE"]),
        "MOVEMENTDATE"          : python2display(l, a["ACTIVEMOVEMENTDATE"]),
        "MOVEMENTTYPE"          : a["ACTIVEMOVEMENTTYPENAME"],
        "ADOPTIONDONATION"      : format_currency_no_symbol(l, a["ACTIVEMOVEMENTDONATION"]),
        "ADOPTIONCREATEDBY"     : a["ACTIVEMOVEMENTCREATEDBY"],
        "ADOPTIONCREATEDBYNAME" : a["ACTIVEMOVEMENTCREATEDBYNAME"],
        "ADOPTIONCREATEDDATE"   : python2display(l, a["ACTIVEMOVEMENTCREATEDDATE"]),
        "ADOPTIONLASTCHANGEDBY" : a["ACTIVEMOVEMENTLASTCHANGEDBY"],
        "ADOPTIONLASTCHANGEDDATE" : python2display(l, a["ACTIVEMOVEMENTLASTCHANGEDDATE"])
    }

    # Set original owner to be current owner on non-shelter animals
    if a["NONSHELTERANIMAL"] == 1 and a["ORIGINALOWNERNAME"] is not None and a["ORIGINALOWNERNAME"] != "":
        tags["CURRENTOWNERNAME"] = a["ORIGINALOWNERNAME"]
        tags["CURRENTOWNERADDRESS"] = a["ORIGINALOWNERADDRESS"]
        tags["CURRENTOWNERTOWN"] = a["ORIGINALOWNERTOWN"]
        tags["CURRENTOWNERCOUNTY"] = a["ORIGINALOWNERCOUNTY"]
        tags["CURRENTOWNERPOSTCODE"] = a["ORIGINALOWNERPOSTCODE"]
        tags["CURRENTOWNERCITY"] = a["ORIGINALOWNERTOWN"]
        tags["CURRENTOWNERSTATE"] = a["ORIGINALOWNERCOUNTY"]
        tags["CURRENTOWNERZIPCODE"] = a["ORIGINALOWNERPOSTCODE"]
        tags["CURRENTOWNERHOMEPHONE"] = a["ORIGINALOWNERHOMETELEPHONE"]
        tags["CURRENTOWNERPHONE"] = a["ORIGINALOWNERHOMETELEPHONE"]
        tags["CURRENTOWNERWORKPHONE"] = a["ORIGINALOWNERWORKTELEPHONE"]
        tags["CURRENTOWNERMOBILEPHONE"] = a["ORIGINALOWNERMOBILETELEPHONE"]
        tags["CURRENTOWNERCELLPHONE"] = a["ORIGINALOWNERMOBILETELEPHONE"]
        tags["CURRENTOWNEREMAIL"] = a["ORIGINALOWNEREMAILADDRESS"]

    # If the animal doesn't have a current owner, but does have an open
    # movement with a future date on it, look up the owner and use that 
    # instead so that we can still generate paperwork for future adoptions.
    if a["CURRENTOWNERID"] is None or a["CURRENTOWNERID"] == 0:
        latest = animal.get_latest_movement(dbo, a["ID"])
        if latest is not None:
            p = person.get_person(dbo, latest["OWNERID"])
            if p is not None:
                tags["CURRENTOWNERNAME"] = p["OWNERNAME"]
                tags["CURRENTOWNERADDRESS"] = p["OWNERADDRESS"]
                tags["CURRENTOWNERTOWN"] = p["OWNERTOWN"]
                tags["CURRENTOWNERCOUNTY"] = p["OWNERCOUNTY"]
                tags["CURRENTOWNERPOSTCODE"] = p["OWNERPOSTCODE"]
                tags["CURRENTOWNERCITY"] = p["OWNERTOWN"]
                tags["CURRENTOWNERSTATE"] = p["OWNERCOUNTY"]
                tags["CURRENTOWNERZIPCODE"] = p["OWNERPOSTCODE"]
                tags["CURRENTOWNERHOMEPHONE"] = p["HOMETELEPHONE"]
                tags["CURRENTOWNERPHONE"] = p["HOMETELEPHONE"]
                tags["CURRENTOWNERWORKPHONE"] = p["WORKTELEPHONE"]
                tags["CURRENTOWNERMOBILEPHONE"] = p["MOBILETELEPHONE"]
                tags["CURRENTOWNERCELLPHONE"] = p["MOBILETELEPHONE"]
                tags["CURRENTOWNEREMAIL"] = p["EMAILADDRESS"]

    # Additional fields
    add = additional.get_additional_fields(dbo, int(a["ID"]), "animal")
    for af in add:
        val = af["VALUE"]
        if af["FIELDTYPE"] == additional.YESNO:
            val = additional_yesno(l, af)
        if af["FIELDTYPE"] == additional.MONEY:
            val = format_currency_no_symbol(l, af["VALUE"])
        tags[af["FIELDNAME"].upper()] = val

    include_incomplete = configuration.include_incomplete_medical_doc(dbo)
    
    # Vaccinations
    vaccasc = medical.get_vaccinations(dbo, int(a["ID"]), not include_incomplete)
    vaccdesc = medical.get_vaccinations(dbo, int(a["ID"]), not include_incomplete, medical.DESCENDING_REQUIRED)
    for idx in range(1, 101):
        tags["VACCINATIONNAME" + str(idx)] = ""
        tags["VACCINATIONREQUIRED" + str(idx)] = ""
        tags["VACCINATIONGIVEN" + str(idx)] = ""
        tags["VACCINATIONCOMMENTS" + str(idx)] = ""
        tags["VACCINATIONDESCRIPTION" + str(idx)] = ""
        tags["VACCINATIONNAMELAST" + str(idx)] = ""
        tags["VACCINATIONREQUIREDLAST" + str(idx)] = ""
        tags["VACCINATIONGIVENLAST" + str(idx)] = ""
        tags["VACCINATIONCOMMENTSLAST" + str(idx)] = ""
        tags["VACCINATIONDESCRIPTIONLAST" + str(idx)] = ""
    idx = 1
    for v in vaccasc:
        tags["VACCINATIONNAME" + str(idx)] = v["VACCINATIONTYPE"]
        tags["VACCINATIONREQUIRED" + str(idx)] = python2display(l, v["DATEREQUIRED"])
        tags["VACCINATIONGIVEN" + str(idx)] = python2display(l, v["DATEOFVACCINATION"])
        tags["VACCINATIONCOMMENTS" + str(idx)] = v["COMMENTS"]
        tags["VACCINATIONDESCRIPTION" + str(idx)] = v["VACCINATIONDESCRIPTION"]
        idx += 1
    idx = 1
    uniquetypes = {}
    recentgiven = {}
    for v in vaccdesc:
        tags["VACCINATIONNAMELAST" + str(idx)] = v["VACCINATIONTYPE"]
        tags["VACCINATIONREQUIREDLAST" + str(idx)] = python2display(l, v["DATEREQUIRED"])
        tags["VACCINATIONGIVENLAST" + str(idx)] = python2display(l, v["DATEOFVACCINATION"])
        tags["VACCINATIONCOMMENTSLAST" + str(idx)] = v["COMMENTS"]
        tags["VACCINATIONDESCRIPTIONLAST" + str(idx)] = v["VACCINATIONDESCRIPTION"]
        idx += 1
        # If this is the first of this type of vacc we've seen, make
        # some keys based on its name.
        if not uniquetypes.has_key(v["VACCINATIONTYPE"]):
            vname = v["VACCINATIONTYPE"].upper().replace(" ", "").replace("/", "")
            uniquetypes[v["VACCINATIONTYPE"]] = v
            tags["VACCINATIONNAME" + vname] = v["VACCINATIONTYPE"]
            tags["VACCINATIONREQUIRED" + vname] = python2display(l, v["DATEREQUIRED"])
            tags["VACCINATIONGIVEN" + vname] = python2display(l, v["DATEOFVACCINATION"])
            tags["VACCINATIONCOMMENTS" + vname] = v["COMMENTS"]
            tags["VACCINATIONDESCRIPTION" + vname] = v["VACCINATIONDESCRIPTION"]
        # If this is the first of this type of vacc we've seen that's been given
        # make some keys based on its name
        if not recentgiven.has_key(v["VACCINATIONTYPE"]) and v["DATEOFVACCINATION"] is not None:
            vname = v["VACCINATIONTYPE"].upper().replace(" ", "").replace("/", "")
            recentgiven[v["VACCINATIONTYPE"]] = v
            tags["VACCINATIONNAMERECENT" + vname] = v["VACCINATIONTYPE"]
            tags["VACCINATIONREQUIREDRECENT" + vname] = python2display(l, v["DATEREQUIRED"])
            tags["VACCINATIONGIVENRECENT" + vname] = python2display(l, v["DATEOFVACCINATION"])
            tags["VACCINATIONCOMMENTSRECENT" + vname] = v["COMMENTS"]
            tags["VACCINATIONDESCRIPTIONRECENT" + vname] = v["VACCINATIONDESCRIPTION"]

    # Tests
    testasc = medical.get_tests(dbo, int(a["ID"]), not include_incomplete)
    testdesc = medical.get_tests(dbo, int(a["ID"]), not include_incomplete, medical.DESCENDING_REQUIRED)
    for idx in range(1, 101):
        tags["TESTNAME" + str(idx)] = ""
        tags["TESTRESULT" + str(idx)] = ""
        tags["TESTREQUIRED" + str(idx)] = ""
        tags["TESTGIVEN" + str(idx)] = ""
        tags["TESTCOMMENTS" + str(idx)] = ""
        tags["TESTDESCRIPTION" + str(idx)] = ""
        tags["TESTNAMELAST" + str(idx)] = ""
        tags["TESTREQUIREDLAST" + str(idx)] = ""
        tags["TESTGIVENLAST" + str(idx)] = ""
        tags["TESTCOMMENTSLAST" + str(idx)] = ""
        tags["TESTDESCRIPTIONLAST" + str(idx)] = ""
    idx = 1
    for t in testasc:
        tags["TESTNAME" + str(idx)] = t["TESTNAME"]
        tags["TESTRESULT" + str(idx)] = t["RESULTNAME"]
        tags["TESTREQUIRED" + str(idx)] = python2display(l, t["DATEREQUIRED"])
        tags["TESTGIVEN" + str(idx)] = python2display(l, t["DATEOFTEST"])
        tags["TESTCOMMENTS" + str(idx)] = t["COMMENTS"]
        tags["TESTDESCRIPTION" + str(idx)] = t["TESTDESCRIPTION"]
        idx += 1
    idx = 1
    uniquetypes = {}
    recentgiven = {}
    for t in testdesc:
        tags["TESTNAMELAST" + str(idx)] = t["TESTNAME"]
        tags["TESTRESULTLAST" + str(idx)] = t["RESULTNAME"]
        tags["TESTREQUIREDLAST" + str(idx)] = python2display(l, t["DATEREQUIRED"])
        tags["TESTGIVENLAST" + str(idx)] = python2display(l, t["DATEOFTEST"])
        tags["TESTCOMMENTSLAST" + str(idx)] = t["COMMENTS"]
        tags["TESTDESCRIPTIONLAST" + str(idx)] = t["TESTDESCRIPTION"]
        idx += 1
        # If this is the first of this type of test we've seen, make
        # some keys based on its name.
        if not uniquetypes.has_key(t["TESTNAME"]):
            tname = t["TESTNAME"].upper().replace(" ", "").replace("/", "")
            uniquetypes[t["TESTNAME"]] = t
            tags["TESTNAME" + tname] = t["TESTNAME"]
            tags["TESTRESULT" + tname] = t["RESULTNAME"]
            tags["TESTREQUIRED" + tname] = python2display(l, t["DATEREQUIRED"])
            tags["TESTGIVEN" + tname] = python2display(l, t["DATEOFTEST"])
            tags["TESTCOMMENTS" + tname] = t["COMMENTS"]
            tags["TESTDESCRIPTION" + tname] = t["TESTDESCRIPTION"]
        # If this is the first of this type of test we've seen that's been given
        # make some keys based on its name
        if not recentgiven.has_key(t["TESTNAME"]) and t["DATEOFTEST"] is not None:
            tname = t["TESTNAME"].upper().replace(" ", "").replace("/", "")
            recentgiven[t["TESTNAME"]] = t
            tags["TESTNAMERECENT" + tname] = t["TESTNAME"]
            tags["TESTRESULTRECENT" + tname] = t["RESULTNAME"]
            tags["TESTREQUIREDRECENT" + tname] = python2display(l, t["DATEREQUIRED"])
            tags["TESTGIVENRECENT" + tname] = python2display(l, t["DATEOFTEST"])
            tags["TESTCOMMENTSRECENT" + tname] = t["COMMENTS"]
            tags["TESTDESCRIPTIONRECENT" + tname] = t["TESTDESCRIPTION"]

    # Medical
    medasc = medical.get_regimens(dbo, int(a["ID"]), not include_incomplete)
    meddesc = medical.get_regimens(dbo, int(a["ID"]), not include_incomplete, medical.DESCENDING_REQUIRED)
    for idx in range(1, 101):
        tags["MEDICALNAME" + str(idx)] = ""
        tags["MEDICALCOMMENTS" + str(idx)] = ""
        tags["MEDICALFREQUENCY" + str(idx)] = ""
        tags["MEDICALNUMBEROFTREATMENTS" + str(idx)] = ""
        tags["MEDICALSTATUS" + str(idx)] = ""
        tags["MEDICALDOSAGE" + str(idx)] = ""
        tags["MEDICALSTARTDATE" + str(idx)] = ""
        tags["MEDICALTREATMENTSGIVEN" + str(idx)] = ""
        tags["MEDICALTREATMENTSREMAINING" + str(idx)] = ""
        tags["MEDICALNAMELAST" + str(idx)] = ""
        tags["MEDICALCOMMENTSLAST" + str(idx)] = ""
        tags["MEDICALFREQUENCYLAST" + str(idx)] = ""
        tags["MEDICALNUMBEROFTREATMENTSLAST" + str(idx)] = ""
        tags["MEDICALSTATUSLAST" + str(idx)] = ""
        tags["MEDICALDOSAGELAST" + str(idx)] = ""
        tags["MEDICALSTARTDATELAST" + str(idx)] = ""
        tags["MEDICALTREATMENTSGIVENLAST" + str(idx)] = ""
        tags["MEDICALTREATMENTSREMAININGLAST" + str(idx)] = ""
    idx = 1
    for m in medasc:
        tags["MEDICALNAME" + str(idx)] = m["TREATMENTNAME"]
        tags["MEDICALCOMMENTS" + str(idx)] = m["COMMENTS"]
        tags["MEDICALFREQUENCY" + str(idx)] = m["NAMEDFREQUENCY"]
        tags["MEDICALNUMBEROFTREATMENTS" + str(idx)] = m["NAMEDNUMBEROFTREATMENTS"]
        tags["MEDICALSTATUS" + str(idx)] = m["NAMEDSTATUS"]
        tags["MEDICALDOSAGE" + str(idx)] = m["DOSAGE"]
        tags["MEDICALSTARTDATE" + str(idx)] = python2display(l, m["STARTDATE"])
        tags["MEDICALTREATMENTSGIVEN" + str(idx)] = str(m["TREATMENTSGIVEN"])
        tags["MEDICALTREATMENTSREMAINING" + str(idx)] = str(m["TREATMENTSREMAINING"])
        idx += 1
    idx = 1
    uniquetypes = {}
    recentgiven = {}
    for m in meddesc:
        tags["MEDICALNAMELAST" + str(idx)] = m["TREATMENTNAME"]
        tags["MEDICALCOMMENTSLAST" + str(idx)] = m["COMMENTS"]
        tags["MEDICALFREQUENCYLAST" + str(idx)] = m["NAMEDFREQUENCY"]
        tags["MEDICALNUMBEROFTREATMENTSLAST" + str(idx)] = m["NAMEDNUMBEROFTREATMENTS"]
        tags["MEDICALSTATUSLAST" + str(idx)] = m["NAMEDSTATUS"]
        tags["MEDICALDOSAGELAST" + str(idx)] = m["DOSAGE"]
        tags["MEDICALSTARTDATELAST" + str(idx)] = python2display(l, m["STARTDATE"])
        tags["MEDICALTREATMENTSGIVENLAST" + str(idx)] = str(m["TREATMENTSGIVEN"])
        tags["MEDICALTREATMENTSREMAININGLAST" + str(idx)] = str(m["TREATMENTSREMAINING"])
        idx += 1
        # If this is the first of this type of med we've seen, make
        # some keys based on its name.
        if not uniquetypes.has_key(m["TREATMENTNAME"]):
            tname = m["TREATMENTNAME"].upper().replace(" ", "").replace("/", "")
            uniquetypes[m["TREATMENTNAME"]] = m
            tags["MEDICALNAME" + tname] = m["TREATMENTNAME"]
            tags["MEDICALCOMMENTS" + tname] = m["COMMENTS"]
            tags["MEDICALFREQUENCY" + tname] = m["NAMEDFREQUENCY"]
            tags["MEDICALNUMBEROFTREATMENTS" + tname] = m["NAMEDNUMBEROFTREATMENTS"]
            tags["MEDICALSTATUS" + tname] = m["NAMEDSTATUS"]
            tags["MEDICALDOSAGE" + tname] = m["DOSAGE"]
            tags["MEDICALSTARTDATE" + tname] = python2display(l, m["STARTDATE"])
            tags["MEDICALTREATMENTSGIVEN" + tname] = str(m["TREATMENTSGIVEN"])
            tags["MEDICALTREATMENTSREMAINING" + tname] = str(m["TREATMENTSREMAINING"])
        # If this is the first of this type of med we've seen that's complete
        if not recentgiven.has_key(m["TREATMENTNAME"]) and m["STATUS"] == 2:
            tname = m["TREATMENTNAME"].upper().replace(" ", "").replace("/", "")
            recentgiven[m["TREATMENTNAME"]] = m
            tags["MEDICALNAMERECENT" + tname] = m["TREATMENTNAME"]
            tags["MEDICALCOMMENTSRECENT" + tname] = m["COMMENTS"]
            tags["MEDICALFREQUENCYRECENT" + tname] = m["NAMEDFREQUENCY"]
            tags["MEDICALNUMBEROFTREATMENTSRECENT" + tname] = m["NAMEDNUMBEROFTREATMENTS"]
            tags["MEDICALSTATUSRECENT" + tname] = m["NAMEDSTATUS"]
            tags["MEDICALDOSAGERECENT" + tname] = m["DOSAGE"]
            tags["MEDICALSTARTDATERECENT" + tname] = python2display(l, m["STARTDATE"])
            tags["MEDICALTREATMENTSGIVENRECENT" + tname] = str(m["TREATMENTSGIVEN"])
            tags["MEDICALTREATMENTSREMAININGRECENT" + tname] = str(m["TREATMENTSREMAINING"])

    # Diet
    dietasc = animal.get_diets(dbo, int(a["ID"]))
    dietdesc = animal.get_diets(dbo, int(a["ID"]), animal.DESCENDING)
    for idx in range(1, 101):
        tags["DIETNAME" + str(idx)] = ""
        tags["DIETDESCRIPTION" + str(idx)] = ""
        tags["DIETDATESTARTED" + str(idx)] = ""
        tags["DIETCOMMENTS" + str(idx)] = ""
        tags["DIETNAMELAST" + str(idx)] = ""
        tags["DIETDESCRIPTIONLAST" + str(idx)] = ""
        tags["DIETDATESTARTEDLAST" + str(idx)] = ""
        tags["DIETCOMMENTSLAST" + str(idx)] = ""
    idx = 1
    for d in dietasc:
        tags["DIETNAME" + str(idx)] = d["DIETNAME"]
        tags["DIETDESCRIPTION" + str(idx)] = d["DIETDESCRIPTION"]
        tags["DIETDATESTARTED" + str(idx)] = python2display(l, d["DATESTARTED"])
        tags["DIETCOMMENTS" + str(idx)] = d["COMMENTS"]
        idx += 1
    idx = 1
    for d in dietdesc:
        tags["DIETNAMELAST" + str(idx)] = d["DIETNAME"]
        tags["DIETDESCRIPTIONLAST" + str(idx)] = d["DIETDESCRIPTION"]
        tags["DIETDATESTARTEDLAST" + str(idx)] = python2display(l, d["DATESTARTED"])
        tags["DIETCOMMENTSLAST" + str(idx)] = d["COMMENTS"]
        idx += 1

    # Donations
    donasc = financial.get_animal_donations(dbo, int(a["ID"]))
    dondesc = financial.get_animal_donations(dbo, int(a["ID"]), financial.DESCENDING)
    for idx in range(1, 101):
        tags["RECEIPTNUM" + str(idx)] = ""
        tags["DONATIONTYPE" + str(idx)] = ""
        tags["DONATIONDATE" + str(idx)] = ""
        tags["DONATIONDATEDUE" + str(idx)] = ""
        tags["DONATIONAMOUNT" + str(idx)] = ""
        tags["DONATIONCOMMENTS" + str(idx)] = ""
        tags["DONATIONGIFTAID" + str(idx)] = ""
        tags["RECEIPTNUMLAST" + str(idx)] = ""
        tags["DONATIONTYPELAST" + str(idx)] = ""
        tags["DONATIONDATELAST" + str(idx)] = ""
        tags["DONATIONDATEDUELAST" + str(idx)] = ""
        tags["DONATIONAMOUNTLAST" + str(idx)] = ""
        tags["DONATIONCOMMENTSLAST" + str(idx)] = ""
        tags["DONATIONGIFTAIDLAST" + str(idx)] = ""
    idx = 1
    for d in donasc:
        tags["RECEIPTNUM" + str(idx)] = utils.padleft(d["ID"], 8)
        tags["DONATIONTYPE" + str(idx)] = d["DONATIONNAME"]
        tags["DONATIONDATE" + str(idx)] = python2display(l, d["DATE"])
        tags["DONATIONDATEDUE" + str(idx)] = python2display(l, d["DATEDUE"])
        tags["DONATIONAMOUNT" + str(idx)] = format_currency_no_symbol(l, d["DONATION"])
        tags["DONATIONCOMMENTS" + str(idx)] = d["COMMENTS"]
        tags["DONATIONGIFTAID" + str(idx)] = d["ISGIFTAID"] == 1 and _("Yes", l) or _("No", l)
    idx = 1
    uniquetypes = {}
    recentrec = {}
    for d in dondesc:
        tags["RECEIPTNUMLAST" + str(idx)] = utils.padleft(d["ID"], 8)
        tags["DONATIONTYPELAST" + str(idx)] = d["DONATIONNAME"]
        tags["DONATIONDATELAST" + str(idx)] = python2display(l, d["DATE"])
        tags["DONATIONDATEDUELAST" + str(idx)] = python2display(l, d["DATEDUE"])
        tags["DONATIONAMOUNTLAST" + str(idx)] = format_currency_no_symbol(l, d["DONATION"])
        tags["DONATIONCOMMENTSLAST" + str(idx)] = d["COMMENTS"]
        tags["DONATIONGIFTAIDLAST" + str(idx)] = d["ISGIFTAID"] == 1 and _("Yes", l) or _("No", l)
        idx += 1
        # If this is the first of this type of donation we've seen, make
        # some keys based on its name.
        if not uniquetypes.has_key(d["DONATIONNAME"]):
            dname = d["DONATIONNAME"].upper().replace(" ", "").replace("/", "")
            uniquetypes[d["DONATIONNAME"]] = d
            tags["RECEIPTNUM" + dname] = utils.padleft(d["ID"], 8)
            tags["DONATIONTYPE" + dname] = d["DONATIONNAME"]
            tags["DONATIONDATE" + dname] = python2display(l, d["DATE"])
            tags["DONATIONDATEDUE" + dname] = python2display(l, d["DATEDUE"])
            tags["DONATIONAMOUNT" + dname] = format_currency_no_symbol(l, d["DONATION"])
            tags["DONATIONCOMMENTS" + dname] = d["COMMENTS"]
            tags["DONATIONGIFTAID" + dname] = d["ISGIFTAID"] == 1 and _("Yes", l) or _("No", l)
        # If this is the first of this type of donation we've seen that's received
        if not recentrec.has_key(d["DONATIONNAME"]) and d["DATE"] is not None:
            dname = d["DONATIONNAME"].upper().replace(" ", "").replace("/", "")
            recentrec[d["DONATIONNAME"]] = d
            tags["RECEIPTNUMRECENT" + dname] = utils.padleft(d["ID"], 8)
            tags["DONATIONTYPERECENT" + dname] = d["DONATIONNAME"]
            tags["DONATIONDATERECENT" + dname] = python2display(l, d["DATE"])
            tags["DONATIONDATEDUERECENT" + dname] = python2display(l, d["DATEDUE"])
            tags["DONATIONAMOUNTRECENT" + dname] = format_currency_no_symbol(l, d["DONATION"])
            tags["DONATIONCOMMENTSRECENT" + dname] = d["COMMENTS"]
            tags["DONATIONGIFTAIDRECENT" + dname] = d["ISGIFTAID"] == 1 and _("Yes", l) or _("No", l)

    # Logs
    logasc = log.get_logs(dbo, log.ANIMAL, int(a["ID"]), 0, log.ASCENDING)
    logdesc = log.get_logs(dbo, log.ANIMAL, int(a["ID"]), 0, log.DESCENDING)
    for idx in range(1, 101):
        tags["LOGNAME" + str(idx)] = ""
        tags["LOGDATE" + str(idx)] = ""
        tags["LOGCOMMENTS" + str(idx)] = ""
        tags["LOGNAMELAST" + str(idx)] = ""
        tags["LOGDATELAST" + str(idx)] = ""
        tags["LOGCOMMENTSLAST" + str(idx)] = ""
    idx = 1
    for o in logasc:
        tags["LOGNAME" + str(idx)] = o["LOGTYPENAME"]
        tags["LOGDATE" + str(idx)] = python2display(l, o["DATE"])
        tags["LOGCOMMENTS" + str(idx)] = o["COMMENTS"]
        idx += 1
    idx = 1
    uniquetypes = {}
    recentgiven = {}
    for o in logdesc:
        tags["LOGNAMELAST" + str(idx)] = o["LOGTYPENAME"]
        tags["LOGDATELAST" + str(idx)] = python2display(l, o["DATE"])
        tags["LOGCOMMENTSLAST" + str(idx)] = o["COMMENTS"]
        idx += 1
        uniquetypes = {}
        recentrec = {}
        # If this is the first of this type of log we've seen, make
        # some keys based on its name.
        if not uniquetypes.has_key(o["LOGTYPENAME"]):
            lname = o["LOGTYPENAME"].upper().replace(" ", "").replace("/", "")
            uniquetypes[o["LOGTYPENAME"]] = o
            tags["LOGNAME" + lname] = o["LOGTYPENAME"]
            tags["LOGDATE" + lname] = python2display(l, o["DATE"])
            tags["LOGCOMMENTS" + lname] = o["COMMENTS"]
            tags["LOGNAMERECENT" + lname] = o["LOGTYPENAME"]
            tags["LOGDATERECENT" + lname] = python2display(l, o["DATE"])
            tags["LOGCOMMENTSRECENT" + lname] = o["COMMENTS"]

    return tags

def donation_tags(dbo, p):
    """
    Generates a list of tags from a donation result.
    """
    l = dbo.locale
    tags = { 
        "DONATIONID"            : str(p["ID"]),
        "RECEIPTNUM"            : utils.padleft(p["ID"], 8),
        "DONATIONTYPE"          : p["DONATIONNAME"],
        "DONATIONDATE"          : python2display(l, p["DATE"]),
        "DONATIONDATEDUE"       : python2display(l, p["DATEDUE"]),
        "DONATIONAMOUNT"        : format_currency_no_symbol(l, p["DONATION"]),
        "DONATIONCOMMENTS"      : p["COMMENTS"],
        "DONATIONGIFTAID"       : p["ISGIFTAIDNAME"],
        "DONATIONCREATEDBY"     : p["CREATEDBY"],
        "DONATIONCREATEDBYNAME" : p["CREATEDBY"],
        "DONATIONCREATEDDATE"   : python2display(l, p["CREATEDDATE"]),
        "DONATIONLASTCHANGEDBY" : p["LASTCHANGEDBY"],
        "DONATIONLASTCHANGEDBYNAME" : p["LASTCHANGEDBY"],
        "DONATIONLASTCHANGEDDATE" : python2display(l, p["LASTCHANGEDDATE"])
    }
    return tags

def person_tags(dbo, p):
    """
    Generates a list of tags from a person result (the deep type from
    calling person.get_person)
    """
    l = dbo.locale
    tags = { 
        "OWNERID"               : str(p["ID"]),
        "OWNERCODE"             : p["OWNERCODE"],
        "OWNERTITLE"            : p["OWNERTITLE"],
        "TITLE"                 : p["OWNERTITLE"],
        "OWNERINITIALS"         : p["OWNERINITIALS"],
        "INITIALS"              : p["OWNERINITIALS"],
        "OWNERFORENAMES"        : p["OWNERFORENAMES"],
        "FORENAMES"             : p["OWNERFORENAMES"],
        "OWNERFIRSTNAMES"       : p["OWNERFORENAMES"],
        "FIRSTNAMES"            : p["OWNERFORENAMES"],
        "OWNERSURNAME"          : p["OWNERSURNAME"],
        "SURNAME"               : p["OWNERSURNAME"],
        "OWNERLASTNAME"         : p["OWNERSURNAME"],
        "LASTNAME"              : p["OWNERSURNAME"],
        "OWNERNAME"             : p["OWNERNAME"],
        "NAME"                  : p["OWNERNAME"],
        "OWNERADDRESS"          : p["OWNERADDRESS"],
        "ADDRESS"               : p["OWNERADDRESS"],
        "OWNERTOWN"             : p["OWNERTOWN"],
        "TOWN"                  : p["OWNERTOWN"],
        "OWNERCOUNTY"           : p["OWNERCOUNTY"],
        "COUNTY"                : p["OWNERCOUNTY"],
        "OWNERCITY"             : p["OWNERTOWN"],
        "CITY"                  : p["OWNERTOWN"],
        "OWNERSTATE"            : p["OWNERCOUNTY"],
        "STATE"                 : p["OWNERCOUNTY"],
        "OWNERPOSTCODE"         : p["OWNERPOSTCODE"],
        "POSTCODE"              : p["OWNERPOSTCODE"],
        "OWNERZIPCODE"          : p["OWNERPOSTCODE"],
        "ZIPCODE"               : p["OWNERPOSTCODE"],
        "HOMETELEPHONE"         : p["HOMETELEPHONE"],
        "WORKTELEPHONE"         : p["WORKTELEPHONE"],
        "MOBILETELEPHONE"       : p["MOBILETELEPHONE"],
        "CELLTELEPHONE"         : p["MOBILETELEPHONE"],
        "EMAILADDRESS"          : p["EMAILADDRESS"],
        "OWNERCOMMENTS"         : p["COMMENTS"],
        "COMMENTS"              : p["COMMENTS"],
        "OWNERCREATEDBY"        : p["CREATEDBY"],
        "OWNERCREATEDBYNAME"    : p["CREATEDBY"],
        "OWNERCREATEDDATE"      : python2display(l, p["CREATEDDATE"]),
        "OWNERLASTCHANGEDBY"    : p["LASTCHANGEDBY"],
        "OWNERLASTCHANGEDBYNAME" : p["LASTCHANGEDBY"],
        "OWNERLASTCHANGEDDATE"  : python2display(l, p["LASTCHANGEDDATE"]),
        "IDCHECK"               : (p["IDCHECK"] == 1 and _("Yes", l) or _("No", l)),
        "MEMBERSHIPNUMBER"      : p["MEMBERSHIPNUMBER"],
        "MEMBERSHIPEXPIRYDATE"  : python2display(l, p["MEMBERSHIPEXPIRYDATE"])
    }

    # Additional fields
    add = additional.get_additional_fields(dbo, int(p["ID"]), "person")
    for af in add:
        val = af["VALUE"]
        if af["FIELDTYPE"] == additional.YESNO:
            val = additional_yesno(l, af)
        tags[af["FIELDNAME"].upper()] = val

    return tags

def append_tags(tags1, tags2):
    """
    Adds two dictionaries of tags together and returns
    a new dictionary containing both sets.
    """
    tags = {}
    tags.update(tags1)
    tags.update(tags2)
    return tags

def substitute_tags_plain(searchin, tags):
    """
    Substitutes the dictionary of tags in "tags" for any found in
    "searchin". This is a convenience method for plain text substitution
    with << >> opener/closers and no XML escaping.
    """
    return substitute_tags(searchin, tags, False, "<<", ">>")

def substitute_tags(searchin, tags, use_xml_escaping = True, opener = "&lt;&lt;", closer = "&gt;&gt;"):
    """
    Substitutes the dictionary of tags in "tags" for any found
    in "searchin". opener and closer denote the start of a tag,
    if use_xml_escaping is set to true, then tags are XML escaped when
    output and opener/closer are escaped.
    """
    if not use_xml_escaping:
        opener = opener.replace("&lt;", "<").replace("&gt;", ">")
        closer = closer.replace("&lt;", "<").replace("&gt;", ">")

    s = searchin
    sp = s.find(opener)
    while sp != -1:
        ep = s.find(closer, sp + len(opener))
        if ep != -1:
            matchtag = s[sp + len(opener):ep].upper()
            newval = ""
            if tags.has_key(matchtag):
                newval = tags[matchtag]
                if newval is not None:
                    newval = str(newval)
                    if use_xml_escaping and not newval.lower().startswith("<img"):
                        newval = newval.replace("&", "&amp;")
                        newval = newval.replace("<", "&lt;")
                        newval = newval.replace(">", "&gt;")
            s = s[0:sp] + str(newval) + s[ep + len(closer):]
            sp = s.find(opener, sp)
        else:
            # No end marker for this tag, stop processing
            break
    return s

def generate_animal_doc(dbo, template, animalid, username):
    """
    Generates an animal document from a template using animal keys and
    (if a currentowner is available) person keys
    template: The path/name of the template to use
    animalid: The animal to generate for
    """
    s = dbfs.get_string_id(dbo, template)
    a = animal.get_animal(dbo, animalid)
    if a is None: raise utils.ASMValidationError("%d is not a valid animal ID" % animalid)
    tags = animal_tags(dbo, a)
    if a["CURRENTOWNERID"] is not None and a["CURRENTOWNERID"] != 0:
        tags = append_tags(tags, person_tags(dbo, person.get_person(dbo, int(a["CURRENTOWNERID"]))))
    tags = append_tags(tags, org_tags(dbo, username))
    s = substitute_tags(s, tags)
    return s

def generate_person_doc(dbo, template, personid, username):
    """
    Generates a person document from a template
    template: The path/name of the template to use
    personid: The person to generate for
    """
    s = dbfs.get_string_id(dbo, template)
    p = person.get_person(dbo, personid)
    if p is None: raise utils.ASMValidationError("%d is not a valid person ID" % personid)
    tags = person_tags(dbo, p)
    tags = append_tags(tags, org_tags(dbo, username))
    s = substitute_tags(s, tags)
    return s

def generate_donation_doc(dbo, template, donationid, username):
    """
    Generates a donation document from a template
    template: The path/name of the template to use
    donationid: The donation to generate for
    """
    s = dbfs.get_string_id(dbo, template)
    d = financial.get_donation(dbo, donationid)
    if d is None: raise utils.ASMValidationError("%d is not a valid donation ID" % donationid)
    tags = donation_tags(dbo, d)
    tags = append_tags(tags, person_tags(dbo, person.get_person(dbo, int(d["OWNERID"]))))
    if d["ANIMALID"] is not None and d["ANIMALID"] != 0:
        tags = append_tags(tags, animal_tags(dbo, animal.get_animal(dbo, d["ANIMALID"])))
    tags = append_tags(tags, org_tags(dbo, username))
    s = substitute_tags(s, tags)
    return s


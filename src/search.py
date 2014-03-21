#!/usr/bin/python

"""
Main ASM search functionality
"""

import animal
import configuration
import datetime
import lostfound
import person
import publish
import time
import users
import waitinglist
from i18n import _, now

def search(dbo, session, q):

    """
    Performs a database wide search for the term given.
    special tokens:

    a:term      Only search animals for term
    p:term      Only search people for term
    wl:term     Only search waiting list entries for term

    sort:az     Sort results alphabetically az
    sort:za     Sort results alphabetically za
    sort:mr     Sort results most recently changed first
    sort:lr     Sort results least recently changed first


    onshelter/os, notforadoption, hold, quarantine, deceased, forpublish
    people, vets, retailers, staff, fosterers, volunteers, shelters, aco, 
    homechecked, homecheckers, members, donors, reservenohomecheck

    returns a tuple of:
    results, timetaken, explain, sortname
    """
    # ar (add results) inner method
    def ar(rlist, rtype, sortfield):
        # Return brief records
        if rtype == "ANIMAL":
            rlist = animal.get_animals_brief(rlist)
        if rtype == "PERSON":
            pass # TODO:
        for r in rlist:
            r["RESULTTYPE"] = rtype
            if sortfield == "RELEVANCE":
                # How "relevant" is this record to what was searched for?
                # animal name and code weight higher than other elements.
                # Note that the code below modifies inbound var q, so by the
                # time we read it here, it should only contain the search term 
                # itself. Weight everything else by last changed date so there
                # is some semblance of useful order for less relevant items
                r["SORTON"] = r["LASTCHANGEDDATE"]
                qlow = q.lower()
                if rtype == "ANIMAL":
                    if r["ANIMALNAME"].lower() == qlow or r["SHELTERCODE"].lower() == qlow or r["SHORTCODE"].lower() == qlow:
                        r["SORTON"] = now()
                    # Put matches where term present just behind direct matches
                    if r["ANIMALNAME"].lower().find(qlow) != -1 or r["SHELTERCODE"].lower().find(qlow) != -1 or r["SHORTCODE"].lower().find(qlow) != -1:
                        r["SORTON"] = now() - datetime.timedelta(seconds=1)
                elif rtype == "PERSON":
                    if r["OWNERSURNAME"].lower() == qlow or r["OWNERNAME"].lower() == qlow:
                        r["SORTON"] = now()
                    # Put matches where term present just behind direct matches
                    if r["OWNERSURNAME"].lower().find(qlow) or r["OWNERNAME"].lower().find(qlow):
                        r["SORTON"] = now() - datetime.timedelta(seconds=1)
            else:
                r["SORTON"] = r[sortfield]
            results.append(r)

    l = dbo.locale

    # start the clock
    starttime = time.time()

    # The returned results
    results = []
    
    # An i18n explanation of what was searched for
    explain = ""

    # Max records to be returned by search
    limit = configuration.record_search_limit(dbo)

    # Default sort for the search
    searchsort = configuration.search_sort(dbo)

    q = q.replace("'", "`")

    # Allow the sort to be overridden
    if q.find("sort:") != -1:
        if "sort:az" in q:
            searchsort = 0
            q = q.replace("sort:az", "")
        elif "sort:za" in q:
            searchsort = 1
            q = q.replace("sort:za", "")
        elif "sort:lr" in q:
            searchsort = 2
            q = q.replace("sort:lr", "")
        elif "sort:mr" in q:
            searchsort = 3
            q = q.replace("sort:mr", "")
        elif "sort:as" in q:
            searchsort = 4
            q = q.replace("sort:as", "")
        elif "sort:sa" in q:
            searchsort = 5
            q = q.replace("sort:sa", "")
        elif "sort:rel" in q:
            searchsort = 6
            q = q.replace("sort:rel", "")

    q = q.strip()

    # Only search indexed fields in larger databases
    indexed_only = dbo.is_large_db

    # Handle sorting ===========================
    animalsort = ""
    personsort = ""
    wlsort = ""
    lasort = ""
    fasort = ""
    sortdir = "a"
    sortname = ""
    # alphanumeric ascending
    if searchsort == 0:
        animalsort = "ANIMALNAME"
        personsort = "OWNERNAME"
        wlsort = "OWNERNAME"
        lasort = "OWNERNAME"
        fasort = "OWNERNAME"
        sortdir = "a"
        sortname = _("Alphabetically A-Z", l)
    # alphanumeric descending
    elif searchsort == 1:
        animalsort = "ANIMALNAME"
        personsort = "OWNERNAME"
        wlsort = "OWNERNAME"
        lasort = "OWNERNAME"
        fasort = "OWNERNAME"
        sortdir = "d"
        sortname = _("Alphabetically Z-A", l)
    # last changed ascending
    elif searchsort == 2:
        animalsort = "LASTCHANGEDDATE"
        personsort = "LASTCHANGEDDATE"
        wlsort = "LASTCHANGEDDATE"
        lasort = "LASTCHANGEDDATE"
        fasort = "LASTCHANGEDDATE"
        sortdir = "a"
        sortname = _("Least recently changed", l)
    # last changed descending
    elif searchsort == 3:
        animalsort = "LASTCHANGEDDATE"
        personsort = "LASTCHANGEDDATE"
        wlsort = "LASTCHANGEDDATE"
        lasort = "LASTCHANGEDDATE"
        fasort = "LASTCHANGEDDATE"
        sortdir = "d"
        sortname = _("Most recently changed", l)
    # species ascending
    elif searchsort == 4:
        animalsort = "SPECIESNAME"
        # This will look screwy if you ask for a species sort and there
        # are records other than animals in there
        personsort = "LASTCHANGEDDATE"
        wlsort = "LASTCHANGEDDATE"
        lasort = "LASTCHANGEDDATE"
        fasort = "LASTCHANGEDDATE"
        sortdir = "a"
        sortname = _("Species A-Z", l)
    elif searchsort == 5:
        animalsort = "SPECIESNAME"
        # This will look screwy if you ask for a species sort and there
        # are records other than animals in there
        personsort = "LASTCHANGEDDATE"
        wlsort = "LASTCHANGEDDATE"
        lasort = "LASTCHANGEDDATE"
        fasort = "LASTCHANGEDDATE"
        sortdir = "d"
        sortname = _("Species Z-A", l)
    elif searchsort == 6:
        animalsort = "RELEVANCE"
        personsort = "RELEVANCE"
        wlsort = "RELEVANCE"
        lasort = "RELEVANCE"
        fasort = "RELEVANCE"
        sortdir = "d"
        sortname = _("Most relevant", l)

    # Special token searches
    if q == "onshelter" or q == "os":
        ar(animal.get_animal_find_simple(dbo, "", "all", limit), "ANIMAL", animalsort)
        explain = _("All animals on the shelter.", l)
    elif q == "notforadoption":
        ar(animal.get_animals_not_for_adoption(dbo), "ANIMAL", animalsort)
        explain = _("All animals who are flagged as not for adoption.", l)
    elif q == "hold":
        ar(animal.get_animals_hold(dbo), "ANIMAL", animalsort)
        explain = _("All animals who are currently held in case of reclaim.", l)
    elif q == "quarantine":
        ar(animal.get_animals_quarantine(dbo), "ANIMAL", animalsort)
        explain = _("All animals who are currently quarantined.", l)
    elif q == "deceased":
        ar(animal.get_animals_recently_deceased(dbo), "ANIMAL", animalsort)
        explain = _("Recently deceased shelter animals (last 30 days).", l)
    elif q == "forpublish":
        pc = publish.PublishCriteria(configuration.publisher_presets(dbo))
        ar(publish.get_animal_data(dbo, pc), "ANIMAL", animalsort)
        explain = _("All animals matching current publishing options.", l)
    elif q == "people":
        ar(person.get_person_find_simple(dbo, "", "all", users.check_permission_bool(session, users.VIEW_STAFF), limit), "PERSON", personsort)
        explain = _("All people on file.", l)
    elif q == "vets":
        ar(person.get_person_find_simple(dbo, "", "vet", users.check_permission_bool(session, users.VIEW_STAFF), limit), "PERSON", personsort)
        explain = _("All vets on file.", l)
    elif q == "retailers":
        ar(person.get_person_find_simple(dbo, "", "retailer", users.check_permission_bool(session, users.VIEW_STAFF), limit), "PERSON", personsort)
        explain = _("All retailers on file.", l)
    elif q == "staff":
        ar(person.get_person_find_simple(dbo, "", "staff", users.check_permission_bool(session, users.VIEW_STAFF), limit), "PERSON", personsort)
        explain = _("All staff on file.", l)
    elif q == "fosterers":
        ar(person.get_person_find_simple(dbo, "", "fosterer", users.check_permission_bool(session, users.VIEW_STAFF), limit), "PERSON", personsort)
        explain = _("All fosterers on file.", l)
    elif q == "volunteers":
        ar(person.get_person_find_simple(dbo, "", "volunteer", users.check_permission_bool(session, users.VIEW_STAFF), limit), "PERSON", personsort)
        explain = _("All volunteers on file.", l)
    elif q == "shelters":
        ar(person.get_person_find_simple(dbo, "", "shelter", users.check_permission_bool(session, users.VIEW_STAFF), limit), "PERSON", personsort)
        explain = _("All animal shelters on file.", l)
    elif q == "aco":
        ar(person.get_person_find_simple(dbo, "", "aco", users.check_permission_bool(session, users.VIEW_STAFF), limit), "PERSON", personsort)
        explain = _("All animal care officers on file.", l)
    elif q == "homechecked":
        ar(person.get_person_find_simple(dbo, "", "homechecked", users.check_permission_bool(session, users.VIEW_STAFF), limit), "PERSON", personsort)
        explain = _("All homechecked owners on file.", l)
    elif q == "homecheckers":
        ar(person.get_person_find_simple(dbo, "", "homechecker", users.check_permission_bool(session, users.VIEW_STAFF), limit), "PERSON", personsort)
        explain = _("All homecheckers on file.", l)
    elif q == "members":
        ar(person.get_person_find_simple(dbo, "", "member", users.check_permission_bool(session, users.VIEW_STAFF), limit), "PERSON", personsort)
        explain = _("All members on file.", l)
    elif q == "donors":
        ar(person.get_person_find_simple(dbo, "", "donor", users.check_permission_bool(session, users.VIEW_STAFF), limit), "PERSON", personsort)
        explain = _("All donors on file.", l)
    elif q == "reservenohomecheck":
        ar(person.get_reserves_without_homechecks(dbo), "PERSON", personsort)
        explain = _("People with active reservations, but no homecheck has been done.", l)
    elif q == "overduedonations":
        ar(person.get_overdue_donations(dbo), "PERSON", personsort)
        explain = _("People with overdue donations.", l)
    elif q == "activelost":
        ar(lostfound.get_lostanimal_find_simple(dbo, ""), "LOSTANIMAL", lasort)
        explain = _("Lost animals reported in the last 30 days.", l)
    elif q == "activefound":
        ar(lostfound.get_foundanimal_find_simple(dbo, ""), "FOUNDANIMAL", fasort)
        explain = _("Found animals reported in the last 30 days.", l)
    elif q.startswith("a:") or q.startswith("animal:"):
        q = q[q.find(":")+1:].strip()
        explain = _("Animals matching '{0}'.", l).format(q)
        ar( animal.get_animal_find_simple(dbo, q, "all", limit, indexed_only), "ANIMAL", animalsort )
    elif q.startswith("p:") or q.startswith("person:"):
        q = q[q.find(":")+1:].strip()
        explain = _("People matching '{0}'.", l).format(q)
        ar( person.get_person_find_simple(dbo, q, "all", users.check_permission_bool(session, users.VIEW_STAFF), limit, indexed_only), "PERSON", personsort )
    elif q.startswith("wl:") or q.startswith("waitinglist:"):
        q = q[q.find(":")+1:].strip()
        explain = _("Waiting list entries matching '{0}'.", l).format(q)
        ar( waitinglist.get_waitinglist_find_simple(dbo, q, limit, indexed_only), "WAITINGLIST", wlsort )
    elif q.startswith("la:") or q.startswith("lostanimal:"):
        q = q[q.find(":")+1:].strip()
        explain = _("Lost animal entries matching '{0}'.", l).format(q)
        ar( lostfound.get_lostanimal_find_simple(dbo, q, limit, indexed_only), "LOSTANIMAL", lasort )
    elif q.startswith("fa:") or q.startswith("foundanimal:"):
        q = q[q.find(":")+1:].strip()
        explain = _("Found animal entries matching '{0}'.", l).format(q)
        ar( lostfound.get_foundanimal_find_simple(dbo, q, limit, indexed_only), "FOUNDANIMAL", fasort )

    # No special tokens, search everything and collate
    else:
        ar( animal.get_animal_find_simple(dbo, q, "all", limit, indexed_only), "ANIMAL", animalsort )
        ar( person.get_person_find_simple(dbo, q, "all", users.check_permission_bool(session, users.VIEW_STAFF), limit, indexed_only), "PERSON", personsort )
        ar( waitinglist.get_waitinglist_find_simple(dbo, q, limit, indexed_only), "WAITINGLIST", wlsort )
        ar( lostfound.get_lostanimal_find_simple(dbo, q, limit, indexed_only), "LOSTANIMAL", lasort )
        ar( lostfound.get_foundanimal_find_simple(dbo, q, limit, indexed_only), "FOUNDANIMAL", fasort )
        explain = _("Results for '{0}'.", l).format(q)

    # Apply the sort to the results
    if sortdir == "a":
        sortresults = sorted(results, key=lambda k: k["SORTON"])
    else:
        sortresults = sorted(results, reverse=True, key=lambda k: k["SORTON"])

    # stop the clock
    timetaken = (time.time() - starttime)

    # Return our final set of values
    return sortresults, timetaken, explain, sortname


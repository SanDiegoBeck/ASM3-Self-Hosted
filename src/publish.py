#!/usr/bin/python

"""
    Module containing all functions/classes for internet publishing
"""

import al
import additional
import animal
import configuration
import datetime, time
import db
import dbfs
import ftplib
import i18n
import lookups
import lostfound
import math
import media
import medical
import movement
import os, glob
import shutil
import sys
import tempfile
import threading
import users
import utils
import wordprocessor
from sitedefs import MULTIPLE_DATABASES_PUBLISH_DIR, MULTIPLE_DATABASES_PUBLISH_FTP

class PublishCriteria:
    """
    Class containing publishing criteria. Has functions to 
    convert to and from a command line string
    """
    includeCaseAnimals = False
    includeReservedAnimals = False
    includeRetailerAnimals = False
    includeFosterAnimals = False
    includeQuarantine = False
    includeHold = False
    includeWithoutImage = False
    includeColours = False
    bondedAsSingle = False
    clearExisting = False
    uploadAllImages = False
    uploadDirectly = False
    forceReupload = False
    noImportFile = False # If a 3rd party has a seperate import disable upload
    generateJavascriptDB = False
    thumbnails = False
    thumbnailSize = "70x70"
    checkSocket = False
    order = 1 # 0 = Ascending entry, 1 = Descending entry, 2 = Ascending name
    excludeUnderWeeks = 12
    animalsPerPage = 10
    htmlByChildAdult = False # True if html pages should be prefixed baby/adult_ and split
    childAdultSplit=26 # Number of weeks before an animal is treated as an adult by the child adult publisher
    htmlBySpecies = False # True if html pages should be prefixed with species name and split
    limit = 0
    style = "."
    extension = "html"
    scaleImages = "" # A resize spec or old values of: 1 = None, 2 = 320x200, 3=640x480, 4=800x600, 5=1024x768, 6=300x300, 7=95x95
    internalLocations = [] # List of either location IDs, or LIKE comparisons
    publishDirectory = None # None = use temp directory for publishing
    ignoreLock = False # Force the publisher to run even if another publisher is running

    def get_int(self, s):
        """
        Returns the val portion of key=val as an int
        """
        return int(s.split("=")[1])

    def get_str(self, s):
        """
        Returns the val portion of key=val as a string
        """
        return s.split("=")[1]

    def __init__(self, fromstring = ""):
        """
        Initialises the publishing criteria from a string if given
        """
        if fromstring == "": return
        for s in fromstring.split(" "):
            if s == "includecase": self.includeCaseAnimals = True
            if s == "includereserved": self.includeReservedAnimals = True
            if s == "includeretailer": self.includeRetailerAnimals = True
            if s == "includefosters": self.includeFosterAnimals = True
            if s == "includehold": self.includeHold = True
            if s == "includequarantine": self.includeQuarantine = True
            if s == "includewithoutimage": self.includeWithoutImage = True
            if s == "includecolours": self.includeColours = True
            if s == "bondedassingle": self.bondedAsSingle = True
            if s == "noimportfile": self.noImportFile = True
            if s == "clearexisting": self.clearExisting = True
            if s == "uploadall": self.uploadAllImages = True
            if s == "forcereupload": self.forceReupload = True
            if s == "generatejavascriptdb": self.generateJavascriptDB = True
            if s == "thumbnails": self.thumbnails = True
            if s == "checksocket": self.checkSocket = True
            if s == "uploaddirectly": self.uploadDirectly = True
            if s == "htmlbychildadult": self.htmlByChildAdult = True
            if s == "htmlbyspecies": self.htmlBySpecies = True
            if s.startswith("order"): self.order = self.get_int(s)
            if s.startswith("excludeunder"): self.excludeUnderWeeks = self.get_int(s)
            if s.startswith("animalsperpage"): self.animalsPerPage = self.get_int(s)
            if s.startswith("limit"): self.limit = self.get_int(s)
            if s.startswith("style"): self.style = self.get_str(s)
            if s.startswith("extension"): self.extension = self.get_str(s)
            if s.startswith("scaleimages"): self.scaleImages = self.get_str(s)
            if s.startswith("thumbnailsize"): self.thumbnailSize = self.get_str(s)
            if s.startswith("includelocations"): self.internalLocations = self.get_str(s).split(",")
            if s.startswith("publishdirectory"): self.publishDirectory = self.get_str(s)
            if s.startswith("childadultsplit"): self.childAdultSplit = self.get_int(s)

    def __str__(self):
        """
        Returns a string representation of the criteria (which corresponds
        exactly to an ASM 2.x command line string to a publisher)
        """
        s = ""
        if self.includeCaseAnimals: s += " includecase"
        if self.includeReservedAnimals: s += " includereserved"
        if self.includeRetailerAnimals: s += " includeretailer"
        if self.includeFosterAnimals: s += " includefosters"
        if self.includeHold: s += " includehold"
        if self.includeQuarantine: s += " includequarantine"
        if self.includeWithoutImage: s += " includewithoutimage"
        if self.includeColours: s += " includecolours"
        if self.bondedAsSingle: s += " bondedassingle"
        if self.noImportFile: s += " noimportfile"
        if self.clearExisting: s += " clearexisting"
        if self.uploadAllImages: s += " uploadall"
        if self.forceReupload: s += " forcereupload"
        if self.generateJavascriptDB: s += " generatejavascriptdb"
        if self.thumbnails: s += " thumbnails"
        if self.checkSocket: s += " checksocket"
        if self.uploadDirectly: s += " uploaddirectly"
        if self.htmlBySpecies: s += " htmlbyspecies"
        if self.htmlByChildAdult: s += " htmlbychildadult"
        s += " order=" + str(self.order)
        s += " excludeunder=" + str(self.excludeUnderWeeks)
        s += " animalsperpage=" + str(self.animalsPerPage)
        s += " limit=" + str(self.limit)
        s += " style=" + str(self.style)
        s += " extension=" + str(self.extension)
        s += " scaleimages=" + str(self.scaleImages)
        s += " thumbnailsize=" + str(self.thumbnailSize)
        s += " childadultsplit=" + str(self.childAdultSplit)
        if len(self.internalLocations) > 0: s += " includelocations=" + ",".join(self.internalLocations)
        if self.publishDirectory is not None: s += " publishdirectory=" + self.publishDirectory
        return s.strip()

def quietcallback(x):
    """ ftplib callback that does nothing instead of dumping to stdout """
    pass

def get_animal_data(dbo, pc, include_additional_fields = False):
    """
    Returns a resultset containing the animal info for the criteria given. 
    """
    sql = get_animal_data_query(pc)
    rows = db.query(dbo, sql)
    # If the sheltercode format has a slash in it, convert it to prevent
    # creating images with broken paths.
    if len(rows) > 0 and rows[0]["SHELTERCODE"].find("/") != -1:
        for r in rows:
            r["SHORTCODE"] = r["SHORTCODE"].replace("/", "-").replace(" ", "")
            r["SHELTERCODE"] = r["SHELTERCODE"].replace("/", "-").replace(" ", "")
    # Embellish additional fields if requested
    if include_additional_fields:
        for r in rows:
            add = additional.get_additional_fields(dbo, int(r["ID"]), "animal")
            for af in add:
                if af["FIELDNAME"].find("&") != -1:
                    # We've got unicode chars for the tag name - not allowed
                    r["ADD" + str(af["ID"])] = af["VALUE"]
                else:
                    r[af["FIELDNAME"]] = af["VALUE"]
    # If bondedAsSingle is on, go through the the set of animals and merge
    # the bonded animals into a single record
    def merge_animal(a, animalid):
        """
        Find the animal in rows with animalid, merge it into a and
        then remove it from the set.
        """
        for r in rows:
            if r["ID"] == animalid:
                a["ANIMALNAME"] = "%s, %s" % (a["ANIMALNAME"], r["ANIMALNAME"])
                rows.remove(r)
                break
    if pc.bondedAsSingle:
        for r in rows:
            if r["BONDEDANIMALID"] is not None and r["BONDEDANIMALID"] != 0:
                merge_animal(r, r["BONDEDANIMALID"])
            if r["BONDEDANIMAL2ID"] is not None and r["BONDEDANIMAL2ID"] != 0:
                merge_animal(r, r["BONDEDANIMAL2ID"])
    return rows

def get_animal_data_query(pc):
    sql = animal.get_animal_query() + " WHERE a.ID > 0"
    if not pc.includeCaseAnimals: 
        sql += " AND a.CrueltyCase = 0"
    if not pc.includeWithoutImage: 
        sql += " AND EXISTS(SELECT ID FROM media WHERE WebsitePhoto = 1 AND LinkID = a.ID AND LinkTypeID = 0)"
    if not pc.includeReservedAnimals: 
        sql += " AND a.HasActiveReserve = 0"
    if len(pc.internalLocations) > 0 and pc.internalLocations[0].strip() != "null":
        if utils.is_numeric(pc.internalLocations[0]):
            # We have a list of internal location IDs
            sql += " AND a.ShelterLocation IN (%s)" % ",".join(pc.internalLocations)
        else:
            # Must be a list of LIKE name comparisons
            sql += " AND ("
            firstLoc = True
            for fr in pc.internalLocations:
                if firstLoc:
                    firstLoc = False
                else:
                    sql += " OR "
                sql += "il.LocationName LIKE '%s'" % fr.replace("*", "%")
            sql += ")"
    # Make sure animal is old enough
    exclude = i18n.now()
    exclude -= datetime.timedelta(days=pc.excludeUnderWeeks * 7)
    sql += " AND a.DateOfBirth <= " + db.dd(exclude)
    # Filter out dead and unadoptable animals
    sql += " AND a.DeceasedDate Is Null AND a.IsNotAvailableForAdoption = 0"
    # Filter out permanent fosters
    sql += " AND a.HasPermanentFoster = 0"
    # Filter out Hold/Quarantine if they aren't included
    if not pc.includeHold: 
        sql += " AND (a.IsHold = 0 OR a.IsHold Is Null)"
    if not pc.includeQuarantine:
        sql += " AND (a.IsQuarantine = 0 OR a.IsQuarantine Is Null)"
    # If including fosters is on, allow animals with an active type of foster
    # (this picks up foster animals even if foster on shelter is not set)
    if pc.includeFosterAnimals and pc.includeRetailerAnimals:
        sql += " AND (a.Archived = 0 OR a.ActiveMovementType = %d OR a.ActiveMovementType = %d)" % (movement.FOSTER, movement.RETAILER)
    elif pc.includeRetailerAnimals:
        sql += " AND (a.Archived = 0 OR a.ActiveMovementType = %d)" % movement.RETAILER
    elif pc.includeFosterAnimals:
        sql += " AND (a.Archived = 0 OR a.ActiveMovementType = %d)" % movement.FOSTER
    else:
        # On shelter only (this filters out fosters even if foster on shelter is set)
        sql += " AND a.Archived = 0 AND (a.ActiveMovementType Is Null OR a.ActiveMovementType <> %d)" % movement.FOSTER
    # Ordering
    if pc.order == 0:
        sql += " ORDER BY a.MostRecentEntryDate"
    elif pc.order == 1:
        sql += " ORDER BY a.MostRecentEntryDate DESC"
    elif pc.order == 2:
        sql += " ORDER BY a.AnimalName"
    else:
        sql += " ORDER BY a.MostRecentEntryDate"
    # Limit
    if pc.limit > 0:
        sql += " LIMIT %d" % pc.limit
    return sql

class AbstractPublisher(threading.Thread):
    """
    Base class for all publishers
    """
    dbo = None
    pc = None
    totalAnimals = 0
    publisherName = ""
    publishDir = ""
    tempPublishDir = True
    locale = "en"
    lastError = ""
    logBuffer = ""
    logName = ""

    def __init__(self, dbo, publishCriteria):
        threading.Thread.__init__(self)
        self.dbo = dbo
        self.locale = configuration.locale(dbo)
        self.pc = publishCriteria
        self.makePublishDirectory()

    def checkMappedSpecies(self):
        """
        Returns True if all species have been mapped for publishers
        """
        return 0 == db.query_int(self.dbo, "SELECT COUNT(*) FROM species " + \
            "WHERE PetFinderSpecies Is Null OR PetFinderSpecies = ''")

    def checkMappedBreeds(self):
        """
        Returns True if all breeds have been mapped for publishers
        """
        return 0 == db.query_int(self.dbo, "SELECT COUNT(*) FROM breed " + \
            "WHERE PetFinderBreed Is Null OR PetFinderBreed = ''")

    def isPublisherExecuting(self):
        """
        Returns True if a publisher is already currently running against
        this database. If the ignoreLock publishCriteria option has been
        set, always returns false.
        """
        if self.pc.ignoreLock: return False
        execstr = configuration.publisher_executing(self.dbo)
        if execstr.startswith("NONE") or execstr.endswith("100"):
            return False
        else:
            return True

    def updatePublisherProgress(self, progress):
        """
        Updates the publisher progress in the database
        """
        configuration.publisher_executing(self.dbo, self.publisherName, progress)

    def replaceMDBTokens(self, dbo, s):
        """
        Replace MULTIPLE_DATABASE tokens in the string given.
        """
        s = s.replace("{alias}", dbo.alias)
        s = s.replace("{database}", dbo.database)
        s = s.replace("{username}", dbo.username)
        return s

    def replaceAnimalTags(self, a, s):
        """
        Replace any $$Tag$$ tags in s, using animal a
        """
        tags = wordprocessor.animal_tags(self.dbo, a)
        return wordprocessor.substitute_tags(s, tags, True, "$$", "$$")

    def resetPublisherProgress(self):
        """
        Resets the publisher progress and stops blocking for other 
        publishers
        """
        configuration.publisher_executing(self.dbo, "NONE", 0)

    def setPublisherComplete(self):
        """
        Mark the current publisher as complete
        """
        configuration.publisher_executing(self.dbo, self.publisherName, 100)

    def getProgress(self, i, n):
        """
        Returns a progress percentage
        i: Current position
        n: Total elements
        """
        return int((float(i) / float(n)) * 100)

    def shouldStopPublishing(self):
        """
        Returns True if we need to stop publishing
        """
        return configuration.publisher_stop(self.dbo)

    def setStartPublishing(self):
        """
        Clears the stop publishing flag so we can carry on publishing.
        """
        configuration.publisher_stop(self.dbo, "No")

    def setLastError(self, msg):
        """
        Sets the last error message and clears the publisher lock
        """
        configuration.publisher_last_error(self.dbo, msg)
        self.lastError = msg
        self.log(self.lastError)
        self.resetPublisherProgress()

    def makePublishDirectory(self):
        """
        Creates a temporary publish directory if one isn't set, or uses
        the one set in the criteria.
        """
        if self.logName.endswith("html.txt"):
            # It's HTML publishing - we have some special rules
            # If the publishing directory has been overridden, set it
            if MULTIPLE_DATABASES_PUBLISH_DIR != "":
                self.publishDir = MULTIPLE_DATABASES_PUBLISH_DIR
                # Replace any tokens
                self.publishDir = self.replaceMDBTokens(self.dbo, self.publishDir)
                self.pc.ignoreLock = True
                # Validate that the directory exists
                if not os.path.exists(self.publishDir):
                    self.setLastError("publishDir does not exist: %s" % self.publishDir)
                    return
                # If they've set the option to reupload animal images, clear down
                # any existing images first
                if self.pc.forceReupload:
                    for f in os.listdir(self.publishDir):
                        if f.lower().endswith(".jpg"):
                            os.unlink(os.path.join(self.publishDir, f))
                # Clear out any existing HTML pages
                for f in os.listdir(self.publishDir):
                    if f.lower().endswith(".html"):
                        os.unlink(os.path.join(self.publishDir, f))
                self.tempPublishDir = False
                return
            if self.pc.publishDirectory is not None and self.pc.publishDirectory.strip() != "":
                # The user has set a target directory for their HTML publishing, use that
                self.publishDir = self.pc.publishDirectory
                # Fix any Windows path backslashes that could have been doubled up
                if self.publishDir.find("\\\\") != -1:
                    self.publishDir = self.publishDir.replace("\\\\", "\\")
                # Validate that the directory exists
                if not os.path.exists(self.publishDir):
                    self.setLastError("publishDir does not exist: %s" % self.publishDir)
                    return
                # If they've set the option to reupload animal images, clear down
                # any existing images first
                if self.pc.forceReupload:
                    for f in os.listdir(self.publishDir):
                        if f.lower().endswith(".jpg"):
                            os.unlink(os.path.join(self.publishDir, f))
                # Clear out any existing HTML pages
                for f in os.listdir(self.publishDir):
                    if f.lower().endswith(".html"):
                        os.unlink(os.path.join(self.publishDir, f))
                self.tempPublishDir = False
                return
        # Use a temporary folder for publishing
        self.tempPublishDir = True
        self.publishDir = tempfile.mkdtemp()

    def deletePublishDirectory(self):
        """
        Removes the publish directory if it was temporary
        """
        if self.tempPublishDir:
            shutil.rmtree(self.publishDir, True)

    def getAnimalInClause(self, animals):
        """
        Returns an IN clause of comma separated animal ids from the list
        """
        batch = []
        for a in animals:
            batch.append(str(a["ID"]))
        return ",".join(batch)

    def getDescription(self, an, crToBr = False):
        """
        Returns the description/bio for an animal.
        """
        notes = an["WEBSITEMEDIANOTES"]
        if notes is None: notes = ""
        if notes == "" and configuration.publisher_use_comments_for_blank_notes(self.dbo):
            notes = an["ANIMALCOMMENTS"]
        # Add any extra text
        notes += configuration.third_party_publisher_sig(self.dbo)
        # Replace any wp tags used in the notes
        notes = self.replaceAnimalTags(an, notes)
        # Escape carriage returns
        cr = ""
        if crToBr: 
            cr = "<br />"
        notes = notes.replace("\r\n", cr)
        notes = notes.replace("\r", cr)
        notes = notes.replace("\n", cr)
        # Escape speechmarks
        notes = notes.replace("\"", "\"\"")
        return notes

    def markAnimalPublished(self, field, linkid, clear = False):
        """
        Marks an animal published at the current date/time
        field: The field in the media table
        id:    The animal id to update
        clear: True if we should be removing the date instead of setting it to now
        """
        datevalue = i18n.now(self.dbo.timezone)
        if clear:
            datevalue = None
        db.execute(self.dbo, "UPDATE media SET %s = %s WHERE LinkID = %d AND LinkTypeID = 0" % (
            field, db.dd(datevalue), linkid))

    def markAnimalsPublished(self, field, animals):
        """
        Marks all animals in the set as published at the current date/time in field
        """
        batch = self.getAnimalInClause(animals)
        db.execute(self.dbo, "UPDATE media SET NewSinceLastPublish = 0, UpdatedSinceLastPublish = 0, " \
            "%s = %s WHERE WebSitePhoto = 1 AND LinkTypeID = 0 AND LinkID IN (%s)" % (
            field, db.dd(i18n.now(self.dbo.timezone)), batch))

    def getMatchingAnimals(self):
        a = get_animal_data(self.dbo, self.pc)
        self.log("Got %d matching animals for publishing." % len(a))
        return a

    def saveFile(self, path, contents):
        f = open(path, "wb")
        f.write(contents)
        f.flush()
        f.close()

    def log(self, msg):
        """
        Logs a message
        """
        self.logBuffer += msg + "\n"
        al.debug(utils.truncate(msg, 1023), self.publisherName, self.dbo)

    def logError(self, msg, ie=None):
        """
        Logs a message to stdout and dumps a stacktrace.
        ie = error info object from sys.exc_info() if available
        """
        self.log(msg)
        al.error(msg, self.publisherName, self.dbo, ie)

    def setLogName(self, logname):
        """
        Sets the logname based on the publisher type given and
        the current date/time.
        """
        d = datetime.datetime.today()
        s = "%d-%02d-%02d_%02d:%02d_%s.txt" % ( d.year, d.month, d.day, d.hour, d.minute, logname )
        self.logName = s

    def saveLog(self):
        """
        Saves the log to the dbfs
        """
        dbfs.put_string_filepath(self.dbo, "/logs/publish/%s" % self.logName, self.logBuffer)

    def isImage(self, path):
        """
        Returns True if the path given has a valid image extension
        """
        return path.lower().endswith("jpg") or path.lower().endswith("jpeg")

    def generateThumbnail(self, image, thumbnail):
        """
        Generates a thumbnail 
        image: Path to the image to generate a thumbnail from
        thumbnail: Path to the target thumbnail image
        """
        self.log("generating thumbnail %s -> %s" % ( image, thumbnail ))
        try:
            media.scale_image_file(image, thumbnail, self.pc.thumbnailSize)
        except Exception,err:
            self.logError("Failed scaling thumbnail: %s" % err, sys.exc_info())

    def scaleImage(self, image, scalesize):
        """
        Scales an image. scalesize is the scaleImage publish criteria and
        can either be a resize spec, or it can be one of our old ASM2
        fixed numbers.
        image: The image file
        Empty string = No scaling
        1 = No scaling
        2 = 320x200
        3 = 640x400
        4 = 800x600
        5 = 1024x768
        6 = 300x300
        7 = 95x95
        """
        sizespec = ""
        if scalesize == "" or scalesize == "1": return image
        elif scalesize == "2": sizespec = "320x200"
        elif scalesize == "3": sizespec = "640x400"
        elif scalesize == "4": sizespec = "800x600"
        elif scalesize == "5": sizespec = "1024x768"
        elif scalesize == "6": sizespec = "300x300"
        elif scalesize == "7": sizespec = "95x95"
        else: sizespec = scalesize
        self.log("scaling %s to %s" % ( image, scalesize ))
        try:
            return media.scale_image_file(image, image, sizespec)
        except Exception,err:
            self.logError("Failed scaling image: %s" % err, sys.exc_info())

class FTPPublisher(AbstractPublisher):
    """
    Base class for publishers that rely on FTP
    """
    socket = None
    ftphost = ""
    ftpuser = ""
    ftppassword = ""
    ftpport = 21
    ftproot = ""
    currentDir = ""
    passive = True

    def __init__(self, dbo, publishCriteria, ftphost, ftpuser, ftppassword, ftpport = 21, ftproot = "", passive = True):
        AbstractPublisher.__init__(self, dbo, publishCriteria)
        self.ftphost = ftphost
        self.ftpuser = ftpuser
        self.ftppassword = ftppassword
        self.ftpport = ftpport
        self.ftproot = ftproot
        self.passive = passive

    def openFTPSocket(self):
        """
        Opens an FTP socket to the server and changes to the
        root FTP directory. Returns True if all was well or
        uploading is disabled.
        """
        if not self.pc.uploadDirectly: return True
        if self.ftphost.strip() == "": raise ValueError("No FTP host set")
        self.log("Connecting to %s as %s" % (self.ftphost, self.ftpuser))
        
        try:
            # open it and login
            self.socket = ftplib.FTP(host=self.ftphost, timeout=15)
            self.socket.login(self.ftpuser, self.ftppassword)
            self.socket.set_pasv(self.passive)

            if self.ftproot is not None and self.ftproot != "":
                # If we had an FTP override, try and create the directory
                # before we change to it.
                if MULTIPLE_DATABASES_PUBLISH_FTP is not None:
                    self.mkdir(self.ftproot)
                self.chdir(self.ftproot)

            return True
        except Exception,err:
            self.logError("Failed opening FTP socket (%s->%s): %s" % (self.dbo.database, self.ftphost, err), sys.exc_info())
            return False

    def closeFTPSocket(self):
        if not self.pc.uploadDirectly: return
        try:
            self.socket.quit()
        except:
            pass

    def checkFTPSocket(self):
        """
        Called before each upload if publishCriteria.checkSocket is
        set to true. It verifies that the socket is still active
        by running a command. If the command fails, the socket is
        reopened and the current FTP directory is returned to.
        """
        if not self.pc.uploadDirectly: return
        try:
            self.socket.retrlines("LIST", quietcallback)
        except Exception,err:
            self.log("Dead socket (%s), reconnecting" % err)
            self.closeFTPSocket()
            self.openFTPSocket()
            if not self.currentDir == "":
                self.chdir(self.currentDir)

    def upload(self, filename):
        """
        Uploads a file to the current FTP directory. If a full path
        is given, this throws it away and just uses the name with
        the temporary publishing directory.
        """
        if filename.find(os.sep) != -1: filename = filename[filename.rfind(os.sep) + 1:]
        if not self.pc.uploadDirectly: return
        if not os.path.exists(os.path.join(self.publishDir, filename)): return
        self.log("Uploading: %s" % filename)
        try:
            if self.pc.checkSocket: self.checkFTPSocket()
            # Force upload if it's our specific extension, a js, cfg or csv file
            # or has no extension (like datafiles for PetFinder, etc)
            if filename.find(".%s" % self.pc.extension) != -1 or \
               filename.find(".js") != -1 or \
               filename.find(".cfg") != -1 or \
               filename.find(".csv") != -1 or \
               filename.find(".") == -1:
                f = open(os.path.join(self.publishDir, filename), "rb")
                self.socket.storbinary("STOR %s" % filename, f, callback=quietcallback)
                f.close()
            # Does the file already exist? If it does, bail out if we're not forcing it
            files = self.socket.retrlines("LIST", quietcallback)
            if files.find(filename) != -1 and not self.pc.forceReupload:
                self.log("%s: already exists on server." % filename)
                return
            f = open(os.path.join(self.publishDir, filename), "rb")
            self.socket.storbinary("STOR %s" % filename, f, callback=quietcallback)
            f.close()
        except Exception, err:
            self.logError("Failed uploading %s: %s" % (filename, err), sys.exc_info())

    def mkdir(self, newdir):
        if not self.pc.uploadDirectly: return
        self.log("FTP mkdir %s" % newdir)
        try:
            self.socket.mkd(newdir)
        except Exception,err:
            self.log("mkdir %s: already exists (%s)" % (newdir, err))

    def chdir(self, newdir, fromroot = ""):
        if not self.pc.uploadDirectly: return
        self.log("FTP chdir to %s" % newdir)
        try:
            self.socket.cwd(newdir)
            if fromroot == "":
                self.currentDir = newdir
            else:
                self.currentDir = fromroot
        except Exception, err:
            self.logError("chdir %s: %s" % (newdir, err), sys.exc_info())

    def clearExistingHTML(self):
        try:
            oldfiles = glob.glob(os.path.join(self.publishDir, "*." + self.pc.extension))
            for f in oldfiles:
                os.remove(f)
        except Exception, err:
            self.logError("warning: failed removing %s from filesystem: %s" % (oldfiles, err), sys.exc_info())
        if not self.pc.uploadDirectly: return
        try:
            for f in self.socket.nlst("*.%s" % self.pc.extension):
                if not f.startswith("search"):
                    self.socket.delete(f)
        except Exception, err:
            self.logError("warning: failed deleting from FTP server: %s" % err, sys.exc_info())

    def cleanup(self):
        """
        Call when the publisher has completed to tidy up.
        """
        self.closeFTPSocket()
        self.deletePublishDirectory()
        self.saveLog()
        self.setPublisherComplete()


    def uploadImage(self, a, medianame, imagename):
        """
        Retrieves image with medianame from the DBFS to the publish
        folder and uploads it via FTP with imagename
        """
        try:
            self.log("Retrieving image: %d::%s" % ( a["ID"], imagename ))
            imagefile = os.path.join(self.publishDir, imagename)
            thumbnail = os.path.join(self.publishDir, "tn_" + imagename)
            dbfs.get_file(self.dbo, medianame, "", imagefile)
            self.log("Retrieved image: %d::%s" % ( a["ID"], imagename ))
            # If scaling is on, do it
            if self.pc.scaleImages > 1:
                self.scaleImage(imagefile, self.pc.scaleImages)
            # If thumbnails are on, do it
            if self.pc.thumbnails:
                self.generateThumbnail(imagefile, thumbnail)
            # Upload
            if self.pc.uploadDirectly:
                self.upload(imagefile)
                if self.pc.thumbnails:
                    self.upload(thumbnail)
        except Exception, err:
            self.logError("Failed uploading image %s: %s" % (medianame, err), sys.exc_info())
            return 0

    def uploadImages(self, a, copyWithMediaIDAsName = False, limit = 0):
        """
        Uploads all the images for an animal as sheltercode-X.jpg if
        upload all is on, or just sheltercode.jpg if upload all is off.
        If copyWithMediaIDAsName is on, it uploads the preferred
        image again and calls it mediaID.jpg (for compatibility with
        older templates).
        Even if uploadDirectly is off, we still pull the images to the
        publish folder.
        If limit is set to zero and uploadAll is on, all images
        are uploaded. If uploadAll is off, only the preferred
        image is uploaded.
        Images with the ExcludeFromPublish flag set are ignored.
        """
        # The first image is always the preferred
        totalimages = 0
        animalcode = a["SHELTERCODE"]
        animalweb = a["WEBSITEMEDIANAME"]
        if animalweb is None or animalweb == "": return totalimages
        # Name it sheltercode-1.jpg or sheltercode.jpg if uploadall is off
        imagename = animalcode + ".jpg"
        if self.pc.uploadAllImages:
            imagename = animalcode + "-1.jpg"
        # Save it to the publish directory
        totalimages = 1
        self.uploadImage(a, animalweb, imagename)
        # If we're saving a copy with the media ID, do that too
        if copyWithMediaIDAsName:
            self.uploadImage(a, animalweb, animalweb)
        # If upload all is set, we need to grab the rest of
        # the animal's images upto the limit. If the limit is
        # zero, we upload everything.
        if self.pc.uploadAllImages:
            mrecs = media.get_image_media(self.dbo, media.ANIMAL, a["ID"], True)
            self.log("Animal has %d media files" % len(mrecs))
            for m in mrecs:
                # Ignore the main media since we used that
                if m["MEDIANAME"] == animalweb:
                    continue
                # Have we hit our limit?
                if totalimages == limit:
                    return totalimages
                totalimages += 1
                # Get the image
                otherpic = m["MEDIANAME"]
                imagename = "%s-%d.jpg" % ( animalcode, totalimages )
                self.uploadImage(a, otherpic, imagename)
        return totalimages

class HTMLPublisher(FTPPublisher):
    """
    Handles publishing to the internet via static HTML files to 
    an FTP server.
    """
    javascript = ""
    javaArrayElement = 0
    navbar = ""
    totalAnimals = 0
    user = "cron"

    def __init__(self, dbo, publishCriteria, user):
        l = dbo.locale
        self.user = user
        self.publisherName = i18n._("HTML/FTP Publisher", l)
        self.setLogName("html")
        # If we have a database override and it's not been ignored, use it
        if MULTIPLE_DATABASES_PUBLISH_FTP is not None and not configuration.publisher_ignore_ftp_override(dbo):
            c = MULTIPLE_DATABASES_PUBLISH_FTP
            publishCriteria.uploadDirectly = True
            FTPPublisher.__init__(self, dbo, publishCriteria,
                self.replaceMDBTokens(dbo, c["host"]),
                self.replaceMDBTokens(dbo, c["user"]),
                self.replaceMDBTokens(dbo, c["pass"]),
                c["port"], 
                self.replaceMDBTokens(dbo, c["chdir"]),
                c["passive"])
        else:                
            FTPPublisher.__init__(self, dbo, publishCriteria, 
                configuration.ftp_host(dbo), configuration.ftp_user(dbo), configuration.ftp_password(dbo),
                configuration.ftp_port(dbo), configuration.ftp_root(dbo), configuration.ftp_passive(dbo))

    def getPathFromStyle(self):
        """
        Looks at the publishing criteria and returns a DBFS path to get
        the template files from
        """
        if self.pc.style == ".": return "/internet"
        return "/internet/" + self.pc.style

    def getHeader(self):
        path = self.getPathFromStyle()
        self.log("Getting header style from: %s" % path)
        header = dbfs.get_string(self.dbo, "head.html", path)
        if header == "": header = dbfs.get_string(self.dbo, "pih.dat", path)
        if header == "":
            header = """<html>
            <head>
            <title>Animals Available For Adoption</title>
            </head>
            <body>
            <p>$$NAV$$</p>
            <table width="100%%">
            """
        return header

    def getFooter(self):
        path = self.getPathFromStyle()
        self.log("Getting footer style from: %s" % path)
        footer = dbfs.get_string(self.dbo, "foot.html", path)
        if footer == "": footer = dbfs.get_string(self.dbo, "pif.dat", path)
        if footer == "":
            footer = "</table></body></html>"
        return footer

    def getBody(self):
        path = self.getPathFromStyle()
        body = dbfs.get_string(self.dbo, "body.html", path)
        if body == "": body = dbfs.get_string(self.dbo, "pib.dat", path)
        if body == "":
            body = "<tr><td><img height=200 width=320 src=$$IMAGE$$></td>" \
                "<td><b>$$ShelterCode$$ - $$AnimalName$$</b><br>" \
                "$$BreedName$$ $$SpeciesName$$ aged $$Age$$<br><br>" \
                "<b>Details</b><br><br>$$WebMediaNotes$$<hr></td></tr>"
        return body

    def saveTemplateImages(self):
        """
        Saves all image files in the template folder to the publish directory
        """
        dbfs.get_files(self.dbo, "%.jp%g", self.getPathFromStyle(), self.publishDir)
        dbfs.get_files(self.dbo, "%.png", self.getPathFromStyle(), self.publishDir)
        dbfs.get_files(self.dbo, "%.gif", self.getPathFromStyle(), self.publishDir)
        # TODO: Upload these via FTP

    def substituteHFTag(self, searchin, page, user):
        """
        Substitutes special header and footer tokens in searchin. page
        contains the current page number.
        """
        output = searchin
        nav = self.navbar.replace("<a href=\"%d.%s\">%d</a>" % (page, self.pc.extension, page), str(page))
        output = output.replace("$$NAV$$", nav)
        output = output.replace("$$TOTAL$$", str(self.totalAnimals))
        output = output.replace("$$DATE$$", i18n.python2display(self.locale, i18n.now(self.dbo.timezone)))
        output = output.replace("$$TIME$$", time.strftime("%H:%M:%S", i18n.now().timetuple()))
        output = output.replace("$$VERSION$$", i18n.get_version())
        output = output.replace("$$REGISTEREDTO$$", configuration.organisation(self.dbo))
        output = output.replace("$$USER$$", "%s (%s)" % (user, users.get_real_name(self.dbo, user)))
        output = output.replace("$$ORGNAME$$", configuration.organisation(self.dbo))
        output = output.replace("$$ORGADDRESS$$", configuration.organisation_address(self.dbo))
        output = output.replace("$$ORGTEL$$", configuration.organisation_telephone(self.dbo))
        output = output.replace("$$ORGEMAIL$$", configuration.email(self.dbo))
        return output

    def substituteBodyTags(self, searchin, a):
        """
        Substitutes any tags in the body for animal data
        """
        tags = wordprocessor.animal_tags(self.dbo, a)
        tags["TotalAnimals"] = str(self.totalAnimals)
        tags["IMAGE"] = str(a["WEBSITEMEDIANAME"])
        # If the option is set and we have blank media notes, use
        # the comments instead.
        notes = a["WEBSITEMEDIANOTES"]
        if notes is None: notes = ""
        if notes == "" and configuration.publisher_use_comments_for_blank_notes(self.dbo):
            notes = a["ANIMALCOMMENTS"]
        # Add any extra text and put the tag back
        notes += configuration.third_party_publisher_sig(self.dbo)
        tags["WEBMEDIANOTES"] = notes 
        return wordprocessor.substitute_tags(searchin, tags, True, "$$", "$$")

    def writeJavaScript(self):
        decs = ""
        idx = self.javaArrayElement
        decs += "var publishDate = \"%s\";\n" % (i18n.python2display(self.locale, i18n.now(self.dbo.timezone)))
        decs += "var aname = new Array(%d);\n" % idx
        decs += "var age = new Array(%d);\n" % idx
        decs += "var image = new Array(%d);\n" % idx
        decs += "var breed = new Array(%d);\n" % idx
        decs += "var species = new Array(%d);\n" % idx
        decs += "var type = new Array(%d);\n" % idx
        decs += "var colour = new Array(%d);\n" % idx
        decs += "var shelterlocation = new Array(%d);\n" % idx
        decs += "var markings = new Array(%d);\n" % idx
        decs += "var details = new Array(%d);\n" % idx
        decs += "var sheltercode = new Array(%d);\n" % idx
        decs += "var dateofbirth = new Array(%d);\n" % idx
        decs += "var sex = new Array(%d);\n" % idx
        decs += "var size = new Array(%d);\n" % idx
        decs += "var goodwithkids = new Array(%d);\n" % idx
        decs += "var goodwithcats = new Array(%d);\n" % idx
        decs += "var goodwithdogs = new Array(%d);\n" % idx
        decs += "var housetrained = new Array(%d);\n" % idx
        decs += "var comments = new Array(%d);\n" % idx
        self.javascript = decs + self.javascript
        self.saveFile(os.path.join(self.publishDir, "db.js"), self.javascript)
        if self.pc.uploadDirectly:
            self.log("Uploading javascript database...")
            self.upload("db.js")
            self.log("Uploaded javascript database.")

    def updateJavaScript(self, a):
        idx = self.javaArrayElement
        javascript = "aname[%d] = \"%s\";\n" % ( idx, a["ANIMALNAME"] )
        javascript += "image[%d] = \"%s\";\n" % ( idx, a["WEBSITEMEDIANAME"] )
        javascript += "age[%d] = \"%s\";\n" % ( idx, a["ANIMALAGE"] )
        javascript += "breed[%d] = \"%s\";\n" % ( idx, a["BREEDNAME"] )
        javascript += "species[%d] = \"%s\";\n" % ( idx, a["SPECIESNAME"] )
        javascript += "type[%d] = \"%s\";\n" % ( idx, a["ANIMALTYPENAME"] )
        javascript += "colour[%d] = \"%s\";\n" % ( idx, a["BASECOLOURNAME"] )
        javascript += "shelterlocation[%d] = \"%s\";\n" % ( idx, a["SHELTERLOCATIONNAME"] )
        javascript += "markings[%d] = \"%s\";\n" % ( idx, str(a["MARKINGS"]).replace("\"", "\\\"").replace("\n", " "))
        javascript += "details[%d] = \"%s\";\n" % ( idx, a["WEBSITEMEDIANOTES"] )
        javascript += "sheltercode[%d] = \"%s\";\n" % ( idx, a["SHELTERCODE"] )
        javascript += "dateofbirth[%d] = \"%s\";\n" % ( idx, i18n.python2display(self.locale, a["DATEOFBIRTH"] ))
        javascript += "sex[%d] = \"%s\";\n" % ( idx, a["SEXNAME"] )
        javascript += "size[%d] = \"%s\";\n" % ( idx, a["SIZENAME"] )
        javascript += "goodwithkids[%d] = \"%s\";\n" % ( idx, a["ISGOODWITHCHILDRENNAME"] )
        javascript += "goodwithcats[%d] = \"%s\";\n" % ( idx, a["ISGOODWITHCATSNAME"] )
        javascript += "goodwithdogs[%d] = \"%s\";\n" % ( idx, a["ISGOODWITHDOGSNAME"] )
        javascript += "housetrained[%d] = \"%s\";\n" % ( idx, a["ISHOUSETRAINEDNAME"] )
        javascript += "comments[%d] = \"%s\";\n" % ( idx, str(a["ANIMALCOMMENTS"] ).replace("\"", "\\\"").replace("\n", " "))
        self.javascript += javascript
        self.javaArrayElement += 1

    def run(self):
        self.setLastError("")
        if self.isPublisherExecuting(): return
        self.updatePublisherProgress(0)
        self.setStartPublishing()
        if self.pc.htmlByChildAdult or self.pc.htmlBySpecies:
            self.executeAgeSpecies(self.user, self.pc.htmlByChildAdult, self.pc.htmlBySpecies)
        else:
            self.executePages()
        self.resetPublisherProgress()

    def executeAgeSpecies(self, user, childadult = True, species = True):
        """
        Publisher that puts animals on pages by age and species
        childadult: True if we should split up pages by animals under/over 6 months 
        species: True if we should split up pages by species
        """
        self.log("HTMLPublisher starting...")

        normHeader = self.getHeader()
        normFooter = self.getFooter()
        body = self.getBody()
        header = self.substituteHFTag(normHeader, 0, user)
        footer = self.substituteHFTag(normFooter, 0, user)

        # Calculate the number of days old an animal has to be to
        # count as an adult
        childAdultSplitDays = self.pc.childAdultSplit * 7

        # Open FTP socket, bail if it fails
        if not self.openFTPSocket():
            self.setLastError("Failed opening FTP socket.")
            return
            
        # Clear any existing uploaded files
        if self.pc.clearExisting: 
            self.clearExistingHTML()

        try:
            animals = self.getMatchingAnimals()
            self.totalAnimals = len(animals)

            anCount = 0
            pages = {}

            # Create default pages for every possible permutation
            defaultpages = []
            if childadult and species:
                spec = lookups.get_species(self.dbo)
                for sp in spec:
                    defaultpages.append("adult" + sp["SPECIESNAME"])
                    defaultpages.append("baby" + sp["SPECIESNAME"])
            elif childadult:
                defaultpages = [ "adult", "baby" ]
            elif species:
                spec = lookups.get_species(self.dbo)
                for sp in spec:
                    defaultpages.append(sp["SPECIESNAME"])
            for dp in defaultpages:
                pages[dp + "." + self.pc.extension] = header

            # Create an all page
            allpage = "all." + self.pc.extension
            pages[allpage] = header

        except Exception, err:
            self.logError("Error setting up page: %s" % err, sys.exc_info())
            self.setLastError("Error setting up page: %s" % err)
            return

        for an in animals:
            try:
                anCount += 1

                # If a limit was set, stop now
                if self.pc.limit > 0 and anCount > self.pc.limit:
                    self.log("Hit publishing limit of %d animals. Stopping." % self.pc.limit)
                    break

                self.log("Processing: %s: %s (%d of %d)" % ( an["SHELTERCODE"], an["ANIMALNAME"], anCount, self.totalAnimals))
                self.updatePublisherProgress(self.getProgress(anCount, len(animals)))

                # If the user cancelled, stop now
                if self.shouldStopPublishing(): 
                    self.log("User cancelled publish. Stopping.")
                    self.resetPublisherProgress()
                    self.cleanup()
                    return

                # upload all images for this animal to our current FTP
                self.uploadImages(an, True)
                
                # Update our ongoing javascript db
                if self.pc.generateJavascriptDB: self.updateJavaScript(an)

                # Calculate the new page name
                pagename = "." + self.pc.extension
                if species:
                    pagename = an["SPECIESNAME"] + pagename
                if childadult:
                    days = i18n.date_diff_days(an["DATEOFBIRTH"], i18n.now(self.dbo.timezone))
                    if days < childAdultSplitDays:
                        pagename = "baby" + pagename
                    else:
                        pagename = "adult" + pagename

                # Does this page exist?
                if not pages.has_key(pagename):
                    # No, create it and add the header
                    page = header
                else:
                    page = pages[pagename]

                # Add this item to the page
                page += self.substituteBodyTags(body, an)
                pages[pagename] = page
                self.log("Finished processing: %s" % an["SHELTERCODE"])

                # Add this item to our magic "all" page
                page = pages[allpage]
                page += self.substituteBodyTags(body, an)
                pages[allpage] = page

            except Exception,err:
                self.logError("Failed processing animal: %s, %s" % (str(an["SHELTERCODE"]), err), sys.exc_info())

        # Mark published
        self.markAnimalsPublished("LastPublished", animals)

        # Upload the pages
        for k, v in pages.iteritems():
            self.log("Saving page to disk: %s" % k)
            self.saveFile(os.path.join(self.publishDir, k), v + footer)
            self.log("Saved page to disk: %s" % k)
            if self.pc.uploadDirectly:
                self.log("Uploading page: %s" % k)
                self.upload(k)
                self.log("Uploaded page: %s" % k)
        # Handle javascript db
        if self.pc.generateJavascriptDB:
            self.writeJavaScript()
        # Save any additional images required by the template
        self.saveTemplateImages()
        self.cleanup()

    def executePages(self):
        """
        Publisher based on assigning animals to pages.
        """

        self.log("HTMLPublisher starting...")

        user = self.user
        normHeader = self.getHeader()
        normFooter = self.getFooter()
        body = self.getBody()

        # Open FTP socket, bail if it fails
        if not self.openFTPSocket():
            self.setLastError("Failed opening FTP socket.")
            return

        # Clear any existing uploaded files
        if self.pc.clearExisting: 
            self.clearExistingHTML()
        
        try:
            animals = self.getMatchingAnimals()
            self.totalAnimals = len(animals)
            noPages = 0
            animalsPerPage = self.pc.animalsPerPage

            # Calculate pages required
            if self.totalAnimals <= animalsPerPage:
                noPages = 1
            else:
                noPages = math.ceil(float(self.totalAnimals) / float(animalsPerPage))

            # Page navigation bar
            if noPages > 1:
                self.navbar = ""
                for i in range(1, int(noPages + 1)):
                    self.navbar += "<a href=\"%d.%s\">%d</a>&nbsp;" % ( i, self.pc.extension, i )

            # Start a new page with a header
            thisPageName = "1." + self.pc.extension
            currentPage = 1
            itemsOnPage = 0

            # Substitute tags in the header and footer
            header = self.substituteHFTag(normHeader, currentPage, user)
            footer = self.substituteHFTag(normFooter, currentPage, user)
            thisPage = header
            anCount = 0
        except Exception, err:
            self.setLastError("Error setting up page: %s" % err)
            self.logError("Error setting up page: %s" % err, sys.exc_info())
            return

        for an in animals:
            try:
                anCount += 1

                # If a limit was set, stop now
                if self.pc.limit > 0 and anCount > self.pc.limit:
                    self.log("Hit publishing limit of %d animals. Stopping." % self.pc.limit)
                    break

                self.log("Processing: %s: %s (%d of %d)" % ( an["SHELTERCODE"], an["ANIMALNAME"], anCount, self.totalAnimals))
                self.updatePublisherProgress(self.getProgress(anCount, len(animals)))

                # If the user cancelled, stop now
                if self.shouldStopPublishing(): 
                    self.log("User cancelled publish. Stopping.")
                    self.resetPublisherProgress()
                    self.cleanup()
                    return

                # upload all images for this animal to our current FTP
                self.uploadImages(an, True)
                
                # Update our ongoing javascript db
                if self.pc.generateJavascriptDB: self.updateJavaScript(an)

                # Slot free on this page?
                if itemsOnPage < animalsPerPage:
                    thisPage += self.substituteBodyTags(body, an)
                    itemsOnPage += 1
                    self.log("Finished processing: %s" % an["SHELTERCODE"])
                else:
                    self.log("Current page complete.")
                    # No, append the footer, flush and upload the page
                    thisPage += footer
                    self.log("Saving page to disk: %s" % thisPageName)
                    self.saveFile(os.path.join(self.publishDir, thisPageName), thisPage)
                    self.log("Saved page to disk: %s" % thisPageName)
                    if self.pc.uploadDirectly:
                        self.log("Uploading page: %s" % thisPageName)
                        self.upload(thisPageName)
                        self.log("Uploaded page: %s" % thisPageName)
                    # New page
                    currentPage += 1
                    thisPageName = "%d.%s" % ( currentPage, self.pc.extension )
                    header = self.substituteHFTag(normHeader, currentPage, user)
                    footer = self.substituteHFTag(normFooter, currentPage, user)
                    thisPage = header
                    # Append this animal
                    thisPage += self.substituteBodyTags(body, an)
                    itemsOnPage = 1
                    self.log("Finished processing: %s" % an["SHELTERCODE"])

            except Exception,err:
                self.logError("Failed processing animal: %s, %s" % (str(an["SHELTERCODE"]), err), sys.exc_info())

        # Mark published
        self.markAnimalsPublished("LastPublished", animals)

        # Done with animals, append the template footer, flush the final
        # page to disk and clean up
        thisPage += footer
        self.saveFile(os.path.join(self.publishDir, thisPageName), thisPage)
        if self.pc.uploadDirectly:
            self.log("Uploading final page.")
            self.upload(thisPageName)
            self.log("Final page uploaded.")
        # Handle javascript db
        if self.pc.generateJavascriptDB:
            self.writeJavaScript()
        # Save any additional images required by the template
        self.saveTemplateImages()
        self.cleanup()

class PetFinderPublisher(FTPPublisher):
    """
    Handles publishing to PetFinder.com
    """
    def __init__(self, dbo, publishCriteria):
        l = dbo.locale
        publishCriteria.uploadDirectly = True
        publishCriteria.thumbnails = False
        publishCriteria.checkSocket = True
        publishCriteria.scaleImages = 1
        self.publisherName = i18n._("PetFinder Publisher", l)
        self.setLogName("petfinder")
        FTPPublisher.__init__(self, dbo, publishCriteria, 
            configuration.petfinder_host(dbo), configuration.petfinder_user(dbo), 
            configuration.petfinder_password(dbo))

    def pfYesNo(self, condition):
        """
        Returns a CSV entry for yes or no based on the condition
        """
        if condition:
            return "\"1\""
        else:
            return "\"\""

    def run(self):

        self.log("PetFinderPublisher starting...")

        if self.isPublisherExecuting(): return
        self.updatePublisherProgress(0)
        self.setLastError("")
        self.setStartPublishing()

        if not self.checkMappedSpecies():
            self.setLastError("Not all species have been mapped.")
            self.cleanup()
            return
        if not self.checkMappedBreeds():
            self.setLastError("Not all breeds have been mapped.")
            self.cleanup()
            return
        shelterid = configuration.petfinder_user(self.dbo)
        if shelterid == "":
            self.setLastError("No PetFinder.com shelter id has been set.")
            self.cleanup()
            return
        animals = self.getMatchingAnimals()
        if len(animals) == 0:
            self.setLastError("No animals found to publish.")
            self.cleanup()
            return

        if not self.openFTPSocket(): 
            self.setLastError("Failed opening FTP socket.")
            self.cleanup()
            return

        # Do the images first
        self.mkdir("import")
        self.chdir("import")
        self.mkdir("photos")
        self.chdir("photos", "import/photos")

        csv = []

        anCount = 0
        for an in animals:
            try:
                line = []
                anCount += 1
                self.log("Processing: %s: %s (%d of %d)" % ( an["SHELTERCODE"], an["ANIMALNAME"], anCount, len(animals)))
                self.updatePublisherProgress(self.getProgress(anCount, len(animals)))

                # If the user cancelled, stop now
                if self.shouldStopPublishing(): 
                    self.log("User cancelled publish. Stopping.")
                    self.resetPublisherProgress()
                    self.cleanup()
                    return

                # If a limit was set, stop now
                if self.pc.limit > 0 and anCount > self.pc.limit:
                    self.log("Hit publishing limit of %d animals. Stopping." % self.pc.limit)
                    break

                # Upload images for this animal
                self.uploadImages(an, False, 3)
                # Mapped species
                line.append("\"%s\"" % an["PETFINDERSPECIES"])
                # Breed 1
                line.append("\"%s\"" % an["PETFINDERBREED"])
                # Age, one of Adult, Baby, Senior and Young
                ageinyears = i18n.date_diff_days(an["DATEOFBIRTH"], i18n.now(self.dbo.timezone))
                ageinyears /= 365.0
                agename = "Adult"
                if ageinyears < 0.5: agename = "Baby"
                elif ageinyears < 2: agename = "Young"
                elif ageinyears < 9: agename = "Adult"
                else: agename = "Senior"
                line.append("\"%s\"" % agename)
                # Name
                line.append("\"%s\"" % an["ANIMALNAME"].replace("\"", "\"\""))
                # Size, one of S, M, L, XL
                ansize = "M"
                if an["SIZE"] == 0: ansize = "XL"
                elif an["SIZE"] == 1: ansize = "L"
                elif an["SIZE"] == 2: ansize = "M"
                elif an["SIZE"] == 3: ansize = "S"
                line.append("\"%s\"" % ansize)
                # Sex, one of M or F
                sexname = "M"
                if an["SEX"] == 0: sexname = "F"
                line.append("\"%s\"" % sexname)
                # Description
                line.append("\"%s\"" % self.getDescription(an, True))
                # Special needs
                if an["CRUELTYCASE"] == 1:
                    line.append("\"1\"")
                elif an["HASSPECIALNEEDS"] == 1:
                    line.append("\"1\"")
                else:
                    line.append("\"\"")
                # Has shots
                line.append(self.pfYesNo(medical.get_vaccinated(self.dbo, int(an["ID"]))))
                # Altered
                line.append(self.pfYesNo(an["NEUTERED"] == 1))
                # No Dogs
                line.append(self.pfYesNo(an["ISGOODWITHDOGS"] == 1))
                # No Cats
                line.append(self.pfYesNo(an["ISGOODWITHCATS"] == 1))
                # No Kids
                line.append(self.pfYesNo(an["ISGOODWITHCHILDREN"] == 1))
                # No Claws
                line.append(self.pfYesNo(an["DECLAWED"] == 1))
                # Housebroken
                line.append(self.pfYesNo(an["ISHOUSETRAINED"] == 0))
                # ID
                line.append("\"%s\"" % an["SHELTERCODE"])
                # Breed 2
                if an["CROSSBREED"] == 1:
                    # If the second breed is one of our magic words, then don't
                    # send it. PetFinder indicate unknown crosses with a blank second
                    # breed but crossbreed set.
                    b2 = an["BREEDNAME2"].lower()
                    if b2 == "mix" or b2 == "cross"  or b2 == "unknown" or b2 == "crossbreed":
                        line.append("\"\"")
                    else:
                        line.append("\"%s\"" % an["PETFINDERBREED2"])
                else:
                    line.append("\"\"")
                # Mix
                line.append(self.pfYesNo(an["CROSSBREED"] == 1))
                # Add to our CSV file
                csv.append(",".join(line))
            except Exception,err:
                self.logError("Failed processing animal: %s, %s" % (str(an["SHELTERCODE"]), err), sys.exc_info())

        # Mark published
        self.markAnimalsPublished("LastPublishedPF", animals)

        # Upload the datafiles
        mapfile = "; PetFinder import map. This file was autogenerated by\n" \
            "; Animal Shelter Manager. http://sheltermanager.com\n" \
            "; The FREE, open source solution for animal sanctuaries and rescue shelters.\n\n" \
            "#SHELTERID:%s\n" \
            "#0:Animal=Animal\n" \
            "#1:Breed=Breed\n" \
            "#2:Age=Age\n" \
            "#3:Name=Name\n" \
            "#4:Size=Size\n" \
            "#5:Sex=Sex\n" \
            "Female=F\n" \
            "Male=M\n" \
            "#6:Description=Dsc\n" \
            "#7:SpecialNeeds=SpecialNeeds\n" \
            "#8:HasShots=HasShots\n" \
            "#9:Altered=Altered\n" \
            "#10:NoDogs=NoDogs\n" \
            "#11:NoCats=NoCats\n" \
            "#12:NoKids=NoKids\n" \
            "#13:Declawed=Declawed\n" \
            "#14:HouseBroken=HouseBroken\n" \
            "#15:Id=Id\n" \
            "#16:Breed2=Breed2\n" \
            "#ALLOWUPDATE:Y\n" \
            "#HEADER:N" % shelterid
        self.saveFile(os.path.join(self.publishDir, shelterid + "import.cfg"), mapfile)
        self.saveFile(os.path.join(self.publishDir, shelterid), "\n".join(csv))
        self.log("Uploading datafile and map, %s %s" % (shelterid, shelterid + "import.cfg"))
        self.chdir("..", "import")
        self.upload(shelterid)
        self.upload(shelterid + "import.cfg")
        self.log("Uploaded %s %s" % ( shelterid, shelterid + "import.cfg"))
        self.cleanup()

class AdoptAPetPublisher(FTPPublisher):
    """
    Handles publishing to AdoptAPet.com
    """
    def __init__(self, dbo, publishCriteria):
        l = dbo.locale
        publishCriteria.uploadDirectly = True
        publishCriteria.checkSocket = True
        publishCriteria.scaleImages = 1
        self.publisherName = i18n._("AdoptAPet Publisher", l)
        self.setLogName("adoptapet")
        FTPPublisher.__init__(self, dbo, publishCriteria, 
            configuration.adoptapet_host(dbo), configuration.adoptapet_user(dbo), 
            configuration.adoptapet_password(dbo))

    def apYesNo(self, condition):
        """
        Returns a CSV entry for yes or no based on the condition
        """
        if condition:
            return "\"1\""
        else:
            return "\"0\""

    def apYesNoUnknown(self, ourval):
        """
        Returns a CSV entry for yes or no based on our yes/no/unknown.
        In our scheme 0 = yes, 1 = no, 2 = unknown
        Their scheme 0 = no, 1 = yes, blank = unknown
        """
        if ourval == "0":
            return "\"1\""
        elif ourval == "1":
            return "\"0\""
        else:
            return "\"\""

    def apMapFile(self, includecolours):
        defmap = "; AdoptAPet.com import map. This file was autogenerated by\n" \
            "; Animal Shelter Manager. http://sheltermanager.com\n" \
            "; The FREE, open source solution for animal sanctuaries and rescue shelters.\n\n" \
            "#1:Id=Id\n" \
            "#2:Animal=Animal\n" \
            "Sugar Glider=Small Animal\n" \
            "Mouse=Small Animal\n" \
            "Rat=Small Animal\n" \
            "Hedgehog=Small Animal\n" \
            "Dove=Bird\n" \
            "Ferret=Small Animal\n" \
            "Chinchilla=Small Animal\n" \
            "Snake=Reptile\n" \
            "Tortoise=Reptile\n" \
            "Terrapin=Reptile\n" \
            "Chicken=Farm Animal\n" \
            "Owl=Bird\n" \
            "Goat=Farm Animal\n" \
            "Goose=Bird\n" \
            "Gerbil=Small Animal\n" \
            "Cockatiel=Bird\n" \
            "Guinea Pig=Small Animal\n" \
            "Hamster=Small Animal\n" \
            "Camel=Horse\n" \
            "Pony=Horse\n" \
            "Donkey=Horse\n" \
            "Llama=Horse\n" \
            "Pig=Farm Animal\n" \
            "#3:Breed=Breed\n" \
            "Appenzell Mountain Dog=Shepherd (Unknown Type)\n" \
            "Australian Cattle Dog/Blue Heeler=Australian Cattle Dog\n" \
            "Belgian Shepherd Dog Sheepdog=Belgian Shepherd\n" \
            "Belgian Shepherd Tervuren=Belgian Tervuren\n" \
            "Belgian Shepherd Malinois=Belgian Malinois\n" \
            "Black Labrador Retriever=Labrador Retriever\n" \
            "Brittany Spaniel=Brittany\n" \
            "Cane Corso Mastiff=Cane Corso\n" \
            "Chinese Crested Dog=Chinese Crested\n" \
            "Chinese Foo Dog=Shepherd (Unknown Type)\n" \
            "Dandi Dinmont Terrier=Dandie Dinmont Terrier\n" \
            "English Cocker Spaniel=Cocker Spaniel\n" \
            "English Coonhound=English (Redtick) Coonhound\n" \
            "Flat-coated Retriever=Flat-Coated Retriever\n" \
            "Fox Terrier=Fox Terrier (Smooth)\n" \
            "Hound=Hound (Unknown Type)\n" \
            "Illyrian Sheepdog=Shepherd (Unknown Type)\n" \
            "McNab =Shepherd (Unknown Type)\n" \
            "New Guinea Singing Dog=Shepherd (Unknown Type)\n" \
            "Newfoundland Dog=Newfoundland\n" \
            "Norweigan Lundehund=Shepherd (Unknown Type)\n" \
            "Peruvian Inca Orchid=Shepherd (Unknown Type)\n" \
            "Poodle=Poodle (Standard)\n" \
            "Retriever=Retriever (Unknown Type)\n" \
            "Saint Bernard St. Bernard=St. Bernard\n" \
            "Schipperkev=Schipperke\n" \
            "Schnauzer=Schnauzer (Standard)\n" \
            "Scottish Terrier Scottie=Scottie, Scottish Terrier\n" \
            "Setter=Setter (Unknown Type)\n" \
            "Sheep Dog=Old English Sheepdog\n" \
            "Shepherd=Shepherd (Unknown Type)\n" \
            "Shetland Sheepdog Sheltie=Sheltie, Shetland Sheepdog\n" \
            "Spaniel=Spaniel (Unknown Type)\n" \
            "Spitz=Spitz (Unknown Type, Medium)\n" \
            "South Russian Ovcharka=Shepherd (Unknown Type)\n" \
            "Terrier=Terrier (Unknown Type, Small)\n" \
            "West Highland White Terrier Westie=Westie, West Highland White Terrier\n" \
            "White German Shepherd=German Shepherd Dog\n" \
            "Wire-haired Pointing Griffon=Wirehaired Pointing Griffon\n" \
            "Wirehaired Terrier=Terrier (Unknown Type, Medium)\n" \
            "Yellow Labrador Retriever=Labrador Retriever\n" \
            "Yorkshire Terrier Yorkie=Yorkie, Yorkshire Terrier\n" \
            "American Siamese=Siamese\n" \
            "Bobtail=American Bobtail\n" \
            "Burmilla=Burmese\n" \
            "Canadian Hairless=Sphynx\n" \
            "Dilute Calico=Calico\n" \
            "Dilute Tortoiseshell=Domestic Shorthair\n" \
            "Domestic Long Hair=Domestic Longhair\n" \
            "Domestic Long Hair-black=Domestic Longhair\n" \
            "Domestic Long Hair - buff=Domestic Longhair\n" \
            "Domestic Long Hair-gray=Domestic Longhair\n" \
            "Domestic Long Hair - orange=Domestic Longhair\n" \
            "Domestic Long Hair - orange and white=Domestic Longhair\n" \
            "Domestic Long Hair - gray and white=Domestic Longhair\n" \
            "Domestic Long Hair-white=Domestic Longhair\n" \
            "Domestic Long Hair-black and white=Domestic Longhair\n" \
            "Domestic Medium Hair=Domestic Mediumhair\n" \
            "Domestic Medium Hair - buff=Domestic Mediumhair\n" \
            "Domestic Medium Hair - gray and white=Domestic Mediumhair\n" \
            "Domestic Medium Hair-white=Domestic Mediumhair\n" \
            "Domestic Medium Hair-orange=Domestic Mediumhair\n" \
            "Domestic Medium Hair - orange and white=Domestic Mediumhair\n" \
            "Domestic Medium Hair -black and white=Domestic Mediumhair\n" \
            "Domestic Short Hair=Domestic Shorthair\n" \
            "Domestic Short Hair - buff=Domestic Shorthair\n" \
            "Domestic Short Hair - gray and white=Domestic Shorthair\n" \
            "Domestic Short Hair-white=Domestic Shorthair\n" \
            "Domestic Short Hair-orange=Domestic Shorthair\n" \
            "Domestic Short Hair - orange and white=Domestic Shorthair\n" \
            "Domestic Short Hair -black and white=Domestic Shorthair\n" \
            "Exotic Shorthair=Exotic\n" \
            "Extra-Toes Cat (Hemingway Polydactyl)=Hemingway/Polydactyl\n" \
            "Havana=Havana Brown\n" \
            "Oriental Long Hair=Oriental\n" \
            "Oriental Short Hair=Oriental\n" \
            "Oriental Tabby=Oriental\n" \
            "Pixie-Bob=Domestic Shorthair\n" \
            "Sphynx (hairless cat)=Sphynx\n" \
            "Tabby=Domestic Shorthair\n" \
            "Tabby - Orange=Domestic Shorthair\n" \
            "Tabby - Grey=Domestic Shorthair\n" \
            "Tabby - Brown=Domestic Shorthair\n" \
            "Tabby - white=Domestic Shorthair\n" \
            "Tabby - buff=Domestic Shorthair\n" \
            "Tabby - black=Domestic Shorthair\n" \
            "Tiger=Domestic Shorthair\n" \
            "Torbie=Domestic Shorthair\n" \
            "Tortoiseshell=Domestic Shorthair\n" \
            "Tuxedo=Domestic Shorthair\n" \
            "#4:Breed2=Breed2\n" \
            "Appenzell Mountain Dog=Shepherd (Unknown Type)\n" \
            "Australian Cattle Dog/Blue Heeler=Australian Cattle Dog\n" \
            "Belgian Shepherd Dog Sheepdog=Belgian Shepherd\n" \
            "Belgian Shepherd Tervuren=Belgian Tervuren\n" \
            "Belgian Shepherd Malinois=Belgian Malinois\n" \
            "Black Labrador Retriever=Labrador Retriever\n" \
            "Brittany Spaniel=Brittany\n" \
            "Cane Corso Mastiff=Cane Corso\n" \
            "Chinese Crested Dog=Chinese Crested\n" \
            "Chinese Foo Dog=Shepherd (Unknown Type)\n" \
            "Dandi Dinmont Terrier=Dandie Dinmont Terrier\n" \
            "English Cocker Spaniel=Cocker Spaniel\n" \
            "English Coonhound=English (Redtick) Coonhound\n" \
            "Flat-coated Retriever=Flat-Coated Retriever\n" \
            "Fox Terrier=Fox Terrier (Smooth)\n" \
            "Hound=Hound (Unknown Type)\n" \
            "Illyrian Sheepdog=Shepherd (Unknown Type)\n" \
            "McNab =Shepherd (Unknown Type)\n" \
            "New Guinea Singing Dog=Shepherd (Unknown Type)\n" \
            "Newfoundland Dog=Newfoundland\n" \
            "Norweigan Lundehund=Shepherd (Unknown Type)\n" \
            "Peruvian Inca Orchid=Shepherd (Unknown Type)\n" \
            "Poodle=Poodle (Standard)\n" \
            "Retriever=Retriever (Unknown Type)\n" \
            "Saint Bernard St. Bernard=St. Bernard\n" \
            "Schipperkev=Schipperke\n" \
            "Schnauzer=Schnauzer (Standard)\n" \
            "Scottish Terrier Scottie=Scottie, Scottish Terrier\n" \
            "Setter=Setter (Unknown Type)\n" \
            "Sheep Dog=Old English Sheepdog\n" \
            "Shepherd=Shepherd (Unknown Type)\n" \
            "Shetland Sheepdog Sheltie=Sheltie, Shetland Sheepdog\n" \
            "Spaniel=Spaniel (Unknown Type)\n" \
            "Spitz=Spitz (Unknown Type, Medium)\n" \
            "South Russian Ovcharka=Shepherd (Unknown Type)\n" \
            "Terrier=Terrier (Unknown Type, Small)\n" \
            "West Highland White Terrier Westie=Westie, West Highland White Terrier\n" \
            "White German Shepherd=German Shepherd Dog\n" \
            "Wire-haired Pointing Griffon=Wirehaired Pointing Griffon\n" \
            "Wirehaired Terrier=Terrier (Unknown Type, Medium)\n" \
            "Yellow Labrador Retriever=Labrador Retriever\n" \
            "Yorkshire Terrier Yorkie=Yorkie, Yorkshire Terrier\n" \
            "American Siamese=Siamese\n" \
            "Bobtail=American Bobtail\n" \
            "Burmilla=Burmese\n" \
            "Canadian Hairless=Sphynx\n" \
            "Dilute Calico=Calico\n" \
            "Dilute Tortoiseshell=Domestic Shorthair\n" \
            "Domestic Long Hair=Domestic Longhair\n" \
            "Domestic Long Hair-black=Domestic Longhair\n" \
            "Domestic Long Hair - buff=Domestic Longhair\n" \
            "Domestic Long Hair-gray=Domestic Longhair\n" \
            "Domestic Long Hair - orange=Domestic Longhair\n" \
            "Domestic Long Hair - orange and white=Domestic Longhair\n" \
            "Domestic Long Hair - gray and white=Domestic Longhair\n" \
            "Domestic Long Hair-white=Domestic Longhair\n" \
            "Domestic Long Hair-black and white=Domestic Longhair\n" \
            "Domestic Medium Hair=Domestic Mediumhair\n" \
            "Domestic Medium Hair - buff=Domestic Mediumhair\n" \
            "Domestic Medium Hair - gray and white=Domestic Mediumhair\n" \
            "Domestic Medium Hair-white=Domestic Mediumhair\n" \
            "Domestic Medium Hair-orange=Domestic Mediumhair\n" \
            "Domestic Medium Hair - orange and white=Domestic Mediumhair\n" \
            "Domestic Medium Hair -black and white=Domestic Mediumhair\n" \
            "Domestic Short Hair=Domestic Shorthair\n" \
            "Domestic Short Hair - buff=Domestic Shorthair\n" \
            "Domestic Short Hair - gray and white=Domestic Shorthair\n" \
            "Domestic Short Hair-white=Domestic Shorthair\n" \
            "Domestic Short Hair-orange=Domestic Shorthair\n" \
            "Domestic Short Hair - orange and white=Domestic Shorthair\n" \
            "Domestic Short Hair -black and white=Domestic Shorthair\n" \
            "Exotic Shorthair=Exotic\n" \
            "Extra-Toes Cat (Hemingway Polydactyl)=Hemingway/Polydactyl\n" \
            "Havana=Havana Brown\n" \
            "Oriental Long Hair=Oriental\n" \
            "Oriental Short Hair=Oriental\n" \
            "Oriental Tabby=Oriental\n" \
            "Pixie-Bob=Domestic Shorthair\n" \
            "Sphynx (hairless cat)=Sphynx\n" \
            "Tabby=Domestic Shorthair\n" \
            "Tabby - Orange=Domestic Shorthair\n" \
            "Tabby - Grey=Domestic Shorthair\n" \
            "Tabby - Brown=Domestic Shorthair\n" \
            "Tabby - white=Domestic Shorthair\n" \
            "Tabby - buff=Domestic Shorthair\n" \
            "Tabby - black=Domestic Shorthair\n" \
            "Tiger=Domestic Shorthair\n" \
            "Torbie=Domestic Shorthair\n" \
            "Tortoiseshell=Domestic Shorthair\n" \
            "Tuxedo=Domestic Shorthair\n" \
            "#5:Age=Age\n" \
            "#6:Name=Name\n" \
            "#7:Size=Size\n" \
            "#8:Sex=Sex\n"
        if not includecolours:
            defmap += "#9:Description=Description\n" \
            "#10:Status=Status\n" \
            "#11:GoodWKids=GoodWKids\n" \
            "#12:GoodWCats=GoodWCats\n" \
            "#13:GoodWDogs=GoodWDogs\n" \
            "#14:SpayedNeutered=SpayedNeutered\n" \
            "#15:ShotsCurrent=ShotsCurrent\n" \
            "#16:Housetrained=Housetrained\n" \
            "#17:Declawed=Declawed\n" \
            "#18:SpecialNeeds=SpecialNeeds"
        else:
            defmap += "#9:Color=Color\n" \
            "Amber=Red/Golden/Orange/Chestnut\n" \
            "Black Tortie=Tortoiseshell\n" \
            "Black and Brindle=Black - with Tan, Yellow or Fawn\n" \
            "Black and Brown=Black - with Tan, Yellow or Fawn\n" \
            "Black and Tan=Black - with Tan, Yellow or Fawn\n" \
            "Black and White=Black - with White\n" \
            "Blue=Gray or Blue\n" \
            "Blue Tortie=Tortoiseshell\n" \
            "Brindle and Black=Brindle\n" \
            "Brindle and White=Brindle - with White\n" \
            "Brown=Brown/Chocolate\n" \
            "Brown and Black=Brown/Chocolate - with Black\n" \
            "Brown and White=Brown/Chocolate - with White\n" \
            "Chocolate=Brown/Chocolate\n" \
            "Chocolate Tortie=Tortoiseshell\n" \
            "Cinnamon=Red/Golden/Orange/Chestnut\n" \
            "Cinnamon Tortoiseshell=Tortoiseshell\n" \
            "Cream=White - with Tan, Yellow or Fawn\n" \
            "Fawn=Tan/Yellow/Fawn\n" \
            "Fawn Tortoise=Tortoiseshell\n" \
            "Ginger=Red/Golden/Orange/Chestnut\n" \
            "Ginger and White=Red/Golden/Orange/Chestnut - with White\n" \
            "Golden=Tan/Yellow/Fawn\n" \
            "Grey=Gray/Blue/Silver/Salt & Pepper\n" \
            "Grey and White=Gray/Silver/Salt & Pepper - with White\n" \
            "Light Amber=Tan/Yellow/Fawn\n" \
            "Lilac=Gray/Blue/Silver/Salt & Pepper\n" \
            "Lilac Tortie=Tortoiseshell\n" \
            "Liver=Brown/Chocolate\n" \
            "Liver and White=Brown/Chocolate - with White\n" \
            "Red=Red/Golden/Orange/Chestnut\n" \
            "Ruddy=Red/Golden/Orange/Chestnut\n" \
            "Seal=Gray/Blue/Silver/Salt & Pepper\n" \
            "Silver=Gray/Blue/Silver/Salt & Pepper\n" \
            "Sorrel=Red/Golden/Orange/Chestnut\n" \
            "Sorrel Tortoiseshell=Tortoiseshell\n" \
            "Tabby=Brown Tabby\n" \
            "Tabby and White=Brown Tabby\n" \
            "Tan=Tan/Yellow/Fawn\n" \
            "Tan and Black=Tan/Yellow/Fawn - with Black\n" \
            "Tan and White=Tan/Yellow/Fawn - with White\n" \
            "Tortie=Tortoiseshell\n" \
            "Tortie and White=Tortoiseshell\n" \
            "Tricolour=Tricolor (Tan/Brown & Black & White)\n" \
            "Various=Tricolor (Tan/Brown & Black & White)\n" \
            "White and Black=White - with Black\n" \
            "White and Brindle=White - with Black\n" \
            "White and Brown=White - with Brown or Chocolate\n" \
            "White and Grey=White - with Gray or Silver\n" \
            "White and Liver=White - with Brown or Chocolate\n" \
            "White and Tabby=White\n" \
            "White and Tan=White - with Tan, Yellow or Fawn\n" \
            "White and Torti=White (Mostly)\n" \
            "#10:Description=Description\n" \
            "#11:Status=Status\n" \
            "#12:GoodWKids=GoodWKids\n" \
            "#13:GoodWCats=GoodWCats\n" \
            "#14:GoodWDogs=GoodWDogs\n" \
            "#15:SpayedNeutered=SpayedNeutered\n" \
            "#16:ShotsCurrent=ShotsCurrent\n" \
            "#17:Housetrained=Housetrained\n" \
            "#18:Declawed=Declawed\n" \
            "#19:SpecialNeeds=SpecialNeeds"
        return defmap

    def run(self):
        
        self.log("AdoptAPetPublisher starting...")

        if self.isPublisherExecuting(): return
        self.updatePublisherProgress(0)
        self.setLastError("")
        self.setStartPublishing()

        if not self.checkMappedSpecies():
            self.setLastError("Not all species have been mapped.")
            self.cleanup()
            return
        if not self.checkMappedBreeds():
            self.setLastError("Not all breeds have been mapped.")
            self.cleanup()
            return
        shelterid = configuration.adoptapet_user(self.dbo)
        if shelterid == "":
            self.setLastError("No AdoptAPet.com shelter id has been set.")
            self.cleanup()
            return
        animals = self.getMatchingAnimals()
        if len(animals) == 0:
            self.setLastError("No animals found to publish.")
            self.cleanup()
            return

        if not self.openFTPSocket(): 
            self.setLastError("Failed opening FTP socket.")
            self.cleanup()
            return

        # Do the images first
        self.mkdir("photos")
        self.chdir("photos")

        csv = []

        anCount = 0
        for an in animals:
            try:
                line = []
                anCount += 1
                self.log("Processing: %s: %s (%d of %d)" % ( an["SHELTERCODE"], an["ANIMALNAME"], anCount, len(animals)))
                self.updatePublisherProgress(self.getProgress(anCount, len(animals)))

                # If the user cancelled, stop now
                if self.shouldStopPublishing(): 
                    self.log("User cancelled publish. Stopping.")
                    self.resetPublisherProgress()
                    self.cleanup()
                    return

                # If a limit was set, stop now
                if self.pc.limit > 0 and anCount > self.pc.limit:
                    self.log("Hit publishing limit of %d animals. Stopping." % self.pc.limit)
                    break

                # Upload images for this animal
                self.uploadImages(an)
                # Id
                line.append("\"%s\"" % an["SHELTERCODE"])
                # Species
                line.append("\"%s\"" % an["PETFINDERSPECIES"])
                # Breed 1
                line.append("\"%s\"" % an["PETFINDERBREED"])
                # Breed 2 (only include if different from breed 1)
                # Breed 2 (blank if not crossbreed or unspecified crossbreed)
                if an["CROSSBREED"] == 1:
                    # If the second breed is one of our magic words, then don't
                    # send it.
                    b2 = an["BREEDNAME2"].lower()
                    if b2 == "mix" or b2 == "cross"  or b2 == "unknown" or b2 == "crossbreed":
                        line.append("\"\"")
                    else:
                        line.append("\"%s\"" % an["PETFINDERBREED2"])
                else:
                    line.append("\"\"")
                # Age, one of Adult, Baby, Senior and Young
                ageinyears = i18n.date_diff_days(an["DATEOFBIRTH"], i18n.now(self.dbo.timezone))
                ageinyears /= 365.0
                agename = "Adult"
                if ageinyears < 0.5: agename = "Baby"
                elif ageinyears < 2: agename = "Young"
                elif ageinyears < 9: agename = "Adult"
                else: agename = "Senior"
                line.append("\"%s\"" % agename)
                # Name
                line.append("\"%s\"" % an["ANIMALNAME"].replace("\"", "\"\""))
                # Size, one of S, M, L, XL
                ansize = "M"
                if an["SIZE"] == 0: ansize = "XL"
                elif an["SIZE"] == 1: ansize = "L"
                elif an["SIZE"] == 2: ansize = "M"
                elif an["SIZE"] == 3: ansize = "S"
                line.append("\"%s\"" % ansize)
                # Sex, one of M or F
                sexname = "M"
                if an["SEX"] == 0: sexname = "F"
                line.append("\"%s\"" % sexname)
                # Colour
                if self.pc.includeColours:
                    line.append("\"%s\"" % an["BASECOLOURNAME"])
                # Description
                line.append("\"%s\"" % self.getDescription(an))
                # Status, one of Available, Adopted or Delete
                line.append("\"Available\"")
                # Good with Kids
                line.append(self.apYesNoUnknown(an["ISGOODWITHCHILDREN"]))
                # Good with Cats
                line.append(self.apYesNoUnknown(an["ISGOODWITHCATS"]))
                # Good with Dogs
                line.append(self.apYesNoUnknown(an["ISGOODWITHDOGS"]))
                # Spayed/Neutered
                line.append(self.apYesNo(an["NEUTERED"] == 1))
                # Shots current
                line.append(self.apYesNo(medical.get_vaccinated(self.dbo, int(an["ID"]))))
                # Housetrained
                line.append(self.apYesNoUnknown(an["ISHOUSETRAINED"]))
                # Declawed
                line.append(self.apYesNo(an["DECLAWED"] == 1))
                # Special needs
                if an["CRUELTYCASE"] == 1:
                    line.append("\"1\"")
                elif an["HASSPECIALNEEDS"] == 1:
                    line.append("\"1\"")
                else:
                    line.append("\"\"")
                # Add to our CSV file
                csv.append(",".join(line))
            except Exception,err:
                self.logError("Failed processing animal: %s, %s" % (str(an["SHELTERCODE"]), err), sys.exc_info())

        # Mark published
        self.markAnimalsPublished("LastPublishedAP", animals)

        # Upload the datafiles
        mapfile = self.apMapFile(self.pc.includeColours)
        self.saveFile(os.path.join(self.publishDir, "import.cfg"), mapfile)
        self.saveFile(os.path.join(self.publishDir, "pets.csv"), "\n".join(csv))
        self.log("Saving datafile and map, %s %s" % ("pets.csv", "import.cfg"))
        self.chdir("..", "")
        self.log("Uploading pets.csv")
        self.upload("pets.csv")
        if not self.pc.noImportFile:
            self.log("Uploading import.cfg")
            self.upload("import.cfg")
        else:
            self.log("import.cfg upload is DISABLED")
        self.cleanup()

class RescueGroupsPublisher(FTPPublisher):
    """
    Handles publishing to PetAdoptionPortal.com/RescueGroups.org
    Note: RG only accept Active FTP connections
    """
    def __init__(self, dbo, publishCriteria):
        l = dbo.locale
        self.publisherName = i18n._("RescueGroups Publisher", l)
        self.setLogName("rescuegroups")
        publishCriteria.uploadDirectly = True
        publishCriteria.thumbnails = False
        publishCriteria.checkSocket = True
        publishCriteria.scaleImages = 1
        FTPPublisher.__init__(self, dbo, publishCriteria, 
            configuration.rescuegroups_host(dbo), configuration.rescuegroups_user(dbo), 
            configuration.rescuegroups_password(dbo), 21, "", False)

    def rgYesNo(self, condition):
        """
        Returns a CSV entry for yes or no based on the condition
        """
        if condition:
            return "\"Yes\""
        else:
            return "\"No\""

    def rgYesNoBlank(self, v):
        """
        Returns 0 == Yes, 1 == No, 2 == Empty string
        """
        if v == 0: return "Yes"
        elif v == 1: return "No"
        else: return ""

    def run(self):
        
        self.log("RescueGroupsPublisher starting...")

        if self.isPublisherExecuting(): return
        self.updatePublisherProgress(0)
        self.setLastError("")
        self.setStartPublishing()

        if not self.checkMappedSpecies():
            self.setLastError("Not all species have been mapped.")
            self.cleanup()
            return
        if not self.checkMappedBreeds():
            self.setLastError("Not all breeds have been mapped.")
            self.cleanup()
            return
        shelterid = configuration.rescuegroups_user(self.dbo)
        if shelterid == "":
            self.setLastError("No RescueGroups.org shelter id has been set.")
            self.cleanup()
            return
        animals = self.getMatchingAnimals()
        if len(animals) == 0:
            self.setLastError("No animals found to publish.")
            self.cleanup()
            return

        if not self.openFTPSocket(): 
            self.setLastError("Failed opening FTP socket.")
            self.cleanup()
            return

        # Do the images first
        self.mkdir("import")
        self.chdir("import")
        self.mkdir("pictures")
        self.chdir("pictures", "import/pictures")

        csv = []

        anCount = 0
        for an in animals:
            try:
                line = []
                anCount += 1
                self.log("Processing: %s: %s (%d of %d)" % ( an["SHELTERCODE"], an["ANIMALNAME"], anCount, len(animals)))
                self.updatePublisherProgress(self.getProgress(anCount, len(animals)))

                # If the user cancelled, stop now
                if self.shouldStopPublishing(): 
                    self.log("User cancelled publish. Stopping.")
                    self.resetPublisherProgress()
                    self.cleanup()
                    return

                # If a limit was set, stop now
                if self.pc.limit > 0 and anCount > self.pc.limit:
                    self.log("Hit publishing limit of %d animals. Stopping." % self.pc.limit)
                    break

                # Upload images for this animal
                totalimages = self.uploadImages(an, False, 4)
                # orgID
                line.append("\"%s\"" % shelterid)
                # ID
                line.append("\"%s\"" % str(an["ID"]))
                # Status
                line.append("\"Available\"")
                # Last updated (Unix timestamp)
                line.append("\"%s\"" % str(time.mktime(an["LASTCHANGEDDATE"].timetuple())))
                # rescue ID (ID of animal at the rescue)
                line.append("\"%s\"" % an["SHELTERCODE"])
                # Name
                line.append("\"%s\"" % an["ANIMALNAME"].replace("\"", "\"\""))
                # Summary (no idea what this is for)
                line.append("\"\"")
                # Species
                line.append("\"%s\"" % an["PETFINDERSPECIES"])
                # Readable breed
                line.append("\"%s\"" % an["BREEDNAME"])
                # Primary breed
                line.append("\"%s\"" % an["PETFINDERBREED"])
                # Secondary (blank if not crossbreed or unspecified crossbreed)
                if an["CROSSBREED"] == 1:
                    # If the second breed is one of our magic words, then don't
                    # send it.
                    b2 = an["BREEDNAME2"].lower()
                    if b2 == "mix" or b2 == "cross"  or b2 == "unknown" or b2 == "crossbreed":
                        line.append("\"\"")
                    else:
                        line.append("\"%s\"" % an["PETFINDERBREED2"])
                else:
                    line.append("\"\"")
                # Sex
                line.append("\"%s\"" % an["SEXNAME"])
                # Mixed
                line.append("\"%s\"" % self.rgYesNo(an["CROSSBREED"] == 1))
                # dogs (good with)
                line.append("\"%s\"" % self.rgYesNoBlank(an["ISGOODWITHDOGS"]))
                # cats (good with)
                line.append("\"%s\"" % self.rgYesNoBlank(an["ISGOODWITHCATS"]))
                # kids (good with)
                line.append("\"%s\"" % self.rgYesNoBlank(an["ISGOODWITHCHILDREN"]))
                # declawed
                line.append("\"%s\"" % self.rgYesNo(an["DECLAWED"] == 1))
                # housetrained
                line.append("\"%s\"" % self.rgYesNoBlank(an["ISHOUSETRAINED"]))
                # Age, one of Adult, Baby, Senior and Young
                ageinyears = i18n.date_diff_days(an["DATEOFBIRTH"], i18n.now(self.dbo.timezone))
                ageinyears /= 365.0
                agename = "Adult"
                if ageinyears < 0.5: agename = "Baby"
                elif ageinyears < 2: agename = "Young"
                elif ageinyears < 9: agename = "Adult"
                else: agename = "Senior"
                line.append("\"%s\"" % agename)
                # Special needs
                if an["CRUELTYCASE"] == 1:
                    line.append("\"1\"")
                elif an["HASSPECIALNEEDS"] == 1:
                    line.append("\"1\"")
                else:
                    line.append("\"\"")
                # Altered
                line.append("\"%s\"" % self.rgYesNo(an["NEUTERED"] == 1))
                # Size, one of S, M, L, XL
                ansize = "M"
                if an["SIZE"] == 0: ansize = "XL"
                elif an["SIZE"] == 1: ansize = "L"
                elif an["SIZE"] == 2: ansize = "M"
                elif an["SIZE"] == 3: ansize = "S"
                line.append("\"%s\"" % ansize)
                # uptodate (Has shots)
                line.append("\"%s\"" % self.rgYesNo(medical.get_vaccinated(self.dbo, int(an["ID"]))))
                # colour
                line.append("\"%s\"" % an["BASECOLOURNAME"])
                # coatLength (not implemented)
                line.append("\"\"")
                # pattern (not implemented)
                line.append("\"\"")
                # courtesy (what is this?)
                line.append("\"\"")
                # Description
                line.append("\"%s\"" % self.getDescription(an))
                # pic1-pic4
                if totalimages > 0:
                    # UploadAll isn't on, there was just one image with sheltercode == name
                    if not self.pc.uploadAllImages:
                        line.append("\"%s.jpg\",\"\",\"\",\"\"" % an["SHELTERCODE"])
                    else:
                        # Output an entry for each image we uploaded,
                        # upto a maximum of 4
                        for i in range(1, 5):
                            if totalimages >= i:
                                line.append("\"%s-%d.jpg\"" % (an["SHELTERCODE"], i))
                            else:
                                line.append("\"\"")
                else:
                    line.append("\"\",\"\",\"\",\"\"")
                # Add to our CSV file
                csv.append(",".join(line))
            except Exception,err:
                self.logError("Failed processing animal: %s, %s" % (str(an["SHELTERCODE"]), err), sys.exc_info())

        # Mark published
        self.markAnimalsPublished("LastPublishedRG", animals)

        header = "orgID, animalID, status, lastUpdated, rescueID, name, summary, species, breed, " \
            "primaryBreed, secondaryBreed, sex, mixed, dogs, cats, kids, declawed, housetrained, age, " \
            "specialNeeds, altered, size, uptodate, color, coatLength, pattern, courtesy, description, pic1, " \
            "pic2, pic3, pic4\n"
        self.saveFile(os.path.join(self.publishDir, "pets.csv"), header + "\n".join(csv))
        self.log("Uploading datafile %s" % "pets.csv")
        self.chdir("..", "import")
        self.upload("pets.csv")
        self.log("Uploaded %s" % "pets.csv")
        self.cleanup()

class SmartTagPublisher(FTPPublisher):
    """
    Handles publishing to SmartTag PETID
    """
    def __init__(self, dbo, publishCriteria):
        l = dbo.locale
        self.publisherName = i18n._("SmartTag Publisher", l)
        self.setLogName("smarttag")
        publishCriteria.uploadDirectly = True
        publishCriteria.thumbnails = False
        FTPPublisher.__init__(self, dbo, publishCriteria, 
            configuration.smarttag_host(dbo), configuration.smarttag_user(dbo), 
            configuration.smarttag_password(dbo))

    def stYesNo(self, condition):
        """
        Returns a CSV entry for yes or no based on the condition
        """
        if condition:
            return "\"Y\""
        else:
            return "\"N\""

    def run(self):
        
        if self.isPublisherExecuting(): return
        self.updatePublisherProgress(0)
        self.setLastError("")
        self.setStartPublishing()

        shelterid = configuration.smarttag_user(self.dbo)
        if shelterid == "":
            self.setLastError("No SmartTag shelter id has been set.")
            self.cleanup()
            return

        where = " WHERE SmartTag = 1 AND SmartTagNumber <> '' AND " \
                "(SmartTagSentDate Is Null OR SmartTagSentDate < ActiveMovementDate) AND " \
                "ActiveMovementID > 0"
        animals = db.query(self.dbo, animal.get_animal_query() + where)
        if len(animals) == 0:
            self.setLastError("No animals found to publish.")
            self.cleanup()
            return

        if not self.openFTPSocket(): 
            self.setLastError("Failed to open FTP socket.")
            self.cleanup()
            return

        # SmartTag want data files called shelterid_mmddyyyy_HHMMSS.csv in a folder
        # called shelterid_mmddyyyy_HHMMSS
        dateportion = i18n.format_date("%m%d%Y_%H%M%S", i18n.now(self.dbo.timezone))
        folder = "%s_%s" % (shelterid, dateportion)
        outputfile = "%s_%s.csv" % (shelterid, dateportion)
        self.mkdir(folder)
        self.chdir(folder)

        csv = []

        anCount = 0
        for an in animals:
            try:
                line = []
                anCount += 1
                self.log("Processing: %s: %s (%d of %d)" % ( an["SHELTERCODE"], an["ANIMALNAME"], anCount, len(animals)))
                self.updatePublisherProgress(self.getProgress(anCount, len(animals)))

                # If the user cancelled, stop now
                if self.shouldStopPublishing(): 
                    self.log("User cancelled publish. Stopping.")
                    self.resetPublisherProgress()
                    self.cleanup()
                    return

                # Upload one image for this animal with the name shelterid_animalid-1.jpg
                self.uploadImage(an, an["WEBSITEMEDIANAME"], "%s_%d-1.jpg" % (shelterid, an["ID"]))
                # accountid
                line.append("\"%s\"" % shelterid)
                # sourcesystem
                line.append("\"ASM\"")
                # sourcesystemanimalkey (corresponds to image name)
                line.append("\"%d\"" % an["ID"])
                # sourcesystemidkey
                line.append("\"%d\"" % an["ID"])
                # sourcesystemownerkey
                line.append("\"%s\"" % str(an["CURRENTOWNERID"]))
                # signupidassigned
                line.append("\"%s\"" % an["SMARTTAGNUMBER"])
                # signuptype
                sttype = "IDTAG-ANNUAL"
                if an["SMARTTAGTYPE"] == 1: sttype = "IDTAG-5 YEAR"
                if an["SMARTTAGTYPE"] == 2: sttype = "IDTAG-LIFETIME"
                line.append("\"%s\"" % sttype)
                # signupeffectivedate
                line.append("\"" + i18n.python2display(self.locale, an["SMARTTAGDATE"]) + "\"")
                # signupbatchpostdt - only used by resending mechanism and we don't do that
                line.append("\"\"")
                # feecharged
                line.append("\"\"")
                # feecollected
                line.append("\"\"")
                # owner related stuff
                address = an["CURRENTOWNERADDRESS"]
                firstline = address
                if firstline.find("\n") != -1: firstline = address[0:address.find("\n")]
                street = firstline.split(" ")
                houseno = ""
                streetname = firstline
                if len(street) > 1:
                    houseno = street[0]
                    streetname = firstline[firstline.find(" ")+1:]
                # ownerfname
                line.append("\"%s\"" % an["CURRENTOWNERFORENAMES"])
                # ownermname
                line.append("\"\"")
                #ownerlname
                line.append("\"%s\"" % an["CURRENTOWNERSURNAME"])
                # addressstreetnumber
                line.append("\"%s\"" % houseno)
                # addressstreetdir
                line.append("\"\"")
                # addressstreetname
                line.append("\"%s\"" % streetname)
                # addressstreettype
                line.append("\"\"")
                # addresscity
                line.append("\"%s\"" % an["CURRENTOWNERTOWN"])
                # addressstate
                line.append("\"%s\"" % an["CURRENTOWNERCOUNTY"])
                # addresspostal
                line.append("\"%s\"" % an["CURRENTOWNERPOSTCODE"])
                # addressctry
                line.append("\"USA\"")
                # owneremail
                line.append("\"%s\"" % an["CURRENTOWNEREMAILADDRESS"])
                # owneremail2
                line.append("\"\"")
                # owneremail3
                line.append("\"\"")
                # ownerhomephone
                line.append("\"%s\"" % an["CURRENTOWNERHOMETELEPHONE"])
                # ownerworkphone
                line.append("\"%s\"" % an["CURRENTOWNERWORKTELEPHONE"])
                # ownerthirdphone
                line.append("\"%s\"" % an["CURRENTOWNERMOBILETELEPHONE"])
                # petname
                line.append("\"%s\"" % an["ANIMALNAME"].replace("\"", "\"\""))
                # species
                line.append("\"%s\"" % an["SPECIESNAME"])
                # primarybreed
                line.append("\"%s\"" % an["BREEDNAME1"])
                # crossbreed (second breed)
                if an["CROSSBREED"] == 1:
                    line.append("\"%s\"" % an["BREEDNAME2"])
                else:
                    line.append("\"\"")
                # purebred
                line.append("\"%s\"" % self.stYesNo(an["CROSSBREED"] == 0))
                # gender
                line.append("\"%s\"" % an["SEXNAME"])
                # sterilized
                line.append("\"%s\"" % self.stYesNo(an["NEUTERED"] == 1))
                # primarycolor
                line.append("\"%s\"" % an["BASECOLOURNAME"])
                # secondcolor
                line.append("\"\"")
                # sizecategory
                line.append("\"%s\"" % an["SIZENAME"])
                # agecategory
                line.append("\"%s\"" % an["AGEGROUP"])
                # declawed
                line.append("\"%s\"" % self.stYesNo(an["DECLAWED"] == 1))
                # animalstatus (blank or D for Deceased)
                if an["DECEASEDDATE"] is not None:
                    line.append("\"D\"")
                else:
                    line.append("\"\"")
                # Add to our CSV file
                csv.append(",".join(line))
            except Exception,err:
                self.logError("Failed processing animal: %s, %s" % (str(an["SHELTERCODE"]), err), sys.exc_info())

        # Mark published
        db.execute(self.dbo, "UPDATE animal SET SmartTagSentDate = %s WHERE ID IN (%s)" % (
            db.dd(i18n.now(self.dbo.timezone)), self.getAnimalInClause(animals)))

        header = "accountid,sourcesystem,sourcesystemidkey,sourcesystemanimalkey," \
            "sourcesystemownerkey,signupidassigned,signuptype,signupeffectivedate," \
            "signupbatchpostdt,feecharged,feecollected,ownerfname,ownermname," \
            "ownerlname,addressstreetnumber,addressstreetdir,addressstreetname," \
            "addressstreettype,addresscity,addressstate,addresspostal,addressctry," \
            "owneremail,owneremail2,owneremail3,ownerhomephone,ownerworkphone," \
            "ownerthirdphone,petname,species,primarybreed,crossbreed,purebred,gender," \
            "sterilized,primarycolor,secondcolor,sizecategory,agecategory,declawed," \
            "animalstatus\n" 
        self.saveFile(os.path.join(self.publishDir, outputfile), header + "\n".join(csv))
        self.log("Uploading datafile %s" % outputfile)
        self.upload(outputfile)
        self.log("Uploaded %s" % outputfile)
        self.cleanup()

class MeetAPetPublisher(AbstractPublisher):
    """
    Handles publishing to MeetAPet.com
    """
    def __init__(self, dbo, publishCriteria):
        l = dbo.locale
        AbstractPublisher.__init__(self, dbo, publishCriteria)
        self.publisherName = i18n._("MeetAPet Publisher", l)
        self.setLogName("meetapet")
        publishCriteria.uploadDirectly = True
        publishCriteria.thumbnails = False

    def mpYesNo(self, condition):
        """
        Returns yes or no for a condition.
        """
        if condition:
            return "yes"
        else:
            return "no"

    def mpYesNoBlank(self, v):
        """
        Returns 0 == Yes, 1 == No, 2 == Empty string
        """
        if v == 0: return "yes"
        elif v == 1: return "no"
        else: return ""

    def mpAverageWeight(self, species, breed):
        """
        Returns an average weight in pounds (as a string) for some
        known species.
        """
        weights = (
            ( "dog", "chihuah", "5" ),
            ( "dog", "pekingese", "7" ),
            ( "dog", "labrador", "65" ),
            ( "dog", "cocker", "25" ),
            ( "dog", "springer", "25" ),
            ( "dog", "shepherd", "75" ),
            ( "dog", "yorkshire", "7" ),
            ( "dog", "terrier", "15" ),
            ( "dog", "mastiff", "150" ),
            ( "dog", "retriever", "65" ),
            ( "dog", "beagle", "20" ),
            ( "dog", "boxer", "50" ),
            ( "dog", "bulldog", "40" ),
            ( "dog", "dachshund", "8" ),
            ( "dog", "poodle", "13" ),
            ( "dog", "shih", "10" ),
            ( "cat", "dom", "9" ),
            ( "cat", "siamese", "7" ),
            ( "cat", "maine", "15" )
        )
        species = str(species).lower()
        breed = str(breed).lower()
        for ws, wb, ww in weights:
            if species.find(ws) != -1 and breed.find(wb) != -1:
                return ww
        if species.find("dog") != -1:
            return "20"
        elif species.find("cat") != -1:
            return "9"
        else:
            return "0"

    def run(self):
        
        self.log("MeetAPetPublisher starting...")

        if self.isPublisherExecuting(): return
        self.updatePublisherProgress(0)
        self.setLastError("")
        self.setStartPublishing()

        key = configuration.meetapet_key(self.dbo)
        secret = configuration.meetapet_secret(self.dbo)
        userkey = configuration.meetapet_userkey(self.dbo)
        baseurl = configuration.meetapet_baseurl(self.dbo)

        # Organisation prefix used to make pet urls unique
        org = configuration.organisation(self.dbo)
        org = org.replace(" ", "").replace("'", "_").lower() + "_"
        if len(org) > 10: org = org[0:10] 
       
        CREATE_URL = baseurl + "pet_create"
        UPDATE_URL = baseurl + "pet_update"
        DELETE_URL = baseurl + "pet_delete"

        if key == "" or secret == "" or userkey == "" or baseurl == "":
            self.setLastError("baseurl, key, secret and userkey all need to be set for meetapet.com publisher")
            return

        animals = self.getMatchingAnimals()
        if len(animals) == 0:
            self.setLastError("No animals found to publish.")
            return

        anCount = 0
        publishedInClause = ""
        for an in animals:
            try:
                anCount += 1
                self.log("Processing: %s: %s (%d of %d)" % ( an["SHELTERCODE"], an["ANIMALNAME"], anCount, len(animals)))
                self.updatePublisherProgress(self.getProgress(anCount, len(animals)))

                # If the user cancelled, stop now
                if self.shouldStopPublishing(): 
                    self.log("User cancelled publish. Stopping.")
                    self.resetPublisherProgress()
                    return

                # If a limit was set, stop now
                if self.pc.limit > 0 and anCount > self.pc.limit:
                    self.log("Hit publishing limit of %d animals. Stopping." % self.pc.limit)
                    break

                # Grab the media record
                mr = db.query(self.dbo, "SELECT * FROM media WHERE MediaName = '%s'" % an["WEBSITEMEDIANAME"])

                # Keep a running list of IDs for animals we've published as an IN clause
                if publishedInClause != "":
                    publishedInClause += ","
                publishedInClause += str(an["ID"])

                # Sort out the pet bio
                notes = self.getDescription(an)

                # Sort out size
                ansize = "m"
                if an["SIZE"] == 0: ansize = "xl"
                elif an["SIZE"] == 1: ansize = "l"
                elif an["SIZE"] == 2: ansize = "m"
                elif an["SIZE"] == 3: ansize = "s"

                # Gender
                gender = "m"
                if an["SEX"] == 0: gender = "f"

                # Has shots
                shots = self.mpYesNo(medical.get_vaccinated(self.dbo, int(an["ID"])))

                # Build the animal POST data
                fields = (
                    ("key", key),
                    ("secret", secret), 
                    ("shelter_key", userkey),
                    ("pet_display", "yes"),
                    ("pet_available", "yes"),
                    ("pet_name", an["ANIMALNAME"]),
                    ("pet_url", org + str(an["SHELTERCODE"])),
                    ("pet_type", an["SPECIESNAME"]),
                    ("pet_breed", an["BREEDNAME1"]),
                    ("pet_breed2", an["BREEDNAME2"]),
                    ("pet_size", ansize),
                    ("pet_weight", self.mpAverageWeight(an["SPECIESNAME"], an["BREEDNAME"])),
                    ("pet_gender", gender),
                    ("pet_birthdate", i18n.format_date("%Y-%m-%d", an["DATEOFBIRTH"])),
                    ("pet_bio", notes),
                    ("pet_neutered", self.mpYesNoBlank(an["NEUTERED"])),
                    ("pet_shots", shots),
                    ("pet_special_needs", self.mpYesNoBlank(an["HASSPECIALNEEDS"]))
                )

                files = (
                    ( "pet_image", an["WEBSITEMEDIANAME"], dbfs.get_string(self.dbo, an["WEBSITEMEDIANAME"])),
                )

                # Do we need to create or update this record? We create if the last published
                # date is blank.
                if len(mr) > 0 and mr[0]["LASTPUBLISHEDMP"] is None:
                    self.log("Using HTTP CREATE %s... %s" % (CREATE_URL, str(fields)))
                    req, hdr, rv = utils.post_multipart(CREATE_URL, fields, files)
                    self.log("response: %s %s" % (str(hdr), rv))
                    if rv.find("success") != -1:
                        self.markAnimalPublished("LastPublishedMP", int(an["ID"]))
                    else:
                        self.log("Found errors, not marking as published.")
                else:
                    self.log("Using HTTP UPDATE %s ... %s" % (UPDATE_URL, str(fields)))
                    req, hdr, rv = utils.post_multipart(UPDATE_URL, fields, files)
                    self.log("response: %s %s" % (str(hdr), rv))

            except Exception,err:
                self.logError("Failed processing animal: %s, %s" % (str(an["SHELTERCODE"]), err), sys.exc_info())

        # Now, have a look back through our animals for anything we've already sent to
        # meetapet.com that's left the shelter so it can be deleted. We find anything
        # that has a non-null LastPublishedMP date that isn't in our current set
        try:
            toremove = db.query(self.dbo, "SELECT a.ID, a.AnimalName, a.ShelterCode FROM animal a INNER JOIN media m ON m.LinkID = a.ID " \
                "WHERE m.LinkTypeID = 0 AND m.LastPublishedMP Is Not Null AND m.WebsitePhoto = 1 AND " \
                "a.ID NOT IN (%s)" % publishedInClause)
            self.log("Found %d previously published animals to remove." % len(toremove))
            for an in toremove:
                fields = {
                    "key": key,
                    "secret": secret,
                    "shelter_key": userkey,
                    "pet_url": an["SHELTERCODE"]
                }
                self.log("Removing %s - %s via HTTP DELETE... %s" % (org + an["SHELTERCODE"], an["ANIMALNAME"], str(fields)))
                headers, rv = utils.post_form(DELETE_URL, fields)
                self.log("response: " + rv)
                if rv.find("success") != -1:
                    self.markAnimalPublished("LastPublishedMP", int(an["ID"]), True)
                else:
                    self.log("Found errors, not marking unpublished.")
        except Exception,err:
            self.logError("Failed removing adopted animals: %s" % err, sys.exc_info())

        self.saveLog()
        self.setPublisherComplete()

class PetLinkPublisher(AbstractPublisher):
    """
    Handles publishing of updated microchip info to PetLink.net
    """
    def __init__(self, dbo, publishCriteria):
        l = dbo.locale
        AbstractPublisher.__init__(self, dbo, publishCriteria)
        self.publisherName = i18n._("PetLink Publisher", l)
        self.setLogName("petlink")
        publishCriteria.uploadDirectly = True
        publishCriteria.thumbnails = False

    def plYesNo(self, condition):
        """
        Returns yes or no for a condition.
        """
        if condition:
            return "y"
        else:
            return "n"

    def plBreed(self, breedname, speciesname, iscross):
        """
        Returns a PetLink breed of either the breed name,
        "Mixed Breed" if iscross == 1 or "Other" if the species
        is not Cat or Dog.
        """
        if speciesname.lower().find("cat") != -1 and speciesname.lower().find("dog") != -1:
            return "Other"
        if iscross == 1:
            return "Mixed Breed"
        return breedname

    def run(self):
        
        self.log("PetLinkPublisher starting...")

        if self.isPublisherExecuting(): return
        self.updatePublisherProgress(0)
        self.setLastError("")
        self.setStartPublishing()

        email = configuration.petlink_email(self.dbo)
        password = configuration.petlink_password(self.dbo)
        chippass = configuration.petlink_chippassword(self.dbo)
        baseurl = configuration.petlink_baseurl(self.dbo)

        if email == "" or password == "":
            self.setLastError("No PetLink login has been set.")
            return

        if chippass == "" or baseurl == "":
            self.setLastError("baseurl and chippass need to be set for petlink.com publisher")
            return

        where = " WHERE (IdentichipNumber Like '98102%') AND " \
                "ActiveMovementID > 0 AND ActiveMovementType = 1 AND " \
                "(CurrentOwnerEmailAddress <> '' OR CurrentOwnerHomeTelephone <> '') AND " \
                "(PetLinkSentDate Is Null OR PetLinkSentDate < ActiveMovementDate) "
        animals = db.query(self.dbo, animal.get_animal_query() + where)
        if len(animals) == 0:
            self.setLastError("No animals found to publish.")
            return

        LOGIN_URL = baseurl + "j_acegi_security_check"
        UPLOAD_URL = baseurl + "animalprofessional/massImportUpload.spring"

        # Login via HTTP
        fields = {
            "j_username": email,
            "j_password": password
        }
        try:
            self.log("Getting PetLink homepage...")
            headers, rv = utils.get_url(baseurl)
            cookie = ""
            for h in headers:
                if h.find("Cookie") != -1 and h.find("JSESSION") != -1:
                    cookie = h
            self.log("Homepage returned headers: " + str(headers))
            if cookie == "":
                self.setLastError("Login failed (no auth cookie).")
                return
            cookie = cookie[cookie.find(":")+1:cookie.find(";")].strip()
            self.log("Found session cookie: " + cookie)
            self.log("Logging in to PetLink.net... ")
            cookieheaders = {"Cookie" : cookie }
            headers, rv = utils.post_form(LOGIN_URL, fields, cookieheaders)
            self.log("response: headers=%s, body=%s" % (str(headers), str(rv)))
            if str(rv).find("Hello") == -1:
                self.setLastError("Login failed (no Hello found).")
                return
        except Exception,err:
            self.logError("Failed logging in: %s" % err, sys.exc_info())
            self.setLastError("Login failed (error during HTTP request).")
            return

        anCount = 0
        csv = []
        processed_ids = []
        csv.append("TransactionType,MicrochipID,FirstName,LastName,Address,City,State,ZipCode,Country," \
            "Phone1,Phone2,Phone3,Email,Password,Date_of_Implant,PetName,Species,Breed,Gender," \
            "Spayed_Neutered,ColorMarkings")
        for an in animals:
            try:
                line = []
                anCount += 1
                self.log("Processing: %s: %s (%d of %d) - %s" % ( an["SHELTERCODE"], an["ANIMALNAME"], anCount, len(animals), an["IDENTICHIPNUMBER"]))
                self.updatePublisherProgress(self.getProgress(anCount, len(animals)))

                # If the user cancelled, stop now
                if self.shouldStopPublishing(): 
                    self.log("User cancelled publish. Stopping.")
                    self.resetPublisherProgress()
                    return

                # If the microchip number isn't 15 digits, skip it
                if len(an["IDENTICHIPNUMBER"].strip()) != 15:
                    self.log("Chip number failed validation (%s not 15 digits), skipping." % an["IDENTICHIPNUMBER"])
                    continue

                # If we don't have an email address, use the owner's
                # phone number @petlink.tmp
                email = an["CURRENTOWNEREMAILADDRESS"]
                if email.strip() == "":
                    email = "".join(c for c in an["CURRENTOWNERHOMETELEPHONE"] if c.isdigit())
                    email = email + "@petlink.tmp"
                # TransactionType
                line.append("\"%s\"" % ( an["PETLINKSENTDATE"] is None and "N" or "T" ))
                # MicrochipID
                line.append("\"%s\"" % ( an["IDENTICHIPNUMBER"] ))
                # FirstName
                line.append("\"%s\"" % ( an["CURRENTOWNERFORENAMES"] ))
                # LastName
                line.append("\"%s\"" % ( an["CURRENTOWNERSURNAME"] ))
                # Address
                line.append("\"%s\"" % ( an["CURRENTOWNERADDRESS"] ))
                # City
                line.append("\"%s\"" % ( an["CURRENTOWNERTOWN"] ))
                # State
                line.append("\"%s\"" % ( an["CURRENTOWNERCOUNTY"] ))
                # ZipCode
                line.append("\"%s\"" % ( an["CURRENTOWNERPOSTCODE"] ))
                # Country
                line.append("\"USA\"")
                # Phone1
                line.append("\"%s\"" % ( an["CURRENTOWNERHOMETELEPHONE"] ))
                # Phone2
                line.append("\"%s\"" % ( an["CURRENTOWNERWORKTELEPHONE"] ))
                # Phone3
                line.append("\"%s\"" % ( an["CURRENTOWNERMOBILETELEPHONE"] ))
                # Email (mandatory)
                line.append("\"%s\"" % ( email ))
                # Password (config item, unique to each shelter)
                line.append("\"%s\"" % chippass)
                # Date_of_Implant (yy-mm-dd)
                line.append("\"%s\"" % i18n.format_date("%y-%m-%d", an["IDENTICHIPDATE"]))
                # PetName
                line.append("\"%s\"" % an["ANIMALNAME"])
                # Species
                line.append("\"%s\"" % an["SPECIESNAME"])
                # Breed (or "Mixed Breed" for crossbreeds, Other for animals not cats and dogs)
                line.append("\"%s\"" % self.plBreed(an["BREEDNAME1"], an["SPECIESNAME"], an["CROSSBREED"]))
                # Gender
                line.append("\"%s\"" % an["SEXNAME"])
                # Spayed_Neutered (y or n)
                line.append("\"%s\"" % self.plYesNo(an["NEUTERED"]))
                # ColorMarkings (our BaseColour field)
                line.append("\"%s\"" % an["BASECOLOURNAME"])
                # Add to our data file.  
                csv.append(",".join(line))
                # Remember we included this one
                processed_ids.append(str(an["ID"]))
            except Exception,err:
                self.logError("Failed processing animal: %s, %s" % (str(an["SHELTERCODE"]), err), sys.exc_info())

        # POST the csv file
        fields = ()
        csvblob = "\n".join(csv)
        files = (
            ( "file", "import.csv", csvblob),
        )
        self.log("Uploading data file to %s..." % (UPLOAD_URL))
        try:
            req, hdr, response = utils.post_multipart(UPLOAD_URL, fields, files, cookieheaders, "form-data")
            self.log("req hdr: %s, \nreq data: %s, \nresponse hdr: %s, \nresponse: %s" % (str(req.header_items()), str(req.get_data()), str(hdr), str(response)))
            if str(response).find("Upload Completed") != -1:
                # Mark published
                self.log("got successful response, marking animals as sent to petlink today")
                db.execute(self.dbo, "UPDATE animal SET PetLinkSentDate = %s WHERE ID IN (%s)" % (
                    db.dd(i18n.now(self.dbo.timezone)), ",".join(processed_ids)))
            else:
                self.log("didn't find successful response, abandoning.")
        except Exception,err:
            self.logError("Failed uploading data file: %s" % err)

        self.saveLog()
        self.setPublisherComplete()

class HelpingLostPetsPublisher(FTPPublisher):
    """
    Handles publishing to helpinglostpets.com
    """
    def __init__(self, dbo, publishCriteria):
        l = dbo.locale
        publishCriteria.uploadDirectly = True
        publishCriteria.thumbnails = False
        publishCriteria.checkSocket = True
        publishCriteria.scaleImages = 1
        self.publisherName = i18n._("HelpingLostPets Publisher", l)
        self.setLogName("helpinglostpets")
        FTPPublisher.__init__(self, dbo, publishCriteria, 
            configuration.helpinglostpets_host(dbo), configuration.helpinglostpets_user(dbo), 
            configuration.helpinglostpets_password(dbo))

    def hlpYesNo(self, condition):
        """
        Returns a CSV entry for yes or no based on the condition
        """
        if condition:
            return "\"Yes\""
        else:
            return "\"No\""

    def run(self):
        
        if self.isPublisherExecuting(): return
        self.updatePublisherProgress(0)
        self.setLastError("")
        self.setStartPublishing()

        shelterid = configuration.helpinglostpets_orgid(self.dbo)
        if shelterid == "":
            self.setLastError("No helpinglostpets.com organisation ID has been set.")
            return
        foundanimals = lostfound.get_foundanimal_find_simple(self.dbo)
        animals = self.getMatchingAnimals()
        if len(animals) == 0 and len(foundanimals) == 0:
            self.setLastError("No animals found to publish.")
            return

        if not self.openFTPSocket(): 
            self.setLastError("Failed opening FTP socket.")
            return

        csv = []

        # Found Animals
        anCount = 0
        for an in foundanimals:
            try:
                line = []
                anCount += 1
                self.log("Processing Found Animal: %d: %s (%d of %d)" % ( an["ID"], an["COMMENTS"], anCount, len(foundanimals)))

                # If the user cancelled, stop now
                if self.shouldStopPublishing(): 
                    self.log("User cancelled publish. Stopping.")
                    self.resetPublisherProgress()
                    return

                # If a limit was set, stop now
                if self.pc.limit > 0 and anCount > self.pc.limit:
                    self.log("Hit publishing limit of %d animals. Stopping." % self.pc.limit)
                    break

                # OrgID
                line.append("\"%s\"" % shelterid)
                # PetID
                line.append("\"F%d\"" % an["ID"])
                # Status
                line.append("\"Found\"")
                # Name
                line.append("\"%d\"" % an["ID"])
                # Species
                line.append("\"%s\"" % an["SPECIESNAME"])
                # Sex
                line.append("\"%s\"" % an["SEXNAME"])
                # PrimaryBreed
                line.append("\"%s\"" % an["BREEDNAME"])
                # SecondaryBreed
                line.append("\"\"")
                # Age, one of Baby, Young, Adult, Senior - just happens to match our default age groups
                line.append("\"%s\"" % an["AGEGROUP"])
                # Altered - don't have
                line.append("\"\"")
                # Size, one of Small, Medium or Large or X-Large - also don't have
                line.append("\"\"")
                # ZipPostal
                line.append("\"%s\"" % an["AREAPOSTCODE"])
                # Description
                notes = str(an["DISTFEAT"]) + "\n" + str(an["COMMENTS"]) + "\n" + str(an["AREAFOUND"])
                # Strip carriage returns
                notes = notes.replace("\r\n", "<br />")
                notes = notes.replace("\r", "<br />")
                notes = notes.replace("\n", "<br />")
                notes = notes.replace("\"", "&ldquo;")
                notes = notes.replace("\'", "&lsquo;")
                notes = notes.replace("\`", "&lsquo;")
                line.append("\"%s\"" % notes)
                # Photo
                line.append("\"\"")
                # Colour
                line.append("\"%s\"" % an["BASECOLOURNAME"])
                # MedicalConditions
                line.append("\"\"")
                # LastUpdated
                line.append("\"%s\"" % i18n.python2unix(an["LASTCHANGEDDATE"]))
                # Add to our CSV file
                csv.append(",".join(line))
            except Exception,err:
                self.logError("Failed processing found animal: %s, %s" % (str(an["ID"]), err), sys.exc_info())

        # Animals
        anCount = 0
        for an in animals:
            try:
                line = []
                anCount += 1
                self.log("Processing: %s: %s (%d of %d)" % ( an["SHELTERCODE"], an["ANIMALNAME"], anCount, len(animals)))
                self.updatePublisherProgress(self.getProgress(anCount, len(animals)))

                # If the user cancelled, stop now
                if self.shouldStopPublishing(): 
                    self.log("User cancelled publish. Stopping.")
                    self.resetPublisherProgress()
                    return

                # If a limit was set, stop now
                if self.pc.limit > 0 and anCount > self.pc.limit:
                    self.log("Hit publishing limit of %d animals. Stopping." % self.pc.limit)
                    break

                # Upload one image for this animal
                self.uploadImage(an, an["WEBSITEMEDIANAME"], an["SHELTERCODE"] + ".jpg")
                # OrgID
                line.append("\"%s\"" % shelterid)
                # PetID
                line.append("\"A%d\"" % an["ID"])
                # Status
                line.append("\"Adoptable\"")
                # Name
                line.append("\"%s\"" % an["ANIMALNAME"])
                # Species
                line.append("\"%s\"" % an["SPECIESNAME"])
                # Sex
                line.append("\"%s\"" % an["SEXNAME"])
                # PrimaryBreed
                line.append("\"%s\"" % an["BREEDNAME1"])
                # SecondaryBreed
                if an["CROSSBREED"] == 1:
                    line.append("\"%s\"" % an["BREEDNAME2"])
                else:
                    line.append("\"\"")
                # Age, one of Baby, Young, Adult, Senior
                ageinyears = i18n.date_diff_days(an["DATEOFBIRTH"], i18n.now(self.dbo.timezone))
                ageinyears /= 365.0
                agename = "Adult"
                if ageinyears < 0.5: agename = "Baby"
                elif ageinyears < 2: agename = "Young"
                elif ageinyears < 9: agename = "Adult"
                else: agename = "Senior"
                line.append("\"%s\"" % agename)
                # Altered
                line.append("\"%s\"" % self.hlpYesNo(an["NEUTERED"] == 1))
                # Size, one of Small, Medium or Large or X-Large
                ansize = "Medium"
                if an["SIZE"] == 0 : ansize = "X-Large"
                elif an["SIZE"] == 1: ansize = "Large"
                elif an["SIZE"] == 2: ansize = "Medium"
                elif an["SIZE"] == 3: ansize = "Small"
                line.append("\"%s\"" % ansize)
                # ZipPostal
                line.append("\"%s\"" % configuration.helpinglostpets_postal(self.dbo))
                # Description
                line.append("\"%s\"" % self.getDescription(an, True))
                # Photo
                line.append("\"%s.jpg\"" % an["SHELTERCODE"])
                # Colour
                line.append("\"%s\"" % an["BASECOLOURNAME"])
                # MedicalConditions
                line.append("\"%s\"" % an["HEALTHPROBLEMS"])
                # LastUpdated
                line.append("\"%s\"" % i18n.python2unix(an["LASTCHANGEDDATE"]))
                # Add to our CSV file
                csv.append(",".join(line))
            except Exception,err:
                self.logError("Failed processing animal: %s, %s" % (str(an["SHELTERCODE"]), err), sys.exc_info())

        # Mark published
        self.markAnimalsPublished("LastPublishedHLP", animals)

        header = "OrgID, PetID, Status, Name, Species, Sex, PrimaryBreed, SecondaryBreed, Age, Altered, Size, ZipPostal, Description, Photo, Colour, MedicalConditions, LastUpdated\n"
        filename = shelterid + ".txt"
        self.saveFile(os.path.join(self.publishDir, filename), header + "\n".join(csv))
        self.log("Uploading datafile %s" % filename)
        self.upload(filename)
        self.log("Uploaded %s" % filename)
        # Clean up
        self.closeFTPSocket()
        self.deletePublishDirectory()
        self.saveLog()
        self.setPublisherComplete()

if __name__ == "__main__":
    pc = PublishCriteria()
    pc.publishDirectory = "/home/robin/.asm/publish"
    pc.clearExisting = True
    pc.htmlByChildAdult = True
    pc.htmlBySpecies = True
    h = HTMLPublisher(db.DatabaseInfo(), pc, "test")
    h.execute("test")

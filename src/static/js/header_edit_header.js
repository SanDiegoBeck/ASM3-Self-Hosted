/*jslint browser: true, forin: true, eqeq: true, white: true, sloppy: true, vars: true, nomen: true */
/*global $, _, asm, common, config, format, header, html */
/*global edit_header: true */

$(function() {

    // If this is the login or database create page, don't do anything - they don't have headers, 
    // but for the sake of making life easy, they still include this file.
    if (common.current_url().indexOf("/login") != -1 ||
        common.current_url().indexOf("/database") != -1) {
        return;
    }

    // The edit header object deals with the banners at the top of the animal,
    // person, waiting list and lost/found edit pages..
    // it also has functions for person flags
    edit_header = {

        /**
         * Renders the header for any of the animal edit pages, with thumbnail image,
         * info and tabs. The caller will need to add a div to close out this header.
         * a: The animal row from the json
         * selected: The name of the selected tab (animal, vaccination, medical, diet, costs,
         *           donations, media, diary, movements, log)
         * counts:   A count of the number of records for each tab (in uppercase). If it's
         *           non-zero, an icon is shown on some tabs.
         */
        animal_edit_header: function(a, selected, counts) {
            var check_display_icon = function(key, iconname) {
                if (key == "animal") { return html.icon("blank"); }
                if (counts[key.toUpperCase()] > 0) {
                    return html.icon(iconname);
                }
                return html.icon("blank");
            };
            var mediaprompt = "";
            if (a.WEBSITEMEDIANAME == null) {
                mediaprompt = '<br /><span style="white-space: nowrap"><a href="animal_media?id=' + a.ID + '&newmedia=1">[ ' + _("Add a photo") + ' ]</a></span>';
            }
            var currentowner = "";
            if (a.CURRENTOWNERID != null) {
                currentowner = " <a href=\"person?id=" + a.CURRENTOWNERID + "\">" + a.CURRENTOWNERNAME + "</a>";
            }
            var available = "";
            if (a.ARCHIVED == 0) {
                available = "<span class=\"asm-search-notforadoption\">" + _("Not available for adoption") + "</span>";
            }
            if (a.ARCHIVED == 0 && a.HASPERMANENTFOSTER == 1) {
                available = "<span class=\"asm-search-notforadoption\">" + _("Permanent Foster") + "</span>";
            }
            if (a.ARCHIVED == 0 && a.ISNOTAVAILABLEFORADOPTION == 0 && a.HASTRIALADOPTION == 0 && !a.HASPERMANENTFOSTER) {
                available = "<span class=\"asm-search-available\">" + _("Available for adoption") + "</span>";
            }
            if (a.ARCHIVED == 0 && a.HASACTIVERESERVE == 1) {
                available = "<span class=\"asm-search-reserved\">" + _("Reserved") + " "  + html.icon("right") + " ";
                available += "<a href=\"person?id=" + a.RESERVEDOWNERID + "\">" + a.RESERVEDOWNERNAME + "</span>";
            }
            if (a.ISHOLD == 1 && !a.HOLDUNTILDATE) {
                available = "<span class=\"asm-search-hold\">" + _("Hold") + "</span>";
            }
            if (a.ISHOLD == 1 && a.HOLDUNTILDATE) {
                available = "<span class=\"asm-search-hold\">" + _("Hold until {0}").replace("{0}", format.date(a.HOLDUNTILDATE))  + "</span>";
            }
            if (a.ISQUARANTINE == 1) {
                available = "<span class=\"asm-search-quarantine\">" + _("Quarantine") + "</span>";
            }
            if (a.CRUELTYCASE == 1) {
                available = "<span class=\"asm-search-cruelty\">" + _("Cruelty Case") + "</span>";
            }
            if (a.NONSHELTERANIMAL == 1) {
                available = "<span class=\"asm-search-nonshelter\">" + _("Non-Shelter Animal");
                if (a.ORIGINALOWNERID && a.ORIGINALOWNERID > 0) {
                    available += " " + html.icon("right") + " ";
                    available += "<a href=\"person?id=" + a.ORIGINALOWNERID + "\">" + a.ORIGINALOWNERNAME + "</a>";
                }
                available += "</span>";
            }
            var banner = [];
            if (common.nulltostr(a.HIDDENANIMALDETAILS) != "") {
                banner.push(a.HIDDENANIMALDETAILS);
            }
            if (common.nulltostr(a.MARKINGS) != "") {
                banner.push(a.MARKINGS);
            }
            if (common.nulltostr(a.ANIMALCOMMENTS) != "") {
                banner.push(a.ANIMALCOMMENTS);
            }
            var displaylocation = "";
            if (a.DECEASEDDATE != null && a.ACTIVEMOVEMENTID == 0) {
                displaylocation = "<span style=\"color: red\">" + _("Deceased") + " " + html.icon("right") + " " + a.DISPLAYLOCATIONNAME + "</span>";
            }
            else {
                displaylocation = a.DISPLAYLOCATIONNAME;
                if (currentowner != "") {
                    displaylocation += " " + html.icon("right") + " " + currentowner;
                }
                else if (a.SHELTERLOCATIONUNIT) {
                    displaylocation += ' <span class="asm-search-locationunit" title="' + html.title(_("Unit")) + '">' + a.SHELTERLOCATIONUNIT + '</span>';
                }
            }
            var first_column = [
                '<input type="hidden" id="animalid" value="' + a.ID + '" />',
                '<table class="asm-left-table"><tr>',
                '<td align="center">',
                '<a href="' + html.img_src(a, "animal") + '">',
                '<img onerror="image_error(this)" class="asm-thumbnail thumbnailshadow" src="' + html.thumbnail_src(a, "animalthumb") + '" />',
                '</a>',
                mediaprompt,
                '</td>',
                '<td width="30%">',
                '<h2>' + a.ANIMALNAME + ' - ' + a.CODE + ' ' + html.animal_emblems(a) + '</h2>',
                '<p>' + common.substitute(_("{0} {1} aged {2}"), { "0": "<b>" + a.SEXNAME, "1": a.SPECIESNAME + "</b>", "2": "<b>" + a.ANIMALAGE + "</b>" })  + '<br />',
                html.truncate(banner.join(". "), 100),
                '</p>',
                '</td>'
            ].join("\n");
            var second_column = [
                '<td width="30%">',
                '<table>',
                '<tr>',
                '<td id="hloc">' + _("Location") + ':</td><td><b>' + displaylocation + '</b></td>',
                '</tr>',
                '<tr>',
                '<td id="hentshel">' + _("Entered shelter") + '</td><td><b>' + format.date(a.DATEBROUGHTIN) + '</b></td>',
                '</tr>',
                '<tr>',
                '<td id="hleftshel">' + _("Left shelter") + ':</td><td><b>' + format.date(a.ACTIVEMOVEMENTDATE) + '</b></td>',
                '</tr>',
                '<tr>',
                '<td id="htimeonshel">' + _("Time on shelter") + ':</td><td><b>' + a.TIMEONSHELTER + '</b></td>',
                '</tr>',
                '</table>',
                '</td>'
            ].join("\n");
            if (a.NONSHELTERANIMAL == 1) {
                second_column = "<td width=\"30%\">&nbsp;</td>";
            }
            var third_column = [
                '<td width="30%">',
                _("Added by {0} on {1}").replace("{0}", "<b>" + a.CREATEDBY + "</b>").replace("{1}", "<b>" + format.date(a.CREATEDDATE) + "</b>") + '<br />',
                _("Last changed by {0} on {1}").replace("{0}", "<b>" + a.LASTCHANGEDBY + "</b>").replace("{1}", "<b>" + format.date(a.LASTCHANGEDDATE) + "</b>") + '<br />',
                available,
                '</td>',
                '</tr>',
                '</table>'
            ].join("\n");
            var s = [
                '<div class="asm-banner ui-helper-reset ui-widget-content ui-corner-all">',
                first_column,
                second_column,
                third_column,
                '</div>',
                '<div class="asm-tabbar">',
                '<ul class="asm-tablist">'
            ].join("\n");
            var tabs = [[ "animal", "animal", _("Animal"), "" ],
                [ "vaccination", "animal_vaccination", _("Vaccination"), "vaccination" ],
                [ "test", "animal_test", _("Test"), "test" ],
                [ "medical", "animal_medical", _("Medical"), "medical" ],
                [ "diet", "animal_diet", _("Diet"), "diet" ],
                [ "costs", "animal_costs", _("Costs"), "cost" ],
                [ "donations", "animal_donations", _("Donations"), "donation" ],
                [ "media", "animal_media", _("Media"), "media" ],
                [ "diary", "animal_diary", _("Diary"), "diary" ],
                [ "movements", "animal_movements", _("Movements"), "movement" ],
                [ "logs", "animal_log", _("Log"), "log"]];
            $.each(tabs, function(it, vt) {
                var key = vt[0], url = vt[1], display = vt[2], iconname = vt[3];
                if (key == selected) {
                    s += "<li class=\"ui-tabs-selected ui-state-active\"><a href=\"#\">" + display + " " + check_display_icon(key, iconname) + "</a></li>";
                }
                else {
                    s += "<li><a href=\"" + url + "?id=" + a.ID + "\">" + display + " " + check_display_icon(key, iconname) + "</a></li>";
                }
            });
            s += "</ul>";
            s += '<div id="asm-content">';
            return s;
        },

        /**
         * Returns a bunch of <li> tags with links to run diary tasks.
         * tasks: A set of diary task records
         * mode: ANIMAL or PERSON
         */
        diary_task_list: function(tasks, mode) {
            var s = [];
            $.each(tasks, function(i, t) {
                s.push('<li class="asm-menu-item"><a href="#" class="diarytask" data="' + mode + ' ' + t.ID + ' ' + t.NEEDSDATE + '">' + t.NAME + '</a></li>');
            });
            return s.join("\n");
        },

        /**
         * Returns the header for the lost and found pages, with the banner info and
         * tabs. Since the content will be contained in a tba, the caller needs to add a
         * div when they are done.
         * mode: "lost" or "found"
         * a: A lost/found animal row from lostfound.get_lostanimal/get_foundanimal
         * selected: The name of the selected tab (details, media, diary, log)
         * counts: A dictionary of tabnames with record counts
         */
        lostfound_edit_header: function(mode, a, selected, counts) {
            var check_display_icon = function(key, iconname) {
                if (key == "animal") { return html.icon("blank"); }
                if (counts[key.toUpperCase()] > 0) {
                    return html.icon(iconname);
                }
                return html.icon("blank");
            };
            var lf = "", area = "", dl = "", dlv = "", prefix = "", tdclass = "";
            if (mode == "lost") {
                lf = _("Lost");
                area = a.AREALOST;
                dl = _("Date Lost");
                dlv = format.date(a.DATELOST);
                prefix = "lostanimal";
                tdclass = "asm-lostanimal-banner centered";
            }
            if (mode == "found") {
                lf = _("Found");
                area = a.AREAFOUND;
                dl = _("Date Found");
                dlv = format.date(a.DATEFOUND);
                prefix = "foundanimal";
                tdclass = "asm-foundanimal-banner centered";
            }
            var h = [
                '<div class="asm-banner ui-helper-reset ui-widget-content ui-corner-all">',
                '<input type="hidden" id="lfid" value="' + a.LFID + '" />',
                '<table class="asm-left-table" width="100%" style="border-collapse: collapse;"><tr>',
                '<td width="30%" class="' + tdclass + '">',
                '<h2>' + a.OWNERNAME + '</h2>',
                '<p>' + lf + ': ' + a.AGEGROUP + ' ' + a.SPECIESNAME + ' / ' + html.truncate(area) + '<br>',
                html.truncate(a.DISTFEAT) + '</p>',
                '</td>',
                '<td width="30%" class="' + tdclass + '">',
                '<table>',
                '<tr>',
                '<td>' + dl + ':</td><td><b>' + dlv + '</b></td>',
                '</tr><tr>',
                '<td>' + _("Date Reported") + ':</td><td><b>' + format.date(a.DATEREPORTED) + '</b></td>',
                '</tr><tr>',
                '<td>' + _("Comments") + ':</td><td><b>' + html.truncate(a.COMMENTS) + '</b></td>',
                '</tr>',
                '</table>',
                '</td>',
                '<td width="30%" class="' + tdclass + '">',
                _("Added by {0} on {1}").replace("{0}", "<b>" + a.CREATEDBY + "</b>").replace("{1}", "<b>" + format.date(a.CREATEDDATE) + "</b>") + ' <br/>',
                _("Last changed by {0} on {1}").replace("{0}", "<b>" + a.LASTCHANGEDBY + "</b>").replace("{1}", "<b>" + format.date(a.LASTCHANGEDDATE) + "</b>"),
                '</td>',
                '</tr>',
                '</table>',
                '</div>',
                '<div class="asm-tabbar">',
                '<ul class="asm-tablist">'
            ];
            var tabs = [[ "details", prefix, _("Details"), "" ],
                [ "media", prefix + "_media", _("Media"), "media" ],
                [ "diary", prefix + "_diary", _("Diary"), "diary" ],
                [ "logs", prefix + "_log", _("Log"), "log"]];
            $.each(tabs, function(it, vt) {
                var key = vt[0], url = vt[1], display = vt[2], iconname = vt[3];
                if (key == selected) {
                    h.push("<li class=\"ui-tabs-selected ui-state-active\"><a href=\"#\">" + display + " " + check_display_icon(key, iconname) + "</a></li>");
                }
                else {
                    h.push("<li><a href=\"" + url + "?id=" + a.ID + "\">" + display + " " + check_display_icon(key, iconname) + "</a></li>");
                }
            });
            h.push('</ul>');
            h.push('<div id="asm-content">');
            return h.join("\n");
        },

        /**
         * Returns the header for any of the person pages, with the thumbnail image, info and tabs
         * Since the content will be contained in a tab, the caller needs to add a div
         * p: A person row from get_person
         * selected: The name of the selected tab (person, donations, vouchers, media, diary, movements, links, log)
         */
        person_edit_header: function(p, selected, counts) {
            var check_display_icon = function(key, iconname) {
                if (key == "person") { return html.icon("blank"); }
                if (counts[key.toUpperCase()] > 0) {
                    return html.icon(iconname);
                }
                return html.icon("blank");
            };
            var flags = this.person_flags(p);
            var s = [
                '<div class="asm-banner ui-helper-reset ui-widget-content ui-corner-all">',
                '<input type="hidden" id="personid" value="' + p.ID + '" />',
                '<table class="asm-left-table"><tr>',
                '<td>',
                '<a href="' + html.img_src(p, "person") + '">',
                '<img onerror="image_error(this)" class="asm-thumbnail thumbnailshadow" src="' + html.thumbnail_src(p, "personthumb") + '" />',
                '</a>',
                '</td>',
                '<td width="30%">',
                '<h2>' + p.OWNERNAME + '</h2>',
                '<p><span style="font-style: italic">' + flags + '</span><br/>',
                html.truncate(p.COMMENTS) + '</p>',
                '</td>',
                '<td width="30%">',
                '<table>',
                '<tr>',
                '<td>' + p.OWNERADDRESS + '<br />',
                p.OWNERTOWN + ' ' + p.OWNERCOUNTY + ' ' + p.OWNERPOSTCODE + '<br />',
                p.HOMETELEPHONE + ' <br />',
                p.WORKTELEPHONE + ' <br />',
                p.MOBILETELEPHONE,
                '</td>',
                '</tr>',
                '</table>',
                '</td>',
                '<td width="30%">',
                _("Added by {0} on {1}").replace("{0}", "<b>" + p.CREATEDBY + "</b>").replace("{1}", "<b>" + format.date(p.CREATEDDATE) + "</b>"),
                '<br />',
                _("Last changed by {0} on {1}").replace("{0}", "<b>" + p.LASTCHANGEDBY + "</b>").replace("{1}", "<b>" + format.date(p.LASTCHANGEDDATE) + "</b>"),
                '</td>',
                '</tr>',
                '</table>',
                '</div>',
                '<div class="asm-tabbar">',
                '<ul class="asm-tablist">'
            ];
            var tabs =[[ "person", "person", _("Person"), "" ],
                [ "investigation", "person_investigation", _("Investigation"), "investigation" ],
                [ "donations", "person_donations", _("Donations"), "donation" ],
                [ "vouchers", "person_vouchers", _("Vouchers"), "donation" ],
                [ "media", "person_media", _("Media"), "media" ],
                [ "diary", "person_diary", _("Diary"), "diary" ],
                [ "movements", "person_movements", _("Movements"), "movement" ],
                [ "links", "person_links", _("Links"), "link" ],
                [ "logs", "person_log", _("Log"), "log"]];
            $.each(tabs, function(it, vt) {
                var key = vt[0], url = vt[1], display = vt[2], iconname = vt[3];
                if (key == "investigation" && config.bool("DisableInvestigation")) {
                    return;
                }
                if (key == selected) {
                    s.push("<li class=\"ui-tabs-selected ui-state-active\"><a href=\"#\">" + display + " " + check_display_icon(key, iconname) + "</a></li>");
                }
                else {
                    s.push("<li><a href=\"" + url + "?id=" + p.ID + "\">" + display + " " + check_display_icon(key, iconname) + "</a></li>");
                }
            });
            s.push("</ul>");
            s.push('<div id="asm-content">');
            return s.join("\n");
        },

        /** 
         * Returns a person's name in the correct
         * format as governed by OwnerNameFormat
         */
        person_name: function(row) {
            var oname = config.str("OwnerNameFormat");
            if (!oname) { oname = "{ownername}"; }
            oname = oname.replace("{ownername}", row.OWNERNAME);
            oname = oname.replace("{ownersurname}", row.OWNERSURNAME);
            oname = oname.replace("{ownerlastname}", row.OWNERSURNAME);
            oname = oname.replace("{ownerforenames}", row.OWNERFORENAMES);
            oname = oname.replace("{ownerfirstname}", row.OWNERFORENAMES);
            oname = oname.replace("{ownertitle}", row.OWNERTITLE);
            oname = oname.replace("{ownerinitials}", row.OWNERINITIALS);
            return oname;          
        },

        /**
         * Returns a link to a person, formatting the name
         * according to the system config element OwnerNameFormat
         * row: A row containing the ownername, ownersurname, etc. fields
         * ownerid: The owner ID number for the link
         */
        person_name_link: function(row, ownerid) {
            var h = '<a href="person?id=' + ownerid + '">';
            h += edit_header.person_name(row) + "</a>";
            return h;
        },

        /**
         * Returns a string list of enabled flags for a person record,
         * Eg: Volunteer, member, donor, etc.
         */
        person_flags: function(p) {
            var flags = [];
            if (p.ISACO == 1) {
                flags.push(_("ACO"));
            }
            if (p.ISBANNED == 1) {
                flags.push("<span style=\"color: red\">" + _("Banned") + "</span>");
            }
            if (p.INVESTIGATION > 0) {
                flags.push("<span style=\"color: red\">" + _("Investigation") + "</span>");
            }
            if (p.ISDONOR == 1) {
                flags.push(_("Donor"));
            }
            if (p.ISFOSTERER == 1) {
                flags.push(_("Fosterer"));
            }
            if (p.IDCHECK == 1) {
                flags.push(_("Homechecked"));
            }
            if (p.ISHOMECHECKER == 1) {
                flags.push(_("Homechecker"));
            }
            if (p.ISMEMBER == 1) {
                flags.push(_("Member"));
            }
            if (p.ISRETAILER == 1) {
                flags.push(_("Retailer"));
            }
            if (p.ISSHELTER == 1) {
                flags.push(_("Shelter"));
            }
            if (p.ISSTAFF == 1) {
                flags.push(_("Staff"));
            }
            if (p.ISVET == 1) {
                flags.push(_("Vet"));
            }
            if (p.ISVOLUNTEER == 1) {
                flags.push(_("Volunteer"));
            }
            if (p.ADDITIONALFLAGS != null) {
                var stock = [ "aco", "banned", "donor", "fosterer", "homechecked", "homechecker", "member",
                    "shelter", "retailer", "staff", "giftaid", "vet", "volunteer"];
                $.each(p.ADDITIONALFLAGS.split("|"), function(i, v) {
                    if (v != "" && $.inArray(v, stock) == -1) {
                        flags.push(v);
                    }
                });
            }
            return flags.join(", ");
        },

        /**
         * Returns a bunch of <li> tags with links to create document templates.
         * templates: A set of template rows from the dbfs
         * mode: ANIMAL or PERSON
         * id: The record ID
         */
        template_list: function(templates, mode, id) {
            var s = [];
            var lastpath = "";
            $.each(templates, function(i, t) {
                if (t.PATH != lastpath) {
                    s.push('<li class="asm-menu-category">' + t.PATH + '</li>');
                    lastpath = t.PATH;
                }
                s.push('<li class="asm-menu-item"><a target="_blank" class="templatelink" data="' + t.ID + '" href="document_gen?mode=' + mode + '&id=' + id + '&template=' + t.ID + '">' + t.NAME + '</a></li>');
            });
            return s.join("\n");
        },

        /** 
         * Returns the header for the waiting list pages, with the banner info and
         * tabs.
         * a: A waiting list row from animal.get_waitinglist_query
         * selected: The name of the selected tab (details, media, diary, log)
         */
        waitinglist_edit_header: function(a, selected, counts) {
            var check_display_icon = function(key, iconname) {
                if (key == "details") { return html.icon("blank"); }
                if (counts[key.toUpperCase()] > 0) {
                    return html.icon(iconname);
                }
                return html.icon("blank");
            };
            var tdclass = "centered", removal = "";
            if (!a.DATEREMOVEDFROMLIST) {
                if (a.URGENCY == 5) { tdclass = "asm-wl-lowest centered"; }
                else if (a.URGENCY == 4) { tdclass = "asm-wl-low centered"; }
                else if (a.URGENCY == 3) { tdclass = "asm-wl-medium centered"; }
                else if (a.URGENCY == 2) { tdclass = "asm-wl-high centered"; }
                else if (a.URGENCY == 1) { tdclass = "asm-wl-urgent centered"; }
            }
            else {
                removal = "<tr><td>" + _("Removed") + "</td><td><b>" + format.date(a.DATEREMOVEDFROMLIST) + "</b></td></tr>";
            }
            var h = [
                '<div class="asm-banner ui-helper-reset ui-widget-content ui-corner-all">',
                '<input type="hidden" id="waitinglistid" value="' + a.WLID + '" />',
                '<table class="asm-left-table" width="100%" style="border-collapse: collapse;"><tr>',
                '<td width="30%" class="' + tdclass + '">',
                '<h2>' + a.OWNERNAME + '</h2>',
                '<p>' + a.SPECIESNAME + ': ' + html.truncate(a.ANIMALDESCRIPTION) + '</p>',
                '</td>',
                '<td width="30%" class="' + tdclass + '">',
                '<table>',
                '<tr>',
                '<td>' + _("Rank") + ':</td><td><b>' + a.RANK + '</b></td>',
                '</tr><tr>',
                '<td>' + _("Date put on list") + ':</td><td><b>' + format.date(a.DATEPUTONLIST) + '</b></td>',
                '</tr><tr>',
                '<td>' + _("Time on list") + ':</td><td><b>' + a.TIMEONLIST + '</b></td>',
                '</tr><tr>',
                '<td>' + _("Reason") + ':</td><td><b>' + html.truncate(a.REASONFORWANTINGTOPART) + '</b></td>',
                '</tr>',
                removal,
                '</table>',
                '</td>',
                '<td width="30%" class="' + tdclass + '">',
                _("Added by {0} on {1}").replace("{0}", "<b>" + a.CREATEDBY + "</b>").replace("{1}", "<b>" + format.date(a.CREATEDDATE) + "</b>") + ' <br/>',
                _("Last changed by {0} on {1}").replace("{0}", "<b>" + a.LASTCHANGEDBY + "</b>").replace("{1}", "<b>" + format.date(a.LASTCHANGEDDATE) + "</b>"),
                '</td>',
                '</tr>',
                '</table>',
                '</div>',
                '<div class="asm-tabbar">',
                '<ul class="asm-tablist">'
            ];
            var tabs = [[ "details", "waitinglist", _("Details"), "" ],
                [ "media", "waitinglist_media", _("Media"), "media" ],
                [ "diary", "waitinglist_diary", _("Diary"), "diary" ],
                [ "logs", "waitinglist_log", _("Log"), "log"]];
            $.each(tabs, function(it, vt) {
                var key = vt[0], url = vt[1], display = vt[2], iconname = vt[3];
                if (key == selected) {
                    h.push("<li class=\"ui-tabs-selected ui-state-active\"><a href=\"#\">" + display + " " + check_display_icon(key, iconname) + "</a></li>");
                }
                else {
                    h.push("<li><a href=\"" + url + "?id=" + a.ID + "\">" + display + " " + check_display_icon(key, iconname) + "</a></li>");
                }
            });
            h.push('</ul>');
            h.push('<div id="asm-content">');
            return h.join("\n");
        }

    };

});


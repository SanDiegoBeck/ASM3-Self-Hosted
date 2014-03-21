/*jslint browser: true, forin: true, eqeq: true, white: true, sloppy: true, vars: true, nomen: true */
/*global $, _, asm, additional, common, config, controller, dlgfx, format, header, html, validate */

$(function() {

    var animal_find_results = {

        render: function() {
            return [
                html.content_header(_("Results")),
                '<div id="asm-results">',
                '<div class="ui-state-highlight ui-corner-all" style="margin-top: 5px; padding: 0 .7em">',
                '<p><span class="ui-icon ui-icon-search" style="float: left; margin-right: .3em;"></span>',
                controller.resultsmessage,
                controller.wasonshelter ? "<br />" + _("You didn't specify any search criteria, so an on-shelter search was assumed.") : "",
                '</p>',
                '</div>',
                '<table id="table-searchresults">',
                animal_find_results.render_tablehead(),
                '<tbody>',
                animal_find_results.render_tablebody(),
                '</tbody>',
                '</table>',
                '</div>',
                html.content_footer()
            ].join("\n");
        },

        /**
         * Renders the table.head tag with columns in the right order
         */
        render_tablehead: function() {
            var labels = animal_find_results.column_labels();
            var s = [];
            s.push("<thead>");
            s.push("<tr>");
            $.each(labels, function(i, label) {
                s.push("<th>" + label + "</th>");
            });
            s.push("</tr>");
            s.push("</thead>");
            return s.join("\n");
        },

        /**
         * Renders the table body with columns in the right order and
         * highlighting styling applied, etc.
         */
        render_tablebody: function() {
            var h = [];
            $.each(controller.rows, function(ir, row) {
                h.push("<tr>");
                $.each(animal_find_results.column_names(), function(ic, name) {

                    // Generate the animal selector
                    var link = "<span style=\"white-space: nowrap\">";
                    link += html.animal_emblems(row);
                    link += " <a id=\"action-" + row.ID + "\" href=\"animal?id=" + row.ID + "\">";
                    // Show the whole row in red if the animal is deceased
                    if (row.DECEASEDDATE) {
                        h.push("<td style=\"color: red\">");
                    }
                    else {
                        h.push("<td>");
                    }
                    var value = "";
                    if (row.hasOwnProperty(name.toUpperCase())) {
                        value = row[name.toUpperCase()];
                    }
                    var formatted = animal_find_results.format_column(row, name, value, controller.additional);
                    if (name == "AnimalName") { 
                        formatted = link + formatted + "</a></span>";
                    }
                    h.push(formatted);
                    h.push("</td>");
                });
                h.push("</tr>");
            });
            return h.join("\n");
        },


        bind: function() {
            $("#table-searchresults").table();
        },

        sync: function() {
            // retrigger the sort
            $("#table-searchresults").trigger("sorton", [[[0,0]]]);
        },

        /** 
         * Returns a list of our configured viewable column names
         */
        column_names: function() {
            var cols = [];
            $.each(config.str("SearchColumns").split(","), function(i, v) {
                cols.push($.trim(v));
            });
            return cols;
        },

        /**
         * Returns a list of our configured viewable column labels
         */
        column_labels: function() {
            var names = animal_find_results.column_names();
            var labels = [];
            $.each(names, function(i, name) {
                labels.push(animal_find_results.column_label(name));
            });
            return labels;
        },

        /**
         * Returns the number of configured viewable columns
         */
        column_count: function() {
            return animal_find_results.column_names().length;
        },

        /**
         * Returns the i18n translated label for a column with name
         * add: Additional fields to scan for labels
         */
        column_label: function(name, add) {
            var labels = {
                "AnimalTypeID": _("Type"),
                "AnimalName": _("Name"),
                "BaseColourID": _("Color"),
                "SpeciesID": _("Species"),
                "BreedName":  _("Breed"),
                "CoatType":  _("Coat Type"),
                "Markings":  _("Features"),
                "ShelterCode":  _("Code"),
                "AcceptanceNumber":  _("Litter Ref"),
                "DateOfBirth":  _("Date Of Birth"),
                "AgeGroup":  _("Age"),
                "AnimalAge":  _("Age"),
                "DeceasedDate":  _("Died"),
                "Sex":  _("Sex"),
                "IdentichipNumber":  _("Microchip"),
                "IdentichipDate":  _("Date"),
                "TattooNumber":  _("Tattoo"),
                "TattooDate":  _("Tattoo"),
                "Neutered":  _("Altered"),
                "NeuteredDate":  _("Altered"),
                "CombiTested":  _("FIV/L Tested"),
                "CombiTestDate":  _("FIV/L Tested"),
                "CombiTestResult":  _("FIV"),
                "FLVResult":  _("FLV"),
                "HeartwormTested":  _("Heartworm Tested"),
                "HeartwormTestDate":  _("Heartworm Tested"),
                "HeartwormTestResult":  _("Heartworm"),
                "Declawed":  _("Declawed"),
                "HiddenAnimalDetails":  _("Hidden"),
                "AnimalComments":  _("Comments"),
                "ReasonForEntry":  _("Entry Reason"),
                "ReasonNO":  _("Reason Not From Owner"),
                "DateBroughtIn":  _("Brought In"),
                "EntryReasonID":  _("Entry Reason"),
                "HealthProblems":  _("Health Problems"),
                "PTSReason":  _("Euthanized"),
                "PTSReasonID":  _("Euthanized"),
                "IsGoodWithCats":  _("Good with Cats"),
                "IsGoodWithDogs":  _("Good with Dogs"),
                "IsGoodWithChildren":  _("Good with Children"),
                "IsHouseTrained":  _("Housetrained"),
                "IsNotAvailableForAdoption":  _("Not Available for Adoption"),
                "IsHold":  _("Hold"),
                "HoldUntilDate": _("Hold until"),
                "IsQuarantine":  _("Quarantine"),
                "HasSpecialNeeds":  _("Special Needs"),
                "ShelterLocation":  _("Location"),
                "ShelterLocationUnit":  _("Unit"),
                "Size":  _("Size"),
                "RabiesTag":  _("RabiesTag"),
                "TimeOnShelter":  _("On Shelter"),
                "DaysOnShelter":  _("On Shelter"),
                "HasActiveReserve": _("Reserved"),
                "Image": _("Image")
            };
            if (labels.hasOwnProperty(name)) {
                return labels[name];
            }
            if (add) {
                var alabel;
                $.each(add, function(i, v) {
                    if (v.FIELDNAME.toLowerCase() == name.toLowerCase()) {
                        alabel = v.FIELDLABEL;
                        return false; // break
                    }
                });
                if (alabel) {
                    return alabel;
                }
            }
            return name;
        },

        /**
         * Returns a formatted column
         * row: A row from the get_waitinglist query
         * name: The name of the column
         * value: The value of the row/column to format from the resultset
         * add: The additional row results
         */
        format_column: function(row, name, value, add) {
            var DATE_FIELDS = [ "DateOfBirth", "DeceasedDate", "IdentichipDate", "TattooDate", 
                "NeuteredDate", "CombiTestDate", "HeartwormTestDate", "DateBroughtIn", "HoldUntilDate" ],
            STRING_FIELDS = [ "AnimalName", "BreedName", "Markings", "AcceptanceNumber", 
                "AgeGroup", "IdentichipNumber", "TattooNumber", "HiddenAnimalDetails", 
                "AnimalComments", "ReasonForEntry", "HealthProblems", "PTSReason", 
                "RabiesTag", "TimeOnShelter", "DaysOnShelter", "AnimalAge", "ShelterLocationUnit" ],
            YES_NO_UNKNOWN_FIELDS = [ "IsGoodWithCats", "IsGoodWithDogs", "IsGoodWithChildren",
                "IsHouseTrained", "IsNotAvailableForAdoption", "IsHold", "IsQuarantine" ],
            YES_NO_FIELDS = [ "Neutered", "CombiTested", "HeartwormTested", "Declawed", 
                "HasActiveReserve", "HasSpecialNeeds" ],
            POS_NEG_UNKNOWN_FIELDS = [ "CombiTestResult", "FLVResult", "HeartwormTestResult" ],
            rv = "";
            if (name == "AnimalTypeID") { rv = row.ANIMALTYPENAME; }
            else if ( name == "BaseColourID") { rv = row.BASECOLOURNAME; }
            else if ( name == "SpeciesID") { rv = row.SPECIESNAME; }
            else if ( name == "CoatType") { rv = row.COATTYPENAME; }
            else if ( name == "Sex") { rv = row.SEXNAME; }
            else if ( name == "EntryReasonID") { rv = row.ENTRYREASONNAME; }
            else if ( name == "PTSReasonID") { rv = row.PTSREASONNAME; }
            else if ( name == "ShelterLocation") { 
                rv = row.DISPLAYLOCATIONNAME; 
                if (row.SHELTERLOCATIONUNIT) {
                    rv += ' <span class="asm-search-locationunit">' + row.SHELTERLOCATIONUNIT + '</span>';
                }
            }
            else if ( name == "Size") { rv = row.SIZENAME; }
            else if ( name == "ShelterCode") { rv = row.CODE; }
            else if ($.inArray(name, DATE_FIELDS) > -1) {
                rv = format.date(value);
            }
            else if ($.inArray(name, STRING_FIELDS) > -1) {
                rv = value;
            }
            else if ($.inArray(name, YES_NO_FIELDS) > -1) {
                if (value == 0) { rv = _("No"); }
                if (value == 1) { rv = _("Yes"); }
            }
            else if ($.inArray(name, YES_NO_UNKNOWN_FIELDS) > -1) {
                if (value == 0) { rv = _("Yes"); }
                else if (value == 1) { rv = _("No"); }
                else { rv = _("Unknown"); }
            }
            else if ($.inArray(name, POS_NEG_UNKNOWN_FIELDS) > -1) {
                if (value == 1) { rv = _("Negative"); }
                else if (value == 2) { rv = _("Positive"); }
                else { rv = _("Unknown"); }
            }
            else if ( name == "Image" ) {
                rv = "<img class=\"asm-thumbnail thumbnailshadow\" src=\"" + html.thumbnail_src(row, "animalthumb") + "\" />";
            }
            else if (add) {
                $.each(add, function(i, v) {
                    if (v.LINKID == row.ID && v.FIELDNAME.toLowerCase() == name.toLowerCase()) {
                        if (v.FIELDTYPE == additional.YESNO) { 
                            rv = v.VALUE == "1" ? _("Yes") : _("No");
                        }
                        else if (v.FIELDTYPE == additional.MONEY) {
                            rv = format.currency(v.VALUE);
                        }
                        else {
                            rv = v.VALUE;
                        }
                        return false; // break
                    }
                });
            }
            return rv;
        }    


    };

    common.module(animal_find_results, "animal_find_results", "results");

});

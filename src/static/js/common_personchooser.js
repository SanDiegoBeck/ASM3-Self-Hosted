/*jslint browser: true, forin: true, eqeq: true, plusplus: true, white: true, sloppy: true, vars: true, nomen: true */
/*global $, console, jQuery */
/*global asm, common, config, dlgfx, format, geo, html, header, validate, _, escape, unescape */

(function($) {

    /**
     * Person chooser widget. To create one, use a hidden input
     * with a class of asm-personchooser. You can also specify
     * a data-filter attribute to only search certain types of person
     * records.
     *     
     *     filter: One of all, vet, retailer, staff, fosterer, volunteer, shelter, 
     *            aco, homechecked, homechecker, member, donor
     *
     * <input id="person" data-filter="vet" class="asm-personchooser" data="boundfield" type="hidden" value="initialid" />
     *
     * callbacks: loaded (after loadbyid is complete)
     *            change (after user has clicked on a new selection)
     */
    $.widget("asm.personchooser", {
        options: {
            id: 0,
            rec: {},
            node: null,
            display: null,
            dialog: null,
            dialogadd: null,
            dialogsimilar: null,
            towns: "",
            counties: "",
            towncounties: "",
            personflags: [],
            filter: "all"
        },
        _create: function() {
            var self = this;
            var h = [
                '<div class="personchooser">',
                '<input class="personchooser-banned" type="hidden" value="" />',
                '<input class="personchooser-postcode" type="hidden" value = "" />',
                '<input class="personchooser-idcheck" type="hidden" value = "" />',
                '<table style="margin-left: 0px; margin-right: 0px; width: 100%">',
                '<tr>',
                '<td class="personchooser-display"></td>',
                '<td valign="top" align="right">',
                '<button class="personchooser-link-find">' + _("Select a person") + '</button>',
                '<button class="personchooser-link-new">' + _("Add a person") + '</button>',
                '<button class="personchooser-link-clear">' + _("Clear") + '</button>',
                '</td>',
                '</tr>',
                '</table>',
                '<div class="personchooser-similar" style="display: none" title="' + html.title(_("Similar Person")) + '">',
                    '<p><span class="ui-icon ui-icon-alert" style="float: left; margin: 0 7px 20px 0;"></span>',
                    _("This person is very similar to another person on file, carry on creating this record?"),
                    '<br /><br />',
                    '<span class="similar-person"></span>',
                    '</p>',
                '</div>',
                '<div class="personchooser-find" style="display: none" title="' + _("Find person") + '">',
                '<input class="asm-textbox" type="text" />',
                '<button>' + _("Search") + '</button>',
                '<img src="static/images/wait/wait16trans.gif" />',
                '<table width="100%">',
                '<thead>',
                    '<tr class="ui-widget-header">',
                        '<th>' + _("Name") + '</th>',
                        '<th>' + _("Code") + '</th>',
                        '<th>' + _("Address") + '</th>',
                        '<th>' + _("City") + '</th>',
                        '<th>' + _("State") + '</th>',
                        '<th>' + _("Zipcode") + '</th>',
                    '</tr>',
                '</thead>',
                '<tbody></tbody>',
                '</table>',
                '</div>',
                '<div class="personchooser-add" style="display: none" title="' + _("Add person") + '">',
                '<div class="ui-state-highlight ui-corner-all" style="margin-top: 20px; padding: 0 .7em">',
                '<p><span class="ui-icon ui-icon-info" style="float: left; margin-right: .3em;"></span>',
                _("At least the last name should be completed."),
                '</p>',
                '</div>',
                '<table width="100%">',
                '<tr>',
                '<td><label>' + _("Title") + '</label></td>',
                '<td><input class="asm-textbox" data="title" type="textbox" /></td>',
                '</tr>',
                '<tr>',
                '<td><label>' + _("Initials") + '</label></td>',
                '<td><input class="asm-textbox" maxlength="50" data="initials" type="textbox" /></td>',
                '</tr>',
                '<tr>',
                '<td><label>' + _("First name(s)") + '</label></td>',
                '<td><input class="asm-textbox" maxlength="200" data="forenames" type="textbox" /></td>',
                '</tr>',
                '<tr>',
                '<td><label>' + _("Last name") + '</label></td>',
                '<td><input class="asm-textbox" maxlength="100" data="surname" type="textbox" /></td>',
                '</tr>',
                '<tr>',
                '<td><label>' + _("Address") + '</label></td>',
                '<td><textarea class="asm-textareafixed" data="address" rows="3"></textarea></td>',
                '</tr>',
                '<tr>',
                '<td><label>' + _("City") + '</label></td>',
                '<td><input class="asm-textbox personchooser-town" maxlength="100" data="town" type="textbox" /></td>',
                '</tr>',
                '<tr>',
                '<td><label>' + _("State") + '</label></td>',
                '<td><input class="asm-textbox personchooser-county" maxlength="100" data="county" type="textbox" /></td>',
                '</tr>',
                '<tr>',
                '<td><label>' + _("Zipcode") + '</label></td>',
                '<td><input class="asm-textbox" data="postcode" type="textbox" /></td>',
                '</tr>',
                '<tr>',
                '<td><label>' + _("Home Phone") + '</label></td>',
                '<td><input class="asm-textbox" data="hometelephone" type="textbox" /></td>',
                '</tr>',
                '<tr>',
                '<td><label>' + _("Work Phone") + '</label></td>',
                '<td><input class="asm-textbox" data="worktelephone" type="textbox" /></td>',
                '</tr>',
                '<tr>',
                '<td><label>' + _("Cell Phone") + '</label></td>',
                '<td><input class="asm-textbox" data="mobiletelephone" type="textbox" /></td>',
                '</tr>',
                '<tr>',
                '<td><label>' + _("Email Address") + '</label></td>',
                '<td><input class="asm-textbox" maxlength="200" data="emailaddress" type="textbox" /></td>',
                '</tr>',
                '<tr>',
                '<td><label>' + _("Flags") + '</label></td>',
                '<td>',
                '<select class="personchooser-flags" data="flags" multiple="multiple">',
                '<option value="aco">' + _("ACO") + '</option>',
                '<option value="banned">' + _("Banned") + '</option>',
                '<option value="donor">' + _("Donor") + '</option>',
                '<option value="fosterer">' + _("Fosterer") + '</option>',
                '<option value="homechecked">' + _("Homechecked") + '</option>',
                '<option value="homechecker">' + _("Homechecker") + '</option>',
                '<option value="member">' + _("Member") + '</option>',
                '<option value="shelter">' + _("Other Shelter") + '</option>',
                '<option value="retailer">' + _("Retailer") + '</option>',
                '<option value="staff">' + _("Staff") + '</option>',
                asm.locale == "en_GB" ? '<option value="giftaid">' + _("UK Giftaid") + '</option>' : "",
                '<option value="vet">' + _("Vet") + '</option>',
                '<option value="volunteer">' + _("Volunteer") + '</option>',
                '</select>',
                '</td>',
                '</tr>',
                '</table>',
                '</div>',
                '</div>'
            ].join("\n");
            var node = $(h);
            this.options.node = node;
            var dialog = node.find(".personchooser-find");
            var dialogadd = node.find(".personchooser-add");
            var dialogsimilar = node.find(".personchooser-similar");
            this.options.dialog = dialog;
            this.options.dialogadd = dialogadd;
            this.options.dialogsimilar = dialogsimilar;
            this.options.display = node.find(".personchooser-display");
            this.element.parent().append(node);
            // Set the filter
            if (this.element.attr("data-filter")) { 
                this.options.filter = this.element.attr("data-filter");
            }
            // Create the find dialog
            var pcbuttons = {};
            pcbuttons[_("Cancel")] = function() { $(this).dialog("close"); };
            dialog.dialog({
                autoOpen: false,
                height: 400,
                width: 800,
                modal: true,
                dialogClass: "dialogshadow",
                show: dlgfx.edit_show,
                hide: dlgfx.edit_hide,
                buttons: pcbuttons
            });
            dialog.find("table").table({ floating_header: false });
            dialog.find("input").keydown(function(event) { if (event.keyCode == 13) { self.find(); return false; }});
            dialog.find("button").button().click(function() { self.find(); });
            dialog.find("img").hide();
            // Create the add dialog
            var pcaddbuttons = {};
            pcaddbuttons[_("Create this person")] = function() {
                var valid = true, dialogadd = self.options.dialogadd;
                // Validate fields that can't be blank
                dialogadd.find("label").removeClass("ui-state-error-text");
                dialogadd.find("input[data='surname']").each(function() {
                    if ($.trim($(this).val()) == "") {
                        $(this).parent().parent().find("label").addClass("ui-state-error-text");
                        $(this).focus();
                        valid = false;
                        return false;
                    }
                });
                if (!valid) { return; }
                // Disable the dialog buttons before we make any ajax requests
                dialogadd.disable_dialog_buttons();
                // check for similar people
                self.check_similar();
            };
            pcaddbuttons[_("Cancel")] = function() {
                $(this).dialog("close");
            };
            dialogadd.dialog({
                autoOpen: false,
                width: 400,
                modal: true,
                dialogClass: "dialogshadow",
                show: dlgfx.add_show,
                hide: dlgfx.add_hide,
                buttons: pcaddbuttons,
                close: function() {
                    dialogadd.find("input").val("");
                    dialogadd.find("label").removeClass("ui-state-error-text");
                }
            });
            // Bind the find button
            node.find(".personchooser-link-find")
                .button({ icons: { primary: "ui-icon-search" }, text: false })
                .click(function() {
                    dialog.dialog("open");
                });
            // Bind the new button
            node.find(".personchooser-link-new")
                .button({ icons: { primary: "ui-icon-plus" }, text: false })
                .click(function() {
                    dialogadd.dialog("open");
                });
            // Bind the clear button
            node.find(".personchooser-link-clear")
                .button({ icons: { primary: "ui-icon-trash" }, text: false })
                .click(function() {
                    self.clear();
                });
            /// Go to the backend to get the towns, counties and person flags  
            $.ajax({
                type: "GET",
                url:  "person_embed",
                data: { mode: "lookup" },
                dataType: "text",
                success: function(data, textStatus, jqXHR) {
                    var h = "";
                    var d = jQuery.parseJSON(data);
                    self.options.towns = d.towns;
                    self.options.counties = d.counties;
                    self.options.towncounties = d.towncounties;
                    self.options.personflags = d.flags;
                    // Add additional person flags to the screen
                    var exopt = "";
                    $.each(self.options.personflags, function(i, flag) {
                        exopt += "<option>" + flag.FLAG + "</option>";
                    });
                    if (exopt != "") {
                        dialogadd.find(".personchooser-flags").append(exopt);
                    }
                    // Setup autocomplete widgets with the towns/counties
                    dialogadd.find(".personchooser-town").autocomplete({ source: html.decode(self.options.towns).split("|") });
                    dialogadd.find(".personchooser-county").autocomplete({ source: html.decode(self.options.counties).split("|") });
                    // When the user changes a town, suggest a county if it's blank
                    dialogadd.find(".personchooser-town").blur(function() {
                        if (dialogadd.find(".personchooser-county").val() == "") {
                            var tc = html.decode(self.options.towncounties);
                            var idx = tc.indexOf(dialogadd.find(".personchooser-town").val() + "^");
                            if (idx != -1) {
                                dialogadd.find(".personchooser-county").val(tc.substring(tc.indexOf("^^", idx) + 2, tc.indexOf("|", idx)));
                            }
                        }
                    });
                    // Setup person flag select widget
                    dialogadd.find(".personchooser-flags").attr("title", _("Select"));
                    dialogadd.find(".personchooser-flags").asmSelect({
                        animate: true,
                        sortable: true,
                        removeLabel: '<strong>X</strong>',
                        listClass: 'bsmList-custom',  
                        listItemClass: 'bsmListItem-custom',
                        listItemLabelClass: 'bsmListItemLabel-custom',
                        removeClass: 'bsmListItemRemove-custom'
                    });
                    // Was there a value already set by the markup? If so, use it
                    if (self.element.val() != "" && self.element.val() != "0") {
                        self.loadbyid(self.element.val());
                    }
                },
                error: function(jqxhr, textstatus, response) {
                    common.console_log(response);
                }
            });
        },
        /**
         * Load a person record from its ID
         */
        loadbyid: function(personid) {
            this.clear();
            if (!personid || personid == "0" || personid == "") { return; }
            var self = this, node = this.options.node, display = this.options.display, dialog = this.options.dialog;
            var formdata = "mode=id&id=" + personid;
            $.ajax({
                type: "POST",
                url:  "person_embed",
                data: formdata,
                dataType: "text",
                success: function(data, textStatus, jqXHR) {
                    var h = "";
                    var people = jQuery.parseJSON(data);
                    var rec = people[0];
                    self.element.val(rec.ID);
                    var disp = "<span class=\"justlink\"><a class=\"asm-embed-name\" href=\"person?id=" + rec.ID + "\">" + 
                        rec.OWNERNAME + " - " + rec.OWNERCODE + "</a></span>";
                    disp += "<br/>" + rec.OWNERADDRESS + "<br/>" + rec.OWNERTOWN + "<br/>" + rec.OWNERCOUNTY + 
                        "<br/>" + rec.OWNERPOSTCODE + "<br/>" + rec.HOMETELEPHONE + "<br/>" + rec.WORKTELEPHONE + 
                        "<br/>" + rec.MOBILETELEPHONE + "<br/>" + rec.EMAILADDRESS;
                    display.html(disp);
                    node.find(".personchooser-banned").val(rec.ISBANNED);
                    node.find(".personchooser-idcheck").val(rec.IDCHECK);
                    node.find(".personchooser-postcode").val(rec.OWNERPOSTCODE);
                    common.inject_target();
                    self._trigger("loaded", null, rec);
                },
                error: function(jqxhr, textstatus, response) {
                    common.console_log(response);
                }
            });
        },
        /**
         * Does the backend find and updates the onscreen table
         * in the find dialog
         */
        find: function() {
            var self = this, dialog = this.options.dialog, node = this.options.node, 
                display = this.options.display;
            dialog.find("img").show();
            dialog.find("button").button("disable");
            var q = encodeURIComponent(dialog.find("input").val());
            var filter = this.options.filter;
            var formdata = "mode=find&filter=" + filter + "&q=" + q;
            $.ajax({
                type: "POST",
                url:  "person_embed",
                data: formdata,
                dataType: "text",
                success: function(data, textStatus, jqXHR) {
                    var h = "";
                    var people = jQuery.parseJSON(data);
                    $.each(people, function(i, p) {
                        h += "<tr>";
                        h += "<td><a href=\"#\" data=\"" + i + "\">" + p.OWNERNAME + "</a></td>";
                        h += "<td>" + p.OWNERCODE + "</td>";
                        h += "<td>" + p.OWNERADDRESS + "</td>";
                        h += "<td>" + p.OWNERTOWN + "</td>";
                        h += "<td>" + p.OWNERCOUNTY + "</td>";
                        h += "<td>" + p.OWNERPOSTCODE + "</td>";
                        h += "</tr>";
                    });
                    dialog.find("table > tbody").html(h);
                    // Remove any existing events from previous searches
                    dialog.off("click", "a");
                    // Use delegation to bind click events for 
                    // the person once clicked. Triggers the change callback
                    dialog.on("click", "a", function(e) {
                        var rec = people[$(this).attr("data")];
                        self.element.val(rec.ID);
                        self.options.rec = rec;
                        var disp = "<span class=\"justlink\"><a class=\"asm-embed-name\" href=\"person?id=" + rec.ID + 
                            "\">" + rec.OWNERNAME + " - " + rec.OWNERCODE + "</a></span>";
                        disp += "<br/>" + rec.OWNERADDRESS + "<br/>" + rec.OWNERTOWN + "<br/>" + rec.OWNERCOUNTY + "<br/>" + 
                            rec.OWNERPOSTCODE + "<br/>" + rec.HOMETELEPHONE + "<br/>" + rec.WORKTELEPHONE + "<br/>" + 
                            rec.MOBILETELEPHONE + "<br/>" + rec.EMAILADDRESS;
                        display.html(disp);
                        node.find(".personchooser-banned").val(rec.ISBANNED);
                        node.find(".personchooser-idcheck").val(rec.IDCHECK);
                        node.find(".personchooser-postcode").val(rec.OWNERPOSTCODE);
                        try { validate.dirty(true); } catch(exp) { }
                        dialog.dialog("close");
                        self._trigger("change", null, rec);
                    });
                    dialog.find("table").trigger("update");
                    dialog.find("img").hide();
                    dialog.find("button").button("enable");
                    common.inject_target();
                },
                error: function(jqxhr, textstatus, response) {
                    dialog.dialog("close");
                    common.console_log(response);
                    dialog.find("img").hide();
                    dialog.find("button").button("enable");
                }
            });
        },
        /**
         * Updates the geocode for a new person
         */
        update_geo: function(personid) {
            var dialogadd = this.options.dialogadd,
                address = dialogadd.find("[data='address']").val(), 
                town = dialogadd.find("[data='town']").val(), 
                county = dialogadd.find("[data='county']").val(), 
                postcode = dialogadd.find("[data='postcode']").val();
            var addrhash = geo.address_hash(address, town, county, postcode);
            geo.get_lat_long(address, town, county, postcode, function(lat, lon) {
                if (lat) {
                    var latlong = lat + "," + lon + "," + addrhash;
                    var formdata = "personid=" + personid + "&latlong=" + latlong;
                    common.ajax("person", formdata);
                }
            });
        },
        /**
         * Posts the add dialog to the backend to create the owner
         */
        add_person: function() {
            var self = this, dialogadd = this.options.dialogadd, dialogsimilar = this.options.dialogsimilar,
                display = this.options.display, node = this.options.node;
            var formdata = "mode=add&" + dialogadd.find("input, textarea, select").toPOST();
            $.ajax({
                type: "POST",
                url:  "person_embed",
                data: formdata,
                dataType: "text",
                success: function(result) {
                    var people = jQuery.parseJSON(result);
                    var rec = people[0];
                    self.element.val(rec.ID);
                    var disp = "<span class=\"justlink\"><a class=\"asm-embed-name\" href=\"person?id=" + rec.ID + "\">" + rec.OWNERNAME + "</a></span>";
                    disp += "<br/>" + rec.OWNERADDRESS + "<br/>" + rec.OWNERTOWN + "<br/>" + rec.OWNERCOUNTY + "<br/>" + rec.OWNERPOSTCODE + "<br/>" + rec.HOMETELEPHONE + "<br/>" + rec.WORKTELEPHONE + "<br/>" + rec.MOBILETELEPHONE + "<br/>" + rec.EMAILADDRESS;
                    display.html(disp);
                    node.find(".personchooser-banned").val(rec.ISBANNED);
                    node.find(".personchooser-idcheck").val(rec.IDCHECK);
                    node.find(".personchooser-postcode").val(rec.OWNERPOSTCODE);
                    try { validate.dirty(true); } catch(e) { }
                    dialogadd.dialog("close");
                    dialogsimilar.dialog("close");
                    common.inject_target();
                    dialogadd.enable_dialog_buttons();
                    dialogsimilar.enable_dialog_buttons();
                    // Update the geocode for the newly created record
                    self.update_geo(rec.ID);
                },
                error: function(jqxhr, textstatus, response) {
                    dialogadd.dialog("close");
                    common.console_log(response);
                }
            });
        },
        /**
         * Pops up the similar dialog box to prompt the user to decide
         * whether they want to create the owner or not. If they do,
         * calls add_person to do the adding.
         */
        show_similar: function() {
            var b = {}, self = this, dialogsimilar = this.options.dialogsimilar, dialogadd = this.options.dialogadd;
            b[_("Create")] = function() {
                dialogsimilar.disable_dialog_buttons();
                self.add_person();
                dialogsimilar.close();
                dialogadd.close();
                dialogsimilar.enable_dialog_buttons();
                dialogadd.enable_dialog_buttons();
            };
            b[_("Cancel")] = function() { 
                $(this).dialog("close");
                dialogsimilar.enable_dialog_buttons();
                dialogadd.enable_dialog_buttons();
            };
            dialogsimilar.dialog({
                 resizable: false,
                 modal: true,
                 width: 500,
                 dialogClass: "dialogshadow",
                 show: dlgfx.delete_show,
                 hide: dlgfx.delete_hide,
                 buttons: b
            });
        },
        /**
         * Checks to see whether we have a similar person
         * on file. If we do, calls show_siilar to popup the
         * confirmation dialog
         */
        check_similar: function() {
            var self = this, dialogadd = this.options.dialogadd, dialogsimilar = this.options.dialogsimilar;
            var formdata = "mode=similar&" + dialogadd.find("input[data='surname'], input[data='forenames'], input[data='address']").toPOST();
            $.ajax({
                type: "POST",
                url:  "person_embed",
                data: formdata,
                dataType: "text",
                success: function(result) {
                    var people = jQuery.parseJSON(result);
                    var rec = people[0];
                    if (rec === undefined) {
                        self.add_person();
                    }
                    else {
                        var disp = "<span class=\"justlink\"><a class=\"asm-embed-name\" href=\"#\">" + rec.OWNERNAME + "</a></span>";
                        disp += "<br/>" + rec.OWNERADDRESS + "<br/>" + rec.OWNERTOWN + "<br/>" + rec.OWNERCOUNTY + "<br/>" + rec.OWNERPOSTCODE + "<br/>" + rec.HOMETELEPHONE + "<br/>" + rec.WORKTELEPHONE + "<br/>" + rec.MOBILETELEPHONE + "<br/>" + rec.EMAILADDRESS;
                        dialogsimilar.find(".similar-person").html(disp);
                        // When the user clicks the name of the similar person,
                        // select it for the field instead
                        dialogsimilar.find(".asm-embed-name").click(function() {
                            self.loadbyid(rec.ID);
                            dialogsimilar.dialog("close");
                            dialogadd.dialog("close");
                            dialogsimilar.enable_dialog_buttons();
                            dialogadd.enable_dialog_buttons();
                        });
                        self.show_similar();
                    }
                },
                error: function(jqxhr, textstatus, response) {
                    common.console_log(response);
                }
            });
        },
        clear: function() {
            this.element.val("0");
            this.options.display.html("");
            //try { validate.dirty(true); } catch(e) { }
        }

    });

} (jQuery));
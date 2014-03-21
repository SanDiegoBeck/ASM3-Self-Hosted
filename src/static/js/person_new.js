/*jslint browser: true, forin: true, eqeq: true, white: true, sloppy: true, vars: true, nomen: true */
/*global $, jQuery, _, asm, common, config, controller, dlgfx, format, geo, header, html, validate */

$(function() {

    var person_new = {

        render: function() {
            return [
                '<div id="dialog-similar" style="display: none" title="' + html.title(_("Similar Person")) + '">',
                '<p><span class="ui-icon ui-icon-alert" style="float: left; margin: 0 7px 20px 0;"></span>',
                _("This person is very similar to another person on file, carry on creating this record?"),
                '<br /><br />',
                '<span class="similar-person"></span>',
                '</p>',
                '</div>',
                html.content_header(_("Add a new person")),
                '<table class="asm-table-layout">',
                '<tr>',
                '<td><label for="title">' + _("Title") + '</label></td>',
                '<td><input class="asm-textbox" maxlength="50" id="title" data="title" type="textbox" /></td>',
                '</tr>',
                '<tr>',
                '<td><label for="initials">' + _("Initials") + '</label></td>',
                '<td><input class="asm-textbox" maxlength="50" id="initials" data="initials" type="textbox" /></td>',
                '</tr>',
                '<tr>',
                '<td><label for="forenames">' + _("First name(s)") + '</label></td>',
                '<td><input class="asm-textbox" maxlength="200" id="forenames" data="forenames" type="textbox" /></td>',
                '</tr>',
                '<tr>',
                '<td><label for="surname">' + _("Last name") + '</label></td>',
                '<td><input class="asm-textbox" maxlength="100" id="surname" data="surname" type="textbox" /></td>',
                '</tr>',
                '<tr>',
                '<td><label for="address">' + _("Address") + '</label></td>',
                '<td><textarea class="asm-textareafixed" id="address" data="address" rows="3"></textarea></td>',
                '</tr>',
                '<tr class="towncounty">',
                '<td><label for="town">' + _("City") + '</label></td>',
                '<td><input class="asm-textbox" maxlength="100" id="town" data="town" type="textbox" /></td>',
                '</tr>',
                '<tr class="towncounty">',
                '<td><label for="county">' + _("State") + '</label></td>',
                '<td><input class="asm-textbox" maxlength="100" id="county" data="county" type="textbox" /></td>',
                '</tr>',
                '<tr>',
                '<td><label for="postcode">' + _("Zipcode") + '</label></td>',
                '<td><input class="asm-textbox" id="postcode" data="postcode" type="textbox" /></td>',
                '</tr>',
                '<tr>',
                '<td><label for="hometelephone">' + _("Home Phone") + '</label></td>',
                '<td><input class="asm-textbox" id="hometelephone" data="hometelephone" type="textbox" /></td>',
                '</tr>',
                '<tr>',
                '<td><label for="worktelephone">' + _("Work Phone") + '</label></td>',
                '<td><input class="asm-textbox" id="worktelephone" data="worktelephone" type="textbox" /></td>',
                '</tr>',
                '<tr>',
                '<td><label for="mobiletelephone">' + _("Cell Phone") + '</label></td>',
                '<td><input class="asm-textbox" id="mobiletelephone" data="mobiletelephone" type="textbox" /></td>',
                '</tr>',
                '<tr>',
                '<td><label for="emailaddress">' + _("Email Address") + '</label></td>',
                '<td><input class="asm-textbox" maxlength="200" id="emailaddress" data="emailaddress" type="textbox" /></td>',
                '</tr>',
                '<tr>',
                '<td><label for="flags">' + _("Flags") + '</label></td>',
                '<td>',
                '<select id="flags" data="flags" class="asm-bsmselect" multiple="multiple">',
                '</select>',
                '</td>',
                '</tr>',
                '</table>',
                '<div class="centered">',
                '<button id="add">' + html.icon("person-add") + ' ' + _("Create and edit") + '</button>',
                '</div>',
                html.content_footer()
            ].join("\n");
        },

        load_person_flags: function() {

            var field_option = function(json, post, label) {
                return '<option value="' + post + '">' + label + '</option>\n';
            };

            var flag_option = function(flag) {
                return '<option>' + flag + '</option>';
            };

            var h = [
                field_option("ISACO", "aco", _("ACO")),
                field_option("ISBANNED", "banned", _("Banned")),
                field_option("ISDONOR", "donor", _("Donor")),
                field_option("ISFOSTERER", "fosterer", _("Fosterer")),
                field_option("IDCHECK", "homechecked", _("Homechecked")),
                field_option("ISHOMECHECKER", "homechecker", _("Homechecker")),
                field_option("ISMEMBER", "member", _("Member")),
                field_option("ISSHELTER", "shelter", _("Other Shelter")),
                field_option("ISRETAILER", "retailer", _("Retailer")),
                field_option("ISSTAFF", "staff", _("Staff")),
                asm.locale == "en_GB" ? field_option("ISGIFTAID", "giftaid", _("UK Giftaid")) : "",
                field_option("ISVET", "vet", _("Vet")),
                field_option("ISVOLUNTEER", "volunteer", _("Volunteer"))
            ];

            $.each(controller.flags, function(i, v) {
                h.push(flag_option(v.FLAG));
            });

            $("#flags").html(h.join("\n"));
            $("#flags").change();

        },

        bind: function() {
            var validation = function() {
                // Remove any previous errors
                header.hide_error();
                $("label").removeClass("ui-state-error-text");
                var fields = [ "surname" ];
                var valid = true;
                $.each(fields, function(i, f) {
                    if ($("#" + f).val() == "") {
                        $("label[for='" + f + "']").addClass("ui-state-error-text");
                        $("#" + f).focus();
                        valid = false;
                        return false;
                    }
                });
                return valid;
            };

            var addPerson = function() {
                if (!validation()) { 
                    $("#asm-content button").button("enable"); 
                    return; 
                }
                header.show_loading(_("Creating..."));
                var formdata = $("input, textarea, select").toPOST();
                common.ajax_post("person_new", formdata, function(personid) { 
                    if (personid) { window.location = "person?id=" + personid; }
                    $("#asm-content button").button("enable");
                }, function() {
                    $("#asm-content button").button("enable");
                });
            };

            var similar_dialog = function() {
                var b = {}; 
                b[_("Create")] = function() {
                    $("#dialog-similar").disable_dialog_buttons();
                    addPerson();
                    $("#asm-content button").button("enable");
                };
                b[_("Cancel")] = function() { 
                    $(this).dialog("close");
                    $("#asm-content button").button("enable");
                };
                $("#dialog-similar").dialog({
                     resizable: false,
                     modal: true,
                     width: 500,
                     dialogClass: "dialogshadow",
                     show: dlgfx.delete_show,
                     hide: dlgfx.delete_hide,
                     buttons: b
                });
            };

            var check_for_similar = function() {
                if (!validation()) { return; }
                var formdata = "mode=similar&" + $("#surname, #forenames, #address").toPOST();
                common.ajax_post("person_embed", formdata, function(result) { 
                    var people = jQuery.parseJSON(result);
                    var rec = people[0];
                    if (rec === undefined) {
                        addPerson();
                    }
                    else {
                        var disp = "<span class=\"justlink\"><a class=\"asm-embed-name\" href=\"person?id=" + rec.ID + "\">" + rec.OWNERNAME + "</a></span>";
                        disp += "<br/>" + rec.OWNERADDRESS + "<br/>" + rec.OWNERTOWN + "<br/>" + rec.OWNERCOUNTY + "<br/>" + rec.OWNERPOSTCODE + "<br/>" + rec.HOMETELEPHONE + "<br/>" + rec.WORKTELEPHONE + "<br/>" + rec.MOBILETELEPHONE + "<br/>" + rec.EMAILADDRESS;
                        $(".similar-person").html(disp);
                        similar_dialog();
                    }
                });
            };

            person_new.load_person_flags();

            if (config.bool("HideTownCounty")) {
                $(".towncounty").hide();
            }

            $("#town").autocomplete({ source: controller.towns.split("|") });
            $("#county").autocomplete({ source: controller.counties.split("|") });
            $("#town").blur(function() {
                if ($("#county").val() == "") {
                    var tc = html.decode(controller.towncounties);
                    var idx = tc.indexOf($("#town").val() + "^");
                    if (idx != -1) {
                        $("#county").val(tc.substring(tc.indexOf("^^", idx) + 2, tc.indexOf("|", idx)));
                    }
                }
            });


            $("#add").button().click(function() {
                $("#asm-content button").button("disable");
                check_for_similar();
            });
        }
    };

    common.module(person_new, "person_new", "newdata");

});

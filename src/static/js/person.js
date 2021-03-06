/*jslint browser: true, forin: true, eqeq: true, white: true, sloppy: true, vars: true, nomen: true */
/*global $, jQuery, _, additional, asm, common, config, controller, dlgfx, edit_header, format, geo, header, html, mapping, validate */

$(function() {

    var person = {

        render_dialogs: function() {
            return [
                '<div id="dialog-dt-date" style="display: none" title="' + html.title(_("Select date for diary task")) + '">',
                '<input type="hidden" id="diarytaskid" />',
                '<table width="100%">',
                '<tr>',
                '<td><label for="seldate">' + _("Date") + '</label></td>',
                '<td><input id="seldate" type="text" class="asm-textbox asm-datebox" /></td>',
                '</tr>',
                '</table>',
                '</div>',
                '<div id="dialog-merge" style="display: none" title="' + html.title(_("Select person to merge")) + '">',
                '<div class="ui-state-highlight ui-corner-all" style="margin-top: 20px; padding: 0 .7em">',
                '<p><span class="ui-icon ui-icon-info" style="float: left; margin-right: .3em;"></span>',
                _("Select a person to merge into this record. The selected person will be removed, and their movements, diary notes, log entries, etc. will be reattached to this record."),
                '</p>',
                '</div>',
                html.capture_autofocus(),
                '<table width="100%">',
                '<tr>',
                '<td><label for="mergeperson">' + _("Person") + '</label></td>',
                '<td>',
                '<input id="mergeperson" data="mergeperson" type="hidden" class="asm-personchooser" value="" />',
                '</td>',
                '</tr>',
                '</table>',
                '</div>',
                '<div id="dialog-email" style="display: none" title="' + html.title(_("Email person"))  + '">',
                '<table width="100%">',
                '<tr>',
                '<td><label for="emailfrom">' + _("From") + '</label></td>',
                '<td><input id="emailfrom" data="from" type="text" class="asm-doubletextbox" /></td>',
                '</tr>',
                '<tr>',
                '<td><label for="emailto">' + _("To") + '</label></td>',
                '<td><input id="emailto" data="to" type="text" class="asm-doubletextbox" /></td>',
                '</tr>',
                '<tr>',
                '<td><label for="emailcc">' + _("CC") + '</label></td>',
                '<td><input id="emailcc" data="cc" type="text" class="asm-doubletextbox" /></td>',
                '</tr>',
                '<tr>',
                '<td><label for="emailsubject">' + _("Subject") + '</label></td>',
                '<td><input id="emailsubject" data="subject" type="text" class="asm-doubletextbox" /></td>',
                '</tr>',
                '<tr>',
                '<td></td>',
                '<td><input id="emailhtml" data="html" type="checkbox"',
                'title="' + html.title(_("Set the email content-type header to text/html")) + '" ',
                'class="asm-checkbox" /><label for="emailhtml">' + _("HTML") + '</label></td>',
                '</tr>',
                '<tr>',
                '<td></td>',
                '<td><input id="emailaddtolog" data="addtolog" type="checkbox"',
                'title="' + html.title(_("Add details of this email to the log after sending")) + '" ',
                'class="asm-checkbox" /><label for="emailaddtolog">' + _("Add to log") + '</label>',
                '<select id="emaillogtype" data="logtype" class="asm-selectbox">',
                html.list_to_options(controller.logtypes, "ID", "LOGTYPENAME"),
                '</select>',
                '</td>',
                '</tr>',
                '</table>',
                '<textarea id="emailbody" data="body" rows="15" class="asm-textarea"></textarea>',
                '</div>',
                '<div id="dialog-delete" style="display: none" title="' + _("Delete") + '">',
                '<p><span class="ui-icon ui-icon-alert" style="float: left; margin: 0 7px 20px 0;"></span>' + _("This will permanently remove this person, are you sure?") + '</p>',
                '</div>'
            ].join("\n");
        },

        render_details: function() {
            return [
                '<h3><a href="#">' + _("Name and Address") + '</a></h3>',
                '<div>',
                '<table width="100%">',
                '<tr>',
                '<!-- left table -->',
                '<td width="35%">',
                '<table class="additionaltarget" data="to7">',
                '<tr>',
                '<td><label for="code">' + _("Code") + '</label></td>',
                '<td>',
                '<span class="asm-person-code">' + controller.person.OWNERCODE + '</span>',
                '</td>',
                '</tr>',
                '<tr>',
                '<td><label for="title">' + _("Title") + '</label></td>',
                '<td>',
                '<input type="text" id="title" data-json="OWNERTITLE" data-post="title" maxlength="50" class="asm-textbox" />',
                '</td>',
                '</tr>',
                '<tr>',
                '<td><label for="initials">' + _("Initials") + '</label></td>',
                '<td>',
                '<input type="text" id="initials" data-json="OWNERINITIALS" data-post="initials" maxlength="50" class="asm-textbox" />',
                '</td>',
                '</tr>',
                '<tr>',
                '<td><label for="forenames">' + _("First Names") + '</label></td>',
                '<td>',
                '<input type="text" id="forenames" data-json="OWNERFORENAMES" data-post="forenames" maxlength="200" class="asm-textbox" />',
                '</td>',
                '</tr>',
                '<tr>',
                '<td><label for="surname">' + _("Last Name") + '</label></td>',
                '<td>',
                '<input type="text" id="surname" data-json="OWNERSURNAME" data-post="surname" maxlength="100" class="asm-textbox" />',
                '</td>',
                '</tr>',
                '<tr>',
                '<td><label for="email">' + _("Email") + '</label></td>',
                '<td>',
                '<input type="text" id="email" data-json="EMAILADDRESS" data-post="email" maxlength="200" class="asm-textbox" />',
                '</td>',
                '</tr>',
                '<tr>',
                '<td><label for="hometelephone">' + _("Home Phone") + '</label></td>',
                '<td>',
                '<input type="text" id="hometelephone" data-json="HOMETELEPHONE" data-post="hometelephone" class="asm-textbox" />',
                '</td>',
                '</tr>',
                '<tr>',
                '<td><label for="mobiletelephone">' + _("Cell Phone") + '</label></td>',
                '<td>',
                '<input type="text" id="mobiletelephone" data-json="MOBILETELEPHONE" data-post="mobiletelephone" class="asm-textbox" />',
                '</td>',
                '</tr>',
                '<tr>',
                '<td><label for="worktelephone">' + _("Work Phone") + '</label></td>',
                '<td>',
                '<input type="text" id="worktelephone" data-json="WORKTELEPHONE" data-post="worktelephone" class="asm-textbox" />',
                '</td>',
                '</tr>',
                '</table>',
                '<!-- right table -->',
                '<td width="30%">',
                '<table width="100%">',
                '<tr>',
                '<td><label for="address">' + _("Address") + '</label></td>',
                '<td>',
                '<textarea id="address" title="' + html.title(_("Address")) + '" data-json="OWNERADDRESS" data-post="address" rows="5" class="asm-textareafixed"></textarea>',
                '</td>',
                '</tr>',
                '<tr class="towncounty">',
                '<td><label for="town">' + _("City") + '</label></td>',
                '<td>',
                '<input type="text" id="town" data-json="OWNERTOWN" data-post="town" maxlength="100" class="asm-textbox" />',
                '</td>',
                '</tr>',
                '<tr class="towncounty">',
                '<td><label for="county">' + _("State") + '</label></td>',
                '<td>',
                '<input type="text" id="county" data-json="OWNERCOUNTY" data-post="county" maxlength="100" class="asm-textbox" />',
                '</td>',
                '</tr>',
                '<tr>',
                '<td><label for="postcode">' + _("Zipcode") + '</label></td>',
                '<td>',
                '<input type="text" id="postcode" data-json="OWNERPOSTCODE" data-post="postcode" class="asm-textbox" />',
                '</td>',
                '</tr>',
                '<!-- end right table -->',
                '</table>',
                '<!-- Third column, embedded map placeholder -->',
                '</td>',
                '<td width="35%">',
                '<input type="hidden" id="latlong" data-json="LATLONG" data-post="latlong" />',
                '<div id="embeddedmap" style="width: 100%; height: 300px; color: #000" />',
                '<!-- end outer table -->',
                '</td>',
                '</tr>',
                '</table>',
                '</div>'
            ].join("\n");
        },

        render_type: function() {
            return [
                '<h3><a href="#">' + _("Type") + '</a></h3>',
                '<div>',
                '<!-- Outer table -->',
                '<table width="100%">',
                '<tr>',
                '<td width="50%">',
                '<!-- Left table -->',
                '<table class="additionaltarget" data="to8">',
                '<tr>',
                '<td><label for="flags">' + _("Flags") + '</label></td>',
                '<td>',
                '<select id="flags" data="flags" class="asm-bsmselect" multiple="multiple">',
                '</select>',
                '</td>',
                '</tr>',
                '<tr>',
                '<td><label for="homecheckedby">' + _("Homechecked by") + '</label></td>',
                '<td>',
                '<input id="homecheckedby" data-json="HOMECHECKEDBY" data-post="homecheckedby" type="hidden" data-filter="homechecker" class="asm-personchooser" />',
                '</td>',
                '</tr>',
                '<tr>',
                '<td><label for="homechecked">' + _("on") + '</label></td>',
                '<td><input type="textbox" id="homechecked" data-json="DATELASTHOMECHECKED" data-post="homechecked" title="' + html.title(_("The date this person was homechecked.")) + '" class="asm-textbox asm-datebox" /></td>',
                '</tr>',
                '<tr>',
                '<td><label for="membershipnumber">' + _("Membership Number") + '</label></td>',
                '<td><input type="textbox" id="membershipnumber" data-json="MEMBERSHIPNUMBER" data-post="membershipnumber" title="' + html.title(_("If this person is a member, their membership number.")) + '" class="asm-textbox" /></td>',
                '</tr>',
                '<tr>',
                '<td><label for="membershipexpires">' + _("Membership Expiry") + '</label></td>',
                '<td><input type="textbox" id="membershipexpires" data-json="MEMBERSHIPEXPIRYDATE" data-post="membershipexpires" title="' + html.title(_("If this person is a member, the date that membership expires.")) + '" class="asm-textbox asm-datebox" /></td>',
                '</tr>',
                '</table>',
                '</td>',
                '<td>',
                '<!-- Right table -->',
                '<table width="100%">',
                '<tr>',
                '<td><label for="comments">' + _("Comments") + '</label</td>',
                '<td>',
                '<textarea id="comments" title="' + _("Comments") + '" data-json="COMMENTS" data-post="comments" rows="10" class="asm-textarea"></textarea>',
                '</td>',
                '</tr>',
                '</table>',
                '<!-- end outer table -->',
                '</td>',
                '</tr>',
                '</table>',
                '</div>'
            ].join("\n");
        },

        render_homechecker: function() {
            return [
                '<h3><a href="#">' + _("Homechecker") + '</a></h3>',
                '<div>',
                '<!-- outer table -->',
                '<table width="100%">',
                '<tr>',
                '<td width="50%">',
                '<p class="asm-header"><label for="areas">' + _("Homecheck Areas") + '</label></p>',
                '<textarea id="areas" class="asm-textarea" data-json="HOMECHECKAREAS" data-post="areas" rows="8" title="' + html.title(_("A list of areas this person will homecheck - eg: S60 S61")) + '"></textarea>',
                '</td>',
                '<td width="50%" valign="top">',
                '<!-- history table -->',
                '<p class="asm-header"><label>' + _("Homecheck History") + '</label></p>',
                '<table id="homecheckhistory" width="100%">',
                '<thead>',
                '<tr>',
                '<th>' + _("Date") + '</th>',
                '<th>' + _("Person") + '</th>',
                '<th>' + _("Comments") + '</th>',
                '</tr>',
                '</thead>',
                '<tbody>',
                '</tbody>',
                '</table>',
                '<!-- end outer table -->',
                '</td>',
                '</tr>',
                '</table>',
                '</div>'
            ].join("\n");
        },

        render_lookingfor: function() {
            return [
                '<h3><a href="#">' + _("Looking for") + ' <span id="tabcriteria" style="display: none" class="asm-icon asm-icon-animal"></span></a></h3><div>',
                '<!-- Outer table -->',
                '<table width="100%">',
                '<tr>',
                '<td>',
                '<!-- left table -->',
                '<table>',
                '<tr>',
                '<td><label for="matchactive">' + _("Status") + '</label></td>',
                '<td><select class="asm-selectbox" id="matchactive" data-json="MATCHACTIVE" data-post="matchactive">',
                '<option value="0">' + _("Inactive - do not include") + '</option>',
                '<option value="1">' + _("Active") + '</option>',
                '</select></td>',
                '</tr>',
                '<tr>',
                '<td><label for="matchadded">' + _("Added") + '</label></td>',
                '<td><input type="text" class="lft asm-textbox asm-datebox" id="matchadded" data-json="MATCHADDED" data-post="matchadded" /></td>',
                '</tr>',
                '<tr>',
                '<td><label for="matchexpires">' + _("Expires") + '</label></td>',
                '<td><input type="text" class="lft asm-textbox asm-datebox" id="matchexpires" data-json="MATCHEXPIRES" data-post="matchexpires" /></td>',
                '</tr>',
                '<tr>',
                '<td><label for="matchagedfrom">' + _("Aged From") + '</label></td>',
                '<td><input type="text" class="lft asm-textbox asm-numberbox" id="agedfrom" data-json="MATCHAGEFROM" data-post="agedfrom" /></td>',
                '</tr>',
                '<tr>',
                '<td><label for="matchagedto">' + _("Aged To") + '</label></td>',
                '<td><input type="text" class="lft asm-textbox asm-numberbox" id="agedto" data-json="MATCHAGETO" data-post="agedto" /></td>',
                '</tr>',
                '<tr>',
                '<td><label for="matchcommentscontain">' + _("Comments Contain") + '</label></td>',
                '<td><textarea id="commentscontain" data-json="MATCHCOMMENTSCONTAIN" data-post="commentscontain" rows="5" maxlength="255" class="lft asm-textareafixed"></textarea></td>',
                '</tr>',
                '</table>',
                '</td>',
                '<td>',
                '<!-- right table -->',
                '<table>',
                '<tr>',
                '<td><label for="matchsex">' + _("Sex") + '</label></td>',
                '<td><select id="matchsex" data-json="MATCHSEX" data-post="matchsex" class="lfs asm-selectbox">',
                '<option value="-1">' + _("(any)") + '</option>',
                html.list_to_options(controller.sexes, "ID", "SEX"),
                '</select></td>',
                '</tr>',
                '<tr>',
                '<td><label for="matchsize">' + _("Size") + '</label></td>',
                '<td><select id="matchsize" data-json="MATCHSIZE" data-post="matchsize" class="lfs asm-selectbox">',
                '<option value="-1">' + _("(any)") + '</option>',
                html.list_to_options(controller.sizes, "ID", "SIZE"),
                '</select></td>',
                '</tr>',
                '<tr>',
                '<td><label for="matchcolour">' + _("Color") + '</label></td>',
                '<td><select id="matchcolour" data-json="MATCHCOLOUR" data-post="matchcolour" class="lfs asm-selectbox">',
                '<option value="-1">' + _("(any)") + '</option>',
                html.list_to_options(controller.colours, "ID", "BASECOLOUR"),
                '</select></td>',
                '</tr>',

                '<tr>',
                '<td><label for="matchtype">' + _("Type") + '</label></td>',
                '<td><select id="matchtype" data-json="MATCHANIMALTYPE" data-post="matchtype" class="lfs asm-selectbox">',
                '<option value="-1">' + _("(any)") + '</option>',
                html.list_to_options(controller.animaltypes, "ID", "ANIMALTYPE"),
                '</select></td>',
                '</tr>',
                '<tr>',
                '<td><label for="matchspecies">' + _("Species") + '</label></td>',
                '<td><select id="matchspecies" data-json="MATCHSPECIES" data-post="matchspecies" class="lfs asm-selectbox">',
                '<option value="-1">' + _("(any)") + '</option>',
                html.list_to_options(controller.species, "ID", "SPECIESNAME"),
                '</select></td>',
                '</tr>',
                '<tr>',
                '<td><label for="matchbreed1">' + _("Breed") + '</label></td>',
                '<td><select id="matchbreed1" data-json="MATCHBREED" data-post="matchbreed1" class="lfs asm-selectbox">',
                '<option value="-1">' + _("(any)") + '</option>',
                html.list_to_options_breeds(controller.breeds, "ID", "BREEDNAME"),
                '</select></td>',
                '</tr>',
                '<tr>',
                '<td><label for="matchbreed2">' + _("or") + '</label></td>',
                '<td><select id="matchbreed2" data-json="MATCHBREED2" data-post="matchbreed2" class="lfs asm-selectbox">',
                '<option value="-1">' + _("(any)") + '</option>',
                html.list_to_options_breeds(controller.breeds, "ID", "BREEDNAME"),
                '</select></td>',
                '</tr>',
                '</table>',
                '<!-- far right table -->',
                '</td>',
                '<td>',
                '<table>',
                '<tr>',
                '<td><label for="matchgoodwithcats">' + _("Good with cats") + '</label></td>',
                '<td><select id="matchgoodwithcats" data-json="MATCHGOODWITHCATS" data-post="matchgoodwithcats" class="lfs asm-halftextbox selectbox">',
                '<option value="-1">' + _("(any)") + '</option>',
                html.list_to_options(controller.ynun, "ID", "NAME"),
                '</select></td>',
                '</tr>',
                '<tr>',
                '<td><label for="matchgoodwithdogs">' + _("Good with dogs") + '</label></td>',
                '<td><select id="matchgoodwithdogs" data-json="MATCHGOODWITHDOGS" data-post="matchgoodwithdogs" class="lfs asm-halftextbox selectbox">',
                '<option value="-1">' + _("(any)") + '</option>',
                html.list_to_options(controller.ynun, "ID", "NAME"),
                '</select></td>',
                '</tr>',
                '',
                '<tr>',
                '<td><label for="matchgoodwithchildren">' + _("Good with children") + '</label></td>',
                '<td><select id="matchgoodwithchildren" data-json="MATCHGOODWITHCHILDREN" data-post="matchgoodwithchildren" class="lfs asm-halftextbox selectbox">',
                '<option value="-1">' + _("(any)") + '</option>',
                html.list_to_options(controller.ynun, "ID", "NAME"),
                '</select></td>',
                '</tr>',
                '<tr>',
                '<td><label for="matchhousetrained">' + _("Housetrained") + '</label></td>',
                '<td><select id="matchhousetrained" data-json="MATCHHOUSETRAINED" data-post="matchhousetrained" class="lfs asm-halftextbox selectbox">',
                '<option value="-1">' + _("(any)") + '</option>',
                html.list_to_options(controller.ynun, "ID", "NAME"),
                '</select></td>',
                '</tr>',
                '</table>',
                '<!-- end outer table -->',
                '</td>',
                '</tr>',
                '</table>',
                '</div>'
            ].join("\n");
        },

        render_toolbar: function() {
            return [
                '<div class="asm-toolbar">',
                '<table>',
                '<tr>',
                '<td><button id="button-save" title="' + _("Save this person") + '">' + html.icon("save") + ' ' + _("Save") + '</button></td>',
                '<td><button id="button-delete" title="' + _("Delete this person") + '">' + html.icon("delete") + ' ' + _("Delete") + '</button></td>',
                '<td><button id="button-merge" title="' + _("Merge another person into this one") + '">' + html.icon("copy") + ' ' + _("Merge") + '</button></td>',
                '<td><span id="button-document" title="' + _("Generate a document from this person") + '" class="asm-menu-icon">' + html.icon("document") + ' ' + _("Document") + '</span></td>',
                '<td><span id="button-diarytask" title="' + _("Create diary notes from a task") + '" class="asm-menu-icon">' + html.icon("diary-task") + ' ' + _("Diary Task") + '</span></td>',
                '<td><button id="button-map" title="' + _("Find this address on a map") + '">' + html.icon("map") + ' ' + _("Map") + '</button></td>',
                '<td><button id="button-email" title="' + _("Email this person") + '">' + html.icon("email") + ' ' + _("Email") + '</button></td>',
                '</tr>',
                '</table>',
                '</div>'
            ].join("\n");
        },

        render_submenus: function() {
            return [
                '<div id="button-document-body" class="asm-menu-body">',
                '<ul class="asm-menu-list">',
                edit_header.template_list(controller.templates, "PERSON", controller.person.ID),
                '</ul>',
                '</div>',
                '<div id="button-diarytask-body" class="asm-menu-body">',
                '<ul class="asm-menu-list">',
                edit_header.diary_task_list(controller.diarytasks, "PERSON"),
                '</ul>',
                '</div>'
            ].join("\n");
        },

        render: function() {
            return [
                person.render_submenus(),
                person.render_dialogs(),
                edit_header.person_edit_header(controller.person, "person", controller.tabcounts),
                person.render_toolbar(),
                '<div id="asm-details-accordion">',
                person.render_details(),
                person.render_type(),
                '<h3><a href="#">' + _("Additional") + '</a></h3>',
                '<div>',
                additional.additional_fields(controller.additional),
                '</div>',
                person.render_homechecker(),
                person.render_lookingfor(),
                '</div> <!-- accordion -->',
                '</div> <!-- asmcontent -->',
                '</div> <!-- tabs -->'
            ].join("\n");
        },

        enable_widgets: function() {

            // DATA ===========================================

            // If the looking for status is inactive, disable the fields
            if ($("#matchactive").val() == "0") {
                $(".lft").closest("tr").fadeOut();
                $(".lfs").closest("tr").fadeOut();
            }
            else {
                $(".lft").closest("tr").fadeIn();
                $(".lfs").closest("tr").fadeIn();
            }

            // Hide additional accordion section if there aren't
            // any additional fields declared
            var ac = $("#ui-accordion-asm-details-accordion-header-2");
            var an = ac.next();
            if (an.find(".additional").length == 0) {
                ac.hide(); an.hide();
            }

            // CONFIG ===========================
            if (config.bool("HideTownCounty")) {
                $(".towncounty").hide();
            }

            // SECURITY =============================================================

            if (!common.has_permission("co")) { $("#button-save").hide(); }
            if (!common.has_permission("do")) { $("#button-delete").hide(); }
            if (!common.has_permission("gaf")) { $("#button-document").hide(); }

            // ACCORDION ICONS =======================================================

        },

        validation: function() {

            // Remove any previous errors
            header.hide_error();
            $("label").removeClass("ui-state-error-text");

            // name
            if ($.trim($("#surname").val()) == "") {
                header.show_error(_("Name cannot be blank"));
                $("label[for='surname']").addClass("ui-state-error-text");
                $("#asm-details-accordion").accordion("option", "active", 0);
                $("#surname").focus();
                return false;
            }

            // any additional fields that are marked mandatory
            var valid = true;
            $(".additional").each(function() {
                var t = $(this);
                if (t.attr("type") != "checkbox") {
                    var d = String(t.attr("data"));
                    if (d.indexOf("a.1") != -1) {
                        if ($.trim(t.val()) == "") {
                            header.show_error(_("{0} cannot be blank").replace("{0}", d.substring(4)));
                            $("#asm-details-accordion").accordion("option", "active", 2);
                            $("label[for='" + t.attr("id") + "']").addClass("ui-state-error-text");
                            t.focus();
                            valid = false;
                            return;
                        }
                    }
                }
            });

            return valid;
        },

        get_map_url: function() {
            var add = $("#address").val().replace("\n", ",");
            var town = $("#town").val();
            var county = $("#county").val();
            var postcode = $("#postcode").val();
            var map = add;
            if (town != "") { map += "," + town; }
            if (county != "") { map += "," + county; }
            if (postcode != "") { map += "," + postcode; }
            map = encodeURIComponent(map);
            return map;
        },

        show_mini_map: function() {
            setTimeout(function() {
                mapping.draw_map("embeddedmap", 15, controller.person.LATLONG, [{ 
                    latlong: controller.person.LATLONG, popuptext: controller.person.OWNERADDRESS, popupactive: true }]);
            }, 50);
        },

        get_geocode_show_mini_map: function() {
            var p = controller.person;
            var addrhash = geo.address_hash(p.OWNERADDRESS, p.OWNERTOWN, p.OWNERCOUNTY, p.OWNERPOSTCODE);
            // Do we already have a LATLONG? If it's upto date,
            // just show the map position
            if (p.LATLONG) {
                var b = p.LATLONG.split(",");
                if (b[2] == addrhash) {
                    person.show_mini_map();
                    return;
                }
            }
            // Lookup the LATLONG and then show the map
            geo.get_lat_long(p.OWNERADDRESS, p.OWNERTOWN, p.OWNERCOUNTY, p.OWNERPOSTCODE, function(lat, lon) {
                var latlon = lat + "," + lon + "," + addrhash;
                p.LATLONG = latlon;
                $("#latlong").val(latlon);
                // We updated the latlong, rather than dirtying the form, send it to the DB
                common.ajax_post("person", "mode=latlong&personid=" + p.ID + "&latlong=" + encodeURIComponent(latlon));
                person.show_mini_map();
            });
        },

        bind: function() {

            // Load the tab strip and accordion
            $(".asm-tabbar").asmtabs();
            $("#asm-details-accordion").accordion({
                heightStyle: "content"
            }); 

            // Setup the document/diary task menu buttons
            $("#button-diarytask, #button-document").asmmenu();

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

            // If any of our additional fields need moving to other tabs, 
            // let's take care of that. Additional fields are always in pairs of
            // <td> fields, with the label containing a toX class, where toX is
            // an entry in lksfieldlink. Some tables in the form have a .additionaltarget
            // class with a data element marked toX. We reparent our .toX elements
            // to those elements.
            $(".additionaltarget").each(function() {
                var target = $(this);
                var targetname = target.attr("data");
                $(".additionalmove ." + targetname).each(function() {
                    // $(this) is the td containing the label
                    var label = $(this);
                    var item = $(this).next();
                    // For some reason, jquery gets confused if we reparent the row, so
                    // we have to add a new row to the table and then move our cells in.
                    target.append("<tr></tr>");
                    target.find("tr:last").append(label);
                    target.find("tr:last").append(item);
                });
            });

            // Diary task create ajax call
            var create_task = function(taskid) {
                var formdata = "mode=exec&id=" + $("#personid").val() + "&tasktype=PERSON&taskid=" + taskid + "&seldate=" + $("#seldate").val();
                common.ajax_post("diarytask", formdata, function() { window.location = "person_diary?id=" + $("#personid").val(); });
            };

            // Diary task select date dialog
            var addbuttons = { };
            addbuttons[_("Select")] = function() {
                var valid = true;
                var fields = [ "seldate" ];
                $.each(fields, function(i, f) {
                    if ($("#" + f).val() == "") {
                        $("label[for='" + f + "']").addClass("ui-state-error-text");
                        $("#" + f).focus();
                        valid = false;
                        return false;
                    }
                });
                if (valid) { create_task($("#diarytaskid").val()); }
            };
            addbuttons[_("Cancel")] = function() {
                $("#dialog-dt-date").dialog("close");
            };

            $("#dialog-dt-date").dialog({
                autoOpen: false,
                modal: true,
                dialogClass: "dialogshadow",
                show: dlgfx.add_show,
                hide: dlgfx.add_hide,
                buttons: addbuttons
            });

            // Attach handlers for diary tasks
            $(".diarytask").each(function() {
                var a = $(this);
                var task = a.attr("data").split(" ");
                var taskmode = task[0];
                var taskid = task[1];
                var taskneeddate = task[2];
                $(this).click(function() {
                    $("#seldate").val("");
                    // If the task needs a date, prompt for it
                    if (taskneeddate == "1") {
                        $("#diarytaskid").val(taskid);
                        $("#dialog-dt-date").dialog("open");
                    }
                    else {
                        // No need for anything else, go create the task
                        create_task(taskid);
                    }
                });
            });

            var set_membership_flag = function() {
                // Called when the membership number field is changed - if it has something
                // in it, then set the member flag
                if ($("#membershipnumber").val() != "") {
                    $("#flags option[value='member']").prop("selected", "selected");
                    $("#flags").change();
                }
            };

            var set_homechecked_flag = function() {
                $("#flags option[value='homechecked']").prop("selected", "selected");
                $("#flags").change();
            };

            $("#homecheckedby").personchooser().bind("personchooserchange", function(event, rec) {
                set_homechecked_flag();
            });

            // Controls that update the screen when changed
            $("#matchactive").change(person.enable_widgets);
            $("#homechecked").keyup(set_homechecked_flag);
            $("#homechecked").change(set_homechecked_flag);
            $("#membershipnumber").keyup(set_membership_flag).change(set_membership_flag);
            $("#membershipexpires").change(set_membership_flag);

            $("#flags").change(function() {
                // if the member flag is selected and membership number is blank,
                // default the membership number from the person id.
                if ($("#flags option[value='member']").is(":selected")) {
                    if ($.trim($("#membershipnumber").val()) == "") {
                        $("#membershipnumber").val( 
                            format.padleft($("#personid").val(), 10));
                    }
                }
            });

            validate.save = function(callback) {
                if (!person.validation()) { return; }
                validate.dirty(false);
                var formdata = "mode=save&id=" + $("#personid").val() + "&" + $("input, select, textarea").toPOST();
                common.ajax_post("person", formdata, callback);
            };

           // Toolbar buttons
            $("#button-save").button().click(function() {
                header.show_loading(_("Saving..."));
                validate.save(function() {
                    window.location="person?id=" + $("#personid").val();
                });
            });

            $("#button-delete").button().click(function() {
                var b = {}; 
                b[_("Delete")] = function() { 
                    var formdata = "mode=delete&personid=" + $("#personid").val();
                    common.ajax_post("person", formdata, function() { window.location = "main"; });
                };
                b[_("Cancel")] = function() { $(this).dialog("close"); };
                $("#dialog-delete").dialog({
                     resizable: false,
                     modal: true,
                     dialogClass: "dialogshadow",
                     show: dlgfx.delete_show,
                     hide: dlgfx.delete_hide,
                     buttons: b
                });
            });

            $("#button-merge").button().click(function() {
                var mb = {}; 
                mb[_("Merge")] = function() { 
                    var formdata = "mode=merge&personid=" + $("#personid").val() + "&mergepersonid=" + $("#mergeperson").val();
                    common.ajax_post("person", formdata, function() { window.location = "person?id=" + $("#personid").val(); });
                };
                mb[_("Cancel")] = function() { $(this).dialog("close"); };
                $("#dialog-merge").dialog({
                     width: 600,
                     resizable: false,
                     modal: true,
                     dialogClass: "dialogshadow",
                     show: dlgfx.delete_show,
                     hide: dlgfx.delete_hide,
                     buttons: mb
                });
            });

            $("#button-email").button().click(function() {
                var b = {}; 
                b[_("Send")] = function() { 
                    var formdata = "mode=email&personid=" + $("#personid").val() + "&" +
                        $("#dialog-email input, #dialog-email select, #dialog-email textarea").toPOST();
                    common.ajax_post("person", formdata, function() { 
                        header.show_info(_("Message successfully sent"));
                        $("#dialog-email").dialog("close");
                    });
                };
                b[_("Cancel")] = function() { $(this).dialog("close"); };
                $("#dialog-email").dialog({
                     resizable: false,
                     modal: true,
                     dialogClass: "dialogshadow",
                     width: 640,
                     show: dlgfx.add_show,
                     hide: dlgfx.add_hide,
                     buttons: b
                });
                var mailaddresses = [];
                var conf_org = html.decode(config.str("Organisation").replace(",", ""));
                var conf_email = config.str("EmailAddress");
                var org_email = conf_org + " <" + conf_email + ">";
                mailaddresses.push(org_email);
                $("#emailfrom").val(org_email);
                if (asm.useremail) {
                    mailaddresses.push(html.decode(asm.userreal) + " <" + asm.useremail + ">");
                }
                $("#emailfrom").autocomplete({source: mailaddresses});
                $("#emailfrom").autocomplete("widget").css("z-index", 1000);
                $("#emailto").val(html.decode($("#forenames").val() + " " + $("#surname").val()) + " <" + $("#email").val() + ">");
                var sig = config.str("EmailSignature");
                if (sig != "") {
                    $("#emailbody").val(html.decode("\n--\n" + sig));
                }
                $("#emailsubject").focus();
            });

        },

        load_person_flags: function() {

            var field_option = function(json, post, label) {
                var sel = controller.person[json] == 1 ? "selected" : "";
                return '<option value="' + post + '" ' + sel + '>' + label + '</option>\n';
            };

            var flag_option = function(flag) {
                var sel = controller.person.ADDITIONALFLAGS && controller.person.ADDITIONALFLAGS.indexOf(flag + "|") != -1 ? "selected" : "";
                return '<option ' + sel + '>' + flag + '</option>';
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

        sync: function() {

            // Load the data into the controls for the screen
            $("#asm-content input, #asm-content select, #asm-content textarea").fromJSON(controller.person);

            // Load person flags
            person.load_person_flags();

            // Load homecheck history
            var h = [];
            $.each(controller.homecheckhistory, function(i, v) {
                h.push("<tr>");
                h.push('<td class="centered">' + format.date(v.DATELASTHOMECHECKED) + '</td>');
                h.push('<td class="centered"><a class="asm-embed-name" href="person?id=' + v.ID + '">' + v.OWNERNAME + '</a></td>');
                h.push('<td class="centered">' + v.COMMENTS + '</td>');
                h.push('</tr>');
            });
            $("#homecheckhistory tbody").html(h.join("\n"));

            // Update on-screen fields from the data and display the screen
            person.enable_widgets();

            // Map button
            var map = person.get_map_url();
            var maplinkref = String(asm.maplink).replace("{0}", map);
            $("#button-map").button().click(function() {
                window.open(maplinkref, "_blank");
            });

            if (config.bool("ShowPersonMiniMap")) {
                person.get_geocode_show_mini_map();
            }

            // Dirty handling
            validate.bind_dirty();
            validate.dirty(false);
            validate.check_unsaved_links("person_");
        }

    };

    common.module(person, "person", "formtab");

});

function image_error(image) {
    image.style.display = "none";
}

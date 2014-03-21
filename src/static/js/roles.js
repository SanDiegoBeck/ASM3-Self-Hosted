/*jslint browser: true, forin: true, eqeq: true, white: true, sloppy: true, vars: true, nomen: true */
/*global $, jQuery, _, asm, common, config, controller, dlgfx, format, header, html, tableform, validate */

$(function() {

    var roles = {

        render: function() {
            var cl = function(s) { return "<p class='asm-header'>" + s + "</p>"; };
            var cr = function(token, s) { return "<input id='" + token + "' type='checkbox' class='token' /> <label for='" + token + "'>" + s + "</label><br />"; };
            var h = [
                '<div id="dialog-add" style="display: none" title="' + html.title(_("Add role")) + '">',
                '<div class="ui-state-highlight ui-corner-all" style="margin-top: 20px; padding: 0 .7em">',
                '<p><span class="ui-icon ui-icon-info" style="float: left; margin-right: .3em;"></span>',
                _("Roles need a name."),
                '</p>',
                '</div>',
                '<input type="hidden" id="roleid" />',
                '<input type="hidden" id="rolemap" />',
                '<table width="100%">',
                '<tr>',
                '<td><label for="rolename">' + _("Name") + '</label></td>',
                '<td><input id="rolename" type="text" data="rolename" class="asm-textbox" />',
                '</td>',
                '</tr>',
                '</table>',
                '<table width="100%">',
                '<tr>',
                '<td width="33%" valign="top">',
                '<p>',
                cl(_("Animals")),
                cr("aa", _("Add Animals")),
                cr("ca", _("Change Animals")),
                cr("va", _("View Animals")),
                cr("vavet", _("View Animal Vet")),
                cr("da", _("Delete Animals")),
                cr("cloa", _("Clone Animals")),
                cr("gaf", _("Generate Documents")),
                cl(_("Litters")),
                cr("all", _("Add Litter")),
                cr("vll", _("View Litter")),
                cr("cll", _("Change Litter")),
                cr("dll", _("Delete Litter")),
                cl(_("Tests")),
                cr("aat", _("Add Tests")),
                cr("vat", _("View Tests")),
                cr("cat", _("Change Tests")),
                cr("dat", _("Delete Tests")),
                cl(_("Vaccinations")),
                cr("aav", _("Add Vaccinations")),
                cr("vav", _("View Vaccinations")),
                cr("cav", _("Change Vaccinations")),
                cr("dav", _("Delete Vaccinations")),
                cr("bcav", _("Bulk Complete Vaccinations")),
                cl(_("Medical")),
                cr("maam", _("Add Medical Records")),
                cr("mvam", _("View Medical Records")),
                cr("mcam", _("Change Medical Records")),
                cr("mdam", _("Delete Medical Records")),
                cr("bcam", _("Bulk Complete Medical Records")),
                cl(_("Diets")),
                cr("daad", _("Add Diets")),
                cr("dvad", _("View Diets")),
                cr("dcad", _("Change Diets")),
                cr("ddad", _("Delete Diets")),
                cl(_("Media")),
                cr("aam", _("Add Media")),
                cr("vam", _("View Media")),
                cr("cam", _("Change Media")),
                cr("dam", _("Delete Media")),
                cl(_("Document Repository")),
                cr("ard", _("Add Document to Repository")),
                cr("vrd", _("View Document Repository")),
                cr("drd", _("Delete Document from Repository")),
                '</p>',
                '</td>',
                '<td width="33%" valign="top">',
                '<p>',
                cl(_("People")),
                cr("ao", _("Add Person")),
                cr("vo", _("View Person")),
                cr("vso", _("View Staff Person Records")),
                cr("volk", _("View Person Links")),
                cr("co", _("Change Person")),
                cr("do", _("Delete Person")),
                cl(_("Investigations")),
                cr("aoi", _("Add Investigation")),
                cr("voi", _("View Investigations")),
                cr("coi", _("Change Investigation")),
                cr("doi", _("Delete Investigation")),
                cl(_("Movements")),
                cr("aamv", _("Add Movement")),
                cr("vamv", _("View Movement")),
                cr("camv", _("Change Movement")),
                cr("damv", _("Delete Movement")),
                cl(_("Log")),
                cr("ale", _("Add Log")),
                cr("vle", _("View Log")),
                cr("cle", _("Change Log")),
                cr("dle", _("Delete Log")),
                cl(_("Diary")),
                cr("adn", _("Add Diary")),
                cr("vdn", _("View Diary")),
                cr("emdn", _("Edit My Diary Notes")),
                cr("eadn", _("Edit All Diary Notes")),
                cr("bcn", _("Bulk Complete Diary")),
                cr("ddn", _("Delete Diary")),
                cr("edt", _("Edit Diary Tasks")),
                cl(_("Lost and Found")),
                cr("ala", _("Add Lost Animal")),
                cr("vla", _("View Lost Animal")),
                cr("cla", _("Change Lost Animal")),
                cr("dla", _("Delete Lost Animal")),
                cr("afa", _("Add Found Animal")),
                cr("vfa", _("View Found Animal")),
                cr("cfa", _("Change Found Animal")),
                cr("dfa", _("Delete Found Animal")),
                cr("mlaf", _("Match Lost and Found")),
                cl(_("Waiting List")),
                cr("awl", _("Add Waiting List")),
                cr("vwl", _("View Waiting List")),
                cr("cwl", _("Change Waiting List")),
                cr("dwl", _("Delete Waiting List")),
                cr("bcwl", _("Bulk Complete Waiting List")),
                '</p>',
                '</td>',
                '<td width="33%" valign="top">',
                '<p>',
                cl(_("Accounts")),
                cr("aac", _("Add Accounts")),
                cr("vac", _("View Accounts")),
                cr("cac", _("Change Accounts")),
                cr("ctrx", _("Change Transactions")),
                cr("dac", _("Delete Accounts")),
                cl(_("Costs")),
                cr("caad", _("Add Cost")),
                cr("cvad", _("View Cost")),
                cr("ccad", _("Change Cost")),
                cr("cdad", _("Delete Cost")),
                cl(_("Donations")),
                cr("oaod", _("Add Donation")),
                cr("ovod", _("View Donation")),
                cr("ocod", _("Change Donation")),
                cr("odod", _("Delete Donation")),
                cl(_("Vouchers")),
                cr("vaov", _("Add Vouchers")),
                cr("vvov", _("View Vouchers")),
                cr("vcov", _("Change Vouchers")),
                cr("vdov", _("Delete Vouchers")),
                cl(_("System")),
                cr("asm", _("Access System Menu")),
                cr("cso", _("Change System Options")),
                cr("ml", _("Modify Lookups")),
                cr("usi", _("Use SQL Interface")),
                cr("uipb", _("Publish Animals to the Internet")),
                cr("mmeo", _("Send mass emails and perform mail merges")),
                cl(_("Online Forms")),
                cr("eof", _("Edit Online Forms")),
                cr("vif", _("View Incoming Forms")),
                cr("dif", _("Delete Incoming Forms")),
                cl(_("Users")),
                cr("asu", _("Add Users")),
                cr("esu", _("Edit Users")),
                cl(_("Reports")),
                cr("ccr", _("Add Report")),
                cr("vcr", _("View Report")),
                cr("hcr", _("Change Report")),
                cr("dcr", _("Delete Report")),
                '</p>',
                '</td>',
                '</tr>',
                '</table>',
                '</div>',

                html.content_header(_("User Roles")),

                '<div class="asm-toolbar">',
                '<button id="button-new">' + html.icon("new") + ' ' +_("New Role") + '</button>',
                '<button id="button-delete">' + html.icon("delete") + ' ' + _("Delete") + '</button>',
                '</div>',

                '<table id="table-roles">',
                '<thead>',
                '<tr>',
                '<th>' + _("Name") + '</th>',
                '</tr>',
                '</thead>',
                '<tbody>'
            ];

            $.each(controller.rows, function(i, r) {
                h.push('<tr id="rolerow-' + r.ID + '">');
                h.push('<td>');
                h.push('<span style="white-space: nowrap">');
                h.push('<input type="checkbox" data="' + r.ID + '" title="' + html.title(_('Select')) + '" />');
                h.push('<a href="#" class="role-edit-link" data="' + r.ID + '">' + r.ROLENAME + '</a>');
                h.push('</span>');
                h.push('<input class="role-name" type="hidden" value="' + html.title(r.ROLENAME) + '" />');
                h.push('<input class="role-map" type="hidden" value="' + r.SECURITYMAP + '" />');
                h.push('</td>');
                h.push('</tr>');
            });

            h.push('</tbody>');
            h.push('</table>');
            h.push(html.content_footer());
            return h.join("\n");
        },

        bind: function() {
            $("#table-roles").table();

            $("#table-roles input").change(function() {
                if ($("#table-roles input:checked").size() > 0) {
                    $("#button-delete").button("option", "disabled", false); 
                }
                else {
                    $("#button-delete").button("option", "disabled", true); 
                }
            });

            var addbuttons = { };
            addbuttons[_("Create")] = function() {
                $("#dialog-add label").removeClass("ui-state-error-text");
                if (!validate.notblank([ "rolename" ])) { return; }
                var securitymap = "";
                $(".token").each(function() {
                    if ($(this).is(":checked")) { securitymap += $(this).attr("id") + " *"; }
                });
                var formdata = "mode=create&securitymap=" + securitymap + "&" + $("#dialog-add input").toPOST();
                $("#dialog-add").disable_dialog_buttons();
                common.ajax_post("roles", formdata, function() { window.location = "roles"; }, function() { $("#dialog-add").dialog("close"); });
            };
            addbuttons[_("Cancel")] = function() {
                $("#dialog-add").dialog("close");
            };

            var editbuttons = { };
            editbuttons[_("Save")] = function() {
                $("#dialog-add label").removeClass("ui-state-error-text");
                if (!validate.notblank([ "rolename" ])) { return; }
                var securitymap = "";
                $(".token").each(function() {
                    if ($(this).is(":checked")) { securitymap += $(this).attr("id") + " *"; }
                });
                var formdata = "mode=update&roleid=" + $("#roleid").val() + "&" + 
                    "securitymap=" + securitymap + "&" +
                    $("#dialog-add input").toPOST();
                $("#dialog-add").disable_dialog_buttons();
                common.ajax_post("roles", formdata, function() { window.location = "roles"; }, function() { $("#dialog-add").dialog("close"); });
            };
            editbuttons[_("Cancel")] = function() {
                $("#dialog-add").dialog("close");
            };

            $("#dialog-add").dialog({
                autoOpen: false,
                modal: true,
                width: 900,
                height: 500,
                dialogClass: "dialogshadow",
                show: dlgfx.add_show,
                hide: dlgfx.add_hide,
                buttons: addbuttons
            });
         
            $("#button-new").button().click(function() {
               $("#dialog-add .asm-textbox").val("");
               $("#dialog-add input:checkbox").attr("checked", false);
               $("#dialog-add label").removeClass("ui-state-error-text");
               $("#dialog-add").dialog("option", "buttons", addbuttons);
               $("#dialog-add").dialog("option", "title", _("Add role"));
               $("#dialog-add").dialog("open"); 
            });

            $("#button-delete").button({disabled: true}).click(function() {
                tableform.delete_dialog(function() {
                    var formdata = "mode=delete&ids=";
                    $("#table-roles input").each(function() {
                        if ($(this).attr("type") == "checkbox") {
                            if ($(this).is(":checked")) {
                                formdata += $(this).attr("data") + ",";
                            }
                        }
                    });
                    $("#dialog-delete").disable_dialog_buttons();
                    common.ajax_post("roles", formdata, function() { window.location = "roles"; }, function() { $("#dialog-add").dialog("close"); });
                },
                _("This will permanently remove the selected roles, are you sure?")
                );
            });

            $(".role-edit-link")
            .click(function() {
                var rid = $(this).attr("data");
                var rrow = "#rolerow-" + rid + " ";
                $("#dialog-add label").removeClass("ui-state-error-text");
                $("#roleid").val($(this).attr("data"));
                $("#rolename").val($(rrow + ".role-name").val());
                var perms = $(rrow + ".role-map").val().replace(/\*/g, "").split(" ");
                $(".token").attr("checked", false);
                $.each(perms, function(i, v) {
                    $("#" + v).prop("checked", true);
                });
                $("#dialog-add").dialog("option", "buttons", editbuttons);
                $("#dialog-add").dialog("option", "title", _("Edit role"));
                $("#dialog-add").dialog("open");
                return false; // prevents # href
            });

        }
    };

    common.module(roles, "roles", "options");

});

/*jslint browser: true, forin: true, eqeq: true, white: true, sloppy: true, vars: true, nomen: true */
/*global $, jQuery, _, asm, common, config, controller, dlgfx, format, header, html, tableform, validate */

$(function() {

    var users = {};

    var dialog = {
        add_title: _("Add user"),
        edit_title: _("Edit user"),
        helper_text: _("Users need a username, password and at least one role or the superuser flag setting."),
        close_on_ok: true,
        hide_read_only: true,
        columns: 1,
        width: 550,
        fields: [
            { json_field: "USERNAME", post_field: "username", label: _("Username"), type: "text", validation: "notblank", readonly: true },
            { json_field: "PASSWORD", post_field: "password", label: _("Password"), type: "text", readonly: true },
            { json_field: "REALNAME", post_field: "realname", label: _("Real name"), type: "text" },
            { json_field: "EMAILADDRESS", post_field: "email", label: _("Email"), type: "text" },
            { json_field: "SUPERUSER", post_field: "superuser", label: _("Type"),  type: "select", defaultval: 0, options: 
                '<option value="0">' + _("Normal user") + '</option>' +
                '<option value="1">' + _("Super user") + '</option>'},
            { json_field: "ROLEIDS", post_field: "roles", label: _("Roles"), type: "selectmulti", 
                options: { rows: controller.roles, valuefield: "ID", displayfield: "ROLENAME" }},
            { json_field: "OWNERID", post_field: "person", label: _("Staff record"), type: "person", personfilter: "staff" },
            { json_field: "LOCATIONFILTER", post_field: "locationfilter", label: _("Location Filter"), type: "selectmulti", 
                options: { rows: controller.internallocations, valuefield: "ID", displayfield: "LOCATIONNAME" }},
            { type: "raw", label: "", markup: html.info(_("Setting a location filter will prevent this user seeing animals who are not in these locations on shelterview, find animal and search."))
            },
            { json_field: "IPRESTRICTION", post_field: "iprestriction", label: _("IP Restriction"), type: "textarea", classes: "asm-ipbox" },
            { type: "raw", label: "", markup: html.info(_("IP restriction is a space-separated list of IP netblocks in CIDR notation that this user is *only* permitted to login from (eg: 192.168.0.0/24 127.0.0.0/8). If left blank, the user can login from any address."))
            }
        ]
    };

    var table = {
        rows: controller.rows,
        idcolumn: "ID",
        edit: function(row) {
            if (row.USERNAME == asm.useraccount) { return false; }
            tableform.dialog_show_edit(dialog, row, function() {
                tableform.fields_update_row(dialog.fields, row);
                users.set_extra_fields(row);
                tableform.fields_post(dialog.fields, "mode=update&userid=" + row.ID, "systemusers", function(response) {
                    tableform.table_update(table);
                });
            });
        },
        columns: [
            { field: "USERNAME", display: _("Username"), initialsort: true, formatter: function(row) {
                    if (row.USERNAME == asm.useraccount) {
                        return row.USERNAME;
                    }
                    return "<span style=\"white-space: nowrap\">" +
                        "<input type=\"checkbox\" data-id=\"" + row.ID + "\" title=\"" + html.title(_("Select")) + "\" />" +
                        "<a href=\"#\" class=\"link-edit\" data-id=\"" + row.ID + "\">" + row.USERNAME + "</a>" +
                        "</span>";
                }},
            { field: "REALNAME", display: _("Real name"), formatter: function(row) {
                    if (row.USERNAME == asm.useraccount) { 
                        return _("(master user, not editable)");
                    }
                    if (row.REALNAME) {                        
                        return row.REALNAME;
                    }
                    return "";
                }},
            { field: "EMAILADDRESS", display: _("Email") },
            { field: "ROLES", display: _("Roles"), formatter: function(row) {
                    return common.nulltostr(row.ROLES).replace(/[|]+/g, ", ");
                }},
            { field: "SUPERUSER", display: _("Superuser"), formatter: function(row) {
                    if (row.SUPERUSER == 1) {
                        return _("Yes");
                    }
                    return _("No");
                }},
            { field: "IPRESTRICTION", display: _("IP Restriction") }
        ]
    };

    var buttons = [
         { id: "new", text: _("New User"), icon: "new", enabled: "always", 
             click: function() { 
                 tableform.dialog_show_add(dialog, function() {
                     tableform.fields_post(dialog.fields, "mode=create", "systemusers", function(response) {
                         var row = {};
                         row.ID = response;
                         tableform.fields_update_row(dialog.fields, row);
                         users.set_extra_fields(row);
                         controller.rows.push(row);
                         tableform.table_update(table);
                     });
                 });
             } 
         },
         { id: "delete", text: _("Delete"), icon: "delete", enabled: "multi", 
             click: function() { 
                 tableform.delete_dialog(function() {
                     tableform.buttons_default_state(buttons);
                     var ids = tableform.table_ids(table);
                     common.ajax_post("systemusers", "mode=delete&ids=" + ids , function() {
                         tableform.table_remove_selected_from_json(table, controller.rows);
                         tableform.table_update(table);
                     });
                 });
             } 
         },
         { id: "reset", text: _("Reset Password"), icon: "auth", enabled: "multi", 
             click: function() { 
                 var ids = tableform.table_ids(table);
                 common.ajax_post("systemusers", "mode=reset&ids=" + ids , function() {
                     var h = "";
                     $("#tableform input:checked").each(function() {
                        var username = $(this).next().text();
                        $(this).prop("checked", false);
                        h += _("Password for '{0}' has been reset to default of 'password'").replace("{0}", username) + "<br />";
                     });
                     header.show_info(h);
                 });
             } 
         }
    ];

    users = {

        render: function() {
            var s = "";
            s += tableform.dialog_render(dialog);
            s += html.content_header(_("User Accounts"));
            s += tableform.buttons_render(buttons);
            s += tableform.table_render(table);
            s += html.content_footer();
            return s;
        },

        bind: function() {
            tableform.dialog_bind(dialog);
            tableform.buttons_bind(buttons);
            tableform.table_bind(table, buttons);
        },

        set_extra_fields: function(row) {
            // Build list of ROLES from ROLEIDS
            var roles = [];
            var roleids = row.ROLEIDS;
            if ($.isArray(roleids)) { roleids = roleids.join(","); }
            $.each(roleids.split(/[|,]+/), function(i, v) {
                roles.push(common.get_field(controller.roles, v, "ROLENAME"));
            });
            row.ROLES = roles.join("|");
        }

    };
    
    common.module(users, "users", "options");

});

/*jslint browser: true, forin: true, eqeq: true, white: true, sloppy: true, vars: true, nomen: true */
/*global $, jQuery, _, asm, common, config, controller, dlgfx, format, header, html, tableform, validate */

$(function() {

    var onlineform = {};
    var fieldtypes = [
        { "ID": 0, "NAME": _("Yes/No") },
        { "ID": 1, "NAME": _("Text") },
        { "ID": 2, "NAME": _("Notes") },
        { "ID": 3, "NAME": _("Lookup") }
    ];

    var dialog = {
        add_title: _("Add form field"),
        edit_title: _("Edit form field"),
        helper_text: _("Online form fields need a name and label."),
        close_on_ok: true,
        columns: 1,
        width: 550,
        fields: [
            { json_field: "FIELDNAME", post_field: "fieldname", label: _("Name"), type: "text", validation: "notblank" }, 
            { json_field: "FIELDTYPE", post_field: "fieldtype", label: _("Type"), type: "select", options: {
                valuefield: "ID", displayfield: "NAME", 
                rows: fieldtypes }},
            { json_field: "LABEL", post_field: "label", label: _("Label"), type: "text", validation: "notblank" }, 
            { json_field: "DISPLAYINDEX", post_field: "displayindex", label: _("Display Index"), type: "number" }, 
            { json_field: "LOOKUPS", post_field: "lookups", label: _("Lookups"), type: "textarea" }, 
            { json_field: "TOOLTIP", post_field: "tooltip", label: _("Tooltip"), type: "textarea" }
        ]
    };

    var table = {
        rows: controller.rows,
        idcolumn: "ID",
        edit: function(row) {
            tableform.dialog_show_edit(dialog, row, function() {
                tableform.fields_update_row(dialog.fields, row);
                tableform.fields_post(dialog.fields, "mode=update&formfieldid=" + row.ID, "onlineform", function(response) {
                    tableform.table_update(table);
                });
            }, function() { onlineform.check_lookups(); });
        },
        columns: [
            { field: "FIELDNAME", display: _("Name") },
            { field: "DISPLAYINDEX", display: _("Display Index"), initialsort: true },
            { field: "FIELDTYPE", display: _("Type"), formatter: function(row) {
                return common.get_field(fieldtypes, row.FIELDTYPE, "NAME");
            }},
            { field: "LABEL", display: _("Label") }
        ]
    };

    var buttons = [
         { id: "new", text: _("New form field"), icon: "new", enabled: "always", 
             click: function() { 
                 tableform.dialog_show_add(dialog, function() {
                     tableform.fields_post(dialog.fields, "mode=create&formid=" + controller.formid, "onlineform", function(response) {
                         var row = {};
                         row.ID = response;
                         tableform.fields_update_row(dialog.fields, row);
                         controller.rows.push(row);
                         tableform.table_update(table);
                     });
                 }, function() { onlineform.check_lookups(); });
             } 
         },
         { id: "delete", text: _("Delete"), icon: "delete", enabled: "multi", 
             click: function() { 
                 tableform.delete_dialog(function() {
                     tableform.buttons_default_state(buttons);
                     var ids = tableform.table_ids(table);
                     common.ajax_post("onlineform", "mode=delete&ids=" + ids , function() {
                         tableform.table_remove_selected_from_json(table, controller.rows);
                         tableform.table_update(table);
                     });
                 });
             } 
         }
         /*
         { id: "back", text: _("Back"), icon: "back", enabled: "always", click: function() {
             window.location = "onlineforms";
         }}
         */
    ];

    onlineform = {

        /** Check if we should show the lookups row (only
          * valid if the field type is lookup)
          */
        check_lookups: function() {
            var ft = $("#fieldtype").select("value");
            if (ft == 3) {
                $("#lookups").closest("tr").fadeIn();
            }
            else {
                $("#lookups").closest("tr").fadeOut();
            }
        },

        render: function() {
            var s = "";
            s += tableform.dialog_render(dialog);
            s += html.content_header(_("Online Form: {0}").replace("{0}", controller.formname));
            s += tableform.buttons_render(buttons);
            s += tableform.table_render(table);
            s += html.content_footer();
            return s;
        },

        bind: function() {
            tableform.dialog_bind(dialog);
            tableform.buttons_bind(buttons);
            tableform.table_bind(table, buttons);

            // Stop users entering a space in the fieldname box
            $("#fieldname").keydown(function (e) {
                if (e.keyCode == 32) { return false; }
            });

            // Show/hide the lookup values box if type changes
            $("#fieldtype").change(this.check_lookups);

            // Prompt with our recognised fields in the autocomplete
            $("#fieldname").autocomplete({ source: controller.formfields }); 
            // Fix for JQuery UI 10.3, autocomplete has to be created after the dialog is
            // shown or the stacking order is wrong. This fixes it now.
            $("#fieldname").autocomplete("widget").css("z-index", 1000);

        }

    };

    common.module(onlineform, "onlineform", "formtab");

});

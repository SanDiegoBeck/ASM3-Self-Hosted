/*jslint browser: true, forin: true, eqeq: true, white: true, sloppy: true, vars: true, nomen: true */
/*global $, jQuery, _, asm, common, config, controller, dlgfx, format, header, html, tableform, validate */

$(function() {

    var dialog = {
        add_title: _("New template"),
        helper_text: _("Template names can include a path portion with /, eg: Vets/Rabies Certificate"),
        close_on_ok: true,
        columns: 1,
        width: 550,
        fields: [
            { post_field: "template", label: _("Template Name"), validation: "notblank", type: "text" }
        ]
    };

    var table = {
        rows: controller.rows,
        idcolumn: "ID",
        edit: function(row) {
            window.location = "document_edit?template=" + row.ID;
        },
        columns: [
            { field: "NAME", display: _("Template") },
            { field: "PATH", display: _("Path"), initialsort: true }
        ]
    };

    var buttons = [
         { id: "new", text: _("New"), icon: "new", tooltip: _("Create a new template"), enabled: "always", 
             click: function() { 
                 tableform.dialog_show_add(dialog, function() {
                     tableform.fields_post(dialog.fields, "mode=create", "document_templates", function(response) {
                         window.location="document_edit?template=" + response;
                     });
                 });
             } 
         },
         { id: "clone", text: _("Clone"), icon: "copy", tooltip: _("Create a new template by copying the selected template"), enabled: "one", 
             click: function() { 
                 var ids = tableform.table_ids(table);
                 tableform.dialog_show_add(dialog, function() {
                     tableform.fields_post(dialog.fields, "mode=clone&ids=" + ids , "document_templates", function(response) {
                         window.location="document_edit?template=" + response;
                     });
                 });
             } 
         },
         { id: "delete", text: _("Delete"), icon: "delete", enabled: "multi", 
             click: function() { 
                 tableform.delete_dialog(function() {
                     tableform.buttons_default_state(buttons);
                     var ids = tableform.table_ids(table);
                     common.ajax_post("document_templates", "mode=delete&ids=" + ids , function() {
                         tableform.table_remove_selected_from_json(table, controller.rows);
                         tableform.table_update(table);
                     });
                 });
             } 
         }
    ];

    var document_templates = {

        render: function() {
            var s = "";
            s += tableform.dialog_render(dialog);
            s += html.content_header(_("Document Templates"));
            s += tableform.buttons_render(buttons);
            s += tableform.table_render(table);
            s += html.content_footer();
            return s;
        },

        bind: function() {
            tableform.dialog_bind(dialog);
            tableform.buttons_bind(buttons);
            tableform.table_bind(table, buttons);
        }

    };

    common.module(document_templates, "document_templates", "options");

});

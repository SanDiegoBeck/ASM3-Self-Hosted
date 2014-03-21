/*jslint browser: true, forin: true, eqeq: true, white: true, sloppy: true, vars: true, nomen: true */
/*global $, jQuery, _, asm, common, config, controller, dlgfx, format, header, html, tableform, validate */

$(function() {

    var medicalprofile = {};

    var dialog = {
        add_title: _("Add medical profile"),
        edit_title: _("Edit medical profile"),
        helper_text: _("Medical profiles need a profile name, treatment, dosage and frequencies."),
        close_on_ok: true,
        columns: 1,
        width: 800,
        fields: [
            { json_field: "PROFILENAME", post_field: "profilename", label: _("Profile"), type: "text", validation: "notblank" },
            { json_field: "TREATMENTNAME", post_field: "treatmentname", label: _("Name"), type: "text", validation: "notblank" },
            { json_field: "DOSAGE", post_field: "dosage", label: _("Dosage"), type: "text", validation: "notblank" },
            { json_field: "COST", post_field: "cost", label: _("Cost"), type: "currency" },
            { json_field: "STATUS", post_field: "status", label: _("Status"), type: "select",
                options: '<option value="0">' + _("Active") + '</option><option value="1">' 
                    + _("Held") + '</option><option value="2">' + _("Completed") + '</option>' },
            { post_field: "singlemulti", label: _("Frequency"), type: "select",  
                options: '<option value="0">' + _("Single Treatment") + '</option>' +
                '<option value="1" selected="selected">' + _("Multiple Treatments") + '</option>' },
            { type: "raw", justwidget: true, markup: "<tr><td></td><td>" },
            { json_field: "TIMINGRULE", post_field: "timingrule", type: "number", justwidget: true, halfsize: true, defaultval: "1" },
            { type: "raw", justwidget: true, markup: " " + _("treatments, every") + " " },
            { json_field: "TIMINGRULENOFREQUENCIES", post_field: "timingrulenofrequencies", type: "number", justwidget: true, halfsize: true, defaultval: "1" },
            { type: "raw", justwidget: true, markup: " " },
            { json_field: "TIMINGRULEFREQUENCY", post_field: "timingrulefrequency", type: "select", justwidget: true, halfsize: true, options: 
                    '<option value="0">' + _("days") + '</option>' + 
                    '<option value="1">' + _("weeks") + '</option>' +
                    '<option value="2">' + _("months") + '</option>' + 
                    '<option value="3">' + _("years") + '</option>' },
            { type: "raw", justwidget: true, markup: "</td></tr>" },
            { type: "raw", justwidget: true, markup: "<tr><td>" + _("Duration") + "</td><td>" },
            { json_field: "TREATMENTRULE", post_field: "treatmentrule", justwidget: true, type: "select", halfsize: true, options:
                    '<option value="0">' + _("Ends after") + '</option>' +
                    '<option value="1">' + _("Unspecified") + '</option>' },
            { type: "raw", justwidget: true, markup: " " },
            { json_field: "TOTALNUMBEROFTREATMENTS", post_field: "totalnumberoftreatments", justwidget: true, halfsize: true, type: "number", defaultval: "1" },
            { type: "raw", justwidget: true, markup:
                ' <span id="timingrulefrequencyagain">' + _("days") + '</span> ' +
                '(<span id="displaytotalnumberoftreatments">0</span> ' + _("treatments") + ')' +
                '</span>' +
                '</td></tr>'},
            { json_field: "COMMENTS", post_field: "comments", label: _("Comments"), type: "textarea" }
        ]
    };

    var table = {
        rows: controller.rows,
        idcolumn: "ID",
        edit: function(row) {
            tableform.fields_populate_from_json(dialog.fields, row);
            if (row.TIMINGRULE == 0) {
                $("#singlemulti").select("value", "0");
            }
            else {
                $("#singlemulti").select("value", "1");
            }
            medicalprofile.change_singlemulti();
            medicalprofile.change_values();
            tableform.dialog_show_edit(dialog, row, function() {
                tableform.fields_update_row(dialog.fields, row);
                medicalprofile.set_extra_fields(row);
                tableform.fields_post(dialog.fields, "mode=update&profileid=" + row.ID, "medicalprofile", function(response) {
                    tableform.table_update(table);
                    tableform.dialog_close();
                },
                function(response) {
                    tableform.dialog_error(response);
                    tableform.dialog_enable_buttons();
                });
            });
        },
        columns: [
            { field: "PROFILENAME", display: _("Name"), initialsort: true },
            { field: "TREATMENTNAME", display: _("Treatment") },
            { field: "DOSAGE", display: _("Dosage") },
            { field: "COST", display: _("Cost"), formatter: tableform.format_currency },
            { field: "NAMEDFREQUENCY", display: _("Frequency") },
            { field: "COMMENTS", display: _("Comments") }
        ]
    };

    var buttons = [
        { id: "new", text: _("New Profile"), icon: "new", enabled: "always", 
             click: function() { medicalprofile.new_medicalprofile(); }},
         { id: "delete", text: _("Delete"), icon: "delete", enabled: "multi", 
             click: function() { 
                 tableform.delete_dialog(function() {
                     tableform.buttons_default_state(buttons);
                     var ids = tableform.table_ids(table);
                     common.ajax_post(controller.name, "mode=delete&ids=" + ids , function() {
                         tableform.table_remove_selected_from_json(table, controller.rows);
                         tableform.table_update(table);
                     });
                 });
             } 
         }
    ];

    medicalprofile = {

        render: function() {
            var s = "";
            s += tableform.dialog_render(dialog);
            s += html.content_header(_("Medical Profiles"));
            s += tableform.buttons_render(buttons);
            s += tableform.table_render(table);
            s += html.content_footer();
            return s;
        },

        new_medicalprofile: function() { 
            $("#dialog-tableform .asm-textbox, #dialog-tableform .asm-textarea").val("");
            tableform.dialog_show_add(dialog, function() {
                tableform.fields_post(dialog.fields, "mode=create", "medicalprofile", function(response) {
                    window.location = "medicalprofile";
                    /** Medical profile has too much server side logic when creating, reload the form
                    var row = {};
                    row.ID = response;
                    tableform.fields_update_row(dialog.fields, row);
                    medical.set_extra_fields(row);
                    controller.rows.push(row);
                    tableform.table_update(table);
                    tableform.dialog_close();
                    */
                }, function() {
                    tableform.dialog_enable_buttons();   
                });
            });
        },

        /* What to do when we switch between single/multiple treatments */
        change_singlemulti: function() {
            if ($("#singlemulti").val() == 0) {
                $("#timingrule").val("1");
                $("#timingrulenofrequencies").val("1");
                $("#timingrulefrequency").select("value", "0");
                $("#timingrulefrequency").select("disable");
                $("#treatmentrule").select("value", "0");
                $("#treatmentrule").select("disable");
                $("#totalnumberoftreatments").val("1");

                $("#timingrule").closest("tr").fadeOut();
                $("#treatmentrule").closest("tr").fadeOut();
            }
            else {
                $("#timingrule").val("1");
                $("#timingrulenofrequencies").val("1");
                $("#timingrulefrequency").select("value", "0");
                $("#timingrulefrequency").select("enable");
                $("#treatmentrule").select("value", "0");
                $("#treatmentrule").select("enable");
                $("#totalnumberoftreatments").val("1");

                $("#timingrule").closest("tr").fadeIn();
                $("#treatmentrule").closest("tr").fadeIn();
            }
        },

        /* Recalculate ends after period and update screen*/
        change_values: function() {
            if ($("#treatmentrule").val() == "0") {
                $("#displaytotalnumberoftreatments").text( parseInt($("#timingrule").val(), 10) * parseInt($("#totalnumberoftreatments").val(), 10));
                $("#timingrulefrequencyagain").text($("#timingrulefrequency option[value=\"" + $("#timingrulefrequency").val() + "\"]").text());
            }
        },

        bind: function() {
            $(".asm-tabbar").asmtabs();
            tableform.dialog_bind(dialog);
            tableform.buttons_bind(buttons);
            tableform.table_bind(table, buttons);

            $("#singlemulti").change(function() {
                medicalprofile.change_singlemulti();
            });

            $("#treatmentrule").change(function() {
                if ($("#treatmentrule").val() == "1") {
                    $("#treatmentrulecalc").fadeOut();
                }
                else {
                    $("#treatmentrulecalc").fadeIn();
                    medicalprofile.change_values();
                }
            });

            $("#timingrule").change(medicalprofile.change_values);
            $("#timingrulefrequency").change(medicalprofile.change_values);
            $("#timingrulenofrequencies").change(medicalprofile.change_values);
            $("#treatmentrule").change(medicalprofile.change_values);
            $("#totalnumberoftreatments").change(medicalprofile.change_values);

        },

        sync: function() {
        },

        set_extra_fields: function(row) {
        }
    };

    common.module(medicalprofile, "medicalprofile", "book");

});

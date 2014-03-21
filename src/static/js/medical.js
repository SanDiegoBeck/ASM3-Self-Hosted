/*jslint browser: true, forin: true, eqeq: true, white: true, sloppy: true, vars: true, nomen: true */
/*global $, jQuery, _, asm, common, config, controller, dlgfx, edit_header, format, header, html, tableform, validate */

$(function() {

    var medical = {}, lastanimal;

    var dialog = {
        add_title: _("Add medical regimen"),
        edit_title: _("Edit medical regimen"),
        helper_text: _("Medical regimens need an animal, name, dosage, a start date and frequencies."),
        close_on_ok: true,
        autofocus: false,
        hide_read_only: true,
        columns: 1,
        width: 800,
        fields: [
            { json_field: "ANIMALID", post_field: "animal", label: _("Animal"), type: "animal", validation: "notzero" },
            { json_field: "MEDICALPROFILEID", post_field: "profileid", label:_("Profile"), type: "select",
                options: '<option value="0"></option>' +
                html.list_to_options(controller.profiles, "ID", "PROFILENAME") },
            { json_field: "TREATMENTNAME", post_field: "treatmentname", label: _("Name"), type: "text", validation: "notblank" },
            { json_field: "DOSAGE", post_field: "dosage", label: _("Dosage"), type: "text", validation: "notblank" },
            { json_field: "COST", post_field: "cost", label: _("Cost"), type: "currency" },
            { json_field: "STARTDATE", post_field: "startdate", label: _("Start Date"), type: "date", validation: "notblank" },
            { json_field: "STATUS", post_field: "status", label: _("Status"), type: "select",
                options: '<option value="0">' + _("Active") + '</option><option value="1">' 
                    + _("Held") + '</option><option value="2">' + _("Completed") + '</option>' },
            { post_field: "singlemulti", label: _("Frequency"), type: "select", readonly: true, 
                options: '<option value="0">' + _("Single Treatment") + '</option>' +
                '<option value="1" selected="selected">' + _("Multiple Treatments") + '</option>' },
            { type: "raw", justwidget: true, markup: "<tr><td></td><td>" },
            { json_field: "TIMINGRULE", post_field: "timingrule", type: "number", readonly: true, justwidget: true, halfsize: true, defaultval: "1" },
            { type: "raw", justwidget: true, markup: " " + _("treatments, every") + " " },
            { json_field: "TIMINGRULENOFREQUENCIES", post_field: "timingrulenofrequencies", type: "number", justwidget: true, halfsize: true, readonly: true, defaultval: "1" },
            { type: "raw", justwidget: true, markup: " " },
            { json_field: "TIMINGRULEFREQUENCY", post_field: "timingrulefrequency", type: "select", justwidget: true, halfsize: true, readonly: true, options: 
                    '<option value="0">' + _("days") + '</option>' + 
                    '<option value="1">' + _("weeks") + '</option>' +
                    '<option value="2">' + _("months") + '</option>' + 
                    '<option value="3">' + _("years") + '</option>' },
            { type: "raw", justwidget: true, markup: "</td></tr>" },
            { type: "raw", justwidget: true, markup: "<tr><td>" + _("Duration") + "</td><td>" },
            { json_field: "TREATMENTRULE", post_field: "treatmentrule", justwidget: true, type: "select", halfsize: true, readonly: true, options:
                    '<option value="0">' + _("Ends after") + '</option>' +
                    '<option value="1">' + _("Unspecified") + '</option>' },
            { type: "raw", justwidget: true, markup: " " },
            { json_field: "TOTALNUMBEROFTREATMENTS", post_field: "totalnumberoftreatments", justwidget: true, halfsize: true, type: "number", readonly: true, defaultval: "1" },
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
        idcolumn: "COMPOSITEID",
        edit: function(row) {
            if (controller.animal) {
                $("#animal").closest("tr").hide();
            }
            $("#profileid").closest("tr").hide();
            $("#treatmentrulecalc").hide();
            $("#status").closest("tr").show();
            tableform.fields_populate_from_json(dialog.fields, row);
            tableform.dialog_show_edit(dialog, row, function() {
                tableform.fields_update_row(dialog.fields, row);
                medical.set_extra_fields(row);
                tableform.fields_post(dialog.fields, "mode=update&regimenid=" + row.REGIMENID, controller.name, function(response) {
                    tableform.table_update(table);
                    tableform.dialog_close();
                },
                function(response) {
                    tableform.dialog_error(response);
                    tableform.dialog_enable_buttons();
                });
            });
        },
        complete: function(row) {
            if (row.DATEGIVEN || row.STATUS == 2) { return true; }
            return false;
        },
        overdue: function(row) {
            return !row.DATEGIVEN && row.STATUS == 0 && format.date_js(row.DATEREQUIRED) < common.today_no_time();
        },
        columns: [
            { field: "TREATMENTNAME", display: _("Name") },
            { field: "IMAGE", display: "", 
                formatter: function(row) {
                    return '<a href="animal?id=' + row.ANIMALID + '"><img src=' + html.thumbnail_src(row, "animalthumb") + ' style="margin-right: 8px" class="asm-thumbnail" /></a>';
                },
                hideif: function(row) {
                    // Don't show this column if we're in an animal record, or the option is turned off
                    if (controller.animal || !config.bool("PicturesInBooks")) {
                        return true;
                    }
                }
            },
            { field: "ANIMAL", display: _("Animal"), 
                formatter: function(row) {
                    return '<a href="animal?id=' + row.ANIMALID + '">' + row.ANIMALNAME + ' - ' + row.SHELTERCODE + '</a>';
                },
                hideif: function(row) {
                    // Don't show for animal records
                    if (controller.animal) { return true; }
                }
            },
            { field: "LOCATIONNAME", display: _("Location"),
                formatter: function(row) {
                    var s = row.LOCATIONNAME;
                    if (row.LOCATIONUNIT) {
                        s += ' <span class="asm-search-locationunit">' + row.LOCATIONUNIT + '</span>';
                    }
                    return s;
                },
                hideif: function(row) {
                     // Don't show for animal records
                    if (controller.animal) { return true; }
                }
            },
            { field: "DOSAGE", display: _("Dosage") },
            { field: "STARTDATE", display: _("Started"), formatter: tableform.format_date },
            { field: "NAMEDSTATUS", display: _("Status"), formatter: function(row) {
                return row.NAMEDSTATUS + ", " + row.NAMEDFREQUENCY + " " + html.icon("right") + " " + row.NAMEDNUMBEROFTREATMENTS +
                    " (" + row.TREATMENTNUMBER + "/" + row.TOTALTREATMENTS + ")";
            }},
            { field: "COST", display: _("Cost"), formatter: tableform.format_currency },
            { field: "DATEREQUIRED", display: _("Required"), formatter: tableform.format_date, initialsort: true },
            { field: "DATEGIVEN", display: _("Given"), formatter: tableform.format_date },
            { field: "GIVENBY", display: _("By") },
            { field: "COMMENTS", display: _("Comments") }
        ]
    };

    var buttons = [
        { id: "new", text: _("New Regimen"), icon: "new", enabled: "always", 
             click: function() { medical.new_medical(); }},
         { id: "delete-regimens", text: _("Delete Regimen"), icon: "delete", enabled: "multi", 
             mouseover: function() {
                medical.highlight_selected_regimens(true);
             },
             mouseleave: function() {
                medical.highlight_selected_regimens(false);
             },
             click: function() { 
                 tableform.delete_dialog(function() {
                     tableform.buttons_default_state(buttons);
                     var ids = medical.selected_regimen_ids();
                     common.ajax_post(controller.name, "mode=delete_regimen&ids=" + ids , function() {
                         medical.remove_selected_regimens();
                         tableform.table_update(table);
                     });
                 });
             } 
         },
         { id: "delete-treatments", text: _("Delete Treatments"), icon: "delete", enabled: "multi", 
             mouseover: function() {
                medical.highlight_selected_treatments(true);
             },
             mouseleave: function() {
                medical.highlight_selected_treatments(false);
             },
             click: function() { 
                 tableform.delete_dialog(function() {
                     tableform.buttons_default_state(buttons);
                     var ids = medical.selected_treatment_ids();
                     common.ajax_post(controller.name, "mode=delete_treatment&ids=" + ids , function() {
                         medical.remove_selected_treatments();
                         tableform.table_update(table);
                     });
                 });
             } 
         },
         { id: "given", text: _("Give"), icon: "complete", enabled: "multi", 
             tooltip: _("Mark treatments given"),
             click: function() {
                $("#newdate").datepicker("setDate", new Date());
                $("#dialog-given").dialog("open");
             }
         },
         { id: "required", text: _("Change Date Required"), icon: "calendar", enabled: "multi", 
             tooltip: _("Change date required on selected treatments"),
             click: function() {
                $("#newdater").datepicker("setDate", new Date());
                $("#dialog-required").dialog("open");
             }
         },

         { id: "offset", type: "dropdownfilter", 
             options: [ "m31|" + _("Due today"), "p7|" + _("Due in next week"), "p31|" + _("Due in next month"), "p365|" + _("Due in next year") ],
             click: function(selval) {
                window.location = controller.name + "?offset=" + selval;
             },
             hideif: function(row) {
                 // Don't show for animal records
                 if (controller.animal) {
                     return true;
                 }
             }
         }
    ];

    medical = {

        render: function() {
            var s = "";
            s += tableform.dialog_render(dialog);
            s += medical.render_givendialog();
            s += medical.render_requireddialog();
            if (controller.animal) {
                s += edit_header.animal_edit_header(controller.animal, "medical", controller.tabcounts);
            }
            else {
                s += html.content_header(_("Medical Book"));
            }
            s += tableform.buttons_render(buttons);
            s += tableform.table_render(table);
            s += html.content_footer();
            return s;
        },


        /** Removes selected treatments from the local json */
        remove_selected_treatments: function() {
             var seltreat = this.selected_treatment_ids().split(",");
             var i = 0, v;
             for (i = controller.rows.length - 1; i >= 0; i = i-1) {
                 v = controller.rows[i];
                 if ($.inArray(String(v.TREATMENTID), seltreat) != -1) {
                     controller.rows.splice(i, 1);
                 }
             }
        },

        /** Removes treatments in the selected regimens from the local json */
        remove_selected_regimens: function() {
             var selreg = this.selected_regimen_ids().split(",");
             var i = 0, v;
             for (i = controller.rows.length - 1; i >= 0; i = i-1) {
                 v = controller.rows[i];
                 if ($.inArray(String(v.REGIMENID), selreg) != -1) {
                     controller.rows.splice(i, 1);
                 }
             }
        },

        /** Returns a comma separated list of selected regimen ids */
        selected_regimen_ids: function() {
             var selreg = [];
             $.each(controller.rows, function(i, v) {
                if (tableform.table_id_selected(v.COMPOSITEID)) {
                    selreg.push(v.REGIMENID);
                }
             });
             return selreg.join(",");
        },

        /** Returns a comma separated list of selected treatment ids */
        selected_treatment_ids: function() {
             var seltreat = [];
             $.each(controller.rows, function(i, v) {
                if (tableform.table_id_selected(v.COMPOSITEID)) {
                    seltreat.push(v.TREATMENTID);
                }
             });
             return seltreat.join(",");
        },

        /** Puts a red border around the rows of all treatments in the selected regimens, 
         * unless enable is false, when it will be removed */
        highlight_selected_regimens: function(enable) {
             var selreg = this.selected_regimen_ids().split(",");
             var bval = "1px solid red";
             if (!enable) { bval = ""; }
             $.each(controller.rows, function(i, v) {
                 if ($.inArray(String(v.REGIMENID), selreg) != -1) {
                     $("[data-id='" + v.COMPOSITEID + "']").closest("tr").find("td").css({ border: bval });
                 }
             });
        },

        /** Puts a red border around the rows of all selected treatments,
         * unless enable is false, when it will be removed */
        highlight_selected_treatments: function(enable) {
             var seltreat = this.selected_treatment_ids().split(",");
             var bval = "1px solid red";
             if (!enable) { bval = ""; }
             $.each(controller.rows, function(i, v) {
                 if ($.inArray(String(v.TREATMENTID), seltreat) != -1) {
                     $("[data-id='" + v.COMPOSITEID + "']").closest("tr").find("td").css({ border: bval });
                 }
             });
        },

        new_medical: function() { 
            if (controller.animal) {
                $("#animal").animalchooser("loadbyid", controller.animal.ID);
                $("#animal").closest("tr").hide();
            }
            else {
                $("#animal").animalchooser("clear");
            }
            $("#dialog-tableform .asm-textbox, #dialog-tableform .asm-textarea").val("");
            $("#profileid").closest("tr").show();
            $("#treatmentrulecalc").show();
            $("#status").closest("tr").hide();
            tableform.dialog_show_add(dialog, function() {
                tableform.dialog_disable_buttons();   
                tableform.fields_post(dialog.fields, "mode=create", controller.name, function(response) {
                    if (controller.animal) {
                        window.location = controller.name + "?id=" + controller.animal.ID;
                    }
                    else {
                        window.location = controller.name + "?offset=" + $("#offset").val();
                    }
                    /** Medical has too much server side logic when creating, reload the form
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

        render_givendialog: function() {
            return [
                '<div id="dialog-given" style="display: none" title="' + html.title(_("Give Treatments")) + '">',
                '<table width="100%">',
                '<tr>',
                '<td><label for="newdate">' + _("Given") + '</label></td>',
                '<td><input id="newdate" data="newdate" type="textbox" class="asm-textbox asm-datebox" /></td>',
                '</tr>',
                '</table>',
                '</div>'
            ].join("\n");
        },

        bind_givendialog: function() {

            var givenbuttons = { };
            givenbuttons[_("Save")] = function() {
                $("#dialog-given label").removeClass("ui-state-error-text");
                if (!validate.notblank([ "newdate" ])) { return; }
                $("#dialog-given").disable_dialog_buttons();
                var ids = medical.selected_treatment_ids();
                var newdate = encodeURIComponent($("#newdate").val());
                common.ajax_post(controller.name, "mode=given&newdate=" + newdate + "&ids=" + ids , function() {
                    $.each(controller.rows, function(i, v) {
                        if (tableform.table_id_selected(v.COMPOSITEID)) {
                            v.DATEGIVEN = format.date_iso($("#newdate").val());
                            if (!v.GIVENBY) { v.GIVENBY = asm.user; }
                        }
                    });
                    tableform.table_update(table);
                    $("#dialog-given").dialog("close");
                    $("#dialog-given").enable_dialog_buttons();
                });
            };
            givenbuttons[_("Cancel")] = function() {
                $("#dialog-given").dialog("close");
            };

            $("#dialog-given").dialog({
                autoOpen: false,
                width: 550,
                modal: true,
                dialogClass: "dialogshadow",
                show: dlgfx.edit_show,
                hide: dlgfx.edit_hide,
                buttons: givenbuttons
            });

        },

        render_requireddialog: function() {
            return [
                '<div id="dialog-required" style="display: none" title="' + html.title(_("Change Date Required")) + '">',
                '<table width="100%">',
                '<tr>',
                '<td><label for="newdater">' + _("Required") + '</label></td>',
                '<td><input id="newdater" data="newdater" type="textbox" class="asm-textbox asm-datebox" /></td>',
                '</tr>',
                '</table>',
                '</div>'
            ].join("\n");
        },

        bind_requireddialog: function() {

            var requiredbuttons = { };
            requiredbuttons[_("Save")] = function() {
                $("#dialog-required label").removeClass("ui-state-error-text");
                if (!validate.notblank([ "newdater" ])) { return; }
                $("#dialog-required").disable_dialog_buttons();
                var ids = medical.selected_treatment_ids();
                var newdate = encodeURIComponent($("#newdater").val());
                common.ajax_post(controller.name, "mode=required&newdate=" + newdate + "&ids=" + ids , function() {
                    $.each(controller.rows, function(i, v) {
                        if (tableform.table_id_selected(v.COMPOSITEID)) {
                            v.DATEREQUIRED = format.date_iso($("#newdater").val());
                        }
                    });
                    tableform.table_update(table);
                    $("#dialog-required").dialog("close");
                    $("#dialog-required").enable_dialog_buttons();
                });
            };
            requiredbuttons[_("Cancel")] = function() {
                $("#dialog-required").dialog("close");
            };

            $("#dialog-required").dialog({
                autoOpen: false,
                width: 550,
                modal: true,
                dialogClass: "dialogshadow",
                show: dlgfx.edit_show,
                hide: dlgfx.edit_hide,
                buttons: requiredbuttons
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
            this.bind_givendialog();
            this.bind_requireddialog();

            // Remember the currently selected animal when it changes so we can add
            // its name and code to the local set
            $("#animal").bind("animalchooserchange", function(event, rec) { lastanimal = rec; });
            $("#animal").bind("animalchooserloaded", function(event, rec) { lastanimal = rec; });

            $("#singlemulti").change(function() {
                medical.change_singlemulti();
            });

            $("#treatmentrule").change(function() {
                if ($("#treatmentrule").val() == "1") {
                    $("#treatmentrulecalc").fadeOut();
                }
                else {
                    $("#treatmentrulecalc").fadeIn();
                    medical.change_values();
                }
            });

            if ($("#profileid option").length == 1) {
                $("#profilerow").hide();
            }

            $("#profileid").change(function() {
                if ($("#profileid").val() == "0") { return; }
                var formdata = "mode=get_profile&profileid=" + $("#profileid").val();
                common.ajax_post("medical", formdata, function(result) {
                    var p = jQuery.parseJSON(result)[0];
                    $("#treatmentname").val( html.decode(p.TREATMENTNAME));
                    $("#dosage").val( html.decode(p.DOSAGE) );
                    $("#cost").currency("value", p.COST );
                    $("#comments").val( html.decode(p.COMMENTS) );
                    $("#totalnumberoftreatments").val( p.TOTALNUMBEROFTREATMENTS );
                    $("#singlemulti").val( p.TOTALNUMBEROFTREATMENTS == 1 ? "0" : "1" );
                    medical.change_singlemulti();
                    $("#timingrule").val( p.TIMINGRULE );
                    $("#timingrulenofrequencies").val( p.TIMINGRULENOFREQUENCIES );
                    $("#timingrulefrequency").val( p.TIMINGRULEFREQUENCY );
                    $("#treatmentrule").val( p.TREATMENTRULE );
                    $("#totalnumberoftreatments").val( p.TOTALNUMBEROFTREATMENTS );
                    medical.change_values();
                });
            });

            $("#timingrule").change(medical.change_values);
            $("#timingrulefrequency").change(medical.change_values);
            $("#timingrulenofrequencies").change(medical.change_values);
            $("#treatmentrule").change(medical.change_values);
            $("#totalnumberoftreatments").change(medical.change_values);

            if (controller.newmed == 1) {
                this.new_medical();
            }
        },

        sync: function() {
            // If an offset is given in the querystring, update the select
            if (common.current_url().indexOf("offset=") != -1) {
                var offurl = common.current_url().substring(common.current_url().indexOf("=")+1);
                $("#offset").select("value", offurl);
            }
        },

        set_extra_fields: function(row) {
            if (controller.animal) {
                row.LOCATIONUNIT = controller.animal.SHELTERLOCATIONUNIT;
                row.LOCATIONNAME = controller.animal.SHELTERLOCATIONNAME;
                row.ANIMALNAME = controller.animal.ANIMALNAME;
                row.SHELTERCODE = controller.animal.SHELTERCODE;
                row.WEBSITEMEDIANAME = controller.animal.WEBSITEMEDIANAME;
            }
            else if (lastanimal) {
                row.LOCATIONUNIT = lastanimal.SHELTERLOCATIONUNIT;
                row.LOCATIONNAME = lastanimal.SHELTERLOCATIONNAME;
                row.ANIMALNAME = lastanimal.ANIMALNAME;
                row.SHELTERCODE = lastanimal.SHELTERCODE;
                row.WEBSITEMEDIANAME = lastanimal.WEBSITEMEDIANAME;
            }
        }
    };

    common.module(medical, "medical", common.current_url().indexOf("medical") == 0 ? "book" : "formtab");

});

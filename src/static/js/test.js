/*jslint browser: true, forin: true, eqeq: true, white: true, sloppy: true, vars: true, nomen: true */
/*global $, jQuery, _, asm, common, config, controller, dlgfx, edit_header, format, header, html, tableform, validate */

$(function() {

    var test = {}, lastanimal;

    var dialog = {
        add_title: _("Add test"),
        edit_title: _("Edit test"),
        helper_text: _("Tests need an animal and at least a required date."),
        close_on_ok: true,
        autofocus: false,
        use_default_values: false,
        columns: 1,
        width: 500,
        fields: [
            { json_field: "ANIMALID", post_field: "animal", label: _("Animal"), type: "animal", validation: "notzero" },
            { json_field: "TESTTYPEID", post_field: "type", label: _("Type"), type: "select", 
                options: { displayfield: "TESTNAME", valuefield: "ID", rows: controller.testtypes }},
            { json_field: "DATEREQUIRED", post_field: "required", label: _("Required"), type: "date", validation: "notblank" },
            { json_field: "DATEOFTEST", post_field: "given", label: _("Performed"), type: "date" },
            { json_field: "TESTRESULTID", post_field: "result", label: _("Result"), type: "select", 
                options: { displayfield: "RESULTNAME", valuefield: "ID", rows: controller.testresults }},
            { json_field: "COST", post_field: "cost", label: _("Cost"), type: "currency" },
            { json_field: "COMMENTS", post_field: "comments", label: _("Comments"), type: "textarea" }
        ]
    };

    var table = {
        rows: controller.rows,
        idcolumn: "ID",
        edit: function(row) {
            if (controller.animal) {
                $("#animal").closest("tr").hide();
            }
            test.enable_default_cost = false;
            tableform.fields_populate_from_json(dialog.fields, row);
            test.enable_default_cost = true;
            tableform.dialog_show_edit(dialog, row, function() {
                tableform.fields_update_row(dialog.fields, row);
                test.set_extra_fields(row);
                tableform.fields_post(dialog.fields, "mode=update&testid=" + row.ID, controller.name, function(response) {
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
            if (row.DATEOFTEST) { return true; }
            return false;
        },
        overdue: function(row) {
            return !row.DATEOFTEST && format.date_js(row.DATEREQUIRED) < common.today_no_time();
        },
        columns: [
            { field: "TESTNAME", display: _("Type") },
            { field: "IMAGE", display: "", 
                formatter: function(row) {
                    return '<a href="animal?id=' + row.ANIMALID + '"><img src=' + html.thumbnail_src(row, "animalthumb") + ' style="margin-right: 8px" class="asm-thumbnail thumbnailshadow" /></a>';
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
            { field: "DATEREQUIRED", display: _("Required"), formatter: tableform.format_date, initialsort: true },
            { field: "DATEOFTEST", display: _("Performed"), formatter: tableform.format_date },
            { field: "RESULTNAME", display: _("Result"), formatter: function(row) {
                    if (row.DATEOFTEST) {
                        return row.RESULTNAME;
                    }
                    return "";
                }},
            { field: "COST", display: _("Cost"), formatter: tableform.format_currency },
            { field: "COMMENTS", display: _("Comments") }
        ]
    };

    var buttons = [
        { id: "new", text: _("New Test"), icon: "new", enabled: "always", 
             click: function() { test.new_test(); }},
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

    test = {

        render: function() {
            var s = "";
            s += tableform.dialog_render(dialog);
            if (controller.animal) {
                s += edit_header.animal_edit_header(controller.animal, "test", controller.tabcounts);
            }
            else {
                s += html.content_header(_("Test Book"));
            }
            s += tableform.buttons_render(buttons);
            s += tableform.table_render(table);
            s += html.content_footer();
            return s;
        },

        new_test: function() { 
            if (controller.animal) {
                $("#animal").animalchooser("loadbyid", controller.animal.ID);
                $("#animal").closest("tr").hide();
            }
            else {
                $("#animal").animalchooser("clear");
            }
            $("#dialog-tableform .asm-textbox, #dialog-tableform .asm-textarea").val("");
            $("#type").select("value", config.str("AFDefaultTestType"));
            test.enable_default_cost = true;
            test.set_default_cost();
            tableform.dialog_show_add(dialog, function() {
                tableform.fields_post(dialog.fields, "mode=create", controller.name, function(response) {
                    var row = {};
                    row.ID = response;
                    tableform.fields_update_row(dialog.fields, row);
                    test.set_extra_fields(row);
                    controller.rows.push(row);
                    tableform.table_update(table);
                    tableform.dialog_close();
                }, function() {
                    tableform.dialog_enable_buttons();   
                });
            });
        },

        bind: function() {
            $(".asm-tabbar").asmtabs();
            tableform.dialog_bind(dialog);
            tableform.buttons_bind(buttons);
            tableform.table_bind(table, buttons);

            // When the test type is changed, use the default cost from the test type
            $("#type").change(test.set_default_cost);

            // Remember the currently selected animal when it changes so we can add
            // its name and code to the local set
            $("#animal").bind("animalchooserchange", function(event, rec) { lastanimal = rec; });
            $("#animal").bind("animalchooserloaded", function(event, rec) { lastanimal = rec; });

            if (controller.newtest == 1) {
                this.new_test();
            }
        },

        sync: function() {
            // If an offset is given in the querystring, update the select
            if (common.current_url().indexOf("offset=") != -1) {
                var offurl = common.current_url().substring(common.current_url().indexOf("=")+1);
                $("#offset").select("value", offurl);
            }
        },

        /** Whether or not we should allow overwriting of the cost */
        enable_default_cost: true,

        /** Sets the default cost based on the selected test type */
        set_default_cost: function() {
            if (!test.enable_default_cost) { return; }
            var seltype = $("#type").val();
            $.each(controller.testtypes, function(i, v) {
                if (seltype == v.ID) {
                    if (v.DEFAULTCOST) {
                        $("#cost").currency("value", v.DEFAULTCOST);
                    }
                    else {
                        $("#cost").currency("value", 0);
                    }
                    return true;
                }
            });
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
            row.TESTNAME = common.get_field(controller.testtypes, row.TESTTYPEID, "TESTNAME");
            row.RESULTNAME = common.get_field(controller.testresults, row.TESTRESULTID, "RESULTNAME");
        }
    };
    
    common.module(test, "test", controller.animal ? "formtab" : "book");

});

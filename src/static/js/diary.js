/*jslint browser: true, forin: true, eqeq: true, white: true, sloppy: true, vars: true, nomen: true */
/*global $, jQuery, _, asm, common, config, controller, dlgfx, edit_header, format, header, html, tableform, validate */

$(function() {

    var diary = {};

    var dialog = {
        add_title: _("Add diary"),
        edit_title: _("Edit diary"),
        helper_text: _("Diary notes need a date and subject.") + "<br />" + 
            _("Times should be in HH:MM format, eg: 09:00, 16:30"),
        close_on_ok: true,
        columns: 1,
        width: 500,
        fields: [
            { json_field: "DIARYFORNAME", post_field: "diaryfor", label: _("For"), type: "select", 
                options: { rows: controller.forlist, displayfield: "USERNAME", valuefield: "USERNAME" }},
            { json_field: "DIARYDATETIME", post_field: "diarydate", label: _("Date"), type: "date", validation: "notblank", defaultval: new Date() },
            { json_field: "DIARYDATETIME", post_field: "diarytime", label: _("Time"), type: "time" },
            { json_field: "DATECOMPLETED", post_field: "completed", label: _("Completed"), type: "date" },
            { json_field: "SUBJECT", label: _("Subject"), post_field: "subject", validation: "notblank", type: "text" },
            { json_field: "NOTE", label: _("Note"), post_field: "note", validation: "notblank", type: "textarea" },
            { json_field: "COMMENTS", label: _("Comments"), post_field: "comments", type: "textarea" }
        ]
    };

    var table = {
        rows: controller.rows,
        idcolumn: "ID",
        edit: function(row) {
            tableform.fields_populate_from_json(dialog.fields, row);
            tableform.dialog_show_edit(dialog, row, function() {
                tableform.fields_update_row(dialog.fields, row);
                tableform.fields_post(dialog.fields, "mode=update&diaryid=" + row.ID, controller.name, function(response) {
                    tableform.table_update(table);
                    tableform.dialog_close();
                },
                function(response) {
                    tableform.dialog_error(response);
                    tableform.dialog_enable_buttons();
                });
            }, function(row) {
               
                // If this is the my/all diary note screen, and the user is not a 
                // superuser and not the person who created the diary note, they
                // should only be able to edit the comments.
                if ((controller.name.indexOf("diary_edit") == 0) && (row.CREATEDBY != asm.user) && (!asm.superuser)) {
                    $("#subjecttext").remove();
                    $("#notetext").remove();
                    $("#note").closest("span").hide();
                    $("#subject").hide();
                    $("#note").closest("td").append("<span id='notetext'>" + row.NOTE + "</span>");
                    $("#subject").closest("td").append("<span id='subjecttext'>" + row.SUBJECT + "</span>");
                }
                else {
                    $("#subjecttext").remove();
                    $("#notetext").remove();
                    $("#subject").show();
                    $("#note").closest("span").show();
                }

                // Allow editing of the comments once the diary is created
                $("#comments").closest("tr").show();
            });
        },
        complete: function(row) {
            if (row.DATECOMPLETED) { return true; }
            return false;
        },
        overdue: function(row) {
            return !row.DATECOMPLETED && format.date_js(row.DIARYDATETIME) < common.today_no_time();
        },
        columns: [
            { field: "DIARYFORNAME", display: _("For") },
            { field: "DIARYDATETIME", display: _("Date"), formatter: tableform.format_datetime, initialsort: true, initialsortdirection: "desc" },
            { field: "DATECOMPLETED", display: _("Completed"), formatter: tableform.format_date },
            { field: "LINKINFO", display: _("Link"), 
                formatter: function(row) {
                    var link = "#";
                    if (row.LINKTYPE == 1) { link = "animal?id=" + row.LINKID; }
                    if (row.LINKTYPE == 2) { link = "person?id=" + row.LINKID; }
                    if (row.LINKTYPE == 3) { link = "lostanimal?id=" + row.LINKID; }
                    if (row.LINKTYPE == 4) { link = "foundanimal?id=" + row.LINKID; }
                    if (row.LINKTYPE == 5) { link = "waitinglist?id=" + row.LINKID; }
                    if (link != "#") { return '<a href="' + link + '">' + row.LINKINFO + '</a>'; }
                    return row.LINKINFO;
                },
                hideif: function() {
                    return common.current_url().indexOf("diary_edit") == -1;
                }
            },
            { field: "SUBJECT", display: _("Subject") },
            { field: "NOTE", display: _("Note") },
            { field: "CREATEDBY", display: _("By") }
        ]
    };

    var buttons = [
         { id: "new", text: _("New Diary"), icon: "new", enabled: "always", click: function() { 
             diary.new_note();
         }},
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
         { id: "complete", text: _("Complete"), icon: "complete", enabled: "multi", 
             click: function() { 
                 var ids = tableform.table_ids(table);
                 common.ajax_post(controller.name, "mode=complete&ids=" + ids, function() {
                     $.each(controller.rows, function(i, v) {
                        if (tableform.table_id_selected(v.ID)) {
                            v.DATECOMPLETED = format.date_iso(new Date());
                        }
                     });
                     tableform.table_update(table);
                 });
             } 
         },
         { id: "filter", type: "dropdownfilter", 
             options: [ "uncompleted|" + _("Incomplete notes upto today"),
                "completed|" + _("Completed notes upto today"),
                "all|" + _("All notes upto today"),
                "future|" + _("Future notes")
                ],
             hideif: function() {
                return common.current_url().indexOf("diary_edit") == -1;
             },
             click: function(selval) {
                window.location = controller.name + "?filter=" + selval;
             }
         }
    ];

    diary = {

        set_extra_fields: function(row) {
            row.CREATEDBY = asm.user;
        },

        render: function() {
            var h = [];
            h.push(tableform.dialog_render(dialog));
            if (controller.name == "animal_diary") {
                h.push(edit_header.animal_edit_header(controller.animal, "log", controller.tabcounts));
            }
            else if (controller.name == "person_diary") {
                h.push(edit_header.person_edit_header(controller.person, "log", controller.tabcounts));
            }
            else if (controller.name == "waitinglist_diary") {
                h.push(edit_header.waitinglist_edit_header(controller.animal, "log", controller.tabcounts));
            }
            else if (controller.name == "lostanimal_diary") {
                h.push(edit_header.lostfound_edit_header("lost", controller.animal, "log", controller.tabcounts));
            }
            else if (controller.name == "foundanimal_diary") {
                h.push(edit_header.lostfound_edit_header("found", controller.animal, "log", controller.tabcounts));
            }
            else if (controller.name == "diary_edit") {
                h.push(html.content_header(_("Edit diary notes")));
            }
            else if (controller.name == "diary_edit_my") {
                h.push(html.content_header(_("Edit my  diary notes")));
            }
            h.push(tableform.buttons_render(buttons));
            h.push(tableform.table_render(table));
            h.push(html.content_footer());
            return h.join("\n");
        },

        bind: function() {
            $(".asm-tabbar").asmtabs();
            tableform.dialog_bind(dialog);
            tableform.buttons_bind(buttons);
            tableform.table_bind(table, buttons);
        },

        sync: function() {
            // If a filter is given in the querystring, update the select
            if (common.current_url().indexOf("filter=") != -1) {
                var filterurl = common.current_url().substring(common.current_url().indexOf("filter=")+7);
                $("#filter").select("value", filterurl);
            }

            if (controller.newnote) {
                diary.new_note();
            }
        },

        new_note: function() {
            tableform.dialog_show_add(dialog, function() {
                tableform.fields_post(dialog.fields, "mode=create&linkid=" + controller.linkid, controller.name, function(response) {
                    var row = {};
                    row.ID = response;
                    tableform.fields_update_row(dialog.fields, row);
                    diary.set_extra_fields(row);
                    controller.rows.push(row);
                    tableform.table_update(table);
                    tableform.dialog_close();
                }, function() {

                    tableform.dialog_enable_buttons(); 

                    // Show the note textarea and subject box and remove any old text display of notes
                    $("#notetext").remove();
                    $("#subjecttext").remove();
                    $("#note").closest("span").show();
                    $("#subject").show();

                    // Hide the comments field for new diary notes
                    $("#comments").closest("tr").hide();
                });
            });
        }
    };

    common.module(diary, "diary", common.current_url().indexOf("diary_edit") != -1 ? "book" : "formtab");

});

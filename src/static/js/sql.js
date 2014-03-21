/*jslint browser: true, forin: true, eqeq: true, white: true, sloppy: true, vars: true, nomen: true */
/*global $, jQuery, _, asm, common, config, controller, dlgfx, format, header, html, tableform, validate */

$(function() {

    var sql = {

        render: function() {
            return [
                html.content_header(_("SQL Interface")),
                '<div id="dialog-dump" class="hidden" title="' + html.title(_("Confirm")) + '">',
                _("This can take some time and generate a large file, are you sure?") + '</div>',
                '<div class="asm-toolbar">',
                tableform.buttons_render([
                    { id: "exec", text: _("Execute"), tooltip: _("Execute the SQL in the box below"), icon: "sql" },
                    { id: "export", text: _("Export"), tooltip: _("Export this database in various formats"), icon: "database",
                        type: "buttonmenu", 
                    options: [ 
                        "dumpsql|" + _("SQL dump"), 
                        "dumpsqlnomedia|" + _("SQL dump (without media)"),
                        // ASM2_COMPATIBILITY
                        "dumpsqlasm2|" + _("SQL dump (ASM2 HSQLDB Format)"),
                        "dumpsqlasm2nomedia|" + _("SQL dump (ASM2 HSQLDB Format, without media)"),
                        "animalcsv|" + _("CSV of animal/adopter data"), 
                        "personcsv|" + _("CSV of person data") ]}
                ], true),
                '<span style="float: right">',
                '<label for="tables">' + _("Table") + '</label>',
                '<select id="tables" data="table" class="asm-selectbox">',
                '<option></option>',
                sql.render_table_options(),
                '</select>',
                '<label for="columns">' + _("Column") + '</label>',
                '<select id="columns" class="asm-selectbox">',
                '</select>',
                '</span>',
                '</div>',
                '<textarea id="sql" class="asm-textarea" style="font-family: monospace" data="sql" rows="10"></textarea>',
                '<hr />',
                '<form id="sqlfileform" action="sql" method="post" enctype="multipart/form-data">',
                '<input name="mode" value="execfile" type="hidden" />',
                '<label for="sqlfile">' + _("Or upload a script") + ' <input id="sqlfile" type="file" name="sqlfile" />',
                '<button id="button-submitfile" type="button">' + html.icon("sql") + ' ' + _("Execute Script") + '</button>',
                '</form>',
                '<table id="sql-results"></table>',
                html.content_footer()
            ].join("\n");
        },

        render_table_options: function() {
            var h = [];
            $.each(controller.tables, function(i, v) {
                h.push("<option>" + v + "</option>");
            });
            return h.join("\n");
        },

        /** One of the three dump button choices so once the confirm dialog has been agreed
         *  to, we know where to redirect to
         */
        dumpchoice: "dumpsql",

        bind: function() {
            $("#tables").change(function() {
                var formdata = "mode=cols&" + $("#tables").toPOST();
                header.show_loading(_("Loading..."));
                common.ajax_post("sql", formdata, function(result) { 
                    var cols = result.split("|");
                    var h = "<option></option>";
                    $.each(cols, function(i, v) {
                        h += "<option>" + v + "</option>";
                    });
                    $("#columns").html(h);
                }, function() {
                    $("#button-exec").button("enable");
                });
            });

            $("#columns").change(function() {
                $("#sql").val( $("#sql").val() + $("#columns").val() + ", " );
            });

            $("#button-submitfile").button().click(function() {
                if ($("#sqlfile").val() != "") {
                    $("#sqlfileform").submit();
                }
            });

            var dbuttons = {};
            dbuttons[_("Yes")] = function() {
                $(this).dialog("close");
                window.location = "sql?mode=" + sql.dumpchoice;
            };
            dbuttons[_("No")] = function() {
                $(this).dialog("close");
            };

            var confirm_dump = function(action) {
                sql.dumpchoice = action;
                $("#dialog-dump").dialog({ 
                    autoOpen: true,
                    modal: true,
                    dialogClass: "dialogshadow",
                    show: dlgfx.add_show,
                    hide: dlgfx.add_hide,
                    buttons: dbuttons 
                });
            };

            // Handles all export menu clicks by passing the action on to confirm_dump
            $("#button-export").asmmenu();
            $("#button-export-body a").click(function() {
                confirm_dump($(this).attr("data"));
                return false;
            });

            $("#button-exec").button().click(function() {
                var formdata = "mode=exec&" + $("#sql").toPOST();
                $("#button-exec").button("disable");
                header.show_loading(_("Executing..."));
                common.ajax_post("sql", formdata, function(result) { 
                    if (result.indexOf("<thead") == 0) {
                        $("#sql-results").html(result);
                        $("#sql-results").table();
                        $("#sql-results").fadeIn();
                        var norecs = String($("#sql-results tr").length - 1);
                        header.show_info(_("{0} results.").replace("{0}", norecs));
                    }
                    else {
                        $("#sql-results").fadeOut();
                        if (result != "") {
                            header.show_info(result);
                        }
                        else {
                            header.show_info(_("No results."));
                        }
                    }
                    $("#button-exec").button("enable");
                }, function() {
                    $("#button-exec").button("enable");
                });
            });
        }
    };

    common.module(sql, "sql", "options");

});

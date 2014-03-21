/*jslint browser: true, forin: true, eqeq: true, plusplus: true, white: true, sloppy: true, vars: true, nomen: true */
/*global $, console, jQuery */
/*global asm, common, dlgfx, format, html, validate, header, _, escape, unescape */
/*global tableform: true */

(function($) {

    tableform = {

        /**
         * Renders a toolbar button set. If notoolbar is true, just renders the button tags, otherwise
         * wraps them in a toolbar div.
         *
         * buttons: [
         *      { id: "new", text: _("Text"), tooltip: _("Tooltip"), icon: "iconname", enabled: "always|multi|one", hideif: function() {}, click: tableform.click_delete }
         *      { id: "buttonmenu", type: "buttonmenu", text: _("Text"), tooltip: _("Tooltip"), icon: "iconname", enabled: "always|multi|one", 
         *          hideif: function() {}, click: function(selval) {}}
         *      { id: "dropdownfilter", type: "dropdownfilter", options: [ "value1|text1", "value2|text2" ] }
         *      { type: "raw", markup: "<span>" }
         * ]
         */
        buttons_render: function(buttons, notoolbar) {
            var b = "";
            if (!notoolbar) {
                b += "<div class=\"asm-toolbar\">";
            }
            $.each(buttons, function(i, v) {
                if (v.hideif && v.hideif()) { return; }
                if (!v.type || v.type == "button") {
                    b += "<button id=\"button-" + v.id + "\" title=\"" + html.title(v.tooltip) + "\">" + html.icon(v.icon);
                    if (v.text) {
                        b += " " + v.text;
                    }
                    b += "</button>";
                }
                else if (v.type == "raw") {
                    b += v.markup;
                }
                else if (v.type == "dropdownfilter") {
                    b += '<span style="float: right"><select id="' + v.id + '" title="' + html.title(v.tooltip) + '" class="asm-selectbox">';
                    if (common.is_array(v.options)) {
                        // If v.options is a  list, then assume
                        // either value|label or just value for only one item.
                        $.each(v.options, function(io, vo) {
                            var opt = vo.split("|");
                            var val, label;
                            val = opt[0];
                            if (opt.length > 1) {
                                label = opt[1];
                            }
                            else {
                                label = opt[0];
                            }
                            b += '<option value="' + val + '">' + label + '</option>';
                        });
                    }
                    // Assume v.options is a string 
                    else {
                        b += v.options;
                    }

                    b += '</select></span>';
                }
                else if (v.type == "buttonmenu") {
                    b += '<span id="button-' + v.id + '" class="asm-menu-icon" title="' + html.title(v.tooltip) + '">' + html.icon(v.icon);
                    if (v.text) {
                        b += " " + v.text;
                    }
                    b += '</span>';
                    // If no options are supplied, don't create the menu body
                    if (v.options) {
                        var menu = '<div id="button-' + v.id + '-body" class="asm-menu-body"><ul class="asm-menu-list">';
                        $.each(v.options, function(io, vo) {
                            var opt = vo.split("|");
                            var val, label;
                            val = opt[0];
                            if (opt.length > 1) {
                                label = opt[1];
                            }
                            else {
                                label = opt[0];
                            }
                            menu += '<li class="asm-menu-item"><a href="#" data="' + val + '">' + label + '</a></li>';
                        });
                        menu += '</ul></div>';
                        $("body").prepend(menu);
                    }
                }
                b += " ";
            });
            if (!notoolbar) {
                b += "</div>";
            }
            return b;
        },

        /**
         * Binds events to a toolbar button set
         *
         * buttons: [
         *      { id: "new", text: _("Text"), tooltip: _("Tooltip"), icon: "iconname", enabled: "always|multi|one", click: tableform.click_delete, mouseover: function(e), mouseleave: function(e) }
         * ]
         */
        buttons_bind: function(buttons) {
            $.each(buttons, function(i, v) {
                if (!v.type || v.type == "button") {
                    $("#button-" + v.id).button();
                    if (v.click) { $("#button-" + v.id).click(v.click); }
                    if (v.mouseover) { $("#button-" + v.id).mouseover(v.mouseover); }
                    if (v.mouseleave) { $("#button-" + v.id).mouseleave(v.mouseleave); }
                    if (v.enabled != "always") { $("#button-" + v.id).button("disable"); }
                }
                else if (v.type == "buttonmenu") {
                    $("#button-" + v.id).asmmenu();
                    $("#button-" + v.id + "-body a").each(function() {
                        if (v.click) {
                            var dataval = $(this).attr("data");
                            $(this).click(function() {
                                v.click(dataval);
                                return false;
                            });
                        }
                    });
                    if (v.enabled != "always") {
                        $("#button-" + v.id).addClass("ui-state-disabled").addClass("ui-button-disabled");
                    }
                }
                else if (v.type == "dropdownfilter") {
                    $("#" + v.id).change(function() {
                        if (v.click) {
                            v.click($("#" + v.id).val());
                        }
                    });
                }
            });
        },

        /**
         * Resets the default state of any toolbar buttons
         */
        buttons_default_state: function(buttons) {
            $.each(buttons, function(i, v) {
                if (!v.type || v.type == "button") {
                    $("#button-" + v.id).button("enable");
                    if (v.enabled != "always") { $("#button-" + v.id).button("disable"); }
                }
                else if (v.type == "buttonmenu") {
                    if (v.enabled != "always") { 
                        $("#button-" + v.id).addClass("ui-state-disabled").addClass("ui-button-disabled");
                    }
                }
            });
        },

        /** Formats a value as a currency */
        format_currency: function(row, v) {
            return format.currency(v);
        },

        /** Formats a value as a date */
        format_date: function(row, v) {
            return format.date(v);
        },

        /** Formats a value as a date and time */
        format_datetime: function(row, v) {
            return format.date(v) + " " + format.time(v);
        },

        /** Formats a value as a string */
        format_string: function(row, v) {
            if (!v) { return ""; }
            return String(v);
        },

        /**
         * Renders a table
         *
         * formatter function is called for every value to display it
         * hideif is called for every column and row. If true is returned, the
         * column is not displayed.
         *
         * table = { rows: {json containing rows}, 
         *   idcolumn: "ID",
         *   edit: function(row) { callback for when a row is edited with the row data }
         *   complete: function(row) { return true if the row should be drawn as complete },
         *   overdue: function(row) { return true if the row should be drawn as overdue },
         *   columns:  [
         *      { initialsort: true, initialsortdirection: "asc", field: "jsonfield", display: _("Text"), formatter: tableform.format_date, hideif: function(row) } 
         *   ]
         *
         * bodyonly: If you only want the tbody contents, set this to true
         */
        table_render: function(table, bodyonly) {
            var t = [];
            if (!bodyonly) {
                t.push("<table id=\"tableform\" width=\"100%\"><thead><tr>");
                $.each(table.columns, function(i, v) {
                    if (v.hideif && v.hideif()) { return; }
                    t.push("<th>" + v.display + "</th>");
                });
                t.push("</tr><thead><tbody>");
            }
            $.each(table.rows, function(ir, vr) {
                if (table.hideif && table.hideif(vr)) { return; }
                var rowid = vr[table.idcolumn];
                t.push("<tr id=\"row-" + rowid + "\">");
                $.each(table.columns, function(ic, vc) {
                    var formatter = vc.formatter;
                    if (vc.hideif && vc.hideif(vr)) { return; }
                    var extraclasses = "";
                    if (table.complete) {
                        if (table.complete(vr)) {
                            extraclasses += " asm-completerow";
                        }
                    }
                    if (table.overdue) {
                        if (table.overdue(vr)) {
                            extraclasses += " asm-overduerow";
                        }
                    }
                    t.push("<td class=\"ui-widget-content " + extraclasses + "\">");
                    if (ic == 0 && formatter === undefined) {
                        t.push("<span style=\"white-space: nowrap\">");
                        t.push("<input type=\"checkbox\" data-id=\"" + rowid + "\" title=\"" + html.title(_("Select")) + "\" />");
                        t.push("<a href=\"#\" class=\"link-edit\" data-id=\"" + rowid + "\">" + tableform.format_string(vr, vr[vc.field]) + "</a>");
                        t.push("</span>");
                    }
                    else {
                        if (formatter === undefined) { formatter = tableform.format_string; }
                        t.push(formatter(vr, vr[vc.field]));
                    }
                    t.push("</td>");
                });
                t.push("</tr>");
            });
            if (!bodyonly) {
                t.push("</tbody></table>");
            }
            return t.join("\n");
        },

        /**
         * Updates the contents within the tbody of a table from
         * the table rows.
         *
         * table = ( see render_table )
         */
        table_update: function(table) {
            $("#tableform tbody").empty();
            $("#tableform tbody").html(this.table_render(table, true));
            // If the table had td styling on, re-apply it
            if ($("#tableform").prop("data-style-td")) {
                $("#tableform td").addClass("ui-widget-content");
            }
            $("#tableform").trigger("update");
            this.table_apply_sort(table);
        },

        /**
         * Binds table events and widgets. If there's a toolbar button set, can be
         * passed to bind watching for selections to them.
         *
         * table = ( see table_render )
         * buttons = { see buttons_render }
         */
        table_bind: function(table, buttons) {
            if (table.edit) {
                $("#tableform").on("click", "a", function() {
                    var anchor = $(this);
                    var iseditlink = false;
                    $.each(table.rows, function(i, v) {
                        if (v[table.idcolumn] == anchor.attr("data-id")) {
                            iseditlink = true;
                            table.edit(v);
                        }
                    });
                    // Edit links should cancel navigation
                    if (iseditlink) {
                        return false;
                    }
                });
            }

            // Watch for number of selected checkboxes changing and update 
            // the enable/disabled state of buttons
            if (buttons) {
                $("#tableform").on("click", "input[type='checkbox']", function() {
                    var nosel = $("#tableform input:checked").length;
                    $.each(buttons, function(i, b) {
                        var bn = $("#button-" + b.id), enabled = false;
                        if (b.enabled == "always") {
                            enabled = true;
                        }
                        if (b.enabled == "multi" && nosel > 0) {
                            enabled = true;
                        }
                        if (b.enabled == "one" && nosel == 1) {
                            enabled = true;
                        }
                        if (enabled) {
                            if (!b.type || b.type == "button") {
                                bn.button("enable");
                            }
                            else if (b.type == "buttonmenu") {
                                $("#button-" + b.id).removeClass("ui-state-disabled").removeClass("ui-button-disabled");
                            }
                        }
                        else {
                            if (!b.type || b.type == "button") {
                                bn.button("disable");
                            }
                            else if (b.type == "buttonmenu") {
                                bn.addClass("ui-state-disabled").addClass("ui-button-disabled");
                            }
                        }
                    });
                });
            }

            // Apply tablesorter widget
            $("#tableform").table();

            // And the default sort
            this.table_apply_sort(table);

        },

        /**
         * Applies any sorts necessary to the table
         * table = (see table_render)
         */
        table_apply_sort: function(table) {
            // If we don't have anything in the table, there's no point
            if ($("#tableform tbody tr").length == 0) {
                return;
            }
            var sortList;
            // Since some columns can be hidden, don't count those when figuring
            // out which columns to sort
            var visibleIndex = 0;
            $.each(table.columns, function(i, v) {
                if (sortList) { return; }
                if (v.hideif && v.hideif()) {
                    return;
                }
                if (v.initialsort) {
                     var sortdir = 0;
                     if (v.initialsortdirection && v.initialsortdirection == "desc") {
                         sortdir = 1;
                     }
                     sortList = [[visibleIndex, sortdir]];
                     return;
                }
                visibleIndex += 1;
            });
            $("#tableform").trigger("sorton", [sortList]);
        },

        /**
         * Returns a comma separated list of selected ids from
         * the table.
         * table = ( see table_render )
         */
        table_ids: function(table) {
            var s = "";
            $("#tableform input:checked").each(function() {
                s += $(this).attr("data-id") + ",";
            });
            return s;
        },

        /**
         * Returns the selected row in the table.
         * Returns undefined if nothing is selected.
         */
        table_selected_row: function(table) {
            var result, selid = $("#tableform input:checked").attr("data-id");
            if (!selid) { return undefined; }
            $.each(table.rows, function(i, v) {
                if (v[table.idcolumn] == selid) {
                    result = v;
                }
            });
            return result;
        },

        /**
         * Returns the selected rows in the table.
         * Returns undefined if nothing is selected.
         */
        table_selected_rows: function(table) {
            var results = [], selid = $("#tableform input:checked").attr("data-id");
            $("#tableform input:checked").each(function() {
                var el = $(this);
                $.each(table.rows, function(i, v) {
                    if (v[table.idcolumn] == el.attr("data-id")) {
                        results.push(v);
                    }
                });
            });
            return results;
        },

        /**
         * Returns true if the id given is selected in the table currently
         */
        table_id_selected: function(id) {
            var issel = false;
            $("#tableform input:checked").each(function() {
                if ($(this).attr("data-id") == id) {
                    issel = true;
                }
            });
            return issel;
        },

        /**
         * Removes selected items in the table from the model
         * table = ( see table_render )
         * rows = the json rows from the controller
         */
        table_remove_selected_from_json: function(table, rows) {
            var ids = this.table_ids(table).split(",");
            $.each(ids, function(ix, id) {
                // Have to use a nest because we can't delete during iteration
                $.each(rows, function(i, row) {
                    if (row && row[table.idcolumn] == id) {
                        rows.splice(i, 1); 
                    }
                });
            });
        },

        /**
         * Renders dialog
         *
         *   dialog = {
         *      add_title: _("Dialog title"),
         *      edit_title: _("Dialog title"),
         *      helper_text: _("Some info text"),
         *      close_on_ok: false,
         *      hide_read_only: false, // whether or not to hide read only fields in editing
         *      use_default_values: false,
         *      autofocus: true,
         *      columns: 1,
         *      width: 500,
         *      height: 200, (omit for auto)
         *      html_form_action: target (renders form tag around fields if set)
         *      html_form_enctype: enctype
         *      fields: (see fields_render)
         *  }
         */
        dialog_render: function(dialog) {
            var d =[];
            d.push("<div id=\"dialog-tableform\" style=\"display: none\">");
            if (dialog.helper_text) {
                d.push("<div id=\"dialog-tableform-help\" class=\"ui-widget\">");
                d.push("<div class=\"ui-state-highlight ui-corner-all\"><p>");
                d.push("<span class=\"ui-icon ui-icon-info\" style=\"float: left; margin-right: .3em;\"></span>");
                d.push("<span id=\"dialog-tableform-help-text\">" + dialog.helper_text + "</span>");
                d.push("</p></div></div>");
            }
            d.push("<div id=\"dialog-tableform-error\" style=\"display: none\" class=\"ui-widget\">");
            d.push("<div class=\"ui-state-error ui-corner-all\"><p>");
            d.push("<span class=\"ui-icon ui-icon-alert\" style=\"float: left; margin-right: .3em;\"></span>");
            d.push("<strong><span id=\"dialog-tableform-error-text\"></span></strong>");
            d.push("</p></div></div>");
            d.push("<div id=\"dialog-tableform-info\" style=\"display: none\" class=\"ui-widget\">");
            d.push("<div class=\"ui-state-highlight ui-corner-all\"><p>");
            d.push("<span class=\"ui-icon ui-icon-info\" style=\"float: left; margin-right: .3em;\"></span>");
            d.push("<span id=\"dialog-tableform-info-text\"></span>");
            d.push("</p></div></div>");
            if (dialog.html_form_action) {
                d.push("<form id=\"form-tableform\" method=\"post\" action=\"" + dialog.html_form_action + "\"");
                if (dialog.html_form_enctype) { d.push(" enctype=\"" + dialog.html_form_enctype + "\""); }
                d.push(">");
            }
            // If autofocus is defined and set to false, add a hidden
            // field that prevents JQuery UI autofocusing on any of our
            // fields (good for when choosers are the first field)
            if (dialog.autofocus === false) {
                d.push(html.capture_autofocus());
            }
            d.push(this.fields_render(dialog.fields, dialog.columns));
            if (dialog.html_form_action) {
                d.push("</form>");
            }
            d.push("</div>");
            return d.join("\n");
        },

        /**
         * Binds dialog field events
         *
         * dialog = (see dialog_render)
         */
        dialog_bind: function(dialog) {
            this.fields_bind(dialog.fields);
        },

        /**
         * Closes the dialog if it's open
         */
        dialog_close: function() {
            $("#dialog-tableform").dialog("close");
            $("#dialog-tableform").enable_dialog_buttons();
        },

        /**
         * Displays the dialog error text. If no text is supplied, 
         * removes the error.
         */
        dialog_error: function(text) {
            if (!text) {
                $("#dialog-tableform-error").hide();
            }
            else {
                $("#dialog-tableform-error-text").html(text);
                $("#dialog-tableform-error").fadeIn();
            }
        },

        dialog_info: function(text) {
            if (!text) {
                $("#dialog-tableform-info").hide();
            }
            else {
                $("#dialog-tableform-info-text").html(text);
                $("#dialog-tableform-info").fadeIn().delay(5000).fadeOut();
            }
        },

        dialog_disable_buttons: function() {
            $("#dialog-tableform").disable_dialog_buttons();
        },

        dialog_enable_buttons: function() {
            $("#dialog-tableform").enable_dialog_buttons();
        },

        /**
         * Shows the dialog in add mode 
         * 
         * dialog: (see dialog_render)
         * callback: function to run when the user clicks the add button (after validation)
         * onloadcallback: function to run when the form has loaded and been displayed
         */
        dialog_show_add: function(dialog, callback, onloadcallback) {
            var b = {}; 
            // Set fields to their default values
            if (dialog.use_default_values === undefined || dialog.use_default_values === true) {
                tableform.fields_default(dialog.fields);
            }
            // Find any fields marked readonly and enable them
            $.each(dialog.fields, function(i, v) {
                if (v.readonly) { 
                    $("#" + v.post_field).prop("disabled", false);
                    if (dialog.hide_read_only) {
                        $("#" + v.post_field).closest("tr").show(); 
                    }
                }
            });
            b[_("Add")] = function() {
                if (tableform.fields_validate(dialog.fields)) {
                    if (dialog.close_on_ok) {
                        $(this).dialog("close");
                    }
                    else {
                        $("#dialog-tableform").disable_dialog_buttons();
                    }
                    callback();
                }
            };
            b[_("Cancel")] = function() { $(this).dialog("close"); };
            $("#dialog-tableform").dialog({
                resizable: false,
                width: (dialog.width || "auto"),
                height: (dialog.height || "auto"),
                modal: true,
                dialogClass: "dialogshadow",
                autoOpen: false,
                title: dialog.add_title,
                show: dlgfx.add_show,
                hide: dlgfx.add_hide,
                buttons: b
            });
            this.dialog_error("");
            $("#dialog-tableform").dialog("open");
            if (onloadcallback) {
                onloadcallback();
            }
        },

        /**
         * Shows the dialog in edit mode 
         * 
         * dialog: (see dialog_render)
         * row: The row to edit
         * changecallback: function to run when the user clicks the change button (after validation)
         * onloadcallback: function to run after the form has been loaded and displayed
         */
        dialog_show_edit: function(dialog, row, changecallback, onloadcallback) {
            this.fields_populate_from_json(dialog.fields, row);
            // Find any fields marked readonly and disable/hide them
            $.each(dialog.fields, function(i, v) {
                if (v.readonly) { 
                    $("#" + v.post_field).prop("disabled", true);
                    if (dialog.hide_read_only) {
                        $("#" + v.post_field).closest("tr").hide(); 
                    }
                }
            });
            var b = {}; 
            b[_("Change")] = function() {
                if (tableform.fields_validate(dialog.fields)) {
                    if (dialog.close_on_ok) {
                        $(this).dialog("close");
                    }
                    else {
                        $("#dialog-tableform").disable_dialog_buttons();
                    }
                    if (changecallback) {
                        changecallback(row);
                    }
                }
            };
            b[_("Cancel")] = function() { $(this).dialog("close"); };
            $("#dialog-tableform").dialog({
                resizable: false,
                width: (dialog.width || "auto"),
                height: (dialog.height || "auto"),
                modal: true,
                dialogClass: "dialogshadow",
                autoOpen: false,
                title: dialog.edit_title,
                show: dlgfx.edit_show,
                hide: dlgfx.edit_hide,
                buttons: b
            });
            this.dialog_error("");
            $("#dialog-tableform").dialog("open");
            if (onloadcallback) {
                onloadcallback(row);
            }
        },


        /**
         * Renders fields
         *
         * fields: [
         *      { json_field: "name", 
         *        post_field: "name", 
         *        label: "label", 
         *        labelpos: "left", (or above, only really valid for textareas)
         *        type: "check|text|textarea|date|currency|number|select|animal|person|raw|nextcol", 
         *        readonly: false, (read only for editing, ok for creating)
         *        halfsize: false, (use the asm-halftextbox class)
         *        justwidget: false, (output tr/td/label)
         *        defaultval: expression or function to evaluate.
         *        validation: "notblank|notzero",
         *        classes: "extraclass anotherone",
         *        tooltip: _("Text"), 
         *        markup: "<input type='text' value='raw' />",
         *        options: { displayfield: "DISPLAY", valuefield: "VALUE", rows: [ {rows} ] }, (only valid for select type)
         *        options: "<option>test</option>" also valid
         *        personfilter: "all",   (only valid for person type)
         *        change: function(changeevent), 
         *        blur: function(blurevent)
         *      } ]
         * columns: number of cols to render (1 if undefined)
         * dontrenderoutertable: don't render the outer table tag (undefined means render it)
         */
        fields_render: function(fields, columns, dontrenderoutertable) {
            var d = "";
            if (columns === undefined) { columns = 1; }
            if (!dontrenderoutertable) {
                d = "<table width=\"100%\">";
            }
            if (columns > 1) {
                // We have multiple columns, start the first one
                d += "<tr><td><table>";
            }
            $.each(fields, function(i, v) {
                if (v.hideif && v.hideif()) {
                    return;
                }
                if (v.type == "check") {
                    if (!v.justwidget) { d += "<tr><td></td><td>"; }
                    d += "<input id=\"" + v.post_field + "\" type=\"checkbox\" class=\"asm-checkbox\" ";
                    d += "data-json=\"" + v.json_field + "\" data-post=\"" + v.post_field + "\" ";
                    if (v.readonly) { d += " data-noedit=\"true\" "; }
                    if (v.tooltip) { d += "title=\"" + html.title(v.tooltip) + "\""; }
                    d += "/>";
                    if (!v.justwidget) { d += "<label for=\"" + v.post_field + "\">" + v.label + "</label></td></tr>"; }
                }
                else if (v.type == "text") {
                    if (!v.justwidget) { d += "<tr><td><label for=\"" + v.post_field + "\">" + v.label + "</label></td><td>"; }
                    d += "<input id=\"" + v.post_field + "\" type=\"text\" class=\"asm-textbox " + v.classes;
                    if (v.halfsize) { d += " asm-halftextbox"; }
                    d += "\" ";
                    d += "data-json=\"" + v.json_field + "\" data-post=\"" + v.post_field + "\" ";
                    if (v.readonly) { d += " data-noedit=\"true\" "; }
                    if (v.validation) { d += "data-validation=\"" + v.validation + "\" "; }
                    if (v.tooltip) { d += "title=\"" + html.title(v.tooltip) + "\""; }
                    d += "/>";
                    if (!v.justwidget) { d += "</td></tr>"; }
                }
                else if (v.type == "textarea") {
                    if (!v.justwidget) {
                        if (v.labelpos && v.labelpos == "above") {
                            d += "<tr><td><label for=\"" + v.post_field + "\">" + v.label + "</label><br />";
                        }
                        else {
                            d += "<tr><td><label for=\"" + v.post_field + "\">" + v.label + "</label></td><td>";
                        }
                    }
                    if (!v.rows) { v.rows = 5; }
                    d += "<textarea id=\"" + v.post_field + "\" class=\"asm-textarea " + v.classes + "\" rows=\"" + v.rows + "\" ";
                    d += "data-json=\"" + v.json_field + "\" data-post=\"" + v.post_field + "\" ";
                    if (v.readonly) { d += " data-noedit=\"true\" "; }
                    if (v.validation) { d += "data-validation=\"" + v.validation + "\" "; }
                    if (v.tooltip) { d += "title=\"" + html.title(v.tooltip) + "\""; }
                    d += "></textarea>";
                    if (!v.justwidget) { d += "</td></tr>"; }
                }
                else if (v.type == "date") {
                    if (!v.justwidget) { d += "<tr><td><label for=\"" + v.post_field + "\">" + v.label + "</label></td><td>"; }
                    d += "<input id=\"" + v.post_field + "\" type=\"text\" class=\"asm-textbox asm-datebox\" ";
                    d += "data-json=\"" + v.json_field + "\" data-post=\"" + v.post_field + "\" ";
                    if (v.readonly) { d += " data-noedit=\"true\" "; }
                    if (v.validation) { d += "data-validation=\"" + v.validation + "\" "; }
                    if (v.tooltip) { d += "title=\"" + html.title(v.tooltip) + "\""; }
                    d += "/>";
                    if (!v.justwidget) { d += "</td></tr>"; }
                }
                else if (v.type == "time") {
                    if (!v.justwidget) { d += "<tr><td><label for=\"" + v.post_field + "\">" + v.label + "</label></td><td>"; }
                    d += "<input id=\"" + v.post_field + "\" type=\"text\" class=\"asm-textbox asm-timebox ";
                    if (v.halfsize) { d += " asm-halftextbox"; }
                    d += "\" ";
                    d += "data-json=\"" + v.json_field + "\" data-post=\"" + v.post_field + "\" ";
                    if (v.readonly) { d += " data-noedit=\"true\" "; }
                    if (v.validation) { d += "data-validation=\"" + v.validation + "\" "; }
                    if (v.tooltip) { d += "title=\"" + html.title(v.tooltip) + "\""; }
                    d += "/>";
                    if (!v.justwidget) { d += "</td></tr>"; }
                }
                else if (v.type == "currency") {
                    if (!v.justwidget) { d += "<tr><td><label for=\"" + v.post_field + "\">" + v.label + "</label></td><td>"; }
                    d += "<input id=\"" + v.post_field + "\" type=\"text\" class=\"asm-textbox asm-currencybox";
                    if (v.halfsize) { d += " asm-halftextbox"; }
                    d += "\" ";
                    d += "data-json=\"" + v.json_field + "\" data-post=\"" + v.post_field + "\" ";
                    if (v.readonly) { d += " data-noedit=\"true\" "; }
                    if (v.validation) { d += "data-validation=\"" + v.validation + "\" "; }
                    if (v.tooltip) { d += "title=\"" + html.title(v.tooltip) + "\""; }
                    d += "/>";
                    if (!v.justwidget) { d += "</td></tr>"; }
                }
                else if (v.type == "number") {
                    if (!v.justwidget) { d += "<tr><td><label for=\"" + v.post_field + "\">" + v.label + "</label></td><td>"; }
                    d += "<input id=\"" + v.post_field + "\" type=\"text\" class=\"asm-textbox asm-numberbox ";
                    if (v.halfsize) { d += " asm-halftextbox"; }
                    d += "\" ";
                    d += "data-json=\"" + v.json_field + "\" data-post=\"" + v.post_field + "\" ";
                    if (v.readonly) { d += " data-noedit=\"true\" "; }
                    if (v.validation) { d += "data-validation=\"" + v.validation + "\" "; }
                    if (v.tooltip) { d += "title=\"" + html.title(v.tooltip) + "\""; }
                    d += "/>";
                    if (!v.justwidget) { d += "</td></tr>"; }
                }
                else if (v.type == "select") {
                    if (!v.justwidget) { d += "<tr><td><label for=\"" + v.post_field + "\">" + v.label + "</label></td><td>"; }
                    d += "<select id=\"" + v.post_field + "\" class=\"asm-selectbox";
                    if (v.halfsize) { d += " asm-halftextbox"; }
                    d += "\" ";
                    d += "data-json=\"" + v.json_field + "\" data-post=\"" + v.post_field + "\" ";
                    if (v.readonly) { d += " data-noedit=\"true\" "; }
                    if (v.validation) { d += "data-validation=\"" + v.validation + "\" "; }
                    if (v.tooltip) { d += "title=\"" + html.title(v.tooltip) + "\""; }
                    d += ">";
                    if (common.is_array(v.options)) {
                        $.each(v.options, function(ia, va) {
                            d += "<option>" + va + "</option>";
                        });
                    }
                    else if (common.is_string(v.options)) {
                        d += v.options;
                    }
                    else if (v.options && v.options.rows) {
                        // Assume we have rows, valuefield and displayfield properties
                        $.each(v.options.rows, function(io, vo) {
                            d += "<option value=\"" + vo[v.options.valuefield] + "\">" + vo[v.options.displayfield] + "</option>";
                        });
                    }
                    d += "</select>";
                    if (!v.justwidget) { d += "</td></tr>"; }
                }
                else if (v.type == "selectmulti") {
                    if (!v.justwidget) { d += "<tr><td><label for=\"" + v.post_field + "\">" + v.label + "</label></td><td>"; }
                    d += "<select id=\"" + v.post_field + "\" multiple=\"multiple\" class=\"asm-bsmselect";
                    if (v.halfsize) { d += " asm-halftextbox"; }
                    d += "\" ";
                    d += "data-json=\"" + v.json_field + "\" data-post=\"" + v.post_field + "\" ";
                    if (v.readonly) { d += " data-noedit=\"true\" "; }
                    if (v.validation) { d += "data-validation=\"" + v.validation + "\" "; }
                    if (v.tooltip) { d += "title=\"" + html.title(v.tooltip) + "\""; }
                    d += ">";
                    if (v.options && v.options.rows) {
                        $.each(v.options.rows, function(io, vo) {
                            d += "<option value=\"" + vo[v.options.valuefield] + "\">" + vo[v.options.displayfield] + "</option>";
                        });
                    }
                    else if (v.options) {
                        d += v.options;
                    }
                    d += "</select>";
                    if (!v.justwidget) { d += "</td></tr>"; }
                }
                else if (v.type == "person") {
                    if (!v.justwidget) { d += "<tr><td><label for=\"" + v.post_field + "\">" + v.label + "</label></td><td>"; }
                    d += "<input id=\"" + v.post_field + "\" type=\"hidden\" class=\"asm-personchooser\" ";
                    d += "data-json=\"" + v.json_field + "\" data-post=\"" + v.post_field + "\" ";
                    if (v.readonly) { d += " data-noedit=\"true\" "; }
                    if (v.personfilter) { d += "data-filter=\"" + v.personfilter + "\" "; }
                    if (v.validation) { d += "data-validation=\"" + v.validation + "\" "; }
                    d += "/>";
                    if (!v.justwidget) { d += "</td></tr>"; }
                }
                else if (v.type == "animal") {
                    if (!v.justwidget) { d += "<tr><td><label for=\"" + v.post_field + "\">" + v.label + "</label></td><td>"; }
                    d += "<input id=\"" + v.post_field + "\" type=\"hidden\" class=\"asm-animalchooser\" ";
                    d += "data-json=\"" + v.json_field + "\" data-post=\"" + v.post_field + "\" ";
                    if (v.readonly) { d += " data-noedit=\"true\" "; }
                    if (v.animalfilter) { d += "data-filter=\"" + v.animalfilter + "\" "; }
                    if (v.validation) { d += "data-validation=\"" + v.validation + "\" "; }
                    d += "/>";
                    if (!v.justwidget) { d += "</td></tr>"; }
                }
                else if (v.type == "file") {
                    if (!v.justwidget) { d += "<tr><td><label for=\"" + v.post_field + "\">" + v.label + "</label></td><td>"; }
                    d += "<input id=\"" + v.post_field + "\" name=\"" + v.post_field + "\" type=\"file\" ";
                    d += "data-json=\"" + v.json_field + "\" data-post=\"" + v.post_field + "\" ";
                    if (v.readonly) { d += " data-noedit=\"true\" "; }
                    if (v.validation) { d += "data-validation=\"" + v.validation + "\" "; }
                    if (v.tooltip) { d += "title=\"" + html.title(v.tooltip) + "\""; }
                    d += "/>";
                    if (!v.justwidget) { d += "</td></tr>"; } 
                }
                else if (v.type == "raw") {
                    // Special widget that allows custom markup instead
                    if (!v.justwidget) { d += "<tr id=\"" + v.post_field + "\"><td><label>" + v.label + "</label></td><td>"; }
                    d += v.markup;
                    if (!v.justwidget) { d += "</td></tr>"; } 
                }
                else if (v.type == "nextcol") {
                    // Special fake widget that causes rendering to move to the next column
                    d += "</table><td><td><table>";
                }
            });
            if (columns > 1) {
                // Close out the current column for multi column layouts
                d += "</table></td></tr>";
            }
            if (!dontrenderoutertable) {
                d += "</table>";
            }
            return d;
        },

        /**
         * Binds fields
         *
         * fields: (see fields_render) 
         */
        fields_bind: function(fields) {
            $.each(fields, function(i, v) {
                if (v.change) {
                    $("#" + v.post_field).change(v.change);
                }
                if (v.blur) {
                    $("#" + v.post_field).blur(v.blur);
                }
            });
        },

        /**
         * Sets on screen fields to their default values
         */
        fields_default: function(fields) {
            $.each(fields, function(i, v) {
                // No default value given, use a blank
                if (!v.defaultval) {
                    if (v.type == "check") { $("#" + v.post_field).prop("checked", false); return; }
                    if (v.type == "animal") { $("#" + v.post_field).animalchooser("clear"); return; }
                    if (v.type == "person") { $("#" + v.post_field).personchooser("clear"); return; }
                    if (v.type == "selectmulti") { 
                        $("#" + v.post_field).children().prop("selected", false); 
                        $("#" + v.post_field).change(); 
                        return;
                    }
                    if (v.type == "textarea") { $("#" + v.post_field).val("");  return; }
                    if (v.type != "select" && v.type != "nextcol") { $("#" + v.post_field).val(""); }
                }
                else {
                    // Is the default value a function? If so, run it 
                    // to get the real value to assign
                    var dval = v.defaultval;
                    if (v.defaultval instanceof Function) {
                        dval = v.defaultval();
                    }
                    if (v.defaultval instanceof Date) {
                        dval = format.date(v.defaultval);
                    }
                    if (v.type == "check") { $("#" + v.post_field).prop("checked", dval); return; }
                    if (v.type == "animal") { $("#" + v.post_field).animalchooser("loadbyid", dval); return; }
                    if (v.type == "person") { $("#" + v.post_field).personchooser("loadbyid", dval); return; }
                    if (v.type == "select") { $("#" + v.post_field).select("value", dval); return; }
                    if (v.type == "textarea") { $("#" + v.post_field).val(dval); return; }
                    if (v.type != "nextcol") { $("#" + v.post_field).val(dval); }
                }
            });
        },

        /**
         * Populates fields
         *
         * fields: ( see fields_render) 
         * row: The json row to use
         */
        fields_populate_from_json: function(fields, row) {
            $.each(fields, function(i, v) {
                var n = $("#" + v.post_field);
                if (n.length == 0) { return; }
                if (v.type == "animal") {
                    n.animalchooser("loadbyid", row[v.json_field]);
                }
                else if (v.type == "person") {
                    n.personchooser("loadbyid", row[v.json_field]);
                }
                else if (v.type == "currency") {
                    n.currency("value", row[v.json_field]);
                }
                else if (v.type == "date") {
                    n.val(format.date(row[v.json_field]));
                }
                else if (v.type == "time") {
                    n.val(format.time(row[v.json_field]));
                }
                else if (v.type == "check") {
                    n.prop("checked", row[v.json_field] == 1);
                }
                else if (v.type =="select") {
                    n.select("value", row[v.json_field]);
                }
                else if (v.type == "selectmulti") {
                    n.children().prop("selected", false);
                    $.each(String(row[v.json_field]).split(/[|,]+/), function(mi, mv) {
                        n.find("[value='" + mv + "']").prop("selected", true);
                    });
                    n.change();
                }
                else if (v.type == "textarea") {
                    // Unescaped tags in textareas behave unpredictably
                    var s = row[v.json_field];
                    if (!s) { s = ""; }
                    s = s.replace(/</g, "&lt;").replace(/>/g, "&gt;");
                    n.val(html.decode(s));
                }
                else {
                    n.val(html.decode(row[v.json_field]));
                }
            });
        },

        /**
         * Updates a row with the field contents
         * fields: (see render_fields)
         * row: The row to update
         */
        fields_update_row: function(fields, row) {
            $.each(fields, function(i, v) {
                var n = $("#" + v.post_field);
                if (v.type == "currency") {
                    row[v.json_field] = n.currency("value");
                }
                else if (v.type == "date") {
                    row[v.json_field] = format.date_iso(n.val());
                }
                else if (v.type == "time") {
                    // always declare time fields after dates so we can
                    // modify the time on the timestamp
                    row[v.json_field] = format.date_iso_settime(row[v.json_field], n.val());
                }
                else if (v.type == "check") {
                    row[v.json_field] = n.is(":checked") ? 1 : 0;
                }
                else if (v.type == "selectmulti") {
                    if (!n.val()) { 
                        row[v.json_field] = ""; 
                    }
                    else if ($.isArray(n.val())) {
                        row[v.json_field] = n.val().join("|");
                    }
                    else {
                        row[v.json_field] = n.val();
                    }
                }
                else {
                    row[v.json_field] = n.val();
                }
            });
        },

        /**
         * Validates the fields against their rules. Returns false if there
         * was a problem or true for ok.
         *
         * fields: (see fields_render) 
         * row: The json row to use
         */
        fields_validate: function(fields) {
            var nbids = [];
            var nzids = [];
            $.each(fields, function(i, v) {
                $("label[for='" + v.post_field + "']").removeClass("ui-state-error-text");
                if (v.validation == "notblank") {
                    nbids.push(v.post_field);
                }
                if (v.validation == "notzero") {
                    nzids.push(v.post_field);
                }
            });
            var rv = true;
            if (nbids.length > 0) {
                rv = validate.notblank(nbids);
                if (!rv) { return rv; }
            }
            if (nzids.length > 0) {
                rv = validate.notzero(nzids);
                if (!rv) { return rv; }
            }
            return true;
        },

        /**
         * Posts the fields back to the controller. If an error occurred,
         * the message is output to the header. On success, the callback
         * method is called.
         * fields: (see fields_render) 
         * postvar: any extra post variables to send, eg: mode=amazing - don't leave trailing &
         * postto: The URL to post to
         * callback: function to call on success of the post, the ajax response is passed
         * errorcallback: function to call on error, the reponse is passed
         */
        fields_post: function(fields, postvar, postto, callback, errorcallback) {
            var post = "";
            if (postvar) { post = postvar; }
            $.each(fields, function(i, v) {
                var n = $("#" + v.post_field);
                if (v.type == "check") {
                    if (post != "") { post += "&"; }
                    if (n.is(":checked")) {
                        post += v.post_field + "=checked";
                    }
                    else {
                        post += v.post_field + "=off";
                    }
                }
                else if (v.type != "raw") {
                    if (post != "") { post += "&"; }
                    var pv = "";
                    if (n.val()) { pv = n.val(); }
                    post += v.post_field + "=" + encodeURIComponent(pv);
                }
            });
            $.ajax({
                type: "POST",
                url:  postto,
                data: post,
                dataType: "text",
                success: function(result) {
                    callback(result);
                },
                error: function(jqxhr, textstatus, response) {
                    var errmessage = common.get_error_response(jqxhr, response);
                    tableform.dialog_error(errmessage);
                    if (errorcallback) { errorcallback(errmessage); }
                }
            });
            return post;
        },

        /**
         * Prompts the user to delete with a dialog.
         * callback: Function to be run if the user clicks delete
         * text: The delete dialog text (don't pass for the default)
         */
        delete_dialog: function(callback, text) {
            var b = {}; 
            b[_("Delete")] = function() {
                $("#dialog-delete").dialog("close");
                callback();
            };
            b[_("Cancel")] = function() { $(this).dialog("close"); };
            var mess = _("This will permanently remove the selected records, are you sure?"); 
            if (text && text != "") {
                mess = text;
            }
            if ($("#dialog-delete").length == 0) {
                $("body").append('<div id="dialog-delete" style="display: none" title="' +
                    _("Delete") + '"><p><span class="ui-icon ui-icon-alert" style="float: left; margin: 0 7px 20px 0;"></span>' +
                    '<span id="dialog-delete-text"></span></p></div>');
            }
            $("#dialog-delete-text").html(mess);
            $("#dialog-delete").dialog({
                resizable: false,
                height: 170,
                width: 400,
                modal: true,
                dialogClass: "dialogshadow",
                show: dlgfx.delete_show,
                hide: dlgfx.delete_hide,
                buttons: b
            });
        }

    };

} (jQuery));

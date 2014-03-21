/*jslint browser: true, forin: true, eqeq: true, plusplus: true, white: true, regexp: true, sloppy: true, vars: true, nomen: true */
/*global $, console, jQuery */
/*global asm, common, config, dlgfx, format, html, header, validate, _, escape, unescape */

(function($) {

    // Generates a javascript object of parameters by looking
    // at the data attribute of all items matching the
    // selector
    $.fn.toJSON = function() {
        var params = {};
        this.each(function() {
            var t = $(this);
            if (t.attr("type") == "checkbox" && t.attr("data")) {
                if (t.is(":checked")) {
                    params[t.attr("data")] = "checked";
                }
            }
            else if (t.attr("data") && t.val()) {
                params[t.attr("data")] = t.val();
            }
        });
        return params;
    };

    // Populates fields matching the selector by looking up their
    // data-json attribute 
    $.fn.fromJSON = function(row) {
        this.each(function() {
            var n = $(this);
            var f = $(this).attr("data-json");
            if (f === undefined || f == null || f == "") { return; }
            if (n.hasClass("asm-animalchooser")) {
                n.animalchooser().animalchooser("loadbyid", row[f]);
            }
            else if (n.hasClass("asm-personchooser")) {
                n.personchooser().personchooser("loadbyid", row[f]);
            }
            else if (n.hasClass("asm-currencybox")) {
                n.val(format.currency(row[f]));
            }
            else if (n.hasClass("asm-datebox")) {
                n.val(format.date(row[f]));
            }
            else if (n.hasClass("asm-timebox")) {
                n.val(format.time(row[f]));
            }
            else if (n.is("textarea")) {
                n.html(row[f]);
            }
            else if (n.attr("type") == "checkbox") {
                n.prop("checked", row[f] == 1);
            }
            else if (n.hasClass("asm-bsmselect")) {
                n.children().prop("selected", false);
                $.each(String(row[f]).split(/[|,]+/), function(mi, mv) {
                    n.find("[value='" + mv + "']").prop("selected", true);
                });
                n.change();
            }
            else {
                n.val(html.decode(row[f]));
            }
        });
    };

    // Generates a URL encoded form data string of parameters
    // by looking at the data-post or data attribute of all items 
    // matching the selector
    $.fn.toPOST = function(includeblanks) {
        var post = "";
        this.each(function() {
            var t = $(this);
            var pname = t.attr("data-post");
            if (!pname) { pname = t.attr("data"); }
            if (!pname) { return; }
            if (t.attr("type") == "checkbox") {
                if (post != "") { post += "&"; }
                if (t.is(":checked")) {
                    post += pname + "=checked";   
                }
                else {
                    post += pname + "=off";
                }
            }
            else if (t.val()) {
                if (post != "") { post += "&"; }
                post += pname + "=" + encodeURIComponent(t.val());
            }
            else if (includeblanks) {
                if (post != "") { post += "&"; }
                post += pname + "=" + encodeURIComponent(t.val());
            }
        });
        return post;
    };

    // Generates a comma separated list of the data attributes of
    // every single checked checkbox in the selector
    $.fn.tableCheckedData = function() {
        var ids = "";
        this.each(function() {
            if ($(this).attr("type") == "checkbox") {
                if ($(this).is(":checked")) {
                    ids += $(this).attr("data") + ",";
                }
            }
        });
        return ids;
    };

    // Styles an HTML table with jquery stuff and adds sorting
    $.fn.table = function(options) {
        var defaults = {
            css:        'asm-table',
            style_td:   true,
            row_hover:  true,
            row_select: true,
            floating_header: true
        };
        options = $.extend(defaults, options);
        return this.each(function () {
            var input = $(this);
            input.addClass(options.css);
            if (options.row_hover) {
                input.on("mouseover", "tr", function() {
                    $(this).children("td").addClass("ui-state-hover");
                });
                input.on("mouseout", "tr", function() {
                    $(this).children("td").removeClass("ui-state-hover");
                });
            }
            if (options.row_select) {
                input.on("click", "input:checkbox", function() {
                    if ($(this).is(":checked")) {
                        $(this).closest("tr").find("td").addClass("ui-state-highlight");
                    }
                    else {
                        $(this).closest("tr").find("td").removeClass("ui-state-highlight");
                    }
                });
            }
            input.find("th").addClass("ui-state-default");
            if (options.style_td) {
                input.prop("data-style-td", "true");
                input.find("td").addClass("ui-widget-content");
            }
            input.addClass("tablesorter");
            input.tablesorter({
                sortColumn: options.sortColumn,
                sortList: options.sortList,
                textExtraction: function(node) {
                    // custom extraction function turns display dates 
                    // into iso dates behind the scenes for 
                    // alphanumeric sorting
                    var s = $(node).text();
                    if (s.split("/").length == 3) {
                        var rv = format.date_iso(s);
                        rv = rv.replace(/\-/g, "").replace(/\:/g, "").replace("T", "");
                        return rv;
                    }
                    return s;
                }
            });
            if (options.floating_header && config.bool("FloatingHeaders")) {
                var header = $(input).find("thead").clone();
                var fixedheader = $("#header-fixed").append(header);
                //fixedheader.addClass("ui-state-default");
                $(window).bind("scroll", function() {
                    var tableOffset = $(input).offset().top;
                    var offset = $(this).scrollTop();
                    if (offset >= tableOffset && fixedheader.is(":hidden")) {
                        $("#header-fixed").width($(input).width());
                        $(input).find("thead th").each(function(i, v) {
                            if ($(v).is(":visible")) {
                                $($("#header-fixed th")[i]).width($(v).width());
                            }
                            else {
                                $($("#header-fixed th")[i]).hide();
                            }
                        });
                        fixedheader.fadeIn();
                    }
                    else if (offset < tableOffset) {
                        fixedheader.fadeOut();
                    }
                });
            }
        });
    };

    // Styles a tab strip consisting of a div with an unordered list of tabs
    $.fn.asmtabs = function() {
        this.each(function() {
            $(this).addClass("ui-tabs ui-widget ui-widget-content ui-corner-all");
            $(this).find("ul.asm-tablist").addClass("ui-tabs-nav ui-helper-reset ui-helper-clearfix ui-widget-header ui-corner-all");
            $(this).find("ul.asm-tablist li").addClass("ui-state-default ui-corner-top");
            $(this).on("mouseover", "ul.asm-tablist li", function() {
                $(this).addClass("ui-state-hover");
            });
            $(this).on("mouseout", "ul.asm-tablist li", function() {
                $(this).removeClass("ui-state-hover");
            });
        });
    };

    // Textbox that should only contain numbers
    $.fn.number = function() {
        var allowed = [ '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.' ];
        this.each(function() {
            $(this).keypress(function(e) {
                var k = e.charCode || e.keyCode;
                var ch = String.fromCharCode(k);
                // Backspace, tab, ctrl, delete, arrow keys ok
                if (k == 8 || k == 9 || k == 17 || k == 46 || (k >= 35 && k <= 40)) {
                    return true;
                }
                if ($.inArray(ch, allowed) == -1) {
                    e.preventDefault();
                }
            });
        });
    };

    // Textbox that should only contain numbers and letters (no spaces or punctuation)
    $.fn.alphanumber = function() {
        this.each(function() {
            $(this).keydown(function(e) {
                if (!(e.keyCode == 8 // backspace
                    || e.keyCode == 9 // tab
                    || e.keyCode == 17 // ctrl
                    || e.keyCode == 46 // delete
                    || e.keyCode == 190 // point
                    || e.keyCode == 110 // point
                    || (e.keyCode >= 65 && e.keyCode <= 90) // capitals
                    || (e.keyCode >= 97 && e.keyCode <= 122) // lower case
                    || (e.keyCode >= 35 && e.keyCode <= 40) // arrow keys/home
                    || (!e.shiftKey && e.keyCode >= 48 && e.keyCode <= 57) // numbers on keyboard
                    || (e.keyCode >= 96 && e.keyCode <= 105) // numbers on keypad
                )) {
                    e.preventDefault();
                }
            });
        });
    };

    // Textbox that should only contain integer numbers
    $.fn.intnumber = function() {
        var allowed = [ '0', '1', '2', '3', '4', '5', '6', '7', '8', '9' ];
        this.each(function() {
            $(this).keypress(function(e) {
                var k = e.charCode || e.keyCode;
                var ch = String.fromCharCode(k);
                // Backspace, tab, ctrl, delete, arrow keys ok
                if (k == 8 || k == 9 || k == 17 || k == 46 || (k >= 35 && k <= 40)) {
                    return true;
                }
                if ($.inArray(ch, allowed) == -1) {
                    e.preventDefault();
                }
            });
        });
    };

    // Textbox that should only contain CIDR IP subnets
    $.fn.ipnumber = function() {
        var allowed = [ '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.', '/', ' ' ];
        this.each(function() {
            $(this).keypress(function(e) {
                var k = e.charCode || e.keyCode;
                var ch = String.fromCharCode(k);
                // Backspace, tab, ctrl, delete, arrow keys ok
                if (k == 8 || k == 9 || k == 17 || k == 46 || (k >= 35 && k <= 40)) {
                    return true;
                }
                if ($.inArray(ch, allowed) == -1) {
                    e.preventDefault();
                }
            });
        });
    };
    
    $.fn.date = function() {
        this.each(function() {
            $(this).datepicker({ 
                changeMonth: true, 
                changeYear: true,
                firstDay: 1
            });
            $(this).keydown(function(e) {
                var d;
                if (e.keyCode == 84) { // t - today
                    $(this).datepicker("setDate", new Date());
                    $(this).change();
                }
                if (e.keyCode == 68 && e.shiftKey == false) { // d, add a day
                    $(this).datepicker("setDate", "+1d");
                    $(this).change();
                }
                if (e.keyCode == 68 && e.shiftKey == true) { // shift+d, remove a day
                    $(this).datepicker("setDate", "-1d"); 
                    $(this).change();
                }
                if (e.keyCode == 87 && e.shiftKey == false) { // w, add a week
                    $(this).datepicker("setDate", "+1w");
                    $(this).change();
                }
                if (e.keyCode == 87 && e.shiftKey == true) { // shift+w, remove a week
                    $(this).datepicker("setDate", "-1w"); 
                    $(this).change();
                }
                if (e.keyCode == 77 && e.shiftKey == false) { // m, add a month
                    $(this).datepicker("setDate", "+1m");
                    $(this).change();
                }
                if (e.keyCode == 77 && e.shiftKey == true) { // shift+w, remove a month
                    $(this).datepicker("setDate", "-1m"); 
                    $(this).change();
                }
                if (e.keyCode == 89 && e.shiftKey == false) { // y, add a year
                    $(this).datepicker("setDate", "+1y");
                    $(this).change();
                }
                if (e.keyCode == 89 && e.shiftKey == true) { // shift+y, remove a year
                    $(this).datepicker("setDate", "-1y"); 
                    $(this).change();
                }
            });
        });
    };

    // Textbox that should only contain a time (numbers and colon)
    $.fn.time = function() {
        var allowed = [ '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':' ];
        this.each(function() {
            $(this).keypress(function(e) {
                var k = e.charCode || e.keyCode;
                var ch = String.fromCharCode(k);
                // Backspace, tab, ctrl, delete, arrow keys ok
                if (k == 8 || k == 9 || k == 17 || k == 46 || (k >= 35 && k <= 40)) {
                    return true;
                }
                if ($.inArray(ch, allowed) == -1) {
                    e.preventDefault();
                }
            });
        });
    };

    // Select box
    $.fn.select = function(method, newval) {
        if (method === undefined) {
            method = "create";
        }
        if (method == "create") {
            $(this).each(function() {
                // $(this).dosomething
            });
        }
        if (method == "value") {
            var rv = "";
            $(this).each(function() {
                if (newval !== undefined) {
                    $(this).val(newval);
                }
                else {
                    rv = $(this).val();
                    return;
                }
            });
            return rv;
        }
        if (method == "disable") {
            $(this).each(function() {
                $(this).attr("disabled", "disabled");
            });
        }
        if (method == "enable") {
            $(this).each(function() {
                $(this).removeAttr("disabled");
            });
        }
    };

    /**
     * ASM menu widget (we have to use asmmenu so as not to clash
     * with the built in JQuery UI menu widget)
     */
    $.widget("asm.asmmenu", {
        options: {
            button: null,
            menu: null
        },

        _create: function() {
            var self = this;
            var button = this.element;
            this.options.button = button;
            
            // Add display arrow span
            var n = "<span style=\"display: inline\" class=\"ui-button-text ui-icon ui-icon-triangle-1-e\">&nbsp;&nbsp;&nbsp;</span>";
            this.element.append(n);
            
            // If the menu is empty, disable it
            var id = this.element.attr("id");
            var body = $("#" + id + "-body");
            this.options.menu = body;
            if (body.find(".asm-menu-item").size() == 0) {
                button.addClass("ui-state-disabled").addClass("ui-button-disabled");
            }
            
            // Add JQuery widget styles to the menu container/body
            body.addClass("ui-widget ui-widget-content ui-corner-all menushadow");
            button
                .addClass("ui-widget ui-state-default ui-corner-all")
                .mouseover(function() { $(this).addClass("ui-state-hover").removeClass("ui-state-default"); })
                .mouseout(function() { $(this).addClass("ui-state-default").removeClass("ui-state-hover"); });

            // Attach hover styles to the menu items, but make sure they're never bold
            body.find(".asm-menu-item").css("font-weight", "normal");
            body.on("mouseover", ".asm-menu-item", function() {
                $(this).addClass("ui-state-hover");
            });
            body.on("mouseout", ".asm-menu-item", function() {
                $(this).removeClass("ui-state-hover");
            });
            
            // Attach click handler to the button
            if (!button.hasClass("ui-state-disabled")) {
                button.click(function() {
                    self.toggle_menu(id);
                });
            }

            // Hide the menu/body
            body.hide();

            // Hide all menus if any form content is clicked, as long as it's
            // not a menu opening button/icon that was clicked anyway
            // make sure we only do this once
            if (!$("body").attr("data-menu-hide")) {
                $("body").attr("data-menu-hide", "true");
                $("body").click(function(e) {
                    var t = $(e.target);
                    if (t.hasClass("asm-menu-icon") || t.parent().hasClass("asm-menu-icon")) { return true; }
                    if (t.hasClass("asm-menu-button") || t.parent().hasClass("asm-menu-button")) { return true; }
                    if (e.target.offsetParent && e.target.offsetParent.classList &&
                        e.target.offsetParent.classList.contains("asm-menu-button")) { return true; }
                    self.hide_all();
                });
            }

            // Figure out the modifier sequence based on the browser and
            // update all the hotkey sequences in the menu accordingly
            var modifier = "SHIFT+ALT+";
            if (common.is_safari()) { modifier = "CTRL+OPT+"; }
            if (common.is_opera()) { modifier = "SHIFT+ESC+"; }
            // IE can't support accesskeys on our menu as it has to be visible for
            // the accesskey to work (which makes it ultimately pointless)
            if (common.is_msie()) { modifier = "";  }
            body.find(".asm-hotkey").each(function() {
                if (modifier == "") {
                    $(this).text("");
                }
                else {
                    $(this).text(modifier + $(this).text());
                }
            });
        },

        hide_all: function() {
            // Active
            $(".asm-menu-icon").removeClass("ui-state-active").addClass("ui-state-default");
            // Menus
            $(".asm-menu-body").css("z-index", 0).hide();
            // Set icons back to up
            $(".asm-menu-icon span.ui-button-text").removeClass("ui-icon-triangle-1-s").addClass("ui-icon-triangle-1-e");
        },

        toggle_menu: function(id) {
           // Get the menu body element, style it and position it below the button
            var button = "#" + id;
            var body = "#" + id + "-body";
            var topval = $(button).offset().top + $(button).height() + 14;
            var leftval = $(button).offset().left;

            // If the menu button is disabled, don't do anything
            if ($(button).hasClass("ui-state-disabled")) { return; }

            // If the left position puts it off screen, move it over until it fits
            if ((leftval + $(body).width()) > $(window).width()) {
                leftval = $(window).width() - $(body).width() - 15;
            }

            $(body).css({
                top: topval + "px",
                left: leftval + "px"
            });

            // If the width of the body is less than the button, then increase the
            // size to match, otherwise it just looks weird
            if ($(body).width() < $(button).width()) {
                $(body).css({
                    width: String($(button).width() + 8) + "px"
                });
            }

            // If the menu was displayed previously, don't try and display it again
            var wasactive = $(body).css("display") != "none";
            
            // Slide up all existing menus
            this.hide_all();

            // Slide down our newly opened menu
            if (!wasactive) {
                $(button).removeClass("ui-state-default").addClass("ui-state-active");
                $(button + " span.ui-button-text").removeClass("ui-icon-triangle-1-e").addClass("ui-icon-triangle-1-s");
                $(body).css("z-index", "2 !important").slideDown();
            }
        }
    });

    $.widget("asm.textbox", {
        options: {
            disabled: false
        },

        _create: function() {
            var self = this;
            this.element.on("keypress", function(e) {
                if (self.options.disabled) {
                    e.preventDefault();
                }
            });
        },

        enable: function() {
            this.options.disabled = false;
            this.element.removeClass("asm-textbox-disabled");
        },

        disable: function() {
            this.options.disabled = true;
            this.element.addClass("asm-textbox-disabled");
        },

        toggleEnabled: function(enableOrDisable) {
            if (enableOrDisable) { 
                this.enable(); 
            }
            else {
                this.disable();
            }
        }
    });

    $.fn.textarea = function() {
        var pos = "left: -32px; top: -8px;";
        if (common.is_msie()) { pos = "left: -36px;"; }
        this.each(function() {
            var t = $(this);
            var zbid = t.attr("id") + "-zb";
            t.wrap("<span style='white-space: nowrap'></span>");
            t.after("<a style='position: relative; " + pos + " ' id='" + zbid + "' href='#'><span class='asm-icon asm-icon-edit'></span></a>");
            $("#" + zbid).click(function() {
                // If the textarea is disabled, don't do anything
                if (t.is(":disabled")) { return; }
                if (t.attr("maxlength") !== undefined) { $("#textarea-zoom-area").attr("maxlength", t.attr("maxlength")); }
                $("#textarea-zoom-id").val( t.attr("id") );
                $("#textarea-zoom-area").val( t.val() );
                $("#textarea-zoom-area").css({ "font-family": t.css("font-family") });
                var title = "";
                if (t.attr("title")) { title = String(t.attr("title")); }
                $("#dialog-textarea-zoom").dialog("option", "title", title);
                $("#dialog-textarea-zoom").dialog("open");
            });
        });
    };

    // Styles a textbox that should only contain currency
    $.fn.currency = function(cmd, newval) {
        var reset = function(b) {
            // Show a currency symbol and default amount of 0
            if ($(b).val() == "") {
                $(b).val(format.currency(0));
            }
        };
        if (cmd === undefined) {
            var allowed = [ '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.', '-' ];
            this.each(function() {
                $(this).keypress(function(e) {
                    var k = e.charCode || e.keyCode;
                    var ch = String.fromCharCode(k);
                    // Backspace, tab, ctrl, delete, arrow keys ok
                    if (k == 8 || k == 9 || k == 17 || k == 46 || (k >= 35 && k <= 40)) {
                        return true;
                    }
                    if ($.inArray(ch, allowed) == -1) {
                        e.preventDefault();
                    }
                });
                reset(this);
            });
        }
        else if (cmd == "reset") {
            this.each(function() {
                reset(this);
            });
        }
        else if (cmd == "value") {
            if (newval == undefined) {
                // Get the value
                var v = this.val(), f;
                if (!v) {
                    return 0;
                }
                // Extract only the numbers, sign and decimal point
                v = v.replace(/[^0123456789\-\.]/g, '');
                v = $.trim(v);
                f = parseFloat(v);
                f = f * 100;
                return parseInt(f, 10);
            }
            // We're setting the value
            this.each(function() {
                $(this).val(format.currency(newval));
            });
        }
    };

    // Helper to disable jquery ui dialog buttons
    $.fn.disable_dialog_buttons = function() {
        this.each(function() {
            $(this).parent().find("button").button("disable");
        });
    };

    // Helper to enable jquery ui dialog buttons
    $.fn.enable_dialog_buttons = function() {
        this.each(function() {
            $(this).parent().find("button").button("enable");
        });
    };

    // Adds a shadow to an element
    $.fn.shadow = function() {
        this.each(function() {
            $(this).after("<div class=\"shadow\" id=\"" + $(this).attr("id") + "-shadow\" />");
            var h = $(this).outerHeight();
            var w = $(this).outerWidth();
            $(this).next().css({
                "z-index": "-1 !important",
                position: "absolute",
                height: h + "px",
                width: w + "px",
                top: ($(this).offset().top + 15) + "px",
                left: ($(this).offset().left + 15) + "px"
            });
        });
    };

    $.fn.asmcontent = function(type) {
        // Show the content
        this.each(function() {
            // criteria
            // results
            // newdata
            // report
            if (type == "main") {
                $(this).delay(1).show("slide", {direction: 'up'});
                return;
            }
            if (type == "formtab") {
                $(this).delay(1).show("slide", {direction: 'right'});
                return;
            }
            if (type == "book") {
                $(this).delay(1).show("slide", {direction: 'down'});
                return;
            }
            if (type == "options") {
                $(this).delay(1).show("slide", {direction: 'up'});
                return;
            }
            // default
            $(this).delay(1).show("slide", {direction: 'left'});
        });
    };

} (jQuery));

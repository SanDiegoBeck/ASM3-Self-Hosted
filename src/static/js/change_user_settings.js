/*jslint browser: true, forin: true, eqeq: true, white: true, sloppy: true, vars: true, nomen: true */
/*global $, jQuery, _, asm, common, config, controller, dlgfx, format, header, html, validate */

$(function() {

    var BACKGROUND_COLOURS = {
        "black-tie":        "#333333",
        "blitzer":          "#cc0000",
        "cupertino":        "#deedf7",
        "dark-hive":        "#444444",
        "dot-luv":          "#0b3e6f",
        "eggplant":         "#30273a",
        "excite-bike":      "#f9f9f9",
        "flick":            "#dddddd",
        "hot-sneaks":       "#35414f",
        "humanity":         "#cb842e",
        "le-frog":          "#3a8104",
        "mint-choc":        "#453326",
        "overcast":         "#dddddd",
        "pepper-grinder":   "#ffffff",
        "redmond":          "#5c9ccc",
        "smoothness":       "#cccccc",
        "south-street":     "#ece8da",
        "start":            "#2191c0",
        "sunny":            "#817865",
        "swanky-purse":     "#261803",
        "trontastic":       "#9fda58",
        "ui-darkness":      "#333333",
        "ui-lightness":     "#ffffff",
        "vader":            "#888888"
    };

    var change_user_settings = {

        /** Where we have a list of pairs, first is value, second is label */
        two_pair_options: function(o) {
            var s = [];
            $.each(o, function(i, v) {
                s.push('<option value="' + v[0] + '">' + v[1] + '</option>');
            });
            return s.join("\n");
        },

        render: function() {
            return [
                html.content_header(_("Change User Settings")),
                '<table class="asm-table-layout">',
                '<tr>',
                    '<td>' + _("Username") + '</td>',
                    '<td>' + asm.user + '</td>',
                '</tr>',
                '<tr>',
                    '<td>',
                    '<label for="realname">' + _("Real name") + '</label>',
                    '</td>',
                    '<td>',
                    '<input id="realname" data="realname" class="asm-textbox" />',
                    '</td>',
                '</tr>',
                '<tr>',
                    '<td>',
                    '<label for="email">' + _("Email Address") + '</label>',
                    '</td>',
                    '<td>',
                    '<input id="email" data="email" class="asm-textbox" />',
                    '</td>',
                '</tr>',
                '<tr>',
                    '<td>',
                    '<label for="olocale">' + _("Locale") + '</label>',
                    '</td>',
                    '<td>',
                    '<select id="olocale" data="locale" class="asm-selectbox">',
                    '<option value="">' + _("(use system)") + '</option>',
                    this.two_pair_options(controller.locales),
                    '</select> <span id="localeflag"></span>',
                    '</td>',
                '</tr>',
                '<tr>',
                    '<td>',
                    '<label for="systemtheme">' + _("Visual Theme") + '</label>',
                    '</td>',
                    '<td>',
                    '<select id="systemtheme" data="theme" class="asm-selectbox">',
                    '<option value="">' + _("(use system)") + '</option>',
                    this.two_pair_options(controller.themes),
                    '</select>',
                    '</td>',
                '</tr>',
                '</table>',
                '<div class="centered">',
                    '<button id="save">' + html.icon("save") + ' ' + _("Save") + '</button>',
                '</div>',
                html.content_footer()
            ].join("\n");
        },

        bind: function() {
            $("#save").button().click(function() {
                $(".asm-content button").button("disable");
                header.show_loading();
                var formdata = $("input, select").toPOST();
                common.ajax_post("change_user_settings", formdata, function(result) { 
                    window.location = "main"; 
                }, function() { 
                    $(".asm-content button").button("enable");
                });
            });

            var update_flag = function() {
                var h = "<img style='position: relative; vertical-align: middle; left: -48px;' src='static/images/flags/" + 
                    $("#olocale").val() + ".png' title='" + 
                    $("#olocale").val() + "' />";
                $("#localeflag").html(h);
            };
            $("#olocale").change(update_flag);

            // When the visual theme is changed, switch the CSS file so the
            // theme updates immediately.
            $("#systemtheme").change(function() {
                var theme = $("#systemtheme").val();
                if (theme == "") {
                    theme = asm.theme;
                }
                var href = "https://ajax.googleapis.com/ajax/libs/jqueryui/1.10.3/themes/" + theme + "/jquery-ui.css";
                $("#jqt").attr("href", href);
                $("body").css("background-color", BACKGROUND_COLOURS[theme]);
            });

        },

        sync: function() {
            var u = controller.user[0];
            $("#realname").val(html.decode(u.REALNAME));
            $("#email").val(u.EMAIL);
            $("#olocale").val(u.LOCALEOVERRIDE);
            $("#systemtheme").val(u.THEMEOVERRIDE);
        }
    };

    common.module(change_user_settings, "change_user_settings", "options");

});

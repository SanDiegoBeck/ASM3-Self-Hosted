/*jslint browser: true, forin: true, eqeq: true, white: true, sloppy: true, vars: true, nomen: true */
/*global $, jQuery, _, asm, common, config, controller, dlgfx, format, header, html, validate */

$(function() {

    var person_find = {

        render: function() {
            return [
                html.content_header(_("Find Person")),
                '<form id="personsearchform" action="person_find_results" method="GET">',
                '<p class="asm-search-selector">',
                '<a id="asm-search-selector-simple" href="#">' + _("Simple") + '</a> |',
                '<a id="asm-search-selector-advanced" href="#">' + _("Advanced") + '</a>',
                '</p>',
                '<div id="asm-criteria-simple">',
                '<table class="asm-table-layout">',
                '<tr>',
                '<td>',
                '<label for="q">' + _("Search") + '</label>',
                '</td>',
                '<td>',
                '<input id="mode" name="mode" type="hidden" value="SIMPLE" />',
                '<input id="q" name="q" class="asm-textbox" />',
                '</td>',
                '</tr>',
                '</table>',
                '</div>',
                '<div id="asm-criteria-advanced">',
                '<table class="asm-table-layout">',
                '<tr>',
                '<td>',
                '<label for="code">' + _("Code contains") + '</label>',
                '</td>',
                '<td>',
                '<input id="name" code="code" class="asm-textbox" />',
                '</td>',
                '</tr>',
                '<tr>',
                '<td>',
                '<label for="name">' + _("Name contains") + '</label>',
                '</td>',
                '<td>',
                '<input id="name" name="name" class="asm-textbox" />',
                '</td>',
                '<td>',
                '<label for="address">' + _("Address contains") + '</label>',
                '</td>',
                '<td>',
                '<input id="address" name="address" class="asm-textbox" />',
                '</td>',
                '</tr>',
                '<tr id="towncountyrow">',
                '<td>',
                '<label for="town">' + _("City contains") + '</label>',
                '</td>',
                '<td>',
                '<input id="town" name="town" class="asm-textbox" />',
                '</td>',
                '<td>',
                '<label for="county">' + _("State contains") + '</label>',
                '</td>',
                '<td>',
                '<input id="county" name="county" class="asm-textbox" />',
                '</td>',
                '</tr>',
                '<tr>',
                '<td>',
                '<label for="postcode">' + _("Zipcode contains") + '</label>',
                '</td>',
                '<td>',
                '<input id="postcode" name="postcode" class="asm-textbox" />',
                '</td>',
                '<td>',
                '<label for="homecheck">' + _("Homecheck areas") + '</label>',
                '</td>',
                '<td>',
                '<input id="homecheck" name="homecheck" class="asm-textbox" />',
                '</td>',
                '</tr>',
                '<tr>',
                '<td>',
                '<label for="comments">' + _("Comments contain") + '</label>',
                '</td>',
                '<td>',
                '<input id="comments" name="comments" class="asm-textbox" />',
                '</td>',
                '<td>',
                '<label for="email">' + _("Email") + '</label>',
                '</td>',
                '<td>',
                '<input id="email" name="email" class="asm-textbox" />',
                '</td>',
                '</tr>',
                '<tr>',
                '<td>',
                '<label for="medianotes">' + _("Media notes contain") + '</label>',
                '</td>',
                '<td>',
                '<input id="medianotes" name="medianotes" class="asm-textbox" />',
                '</td>',
                '<td>',
                '<label for="filter">' + _("Show") + '</label>',
                '</td>',
                '<td>',
                '<select id="filter" name="filter" class="asm-selectbox">',
                '<option value="all">' + _("(all)") + '</option>',
                '<option value="aco">' + _("ACO") + '</option>',
                '<option value="banned">' + _("Banned") + '</option>',
                '<option value="donor">' + _("Donor") + '</option>',
                '<option value="fosterer">' + _("Fosterer") + '</option>',
                '<option value="homechecked">' + _("Homechecked") + '</option>',
                '<option value="homechecker">' + _("Homechecker") + '</option>',
                '<option value="member">' + _("Member") + '</option>',
                '<option value="shelter">' + _("Other Shelter") + '</option>',
                '<option value="retailer">' + _("Retailer") + '</option>',
                '<option value="staff">' + _("Staff") + '</option>',
                asm.locale == "en_GB" ? '<option value="giftaid">' + _("UK Giftaid") + '</option>' : "",
                '<option value="vet">' + _("Vet") + '</option>',
                '<option value="volunteer">' + _("Volunteer") + '</option>',
                person_find.render_flags(),
                '</select>',
                '</td>',
                '</tr>',
                '</table>',
                '</div>',
                '<p class="centered">',
                '<button id="searchbutton" type="submit">' + _("Search") + '</button>',
                '</p>',
                '</form>',
                html.content_footer()
            ].join("\n");
        },

        render_flags: function() {
            var h = [];
            $.each(controller.flags, function(i, v) {
                h.push('<option>' + v.FLAG + '</option>');
            });
            return h.join("\n");
        },

        bind: function() {
            // Switch to simple search criteria
            var simpleMode = function() {
                $("#mode").val("SIMPLE");
                $("#asm-search-selector-advanced").removeClass("asm-link-disabled");
                $("#asm-search-selector-simple").addClass("asm-link-disabled");
                $("#asm-criteria-advanced").slideUp(function() {
                    $("#asm-criteria-simple").slideDown(function() {
                        $("input[name='q']").focus();
                    });
                });
            };

            // Switch to advanced search criteria
            var advancedMode = function() {
                $("#mode").val("ADVANCED");
                $("input[name='q']").val("");
                $("#asm-search-selector-simple").removeClass("asm-link-disabled");
                $("#asm-search-selector-advanced").addClass("asm-link-disabled");
                $("#asm-criteria-simple").slideUp(function() {
                    $("#asm-criteria-advanced").slideDown(function() {
                        $("input[name='name']").focus();
                    });
                });
            };

            // Handle switching between modes via the links
            $("#asm-search-selector-simple").click(function() {
                simpleMode();
            });

            $("#asm-search-selector-advanced").click(function() {
                advancedMode();
            });

            // Search button
            $("#searchbutton").button();

            // Get the default mode and set that
            $("#asm-criteria-simple").hide();
            $("#asm-criteria-advanced").hide();
            if (config.bool("AdvancedFindOwner")) {
                advancedMode();
            }
            else {
                simpleMode();
            }
        }
    };

    common.module(person_find, "person_find", "criteria");

});

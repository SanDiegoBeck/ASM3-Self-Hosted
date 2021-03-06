/*jslint browser: true, forin: true, eqeq: true, white: true, sloppy: true, vars: true, nomen: true */
/*global $, jQuery, _, asm, common, config, controller, dlgfx, format, header, html, validate */

$(function() {

    var mode = controller.name.indexOf("lost") != -1 ? "lost" : "found";

    var lostfound_find_results = {

        render: function() {
            return [
                html.content_header(_("Results")),
                '<div id="asm-results">',
                '<div class="ui-state-highlight ui-corner-all" style="margin-top: 5px; padding: 0 .7em">',
                '<p><span class="ui-icon ui-icon-search" style="float: left; margin-right: .3em;"></span>',
                controller.resultsmessage,
                '</p>',
                '</div>',
                '<table id="searchresults">',
                '<thead>',
                '<tr>',
                '<th>' + _("Contact") + '</th>',
                '<th>' + _("Number") + '</th>',
                '<th>' + _("Area") + '</th>',
                '<th>' + _("Zipcode") + '</th>',
                '<th>' + _("Date") + '</th>',
                '<th>' + _("Age Group") + '</th>',
                '<th>' + _("Sex") + '</th>',
                '<th>' + _("Species") + '</th>',
                '<th>' + _("Breed") + '</th>',
                '<th>' + _("Color") + '</th>',
                '<th>' + _("Features") + '</th>',
                '</thead>',
                '<tbody>',
                this.render_results(),
                '</tbody>',
                '</table>',
                '</div>',
                html.content_footer()
            ].join("\n");
        },

        render_results: function() {
            var h = [];
            $.each(controller.rows, function(i, r) {
                h.push('<tr>');
                if (mode == "lost") {
                    h.push('<td><a href="lostanimal?id=' + r.ID + '">' + r.OWNERNAME + '</a></td>');
                }
                else {
                    h.push('<td><a href="foundanimal?id=' + r.ID + '">' + r.OWNERNAME + '</a></td>');
                }
                h.push('<td>' + format.padleft(r.ID, 6) + '</td>');
                if (mode == "lost") {
                    h.push('<td>' + r.AREALOST + '</td>');
                }
                else {
                    h.push('<td>' + r.AREAFOUND + '</td>');
                }
                h.push('<td>' + r.AREAPOSTCODE + '</td>');
                if (mode == "lost") {
                    h.push('<td>' + format.date(r.DATELOST) + '</td>');
                }
                else {
                    h.push('<td>' + format.date(r.DATEFOUND) + '</td>');
                }
                h.push('<td>' + r.AGEGROUP + '</td>');
                h.push('<td>' + r.SEXNAME + '</td>');
                h.push('<td>' + r.SPECIESNAME + '</td>');
                h.push('<td>' + r.BREEDNAME + '</td>');
                h.push('<td>' + r.BASECOLOURNAME + '</td>');
                h.push('<td>' + r.DISTFEAT + '</td>');
                h.push('</tr>');
            });
            return h.join("\n");
        },

        bind: function() {
            $("#searchresults").table();
        }
    };

    common.module(lostfound_find_results, "lostfound_find_results", "results");

});

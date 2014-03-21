/*jslint browser: true, forin: true, eqeq: true, white: true, sloppy: true, vars: true, nomen: true */
/*global $, jQuery, _, asm, common, config, controller, dlgfx, format, header, html, validate */

$(function() {

    var shelterview = {

        /**
         * groupfield: The name of the field to group headings on with totals
         * sorton: Comma separated list of fields to sort on
         * dragdrop: Whether dragging and dropping is on and moves between locations
         * translategroup: Whether the group field needs to be translated
         */
        render_view: function(groupfield, sorton, dragdrop, translategroup) {
            var h = [], lastgrp = "", grpdisplay = "", grplink = "", runningtotal = 0, i, showunit = (groupfield == "DISPLAYLOCATIONNAME");
            // Sort the rows for the view
            controller.animals.sort( common.sort_multi(sorton) );
            $.each(controller.animals, function(i, a) {
                if (lastgrp != a[groupfield]) {
                    if (lastgrp != "") { h.push("</div>"); }
                    // Find the last total token and update it
                    for (i = 0; i < h.length; i += 1) {
                        if (h[i].indexOf("##LASTTOTAL") != -1) {
                            h[i] = h[i].replace("##LASTTOTAL", runningtotal);
                        }
                    }
                    // Reset the counter for the new category
                    runningtotal = 0;
                    lastgrp = a[groupfield];
                    // Produce an appropriate link based on the group field
                    grplink = "#";
                    if (groupfield == "DISPLAYLOCATIONNAME") {
                        grplink = "animal_find_results?logicallocation=onshelter&shelterlocation=" + a.SHELTERLOCATION;
                        if (a.ACTIVEMOVEMENTTYPE == 2) {
                            grplink = "move_book_foster";
                        }
                        if (a.HASTRIALADOPTION == 1) {
                            grplink = "move_book_trial_adoption";
                        }
                    }
                    if (groupfield == "SPECIESNAME") {
                        grplink = "animal_find_results?logicallocation=onshelter&speciesid=" + a.SPECIESID;
                    }
                    if (groupfield == "ADOPTIONSTATUS") {
                        if (a.ADOPTIONSTATUS == "Adoptable") {
                            grplink = "animal_find_results?logicallocation=adoptable";
                        }
                        if (a.ADOPTIONSTATUS == "Not For Adoption") {
                            grplink = "animal_find_results?logicallocation=notforadoption";
                        }
                        if (a.ADOPTIONSTATUS == "Reserved") {
                            grplink = "move_book_reservation";
                        }
                        if (a.ADOPTIONSTATUS == "Cruelty Case") {
                            grplink = "animal_find_results?logicallocation=onshelter&showcrueltycaseonly=on";
                        }
                        if (a.ADOPTIONSTATUS == "Hold") {
                            grplink = "animal_find_results?logicallocation=hold";
                        }
                        if (a.ADOPTIONSTATUS == "Quarantine") {
                            grplink = "animal_find_results?logicallocation=quarantine";
                        }
                    }
                    if (groupfield == "CURRENTOWNERNAME" && a.CURRENTOWNERID) {
                        grplink = "person?id=" + a.CURRENTOWNERID;
                    }
                    // Does the name need translating?
                    grpdisplay = lastgrp;
                    if (translategroup) {
                        grpdisplay = _(grpdisplay);
                    }
                    // Turn null into none
                    if (!grpdisplay) {
                        grpdisplay = _("(none)");
                    }
                    h.push('<p class="asm-menu-category"><a href="' + grplink + '">' + 
                        grpdisplay + ' (##LASTTOTAL)</a></p>');
                    // Foster and trial adoptions can't be drop targets and drag/drop must be on for this view
                    if (a.ACTIVEMOVEMENTTYPE != 2 && a.HASTRIALADOPTION == 0 && dragdrop) {
                        h.push('<div class="locationdroptarget" data="' + a.SHELTERLOCATION + '">');
                    }
                    else {
                        h.push('<div>');
                    }
                }
                h.push('<div class="animaldragtarget" data="' + a.ID + '" style="display: inline-block; text-align: center">');
                h.push(html.animal_link(a, {showunit: true}));
                h.push('</div>');
                runningtotal += 1;
            });
            if (lastgrp != "") { 
                // Find the last total token and update it
                for (i = 0; i < h.length; i += 1) {
                    if (h[i].indexOf("##LASTTOTAL") != -1) {
                        h[i] = h[i].replace("##LASTTOTAL", runningtotal);
                    }
                }
                h.push("</div>"); 
            }
            return h.join("\n");
        },

        switch_view: function(viewmode) {
            var h = "", dragdrop = false;
            if (viewmode == "fosterer") {
                h = this.render_view("CURRENTOWNERNAME", "CURRENTOWNERNAME,ANIMALNAME", true, false);
            }
            else if (viewmode == "location") {
                h = this.render_view("DISPLAYLOCATIONNAME", "DISPLAYLOCATIONNAME,ANIMALNAME", true, false);
                dragdrop = true;
            }
            else if (viewmode == "locationspecies") {
                h = this.render_view("DISPLAYLOCATIONNAME", "DISPLAYLOCATIONNAME,SPECIESNAME,ANIMALNAME", true, false);
                dragdrop = true;
            }
            else if (viewmode == "locationunit") {
                h = this.render_view("DISPLAYLOCATIONNAME", "DISPLAYLOCATIONNAME,SHELTERLOCATIONUNIT,ANIMALNAME", true, false);
                dragdrop = true;
            }
            else if (viewmode == "species") {
                h = this.render_view("SPECIESNAME", "SPECIESNAME,ANIMALNAME", false, false);
            }
            else if (viewmode == "status") {
                h = this.render_view("ADOPTIONSTATUS", "ADOPTIONSTATUS,ANIMALNAME", false, true);
            }
            else if (viewmode == "type") {
                h = this.render_view("ANIMALTYPENAME", "ANIMALTYPENAME,ANIMALNAME", false, true);
            }
            $("#viewcontainer").html(h);
            if (dragdrop) {
                $(".animaldragtarget").draggable();
                $(".locationdroptarget").droppable({
                    over: function(event, ui) {
                        $(this).addClass("transparent");
                    },
                    out: function(event, ui) {
                        $(this).removeClass("transparent");
                    },
                    drop: function(event, ui) {
                        var locationid = $(this).attr("data");
                        var animalid = $(ui.draggable).attr("data");
                        var droptarget = $(this);
                        header.show_loading(_("Moving..."));
                        common.ajax_post("shelterview", "locationid=" + locationid + "&animalid=" + animalid, function() {
                            header.hide_loading();
                            droptarget.removeClass("transparent");
                        }, function() {
                            header.hide_loading();
                            droptarget.removeClass("transparent");
                        });
                    }
                });
            }
            common.bind_tooltips();
        },

        render: function() {
            var h = [];
            h.push('<div id="asm-content" class="ui-helper-reset ui-widget-content ui-corner-all" style="padding: 10px;">');
            h.push('<select id="viewmode" style="float: right;" class="asm-selectbox">');
            h.push('<option value="fosterer">' + _("Fosterer") + '</option>');
            h.push('<option value="location">' + _("Location") + '</option>');
            h.push('<option value="locationspecies">' + _("Location and Species") + '</option>');
            h.push('<option value="locationunit">' + _("Location and Unit") + '</option>');
            h.push('<option value="species">' + _("Species") + '</option>');
            h.push('<option value="status">' + _("Status") + '</option>');
            h.push('<option value="type">' + _("Type") + '</option>');
            h.push('</select>');
            h.push('<p class="asm-menu-category">' + config.str("Organisation") + '</p>');
            h.push('<div id="viewcontainer"></div>');
            h.push('</div>');
            return h.join("\n");
        },

        bind: function() {
            $("#viewmode").change(function(e) {
                shelterview.switch_view($("#viewmode").select("value"));
            });
        },

        sync: function() {
            $("#viewmode").select("value", config.str("ShelterViewDefault"));
            $("#viewmode").change();
        }
    };

    common.module(shelterview, "shelterview", "search");

});

/*jslint browser: true, forin: true, eqeq: true, white: true, sloppy: true, vars: true, nomen: true */
/*global $, jQuery, _, asm, common, config, controller, dlgfx, format, header, html, validate */

$(function() {

    var mode = controller.name.indexOf("lost") != -1 ? "lost" : "found";

    var lostfound_new = {

        render: function() {
            return [
                mode == "lost" ? html.content_header(_("Add lost animal")) : html.content_header(_("Add found animal")),
                '<table class="asm-table-layout">',
                '<tr>',
                '<td width="40%">',
                '<table width="100%">',
                '<tr>',
                '<td>',
                mode == "lost" ? '<label for="datelost">' + _("Date Lost") + '</label></td>' : "",
                mode == "lost" ? '<td><input type="text" id="datelost" data="datelost" class="asm-textbox asm-datebox" title="' + html.title(_("The date this animal was lost")) + '"  />' : "",
                mode == "found" ? '<label for="datefound">' + _("Date Found") + '</label></td>' : "",
                mode == "found" ? '<td><input type="text" id="datefound" data="datefound" class="asm-textbox asm-datebox" title="' + html.title(_("The date this animal was found")) + '"  />' : "",
                '</td>',
                '</tr>',
                '<tr>',
                '<td>',
                '<label for="datereported">' + _("Date Reported") + '</label></td>',
                '<td><input type="text" id="datereported" data="datereported" class="asm-textbox asm-datebox" title="' + html.title(_("The date reported to the shelter")) + '" />',
                '</td>',
                '</tr>',
                '<tr>',
                '<td><label for="agegroup">' + _("Age Group") + '</label></td>',
                '<td nowrap="nowrap">',
                '<select id="agegroup" data="agegroup" class="asm-selectbox">',
                '<option value="Unknown">' + _("(unknown)") + '</option>',
                html.list_to_options(controller.agegroups),
                '</select>',
                '</td>',
                '</tr>',
                '<tr>',
                '<td><label for="sex">' + _("Sex") + '</label></td>',
                '<td nowrap="nowrap">',
                '<select id="sex" data="sex" class="asm-selectbox">',
                html.list_to_options(controller.sexes, "ID", "SEX"),
                '</select>',
                '</td>',
                '</tr>',
                '<tr>',
                '<td><label for="species">' + _("Species") + '</label></td>',
                '<td nowrap="nowrap">',
                '<select id="species" data="species" class="asm-selectbox">',
                html.list_to_options(controller.species, "ID", "SPECIESNAME"), 
                '</select>',
                '</td>',
                '</tr>',
                '<tr>',
                '<td><label for="breed">' + _("Breed") + '</label></td>',
                '<td nowrap="nowrap">',
                '<select id="breed" data="breed" class="asm-selectbox">',
                html.list_to_options_breeds(controller.breeds),
                '</select>',
                '<select id="breedp" data="breedp" class="asm-selectbox" style="display:none;">',
                html.list_to_options_breeds(controller.breeds),
                '</select>',
                '</td>',
                '</tr>',
                '<tr>',
                '<td><label for="colour">' + _("Color") + '</label></td>',
                '<td nowrap="nowrap">',
                '<select id="colour" data="colour" class="asm-selectbox">',
                html.list_to_options(controller.colours, "ID", "BASECOLOUR"),
                '</select>',
                '</td>',
                '</tr>',
                '<tr>',
                '<td>',
                '<label for="markings">' + _("Features") + '</label></td>',
                '<td><textarea id="markings" data="markings" rows="4" class="asm-textarea" title="' + html.title(_("Any information about the animal")) + '"></textarea></td>',
                '</td>',
                '</tr>',
                '</table>',
                '</td>',
                '<td width="40%">',
                '<table width="100%">',
                '<tr>',
                '<td>',
                mode == "lost" ? '<label for="arealost">' + _("Area Lost") + '</label></td>' : "",
                mode == "lost" ? '<td><textarea id="arealost" data="arealost" rows="4" class="asm-textarea" title="' + html.title(_("Area where the animal was lost")) + '"></textarea></td>' : "",
                mode == "found" ? '<label for="areafound">' + _("Area Found") + '</label></td>' : "",
                mode == "found" ? '<td><textarea id="areafound" data="areafound" rows="4" class="asm-textarea" title="' + html.title(_("Area where the animal was found")) + '"></textarea></td>' : "",
                '</td>',
                '</tr>',
                '<tr>',
                '<td><label for="areapostcode">' + _("Zipcode") + '</label></td>',
                '<td><input id="areapostcode" data="areapostcode" type="text" class="asm-textbox" /></td>',
                '</tr>',
                '<tr>',
                '<td>',
                '<label for="comments">' + _("Comments") + '</label></td>',
                '<td><textarea id="comments" data="comments" rows="5" class="asm-textarea"></textarea></td>',
                '</td>',
                '</tr>',
                '<tr>',
                '<td>',
                '<label for="owner">' + _("Contact") + '</label></td>',
                '<td>',
                '<input id="owner" data="owner" type="hidden" class="asm-personchooser" value="" />',
                '</td>',
                '</tr>',
                '</table>',
                '</td>',
                '</tr>',
                '</table>',
                '<div class="centered">',
                '<button id="addedit">' + html.icon("animal-add") + ' ' + _("Create and edit") + '</button>',
                '<button id="add">' + html.icon("animal-add") + ' ' + _("Create") + '</button>',
                '</div>',
                html.content_footer()
            ].join("\n");
        },

        bind: function() {

            var validation = function() {
                // Remove any previous errors
                header.hide_error();
                $("label").removeClass("ui-state-error-text");

                // owner
                if ($("#owner").val() == "") {
                    header.show_error(_("Lost and found entries must have a contact"));
                    $("label[for='owner']").addClass("ui-state-error-text");
                    $("#owner").focus();
                    return false;
                }

                // date lost
                if (mode == "lost" && $.trim($("#datelost").val()) == "") {
                    header.show_error(_("Date lost cannot be blank."));
                    $("label[for='datelost']").addClass("ui-state-error-text");
                    $("#datelost").focus();
                    return false;
                }

                // date found
                if (mode == "found" && $.trim($("#datefound").val()) == "") {
                    header.show_error(_("Date found cannot be blank."));
                    $("label[for='datefound']").addClass("ui-state-error-text");
                    $("#datefound").focus();
                    return false;
                }

                // date reported
                if ($.trim($("#datereported").val()) == "") {
                    header.show_error(_("Date reported cannot be blank."));
                    $("label[for='datereported']").addClass("ui-state-error-text");
                    $("#datereported").focus();
                    return false;
                }

                return true;

            };

            var addLFAnimal = function(addmode) {
                if (!validation()) { return; }

                $(".asm-content button").button("disable");
                header.show_loading(_("Creating..."));

                var formdata = $("input, select, textarea").toPOST();
                common.ajax_post(controller.name, formdata, function(createdID) { 
                    if (addmode == "add") {
                        if (mode == "lost") {
                            header.show_info(_("Lost animal entry {0} successfully created.").replace("{0}", format.padleft(createdID, 6)));
                        }
                        else {
                            header.show_info(_("FoundLost animal entry {0} successfully created.").replace("{0}", format.padleft(createdID, 6)));
                        }
                    }
                    else {
                        if (mode == "lost") {
                            if (createdID != "0") { window.location = "lostanimal?id=" + createdID; }
                        }
                        else {
                            if (createdID != "0") { window.location = "foundanimal?id=" + createdID; }
                        }
                    }
                    $(".asm-content button").button("enable");
                    header.hide_loading();
                }, function() {
                    $(".asm-content button").button("enable");
                });
            };

            // Set select box default values
            $("#species").val(config.str("AFDefaultSpecies"));

            // Default dates
            if (mode == "lost") {
                $("#datelost").datepicker("setDate", new Date());
            }
            if (mode == "found") {
                $("#datefound").datepicker("setDate", new Date());
            }
            $("#datereported").datepicker("setDate", new Date());

            // Buttons
            $("#add").button().click(function() {
                addLFAnimal("add");
            });

            $("#addedit").button().click(function() {
                addLFAnimal("addedit");
            });

            // Only show the breeds for the selected species
            // If the species has no breeds the species is shown
            var changebreedselect1 = function() {
                $('optgroup', $('#breed')).remove();
                $('#breedp optgroup').clone().appendTo($('#breed'));

                $('#breed').children().each(function(){
                    if($(this).attr('id') != 'ngp-'+$('#species').val()){
                        $(this).remove();
                    }
                });

                if($('#breed option').size() == 0) {
                    $('#breed').append("<option value='1'>"+$('#species option:selected').text()+"</option>");
                }
            };

            changebreedselect1();

            $('#species').change(function() {
                changebreedselect1();
            });
        }
    };

    common.module(lostfound_new, "lostfound_new", "newdata");

});

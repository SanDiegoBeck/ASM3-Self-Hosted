/*jslint browser: true, forin: true, eqeq: true, white: true, sloppy: true, vars: true, nomen: true */
/*global $, jQuery, _, asm, common, config, controller, dlgfx, format, header, html, validate */

$(function() {

    var animal_new = {

        render: function() {
            return [
                '<div id="dialog-similar" style="display: none" title="' + _("Similar Animal") + '">',
                '<p><span class="ui-icon ui-icon-alert" style="float: left; margin: 0 7px 20px 0;"></span>',
                _("This animal has the same name as another animal recently added to the system.") + '<br /><br />',
                '<span class="similar-animal"></span>',
                '</p>',
                '</div>',
                html.content_header(_("Add a new animal")),
                '<table class="asm-table-layout">',
                '<tr id="coderow">',
                '<td><label for="sheltercode">' + _("Code") + '</label></td>',
                '<td nowrap="nowrap">',
                '<input type="text" id="sheltercode" data="sheltercode" class="asm-halftextbox" title="',
                html.title(_("The shelter reference number")) + '" />',
                '<input type="text" id="shortcode" data="shortcode" class="asm-halftextbox" title="',
                html.title(_("A short version of the reference number")) + '" />',
                '</td>',
                '</tr>',
                '<tr>',
                '<td>',
                '<label for="animalname">' + _("Name") + '</label>',
                '</td>',
                '<td>',
                '<input id="animalname" data="animalname" class="asm-textbox" />',
                '<button id="button-randomname">' + _("Generate a random name for this animal") + '</button>',
                '</td>',
                '</tr>',
                '<tr>',
                '<td><label for="dateofbirth">' + _("Date of Birth") + '</label></td>',
                '<td>',
                '<input id="dateofbirth" data="dateofbirth" class="asm-textbox asm-datebox" title=',
                '"' + html.title(_("The date the animal was born")) + '" />',
                ' <label for="estimatedage">' + _("or estimated age in years") + '</label> ',
                '<input type="text" id="estimatedage" data="estimatedage" class="asm-textbox asm-numberbox" value="1.0" />',
                '</td>',
                '</tr>',
                '<tr>',
                '<td>',
                '<label for="sex">' + _("Sex") + '</label>',
                '</td>',
                '<td>',
                '<select id="sex" data="sex" class="asm-selectbox">',
                html.list_to_options(controller.sexes, "ID", "SEX"),
                '</select>',
                '</td>',
                '</tr>',
                '<tr>',
                '<td>',
                '<label for="animaltype">' + _("Type") + '</label>',
                '</td>',
                '<td>',
                '<select id="animaltype" data="animaltype" class="asm-selectbox">',
                html.list_to_options(controller.animaltypes, "ID", "ANIMALTYPE"), 
                '</select>',
                '</td>',
                '</tr>',
                '<tr>',
                '<td>',
                '<label for="species">' + _("Species") + '</label>',
                '</td>',
                '<td>',
                '<select id="species" data="species" class="asm-selectbox">',
                html.list_to_options(controller.species, "ID", "SPECIESNAME"),
                '</select>',
                '</td>',
                '</tr>',
                '',
                '<tr id="breedrow">',
                '<td>',
                '<label for="breed1">' + _("Breed") + '</label>',
                '</td>',
                '<td>',
                '<select id="breed1" data="breed1" class="asm-selectbox">',
                html.list_to_options_breeds(controller.breeds),
                '</select>',
                '<select id="breedp" data="breedp" class="asm-selectbox" style="display:none;">',
                html.list_to_options_breeds(controller.breeds),
                '</select>',
                '<span id="crossbreedcol">',
                '<input id="crossbreed" data="crossbreed" type="checkbox" class="asm-checkbox" />',
                '<label for="crossbreed">' + _("Crossbreed") + '</label>',
                '</span> ',
                '<span id="secondbreedcol">',
                '<select id="breed2" data="breed2" class="asm-selectbox">',
                html.list_to_options_breeds(controller.breeds),
                '</select>',
                '</span>',
                '</td>',
                '</tr>',
                '<tr id="colourrow">',
                '<td>',
                '<label for="basecolour">' + _("Base Color") + '</label>',
                '</td>',
                '<td>',
                '<select id="basecolour" data="basecolour" class="asm-selectbox">',
                html.list_to_options(controller.colours, "ID", "BASECOLOUR"),
                '</select>',
                '</td>',
                '</tr>',
                '<tr id="locationrow">',
                '<td>',
                '<label for="internallocation">' + _("Internal Location") + '</label>',
                '</td>',
                '<td>',
                '<select id="internallocation" data="internallocation" class="asm-selectbox">',
                html.list_to_options(controller.internallocations, "ID", "LOCATIONNAME"),
                '</select>',
                '</td>',
                '</tr>',
                '<tr id="locationunitrow">',
                '<td><label for="unit">' + _("Unit") + '</label></td>',
                '<td>',
                '<input id="unit" data="unit" class="asm-textbox" title="' + html.title(_("Unit within the location, eg: pen or cage number")) + '" />',
                '</td>',
                '</tr>',
                '<tr id="sizerow">',
                '<td>',
                '<label for="size">' + _("Size") + '</label>',
                '</td>',
                '<td>',
                '<select id="size" data="size" class="asm-selectbox">',
                html.list_to_options(controller.sizes, "ID", "SIZE"),
                '</select>',
                '</td>',
                '</tr>',
                '<tr id="litterrow">',
                '<td>',
                '<label for="litterid">' + _("Litter") + '</label>',
                '</td>',
                '<td>',
                '<input id="litterid" data="litterid" class="asm-textbox" />',
                '</td>',
                '</tr>',
                '<tr id="datebroughtinrow">',
                '<td>',
                '<label for="datebroughtin">' + _("Date Brought In") + '</label>',
                '</td>',
                '<td>',
                '<input id="datebroughtin" data="datebroughtin" class="asm-textbox asm-datebox" />',
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
            // Prevent the act of enabling crossbreeds from resetting the
            // breed selects.
            var crossbreedchange = false;
            $('#crossbreed').change(function() {
                crossbreedchange = true;
            });

            // Only show the breeds for the selected species
            var changebreedselect = function() {
                if (crossbreedchange == false) {
                    $('optgroup', $('#breed1')).remove();
                    $('#breedp optgroup').clone().appendTo($('#breed1'));

                    $('#breed1').children().each(function(){
                        if($(this).attr('id') != 'ngp-'+$('#species').val()){
                            $(this).remove();
                        }
                    });

                    if($('#breed1 option').size() == 0) {
                        $('#breed1').append("<option value='-1'>"+$('#species option:selected').text()+"</option>");
                    }

                    $('optgroup', $('#breed2')).remove();
                    $('#breedp optgroup').clone().appendTo($('#breed2'));

                    $('#breed2').children().each(function(){
                        if($(this).attr('id') != 'ngp-'+$('#species').val()) {
                            $(this).remove();
                        }
                    });
                    if ($('#breed2 option').size() == 0) {
                        $('#breed2').append("<option value='-1'>"+$('#species option:selected').text()+"</option>");
                    }
                } 
                else {
                    crossbreedchange = false;
                }
            };

            var enableScreen = function() {

                changebreedselect();
                    
                $('#species').change(function() {
                    changebreedselect();
                });

                // Crossbreed flag being unset disables second breed field
                if ($("#crossbreed").is(":checked")) {
                    $("#breed2").fadeIn();
                }
                else {
                    $("#breed2").fadeOut();
                    $("#breed2").select("value", ($("#breed1").val()));
                }

                // Not having any active litters disables join litter button
                if ($("#sellitter option").size() == 0) {
                    $("#button-litterjoin").button("disable");
                }
            };

            var validation = function() {
                // Remove any previous errors
                header.hide_error();
                $("label").removeClass("ui-state-error-text");

                // code
                if (config.bool("ManualCodes")) {
                    if ($.trim($("#sheltercode").val()) == "") {
                        header.show_error(_("Shelter code cannot be blank"));
                        $("label[for='sheltercode']").addClass("ui-state-error-text");
                        $("#asm-details-accordion").accordion("option", "active", 0);
                        $("#sheltercode").focus();
                        return false;
                    }
                }

                // name
                if ($.trim($("#animalname").val()) == "") {
                    header.show_error(_("Name cannot be blank"));
                    $("label[for='animalname']").addClass("ui-state-error-text");
                    $("#asm-details-accordion").accordion("option", "active", 0);
                    $("#animalname").focus();
                    return false;
                }

                // date of birth
                if ($.trim($("#dateofbirth").val()) == "" && $.trim($("#estimatedage").val()) == "") {
                    header.show_error(_("Date of birth cannot be blank"));
                    $("label[for='dateofbirth']").addClass("ui-state-error-text");
                    $("#asm-details-accordion").accordion("option", "active", 0);
                    $("#dateofbirth").focus();
                    return false;
                }

                // crossbreed cannot have same breeds
                if ($("#crossbreed").is(":checked")) {
                    if ($("#breed1").val() == $("#breed2").val()) {
                        header.show_error(_("Crossbreed animal should have different breeds"));
                        $("#asm-details-accordion").accordion("option", "active", 0);
                        $("label[for='breed1']").addClass("ui-state-error-text");
                        $("#breed1").focus();
                        return false;
                    }
                }

                return true;
            };

            var addAnimal = function(mode) {
                if (!validation()) { return; }

                $(".asm-content button").button("disable");
                header.show_loading(_("Creating..."));

                var formdata = $("input, select").toPOST();
                common.ajax_post("animal_new", formdata, function(data) { 
                    var bits = data.split(" ");
                    var createdID = bits[0];
                    var newCode = bits[1];
                    if (mode == "add") {
                        header.show_info(_("Animal '{0}' created with code {1}").replace("{0}", $("#animalname").val()).replace("{1}", newCode));
                    }
                    else {
                        if (createdID != "0") { window.location = "animal?id=" + createdID; }
                    }
                    $(".asm-content button").button("enable");
                    header.hide_loading();
                }, function() {
                    $(".asm-content button").button("enable");
                });
            };

            var similarbuttons = {};
            similarbuttons[_("Close")] = function() { 
                $(this).dialog("close");
            };
            $("#dialog-similar").dialog({
                 autoOpen: false,
                 resizable: false,
                 modal: true,
                 width: 500,
                 dialogClass: "dialogshadow",
                 show: dlgfx.delete_show,
                 hide: dlgfx.delete_hide,
                 buttons: similarbuttons
            });

            // Check the name has not been used recently once the user leaves
            // the field.
            if (config.bool("WarnSimilarAnimalName")) {
                $("#animalname").blur(function() {
                    var formdata = "mode=recentnamecheck&animalname=" + encodeURIComponent($("#animalname").val());
                    common.ajax_post("animal_new", formdata, function(data) { 
                        if (data == "None") {
                            return;
                        }
                        var bits = data.split("|");
                        var h = "<a class='asm-embed-name' href='animal?id=" + bits[0] + "'>" + bits[1] + " - " + bits[2] + "</a>";
                        $(".similar-animal").html(h);
                        $("#dialog-similar").dialog("open");
                    }, function() {
                        $(".asm-content button").button("enable");
                    });
                });
            }

            // Disable rows based on config options
            if (!config.bool("AddAnimalsShowSize")) { $("#sizerow").hide(); }
            if (!config.bool("AddAnimalsShowBreed")) { $("#breedrow").hide(); }
            if (!config.bool("AddAnimalsShowColour")) { $("#colourrow").hide(); }
            if (!config.bool("AddAnimalsShowLocation")) { $("#locationrow").hide(); }
            if (!config.bool("AddAnimalsShowLocationUnit")) { $("#locationunitrow").hide(); }
            if (!config.bool("AddAnimalsShowAcceptance")) { $("#litterrow").hide(); }
            if (!config.bool("AddAnimalsShowDateBroughtIn")) { $("#datebroughtinrow").hide(); }
            if (config.bool("UseSingleBreedField")) {
                $("#crossbreedcol").hide();
                $("#secondbreedcol").hide();
            }
            if (config.bool("DisableShortCodesControl")) {
                $("#shortcode").hide();
                $("#sheltercode").addClass("asm-textbox");
                $("#sheltercode").removeClass("asm-halftextbox");
            }
            if (!config.bool("ManualCodes")) { $("#coderow").hide(); }


            // Set select box default values
            $("#animaltype").val(config.str("AFDefaultType"));
            $("#species").val(config.str("AFDefaultSpecies"));
            $("#basecolour").val(config.str("AFDefaultColour"));
            $("#internallocation").val(config.str("AFDefaultLocation"));
            $("#size").val(config.str("AFDefaultSize"));

            // Keep breed2 in sync with breed1 for non-crossbreeds
            $("#breed1").change(function() {
                if (!$("#crossbreed").is(":checked")) {
                    $("#breed2").select("value", $("#breed1").select("value"));
                }
            });

            // Litter autocomplete
            $("#litterid").autocomplete({source: html.decode(controller.autolitters)});

            $("#crossbreed").change(enableScreen);
            enableScreen();

            // The species will have updated the breedlist, apply defaults
            $("#breed1").val(config.str("AFDefaultBreed"));
            $("#breed2").val(config.str("AFDefaultBreed"));

            // Buttons
            $("#add").button().click(function() {
                addAnimal("add");
            });

            $("#addedit").button().click(function() {
                addAnimal("addedit");
            });

            $("#button-randomname")
                .button({ icons: { primary: "ui-icon-tag" }, text: false })
                .click(function() {
                var formdata = "mode=randomname&sex=" + $("#sex").val();
                common.ajax_post("animal", formdata, function(result) { $("#animalname").val(result); });
            });
        }
    };

    common.module(animal_new, "animal_new", "newdata");

});

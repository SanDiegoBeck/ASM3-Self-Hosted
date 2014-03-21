/*jslint browser: true, forin: true, eqeq: true, white: true, sloppy: true, vars: true, nomen: true */
/*global $, _, asm, avid, common, config, controller, dlgfx, additional, edit_header, format, header, html, validate */

$(function() {

    var animal = {

        render_death: function() {
            return [
                '<h3><a href="#">' + _("Death") + ' <img id="tabdeath" style="display: none" class="asm-icon asm-icon-death"></span></a></h3><div>',
                '<table class="additionaltarget" data="to6">',
                '<tr>',
                '<td>',
                '<label for="deceaseddate">' + _("Deceased Date") + '</label>',
                '</td>',
                '<td>',
                '<input class="asm-textbox asm-datebox" id="deceaseddate" data-json="DECEASEDDATE" data-post="deceaseddate" title="' + html.title(_("The date the animal died")) + '" />',
                '</td>',
                '</tr>',
                '<tr>',
                '<td>',
                '<label for="deathcategory">' + _("Category") + '</label>',
                '</td>',
                '<td>',
                '<select class="asm-selectbox" id="deathcategory" data-json="PTSREASONID" data-post="deathcategory">',
                html.list_to_options(controller.deathreasons, "ID", "REASONNAME"),
                '</select>',
                '</td>',
                '</tr>',
                '<tr>',
                '<td colspan="2">',
                '<label for="puttosleep">' + _("Euthanized") + '</label>',
                '<input class="asm-checkbox" type="checkbox" id="puttosleep" data-json="PUTTOSLEEP" data-post="puttosleep" title="' + html.title(_("This animal was euthanized")) + '" />',
                '<label for="deadonarrival">' + _("Dead on arrival") + '</label>',
                '<input class="asm-checkbox" type="checkbox" id="deadonarrival" data-json="ISDOA" data-post="deadonarrival" title="' + html.title(_("This animal was dead on arrival to the shelter")) + '" />',
                '<label for="diedoffshelter">' + _("Died off shelter") + '</label>',
                '<input class="asm-checkbox" type="checkbox" id="diedoffshelter" data-json="DIEDOFFSHELTER" data-post="diedoffshelter" title="',
                html.title(_("This animal died outside the care of the shelter, and the death should be kept out of reports")) + '" />',
                '</td>',
                '</tr>',
                '</table>',
                '<div>',
                _("Notes") + '<br />',
                '<textarea class="asm-textarea" title="' + html.title(_("Notes about the death of the animal")) + '" id="ptsreason" data-json="PTSREASON" data-post="ptsreason" rows="8"></textarea>',
                '</div>',
                '</div>'
            ].join("\n");
        },

        render_details: function() {
            return [
                '<h3><a href="#">' + _("Details") + '</a></h3>',
                '<div>',
                '<table width="100%">',
                '<tr>',
                '<!-- left table -->',
                '<td width="40%">',
                '<table>',
                '<tr>',
                '<td><label for="sheltercode">' + _("Code") + '</label></td>',
                '<td nowrap="nowrap">',
                '<input type="text" id="sheltercode" data-json="SHELTERCODE" data-post="sheltercode" class="asm-halftextbox" title="' + html.title(_("The shelter reference number")) + '"  />',
                '<input type="text" id="shortcode" data-json="SHORTCODE" data-post="shortcode" class="asm-halftextbox" title="' + html.title(_("A short version of the reference number")) + '" />',
                '<input type="hidden" id="yearcode" data-json="YEARCODEID" data-post="yearcode" />',
                '<input type="hidden" id="uniquecode" data-json="UNIQUECODEID" data-post="uniquecode" />',
                '</td>',
                '<td>',
                '<button id="button-gencode">' + _("Generate a new animal code") + '</button>',
                '</td>',
                '</tr>',
                '<tr id="litteridrow">',
                '<td>',
                '<label for="litterid">' + _("Litter") + '</label></td>',
                '<td><input type="text" id="litterid" data-json="ACCEPTANCENUMBER" data-post="litterid" class="asm-textbox" title="' + html.title(_("The litter this animal belongs to")) + '" />',
                '</td>',
                '</tr>',
                '<tr>',
                '<td><label for="animalname">' + _("Name") + '</label></td>',
                '<td><input type="text" id="animalname" data-json="ANIMALNAME" data-post="animalname" maxlength="255" class="asm-textbox" title="' + html.title(_("The animal name")) + '" />',
                '</td>',
                '<td>',
                '<button id="button-randomname">' + _("Generate a random name for this animal") + '</button>',
                '</td>',
                '</tr>',
                '<tr>',
                '<td><label for="sex">' + _("Sex") + '</label></td>',
                '<td><select id="sex" data-json="SEX" data-post="sex" class="asm-selectbox" title="' + html.title(_("The animal sex")) + '">',
                html.list_to_options(controller.sexes, "ID", "SEX"),
                '</select></td>',
                '</tr>',
                '<tr>',
                '<td><label for="animaltype">' + _("Type") + '</label></td>',
                '<td><select id="animaltype" data-json="ANIMALTYPEID" data-post="animaltype" class="asm-selectbox" title="' + html.title(_("The shelter category for this animal")) + '">',
                html.list_to_options(controller.animaltypes, "ID", "ANIMALTYPE"),
                '</select></td>',
                '</tr>',
                '<tr>',
                '<td><label for="basecolour">' + _("Color") + '</label></td>',
                '<td><select id="basecolour" data-json="BASECOLOURID" data-post="basecolour" class="asm-selectbox" title="' + html.title(_("The base color of this animal")) + '">',
                html.list_to_options(controller.colours, "ID", "BASECOLOUR"),
                '</select></td>',
                '</tr>',
                '<tr id="coattyperow">',
                '<td><label for="coattype">' + _("Coat Type") + '</label></td>',
                '<td><select id="coattype" data-json="COATTYPE" data-post="coattype" class="asm-selectbox" title="' + html.title(_("The coat type of this animal")) + '">',
                html.list_to_options(controller.coattypes, "ID", "COATTYPE"),
                '</select></td>',
                '</tr>',
                '</table>',
                '<!-- right table -->',
                '<td>',
                '<table>',
                '<tr>',
                '<td>',
                '<!-- second column-->',
                '<table class="additionaltarget" data="to2">',
                '<tr id="sizerow">',
                '<td><label for="size">' + _("Size") + '</label></td>',
                '<td><select id="size" data-json="SIZE" data-post="size" class="asm-selectbox" title="' + html.title(_("The size of this animal")) + '">',
                html.list_to_options(controller.sizes, "ID", "SIZE"),
                '</select></td>',
                '</tr>',
                '<tr>',
                '<td><label for="species">' + _("Species") + '</label></td>',
                '<td><select id="species" data-json="SPECIESID" data-post="species" class="asm-selectbox" title="' + html.title(_("The species of this animal")) + '">',
                html.list_to_options(controller.species, "ID", "SPECIESNAME"),
                '</select></td>',
                '</tr>',
                '<tr>',
                '<td><label for="breed1">' + _("Breed") + '</label></td>',
                '<td><select id="breed1" data-json="BREEDID" data-post="breed1" class="asm-selectbox" title="' + html.title(_("The primary breed of this animal")) + '">',
                html.list_to_options_breeds(controller.breeds),
                '</select>',
                '<select id="breedp" class="asm-selectbox" style="display:none;">',
                html.list_to_options_breeds(controller.breeds),
                '</select></td>',
                '</tr>',
                '<tr id="secondbreedrow">',
                '<td><label for="crossbreed">' + _("Crossbreed") + '</label>',
                '<input type="checkbox" class="asm-checkbox" id="crossbreed" data-json="CROSSBREED" data-post="crossbreed" title="' + _("This animal is a crossbreed") + '" /></td>',
                '<td><select id="breed2" data-json="BREED2ID" data-post="breed2" class="asm-selectbox" title="' + html.title(_("The secondary breed of this animal")) + '">',
                html.list_to_options_breeds(controller.breeds),
                '</select></td>',
                '</tr>',
                '<tr id="locationrow">',
                '<td><label for="location">' + _("Location") + '</label></td>',
                '<td>',
                '<input id="archived" data-json="ARCHIVED" type="hidden" />',
                '<input id="displaylocationname" data-json="DISPLAYLOCATIONNAME" type="hidden" />',
                '<select id="location" data-json="SHELTERLOCATION" data-post="location" class="asm-selectbox" title="' + html.title(_("Where this animal is located within the shelter")) + '">',
                html.list_to_options(controller.internallocations, "ID", "LOCATIONNAME"),
                '</select></td>',
                '</tr>',
                '<tr id="locationunitrow">',
                '<td><label for="unit">' + _("Unit") + '</label></td>',
                '<td>',
                '<input id="unit" data-json="SHELTERLOCATIONUNIT" data-post="unit" class="asm-textbox" title="' + html.title(_("Unit within the location, eg: pen or cage number")) + '" />',
                '</td>',
                '</tr>',
                '<tr id="lastlocation">',
                '<td><label>' + _("Last Location") + '</label></td>',
                '<td>',
                '<a class="asm-embed-name" href="animal_find_results?logicallocation=onshelter&shelterlocation=' + controller.animal.SHELTERLOCATION + '">' + controller.animal.SHELTERLOCATIONNAME + ' ' + common.nulltostr(controller.animal.SHELTERLOCATIONUNIT) + '</a>',
                '</td>',
                '</tr>',
                '<tr>',
                '<td><label for="dateofbirth">' + _("Date of Birth") + '</label></td>',
                '<td><input id="dateofbirth" data-json="DATEOFBIRTH" data-post="dateofbirth" class="asm-datebox asm-halftextbox" title="' + _("The date the animal was born") + '" />',
                '<input class="asm-checkbox" type="checkbox" id="estimateddob" data-json="ESTIMATEDDOB" data-post="estimateddob" title="' + _("This date of birth is an estimate") + '" />',
                _("Estimate"),
                '</td>',
                '</tr>',
                '<!-- end second column -->',
                '</table>',
                '</td>',
                '</tr>',
                '<!-- end right table -->',
                '</table>',
                '</td>',
                '<!-- final column holds flags -->',
                '<td id="onshelterflags">',
                '<span style="white-space: nowrap">',
                '<input class="asm-checkbox" type="checkbox" id="nonshelter" data-json="NONSHELTERANIMAL" data-post="nonshelter" title=',
                '"' + html.title(_("This animal should not be shown in figures and is not in the custody of the shelter")) + '" />',
                '<label for="nonshelter" class="asm-search-nonshelter">' + _("Non-Shelter") + '</label>',
                '</span>',
                '<br />',
                '<span style="white-space: nowrap">',
                '<input class="asm-checkbox" type="checkbox" id="notforadoption" data-json="ISNOTAVAILABLEFORADOPTION" data-post="notforadoption" title=',
                '"' + html.title(_("This animal should not be included when publishing animals for adoption")) + '" />',
                '<label for="notforadoption" class="asm-search-notforadoption">' + _("Not For Adoption") + '</label>',
                '</span>',
                '<br />',
                '<span style="white-space: nowrap">',
                '<input class="asm-checkbox" type="checkbox" id="hold" data-json="ISHOLD" data-post="hold" title=',
                '"' + html.title(_("This animal should be held in case it is reclaimed")) + '" />',
                '<label for="hold">' + _("Hold until") + '</label>',
                '<input class="asm-halftextbox asm-datebox" id="holduntil" data-json="HOLDUNTILDATE" data-post="holduntil" title=',
                '"' + html.title(_("Hold the animal until this date or blank to hold indefinitely")) + '" />',
                '</span>',
                '<br/>',
                '<span style="white-space: nowrap">',
                '<input class="asm-checkbox" type="checkbox" id="quarantine" data-json="ISQUARANTINE" data-post="quarantine" title=',
                '"' + html.title(_("This animal is quarantined")) + '" />',
                '<label for="quarantine">' + _("Quarantine") + '</label>',
                '</span>',
                '<br />',
                '<span style="white-space: nowrap">',
                '<input class="asm-checkbox" type="checkbox" id="crueltycase" data-json="CRUELTYCASE" data-post="crueltycase" title=',
                '"' + html.title(_("This animal is part of a cruelty case against an owner")) + '" />',
                '<label for="crueltycase">' + _("Cruelty Case") + '</label>',
                '</span>',
                '</td>',
                '<!-- end outer table -->',
                '</tr>',
                '</table>',
                '</div>'
            ].join("\n");
        },

        render_entry: function() {
            return [
                '<h3><a href="#">' + _("Entry") + '</a></h3>',
                '<div>',
                '<!-- outer table -->',
                '<table width="100%">',
                '<tr>',
                '<td width="50%">',
                '<!-- left table -->',
                '<table width="100%">',
                '<tr>',
                '<td valign="top" class="bottomborder">',
                '<label for="originalowner">' + _("Original Owner") + '</label>',
                '</td>',
                '<td valign="top" class="bottomborder">',
                '<input id="originalowner" data-json="ORIGINALOWNERID" data-post="originalowner" type="hidden" class="asm-personchooser" />',
                '</td>',
                '</tr>',
                '<tr>',
                '<td valign="top">',
                '<label for="broughtinby">' + _("Brought In By") + '</label>',
                '</td>',
                '<td valign="top">',
                '<input id="broughtinby" data-json="BROUGHTINBYOWNERID" data-post="broughtinby" type="hidden" class="asm-personchooser" />',
                '</td>',
                '</tr>',
                '</table>',
                '<!-- right table -->',
                '</td>',
                '<td width="50%">',
                '<table width="100%" class="additionaltarget" data="to4">',
                '<tr id="datebroughtinrow">',
                '<td>',
                '<label for="datebroughtin">' + _("Date Brought In") + '</label>',
                '</td>',
                '<td>',
                '<input id="datebroughtin" data-json="DATEBROUGHTIN" data-post="datebroughtin" class="asm-textbox asm-datebox" title="' + html.title(_("The date the animal was brought into the shelter")) + '" />',
                '</td>',
                '</tr>',
                '<tr id="entryreasonrow">',
                '<td><label for="entryreason">' + _("Entry Category") + '</label></td>',
                '<td><select id="entryreason" data-json="ENTRYREASONID" data-post="entryreason" class="asm-selectbox" title=',
                '"' + html.title(_("The entry reason for this animal")) + '">',
                html.list_to_options(controller.entryreasons, "ID", "REASONNAME"),
                '</select></td>',
                '</tr>',
                '<tr class="asilomar">',
                '<td><label for="asilomarintakecategory">' + "Asilomar Category" + '</label></td>',
                '<td><select id="asilomarintakecategory" data-json="ASILOMARINTAKECATEGORY" data-post="asilomarintakecategory" class="asm-selectbox">',
                '<option value="0">Healthy</option>',
                '<option value="1">Treatable - Rehabilitatable</option>',
                '<option value="2">Treatable - Manageable</option>',
                '<option value="3">Unhealthy and Untreatable</option>',
                '</select></td>',
                '</tr>',
                '<tr id="transferinrow">',
                '<td></td>',
                '<td>',
                '<input class="asm-checkbox" type="checkbox" id="transferin" data-json="ISTRANSFER" data-post="transferin" title=',
                '"' + html.title(_("This animal was transferred from another shelter")) + '" />',
                '<label for="transferin">' + _("Transfer In") + '</label>',
                '</td>',
                '</tr>',
                '<tr class="asilomar">',
                '<td></td>',
                '<td>',
                '<input class="asm-checkbox" type="checkbox" id="asilomartransferexternal" data-json="ASILOMARISTRANSFEREXTERNAL" data-post="asilomartransferexternal" title=',
                '"' + html.title("This animal was transferred in from outside the community/coalition") + '" />',
                '<label for="asilomartransferexternal">' + "Outside community/coalition" + '</label>',
                '</td>',
                '</tr>',
                '<tr class="asilomar">',
                '<td></td>',
                '<td>',
                '<input class="asm-checkbox asilomar" type="checkbox" id="asilomarownerrequested" data-json="ASILOMAROWNERREQUESTEDEUTHANASIA" data-post="asilomarownerrequested" title="' + html.title("The owner requested euthanasia") + '" />',
                '<label class="asilomar" for="asilomarownerrequested">' + "Owner requested euthanasia" + '</label>',
                '</td></tr>',
                '<tr id="bondedwith1row">',
                '<td>',
                '<label for="bonded1">' + _("Bonded With") + '</label>',
                '</td>',
                '<td>',
                '<input id="bonded1" data-json="BONDEDANIMALID" data-post="bonded1" type="hidden" class="asm-animalchooser" />',
                '</td>',
                '</tr>',
                '<tr id="bondedwith2row">',
                '<td></td>',
                '<td>',
                '<input id="bonded2" data-json="BONDEDANIMAL2ID" data-post="bonded2" type="hidden" class="asm-animalchooser" />',
                '</td>',
                '</tr>',
                '<tr id="reasonnotfromownerrow">',
                '<td>',
                '<label for="reasonnotfromowner">' + _("Reason not from Owner") + '</label>',
                '</td>',
                '<td>',
                '<textarea class="asm-textarea" id="reasonnotfromowner" title="' + html.title(_("Reason the owner did not bring in the animal themselves")) + '" ',
                'data-json="REASONNO" data-post="reasonnotfromowner" rows="2"></textarea>',
                '</td>',
                '</tr>',
                '<tr id="reasonforentryrow">',
                '<td>',
                '<label for="reasonforentry">' + _("Reason for Entry") + '</label>',
                '</td>',
                '<td>',
                '<textarea class="asm-textarea" title="' + _("Reason for entry") + '" id="reasonforentry" data-json="REASONFORENTRY" data-post="reasonforentry" rows="2"></textarea>',
                '</td>',
                '</tr>',
                '</table>',
                '<!-- end outer table -->',
                '</td>',
                '</tr>',
                '</table>',
                '</div>'
            ].join("\n");
        },

        render_health_and_identification: function() {
            return [
                '<h3><a href="#">' + _("Health and Identification") + ' <span id="tabvet" style="display: none" class="asm-icon asm-icon-health"></span></a></h3><div>',
                '<!-- Outer table -->',
                '<table width="100%">',
                '<tr>',
                '<td>',
                '<!-- Tested flags -->',
                '<table>',
                '<tr id="microchiprow">',
                '<td nowrap="nowrap">',
                '<input class="asm-checkbox" type="checkbox" id="microchipped" data-json="IDENTICHIPPED" data-post="microchipped" title="' + html.title(_("This animal is microchipped")) + '" />',
                '<label for="microchipped">' + _("Microchipped") + '</label>',
                '</td>',
                '<td>',
                '<input id="microchipdate" data-json="IDENTICHIPDATE" data-post="microchipdate" class="asm-halftextbox asm-datebox" title="' + html.title(_("The date the animal was microchipped")) + '" />',
                '</td>',
                '<td>',
                '<input type="text" id="microchipnumber" data-json="IDENTICHIPNUMBER" data-post="microchipnumber" class="asm-textbox" title="' + html.title(_("The microchip number")) + '" />',
                '<button id="button-avid">Update AVID PETtrac with new information for this animal and its current owner</button>',
                '</td>',
                '</tr>',
                '<tr id="tattoorow">',
                '<td>',
                '<input class="asm-checkbox" type="checkbox" id="tattoo" data-json="TATTOO" data-post="tattoo" title="' + html.title(_("This animal has a tattoo")) + '" />',
                '<label for="tattoo">' + _("Tattoo") + '</label>',
                '</td>',
                '<td>',
                '<input id="tattoodate" data-json="TATTOODATE" data-post="tattoodate" class="asm-halftextbox asm-datebox" title="' + html.title(_("The date the animal was tattooed")) + '" />',
                '</td>',
                '<td>',
                '<input type="text" id="tattoonumber" data-json="TATTOONUMBER" data-post="tattoonumber" class="asm-textbox" title="' + html.title(_("The tattoo number")) + '" />',
                '</td>',
                '</tr>',
                '<tr id="smarttagrow">',
                '<td>',
                '<input class="asm-checkbox" type="checkbox" id="smarttag" data-json="SMARTTAG" data-post="smarttag" title="' + html.title(_("This animal has a SmartTag PETID")) + '" />',
                '<label for="smarttag">' + _("SmartTag PETID") + '</label>',
                '</td>',
                '<td>',
                '<input id="smarttagnumber" data-json="SMARTTAGNUMBER" data-post="smarttagnumber" class="asm-halftextbox asm-alphanumberbox" title="' + html.title(_("The SmartTag PETID number")) + '" />',
                '</td>',
                '<td>',
                '<select class="asm-selectbox" id="smarttagtype" data-json="SMARTTAGTYPE" data-post="smarttagtype" title="' + html.title(_("The SmartTag type")) + '">',
                '<option value="0">' + _("Annual") + '</option>',
                '<option value="1">' + _("5 Year") + '</option>',
                '<option value="2">' + _("Lifetime") + '</option>',
                '</select>',
                '</td>',
                '</tr>',
                '<tr id="neuterrow">',
                '<td>',
                '<input class="asm-checkbox" type="checkbox" id="neutered" data-json="NEUTERED" data-post="neutered" title="' + html.title(_("This animal has been altered")) + '" />',
                '<label for="neutered">' + _("Altered") + '</label>',
                '</td>',
                '<td>',
                '<input id="neutereddate" data-json="NEUTEREDDATE" data-post="neutereddate" class="asm-halftextbox asm-datebox" title="' + html.title(_("The date the animal was altered")) + '" />',
                '</td>',
                '</tr>',
                '<tr>',
                '<td>',
                '<input class="asm-checkbox" type="checkbox" id="declawed" data-json="DECLAWED" data-post="declawed" title="' + html.title(_("This animal has been declawed")) + '" />',
                '<label id="declawed-label" for="declawed">' + _("Declawed") + '</label>',
                '</td>',
                '</tr>',
                '<tr id="heartwormrow">',
                '<td>',
                '<input class="asm-checkbox" type="checkbox" id="heartwormtested" data-json="HEARTWORMTESTED" data-post="heartwormtested" title="' + html.title(_("This animal has been heartworm tested")) + '" />',
                '<label for="heartwormtested">' + _("Heartworm Tested") + '</label>',
                '</td>',
                '<td>',
                '<input id="heartwormtestdate" data-json="HEARTWORMTESTDATE" data-post="heartwormtestdate" class="asm-halftextbox asm-datebox" title="' + html.title(_("The date the animal was heartworm tested")) + '" />',
                '</td>',
                '<td>',
                '<select class="asm-selectbox" id="heartwormtestresult" data-json="HEARTWORMTESTRESULT" data-post="heartwormtestresult" title="' + html.title(_("The result of the heartworm test")) + '">',
                html.list_to_options(controller.posneg, "ID", "NAME"),
                '</select>',
                '</td>',
                '</tr>',
                '<tr id="fivlrow">',
                '<td>',
                '<input class="asm-checkbox" type="checkbox" id="fivltested" data-json="COMBITESTED" data-post="fivltested" title="' + html.title(_("This animal has been FIV/L tested")) + '" />',
                '<label for="fivltested">' + _("FIV/L Tested") + '</label>',
                '</td>',
                '<td>',
                '<input id="fivltestdate" data-json="COMBITESTDATE" data-post="fivltestdate" class="asm-halftextbox asm-datebox" title="' + html.title(_("The date the animal was FIV/L tested")) + '" />',
                '</td>',
                '<td>',
                '<select class="asm-halftextbox selectbox" id="fivresult" data-json="COMBITESTRESULT" data-post="fivresult" title="' + html.title(_("The result of the FIV test")) + '">',
                html.list_to_options(controller.posneg, "ID", "NAME"),
                '</select>',
                '<select class="asm-halftextbox selectbox" id="flvresult" data-json="FLVRESULT" data-post="flvresult" title="' + html.title(_("The result of the FLV test")) + '">',
                html.list_to_options(controller.posneg, "ID", "NAME"),
                '</select>',
                '</td>',
                '</tr>',

                '<tr>',
                '<td>',
                '<input class="asm-checkbox" type="checkbox" id="specialneeds" data-json="HASSPECIALNEEDS" data-post="specialneeds" title="' + _("This animal has special needs") + '"  />',
                '<label for="specialneeds">' + _("Special Needs") + '</label>',
                '</td>',
                '</tr>',
                '<!-- end flag table -->',
                '</table>',
                '<!-- separate table for additional fields -->',
                '<table class="additionaltarget" data="to5">',
                '<tr id="rabiestagrow">',
                '<td><label for="rabiestag">' + _("Rabies Tag") + '</label></td>',
                '<td><input id="rabiestag" data-json="RABIESTAG" data-post="rabiestag" class="asm-textbox" maxlength="20" />',
                '</td>',
                '</tr>',
                '</table>',
                '</td>',
                '<td>',
                '<!-- health problems/vet fields -->',
                '<label for="healthproblems">' + _("Health Problems") + '</label><br />',
                '<textarea id="healthproblems" title="' + html.title(_("Any health problems the animal has")) + '" data-json="HEALTHPROBLEMS" data-post="healthproblems" class="asm-textarea" rows="4"></textarea>',
                '<table>',
                '</table>',
                '<table>',
                '<tr>',
                '<td valign="top" class="bottomborder">',
                '<label for="currentvet">' + _("Current Vet") + '</label>',
                '</td>',
                '<td valign="top" class="bottomborder">',
                '<input id="currentvet" data-json="CURRENTVETID" data-post="currentvet" type="hidden" data-filter="vet" class="asm-personchooser" />',
                '</td>',
                '</tr>',
                '<tr>',
                '<td valign="top">',
                '<label for="ownersvet">' + _("Owners Vet") + '</label>',
                '</td>',
                '<td valign="top">',
                '<input id="ownersvet" data-json="OWNERSVETID" data-post="ownersvet" type="hidden" data-filter="vet" class="asm-personchooser"  />',
                '</td>',
                '</tr>',
                '</table>',
                '<!-- end outer table -->',
                '</td>',
                '</tr>',
                '</table>',
                '</div>'
            ].join("\n");
        },

        render_notes: function() {
            return [
                '<h3><a href="#">' + _("Notes") + '</a></h3>',
                '<div>',
                '<!-- Outer table -->',
                '<table width="100%">',
                '<tr>',
                '<td>',
                '<!-- Comments table -->',
                '<table>',
                '<tr id="markingsrow">',
                '<td>',
                '<label for="markings">' + _("Markings") + '</label>',
                '</td>',
                '<td width="80%">',
                '<textarea class="asm-textarea" title="' + html.title(_("Any markings or distinguishing features the animal has")) + '" id="markings" data-json="MARKINGS" data-post="markings" rows="3"></textarea>',
                '</td>',
                '</tr>',
                '<tr id="hiddencommentsrow">',
                '<td>',
                '<label for="hiddencomments">' + _("Hidden Comments") + '</label>',
                '</td>',
                '<td>',
                '<textarea class="asm-textarea" title="' + html.title(_("Hidden comments about the animal")) + '" id="hiddencomments" data-json="HIDDENANIMALDETAILS" data-post="hiddencomments" rows="3"></textarea>',
                '</td>',
                '</tr>',
                '<tr id="commentsrow">',
                '<td>',
                '<label for="comments">' + _("Comments") + '</label>',
                '<button id="button-commentstomedia">' + _('Copy animal comments to the notes field of the web preferred media for this animal') + '</button>',
                '</td>',
                '<td>',
                '<textarea class="asm-textarea" title="' + html.title(_("Comments")) + '" id="comments" data-json="ANIMALCOMMENTS" data-post="comments" rows="3"></textarea>',
                '</td>',
                '</tr>',
                '</table>',
                '</td>',
                '<td>',
                '<!-- Good with table -->',
                '<table id="goodwithrow" class="additionaltarget" data="to3">',
                '<tr>',
                '<td>',
                '<label for="goodwithcats">' + _("Good with cats") + '</label>',
                '</td>',
                '<td>',
                '<select class="asm-selectbox" id="goodwithcats" data-json="ISGOODWITHCATS" data-post="goodwithcats">',
                html.list_to_options(controller.ynun, "ID", "NAME"),
                '</select>',
                '</td>',
                '</tr>',
                '<tr>',
                '<td>',
                '<label for="goodwithdogs">' + _("Good with dogs") + '</label>',
                '</td>',
                '<td>',
                '<select class="asm-selectbox" id="goodwithdogs" data-json="ISGOODWITHDOGS" data-post="goodwithdogs">',
                html.list_to_options(controller.ynun, "ID", "NAME"),
                '</select>',
                '</td>',
                '</tr>',
                '<tr>',
                '<td>',
                '<label for="goodwithkids">' + _("Good with kids") + '</label>',
                '</td>',
                '<td>',
                '<select class="asm-selectbox" id="goodwithkids" data-json="ISGOODWITHCHILDREN" data-post="goodwithkids">',
                html.list_to_options(controller.ynun, "ID", "NAME"),
                '</select>',
                '</td>',
                '</tr>',
                '<tr>',
                '<td>',
                '<label for="housetrained">' + _("Housetrained") + '</label>',
                '</td>',
                '<td>',
                '<select class="asm-selectbox" id="housetrained" data-json="ISHOUSETRAINED" data-post="housetrained">',
                html.list_to_options(controller.ynun, "ID", "NAME"),
                '</select>',
                '</td>',
                '</tr>',
                '<!-- end good with -->',
                '</table>',
                '<!-- end outer table -->',
                '</td>',
                '</tr>',
                '</table>',
                '</div>'
            ].join("\n");
        },

        /**
         * Render the animal details screen
         */
        render: function() {
            var h = [
                '<div id="button-document-body" class="asm-menu-body">',
                '<ul class="asm-menu-list">',
                edit_header.template_list(controller.templates, "ANIMAL", controller.animal.ID),
                '</ul>',
                '</div>',
                '<div id="button-diarytask-body" class="asm-menu-body">',
                '<ul class="asm-menu-list">',
                edit_header.diary_task_list(controller.diarytasks, "ANIMAL"),
                '</ul>',
                '</div>',
                '<div id="dialog-dt-date" style="display: none" title="' + _("Select date for diary task") + '">',
                '<input type="hidden" id="diarytaskid" />',
                '<table width="100%">',
                '<tr>',
                '<td><label for="seldate">' + _("Date") + '</label></td>',
                '<td><input id="seldate" type="text" class="asm-textbox asm-datebox" /></td>',
                '</tr>',
                '</table>',
                '</div>',
                '<div id="dialog-delete" style="display: none" title="' + _("Delete") + '">',
                    '<p><span class="ui-icon ui-icon-alert" style="float: left; margin: 0 7px 20px 0;"></span>' + _("This will permanently remove this animal, are you sure?") + '</p>',
                '</div>',
                '<div id="dialog-avid" style="display: none" title="AVID/PetTRAC Microchip Registration">',
                    '<div id="avid"></div>',
                '</div>',
                edit_header.animal_edit_header(controller.animal, "animal", controller.tabcounts),
                '<div class="asm-toolbar">',
                '<table>',
                '<tr>',
                    '<td><button id="button-save" title="' + _("Save this animal") + '">' + html.icon("save") + ' ' + _("Save") + '</button></td>',
                    '<td><button id="button-clone" title="' + _("Create a new animal by copying this one") + '">' + html.icon("copy") + ' ' + _("Clone") + '</button></td>',
                    '<td><button id="button-delete" title="' + _("Delete this animal") + '">' + html.icon("animal-delete") + ' ' + _("Delete") + '</button></td>',
                    '<td><span id="button-document" title="' + _("Generate a document from this animal") + '" class="asm-menu-icon">' + html.icon("document") + ' ' + _("Document") + '</span></td>',
                    '<td><span id="button-diarytask" title="' + _("Create diary notes from a task") + '" class="asm-menu-icon">' + html.icon("diary-task") + ' ' + _("Diary Task") + '</span></td>',
                    '<td><button id="button-match" title="' + _("Match this animal with the lost and found database") + '">' + html.icon("match") + ' ' + _("Match") + '</button></td>',
                    '<td><button id="button-littermates" title="' + _("View littermates") + '">' + html.icon("litter") + ' ' + _("Littermates") + '</button></td>',
                    '<td><button id="button-facebook" title="' + _("Share this animal on Facebook") + '">' + html.icon("facebook") + ' ' + _("Facebook") + '</button></td>',
                '</tr>',
                '</table>',
                '</div>',
                '<div id="asm-details-accordion">',
                animal.render_details(),
                animal.render_notes(),
                '<h3><a href="#">' + _("Additional") + '</a></h3>',
                '<div>',
                additional.additional_fields(controller.additional),
                '</div>',
                animal.render_entry(),
                animal.render_health_and_identification(),
                animal.render_death(),
                '</div> <!-- accordion -->',
                '</div> <!-- asmcontent -->',
                '</div> <!-- tabs -->'
            ].join("\n");
            return h;
        },

        /** Prevents enabling crossbreeds from resetting the breed select boxes */
        crossbreedchange: false,

        /* Update the breed selects to only show the breeds for the selected species.
         * If no breeds are available the species will be displayed.
         * */
        update_breed_list: function() {
            if (animal.crossbreedchange == false) {
                $('#breed1 optgroup').remove();
                $('#ngp-' + $("#species").val()).clone().appendTo($('#breed1'));
                $('#breed2 optgroup').remove();
                $('#ngp-' + $("#species").val()).clone().appendTo($('#breed2'));
                if($('#breed1 option').size() == 0) {
                    $('#breed1').append("<option value='-1'>"+$('#species option:selected').text()+"</option>");
                }
                if($('#breed2 option').size() == 0) {
                    $('#breed2').append("<option value='-1'>"+$('#species option:selected').text()+"</option>");
                }
            } 
            else {
                animal.crossbreedchange = false;
            }
        },

        /** 
         *  Enable widgets based on loaded data, security and configuration options
         */
        enable_widgets: function() {

            // DATA ===========================================

            // Hide additional accordion section if there aren't
            // any additional fields declared
            var ac = $("#ui-accordion-asm-details-accordion-header-2");
            var an = ac.next();
            if (an.find(".additional").length == 0) {
                ac.hide(); an.hide();
            }
            
            // Crossbreed flag being unset hides second breed field
            if ($("#crossbreed").is(":checked")) {
                $("#breed2").fadeIn();
            }
            else {
                $("#breed2").fadeOut();
                $("#breed2").select("value", $("#breed1").select("value"));
            }
            
            // Show/hide death fields based on deceased date
            if ($("#deceaseddate").val() == "") {
                $("#deathcategory").closest("tr").fadeOut();
                $("#puttosleep").closest("tr").fadeOut();
                $("#ptsreason").closest("div").fadeOut();
            }
            else {
                $("#deathcategory").closest("tr").fadeIn();
                $("#puttosleep").closest("tr").fadeIn();
                $("#ptsreason").closest("div").fadeIn();
                // If the animal is off the shelter, tick the died off shelter box
                if ($("#archived") == "1")  {
                    $("#diedoffshelter").attr("checked", "checked");
                }
            }

            // Enable/disable health and identification fields based on checkboxes
            $("#microchipdate, #microchipnumber").toggle($("#microchipped").is(":checked"));
            $("#tattoodate, #tattoonumber").toggle($("#tattoo").is(":checked"));
            $("#smarttagnumber, #smarttagtype").toggle($("#smarttag").is(":checked"));
            $("#neutereddate").toggle($("#neutered").is(":checked"));
            $("#heartwormtestdate, #heartwormtestresult").toggle($("#heartwormtested").is(":checked"));
            $("#fivltestdate, #fivresult, #flvresult").toggle($("#fivltested").is(":checked"));

            // Show avid submit button for valid microchip numbers in the UK
            var mchipno = String($("#microchipnumber").val());
            var mchipdate = String($("#microchipdate").val());
            if (asm.locale == "en_GB" && mchipno.indexOf("977") == 0 && 
                mchipdate != "" && config.str("AvidOrgName") != "") {
                $("#button-avid").fadeIn();
            }
            else {
                $("#button-avid").hide(); 
            }

            // If the user ticked hold, there's no hold until date and
            // we have an auto remove days period, default the date
            if ($("#hold").is(":checked") && $("#holduntil").val() == "" && config.integer("AutoRemoveHoldDays") > 0) {
                var holddate = format.date_js(controller.animal.DATEBROUGHTIN).getTime();
                holddate += config.integer("AutoRemoveHoldDays") * 86400000;
                holddate = format.date( new Date(holddate) );
                $("#holduntil").val(holddate);
            }

            // If we're a US shelter, show the asilomar categories
            if (asm.locale == "en" && !config.bool("DisableAsilomar")) {
                $(".asilomar").show();
            }
            else {
                $(".asilomar").hide();
            }

            // If the animal doesn't have a litterid, disable the littermates button
            if ($("#litterid").val() == "")  {
                $("#button-littermates").button("disable");
            }
            else {
                $("#button-littermates").button("enable");
            }

            // Not having any active litters disables join litter button
            if ($("#sellitter option").size() == 0) {
                $("#button-litterjoin").button("disable");
            }

            // Hide the internal location dropdown row if the animal is off the shelter
            // and show the last location info instead.
            if ($("#archived").val() == "1") {
                $("#locationrow").hide();
                $("#locationunitrow").hide();
                $("#lastlocation").show();
            }
            else {
                $("#lastlocation").hide();
            }

            // Hide the on shelter flags if the animal is off the shelter
            if (controller.animal.ARCHIVED == 1 && controller.animal.ACTIVEMOVEMENTTYPE != 2 && !$("#nonshelter").is(":checked")) {
                $("#onshelterflags").hide();
            }

            // If the animal is non-shelter, don't show the location
            if ($("#nonshelter").is(":checked")) {
                $("#lastlocation").hide();
                $("#locationrow").hide();
                $("#locationunitrow").hide();
            }

            // If the animal doesn't have a picture, they can't publish to Facebook
            if (!controller.animal.WEBSITEMEDIANAME) {
                $("#button-facebook").hide();
            }

            // CONFIG ===========================

            if (config.bool("DisableShortCodesControl")) {
                $("#shortcode").hide();
                $("#sheltercode").addClass("asm-textbox");
                $("#sheltercode").removeClass("asm-halftextbox");
            }

            if (config.bool("LockCodes") && common.current_url().indexOf("cloned=true") == -1) {
                $("#button-gencode").hide();
                $("#sheltercode").textbox("disable");
                $("#shortcode").textbox("disable");
                // Lock the animal type and datebroughtin fields if they are used 
                // in our coding format.
                if (config.str("CodingFormat").indexOf("T") != -1 || 
                    config.str("ShortCodingFormat").indexOf("T") != -1) {
                    $("#animaltype").select("disable");
                }
                if (config.str("CodingFormat").indexOf("Y") != -1 ||
                    config.str("CodingFormat").indexOf("M") != -1 ||
                    config.str("ShortCodingFormat").indexOf("Y") != -1 ||
                    config.str("ShortCodingFormat").indexOf("M") != -1) {
                    $("#datebroughtin").textbox("disable");
                }
            }

            if (config.bool("DontShowLitterID")) { $("#litteridrow").hide(); }
            if (config.bool("DontShowLocationUnit")) { $("#locationunitrow").hide(); }
            if (config.bool("DontShowRabies")) { $("#rabiestag, label[for='rabiestag']").hide(); }
            if (config.bool("UseSingleBreedField")) { $("#secondbreedrow").hide(); }
            if (config.bool("DontShowCoatType")) { $("#coattyperow").hide(); }
            if (config.bool("DontShowSize")) { $("#sizerow").hide(); }
            if (config.bool("DontShowMicrochip")) { $("#microchiprow").hide(); }
            if (config.bool("DontShowTattoo")) { $("#tattoorow").hide(); }
            if (config.str("SmartTagFTPURL") == "") { $("#smarttagrow").hide(); }
            if (config.bool("DontShowBonded")) { $("#bondedwith1row").hide(); }
            if (config.bool("DontShowBonded")) { $("#bondedwith2row").hide(); }
            if (config.bool("DontShowNeutered")) { $("#neuteredrow").hide(); }
            if (config.bool("DontShowDeclawed")) { $("#declawed").closest("tr").hide(); }
            if (config.bool("DontShowGoodWith")) { $("#goodwithrow").hide(); }
            if (config.bool("DontShowCombi")) { $("#fivlrow").hide(); }
            if (config.bool("DontShowHeartworm")) { $("#heartwormrow").hide(); }
            if (config.bool("DisableLostAndFound")) { $("#button-match").hide(); }
            if (config.bool("ManualCodes")) { $("#button-gencode").hide(); }
            if (!config.bool("FacebookEnabled")) { $("#button-facebook").hide(); }

            // SECURITY =============================================================

            if (!common.has_permission("ca")) { $("#button-save").hide(); }
            if (!common.has_permission("aa")) { $("#button-clone").hide(); }
            if (!common.has_permission("da")) { $("#button-delete").hide(); }
            if (!common.has_permission("gaf")) { $("#button-document").hide(); }
            if (!common.has_permission("vo")) { $("#button-currentowner").hide(); }
            if (!common.has_permission("mlaf")) { $("#button-match").hide(); }
            if (!common.has_permission("vll")) { $("#button-littermates").hide(); }
            if (!common.has_permission("uipb")) { $("#button-facebook").hide(); }

            // ACCORDION ICONS =======================================================

            // A value in health problems or special needs being checked flags Vet tab
            if ($("#healthproblems").val() != "" || $("#specialneeds").is(":checked")) {
                $("#tabvet").show();
            }
            else {
                $("#tabvet").hide();
            }

            // A deceased date being completed flags Death tab
            if ($("#deceaseddate").val() != "") {
                $("#tabdeath").show();
            }
            else {
                $("#tabdeath").hide();
            }

        },

        /** Validates the form fields prior to saving */
        validation: function() {

            // Remove any previous errors
            header.hide_error();
            $("label").removeClass("ui-state-error-text");

            // name
            if ($.trim($("#animalname").val()) == "") {
                header.show_error(_("Name cannot be blank"));
                $("label[for='animalname']").addClass("ui-state-error-text");
                $("#asm-details-accordion").accordion("option", "active", 2);
                $("#animalname").focus();
                return false;
            }

            // date brought in
            if ($.trim($("#datebroughtin").val()) == "") {
                header.show_error(_("Date brought in cannot be blank"));
                $("label[for='datebroughtin']").addClass("ui-state-error-text");
                $("#asm-details-accordion").accordion("option", "active", 3);
                $("#datebroughtin").focus();
                return false;
            }

            // date of birth
            if ($.trim($("#dateofbirth").val()) == "") {
                header.show_error(_("Date of birth cannot be blank"));
                $("label[for='dateofbirth']").addClass("ui-state-error-text");
                $("#asm-details-accordion").accordion("option", "active", 0);
                $("#dateofbirth").focus();
                return false;
            }

            // shelter code
            if ($.trim($("#sheltercode").val()) == "") {
                header.show_error(_("Shelter code cannot be blank"));
                $("label[for='sheltercode']").addClass("ui-state-error-text");
                $("#asm-details-accordion").accordion("option", "active", 0);
                $("#sheltercode").focus();
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

            // any additional fields that are marked mandatory
            var valid = true;
            $(".additional").each(function() {
                var t = $(this);
                if (t.attr("type") != "checkbox") {
                    var d = String(t.attr("data"));
                    if (d.indexOf("a.1") != -1) {
                        if ($.trim(t.val()) == "") {
                            header.show_error(_("{0} cannot be blank").replace("{0}", d.substring(4)));
                            $("#asm-details-accordion").accordion("option", "active", 2);
                            $("label[for='" + t.attr("id") + "']").addClass("ui-state-error-text");
                            t.focus();
                            valid = false;
                            return;
                        }
                    }
                }
            });

            return valid;
        },

        /** Generates a new animal code */
        generate_code: function() {
            validate.dirty(false);
            var formdata = "mode=gencode&datebroughtin=" + $("#datebroughtin").val() + "&animaltypeid=" + $("#animaltype").val();
            common.ajax_post("animal", formdata, function(result) { 
                var codes = result.split("||");
                $("#sheltercode").val(html.decode(codes[0]));
                $("#shortcode").val(html.decode(codes[1]));
                $("#uniquecode").val(codes[2]);
                $("#yearcode").val(codes[3]);
                validate.dirty(true);
            });
        },

        /**
         * Bind widgets and control events
         */
        bind: function() {

            // Setup the document/diary task menu buttons
            $("#button-diarytask, #button-document").asmmenu();

            // If the option isn't set to allow alphanumeric/space
            // characters in microchip and ntattoo numbers, use
            // the alphanumberbox widget.
            if (!config.bool("AllowNonANMicrochip")) {
                $("#microchipnumber").alphanumber();
                $("#tattoonumber").alphanumber();
            }

            // Load the tab strip
            $(".asm-tabbar").asmtabs();

            // Prevent the act of enabling crossbreeds from resetting the
            // breed selects.
            $('#crossbreed').change(function() {
                animal.crossbreedchange = true;
            });

            // Changing the species updates the breed list
            $('#species').change(function() {
                animal.update_breed_list();
            });

            // accordion
            $("#asm-details-accordion").accordion({
                heightStyle: "content"
            });

            // Keep breed2 in sync with breed1 for non-crossbreeds
            $("#breed1").change(function() {
                if (!$("#crossbreed").is(":checked")) {
                    $("#breed2").select("value", $("#breed1").select("value"));
                }
            });

            // If any of our additional fields need moving to other tabs, 
            // let's take care of that. Additional fields are always in pairs of
            // <td> fields, with the label containing a toX class, where toX is
            // an entry in lksfieldlink. Some tables in the form have a .additionaltarget
            // class with a data element marked toX. We reparent our .toX elements
            // to those elements.
            $(".additionaltarget").each(function() {
                var target = $(this);
                var targetname = target.attr("data");
                $(".additionalmove ." + targetname).each(function() {
                    // $(this) is the td containing the label
                    var label = $(this);
                    var item = $(this).next();
                    // For some reason, jquery gets confused if we reparent the row, so
                    // we have to add a new row to the table and then move our cells in.
                    target.append("<tr></tr>");
                    target.find("tr:last").append(label);
                    target.find("tr:last").append(item);
                });
            });


            // If the animal type changes, or the date brought in, we may need to
            // generate a new code
            $("#animaltype").change(function() {
                if (config.bool("ManualCodes")) { 
                    return;
                }
                if (config.str("CodingFormat").indexOf("T") != -1 || 
                    config.str("ShortCodingFormat").indexOf("T") != -1) {
                    animal.generate_code();
                }
            });
            $("#datebroughtin").change(function() {
                if (config.bool("ManualCodes")) { 
                    return;
                }
                if (config.str("CodingFormat").indexOf("Y") != -1 ||
                    config.str("CodingFormat").indexOf("M") != -1 ||
                    config.str("ShortCodingFormat").indexOf("Y") != -1 ||
                    config.str("ShortCodingFormat").indexOf("M") != -1) {
                    animal.generate_code();
                }
            });

            // Litter autocomplete
            $("#litterid").autocomplete({source: html.decode(controller.activelitters)});

            // Diary task create ajax call
            var create_task = function(taskid) {
                var formdata = "mode=exec&id=" + $("#animalid").val() + "&tasktype=ANIMAL&taskid=" + taskid + "&seldate=" + $("#seldate").val();
                common.ajax_post("diarytask", formdata, function(result) { 
                    window.location = "animal_diary?id=" + $("#animalid").val();
                });
            };

            // Diary task select date dialog
            var addbuttons = { };
            addbuttons[_("Select")] = function() {
                var valid = true;
                var fields = [ "seldate" ];
                $.each(fields, function(i, f) {
                    if ($("#" + f).val() == "") {
                        $("label[for='" + f + "']").addClass("ui-state-error-text");
                        $("#" + f).focus();
                        valid = false;
                        return false;
                    }
                });
                if (valid) {
                    create_task($("#diarytaskid").val());
                }
            };
            addbuttons[_("Cancel")] = function() {
                $("#dialog-dt-date").dialog("close");
            };

            $("#dialog-dt-date").dialog({
                autoOpen: false,
                modal: true,
                dialogClass: "dialogshadow",
                show: dlgfx.add_show,
                hide: dlgfx.add_hide,
                buttons: addbuttons
            });

            // Attach handlers for diary tasks
            $(".diarytask").each(function() {
                var a = $(this);
                var task = a.attr("data").split(" ");
                var taskmode = task[0];
                var taskid = task[1];
                var taskneeddate = task[2];
                $(this).click(function() {
                    $("#seldate").val("");
                    // If the task needs a date, prompt for it
                    if (taskneeddate == "1") {
                        $("#diarytaskid").val(taskid);
                        $("#dialog-dt-date").dialog("open");
                    }
                    else {
                        // No need for anything else, go create the task
                        create_task(taskid);
                    }
                });
            });

            // Controls that update the screen when changed
            $("#microchipped").click(animal.enable_widgets).keyup(animal.enable_widgets);
            $("#tattoo").click(animal.enable_widgets).keyup(animal.enable_widgets);
            $("#smarttag").click(animal.enable_widgets).keyup(animal.enable_widgets);
            $("#neutered").click(animal.enable_widgets).keyup(animal.enable_widgets);
            $("#fivltested").click(animal.enable_widgets).keyup(animal.enable_widgets);
            $("#heartwormtested").click(animal.enable_widgets).keyup(animal.enable_widgets);
            $("#hold").click(animal.enable_widgets).keyup(animal.enable_widgets);
            $("#deceaseddate").change(animal.enable_widgets);
            $("#healthproblems").change(animal.enable_widgets);
            $("#specialneeds").change(animal.enable_widgets);
            $("#litterid").keyup(animal.enable_widgets);
            $("#microchipnumber").keyup(animal.enable_widgets);
            $("#microchipdate").change(animal.enable_widgets);

            validate.save = function(callback) {
                if (!animal.validation()) { 
                    header.hide_loading(); 
                    return; 
                }
                validate.dirty(false);
                var formdata = "mode=save&id=" + $("#animalid").val() + "&" + $("input, select, textarea").toPOST();
                common.ajax_post("animal", formdata, callback);
            };

            // Toolbar buttons
            $("#button-save").button().click(function() {
                header.show_loading(_("Saving..."));
                validate.save(function() {
                    window.location="animal?id=" + $("#animalid").val();
                });
            });

            $("#button-clone").button().click(function() {
                $("#button-clone").button("disable");
                var formdata = "mode=clone&animalid=" + $("#animalid").val();
                common.ajax_post("animal", formdata, function(result) { window.location = "animal?id=" + result + "&cloned=true"; });
            });

            $("#button-delete").button().click(function() {
                var b = {}; 
                b[_("Delete")] = function() { 
                    $("#dialog-delete").disable_dialog_buttons();
                    var formdata = "mode=delete&animalid=" + $("#animalid").val();
                    common.ajax_post("animal", formdata, function() { window.location = "main"; });
                };
                b[_("Cancel")] = function() { $(this).dialog("close"); };
                $("#dialog-delete").dialog({
                     resizable: false,
                     modal: true,
                     dialogClass: "dialogshadow",
                     show: dlgfx.delete_show,
                     hide: dlgfx.delete_hide,
                     buttons: b
                });
            });

            $("#button-match").button().click(function() {
                window.location = "lostfound_match?animalid=" + $("#animalid").val();
            });

            $("#button-littermates").button().click(function() {
                window.location = "animal_find_results?mode=ADVANCED&q=&litterid=" + $("#litterid").val();
            });

            // Inline buttons
            $("#button-gencode")
                .button({ icons: { primary: "ui-icon-refresh" }, text: false })
                .click(animal.generate_code);

            $("#button-randomname")
                .button({ icons: { primary: "ui-icon-tag" }, text: false })
                .click(function() {
                validate.dirty(false);
                var formdata = "mode=randomname&sex=" + $("#sex").val();
                common.ajax_post("animal", formdata, function(result) { 
                    $("#animalname").val(result);
                    validate.dirty(true);
                });

            });

            $("#button-commentstomedia")
                .button({ icons: { primary: "ui-icon-arrow-1-ne" }, text: false })
                .click(function() {
                $("#button-commentstomedia").button("disable");
                var formdata = "mode=webnotes&id=" + $("#animalid").val() + "&" + $("#comments").toPOST();
                common.ajax_post("animal", formdata, function(result) { 
                    $("#button-commentstomedia").button("enable");
                    header.show_info(_("Comments copied to web preferred media."));
                });
            });

            $("#button-avid")
                .button({ icons: { primary: "ui-icon-arrow-1-ne" }, text: false })
                .click(function() {
                $("#avid").html(avid.render(controller.animal));
                $(".avidsubmit").button();
                var ab = {};
                ab[_("Cancel")] = function() {
                    $("#dialog-avid").dialog("close");
                };
                $("#dialog-avid").dialog({
                    autoOpen: false,
                    height: 640,
                    width: 800,
                    modal: true,
                    show: dlgfx.edit_show,
                    hide: dlgfx.edit_hide,
                    buttons: ab
                });
                $("#button-avid").button("enable");
                $("#dialog-avid").dialog("open");
            });

            // Facebook button
            if (!controller.hasfacebook) {
                $("#button-facebook").hide();
            }
            else {
                $("#button-facebook").button().click(function() {
                    $("#button-facebook").button("disable");
                    var client_id = controller.facebookclientid;
                    var redirect_uri = asm.baseurl + "/animal_facebook";
                    var scope = "publish_actions,manage_pages,publish_stream";
                    var state = "a" + $("#animalid").val();
                    window.location = "https://www.facebook.com/dialog/oauth/?client_id=" + client_id +
                        "&redirect_uri=" + encodeURIComponent(redirect_uri) +
                        "&scope=" + scope +
                        "&state=" + state;
                });
            }

            // If we just posted to FB, say so
            if (common.current_url().indexOf("facebook=true") != -1) {
                header.show_info(_("Successfully posted to Facebook"));
            }

            // Events that trigger rechecking of the on-screen fields
            $("#crossbreed").click(function() {
                animal.enable_widgets();
                animal.update_breed_list();
            });

        },

        sync: function() {

            // Load the data into the controls for the screen
            $("#asm-content input, #asm-content select, #asm-content textarea").fromJSON(controller.animal);

            // Update the breeds to match the species we just loaded and reload the breed values
            animal.update_breed_list();
            $("#breed1, #breed2").fromJSON(controller.animal);

            // Update on-screen fields from the data and display the screen
            animal.enable_widgets();

            // Dirty handling
            validate.bind_dirty();
            validate.dirty(false);
            validate.check_unsaved_links("animal_");

        }

    };

    
    common.module(animal, "animal", "formtab");

});

function image_error(image) {
    image.style.display = "none";
}

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

    var options = {

        /** Where we have a list of pairs, first is value, second is label */
        two_pair_options: function(o) {
            var s = [];
            $.each(o, function(i, v) {
                s.push('<option value="' + v[0] + '">' + v[1] + '</option>');
            });
            return s.join("\n");
        },

        render_tabs: function() {
            return [
                '<ul>',
                '<li><a href="#tab-shelterdetails">' + _("Shelter Details") + '</a></li>',
                '<li><a href="#tab-accounts">' + _("Accounts") + '</a></li>',
                '<li><a href="#tab-agegroups">' + _("Age Groups") + '</a></li>',
                '<li><a href="#tab-animalcodes">' + _("Animal Codes") + '</a></li>',
                '<li><a href="#tab-costs">' + _("Costs") + '</a></li>',
                '<li><a href="#tab-defaults">' + _("Defaults") + '</a></li>',
                '<li><a href="#tab-diaryandmessages">' + _("Diary and Messages") + '</a></li>',
                '<li><a href="#tab-email">' + _("Email") + '</a></li>',
                '<li><a href="#tab-findanimalperson">' + _("Find Animal/Person") + '</a></li>',
                '<li><a href="#tab-homepage">' + _("Home page") + '</a></li>',
                '<li><a href="#tab-insurance">' + _("Insurance") + '</a></li>',
                '<li><a href="#tab-lostandfound">' + _("Lost and Found") + '</a></li>',
                '<li><a href="#tab-movements">' + _("Movements") + '</a></li>',
                '<li><a href="#tab-search">' + _("Search") + '</a></li>',
                '<li><a href="#tab-waitinglist">' + _("Waiting List") + '</a></li>',
                '<li><a href="#tab-options">' + _("Options") + '</a></li>',
                '</ul>'
            ].join("\n");
        },

        render_shelterdetails: function() {
            return [
                '<div id="tab-shelterdetails">',
                '<table>',
                '<tr>',
                '<td><label for="organisation">' + _("Organization") + '</label></td>',
                '<td><input id="organisation" type="text" class="asm-doubletextbox" data="Organisation" />',
                '</tr>',
                '<tr>',
                '<td><label for="address">' + _("Address") + '</label></td>',
                '<td><textarea id="address" rows="5" class="asm-textareafixeddouble" data="OrganisationAddress"></textarea>',
                '</tr>',
                '<tr>',
                '<td><label for="telephone">' + _("Telephone") + '</label></td>',
                '<td><input id="telephone" type="text" class="asm-textbox" data="OrganisationTelephone" />',
                '</tr>',
                '<tr>',
                '<td><label for="telephone2">' + _("Telephone") + '</label></td>',
                '<td><input id="telephone2" type="text" class="asm-textbox" data="OrganisationTelephone2" />',
                '</tr>',
                '<tr>',
                '<td><label for="timezone">' + _("Server clock adjustment") + '</label></td>',
                '<td><select id="timezone" type="text" class="asm-selectbox" data="Timezone">',
                '<option value="-12">-12:00</option>',
                '<option value="-11">-11:00</option>',
                '<option value="-10">-10:00</option>',
                '<option value="-9">-09:00</option>',
                '<option value="-8">-08:00</option>',
                '<option value="-7">-07:00</option>',
                '<option value="-6">-06:00</option>',
                '<option value="-5">-05:00</option>',
                '<option value="-4">-04:00</option>',
                '<option value="-3">-03:00</option>',
                '<option value="-2">-02:00</option>',
                '<option value="-1">-01:00</option>',
                '<option value="0">' + _("No adjustment") + '</option>',
                '<option value="1">+01:00</option>',
                '<option value="2">+02:00</option>',
                '<option value="3">+03:00</option>',
                '<option value="4">+04:00</option>',
                '<option value="5">+05:00</option>',
                '<option value="6">+06:00</option>',
                '<option value="7">+07:00</option>',
                '<option value="8">+08:00</option>',
                '<option value="9">+09:00</option>',
                '<option value="10">+10:00</option>',
                '<option value="11">+11:00</option>',
                '<option value="12">+12:00</option>',
                '<option value="13">+13:00</option>',
                '<option value="14">+14:00</option>',
                '</select>',
                '</td>',
                '</tr>',
                '<tr>',
                '<td><label for="systemtheme">' + _("Visual Theme") + '</label></td>',
                '<td><select data="SystemTheme" id="systemtheme" class="asm-selectbox">',
                options.two_pair_options(controller.themes),
                '</select></td>',
                '</tr>',
                '<tr>',
                '<td><label for="olocale">' + _("Locale") + '</label></td>',
                '<td><select id="olocale" type="text" class="asm-selectbox" data="Locale">',
                options.two_pair_options(controller.locales),
                '</select> <span id="localeflag"></span>',
                '</td>',
                '</tr>',
                '<tr>',
                '<td></td>',
                '<td>',
                html.info(_("The locale determines the language ASM will use when displaying text, dates and currencies.")),
                '</td>',
                '</tr>',
                '</table>',
                '</div>'
            ].join("\n");
        },

        render_accounts: function() {
            return [
                '<div id="tab-accounts">',
                '<p><input data="rc:DisableAccounts" id="disableaccounts" type="checkbox" class="asm-checkbox" />',
                '<label for="disableaccounts">' + _("Enable accounts functionality") + '</label>',
                '<br />',
                '<input data="CreateDonationTrx" id="createdonations" type="checkbox" class="asm-checkbox" />',
                '<label for="createdonations">' + _("Creating donations and donation types creates matching accounts and transactions") + '</label>',
                '<br />',
                '<input data="AccountPeriodTotals" id="accountperiodtotals" type="checkbox" class="asm-checkbox" />',
                '<label for="accountperiodtotals">' + _("Only show account totals for the current period, which starts on ") + '</label>',
                '<input data="AccountingPeriod" id="accountingperiod" class="asm-datebox asm-textbox" />',
                '</p>',
                '<table>',
                '<td><label for="defaulttrxview">' + _("Default transaction view") + '</td>',
                '<td><select data="DefaultAccountViewPeriod" id="defaulttrxview" class="asm-selectbox">',
                '<option value="0">' + _("This Month") + '</option>',
                '<option value="1">' + _("This Week") + '</option>',
                '<option value="2">' + _("This Year") + '</option>',
                '<option value="3">' + _("Last Month") + '</option>',
                '<option value="4">' + _("Last Week") + '</option>',
                '</select>',
                '</td>',
                '</tr>',
                '<tr>',
                '<td><label for="destinationaccount">' + _("Default destination account for donations") + '</td>',
                '<td><select data="DonationTargetAccount" id="destinationaccount" class="asm-selectbox">',
                html.list_to_options(controller.accounts, "ID", "CODE"),
                '</select>',
                '</td>',
                '</tr>',
                '<tr>',
                '<td><label for="mapdt1">' + _("Donations of type") + '</td>',
                '<td><select id="mapdt1" class="asm-selectbox donmap">',
                '<option value="-1">' + _("[None]") + '</option>',
                html.list_to_options(controller.donationtypes, "ID", "DONATIONNAME"),
                '</select>',
                '</td>',
                '<td>' + _("are sent to") + '</td>',
                '<td><select id="mapac1" class="asm-selectbox">',
                '<option value="-1">' + _("[None]") + '</option>',
                html.list_to_options(controller.accounts, "ID", "CODE"),
                '</select>',
                '</td>',
                '</tr>',
                '<tr>',
                '<td><label for="mapdt2">' + _("Donations of type") + '</td>',
                '<td><select id="mapdt2" class="asm-selectbox donmap">',
                '<option value="-1">' + _("[None]") + '</option>',
                html.list_to_options(controller.donationtypes, "ID", "DONATIONNAME"),
                '</select>',
                '</td>',
                '<td>' + _("are sent to") + '</td>',
                '<td><select id="mapac2" class="asm-selectbox">',
                '<option value="-1">' + _("[None]") + '</option>',
                html.list_to_options(controller.accounts, "ID", "CODE"),
                '</select>',
                '</td>',
                '</tr>',
                '<tr>',
                '<td><label for="mapdt3">' + _("Donations of type") + '</td>',
                '<td><select id="mapdt3" class="asm-selectbox donmap">',
                '<option value="-1">' + _("[None]") + '</option>',
                html.list_to_options(controller.donationtypes, "ID", "DONATIONNAME"),
                '</select>',
                '</td>',
                '<td>' + _("are sent to") + '</td>',
                '<td><select id="mapac3" class="asm-selectbox">',
                '<option value="-1">' + _("[None]") + '</option>',
                html.list_to_options(controller.accounts, "ID", "CODE"),
                '</select>',
                '</td>',
                '</tr>',
                '<tr>',
                '<td><label for="mapdt4">' + _("Donations of type") + '</td>',
                '<td><select id="mapdt4" class="asm-selectbox donmap">',
                '<option value="-1">' + _("[None]") + '</option>',
                html.list_to_options(controller.donationtypes, "ID", "DONATIONNAME"),
                '</select>',
                '</td>',
                '<td>' + _("are sent to") + '</td>',
                '<td><select id="mapac4" class="asm-selectbox">',
                '<option value="-1">' + _("[None]") + '</option>',
                html.list_to_options(controller.accounts, "ID", "CODE"),
                '</select>',
                '</td>',
                '</tr>',
                '<tr>',
                '<td><label for="mapdt5">' + _("Donations of type") + '</td>',
                '<td><select id="mapdt5" class="asm-selectbox donmap">',
                '<option value="-1">' + _("[None]") + '</option>',
                html.list_to_options(controller.donationtypes, "ID", "DONATIONNAME"),
                '</select>',
                '</td>',
                '<td>' + _("are sent to") + '</td>',
                '<td><select id="mapac5" class="asm-selectbox">',
                '<option value="-1">' + _("[None]") + '</option>',
                html.list_to_options(controller.accounts, "ID", "CODE"),
                '</select>',
                '</td>',
                '</tr>',
                '</table>',
                '</div>'
            ].join("\n");
        },

        render_agegroups: function() {
            return [
                '<div id="tab-agegroups">',
                html.info(_("Age groups are assigned based on the age of an animal. The figure in the left column is the upper limit in years for that group.")),
                '<table>',
                '<tr>',
                '<td>' + _("Age Group 1") + '</td>',
                '<td><input id="agegroup1" type="text" class="asm-numberbox asm-textbox" data="AgeGroup1" /></td>',
                '<td><input id="agegroup1name" type="text" class="asm-textbox" data="AgeGroup1Name" /></td>',
                '</tr>',
                '<tr>',
                '<td>' + _("Age Group 2") + '</td>',
                '<td><input id="agegroup2" type="text" class="asm-numberbox asm-textbox" data="AgeGroup2" /></td>',
                '<td><input id="agegroup2name" type="text" class="asm-textbox" data="AgeGroup2Name" /></td>',
                '</tr>',
                '<tr>',
                '<td>' + _("Age Group 3") + '</td>',
                '<td><input id="agegroup3" type="text" class="asm-numberbox asm-textbox" data="AgeGroup3" /></td>',
                '<td><input id="agegroup3name" type="text" class="asm-textbox" data="AgeGroup3Name" /></td>',
                '</tr>',
                '<tr>',
                '<td>' + _("Age Group 4") + '</td>',
                '<td><input id="agegroup4" type="text" class="asm-numberbox asm-textbox" data="AgeGroup4" /></td>',
                '<td><input id="agegroup4name" type="text" class="asm-textbox" data="AgeGroup4Name" /></td>',
                '</tr>',
                '<tr>',
                '<td>' + _("Age Group 5") + '</td>',
                '<td><input id="agegroup5" type="text" class="asm-numberbox asm-textbox" data="AgeGroup5" /></td>',
                '<td><input id="agegroup5name" type="text" class="asm-textbox" data="AgeGroup5Name" /></td>',
                '</tr>',
                '<tr>',
                '<td>' + _("Age Group 6") + '</td>',
                '<td><input id="agegroup6" type="text" class="asm-numberbox asm-textbox" data="AgeGroup6" /></td>',
                '<td><input id="agegroup6name" type="text" class="asm-textbox" data="AgeGroup6Name" /></td>',
                '</tr>',
                '<tr>',
                '<td>' + _("Age Group 7") + '</td>',
                '<td><input id="agegroup7" type="text" class="asm-numberbox asm-textbox" data="AgeGroup7" /></td>',
                '<td><input id="agegroup7name" type="text" class="asm-textbox" data="AgeGroup7Name" /></td>',
                '</tr>',
                '<tr>',
                '<td>' + _("Age Group 8") + '</td>',
                '<td><input id="agegroup8" type="text" class="asm-numberbox asm-textbox" data="AgeGroup8" /></td>',
                '<td><input id="agegroup8name" type="text" class="asm-textbox" data="AgeGroup8Name" /></td>',
                '</tr>',
                '</table>',
                '</div>'
            ].join("\n");
        },

        render_animalcodes: function() {
            return [
                '<div id="tab-animalcodes">',
                html.info(
                    _("Code format tokens:") + '<br />' +
                    _("T = first letter of animal type") + '<br />' +
                    _("TT = first and second letter of animal type") + '<br />' + 
                    _("YY or YYYY = current year") + '<br />' +
                    _("MM = current month") + '<br />' +
                    _("DD = current day") + '<br />' + 
                    _("UUUUUUUUUU or UUUU = unique number") + '<br />' +
                    _("NNN or NN = number unique for this type of animal for this year") + '<br />' +
                    _("Defaults formats for code and shortcode are TYYYYNNN and NNT")),
                '<table>',
                '<tr>',
                '<td><label for="codeformat">' + _("Animal code format") + '</label></td>',
                '<td><input data="CodingFormat" id="codeformat" type="text" class="asm-textbox" /></td>',
                '</tr>',
                '<tr>',
                '<td><label for="shortformat">' + _("Animal shortcode format") + '</label></td>',
                '<td><input data="ShortCodingFormat" id="shortformat" type="text" class="asm-textbox" /></td>',
                '</tr>',
                '</table>',
                '<p>',
                '<input data="ManualCodes" id="manualcodes" type="checkbox" class="asm-checkbox" /> <label for="manualcodes">' + _("Manually enter codes (do not generate)") + '</label>',
                '<br />',
                '<input data="UseShortShelterCodes" id="shortcodes" type="checkbox" class="asm-checkbox" /> <label for="shortcodes">' + _("Show short shelter codes on screens") + '</label>',
                '<br />',
                '<input data="DisableShortCodesControl" id="disableshortcodes" type="checkbox" class="asm-checkbox" /> <label for="disableshortcodes">' + _("Remove short shelter code box from the animal details screen") + '</label>',
                '<br />',
                '<input data="ShelterViewShowCodes" id="shelterviewshowcodes" type="checkbox" class="asm-checkbox" /> <label for="shelterviewshowcodes">' + _("Show codes on the shelter view screen") + '</label>',
                '<br />',

                '<input data="LockCodes" id="lockcodes" type="checkbox" class="asm-checkbox" /> <label for="lockcodes">' + _("Once assigned, codes cannot be changed") + '</label>',
                '</p>',
                '</div>'
            ].join("\n");
        },

        render_costs: function() {
            return [
                '<div id="tab-costs">',
                '<table>',
                '<tr>',
                '<td><label for="dailyboardingcost">' + _("Default daily boarding cost") + '</label></td>',
                '<td><input data="DefaultDailyBoardingCost" id="dailyboardingcost" class="asm-currencybox asm-textbox" type="text" /></td>',
                '</tr>',
                '<tr>',
                '<td></td>',
                '<td>',
                '<input data="CreateBoardingCostOnAdoption" id="costonadoption" type="checkbox" class="asm-checkbox" /> <label for="costonadoption">' + _("Create boarding cost record when animal is adopted") + '</label>',
                '</td>',
                '</tr>',
                '<tr>',
                '<td><label for="costtype">' + _("Boarding cost type") + '</label></td>',
                '<td><select data="BoardingCostType" id="costtype" class="asm-selectbox">',
                html.list_to_options(controller.costtypes, "ID", "COSTTYPENAME"),
                '</select>',
                '</td>',
                '</tr>',
                '</table>',
                '</div>'
            ].join("\n");
        },

        render_defaults: function() {
            return [
                '<div id="tab-defaults">',
                html.info(_("These are the default values for these fields when creating new records.")),
                '<table>',
                '<tr>',
                '<td><label for="defaultspecies">' + _("Default Species") + '</label></td>',
                '<td><select data="AFDefaultSpecies" id="defaultspecies" class="asm-selectbox">',
                html.list_to_options(controller.species, "ID", "SPECIESNAME"),
                '</select></td>',
                '<td><label for="defaulttype">' + _("Default Type") + '</label></td>',
                '<td><select data="AFDefaultType" id="defaulttype" class="asm-selectbox">',
                html.list_to_options(controller.types, "ID", "ANIMALTYPE"),
                '</select>',
                '</td>',
                '</tr>',
                '<tr>',
                '<td><label for="defaultlocation">' + _("Default Location") + '</label></td>',
                '<td><select data="AFDefaultLocation" id="defaultlocation" class="asm-selectbox">',
                html.list_to_options(controller.locations, "ID", "LOCATIONNAME"),
                '</select></td>',
                '<td><label for="defaultentry">' + _("Default Entry Reason") + '</label></td>',
                '<td><select data="AFDefaultEntryReason" id="defaultentry" class="asm-selectbox">',
                html.list_to_options(controller.entryreasons, "ID", "REASONNAME"),
                '</select>',
                '</td>',
                '</tr>',
                '<tr>',
                '<td><label for="defaultcolour">' + _("Default Color") + '</label></td>',
                '<td><select data="AFDefaultColour" id="defaultcolour" class="asm-selectbox">',
                html.list_to_options(controller.colours, "ID", "BASECOLOUR"),
                '</select></td>',
                '<td><label for="defaultdeath">' + _("Default Death Reason") + '</label></td>',
                '<td><select data="AFDefaultDeathReason" id="defaultdeath" class="asm-selectbox">',
                html.list_to_options(controller.deathreasons, "ID", "REASONNAME"),
                '</select>',
                '</td>',
                '</tr>',
                '<tr>',
                '<td><label for="defaultreturn">' + _("Default Return Reason") + '</label></td>',
                '<td><select data="AFDefaultReturnReason" id="defaultreturn" class="asm-selectbox">',
                html.list_to_options(controller.entryreasons, "ID", "REASONNAME"),
                '</select></td>',
                '<td><label for="defaultsize">' + _("Default Size") + '</label></td>',
                '<td><select data="AFDefaultSize" id="defaultsize" class="asm-selectbox">',
                html.list_to_options(controller.sizes, "ID", "SIZE"),
                '</select>',
                '</td>',
                '</tr>',
                '<tr>',
                '<td><label for="defaultlog">' + _("Default Log Filter") + '</label></td>',
                '<td><select data="AFDefaultLogFilter" id="defaultlog" class="asm-selectbox">',
                '<option value="-1">' + _("(all)") + '</option>',
                html.list_to_options(controller.logtypes, "ID", "LOGTYPENAME"),
                '</select></td>',
                '<td><label for="defaultcoattype">' + _("Default Coat Type") + '</label></td>',
                '<td><select data="AFDefaultCoatType" id="defaultcoattype" class="asm-selectbox">',
                html.list_to_options(controller.coattypes, "ID", "COATTYPE"),
                '</select>',
                '</td>',
                '</tr>',
                '<tr>',
                '<td><label for="defaultdonation">' + _("Default Donation Type") + '</label></td>',
                '<td><select data="AFDefaultDonationType" id="defaultdonation" class="asm-selectbox">',
                html.list_to_options(controller.donationtypes, "ID", "DONATIONNAME"),
                '</select></td>',
                '<td><label for="defaultvaccination">' + _("Default Vaccination Type") + '</label></td>',
                '<td><select data="AFDefaultVaccinationType" id="defaultvaccination" class="asm-selectbox">',
                html.list_to_options(controller.vaccinationtypes, "ID", "VACCINATIONTYPE"),
                '</select>',
                '</td>',
                '</tr>',
                '<tr>',
                '<td><label for="defaultbreed">' + _("Default Breed") + '</label></td>',
                '<td><select data="AFDefaultBreed" id="defaultbreed" class="asm-selectbox">',
                html.list_to_options(controller.breeds, "ID", "BREEDNAME"),
                '</select>',
                '</td>',
                '<td><label for="defaulttest">' + _("Default Test Type") + '</label></td>',
                '<td><select data="AFDefaultTestType" id="defaulttest" class="asm-selectbox">',
                html.list_to_options(controller.testtypes, "ID", "TESTNAME"),
                '</select>',
                '</td>',
                '</tr>',
                '<tr>',
                '<td><label for="DefaultBroughtInBy">' + _("Default Brought In By") + '</label></td>',
                '<td>',
                '<input id="DefaultBroughtInBy" data="DefaultBroughtInBy" type="hidden" class="asm-personchooser" value=\'\' />',
                '</td>',
                '</tr>',
                '</table>',
                '<p>',
                '<input data="AutoNotForAdoption" id="autonotadopt" type="checkbox" class="asm-checkbox" /> <label for="autonotadopt">' + _("Mark new animals as not for adoption") + '</label>',
                '<br />',
                '<input data="AutoMediaNotes" id="automedianotes" type="checkbox" class="asm-checkbox" /> <label for="automedianotes">' + _("Prefill new media notes for animal images with animal comments if left blank") + '</label>',
                '<br />',
                '<input data="DefaultMediaNotesFromFile" id="medianotesfile" type="checkbox" class="asm-checkbox" /> <label for="medianotesfile">' + _("Prefill new media notes with the filename if left blank") + '</label>',
                '<br />',
                '<input data="AdvancedFindAnimal" id="advancedfindanimal" type="checkbox" class="asm-checkbox" /> <label for="advancedfindanimal">' + _("Default to advanced find animal screen") + '</label>',
                '<br />',
                '<input data="AdvancedFindAnimalOnShelter" id="advancedfindanimalos" type="checkbox" class="asm-checkbox" /> <label for="advancedfindanimalos">' + _("Advanced find animal screen defaults to on shelter") + '</label>',
                '<br />',
                '<input data="AdvancedFindOwner" id="advancedfindperson" type="checkbox" class="asm-checkbox" /> <label for="advancedfindperson">' + _("Default to advanced find person screen") + '</label>',
                '<br />',
                '<input data="IncludeIncompleteMedicalDoc" id="includeincompletemedical" type="checkbox" class="asm-checkbox" /> <label for="includeincompletemedical">' + _("Include incomplete medical and vaccination records when generating document templates") + '</label>',
                '<br />',
                '<input data="GenerateDocumentLog" id="generatedocumentlog" type="checkbox" class="asm-checkbox" /> <label for="generatedocumentlog">' + _("When I generate a document, make a note of it in the log with this type") + '</label>',
                '<select data="GenerateDocumentLogType" id="generatedocumentlogtype" class="asm-selectbox">',
                html.list_to_options(controller.logtypes, "ID", "LOGTYPENAME"),
                '</select>',
                '</p>',
                '</div>'
            ].join("\n");
        },

        render_diaryandmessages: function() {
            return [
                '<div id="tab-diaryandmessages">',
                '<p>',
                '<input data="AllDiaryHomePage" id="alldiaryhomepage" class="asm-checkbox" type="checkbox" /> <label for="alldiaryhomepage">' + _("Show the full diary (instead of just my notes) on the home page") + '</label><br />',
                '<input data="EmailDiaryNotes" id="emaildiarynotes" class="asm-checkbox" type="checkbox" /> <label for="emaildiarynotes">' + _("Email users their diary notes each day") + '</label><br />',
                '<input data="EmailMessages" id="emailmessages" class="asm-checkbox" type="checkbox" /> <label for="emailmessages">' + _("When a message is created, email it to each matching user") + '</label>',
                '</p>',
                '</div>'
            ].join("\n");
        },

        render_email: function() {
            return [
                '<div id="tab-email">',
                '<table>',
                '<tr>',
                '<td><label for="emailaddress">' + _("Email address") + '</label></td>',
                '<td><input data="EmailAddress" id="emailaddress" type="text" class="asm-doubletextbox" /></td>',
                '</tr>',
                '<tr class="smtp">',
                '<td><label for="smtpserver">' + _("SMTP server") + '</label></td>',
                '<td><input data="SMTPServer" id="smtpserver" type="text" class="asm-doubletextbox" /></td>',
                '</tr>',
                '<tr class="smtp">',
                '<td><label for="smtpusername">' + _("SMTP username") + '</label></td>',
                '<td><input data="SMTPServerUsername" id="smtpusername" type="text" class="asm-doubletextbox" /></td>',
                '</tr>',
                '<tr class="smtp">',
                '<td><label for="smtppassword">' + _("SMTP password") + '</label></td>',
                '<td><input data="SMTPServerPassword" id="smtppassword" type="text" class="asm-doubletextbox" /></td>',
                '</tr>',
                '<tr class="smtp">',
                '<td></td>',
                '<td><input data="SMTPServerUseTLS" id="smtptls" type="checkbox" class="asm-checkbox" />',
                '<label for="smtptls">' + _("Use TLS") + '</label>',
                '</td>',
                '</tr>',
                '<tr>',
                '<td><label for="emailsig">' + _("Email signature") + '</label></td>',
                '<td><textarea data="EmailSignature" id="emailsig" rows="10" class="asm-textareafixeddouble"></textarea></td>',
                '</tr>',
                '</table>',
                '</div>'
            ].join("\n");
        },

        render_findanimalperson: function() {
            return [
                '<div id="tab-findanimalperson">',
                html.info(_("These fields determine which columns are shown on the find animal and find person screens.")),
                '<table>',
                '<tr>',
                '<td><label for="findanimalcols">' + _("Find animal columns") + '</label></td>',
                '<td><select id="searchcolumns" class="asm-bsmselect" data="SearchColumns" multiple="multiple">',
                options.two_pair_options(controller.animalfindcolumns),
                '</select>',
                '</td>',
                '</tr>',
                '<tr>',
                '<td><label for="findpersoncols">' + _("Find person columns") + '</label></td>',
                '<td>',
                '<select id="findpersoncols" class="asm-bsmselect" data="OwnerSearchColumns" multiple="multiple">',
                options.two_pair_options(controller.personfindcolumns),
                '</select>',
                '</td>',
                '</tr>',
                '</table>',
                '</div>'
            ].join("\n");
        },

        render_insurance: function() {
            return [
                '<div id="tab-insurance">',
                html.info(_("These numbers are for shelters who have agreements with insurance companies and are given blocks of policy numbers to allocate.")),
                '<table>',
                '<tr>',
                '<td></td>',
                '<td><input data="UseAutoInsurance" id="autoinsurance" type="checkbox" class="asm-checkbox" /> <label for="autoinsurance">' + _("Use Automatic Insurance Numbers") + '</label></td>',
                '</tr>',
                '<tr>',
                '<td><label for="insurancestart">' + _("Start at") + '</label></td>',
                '<td><input data="AutoInsuranceStart" id="insurancestart" type="text" class="asm-textbox asm-numberbox" /></td>',
                '</tr>',
                '<tr>',
                '<td><label for="insuranceend">' + _("End at") + '</label></td>',
                '<td><input data="AutoInsuranceEnd" id="insuranceend" type="text" class="asm-textbox asm-numberbox" /></td>',
                '</tr>',
                '<tr>',
                '<td><label for="insurancenext">' + _("Next") + '</label></td>',
                '<td><input data="AutoInsuranceNext" id="insurancenext" type="text" class="asm-textbox asm-numberbox" /></td>',
                '</tr>',
                '</table>',
                '</div>'
            ].join("\n");
        },

        render_lostandfound: function() {
            return [
                '<div id="tab-lostandfound">',
                '<p>',
                '<input data="rc:DisableLostAndFound" id="disablelostfound" type="checkbox" class="asm-checkbox" /> <label for="disablelostfound">' + _("Enable lost and found functionality") + '</label>',
                '<br />',
                '<input data="MatchIncludeShelter" id="matchshelter" type="checkbox" class="asm-checkbox" /> <label for="matchshelter">' + _("When matching lost animals, include shelter animals") + '</label>',
                '</p>',
                '<table>',
                '<tr>',
                '<td class="bottomborder"><label for="matchpointfloor">' + _("Points required to appear on match report") + '</label></td>',
                '<td class="bottomborder"><input data="MatchPointFloor" id="matchpointfloor" type="text" class="asm-textbox asm-numberbox strong" /></td>',
                '</tr>',
                '<tr>',
                '<td><label for="matchspecies">' + _("Points for matching species") + '</label></td>',
                '<td><input data="MatchSpecies" id="matchspecies" type="text" class="asm-textbox asm-numberbox" /></td>',
                '</tr>',
                '<tr>',
                '<td><label for="matchbreed">' + _("Points for matching breed") + '</label></td>',
                '<td><input data="MatchBreed" id="matchbreed" type="text" class="asm-textbox asm-numberbox" /></td>',
                '</tr>',
                '<tr>',
                '<td><label for="matchcolour">' + _("Points for matching color") + '</label></td>',
                '<td><input data="MatchColour" id="matchcolour" type="text" class="asm-textbox asm-numberbox" /></td>',
                '</tr>',
                '<tr>',
                '<td><label for="matchagegroup">' + _("Points for matching age group") + '</label></td>',
                '<td><input data="MatchAge" id="matchagegroup" type="text" class="asm-textbox asm-numberbox" /></td>',
                '</tr>',
                '<tr>',
                '<td><label for="matchsex">' + _("Points for matching sex") + '</label></td>',
                '<td><input data="MatchSex" id="matchsex" type="text" class="asm-textbox asm-numberbox" /></td>',
                '</tr>',
                '<tr>',
                '<td><label for="matcharea">' + _("Points for matching lost/found area") + '</label></td>',
                '<td><input data="MatchAreaLost" id="matcharea" type="text" class="asm-textbox asm-numberbox" /></td>',
                '</tr>',
                '<tr>',
                '<td><label for="matchfeatures">' + _("Points for matching features") + '</label></td>',
                '<td><input data="MatchFeatures" id="matchfeatures" type="text" class="asm-textbox asm-numberbox" /></td>',
                '</tr>',
                '<tr>',
                '<td><label for="matchpostcode">' + _("Points for matching zipcode") + '</label></td>',
                '<td><input data="MatchPostcode" id="matchpostcode" type="text" class="asm-textbox asm-numberbox" /></td>',
                '</tr>',
                '<tr>',
                '<td><label for="match2weeks">' + _("Points for being found within 2 weeks of being lost") + '</label></td>',
                '<td><input data="MatchWithin2Weeks" id="match2weeks" type="text" class="asm-textbox asm-numberbox" /></td>',
                '</tr>',
                '</table>',
                '</div>'
            ].join("\n");
        },

        render_movements: function() {
            return [
                '<div id="tab-movements">',
                '<p><label for="cancelunadopted">' + _("Cancel unadopted reservations after") + '</label> <input data="AutoCancelReservesDays" id="cancelunadopted" type="text" class="asm-textbox asm-numberbox" title="' + html.title(_("Cancel unadopted reservations after this many days, or 0 to never cancel")) + '" /> ' + _(" days.") + '</p>',
                '<p><label for="autoremoveholddays">' + _("Remove holds after") + '</label> <input data="AutoRemoveHoldDays" id="autoremoveholddays" type="text" class="asm-textbox asm-numberbox" title="' + html.title(_("Cancel holds on animals this many days after the brought in date, or 0 to never cancel")) + '" /> ' + _(" days.") + '</p>',
                '<input data="FosterOnShelter" id="fosteronshelter" class="asm-checkbox" type="checkbox" /> <label for="fosteronshelter">' + _("Treat foster animals as part of the shelter inventory") + '</label><br />',
                '<input data="CancelReservesOnAdoption" id="cancelresadopt" class="asm-checkbox" type="checkbox" /> <label for="cancelresadopt">' + _("Automatically cancel any outstanding reservations on an animal when it is adopted") + '</label><br />',
                '<input data="MovementDonationsDefaultDue" id="donationsdue" class="asm-checkbox" type="checkbox" /> <label for="donationsdue">' + _("When creating donations from the Move menu screens, mark them due instead of received") + '</label><br />',
                '<input data="SecondDonationOnMove" id="seconddonation" class="asm-checkbox" type="checkbox" /> <label for="seconddonation">' + _("Allow entry of two donations on the Move menu screens") + '</label><br />',
                '<input data="MovementNumberOverride" id="movementoverride" class="asm-checkbox" type="checkbox" /> <label for="movementoverride">' + _("Allow overriding of the movement number on the Move menu screens") + '</label><br />',
                '<input data="TrialAdoptions" id="trialadoptions" class="asm-checkbox" type="checkbox" /> <label for="trialadoptions">' + _("Our shelter does trial adoptions, allow us to mark these on movement screens") + '</label><br />',
                '<input data="TrialOnShelter" id="trialonshelter" class="asm-checkbox" type="checkbox" /> <label for="trialonshelter">' + _("Treat trial adoptions as part of the shelter inventory") + '</label>',
                '</p>',
                '<p class="asm-header">' + _("Warnings") + '</p>',
                '<p>',
                '<input data="WarnNoHomeCheck" id="warnnohomecheck" class="asm-checkbox" type="checkbox" /> <label for="warnnohomecheck">' + _("Warn when adopting to a person who has not been homechecked") + '</label><br />',
                '<input data="WarnBannedOwner" id="warnbanned" class="asm-checkbox" type="checkbox" /> <label for="warnbanned">' + _("Warn when adopting to a person who has been banned from adopting animals") + '</label><br />',
                '<input data="WarnOOPostcode" id="warnoopostcode" class="asm-checkbox" type="checkbox" /> <label for="warnoopostcode">' + _("Warn when adopting to a person who lives in the same area as the original owner") + '</label><br />',
                '<input data="WarnBroughtIn" id="warnbroughtin" class="asm-checkbox" type="checkbox" /> <label for="warnbroughtin">' + _("Warn when adopting to a person who has previously brought an animal to the shelter") + '</label><br />',
                '<input data="WarnMultipleReserves" id="warnmultiplereseves" class="asm-checkbox" type="checkbox" /> <label for="warnmultiplereserves">' + _("Warn when creating multiple reservations on the same animal") + '</label>',
                '</p>',
                '</div>'
            ].join("\n");
        },

        render_homepage: function() {
            return [
                '<div id="tab-homepage">',
                '<p>',
                '<input data="rc:DisableTips" id="disabletips" class="asm-checkbox" type="checkbox" /> <label for="disabletips">' + _("Show tips on the home page") + '</label><br />',
                '<input data="ShowAlertsHomePage" id="showalerts" class="asm-checkbox" type="checkbox" /> <label for="showalerts">' + _("Show alerts on the home page") + '</label><br />',
                '</p>',
                '<p class="asm-header">' + _("Quicklinks") + '</p>',
                html.info(_("Quicklinks are shown on the home page and allow quick access to areas of the system.")),
                '<p style="padding-bottom: 20px">',
                '<select id="quicklinksid" multiple="multiple" class="asm-bsmselect" data="QuicklinksID">',
                options.two_pair_options(controller.quicklinks),
                '</select>',
                '</p>',
                '<p>',
                '<input data="QuicklinksHomeScreen" id="disablequicklinks" class="asm-checkbox" type="checkbox" /> <label for="disablequicklinks">' + _("Show quick links on the home page") + '</label><br />',
                '<input data="QuicklinksAllScreens" id="disablequicklinks" class="asm-checkbox" type="checkbox" /> <label for="disablequicklinks">' + _("Show quick links on all pages") + '</label>',
                '</p>',
                '<table class="asm-left-table">',
                '<tr>',
                '<td><label for="linkmode">' + _("Type of animal links to show") + '</label></td>',
                '<td>',
                '<select id="linkmode" class="asm-selectbox" data="MainScreenAnimalLinkMode">',
                '<option value="none">' + _("Do not show") + '</option>',
                '<option value="recentlychanged">' + _("Recently Changed") + '</option>',
                '<option value="recentlyentered">' + _("Recently Entered Shelter") + '</option>',
                '<option value="recentlyadopted">' + _("Recently Adopted") + '</option>',
                '<option value="recentlyfostered">' + _("Recently Fostered") + '</option>',
                '<option value="adoptable">' + _("Up for adoption") + '</option>',
                '<option value="longestonshelter">' + _("Longest On Shelter") + '</option>',
                '</select>',
                '</td>',
                '</tr>',
                '<tr>',
                '<td><label for="linkmax">' + _("Number of animal links to show") + '</label></td>',
                '<td><input type="text" id="linkmax" data="MainScreenAnimalLinkMax" class="asm-textbox asm-numberbox" /></td>',
                '</tr>',
                '</table>',
                '<p class="asm-header">' + _("Shelter view") + '</p>',
                '<table class="asm-left-table">',
                '<tr>',
                '<td><label for="shelterviewdefault">' + _("Default view") + '</label></td>',
                '<td>',
                '<select id="shelterviewdefault" class="asm-selectbox" data="ShelterViewDefault">',
                '<option value="fosterer">' + _("Fosterer") + '</option>',
                '<option value="location">' + _("Location") + '</option>',
                '<option value="locationspecies">' + _("Location and Species") + '</option>',
                '<option value="locationunit">' + _("Location and Unit") + '</option>',
                '<option value="species">' + _("Species") + '</option>',
                '<option value="status">' + _("Status") + '</option>',
                '<option value="type">' + _("Type") + '</option>',
                '</select>',
                '</td>',
                '</tr>',
                '</table>',
                '<p class="asm-header">' + _("Stats") + '</p>',
                html.info(_("Stats show running figures for the selected period of animals entering and leaving the shelter on the home page.")),
                '<table class="asm-left-table">',
                '<tr>',
                '<td><label for="statmode">' + _("Stats period") + '</label></td>',
                '<td>',
                '<select id="statmode" class="asm-selectbox" data="ShowStatsHomePage">',
                '<option value="none">' + _("Do not show") + '</option>',
                '<option value="today">' + _("Today") + '</option>',
                '<option value="thisweek">' + _("This week") + '</option>',
                '<option value="thismonth">' + _("This month") + '</option>',
                '<option value="thisyear">' + _("This year") + '</option>',
                '<option value="alltime">' + _("All time") + '</option>',
                '</select>',
                '</td>',
                '</tr>',
                '</table>',
                '<p class="asm-header">' + _("Animal Emblems") + '</p>',
                html.info(_("Animal emblems are the little icons that appear next to animal names in shelter view, the home page and search results.")),
                '<p>',
                '<input data="EmblemCrueltyCase" type="checkbox" id="showcrueltycase" class="asm-checkbox" type="checkbox" /> <label for="showcrueltycase">' + _("Cruelty Case") + '</label><br />',
                '<input data="EmblemHold" type="checkbox" id="showhold" class="asm-checkbox" type="checkbox" /> <label for="showhold">' + _("Hold") + '</label><br />',
                '<input data="EmblemNonShelter" type="checkbox" id="shownonshelter" class="asm-checkbox" type="checkbox" /> <label for="shownonshelter">' + _("Non-Shelter") + '</label><br />',
                '<input data="EmblemNotForAdoption" type="checkbox" id="shownotforadoption" class="asm-checkbox" type="checkbox" /> <label for="shownotforadoption">' + _("Not For Adoption") + '</label><br />',
                '<input data="EmblemQuarantine" type="checkbox" id="showquarantine" class="asm-checkbox" type="checkbox" /> <label for="showquarantine">' + _("Quarantine") + '</label><br />',
                '<input data="EmblemReserved" type="checkbox" id="showreserved" class="asm-checkbox" type="checkbox" /> <label for="showreserved">' + _("Reserved") + '</label><br />',
                '<input data="EmblemTrialAdoption" type="checkbox" id="showtrialadoption" class="asm-checkbox" type="checkbox" /> <label for="showtrialadoption">' + _("Trial Adoption") + '</label><br />',
                '<input data="EmblemUnneutered" type="checkbox" id="showunneutered" class="asm-checkbox" type="checkbox" /> <label for="showunneutered">' + _("Unaltered") + '</label><br />',
                '</p>',
                '</div>'
            ].join("\n");
        },

        render_search: function() {
            return [
                '<div id="tab-search">',
                html.info(_("These options change the behaviour of the search box at the top of the page.")),
                '<p>',
                '<input data="ShowSearchGo" id="showsearchgo" class="asm-checkbox" type="checkbox" /> <label for="showsearchgo">' + _("Display a search button at the right side of the search box") + '</label>',
                '</p>',
                '<table>',
                '<tr>',
                '<td><label for="searchsort">' + _("Search sort order") + '</label></td>',
                '<td><select id="searchsort" class="asm-selectbox" data="SearchSort">',
                '<option value="0">' + _("Alphabetically A-Z") + '</option>',
                '<option value="1">' + _("Alphabetically Z-A") + '</option>',
                '<option value="2">' + _("Least recently changed") + '</option>',
                '<option value="3">' + _("Most recently changed") + '</option>',
                '<option value="6">' + _("Most relevant") + '</option>',
                '</tr>',
                '</table>',
                '</div>'
            ].join("\n");
        },

        render_waitinglist: function() {
            return [
                '<div id="tab-waitinglist">',
                '<p>',
                '<input data="rc:DisableWaitingList" id="disablewl" class="asm-checkbox" type="checkbox" /> <label for="disablewl">' + _("Enable the waiting list functionality") + '</label><br />',
                '<input data="WaitingListRankBySpecies" id="wlrank" class="asm-checkbox" type="checkbox" /> <label for="wlrank">' + _("Separate waiting list rank by species") + '</label>',
                '</p>',
                '<table>',
                '<tr>',
                '<td><label for="wlupdate">' + _("Waiting list urgency update period in days") + '</label></td>',
                '<td><input data="WaitingListUrgencyUpdatePeriod" id="wlupdate" class="asm-textbox asm-numberbox" type="text" title="' + _("The period in days before waiting list urgency is increased") + '" />',
                html.info(_("Set to 0 to never update urgencies.")),
                '</td>',
                '</tr>',
                '<tr>',
                '<td><label for="wldu">' + _("Default urgency") + '</label></td>',
                '<td><select data="WaitingListDefaultUrgency" id="wldu" class="asm-selectbox">',
                html.list_to_options(controller.urgencies, "ID", "URGENCY"),
                '</select>',
                '</td>',
                '</tr>',
                '<tr>',
                '<td><label for="wlcolumns">' + _("Columns displayed") + '</label></td>',
                '<td>',
                '<select id="wlcolumns" class="asm-bsmselect" data="WaitingListViewColumns" multiple="multiple">',
                options.two_pair_options(controller.waitinglistcolumns),
                '</select>',
                '</tr>',
                '</table>',
                '</div>'
            ].join("\n");
        },

        render_options: function() {
            return [
                '<div id="tab-options">',
                '<p class="asm-header">' + _("Display") + '</p>',
                '<p>',
                '<input data="rc:DisableEffects" id="disableeffects" class="asm-checkbox" type="checkbox" /> <label for="disableeffects">' + _("Enable visual effects") + '</label><br />',
                '<!-- <input data="FancyTooltips" id="fancytooltips" class="asm-checkbox" type="checkbox" /> <label for="fancytooltips">' + _("Use fancy tooltips") + '</label><br /> -->',
                '<input data="rc:DontUseHTML5Scaling" id="disablehtml5scaling" class="asm-checkbox" type="checkbox" /> <label for="disablehtml5scaling">' + _("Use HTML5 client side image scaling where available to speed up image uploads") + '</label><br />',
                '<input data="PDFInline" id="pdfinline" class="asm-checkbox" type="checkbox" /> <label for="pdfinline">' + _("Show PDF files inline instead of sending them as attachments") + '</label><br />',
                '<input data="PicturesInBooks" id="picsinbooks" class="asm-checkbox" type="checkbox" /> <label for="picsinbooks">' + _("Show animal thumbnails in movement and medical books") + '</label><br />',
                '<input data="ShowPersonMiniMap" id="minimap" class="asm-checkbox" type="checkbox" /> <label for="minimap">' + _("Show a minimap of the address on person screens") + '</label><br />',
                '<input data="FloatingHeaders" id="floatingheaders" class="asm-checkbox" type="checkbox" /> <label for="floatingheaders">' + _("Keep table headers visible when scrolling") + '</label><br />',
                '<input data="RecordNewBrowserTab" id="recordnewbrowsertab" class="asm-checkbox" type="checkbox" /> <label for="recordnewbrowsertab">' + _("Open records in a new browser tab") + '</label><br />',
                '<input data="ReportNewBrowserTab" id="reportnewbrowsertab" class="asm-checkbox" type="checkbox" /> <label for="reportnewbrowsertab">' + _("Open reports in a new browser tab") + '</label><br />',
                '<input data="InactivityTimer" id="inactivitytimer" class="asm-checkbox" type="checkbox" /> <label for="inactivitytimer">' + _("Auto log users out after this many minutes of inactivity") + '</label>',
                '<input data="InactivityTimeout" id="inactivitytimeout" class="asm-textbox asm-numberbox" /><br />',
                '<label for="ownernameformat" style="margin-left: 24px">' + _("When displaying person names in lists, use the format") + '</label> ',
                '<select data="OwnerNameFormat" id="ownernameformat" type="text" class="asm-selectbox">',
                '<option value="{ownername}">' + _("Title First Last") + '</option>',
                '<option value="{ownertitle} {ownerinitials} {ownersurname}">' + _("Title Initials Last") + '</option>',
                '<option value="{ownerforenames} {ownersurname}">' + _("First Last") + '</option>',
                '<option value="{ownersurname}, {ownerforenames}">' + _("Last, First") + '</option>',
                '</select>',
                '</p>',
                '<p class="asm-header">' + _("Remove unwanted functionality") + '</p>',
                '<p>',
                '<input data="DisableRetailer" id="disableretailer" class="asm-checkbox" type="checkbox" /> <label for="disableretailer">' + _("Remove retailer functionality from the movement screens and menus") + '</label><br />',
                '<input data="DisableDocumentRepo" id="disabledocumentrepo" class="asm-checkbox" type="checkbox" /> <label for="disabledocumentrepo">' + _("Remove the document repository functionality from menus") + '</label><br />',
                '<input data="DisableOnlineForms" id="disableonlineforms" class="asm-checkbox" type="checkbox" /> <label for="disableonlineforms">' + _("Remove the online form functionality from menus") + '</label><br />',
                '<input data="DisableAsilomar" id="disableasilomar" class="asm-checkbox us" type="checkbox" /> <label for="disableasilomar" class="us">Remove the asilomar fields from the entry/deceased sections</label><br />',
                '<input data="DisableInvestigation" id="disableinvestigation" class="asm-checkbox" type="checkbox" /> <label for="disableinvestigation">' + _("Remove the investigation tab from person records") + '</label><br />',
                '<input data="HideTownCounty" id="towncounty" class="asm-checkbox" type="checkbox" /> <label for="towncounty">' + _("Remove the city/state fields from person details") + '</label><br />',
                '<input data="DontShowInsurance" id="insuranceno" class="asm-checkbox" type="checkbox" /> <label for="insuranceno">' + _("Remove the insurance number field from the movement screens") + '</label><br />',
                '<input data="DontShowCoatType" id="coattype" class="asm-checkbox" type="checkbox" /> <label for="coattype">' + _("Remove the coat type field from animal details") + '</label><br />',
                '<input data="DontShowSize" id="size" class="asm-checkbox" type="checkbox" /> <label for="size">' + _("Remove the size field from animal details") + '</label><br />',
                '<input data="DontShowMicrochip" id="microchip" class="asm-checkbox" type="checkbox" /> <label for="microchip">' + _("Remove the microchip fields from animal identification details") + '</label><br />',
                '<input data="DontShowTattoo" id="tattoo" class="asm-checkbox" type="checkbox" /> <label for="tattoo">' + _("Remove the tattoo fields from animal identification details") + '</label><br />',
                '<input data="DontShowNeutered" id="neutered" class="asm-checkbox" type="checkbox" /> <label for="neutered">' + _("Remove the neutered fields from animal health details") + '</label><br />',
                '<input data="DontShowDeclawed" id="declawed" class="asm-checkbox" type="checkbox" /> <label for="declawed">' + _("Remove the declawed box from animal health details") + '</label><br />',
                '<input data="DontShowRabies" id="rabiestag" class="asm-checkbox" type="checkbox" /> <label for="rabiestag">' + _("Remove the Rabies Tag field from animal health details") + '</label><br />',
                '<input data="DontShowGoodWith" id="goodwith" class="asm-checkbox" type="checkbox" /> <label for="goodwith">' + _("Remove the good with fields from animal notes") + '</label><br />',
                '<input data="DontShowHeartworm" id="heartworm" class="asm-checkbox" type="checkbox" /> <label for="heartworm">' + _("Remove the heartworm test fields from animal health details") + '</label><br />',
                '<input data="DontShowCombi" id="combitest" class="asm-checkbox" type="checkbox" /> <label for="combitest">' + _("Remove the FIV/L test fields from animal health details") + '</label><br />',
                '<input data="DontShowLitterID" id="litterid" class="asm-checkbox" type="checkbox" /> <label for="litterid">' + _("Remove the Litter ID field from animal details") + '</label><br />',
                '<input data="DontShowLocationUnit" id="subunit" class="asm-checkbox" type="checkbox" /> <label for="subunit">' + _("Remove the location unit field from animal details") + '</label><br />',
                '<input data="DontShowBonded" id="bonded" class="asm-checkbox" type="checkbox" /> <label for="bonded">' + _("Remove the bonded with fields from animal entry details") + '</label>',
                '</p>',
                '<p class="asm-header">' + _("When adding animals") + '</p>',
                '<p>',
                '<input data="AddAnimalsShowBreed" id="aashowbreed" class="asm-checkbox" type="checkbox" /> <label for="aashowbreed">' + _("Show the breed fields") + '</label><br />',
                '<input data="UseSingleBreedField" id="singlebreed" class="asm-checkbox" type="checkbox" /> <label for="singlebreed">' + _("Use a single breed field") + '</label><br />',
                '<input data="AddAnimalsShowColour" id="aashowcolour" class="asm-checkbox" type="checkbox" /> <label for="aashowcolour">' + _("Show the color field") + '</label><br />',
                '<input data="AddAnimalsShowLocation" id="aashowlocation" class="asm-checkbox" type="checkbox" /> <label for="aashowlocation">' + _("Show the internal location field") + '</label><br />',
                '<input data="AddAnimalsShowLocationUnit" id="aashowlocationunit" class="asm-checkbox" type="checkbox" /> <label for="aashowlocationunit">' + _("Show the location unit field") + '</label><br />',
                '<input data="AddAnimalsShowAcceptance" id="aashowacceptance" class="asm-checkbox" type="checkbox" /> <label for="aashowacceptance">' + _("Show the litter ID field") + '</label><br />',
                '<input data="AddAnimalsShowSize" id="aashowsize" class="asm-checkbox" type="checkbox" /> <label for="aashowsize">' + _("Show the size field") + '</label><br />',
                '<input data="AddAnimalsShowDateBroughtIn" id="aashowdatebroughtin" class="asm-checkbox" type="checkbox" /> <label for="aashowdatebroughtin">' + _("Show the date brought in field") + '</label><br />',
                '<input data="WarnSimilarAnimalName" id="warnsimilaranimal" class="asm-checkbox" type="checkbox" /> <label for="warnsimilaranimal">' + _("Warn if the name of the new animal is similar to one entered recently") + '</label>',
                '</p>',
                '</div>'
            ].join("\n");
        },

        render: function() {
            return [
                html.content_header(_("System Options")),
                '<div class="asm-toolbar">',
                '<button id="button-save" title="' + _("Update system options") + '">' + html.icon("save") + ' ' + _("Save") + '</button>',
                '</div>',
                '<div id="tabs">',
                this.render_tabs(),
                this.render_shelterdetails(),
                this.render_accounts(),
                this.render_agegroups(),
                this.render_animalcodes(),
                this.render_costs(),
                this.render_defaults(),
                this.render_diaryandmessages(),
                this.render_email(),
                this.render_findanimalperson(),
                this.render_homepage(),
                this.render_insurance(),
                this.render_lostandfound(),
                this.render_movements(),
                this.render_search(),
                this.render_waitinglist(),
                this.render_options(),
                '</div>',
                html.content_footer()
            ].join("\n");
        },

        bind: function() {
            var get_donation_mappings = function() {
                var mappings = "";
                $(".donmap").each(function() {
                    var t = $(this);
                    var idx = t.attr("id").substring(5, 6);
                    if (t.val() != "" && t.val() != "0" && t.val() != "-1") {
                        if (mappings != "") { mappings += ","; }
                        mappings += t.val() + "=" + $("#mapac" + idx).val();
                    }
                });
                return encodeURIComponent(mappings);
            };

            var update_flag = function() {
                var h = "<img style='position: relative; vertical-align: middle; left: -48px;' src='static/images/flags/" + 
                    $("#olocale").val() + ".png' title='" + 
                    $("#olocale").val() + "' />";
                $("#localeflag").html(h);
            };
            $("#olocale").change(update_flag);

            // Toolbar buttons
            $("#button-save").button().click(function() {
                $("#button-save").button("disable");
                var formdata = "mode=save&" + $("input, select, textarea").toPOST(true);
                formdata += "&DonationAccountMappings=" + get_donation_mappings();
                header.show_loading(_("Saving..."));
                common.ajax_post("options", formdata, function() { window.location = "options"; });
            });

            // Components
            $("#tabs").tabs({ show: "slideDown", hide: "slideUp" });

            $("#button-save").button("disable");

            // Load default values from the config settings
            $("input, select, textarea").each(function() {
                if ($(this).attr("data")) {
                    var d = $(this).attr("data");
                    if ($(this).is(".asm-currencybox")) {
                        $(this).val( html.decode(config.currency(d)));
                    }
                    else if ($(this).is("input:text")) {
                        $(this).val( html.decode(config.str(d)));
                    }
                    else if ($(this).is("input:checkbox")) {
                        if (d.indexOf("rc:") != -1) {
                            // it's a reverse checkbox, not it before setting
                            if (!config.bool(d.substring(3))) {
                                $(this).attr("checked", "checked");
                            }
                        }
                        else if (config.bool(d)) {
                            $(this).attr("checked", "checked");
                        }
                    }
                    else if ($(this).is("input:hidden")) {
                        $(this).val( config.str(d));
                    }
                    else if ($(this).is(".asm-selectbox")) {
                        $(this).select("value", config.str(d));
                    }
                    else if ($(this).is(".asm-bsmselect")) {
                        var ms = config.str(d).split(",");
                        var bsm = $(this);
                        $.each(ms, function(i, v) {
                            bsm.find("option[value='" + $.trim(v + "']")).attr("selected", "selected");
                        });
                        $(this).change();
                    }
                    else if ($(this).is("textarea")) {
                        $(this).val( html.decode(config.str(d)));
                    }
                }
            });

            // When the visual theme is changed, switch the CSS file so the
            // theme updates immediately.
            $("#systemtheme").change(function() {
                var theme = $("#systemtheme").val();
                var href = "https://ajax.googleapis.com/ajax/libs/jqueryui/1.10.3/themes/" + theme + "/jquery-ui.css";
                $("#jqt").attr("href", href);
                $("body").css("background-color", BACKGROUND_COLOURS[theme]);
            });

            // Set donation type maps from DonationAccountMappings field
            var donmaps = config.str("DonationAccountMappings");
            if (donmaps != "") {
                var maps = donmaps.split(",");
                $.each(maps, function(i, v) {
                    var dt = v.split("=")[0];
                    var ac = v.split("=")[1];
                    var idx = i + 1;
                    $("#mapdt" + idx).select("value", dt);
                    $("#mapac" + idx).select("value", ac);
                });
            }

            // Set flag for current locale
            update_flag();

            // Hide options not applicable for some locales
            if (asm.locale != "en") {
                $(".us").hide();
            }

            // Hide smtp settings if they've been overridden
            if (controller.hassmtpoverride) {
                $(".smtp").hide();
            }

            validate.bind_dirty();

        }
    };

    common.module(options, "options", "options");

});


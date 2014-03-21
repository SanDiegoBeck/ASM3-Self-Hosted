/*jslint browser: true, forin: true, eqeq: true, white: true, sloppy: true, vars: true, nomen: true */
/*global $, jQuery, _, asm, common, config, controller, dlgfx, format, header, html, validate */

$(function() {

    var move_reserve = {

        render: function() {
            return [
                '<div id="asm-content">',
                '<input id="movementid" type="hidden" />',
                '<div id="page1">',
                html.content_header(_("Reserve an animal"), true),
                '<div id="ownerwarn" class="ui-state-error ui-corner-all" style="margin-top: 5px; padding: 0 .7em; width: 60%; margin-left: auto; margin-right: auto">',
                '<p class="centered"><span class="ui-icon ui-icon-alert" style="float: left; margin-right: .3em;"></span>',
                '<span id="warntext" class="centered"></span>',
                '</p>',
                '</div>',
                '<div id="multiplereserve" class="ui-state-error ui-corner-all" style="margin-top: 5px; padding: 0 .7em; width: 60%; margin-left: auto; margin-right: auto">',
                '<p class="centered"><span class="ui-icon ui-icon-alert" style="float: left; margin-right: .3em;"></span>',
                '<span class="centered">' + _("This animal already has an active reservation.") + '</span>',
                '</p>',
                '</div>',
                '<div id="notonshelter" class="ui-state-error ui-corner-all" style="margin-top: 5px; padding: 0 .7em; width: 60%; margin-left: auto; margin-right: auto">',
                '<p class="centered"><span class="ui-icon ui-icon-alert" style="float: left; margin-right: .3em;"></span>',
                '<span class="centered">' + _("This animal is not on the shelter.") + '</span>',
                '</p>',
                '</div>',
                '<table class="asm-table-layout">',
                '<tr>',
                '<td>',
                '<label for="animal">' + _("Animal") + '</label>',
                '</td>',
                '<td>',
                '<input id="animal" data="animal" type="hidden" class="asm-animalchooser" value=\'\' />',
                '</td>',
                '</tr>',
                '<tr>',
                '<td>',
                '<label for="person">' + _("Reservation For") + '</label>',
                '</td>',
                '<td>',
                '<input id="person" data="person" type="hidden" class="asm-personchooser" value=\'\' />',
                '</td>',
                '</tr>',
                '<tr id="movementnumberrow">',
                '<td><label for="movementnumber">' + _("Movement Number") + '</label></td>',
                '<td><input id="movementnumber" data="movementnumber" class="asm-textbox" title=',
                '"' + html.title(_("A unique number to identify this movement")) + '"',
                ' /></td>',
                '</tr>',
                '<tr>',
                '<td><label for="reservationdate">' + _("Date") + '</label></td>',
                '<td>',
                '<input id="reservationdate" data="reservationdate" class="asm-textbox asm-datebox" title="' + html.title(_("The date the reservation is effective from")) + '" />',
                '</td>',
                '</tr>',
                '</table>',
                html.content_footer(),
                html.content_header(_("Donation"), true),
                '<table class="asm-table-layout">',
                '<tr>',
                '<td>',
                '<label for="donationtype">' + _("Type") + '</label>',
                '</td>',
                '<td>',
                '<select id="donationtype" data="donationtype" class="asm-selectbox">',
                html.list_to_options(controller.donationtypes, "ID", "DONATIONNAME"),
                '</select>',
                '</td>',
                '</tr>',
                '<tr>',
                '<td>',
                '<label for="payment">' + _("Payment Type") + '</label>',
                '</td>',
                '<td>',
                '<select id="payment" data="payment" class="asm-selectbox">',
                html.list_to_options(controller.paymenttypes, "ID", "PAYMENTNAME"),
                '</select>',
                '</td>',
                '</tr>',
                '<tr>',
                '<td>',
                '<label for="amount">' + _("Amount") + '</label>',
                '</td>',
                '<td>',
                '<input id="amount" data="amount" class="asm-currencybox asm-textbox" />',
                '</td>',
                '</tr>',
                '<tr class="seconddonation">',
                '<td>',
                '<label for="donationtype2">' + _("Type") + '</label>',
                '</td>',
                '<td>',
                '<select id="donationtype2" data="donationtype2" class="asm-selectbox">',
                html.list_to_options(controller.donationtypes, "ID", "DONATIONNAME"),
                '</select>',
                '</td>',
                '</tr>',
                '<tr class="seconddonation">',
                '<td>',
                '<label for="payment2">' + _("Payment Type") + '</label>',
                '</td>',
                '<td>',
                '<select id="payment2" data="payment2" class="asm-selectbox">',
                html.list_to_options(controller.paymenttypes, "ID", "PAYMENTNAME"),
                '</select>',
                '</td>',
                '</tr>',
                '<tr class="seconddonation">',
                '<td>',
                '<label for="amount2">' + _("Amount") + '</label>',
                '</td>',
                '<td>',
                '<input id="amount2" data="amount2" class="asm-currencybox asm-textbox" />',
                '</td>',
                '</tr>',
                '<tr id="giftaidrow">',
                '<td><label for="giftaid">' + _("Gift Aid") + '</label></td>',
                '<td><select id="giftaid" data="giftaid" class="asm-selectbox">',
                '<option value="0">' + _("Not eligible for gift aid") + '</option>',
                '<option value="1">' + _("Eligible for gift aid") + '</option>',
                '</select>',
                '</td>',
                '</tr>',
                '</table>',
                html.content_footer(),
                html.box(5),
                '<button id="reserve">' + html.icon("movement") + ' ' + _("Reserve") + '</button>',
                '</div>',
                '</div>',
                '<div id="page2">',
                '<div class="ui-state-highlight ui-corner-all" style="margin-top: 5px; padding: 0 .7em;">',
                '<p class="centered"><span class="ui-icon ui-icon-info" style="float: left; margin-right: .3em;"></span>',
                '<span class="centered">' + _("Reservation successfully created."),
                '</span>',
                '<span class="centered" id="reservefrom"></span>',
                html.icon("right"),
                '<span class="centered" id="reserveto"></span>',
                '</p>',
                '</div>',
                '<div id="asm-reserve-accordion">',
                '<h3><a href="#">' + _("Generate documentation") + '</a></h3>',
                '<div id="templatelist">',
                '</div>',
                '</div>',
                '</div>'
            ].join("\n");
        },

        bind: function() {
            var validation = function() {
                // Remove any previous errors
                header.hide_error();
                $("label").removeClass("ui-state-error-text");
                // animal
                if ($("#animal").val() == "") {
                    header.show_error(_("Movements require an animal"));
                    $("label[for='animal']").addClass("ui-state-error-text");
                    $("#animal").focus();
                    return false;
                }
                // person
                if ($("#person").val() == "") {
                    header.show_error(_("This type of movement requires a person."));
                    $("label[for='person']").addClass("ui-state-error-text");
                    $("#person").focus();
                    return false;
                }
                // date
                if ($.trim($("#reservationdate").val()) == "") {
                    header.show_error(_("This type of movement requires a date."));
                    $("label[for='reservationdate']").addClass("ui-state-error-text");
                    $("#reservationdate").focus();
                    return false;
                }
                return true;
            };

            // Callback when animal is changed
            $("#animal").animalchooser().bind("animalchooserchange", function(event, rec) {
              
                // Hide things before we start
                $("#notonshelter").fadeOut();
                $("#reserve").button("enable");

                // If the animal is not on the shelter and not fostered, show that warning
                // and stop everything else
                if (rec.ARCHIVED == "1" && rec.ACTIVEMOVEMENTTYPE != 2) {
                    $("#notonshelter").fadeIn();
                    $("#reserve").button("disable");
                    return;
                }

                // If the animal has an active reserve, show the warning, but
                // things can still continue
                if (rec.HASACTIVERESERVE == "1") {
                    $("#multiplereserve").fadeIn();
                }

                // Update the list of document templates
                var formdata = "mode=templates&id=" + rec.ID;
                common.ajax_post("move_reserve", formdata, function(data) { $("#templatelist").html(data); });

            });

            // Callback when person is changed
            $("#person").personchooser().bind("personchooserchange", function(event, rec) {
         
                // Set the gift aid box if they are registered
                $("#giftaid").select("value", rec.ISGIFTAID);
           
                // Owner banned?
                if (rec.ISBANNED == 1 && config.bool("WarnBannedOwner")) {
                    $("#warntext").text(_("This person has been banned from adopting animals"));
                    $("#ownerwarn").fadeIn();
                    return;
                }

                // Owner previously under investigation
                if (rec.INVESTIGATION > 0) {
                    $("#warntext").html(_("This person has been under investigation"));
                    $("#ownerwarn").fadeIn();
                    return;
                }

                // Owner not homechecked?
                if (rec.IDCHECK == 0 && config.bool("WarnNoHomeCheck")) {
                    $("#warntext").text(_("This person has not passed a homecheck"));
                    $("#ownerwarn").fadeIn();
                    return;
                }

                $("#ownerwarn").fadeOut();

            });

            // What to do when donation type is changed
            var donationtype_change = function() {
                var dc = common.get_field(controller.donationtypes, $("#donationtype").select("value"), "DEFAULTCOST");
                $("#amount").currency("value", dc);
            };
            $("#donationtype").change(function() {
                donationtype_change();
            });

            // What to do when second donation type is changed
            var donationtype2_change = function() {
                var dc = common.get_field(controller.donationtypes, $("#donationtype2").select("value"), "DEFAULTCOST");
                $("#amount2").currency("value", dc);
            };
            $("#donationtype2").change(function() {
                donationtype2_change();
            });

            $("#ownerwarn").hide();
            $("#notonshelter").hide();
            $("#multiplereserve").hide();

            $("#movementnumberrow").hide();
            if (config.bool("MovementNumberOverride")) {
                $("#movementnumberrow").show();
            }

            if (asm.locale != "en_GB") { $("#giftaidrow").hide(); }

            $("#page1").show();
            $("#page2").hide();
            $("#asm-reserve-accordion").accordion({
                heightStyle: "content"
            });

            // Set default values
            $("#donationtype").val(config.str("AFDefaultDonationType"));
            donationtype_change();
            $("#reservationdate").datepicker("setDate", new Date());

            // Show second donation field if option is set
            if (config.bool("SecondDonationOnMove")) {
                $(".seconddonation").show();
                $("#donationtype2").val($("#donationtype").val());
                $("#amount2").val($("#amount").val());
            }
            else {
                $(".seconddonation").hide();
            }

            $("#reserve").button().click(function() {
                if (!validation()) { return; }
                $("#reserve").button("disable");
                header.show_loading(_("Creating..."));

                var formdata = $("input, select").toPOST();
                common.ajax_post("move_reserve", formdata, function(data) {

                    $("#movementid").val(data);
                    header.hide_loading();

                    // Copy the animal/owner links to the success page so
                    // the user can go view them quickly again if they want
                    $("#reservefrom").html( $(".animalchooser-display").html() );
                    $("#reserveto").html( $(".personchooser-display .justlink").html() );

                    $("#page1").fadeOut(function() {
                        $("#page2").fadeIn();
                    });
                }, function() {
                    $("#reserve").button("enable");
                });
            });
        }
    };

    common.module(move_reserve, "move_reserve", "newdata");

});

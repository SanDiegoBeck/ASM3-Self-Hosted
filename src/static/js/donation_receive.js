/*jslint browser: true, forin: true, eqeq: true, white: true, sloppy: true, vars: true, nomen: true */
/*global $, jQuery, _, asm, common, config, controller, dlgfx, format, header, html, validate */

$(function() {

    var donation_receive = {

        render: function() {
            return [
                html.content_header(_("Receive a donation")),
                '<table class="asm-table-layout">',
                '<tr>',
                '<td>',
                '<label for="animal">' + _("Animal (optional)") + '</label>',
                '</td>',
                '<td>',
                '<input id="animal" data="animal" type="hidden" class="asm-animalchooser" value=\'\' />',
                '</td>',
                '</tr>',
                '<tr>',
                '<td>',
                '<label for="person">' + _("Person") + '</label>',
                '</td>',
                '<td>',
                '<input id="person" data="person" type="hidden" class="asm-personchooser" value=\'\' />',
                '</td>',
                '</tr>',
                '<tr>',
                '<td><label for="received">' + _("Received") + '</label></td>',
                '<td>',
                '<input id="received" data="received" class="asm-textbox asm-datebox" title=\'' + _("The date the donation was received") + '\' />',
                '</td>',
                '</tr>',
                '<tr>',
                '<td>',
                '<label for="type">' + _("Type") + '</label>',
                '</td>',
                '<td>',
                '<select id="type" data="type" class="asm-selectbox">',
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
                '<tr id="giftaidrow">',
                '<td><label for="giftaid">' + _("Gift Aid") + '</label></td>',
                '<td><select id="giftaid" data="giftaid" class="asm-selectbox">',
                '<option value="0">' + _("Not eligible for gift aid") + '</option>',
                '<option value="1">' + _("Eligible for gift aid") + '</option>',
                '</select>',
                '</td>',
                '</tr>',
                '</table>',
                '<div class="centered" style="margin-top: 10px">',
                '<button id="receive">' + html.icon("donation") + ' ' + _("Receive") + '</button>',
                '</div>',
                html.content_footer()
            ].join("\n");
        },

        bind: function() {
            var validation = function() {
                // Remove any previous errors
                header.hide_error();
                $("label").removeClass("ui-state-error-text");
                // person
                if ($("#person").val() == "0") {
                    header.show_error(_("Donations require a person"));
                    $("label[for='person']").addClass("ui-state-error-text");
                    $("#person").focus();
                    return false;
                }
                // date
                if ($.trim($("#received").val()) == "") {
                    header.show_error(_("Donations require a received date"));
                    $("label[for='received']").addClass("ui-state-error-text");
                    $("#received").focus();
                    return false;
                }
                return true;
            };

            // Look up default amount when type is changed
            var donationtype_change = function() {
                common.ajax_post("move_adopt", 
                    "mode=donationdefault&donationtype=" + $("#type").val(),
                    function(result) { $("#amount").currency("value", result); });
            };
            $("#type").change(function() {
                donationtype_change();
            });


            if (asm.locale != "en_GB") { $("#giftaidrow").hide(); }

            // Set default values
            $("#type").val(config.str("AFDefaultDonationType"));
            donationtype_change();
            $("#received").datepicker("setDate", new Date());

            $("#receive").button().click(function() {
                if (!validation()) { return; }
                $("#receive").button("disable");
                header.show_loading(_("Creating..."));

                var formdata = $("input, select").toPOST();
                common.ajax_post("donation_receive", formdata, function(result) { 
                    header.hide_loading();
                    header.show_info(_("Donation of {0} successfully received ({1}).").replace("{0}", $("#amount").val()).replace("{1}", $("#received").val()));
                    $("#receive").button("enable");
                }, function() {
                    $("#receive").button("enable");
                });
            });
        }
    };

    common.module(donation_receive, "donation_receive", "newdata");

});

/*jslint browser: true, forin: true, eqeq: true, white: true, sloppy: true, vars: true, nomen: true */
/*global $, _, asm, common, config, controller, dlgfx, format, header, html, tableform, validate */

$(function() {

    var accounts_trx = {

        render: function() {
            return [
                '<div id="dialog-edit" style="display: none" title="' + html.title(_("Edit transaction")) + '">',
                '<div class="ui-state-highlight ui-corner-all" style="margin-top: 20px; padding: 0 .7em">',
                '<p><span class="ui-icon ui-icon-info" style="float: left; margin-right: .3em;"></span>',
                _("Transactions need a date and description."),
                '</p>',
                '</div>',
                '<input type="hidden" id="trxid" />',
                '<table width="100%">',
                '<tr>',
                '<td><label for="description">' + _("Description") + '</label></td>',
                '<td><input id="description" data="description" class="asm-textbox" /></td>',
                '</tr>',
                '<tr>',
                '<td><label for="trxdate">' + _("Date") + '</label></td>',
                '<td><input id="trxdate" data="trxdate" class="asm-textbox asm-datebox" /></td>',
                '</tr>',
                '<tr>',
                '<td><label for="reconciled">' + _("Reconciled") + '</label></td>',
                '<td><select id="reconciled" data="reconciled" class="asm-selectbox">',
                '<option value="0">' + _("Not reconciled") + '</option>',
                '<option value="1">' + _("Reconciled") + '</option>',
                '</select>',
                '</td>',
                '</tr>',
                '<tr>',
                '<td>' + _("Account") + '</td>',
                '<td><span id="thisaccount">' + controller.accountcode + '</span></td>',
                '</td>',
                '</tr>',
                '<tr>',
                '<td><label for="otheraccount">' + _("Other Account") + '</label></td>',
                '<td><input id="otheraccount" data="otheraccount" class="asm-textbox" /></td>',
                '</tr>',
                '<tr id="personrow">',
                '<td><label for="person">' + _("Donation From") + '</label></td>',
                '<td>',
                '<a id="personlink" class="asm-embed-name" href="#"></a> <img src="static/images/icons/right.gif" />',
                '<a id="animallink" class="asm-embed-name" href="#"></a>',
                '</td>',
                '</tr>',
                '<tr>',
                '<td><label for="deposit">' + _("Deposit") + '</label></td>',
                '<td><input id="deposit" data="deposit" class="asm-textbox asm-currencybox" /></td>',
                '</tr>',
                '<tr>',
                '<td><label for="withdrawal">' + _("Withdrawal") + '</label></td>',
                '<td><input id="withdrawal" data="withdrawal" class="asm-textbox asm-currencybox" /></td>',
                '</tr>',
                '</table>',
                '</div>',
                html.content_header(_("Transactions")),
                '<form id="criteria" action="accounts_trx" method="GET">',
                '<input type="hidden" name="accountid" value="' + controller.accountid + '" />',
                '<table width="100%">',
                '<tr>',
                '<td>' + _("Show transactions from") + '</td>',
                '<td><input id="fromdate" name="fromdate" type="text" class="asm-textbox asm-datebox" /></td>',
                '<td>' + _("to") + '</td>',
                '<td><input id="todate" name="todate" type="text" class="asm-textbox asm-datebox" /></td>',
                '<td>' + _("Reconciled") + '</td>',
                '<td><select id="recfilter" name="recfilter" class="asm-selectbox">',
                '<option value="0">' + _("Both") + '</option>',
                '<option value="1">' + _("Reconciled") + '</option>',
                '<option value="2">' + _("Not Reconciled") + '</option>',
                '</select></td>',
                '<td><button id="button-refresh">' + html.icon("refresh") + ' ' + _("Refresh") + '</button></td>',
                '</tr>',
                '</table>',
                '</form>',
                '<div class="asm-toolbar">',
                '<button id="button-delete">' + html.icon("delete") + ' ' + _("Delete") + '</button>',
                '<button id="button-reconcile">' + html.icon("transactions") + ' ' + _("Reconcile") + '</button>',
                '</div>',
                '<table id="table-trx" width="100%">',
                '<thead>',
                '<tr>',
                '<th class="left">' + _("Date") + '</th>',
                '<th class="left">' + _("R") + '</th>',
                '<th class="left">' + _("Description") + '</th>',
                '<th class="left">' + _("Account") + '</th>',
                '<th class="right">' + _("Deposit") + '</th>',
                '<th class="right">' + _("Withdrawal") + '</th>',
                '<th class="right">' + _("Balance") + '</th>',
                '</tr>',
                '</thead>',
                '<tbody>',
                this.render_tablebody(),
                '<tr>',
                '<td class="newrow left"><input id="newtrxdate" data="trxdate" type="text" class="asm-halftextbox asm-datebox" />',
                '<input id="newaccountid" data="accountid" type="hidden" value="' + controller.accountid + '" />',
                '</td>',
                '<td class="newrow left"><input id="newreconciled" data="reconciled" type="checkbox" class="asm-checkbox" /></td>',
                '<td class="newrow left"><input id="newdesc" data="description" type="text" class="asm-textbox" /></td>',
                '<td class="newrow left"><input id="newacc" data="otheraccount" class="asm-textbox" /></td>',
                '<td class="newrow right"><input id="newdeposit" data="deposit" type="text" class="asm-halftextbox asm-currencybox" /></td>',
                '<td class="newrow right"><input id="newwithdrawal" data="withdrawal" type="text" class="asm-halftextbox asm-currencybox" /></td>',
                '<td class="newrow right"><button id="button-add">' + html.icon("new") + ' ' + _("Add") + '</button></td>',
                '</tr>',
                '</tbody>',
                '</table>',
                html.content_footer(),
                '<div id="spacer" style="height: 100px" />'
            ].join("\n");
        },

        render_tablebody: function() {
            var h = [],
                tdc = "even",
                futuredrawn = false,
                reconciled = "";
            $.each(controller.rows, function(i, t) {
                tdc = (tdc == "even" ? "odd" : "even");
                if (format.date_js(t.TRXDATE) > new Date() && !futuredrawn) {
                    tdc += " future";
                    futuredrawn = true;
                }
                if (t.RECONCILED == 1) {
                    reconciled = _("R");
                }
                else {
                    reconciled = "";
                }
                h.push("<tr>");
                h.push('<td class="' + tdc + ' left">');
                h.push('<span style="white-space: nowrap">');
                h.push('<input type="checkbox" data="' + t.ID + '" title="' + _('Select') + '" />');
                h.push('<a href="#" class="trx-edit-link asm-embed-name" data-id="' + t.ID + '">' + format.date(t.TRXDATE) + '</a>');
                h.push('</span>');
                h.push('</td>');
                h.push('<td class="' + tdc + ' left">' + reconciled + '</td>');
                h.push('<td class="' + tdc + ' left">' + html.truncate(t.DESCRIPTION) + '</td>');
                h.push('<td class="' + tdc + ' left">' + t.OTHERACCOUNTCODE + '</td>');
                h.push('<td class="right ' + tdc + '">' + format.currency(t.DEPOSIT) + '</td>');
                h.push('<td class="right ' + tdc + '">' + format.currency(t.WITHDRAWAL) + '</td>');
                h.push('<td class="right ' + tdc + '">' + format.currency(t.BALANCE) + '</td>');
                h.push('</tr>');
            });
            return h.join("\n");
        },

        bind: function () {
            var validate_account = function(selector) {
                // Returns true if the value of $(selector) is a valid account code
                var v = $(selector).val(),
                    codes = html.decode(controller.codes).split("|"),
                    validcode;
                $.each(codes, function(i, c) {
                    if (c == v) {
                        validcode = v;
                        return false;
                    }
                });
                if (validcode) {
                    return true;
                }
                $(selector).focus();
                header.show_error(String(_("Account code '{0}' is not valid.").replace("{0}", v)));
                return false;
            };

            $("#table-trx input:checkbox").change(function() {
                if ($("#table-trx input:checked").size() > 0) {
                    $("#button-delete").button("option", "disabled", false); 
                    $("#button-reconcile").button("option", "disabled", false); 
                }
                else {
                    $("#button-delete").button("option", "disabled", true); 
                    $("#button-reconcile").button("option", "disabled", true); 
                }
                if ($(this).is(":checked")) {
                    $(this).closest("tr").find("td").addClass("highlight");
                }
                else {
                    $(this).closest("tr").find("td").removeClass("highlight");
                }
            });

            var editbuttons = { };
            editbuttons[_("Save")] = function() {
                $("#dialog-edit label").removeClass("ui-state-error-text");
                if (!validate_account("#otheraccount")) { return; }
                if (!validate.notblank([ "trxdate", "otheraccount", "description", "deposit", "withdrawal" ])) { return; }
                var formdata = "mode=update&trxid=" + $("#trxid").val() + "&accountid=" + controller.accountid + "&" +
                    $("#dialog-edit input, #dialog-edit select").toPOST();
                $("#dialog-edit").disable_dialog_buttons();
                common.ajax_post("accounts_trx", formdata, function() { $("#criteria").submit(); }, function() { $("#dialog-edit").dialog("close"); });
            };
            editbuttons[_("Cancel")] = function() {
                $("#dialog-edit").dialog("close");
            };

            $("#dialog-edit").dialog({
                autoOpen: false,
                modal: true,
                width: 550,
                dialogClass: "dialogshadow",
                show: dlgfx.add_show,
                hide: dlgfx.add_hide,
                buttons: editbuttons
            });

            $("#button-reconcile").button({disabled: true}).click(function() {
                $("#button-reconcile").button("disable");
                var formdata = "mode=reconcile&ids=" + $("#table-trx input").tableCheckedData();
                common.ajax_post("accounts_trx", formdata, function() { $("#criteria").submit(); });
            });

            $("#button-refresh").button().click(function() {
                $("#criteria").submit();
            });

            $("#button-add").button().click(function() {
                if (!validate_account("#newacc")) { return; }
                if (!validate.notblank([ "newtrxdate", "newdesc", "newacc" ])) { return; }
                $("#button-add").button("disable");
                var formdata = "mode=create&accountid=" + controller.accountid + "&" +
                    $("#table-trx input, #table-trx select").toPOST();
                common.ajax_post("accounts_trx", formdata, function() { $("#criteria").submit(); });
            });

            $("#button-delete").button({disabled: true}).click(function() {
                tableform.delete_dialog(function() {
                    var formdata = "mode=delete&ids=" + $("#table-trx input").tableCheckedData();
                    $("#dialog-delete").disable_dialog_buttons();
                    common.ajax_post("accounts_trx", formdata, function() { $("#criteria").submit(); });
                });
            });

            $(".trx-edit-link").click(function() {
                if (accounts_trx.readonly) { return false; }
                var row = common.get_row(controller.rows, $(this).attr("data-id"));
                $("#dialog-edit label").removeClass("ui-state-error-text");
                $("#trxid").val(row.ID);
                $("#trxdate").val(format.date(row.TRXDATE));
                $("#description").val(html.decode(row.DESCRIPTION));
                $("#reconciled").select("value", row.RECONCILED);
                $("#otheraccount").val(html.decode(row.OTHERACCOUNTCODE));
                if (!row.PERSONNAME) {
                    $("#personrow").hide();
                }
                else {
                    $("#personlink").html(row.PERSONNAME);
                    $("#personlink").prop("href", "person_donations?id=" + row.PERSONID);
                    $("#personrow").show();
                    $("#animallink").html(row.ANIMALCODE + " " + row.ANIMALNAME);
                    $("#animallink").prop("href", "animal_donations?id=" + row.ANIMALID);
                }
                common.inject_target();
                $("#deposit").val(format.currency(row.DEPOSIT));
                $("#withdrawal").val(format.currency(row.WITHDRAWAL));
                $("#dialog-edit").dialog("open");
                $("#description").focus();
                return false; // prevents # href
            });

        },

        readonly: false,

        sync: function() {

            // When first loaded, scroll to the bottom of the page and make the
            // new description active
            setTimeout(function() {
                $("html, body").animate({scrollTop: $(document).height()});
                $("#newdesc").focus();
            }, 1000);

            // Set the filter at the top to match our current view
            $("#recfilter").select("value", controller.recfilter);
            $("#fromdate").val(controller.fromdate);
            $("#todate").val(controller.todate);

            // Default values for the new row
            $("#newtrxdate").datepicker("setDate", new Date());
            $("#newacc").autocomplete({ source: html.decode(controller.codes).split("|") });
            $("#otheraccount").autocomplete({ source: html.decode(controller.codes).split("|") });

            // If this account has edit roles set and our user is
            // not a superuser and not in one of those roles then
            // hide the add row and prevent editing the transactions
            if (controller.accounteditroles && !asm.superuser && !common.array_overlap(controller.accounteditroles.split("|"), asm.roleids.split("|"))) {
                accounts_trx.readonly = true;
                $(".newrow").hide();
                $("#asm-content .asm-toolbar").hide();
            }
        }
    };

    common.module(accounts_trx, "accounts_trx", "book");

});

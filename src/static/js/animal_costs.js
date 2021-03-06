/*jslint browser: true, forin: true, eqeq: true, white: true, sloppy: true, vars: true, nomen: true */
/*global $, _, asm, common, config, controller, dlgfx, edit_header, format, header, html, tableform, validate */

$(function() {

    var animal_costs;

    var dialog = {
        add_title: _("Add cost"),
        edit_title: _("Edit cost"),
        helper_text: _("Costs need a date and amount."),
        close_on_ok: true,
        columns: 1,
        width: 550,
        fields: [
            { json_field: "COSTTYPEID", post_field: "type", label: _("Type"), type: "select", options: { displayfield: "COSTTYPENAME", valuefield: "ID", rows: controller.costtypes }},
            { json_field: "COSTDATE", post_field: "costdate", label: _("Date"), type: "date", validation: "notblank", defaultval: new Date() },
            { json_field: "COSTAMOUNT", post_field: "cost", label: _("Cost"), type: "currency" },
            { json_field: "DESCRIPTION", post_field: "description", label: _("Description"), type: "textarea" }
        ]
    };

    var table = {
        rows: controller.rows,
        idcolumn: "ID",
        edit: function(row) {
            tableform.dialog_show_edit(dialog, row, function() {
                tableform.fields_update_row(dialog.fields, row);
                row.COSTTYPENAME = common.get_field(controller.costtypes, row.COSTTYPEID, "COSTTYPENAME");
                tableform.fields_post(dialog.fields, "mode=update&costid=" + row.ID, "animal_costs", function(response) {
                    tableform.table_update(table);
                    animal_costs.calculate_costtotals();
                });
            });
        },
        columns: [
            { field: "COSTTYPENAME", display: _("Type") },
            { field: "COSTDATE", display: _("Date"), initialsort: true, initialsortdirection: "desc", formatter: tableform.format_date },
            { field: "COSTAMOUNT", display: _("Cost"), formatter: tableform.format_currency },
            { field: "DESCRIPTION", display: _("Description") }
        ]
    };

    var buttons = [
         { id: "new", text: _("New Cost"), icon: "new", enabled: "always", 
             click: function() { 
                 tableform.dialog_show_add(dialog, function() {
                     tableform.fields_post(dialog.fields, "mode=create&animalid="  + controller.animal.ID, "animal_costs", function(response) {
                         var row = {};
                         row.ID = response;
                         tableform.fields_update_row(dialog.fields, row);
                         row.COSTTYPENAME = common.get_field(controller.costtypes, row.COSTTYPEID, "COSTTYPENAME");
                         controller.rows.push(row);
                         tableform.table_update(table);
                         animal_costs.calculate_costtotals();
                     });
                 }, function() { animal_costs.costtype_change(); });
             } 
         },
         { id: "delete", text: _("Delete"), icon: "delete", enabled: "multi", 
             click: function() { 
                 tableform.delete_dialog(function() {
                     tableform.buttons_default_state(buttons);
                     var ids = tableform.table_ids(table);
                     common.ajax_post("animal_costs", "mode=delete&ids=" + ids , function() {
                         tableform.table_remove_selected_from_json(table, controller.rows);
                         tableform.table_update(table);
                         animal_costs.calculate_costtotals();
                     });
                 });
             } 
         },
         { type: "raw", markup: [
             '<span id="onshelterboard" style="float: right">',
             _("Daily Boarding Cost"),
             ' <input id="dailyboardingcost" type="textbox" class="asm-textbox asm-currencybox" />',
             '<button id="button-savecost">' + _("Update the daily boarding cost for this animal") + '</button>',
             '<span id="costonshelter"></span>',
             '</span>'
             ].join("\n")
         }
    ];

    animal_costs = {

        render: function() {
            var s = "";
            s += tableform.dialog_render(dialog);
            s += edit_header.animal_edit_header(controller.animal, "costs", controller.tabcounts);
            s += tableform.buttons_render(buttons);
            s += tableform.table_render(table);
            s += [
                '<div id="asm-cost-footer">',
                '<div class="ui-state-highlight ui-corner-all" style="margin-top: 20px; padding: 0 .7em">',
                '<p><span class="ui-icon ui-icon-info" style="float: left; margin-right: .3em;"></span>',
                '<span id="costtotals"></span>',
                '</div>',
                '</div>'
            ].join("\n");
            s += html.content_footer();
            return s;
        },

        bind: function() {
            $(".asm-tabbar").asmtabs();
            tableform.dialog_bind(dialog);
            tableform.buttons_bind(buttons);
            tableform.table_bind(table, buttons);
            
            $("#type").change(animal_costs.costtype_change);

            $("#button-savecost")
                .button({ icons: { primary: "ui-icon-disk" }, text: false })
                .click(animal_costs.save_boarding_cost);

            $("#dailyboardingcost").keyup(function() {
                animal_costs.recalc_daysonshelter();
                animal_costs.calculate_costtotals();
            });

            $("#button-savecost").button("disable");

            // If the animal isn't on the shelter, daysonshelter == 0 so hide running board
            if (controller.animal.DAYSONSHELTER == 0) {
                $("#onshelterboard").hide();
            }

        },

        costtype_change: function() {
            var dc = common.get_field(controller.costtypes, $("#type").select("value"), "DEFAULTCOST");
            $("#cost").currency("value", dc);
        },

        sync: function() {
            $("#dailyboardingcost").currency("value", controller.animal.DAILYBOARDINGCOST);
            animal_costs.recalc_daysonshelter();
            animal_costs.calculate_costtotals();
        },

        calculate_costtotals: function() {
            var s = _("Vaccinations: {0}, Tests: {1}, Medical Treatments: {2}, Costs: {3}, Total Costs: {4} Total Donations: {5}, Balance: {6}");
            var bc = $("#dailyboardingcost").currency("value");
            if (!bc) { bc = config.integer("DefaultDailyBoardingCost"); }
            var dons = format.to_int(controller.animal.DAYSONSHELTER);
            var tb = bc * dons;
            var tv = format.to_int(controller.costtotals.TV);
            var tt = format.to_int(controller.costtotals.TT);
            var tm = format.to_int(controller.costtotals.TM);
            var tc = 0;
            var td = format.to_int(controller.costtotals.TD);
            // Calculate tc from our current cost rows
            $.each(controller.rows, function(i, v) {
                tc += format.to_int(v.COSTAMOUNT);
            });
            // Total without boarding costs
            var totc = tv + tt + tm + tc;
            // Only add current boarding cost if the animal is on the shelter
            if (controller.animal.ARCHIVED == 0) { totc += tb; }
            var bal = td - totc;
            $("#costtotals").html(common.substitute(s,
                { 
                    "0": format.currency(tv), 
                    "1": format.currency(tt), 
                    "2": format.currency(tm),
                    "3": format.currency(tc),
                    "4": "<b>" + format.currency(totc) + "</b><br />",
                    "5": format.currency(td),
                    "6": "<b>" + format.currency(bal) + "</b>"
                }));
        },

        recalc_daysonshelter: function() {
            var days = controller.animal.DAYSONSHELTER;
            var cost = format.currency_to_float($("#dailyboardingcost").val());
            var costrounded = format.float_to_dp(cost, asm.currencydp);
            var tot = (days * costrounded) * 100;
            var s = _("On shelter for {0} days. Total cost: {1}");
            s = s.replace("{0}", "<b>" + days + "</b>");
            s = s.replace("{1}", "<b>" + format.currency(tot) + "</b>");
            $("#costonshelter").html(s);
            $("#button-savecost").button("enable");
        },

        save_boarding_cost: function() {
            $("#button-savecost").button("disable");
            var formdata = "mode=dailyboardingcost&animalid=" + $("#animalid").val() + 
                "&dailyboardingcost=" + $("#dailyboardingcost").val();
            header.show_loading(_("Saving..."));
            common.ajax_post("animal_costs", formdata, function() { 
                $("#button-savecost").button("enable");
            }, function() {
                $("#button-savecost").button("enable");
            });
        }
    };

    common.module(animal_costs, "animal_costs", "formtab");

});

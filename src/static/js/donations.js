/*jslint browser: true, forin: true, eqeq: true, white: true, sloppy: true, vars: true, nomen: true */
/*global $, jQuery, _, asm, common, config, controller, dlgfx, edit_header, format, header, html, tableform, validate */

$(function() {

    var lastanimal,
        lastperson,
        dialog_row,
        donations = {};

    var dialog = {
        add_title: _("Add donation"),
        edit_title: _("Edit donation"),
        close_on_ok: false,
        width: 550,
        helper_text: _("Donations need at least one date, an amount and a person."),
        columns: 1,
        fields: [
            { json_field: "DONATIONTYPEID", post_field: "type", label: _("Type"), type: "select", options: { displayfield: "DONATIONNAME", valuefield: "ID", rows: controller.donationtypes }},
            { json_field: "DONATIONPAYMENTID", post_field: "payment", label: _("Payment Type"), type: "select", options: { displayfield: "PAYMENTNAME", valuefield: "ID", rows: controller.paymenttypes }},
            { json_field: "FREQUENCY", post_field: "frequency", label: _("Frequency"), type: "select", options: { displayfield: "FREQUENCY", valuefield: "ID", rows: controller.frequencies }},
            { json_field: "DATEDUE", post_field: "due", label: _("Due"), type: "date" },
            { json_field: "DATE", post_field: "received", label: _("Received"), type: "date" },
            { json_field: "DONATION", post_field: "amount", label: _("Amount"), type: "currency" },
            { json_field: "ISGIFTAID", post_field: "giftaid", label: _("Gift Aid"), type: "select", options: 
                '<option value="0">' + _("Not eligible for gift aid") + '</option>' +
                '<option value="1">' + _("Eligible for gift aid") + '</option>' },
            { json_field: "ANIMALID", post_field: "animal", label: _("Animal"), type: "animal" },
            { json_field: "OWNERID", post_field: "person", label: _("Person"), type: "person" },
            { json_field: "MOVEMENTID", post_field: "movement", label: _("Movement"), type: "select", options: "" },
            { json_field: "COMMENTS", post_field: "comments", label: _("Comments"), type: "textarea" }
        ]
    };

    var table = {
        rows: controller.rows,
        idcolumn: "ID",
        edit: function(row) {
            tableform.fields_populate_from_json(dialog.fields, row);
            dialog_row = row;
            donations.create_semaphore = false;
            donations.update_movements(row.OWNERID);
            tableform.dialog_show_edit(dialog, row, function() {
                if (!donations.validation()) { tableform.dialog_enable_buttons(); return; }
                tableform.fields_update_row(dialog.fields, row);
                donations.set_extra_fields(row);
                tableform.fields_post(dialog.fields, "mode=update&donationid=" + row.ID, controller.name, function(response) {
                    donations.calculate_total();
                    tableform.table_update(table);
                    tableform.dialog_close();
                },
                function(response) {
                    tableform.dialog_error(response);
                    tableform.dialog_enable_buttons();
                });
            });
        },
        complete: function(row) {
        },
        overdue: function(row) {
            return !row.DATE && format.date_js(row.DATEDUE) < common.today_no_time();
        },
        columns: [
            { field: "DONATIONNAME", display: _("Type") },
            { field: "PAYMENTNAME", display: _("Payment Type") },
            { field: "FREQUENCYNAME", display: _("Frequency") },
            { field: "DATEDUE", display: _("Due"), formatter: tableform.format_date },
            { field: "DATE", display: _("Received"), formatter: tableform.format_date, initialsort: true, initialsortdirection: "desc" },
            { field: "ID", display: _("Receipt No"), formatter: function(row) {
                return format.padleft(row.ID, 8);
            }},
            { field: "DONATION", display: _("Amount"), formatter: tableform.format_currency },
            { field: "PERSON", display: _("Person"),
                formatter: function(row) {
                    if (row.OWNERID) {
                        return edit_header.person_name_link(row, row.OWNERID);
                    }
                    return "";
                },
                hideif: function(row) {
                    return controller.name.indexOf("person_") != -1;
                }
            },
            { field: "ANIMAL", display: _("Animal"), 
                formatter: function(row) {
                    if (!row.ANIMALID || row.ANIMALID == 0) { return ""; }
                    return '<a href="animal?id=' + row.ANIMALID + '">' + row.ANIMALNAME + ' - ' + row.SHELTERCODE + '</a>';
                },
                hideif: function(row) {
                    return controller.name.indexOf("animal_") != -1;
                }
            },
            { field: "COMMENTS", display: _("Comments") }
        ]
    };

    var buttons = [
        { id: "new", text: _("New Donation"), icon: "new", enabled: "always", 
             click: function() { 
                donations.create_semaphore = true;
                $("#animal").animalchooser("clear");
                $("#person").personchooser("clear");
                if (controller.animal) {
                    $("#animal").animalchooser("loadbyid", controller.animal.ID);
                }
                if (controller.person) {
                    $("#person").personchooser("loadbyid", controller.person.ID);
                    donations.update_movements(controller.person.ID);
                }
                $("#type").select("value", config.integer("AFDefaultDonationType"));
                $("#giftaid").select("value", "0");
                donations.type_change();
                tableform.dialog_show_add(dialog, function() {
                    if (!donations.validation()) { tableform.dialog_enable_buttons(); return; }
                    tableform.fields_post(dialog.fields, "mode=create", controller.name, function(response) {
                        var row = {};
                        row.ID = response;
                        tableform.fields_update_row(dialog.fields, row);
                        donations.set_extra_fields(row);
                        controller.rows.push(row);
                        tableform.table_update(table);
                        donations.calculate_total();
                        tableform.dialog_close();
                    }, function() {
                        tableform.dialog_enable_buttons();   
                    });
                });
             } 
         },
         { id: "delete", text: _("Delete"), icon: "delete", enabled: "multi", 
             click: function() { 
                 tableform.delete_dialog(function() {
                     tableform.buttons_default_state(buttons);
                     var ids = tableform.table_ids(table);
                     common.ajax_post(controller.name, "mode=delete&ids=" + ids , function() {
                         tableform.table_remove_selected_from_json(table, controller.rows);
                         tableform.table_update(table);
                     donations.calculate_total();
                     });
                 });
             } 
         },
         { id: "receive", text: _("Receive"), icon: "complete", enabled: "multi", tooltip: _("Mark selected donations received"),
             click: function() {
                 var ids = tableform.table_ids(table);
                 common.ajax_post(controller.name, "mode=receive&ids=" + ids, function() {
                     $.each(controller.rows, function(i, v) {
                        if (tableform.table_id_selected(v.ID)) {
                            v.DATE = format.date_iso(new Date());
                        }
                     });
                     tableform.table_update(table);
                     donations.calculate_total();
                 });
             }
         },
         { id: "document", text: _("Receipt/Invoice"), icon: "document", enabled: "one", 
             tooltip: _("Generate document from this donation"), type: "buttonmenu" },
         { id: "offset", type: "dropdownfilter", 
             options: [ "m7|" + _("Received in last week"), 
                "m31|" + _("Received in last month"),
                "m365|" + _("Received in last year"),
                "d0|" + _("Overdue"),
                "p7|" + _("Due in next week"), 
                "p31|" + _("Due in next month"), 
                "p365|" + _("Due in next year") ],
             click: function(selval) {
                window.location = controller.name + "?offset=" + selval;
             },
             hideif: function(row) {
                 // Don't show for animal or person records
                 if (controller.animal || controller.person) {
                     return true;
                 }
             }
         }

    ];

    donations = {

        // Used to let person_loaded know whether we are creating or not
        create_semaphore: false,

        validation: function() {
            if (!validate.notzero(["person"])) { return false; }
            if ($("#due").val() == "" && $("#received").val() == "") {
                validate.notblank(["due", "received"]);
                return false;
            }
            return true;
        },

        type_change: function() {
            var dc = common.get_field(controller.donationtypes, $("#type").select("value"), "DEFAULTCOST");
            $("#amount").currency("value", dc);
        },

        update_movements: function(personid) {
            var formdata = "mode=personmovements&personid=" + personid;
            common.ajax_post(controller.name, "mode=personmovements&personid=" + personid,
                function(result) {
                    var h = "<option value=\"0\"></option>";
                    $.each(jQuery.parseJSON(result), function(i,v) {
                        h += "<option value=\"" + v.ID + "\">";
                        h += v.ADOPTIONNUMBER + " - " + v.MOVEMENTNAME + ": " + v.ANIMALNAME;
                        h += "</option>";
                    });
                    $("#movement").html(h);
                    if (dialog_row && dialog_row.MOVEMENTID) {
                        $("#movement").select("value", dialog_row.MOVEMENTID);
                    }
                    $("#movement").closest("tr").fadeIn();
                },
                function(jqxhr, textstatus, response) {
                    header.show_error(response);
                }
            );
        },

        set_extra_fields: function(row) {
            if (controller.animal) {
                row.ANIMALNAME = controller.animal.ANIMALNAME;
                row.SHELTERCODE = controller.animal.SHELTERCODE;
            }
            else if (lastanimal) {
                row.ANIMALNAME = lastanimal.ANIMALNAME;
                row.SHELTERCODE = lastanimal.SHELTERCODE;
            }
            else {
                row.ANIMALNAME = "";
                row.SHELTERCODE = "";
            }
            if (controller.person) {
                row.OWNERNAME = controller.person.OWNERNAME;
                row.OWNERADDRESS = controller.person.OWNERADDRESS;
                row.HOMETELEPHONE = controller.person.HOMETELEPHONE;
                row.WORKTELEPHONE = controller.person.WORKTELEPHONE;
                row.MOBILETELEPHONE = controller.person.MOBILETELEPHONE;
            }
            else if (lastperson) {
                row.OWNERNAME = lastperson.OWNERNAME;
                row.OWNERADDRESS = lastperson.OWNERADDRESS;
                row.HOMETELEPHONE = lastperson.HOMETELEPHONE;
                row.WORKTELEPHONE = lastperson.WORKTELEPHONE;
                row.MOBILETELEPHONE = lastperson.MOBILETELEPHONE;
            }
            row.DONATIONNAME = common.get_field(controller.donationtypes, row.DONATIONTYPEID, "DONATIONNAME");
            row.PAYMENTNAME = common.get_field(controller.paymenttypes, row.DONATIONPAYMENTID, "PAYMENTNAME");
            row.FREQUENCYNAME = common.get_field(controller.frequencies, row.FREQUENCY, "FREQUENCY");
        },

        calculate_total: function() {
            var tot = 0, due = 0;
            $.each(controller.rows, function(i, v) {
                if (v.DATE) { tot += v.DONATION; }
                else { due += v.DONATION; }
            });
            $("#donationtotal").html(format.currency(tot) + " / " + format.currency(due));
        },

        render: function() {
            var s = "";
            s += tableform.dialog_render(dialog);
            s += '<div id="button-document-body" class="asm-menu-body">' +
                '<ul class="asm-menu-list">' +
                edit_header.template_list(controller.templates, "DONATION", 0) +
                '</ul></div>';
            if (controller.name == "animal_donations") {
                s += edit_header.animal_edit_header(controller.animal, "donations", controller.tabcounts);
            }
            else if (controller.name == "person_donations") {
                s += edit_header.person_edit_header(controller.person, "donations", controller.tabcounts);
            }
            else {
                s += html.content_header(document.title);
            }
            s += tableform.buttons_render(buttons);
            s += tableform.table_render(table);
            s += '<div class="ui-state-highlight ui-corner-all" style="margin-top: 20px; padding: 0 .7em">';
            s += '<p><span class="ui-icon ui-icon-info" style="float: left; margin-right: .3em;"></span>';
            s += _("Total donations") + ': <span class="strong" id="donationtotal"></span>';
            s += '</p></div>';
            s += html.content_footer();
            return s;
        },

        bind: function() {

            tableform.dialog_bind(dialog);
            tableform.buttons_bind(buttons);
            tableform.table_bind(table, buttons);

            if (controller.name.indexOf("animal_") != -1) {
                $("#animal").closest("tr").hide();
                $(".asm-tabbar").asmtabs();
            }
            if (controller.name.indexOf("person_") != -1) {
                $("#person").closest("tr").hide();
                $(".asm-tabbar").asmtabs();
            }
            if (asm.locale != "en_GB") {
                $("#giftaid").closest("tr").hide();
            }

            $("#movement").closest("tr").hide();

            $("#animal").animalchooser().bind("animalchooserchange", function(event, rec) {
                lastanimal = rec;
            });

            $("#animal").animalchooser().bind("animalchooserloaded", function(event, rec) {
                lastanimal = rec;
            });

            $("#person").personchooser().bind("personchooserchange", function(event, rec) {
                lastperson = rec;
                donations.update_movements(rec.ID);
                $("#giftaid").select("value", rec.ISGIFTAID);
            });

            $("#person").personchooser().bind("personchooserloaded", function(event, rec) {
                lastperson = rec;
                if (donations.create_semaphore) {
                    $("#giftaid").select("value", rec.ISGIFTAID);
                }
            });

            $("#type").change(function() {
                donations.type_change();
            });

            // Add click handlers to templates to figure out where to go based
            // on the selected donations
            $(".templatelink").click(function() {
                var template_name = $(this).attr("data");
                $("#tableform input:checked").each(function() {
                    var did = $(this).attr("data-id");
                    window.location = "document_gen?mode=DONATION&id=" + did + "&template=" + template_name;
                });
                return false;
            });
        },

        sync: function() {

            this.calculate_total();

            // If an offset is given in the querystring, update the select
            if (common.current_url().indexOf("offset=") != -1) {
                var offurl = common.current_url().substring(common.current_url().indexOf("=")+1);
                $("#offset").select("value", offurl);
            }

        }
    };

    common.module(donations, "donations", common.current_url().indexOf("book") != -1 ? "book" : "formtab");

});

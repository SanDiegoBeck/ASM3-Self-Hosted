#!/usr/bin/python

import additional
import animal
import configuration
import diary
import html
import log
import lookups
import media
import medical
import person
import reports
import smcom
import users
from i18n import _, python2display, now, add_days, add_months, add_years
from sitedefs import MULTIPLE_DATABASES
from sitedefs import JQUERY_JS, JQUERY_MOBILE_CSS, JQUERY_MOBILE_JS

def header(l):
    return """<!DOCTYPE html>
    <html>
    <head>
    <title>
    %(title)s
    </title>
    <meta name="viewport" content="width=device-width, initial-scale=1"> 
    %(css)s
    %(scripts)s
    <script type="text/javascript">
        $(document).ready(function() {

            // Flag if we have an idevice
            is_idevice = navigator.userAgent.toLowerCase().indexOf("ipod") != -1 || 
                navigator.userAgent.toLowerCase().indexOf("ipad") != -1 ||
                navigator.userAgent.toLowerCase().indexOf("iphone") != -1;

            // Flag if we have old Android (1/2)
            is_oldandroid = navigator.userAgent.indexOf("Android 2") != -1 ||
                navigator.userAgent.indexOf("Android 1") != -1;

            // If the user sets a new diary date in the future, post it
            $(".diaryon").change(function() {
                $.mobile.changePage("mobile_post?posttype=dia&on=" + $(this).val() + "&id=" + $(this).attr("data"));
            });

            // If the user chooses a test result, post it
            $(".testresult").change(function() {
                $.mobile.changePage("mobile_post?posttype=test&resultid=" + $(this).val() + 
                    "&animalid=" + $(this).attr("data-animal") + "&id=" + $(this).attr("data"));
            });

            $("#home a").attr("data-transition", "slide");
        });
    </script>
    <style>
    .asm-thumbnail {
        max-width: 70px;
        max-height: 70px;
    }
    </style>
    </head>
    <body>
    """ % {
        "title":    _("Animal Shelter Manager", l),
        "css":      html.css_tag("asm-icon.css"),
        "scripts":  JQUERY_JS + "\n" + JQUERY_MOBILE_CSS + "\n" + JQUERY_MOBILE_JS 
    }

def jqm_button(href, text, icon = "", ajax = ""):
    if icon != "": icon = "data-icon=\"%s\"" % icon
    if ajax != "": ajax = "data-ajax=\"%s\"" % ajax
    return "<a data-role=\"button\" %(icon)s %(ajax)s href=\"%(href)s\">%(text)s</a>" % { "icon": icon, "ajax": ajax, "href": href, "text": text }

def jqm_checkbox(name, checked = False):
    c = ""
    if checked: c = "checked=\"checked\""
    return "<input type=\"checkbox\" id=\"%s\" name=\"%s\" %s />" % (name, name, c)

def jqm_collapsible(s, icon = ""):
    return "<div data-role=\"collapsible\" data-collapsed=\"true\" data-collapsed-icon=\"%s\">%s</div>\n" % (icon, s)

def jqm_collapsible_set(s):
    return "<div data-role=\"collapsible-set\">%s</div>\n" % s

def jqm_fieldcontain(name, label, inner):
    return "<div data-role=\"fieldcontain\"><label for=\"%(name)s\">%(label)s</label>%(inner)s</div>" % { "name": name, "label": label, "inner": inner }

def jqm_form(name, action="mobile_post", method="post"):
    return "<form id=\"%s\" action=\"%s\" method=\"%s\">\n" % (name, action, method)

def jqm_form_end():
    return "</form>\n"

def jqm_h3(s):
    return "<h3>%s</h3>\n" % s

def jqm_hidden(name, value):
    return "<input type=\"hidden\" id=\"%(name)s\" name=\"%(name)s\" value=\"%(value)s\" />\n" % { "name": name, "value": value }

def jqm_link(href, text, icon = "", linkclass = "", theme = ""):
    if linkclass != "": linkclass = "class=\"" + linkclass + "\""
    if icon != "": icon = "data-icon=\"" + icon + "\""
    if theme != "": theme = "data-theme=\"" + theme + "\""
    return "<a href=\"%(href)s\" %(linkclass)s %(icon)s %(theme)s>%(text)s</a>\n" % {
        "href": href, "text": text, "icon": icon, "linkclass": linkclass, "theme": theme }

def jqm_list(s, showfilter = False):
    return "<ul data-role=\"listview\" data-filter=\"%s\">\n%s</ul>\n" % (showfilter and "true" or "false", s)

def jqm_list_divider(s):
    return "<li data-role=\"list-divider\" role=\"heading\">%s</li>" % s

def jqm_listitem(s):
    return "<li>%s</li>" % s

def jqm_listitem_link(href, text = "", icon = "", counter = -1, rel = ""):
    counterdisplay = ""
    if counter >= 0: counterdisplay = "<span class=\"ui-li-count ui-btn-up-c ui-btn-corner-all\">%d</span>" % counter
    if icon != "": icon = html.icon(icon)
    if rel != "": rel = "data-rel=\"%s\"" % rel
    return "<li><a href=\"%(href)s\" %(rel)s>%(icon)s %(text)s %(counterdisplay)s</a></li>\n" % {
        "href": href, "text": text, "icon": icon, "counterdisplay": counterdisplay, "rel": rel }

def jqm_option(value, label = "", selected = False):
    if selected: selected = "selected=\"selected\""
    if label == "":
        return "<option %s>%s</option>" % (selected, value)
    return "<option value=\"%s\" %s>%s</option>\n" % (value, selected, label)

def jqm_options_next_month(l):
    d = now()
    days = []
    for dummy in xrange(0, 31):
        days.append(jqm_option(python2display(l,d)))
        d = add_days(d, 1)
    d = add_months(now(), 3)
    days.append(jqm_option(python2display(l,d)))
    d = add_months(now(), 6)
    days.append(jqm_option(python2display(l,d)))
    d = add_years(now(), 1)
    days.append(jqm_option(python2display(l,d)))
    return "\n".join(days)

def jqm_options_testresults(testresults):
    res = []
    for r in testresults:
        res.append(jqm_option(str(r["ID"]), r["RESULTNAME"]))
    return "\n".join(res)

def jqm_p(s):
    return "<p>%s</p>\n" % s

def jqm_page_footer():
    return "</div>\n</div>\n"

def jqm_page_header(pageid, title, link = "", backbutton = True):
    backbuttonattr = ""
    if backbutton: backbuttonattr = "data-add-back-btn=\"true\""
    if pageid != "": pageid = "id=\"%s\"" % pageid
    return "<div data-role=\"page\" %(back)s %(pageid)s\">\n" \
        "<div data-role=\"header\">" \
        "<h1>%(title)s</h1>%(link)s" \
        "</div>\n" \
        "<div data-role=\"content\">\n" % { 
            "pageid": pageid, "title": title, "link": link, "back": backbuttonattr }

def jqm_select(name, options, selclass = ""):
    if selclass != "": selclass = "class=\"" + selclass + "\""
    return "<select id=\"%(name)s\" name=\"%(name)s\" %(selclass)s>%(options)s</select>\n" % { "name": name, "options": options, "selclass": selclass }

def jqm_span(s):
    return "<span>%s</span>\n" % s

def jqm_submit(label):
    return "<button data-icon=\"check\" type=\"submit\">%s</button>\n" % label

def jqm_table():
    return "<table>\n"

def jqm_table_end():
    return "</table>\n"

def jqm_tablerow(cell1, cell2 = "", cell3 = "", cell4 = ""):
    s = "<tr>\n<td>" + cell1 + "</td>\n"
    if cell2 != "": s += "<td>%s</td>\n" % cell2
    if cell3 != "": s += "<td>%s</td>\n" % cell3
    if cell4 != "": s += "<td>%s</td>\n" % cell4
    s += "</tr>\n"
    return s

def jqm_text(name, value = ""):
    return "<input id=\"%(name)s\" name=\"%(name)s\" value=\"%(value)s\" type=\"text\" />\n" % { "name": name, "value": value }

def page(dbo, session, username):
    """
    Generates the main mobile web page
    dbo: Database info
    """
    l = dbo.locale
    nsa = animal.get_number_animals_on_shelter_now(dbo)
    osa = nsa > 0
    ar = reports.get_available_reports(dbo, False)
    vacc = medical.get_vaccinations_outstanding(dbo)
    test = medical.get_tests_outstanding(dbo)
    med = medical.get_treatments_outstanding(dbo)
    dia = diary.get_uncompleted_upto_today(dbo, username)
    hck = person.get_reserves_without_homechecks(dbo)
    mess = lookups.get_messages(dbo, session.user, session.roles, session.superuser)
    testresults = lookups.get_test_results(dbo)
    homelink = jqm_link("mobile", _("Home", l), "home", "ui-btn-right", "b")
    h = []

    h.append(header(l))

    logoutlink = jqm_link("mobile_logout", _("Logout", l), "delete", "ui-btn-right", "b")
    h.append(jqm_page_header("home", _("ASM", l), logoutlink , False))
    items = []
    if configuration.smdb_locked(dbo):
        items.append(jqm_listitem(_("This database is locked and in read-only mode. You cannot add, change or delete records.", l)))
    if len(mess) > 0: 
        items.append(jqm_listitem_link("#messages", _("Messages", l), "message", len(mess)))
    if len(ar) > 0 and users.check_permission_bool(session, users.VIEW_REPORT):
        items.append(jqm_listitem_link("#reports", _("Generate Report", l), "report"))
    items.append(jqm_list_divider(_("Animal", l)))
    if osa and users.check_permission_bool(session, users.VIEW_ANIMAL):
        items.append(jqm_listitem_link("mobile_post?posttype=vsa", _("View Shelter Animals", l), "animal", nsa))
    if len(vacc) > 0 and users.check_permission_bool(session, users.CHANGE_VACCINATION):
        items.append(jqm_listitem_link("#vacc", _("Vaccinate Animal", l), "vaccination", len(vacc)))
    if len(test) > 0 and users.check_permission_bool(session, users.CHANGE_TEST):
        items.append(jqm_listitem_link("#test", _("Test Animal", l), "test", len(test)))
    if len(med) > 0 and users.check_permission_bool(session, users.CHANGE_MEDICAL):
        items.append(jqm_listitem_link("#med", _("Medicate Animal", l), "medical", len(med)))
    if osa and users.check_permission_bool(session, users.ADD_LOG):
        items.append(jqm_listitem_link("#log", _("Add Log to Animal", l), "log", -1, "dialog"))
    items.append(jqm_list_divider(_("Diary", l)))
    items.append(jqm_listitem_link("#diaryadd", _("New Task", l), "diary"))
    if len(dia) > 0 and users.check_permission_bool(session, users.EDIT_MY_DIARY_NOTES):
        items.append(jqm_listitem_link("#diary", _("Complete Tasks", l), "diary", len(dia)))
    items.append(jqm_list_divider(_("Person", l)))
    if len(hck) > 0 and users.check_permission_bool(session, users.CHANGE_PERSON):
        items.append(jqm_listitem_link("#homecheck", _("Perform Homecheck", l), "person", -1, "dialog"))
    h.append(jqm_list("\n".join(items)))
    h.append(jqm_page_footer())

    h += page_messages(l, homelink, mess)
    h += page_message_add(l, homelink, dbo)
    h += page_reports(l, homelink, ar)
    h += page_vaccinations(l, homelink, vacc)
    h += page_tests(l, homelink, test, testresults)
    h += page_medication(l, homelink, med)
    h += page_log_add(l, homelink, dbo)
    h += page_diary_add(l, homelink, dbo)
    h += page_diary(l, homelink, dia)
    h += page_homecheck(l, homelink, dbo)

    h.append("</body></html>")
    return "\n".join(h)

def page_messages(l, homelink, mess):
    h = []
    h.append(jqm_page_header("messages", _("Messages", l), homelink))
    h.append(jqm_list(jqm_link("#addmessage", _("Add Message", l), "message_new")))
    hm = []
    for m in mess:
        icon = "info"
        if m["PRIORITY"] == 1:
            icon = "alert"
        inner = jqm_h3(python2display(l, m["ADDED"]) + " " + m["CREATEDBY"])
        inner += jqm_p(m["MESSAGE"])
        hm.append(jqm_collapsible(inner, icon))
    h.append(jqm_collapsible_set("\n".join(hm)))
    h.append(jqm_page_footer())
    return h

def page_message_add(l, homelink, dbo):
    h = []
    h.append(jqm_page_header("addmessage", _("Add Message", l), homelink))
    h.append(jqm_form("messageform"))
    h.append(jqm_hidden("posttype", "message"))
    h.append(jqm_fieldcontain("forname", _("For", l), jqm_select("forname", html.options_users_and_roles(dbo, False, True))))
    h.append(jqm_fieldcontain("expires", _("Expires", l), jqm_options_next_month(l)))
    h.append(jqm_fieldcontain("priority", _("Priority", l), jqm_option("0", _("Information", l), True) + jqm_option("1", _("Important", l), False)))
    h.append(jqm_fieldcontain("email", _("Send via email", l), jqm_checkbox("email", configuration.email_messages(dbo))))
    h.append(jqm_fieldcontain("message", _("Note", l), jqm_text("message")))
    h.append(jqm_submit(_("Add Message", l)))
    h.append(jqm_form_end())
    h.append(jqm_page_footer())
    return h

def page_reports(l, homelink, ar):
    h = []
    h.append(jqm_page_header("reports", _("Reports", l), homelink))
    rs = []
    group = ""
    for r in ar:
        if group != r["CATEGORY"]:
            group = r["CATEGORY"]
            rs.append(jqm_list_divider(group))
        rs.append(jqm_listitem_link("mobile_report?id=%d" % r["ID"], r["TITLE"], "report"))
    h.append(jqm_list("\n".join(rs), True))
    h.append(jqm_page_footer())
    return h

def page_vaccinations(l, homelink, vacc):
    h = []
    h.append(jqm_page_header("vacc", _("Vaccinate", l), homelink))
    group = ""
    vlist = []
    vforms = []
    for v in vacc:
        required = python2display(l, v["DATEREQUIRED"])
        if group != required:
            group = required
            vlist.append(jqm_list_divider(group))
        pageid = "v" + str(v["ID"])
        vlist.append(jqm_listitem_link("#" + pageid, 
            "%s - %s (%s)" % (v["ANIMALNAME"], v["SHELTERCODE"], v["VACCINATIONTYPE"]),
            "vaccination", -1, "dialog"))
        vforms.append(jqm_page_header(pageid, v["VACCINATIONTYPE"], homelink))
        vforms.append(jqm_table())
        vforms.append(jqm_tablerow( _("Animal", l), 
            jqm_link("mobile_post?posttype=va&id=%d" % v["ANIMALID"], v["SHELTERCODE"] + " " + v["ANIMALNAME"])))
        vforms.append(jqm_tablerow( _("Vaccination", l), required + " " + v["VACCINATIONTYPE"]))
        vforms.append(jqm_tablerow( _("Comments", l), v["COMMENTS"]))
        vforms.append(jqm_table_end())
        vforms.append(jqm_button("mobile_post?posttype=vacc&id=%s&animalid=%s" % (str(v["ID"]), str(v["ANIMALID"])), _("Vaccinate", l), "check"))
        vforms.append(jqm_page_footer())
    h.append(jqm_list("\n".join(vlist), True))
    h.append(jqm_page_footer())
    h.append("\n".join(vforms))
    return h

def page_tests(l, homelink, test, testresults):
    h = []
    h.append(jqm_page_header("test", _("Test", l), homelink))
    group = ""
    tlist = []
    tforms = []
    for t in test:
        required = python2display(l, t["DATEREQUIRED"])
        if group != required:
            group = required
            tlist.append(jqm_list_divider(group))
        pageid = "t" + str(t["ID"])
        tlist.append(jqm_listitem_link("#" + pageid, 
            "%s - %s (%s)" % (t["ANIMALNAME"], t["SHELTERCODE"], t["TESTNAME"]),
            "vaccination", -1, "dialog"))
        tforms.append(jqm_page_header(pageid, t["TESTNAME"], homelink))
        tforms.append(jqm_table())
        tforms.append(jqm_tablerow( _("Animal", l), 
            jqm_link("mobile_post?posttype=va&id=%d" % t["ANIMALID"], t["SHELTERCODE"] + " " + t["ANIMALNAME"])))
        tforms.append(jqm_tablerow( _("Test", l), required + " " + t["TESTNAME"]))
        tforms.append(jqm_tablerow( _("Comments", l), t["COMMENTS"]))
        tforms.append(jqm_table_end())
        tforms.append(jqm_p(_("Result", l) + ": " + 
            "<select class=\"testresult\" data=\"%s\" data-animal=\"%s\">" % (str(t["ID"]), t["ANIMALID"]) +
            "<option value=""></option>" + 
            jqm_options_testresults(testresults) + "</select>"))
        tforms.append(jqm_page_footer())
    h.append(jqm_list("\n".join(tlist), True))
    h.append(jqm_page_footer())
    h.append("\n".join(tforms))
    return h

def page_medication(l, homelink, med):
    h = []
    h.append(jqm_page_header("med", _("Medicate", l), homelink))
    group = ""
    mlist = []
    mforms = []
    for m in med:
        required = python2display(l, m["DATEREQUIRED"])
        if group != required:
            group = required
            mlist.append(jqm_list_divider(group))
        pageid = "m" + str(m["TREATMENTID"])
        mlist.append(jqm_listitem_link("#" + pageid,
            "%s - %s (%s)" % (m["ANIMALNAME"], m["SHELTERCODE"], m["TREATMENTNAME"]),
            "medical", -1, "dialog"))
        mforms.append(jqm_page_header(pageid, m["TREATMENTNAME"], homelink))
        mforms.append(jqm_table());
        mforms.append(jqm_tablerow(_("Animal", l),
            jqm_link("mobile_post?posttype=va&id=%d" % m["ANIMALID"], m["SHELTERCODE"] + " " + m["ANIMALNAME"])))
        mforms.append(jqm_tablerow(_("Treatment", l), "%s %s<br />%s" % (required, m["TREATMENTNAME"], m["DOSAGE"])))
        mforms.append(jqm_tablerow(_("Comments", l), m["COMMENTS"]))
        mforms.append(jqm_table_end())
        mforms.append(jqm_button("mobile_post?posttype=med&id=%s&animalid=%s&medicalid=%s" % 
            (str(m["TREATMENTID"]), str(m["ANIMALID"]), str(m["REGIMENID"])), _("Medicate", l), "check"))
        mforms.append(jqm_page_footer())
    h.append(jqm_list("\n".join(mlist), True))
    h.append(jqm_page_footer())
    h.append("\n".join(mforms))
    return h

def page_diary(l, homelink, dia):
    h = []
    h.append(jqm_page_header("diary", _("Diary", l), homelink))
    group = ""
    dlist = []
    dforms = []
    for d in dia:
        fordate = python2display(l, d["DIARYDATETIME"])
        if group != fordate:
            group = fordate
            dlist.append(jqm_list_divider(group))
        pageid = "d" + str(d["ID"])
        dlist.append(jqm_listitem_link("#" + pageid,
            "%s (%s)" % (d["SUBJECT"], d["LINKINFO"]),
            "diary", -1, "dialog"))
        dforms.append(jqm_page_header(pageid, d["SUBJECT"], homelink))
        dforms.append(jqm_table());
        dforms.append(jqm_tablerow(_("Subject", l), d["SUBJECT"]))
        lt = d["LINKINFO"]
        if d["LINKTYPE"] == diary.ANIMAL:
            lt = jqm_link("mobile_post?posttype=va&id=%d" % d["LINKID"], d["LINKINFO"])
        dforms.append(jqm_tablerow(_("Link", l), lt))
        dforms.append(jqm_tablerow(_("Note", l), d["NOTE"]))
        dforms.append(jqm_table_end())
        dforms.append(jqm_button("mobile_post?posttype=dia&on=0&id=%s" % str(d["ID"]), _("Complete", l), "check"))
        dforms.append(jqm_p(_("Or move this diary on to", l) + ": " + 
            "<select class=\"diaryon\" data=\"%s\">" % str(d["ID"]) +
            jqm_options_next_month(l) + "</select>"))
        dforms.append(jqm_page_footer())
    h.append(jqm_list("\n".join(dlist), True))
    h.append(jqm_page_footer())
    h.append("\n".join(dforms))
    return h

def page_diary_add(l, homelink, dbo):
    h = []
    h.append(jqm_page_header("diaryadd", _("Add Diary", l), homelink))
    h.append(jqm_form("diaryform"))
    h.append(jqm_hidden("posttype", "dianew"))
    h.append(jqm_fieldcontain("diaryfor", _("For", l), jqm_select("diaryfor", html.options_users_and_roles(dbo))))
    h.append(jqm_fieldcontain("diarydate", _("Date", l), jqm_select("diarydate", jqm_options_next_month(l))))
    h.append(jqm_fieldcontain("subject", _("Subject", l), jqm_text("subject")))
    h.append(jqm_fieldcontain("note", _("Note", l), jqm_text("note")))
    h.append(jqm_submit(_("Add Diary", l)))
    h.append(jqm_form_end())
    h.append(jqm_page_footer())
    return h

def page_log_add(l, homelink, dbo):
    h = []
    h.append(jqm_page_header("log", _("Add Log", l), homelink))
    h.append(jqm_form("logform"))
    h.append(jqm_hidden("posttype", "log"))
    h.append(jqm_fieldcontain("animalid", _("Animal", l), jqm_select("animalid", html.options_animals_on_shelter(dbo))))
    h.append(jqm_fieldcontain("logtypeid", _("Log Type", l), jqm_select("logtypeid", html.options_log_types(dbo))))
    h.append(jqm_fieldcontain("logtext", _("Log Text", l), jqm_text("logtext")))
    h.append(jqm_submit(_("Add Log", l)))
    h.append(jqm_form_end())
    h.append(jqm_page_footer())
    return h

def page_homecheck(l, homelink, dbo):
    h = []
    h.append(jqm_page_header("homecheck", _("Perform Homecheck", l), homelink))
    h.append(jqm_form("hcform"))
    h.append(jqm_hidden("posttype", "hc"))
    h.append(jqm_fieldcontain("personid", _("Person", l), jqm_select("personid", html.options_people_not_homechecked(dbo))))
    h.append(jqm_fieldcontain("comments", _("Comments", l), jqm_text("comments")))
    h.append(jqm_submit(_("Pass Homecheck", l)))
    h.append(jqm_form_end())
    h.append(jqm_page_footer())
    return h

def page_login(l):
    accountline = ""
    accounttext = _("Database", l)
    if smcom.active(): accounttext = _("SM Account", l)
    if MULTIPLE_DATABASES:
        accountline = "<div data-role='fieldcontain'><label for='database'>%s</label><input type='text' id='database' name='database' /></div>" % accounttext
    return header(l) + """
        <div data-role='page' id='login'>
        <div data-role='header'>
        <h1>%s</h1>
        </div>
        <div data-role='content'>
        <form id="loginform" action="mobile_login" target="_self" method="post">
        <h2>%s</h2>
        %s
        <div data-role="fieldcontain">
            <label for="username">%s</label>
            <input type="text" id="username" name="username" />
        </div>
        <div data-role="fieldcontain">
            <label for="password">%s</label>
            <input type="password" id="password" name="password" />
        </div>
        <button type="submit">%s</button>
        </form>
        </div>
        </div>
        </body>
        </html>
    """ % ( _("Login", l), _("Login", l), accountline, _("Username", l), _("Password", l), _("Login", l) )

def handler(dbo, user, post):
    """
    Handles posts from the frontend. Depending on the type we either
    return more HTML for the javascript to inject, or GO URL to have
    the controller redirect to URL
    """
    l = dbo.locale
    homelink = "<a href='mobile' class='ui-btn-right' data-icon='home' data-theme='b'>%s</a>" % _("Home", l)
    mode = post["posttype"]
    pid = post.integer("id")
    animalid = post.integer("animalid")

    if mode == "vacc":
        # We're vaccinating an animal
        a = animal.get_animal(dbo, animalid)
        medical.update_vaccination_today(dbo, user, pid)
        return jqm_page_header("", _("Vaccination Given", l), homelink) + \
            jqm_p(_("Vaccination marked as given for {0} - {1}", l).format(a["ANIMALNAME"], a["SHELTERCODE"])) + \
            jqm_button("mobile#vacc", _("More Vaccinations", l), "", "false") + \
            jqm_page_footer()

    if mode == "test":
        # We're performing a test on an animal
        a = animal.get_animal(dbo, animalid)
        medical.update_test_today(dbo, user, pid, post.integer("resultid"))
        return jqm_page_header("", _("Test Performed", l), homelink) + \
            jqm_p(_("Test marked as performed for {0} - {1}", l).format(a["ANIMALNAME"], a["SHELTERCODE"])) + \
            jqm_button("mobile#test", _("More Tests", l), "", "false") + \
            jqm_page_footer()

    elif mode == "med":
        # We're treating an animal
        a = animal.get_animal(dbo, animalid)
        medical.update_treatment_today(dbo, user, pid)
        return jqm_page_header("", _("Treatment Given", l), homelink) + \
            jqm_p(_("Treatment marked as given for {0} - {1}", l).format(a["ANIMALNAME"], a["SHELTERCODE"])) + \
            jqm_button("mobile#med", _("More Medications", l), "", "false") + \
            jqm_page_footer()

    elif mode == "dia":
        # We're completing a diary task
        d = diary.get_diary(dbo, pid)
        if post["on"] == "0":
            diary.complete_diary_note(dbo, user, pid)
            return jqm_page_header("", _("Completed", l), homelink) + \
                jqm_p(_("Diary note {0} marked completed", l).format(d["SUBJECT"])) + \
                jqm_button("mobile#diary", _("More diary notes", l), "", "false") + \
                jqm_page_footer()
        else:
            diary.rediarise_diary_note(dbo, user, pid, post.date("on"))
            return jqm_page_header("", _("Rediarised", l), homelink) + \
                jqm_p(_("Diary note {0} rediarised for {1}", l).format(d["SUBJECT"], post["on"])) + \
                jqm_button("mobile#diary", _("More diary notes", l), "", "false") + \
                jqm_page_footer()

    elif mode == "dianew":
        # We're adding a diary note
        diary.insert_diary(dbo, user, 0, 0, post.date("diarydate"), 
            post["diaryfor"], post["subject"], post["note"])
        return "GO mobile"

    elif mode == "message":
        # We're adding a message
        lookups.add_message(dbo, user, post.boolean("email"), post["message"], post["forname"], post.integer("priority"), post.date("expires"))
        return "GO mobile"

    elif mode == "log":
        # We're adding a log to an animal
        a = animal.get_animal(dbo, animalid)
        log.add_log(dbo, user, log.ANIMAL, animalid, post.integer("logtypeid"), post["logtext"])
        return "GO mobile"

    elif mode == "hc":
        # We're marking an owner homechecked
        person.update_pass_homecheck(dbo, user, post.integer("personid"), post["comments"])
        return "GO mobile"

    elif mode == "vsa":
        # Return a list of the shelter animals
        h = []
        alin = []
        h.append(header(l))
        h.append(jqm_page_header("", _("Shelter Animals", l), homelink))
        an = animal.get_animal_find_simple(dbo, "", "all")
        for a in an:
            alin.append(jqm_listitem_link("mobile_post?posttype=va&id=%d" % a["ID"],
                "%s - %s (%s %s %s) %s" % (a["CODE"], a["ANIMALNAME"], a["SEXNAME"], a["BREEDNAME"], a["SPECIESNAME"], a["IDENTICHIPNUMBER"]),
                "animal"))
        h.append(jqm_list("\n".join(alin), True))
        h.append(jqm_page_footer())
        h.append("</body></html>")
        return "\n".join(h)

    elif mode == "uai":
        # Upload an animal image
        media.attach_file_from_form(dbo, user, media.ANIMAL, animalid, post.data)
        return "GO mobile_post?posttype=va&id=%d&success=true" % animalid

    elif mode == "va":
        # Display a page containing the selected animal by id
        a = animal.get_animal(dbo, pid)
        af = additional.get_additional_fields(dbo, pid, "animal")
        return handler_viewanimal(l, a, af, homelink, post)

def handler_viewanimal(l, a, af, homelink, post):
    """
    Generate the view animal mobile page.
    l:  The locale
    a:  An animal record
    af: Additional fields for the animal record
    homelink: Link to the home menu
    post: The posted values
    """
    def table():
        return "<table style='width: 100%; border-bottom: 1px solid black;'>"
    def table_end():
        return "</table>"
    def tr(label, value, value2 = ""):
        if value is None or str(value).startswith("None "): value = ""
        if value2 is None or str(value2).startswith("None"): value2 = ""
        if value2 is not None and value2 != "": value2 = "<td>%s</td>" % value2
        return "<tr><td style='font-weight: bold; width: 150px'>%s</td><td>%s</td>%s</tr>" % (label, value, value2)
    h = []
    h.append(header(l))
    h.append(jqm_page_header("", "%s - %s" % (a["CODE"], a["ANIMALNAME"]), homelink))
    h.append(table())
    h.append("<td><img src='%s' class='asm-thumbnail' /></td>" % html.thumbnail_img_src(a, "animalthumb"))
    h.append("<td><h2 style='margin: 2px;'>%s - %s</h2>" % (a["CODE"], a["ANIMALNAME"]))
    h.append("%s %s %s</td>" % (a["SEXNAME"], a["BREEDNAME"], a["SPECIESNAME"]))
    h.append("</tr></table>")
    h.append(table())
    uploadstatus = ""
    if post["success"] == "true":
        uploadstatus = _("Photo successfully uploaded.", l)
    h.append("""
        <tr><td style='font-weight: bold; width: 150px;'>%s</td>
        <td>
        <form data-ajax="false" action="mobile_post" method="post" enctype="multipart/form-data">
        <input type="hidden" name="animalid" value="%d" />
        <input type="hidden" name="posttype" value="uai" />
        <input type="hidden" name="comments" value="" />
        <input type="hidden" name="base64image" value="" />
        <input type="file" data-role='none' name="filechooser" id="fc%d" />
        <span class=".tipios6" style="display: none">%s</span>
        <input id='sfc%d' type='submit' data-icon='arrow-u' data-inline='true' data-mini='true' value='%s' />
        </form>
        <span class="tip">%s</span>
        </td></tr>""" % (_("Upload Photo", l), a["ID"], a["ID"], 
                        _("You will need to upgrade to iOS 6 or higher to upload files.", l),
                         a["ID"], _("Send", l), uploadstatus))
    h.append(table())
    h.append(tr( _("Type", l), a["ANIMALTYPENAME"]))
    h.append(tr( _("Location", l), a["DISPLAYLOCATIONNAME"]))
    h.append(tr( _("Color", l), a["BASECOLOURNAME"]))
    h.append(tr( _("Coat Type", l), a["COATTYPENAME"]))
    h.append(tr( _("Size", l), a["SIZENAME"]))
    h.append(tr( _("DOB", l), python2display(l, a["DATEOFBIRTH"]), a["ANIMALAGE"]))
    h.append(table_end())
    h.append(table())
    h.append(tr( _("Markings", l), a["MARKINGS"]))
    h.append(tr( _("Hidden Comments", l), a["HIDDENANIMALDETAILS"]))
    h.append(tr( _("Comments", l), a["ANIMALCOMMENTS"]))
    h.append(table_end())
    h.append(table())
    h.append(tr( _("Cats", l), a["ISGOODWITHCATSNAME"]))
    h.append(tr( _("Dogs", l), a["ISGOODWITHDOGSNAME"]))
    h.append(tr( _("Children", l), a["ISGOODWITHCHILDRENNAME"]))
    h.append(tr( _("Housetrained", l), a["ISHOUSETRAINEDNAME"]))
    h.append(table_end())
    h.append(table())
    h.append(tr( _("Original Owner", l), a["ORIGINALOWNERNAME"]))
    h.append(tr( _("Brought In By", l), a["BROUGHTINBYOWNERNAME"]))
    h.append(tr( _("Date Brought In", l), python2display(l, a["DATEBROUGHTIN"])))
    h.append(tr( _("Bonded With", l), "%s %s %s %s" % (a["BONDEDANIMAL1CODE"], a["BONDEDANIMAL1NAME"], a["BONDEDANIMAL2CODE"], a["BONDEDANIMAL2NAME"])))
    h.append(tr( _("Transfer?", l), a["ISTRANSFERNAME"] == 1))
    h.append(tr( _("Entry Category", l), a["ENTRYREASONNAME"]))
    h.append(tr( _("Entry Reason", l), a["REASONFORENTRY"]))
    h.append(table_end())
    h.append(table())
    h.append(tr( _("Microchipped", l), python2display(l, a["IDENTICHIPDATE"]), a["IDENTICHIPNUMBER"]))
    h.append(tr( _("Tattoo", l), python2display(l, a["TATTOODATE"]), a["TATTOONUMBER"]))
    h.append(tr( _("Neutered", l), python2display(l, a["NEUTEREDDATE"])))
    h.append(tr( _("Declawed", l), a["DECLAWEDNAME"]))
    h.append(tr( _("Heartworm Tested", l), python2display(l, a["HEARTWORMTESTDATE"]), a["HEARTWORMTESTRESULTNAME"]))
    h.append(tr( _("FIV/L Tested", l), python2display(l, a["COMBITESTDATE"]), "%s %s" % (a["COMBITESTRESULTNAME"], a["FLVRESULTNAME"])))
    h.append(tr( _("Health Problems", l), a["HEALTHPROBLEMS"]))
    h.append(tr( _("Rabies Tag", l), a["RABIESTAG"]))
    h.append(tr( _("Special Needs", l), a["HASSPECIALNEEDSNAME"]))
    h.append(tr( _("Current Vet", l), a["CURRENTVETNAME"], a["CURRENTVETWORKTELEPHONE"]))
    h.append(table_end())
    if len(af) > 0:
        h.append(table())
        for d in af:
            h.append(tr(d["FIELDLABEL"], d["VALUE"]))
        h.append(table_end())
    h.append("""
    <script type="text/javascript">
        // If this is an idevice and the file upload box is
        // disabled, it needs upgrading to iOS6 or better.
        if (is_idevice && $("#fc%d").attr("disabled")) {
            $(".tipios6").show();
        }
    </script>
    """ % ( a["ID"] ))
    h.append(jqm_page_footer())
    h.append("</body></html>")
    return "\n".join(h)

def login(post, session, remoteip, path):
    """
    Handles the login post
    """
    url = users.web_login(post, session, remoteip, path)
    if url == "FAIL" or url == "DISABLED":
        return "mobile_login"
    else:
        return "mobile"

def report(dbo, crid, user):
    """
    Generates a report for mobile devices. 
    crid: The custom report id
    user: The username of the user running the report
    """
    return reports.execute(dbo, crid, user)


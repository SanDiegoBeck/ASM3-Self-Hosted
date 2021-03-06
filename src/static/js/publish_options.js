/*jslint browser: true, forin: true, eqeq: true, white: true, sloppy: true, vars: true, nomen: true */
/*global $, jQuery, _, asm, common, config, controller, dlgfx, format, header, html, validate */

$(function() {

    var publish_options = {

        render_tabs: function() {
            return [
                '<ul>',
                '<li><a href="#tab-animalselection">' + _("Animal Selection") + '</a></li>',
                '<li><a href="#tab-allpublishers">' + _("All Publishers") + '</a></li>',
                '<li class="localegb"><a href="#tab-avid">AVID/PETtrac Microchips</a></li>',
                '<li class="localeus"><a href="#tab-petlink">PetLink Microchips</a></li>',
                '<li class="facebook"><a href="#tab-facebook">' + _("Facebook Sharing") + '</a></li>',
                '<li><a href="#tab-htmlftp">' + _("HTML/FTP Publisher") + '</a></li>',
                '<li class="localeus localeca"><a href="#tab-petfinder">PetFinder Publisher</a></li>',
                '<li class="localeus localeca"><a href="#tab-rescuegroups">RescueGroups Publisher</a></li>',
                '<li class="localeus"><a href="#tab-adoptapet">AdoptAPet Publisher</a></li>',
                '<li class="localeus localeca"><a href="#tab-meetapet">MeetAPet Publisher</a></li>',
                '<li><a href="#tab-helpinglostpets">HelpingLostPets.com Publisher</a></li>',
                '<li class="localeus"><a href="#tab-smarttag">SmartTag Updater</a></li>',
                '</ul>'
            ].join("\n");
        },

        render_animalselection: function() {
            return [
                '<div id="tab-animalselection">',
                '<table>',
                '<tr>',
                '<td><label for="caseanimals">' + _("Include cruelty case animals") + '</label></td>',
                '<td><select id="caseanimals" class="asm-selectbox pbool preset" data="includecase">',
                '<option value="0">' + _("No") + '</option>',
                '<option value="1">' + _("Yes") + '</option>',
                '</select></td>',
                '</tr>',
                '<tr>',
                '<td><label for="reservedanimals">' + _("Include reserved animals") + '</label></td>',
                '<td><select id="reservedanimals" class="asm-selectbox pbool preset" data="includereserved">',
                '<option value="0">' + _("No") + '</option>',
                '<option value="1">' + _("Yes") + '</option>',
                '</select></td>',
                '</tr>',
                '<tr>',
                '<td><label for="retaileranimals">' + _("Include retailer animals") + '</label></td>',
                '<td><select id="retaileranimals" class="asm-selectbox pbool preset" data="includeretailer">',
                '<option value="0">' + _("No") + '</option>',
                '<option value="1">' + _("Yes") + '</option>',
                '</select></td>',
                '</tr>',
                '<tr>',
                '<td><label for="fosteredanimals">' + _("Include fostered animals") + '</label></td>',
                '<td><select id="fosteredanimals" class="asm-selectbox pbool preset" data="includefosters">',
                '<option value="0">' + _("No") + '</option>',
                '<option value="1">' + _("Yes") + '</option>',
                '</select></td>',
                '</tr>',
                '<tr>',
                '<td><label for="heldanimals">' + _("Include held animals") + '</label></td>',
                '<td><select id="heldanimals" class="asm-selectbox pbool preset" data="includehold">',
                '<option value="0">' + _("No") + '</option>',
                '<option value="1">' + _("Yes") + '</option>',
                '</select></td>',
                '</tr>',
                '<tr>',
                '<td><label for="quarantinedanimals">' + _("Include quarantined animals") + '</label></td>',
                '<td><select id="quarantinedanimals" class="asm-selectbox pbool preset" data="includequarantine">',
                '<option value="0">' + _("No") + '</option>',
                '<option value="1">' + _("Yes") + '</option>',
                '</select></td>',
                '</tr>',
                '<tr>',
                '<td><label for="noimage">' + _("Include animals who don\'t have a picture") + '</label></td>',
                '<td><select id="noimage" class="asm-selectbox pbool preset" data="includewithoutimage">',
                '<option value="0">' + _("No") + '</option>',
                '<option value="1">' + _("Yes") + '</option>',
                '</select></td>',
                '</tr>',
                '<tr>',
                '<td><label for="bonded">' + _("Merge bonded animals into a single record") + '</label></td>',
                '<td><select id="bonded" class="asm-selectbox pbool preset" data="bondedassingle">',
                '<option value="0">' + _("No") + '</option>',
                '<option value="1">' + _("Yes") + '</option>',
                '</select></td>',
                '</tr>',
                '<tr>',
                '<td><label for="excludeunder">' + _("Exclude animals who are aged under") + '</label></td>',
                '<td><select id="excludeunder" class="asm-selectbox preset" data="excludeunder">',
                '<option value="1">' + _("1 week") + '</option>',
                '<option value="2">' + _("2 weeks") + '</option>',
                '<option value="4">' + _("4 weeks") + '</option>',
                '<option value="8">' + _("8 weeks") + '</option>',
                '<option value="12">' + _("3 months") + '</option>',
                '<option value="26">' + _("6 months") + '</option>',
                '<option value="38">' + _("9 months") + '</option>',
                '<option value="52">' + _("1 year") + '</option>',
                '</select></td>',
                '</tr>',
                '<tr>',
                '<td><label for="locations">' + _("Include animals in the following locations") + '</label></td>',
                '<td><select id="locations" class="asm-bsmselect preset" multiple="multiple" data="includelocations">',
                html.list_to_options(controller.locations, "ID", "LOCATIONNAME"),
                '</select></td>',
                '</tr>',
                '<tr>',
                '<td></td>',
                '<td>',
                '<div class="ui-state-highlight ui-corner-all" style="padding: 0 .7em;">',
                '<p><span class="ui-icon ui-icon-info" style="float: left; margin-right: .3em;"></span>',
                _("If you don\'t select any locations, publishers will include animals in all locations."),
                '</p>',
                '</div>',
                '</td>',
                '</tr>',
                '</table>',
                '</div>'
            ].join("\n");
        },

        render_allpublishers: function() {
            return [
                '<div id="tab-allpublishers">',
                '<table>',
                '<tr>',
                '<td><label for="limit">' + _("Only publish a set number of animals") + '</label></td>',
                '<td><input id="limit" type="text" class="asm-textbox asm-numberbox preset" data="limit" value="0" />',
                '<div class="ui-state-highlight ui-corner-all" style="padding: 0 .7em; float: right;">',
                '<p><span class="ui-icon ui-icon-info" style="float: left; margin-right: .3em;"></span>',
                _("Set to 0 for no limit."),
                '</p>',
                '</div>',
                '</td>',
                '</tr>',
                '<tr>',
                '<td><label for="forcereupload">' + _("Reupload animal images every time") + '</label></td>',
                '<td><select id="forcereupload" class="asm-selectbox pbool preset" data="forcereupload">',
                '<option value="0">' + _("No") + '</option>',
                '<option value="1">' + _("Yes") + '</option>',
                '</select></td>',
                '</tr>',
                '<tr>',
                '<td><label for="uploadall">' + _("Upload all available images for animals") + '</label></td>',
                '<td><select id="uploadall" class="asm-selectbox pbool preset" data="uploadall">',
                '<option value="0">' + _("No") + '</option>',
                '<option value="1">' + _("Yes") + '</option>',
                '</select></td>',
                '</tr>',
                '<tr>',
                '<td><label for="usecomments">' + _("Use animal comments if photo notes are blank") + '</label></td>',
                '<td><select id="usecomments" class="asm-selectbox cfg" data="PublisherUseCommentsForBlankNotes">',
                '<option value="No">' + _("No") + '</option>',
                '<option value="Yes">' + _("Yes") + '</option>',
                '</select></td>',
                '</tr>',
                '',
                '<tr>',
                '<td><label for="order">' + _("Order published animals by") + '</label></td>',
                '<td><select id="order" class="asm-selectbox preset" data="order">',
                '<option value="0">' + _("Entered (oldest first)") + '</option>',
                '<option value="1">' + _("Entered (newest first)") + '</option>',
                '<option value="2">' + _("Animal Name") + '</option>',
                '</select></td>',
                '</tr>',
                '<tr>',
                '<td><label for="tppublishersig">' + _("Add this text to all animal descriptions") + '</label></td>',
                '<td><textarea id="tppublishersig" type="text" rows="5" class="asm-textarea cfg" data="TPPublisherSig"',
                'title="' + html.title(_("When publishing to third party services, add this extra text to the bottom of all animal descriptions")) + '"></textarea></td>',
                '</tr>',
                '</table>',
                '</div>'
            ].join("\n");
        },

        render_avid: function() {
            return [
                '<div id="tab-avid">',
                '<div class="ui-state-highlight ui-corner-all" style="padding: 0 .7em">',
                '<p><span class="ui-icon ui-icon-info" style="float: left; margin-right: .3em;"></span>',
                'These settings are for uploading new owner information to the AVID PETtrac microchip database. This information is prompted for staff to send during the adoption workflow.',
                '</p>',
                '</div>',
                '<table>',
                '<tr>',
                '<td><label for="avidorgname">Organisation Name</label></td>',
                '<td><input data="AvidOrgName" id="avidorgname" type="text" class="asm-doubletextbox cfg" /></td>',
                '</tr>',
                '<tr>',
                '<td><label for="avidorgserial">Serial Number</label></td>',
                '<td><input data="AvidOrgSerial" id="avidorgserial" type="text" class="asm-doubletextbox cfg" /></td>',
                '</tr>',
                '<tr>',
                '<td><label for="avidorgpostcode">Postcode</label></td>',
                '<td><input data="AvidOrgPostcode" id="avidorgpostcode" type="text" class="asm-doubletextbox cfg" /></td>',
                '</tr>',
                '<tr>',
                '<td><label for="avidorgpassword">Password</label></td>',
                '<td><input data="AvidOrgPassword" id="avidorgpassword" type="text" class="asm-doubletextbox cfg" /></td>',
                '</tr>',
                '</table>',
                '</div>'
            ].join("\n");
        },

        render_petlink: function() {
            return [
                '<div id="tab-petlink">',
                '<p><input id="enabledpl" type="checkbox" class="asm-checkbox enablecheck" /><label for="enabledpl">' + _("Enabled") + '</label></p>',
                '<div class="ui-state-highlight ui-corner-all" style="padding: 0 .7em;">',
                '<p><span class="ui-icon ui-icon-info" style="float: left; margin-right: .3em;">',
                '</span>',
                'These settings are for uploading new owner information to the PetLink/DataMARS microchip database.',
                'The default PetLink Base URL is "www.petlink.net/us/".',
                '</p>',
                '</div>',
                '<table>',
                '<tr>',
                '<td><label for="plemail">Login Email</label></td>',
                '<td><input id="plemail" type="text" class="asm-textbox cfg" data="PetLinkEmail" /></td>',
                '</tr>',
                '<tr>',
                '<td><label for="plpass">Password</label></td>',
                '<td><input id="plpass" type="text" class="asm-textbox cfg" data="PetLinkPassword" /></td>',
                '</tr>',
                '<tr>',
                '<td><label for="plchippass">Chip Password</label></td>',
                '<td><input id="plchippass" type="text" class="asm-textbox cfg" data="PetLinkChipPassword" /></td>',
                '</tr>',
                '<tr>',
                '<td></td>',
                '<td>',
                '<div class="ui-state-highlight ui-corner-all" style="padding: 0 .7em;">',
                '<p><span class="ui-icon ui-icon-info" style="float: left; margin-right: .3em;">',
                '</span>',
                'The chip password is the password that allows owners to update their own information on the PetLink',
                'website in combination with their email address.',
                '</p>',
                '</div>',
                '</td>',
                '</tr>',
                '<tr>',
                '<td><label for="plbaseurl">PetLink Base URL</label></td>',
                '<td><input id="plbaseurl" type="text" class="asm-textbox cfg" data="PetLinkBaseURL" /></td>',
                '</tr>',
                '</table>',
                '</div>'
            ].join("\n");
        },

        render_facebook: function() {
            return [
                '<div id="tab-facebook">',
                '<p>',
                '<input id="enabledfb" type="checkbox" class="asm-checkbox cfg enablecheck" data="FacebookEnabled" /><label for="enablefb">' + _("Enable sharing animals via Facebook") + '</label>',
                '</p>',
                '<table>',
                '<tr>',
                '<td><label for="fbformat">' + _("Template for Facebook posts") + '</label></td>',
                '<td><textarea id="fbformat" type="text" rows="5" class="asm-textareafixeddouble cfg" data="FacebookTemplate"',
                'title="' + html.title(_("Include this information on animals shared via Facebook")) + '"></textarea></td>',
                '</tr>',
                '<tr>',
                '<td><label for="fbpostas">' + _("Post to Facebook as") + '</label></td>',
                '<td><select id="fbpostas" class="asm-selectbox cfg" data="FacebookPostAs">',
                '<option value="me">' + _("Logged in Facebook user") + '</option>',
                '<option value="page">' + _("Facebook page") + '</option>',
                '</select></td>',
                '</tr>',
                '<tr>',
                '<tr>',
                '<td><label for="fbpagename">' + _("Facebook page name") + '</label></td>',
                '<td><input id="fbpagename" class="asm-textbox cfg" data="FacebookPageName" title="' + html.title(_("The name of the page you want to post to (eg: Your Humane Society). Leave blank to post to your wall.")) + '" /></td>',
                '</tr>',
                '<tr>',
                '<td></td>',
                '<td>',
                '<input id="logonfb" type="checkbox" class="asm-checkbox cfg" data="FacebookLog" /><label for="logonfb">' + _("When posting an animal to Facebook, make a note of it in the log with this type") + '</label>',
                '<select data="FacebookLogType" id="facebooklogtype" class="asm-selectbox cfg">',
                html.list_to_options(controller.logtypes, "ID", "LOGTYPENAME"),
                '</select>',
                '</td>',
                '</tr>',
                '</table>',
                '</div>'
            ].join("\n");
        },

        render_htmlftp: function() {
            return [
                '<div id="tab-htmlftp">',
                '<p><input id="enabledhtml" type="checkbox" class="asm-checkbox enablecheck" /><label for="enabledhtml">' + _("Enabled") + '</label></p>',
                '<table>',
                '<tr>',
                '<td>',
                '<table>',
                '<tr>',
                '<td><label for="generatejavascript">' + _("Generate a javascript database for the search page") + '</label></td>',
                '<td><select id="generatejavascript" class="asm-selectbox pbool preset" data="generatejavascriptdb">',
                '<option value="0">' + _("No") + '</option>',
                '<option value="1">' + _("Yes") + '</option>',
                '</select></td>',
                '</tr>',
                '<tr>',
                '<td><label for="thumbnails">' + _("Generate image thumbnails as tn_$$IMAGE$$") + '</label></td>',
                '<td><select id="thumbnails" class="asm-selectbox pbool preset" data="thumbnails">',
                '<option value="0">' + _("No") + '</option>',
                '<option value="1">' + _("Yes") + '</option>',
                '</select></td>',
                '</tr>',
                '<tr>',
                '<td><label for="scale">' + _("Thumbnail size") + '</label></td>',
                '<td><select id="scale" class="asm-selectbox preset" data="thumbnailsize">',
                '<option value="70x70">70 px</option>',
                '<option value="80x80">80 px</option>',
                '<option value="90x90">90 px</option>',
                '<option value="100x100">100 px</option>',
                '<option value="120x120">120 px</option>',
                '<option value="150x150">150 px</option>',
                '</select></td>',
                '</tr>',
                '<tr>',
                '<td><label for="childadult">' + _("Split pages with a baby/adult prefix") + '</label></td>',
                '<td><select id="childadult" class="asm-selectbox pbool preset" data="htmlbychildadult">',
                '<option value="0">' + _("No") + '</option>',
                '<option value="1">' + _("Yes") + '</option>',
                '</select></td>',
                '</tr>',
                '<tr>',
                '<td><label for="childsplit">' + _("Split baby/adult age at") + '</label></td>',
                '<td><select id="childsplit" class="asm-selectbox preset" data="childadultsplit">',
                '<option value="1">' + _("1 week") + '</option>',
                '<option value="2">' + _("2 weeks") + '</option>',
                '<option value="4">' + _("4 weeks") + '</option>',
                '<option value="8">' + _("8 weeks") + '</option>',
                '<option value="12">' + _("3 months") + '</option>',
                '<option value="26">' + _("6 months") + '</option>',
                '<option value="38">' + _("9 months") + '</option>',
                '<option value="52">' + _("1 year") + '</option>',
                '</select></td>',
                '</tr>',
                '<tr>',
                '<td><label for="speciessplit">' + _("Split pages with a species name prefix") + '</label></td>',
                '<td><select id="speciessplit" class="asm-selectbox pbool preset" data="htmlbyspecies">',
                '<option value="0">' + _("No") + '</option>',
                '<option value="1">' + _("Yes") + '</option>',
                '</select></td>',
                '</tr>',
                '<tr>',
                '<td><label for="animalsperpage">' + _("Animals per page") + '</label></td>',
                '<td><select id="animalsperpage" class="asm-selectbox preset" data="animalsperpage">',
                '<option value="5">5</option>',
                '<option value="10" selected="selected">10</option>',
                '<option value="15">15</option>',
                '<option value="20">20</option>',
                '<option value="50">50</option>',
                '<option value="100">100</option>',
                '<option value="999999">Unlimited (one page)</option>',
                '</select></td>',
                '</tr>',
                '<tr>',
                '<td><label for="extension">' + _("Page extension") + '</label></td>',
                '<td><select id="extension" class="asm-selectbox preset" data="extension">',
                '<option value="html">html</option>',
                '<option value="xml">xml</option>',
                '<option value="cgi">cgi</option>',
                '<option value="php">php</option>',
                '<option value="py">py</option>',
                '<option value="rb">rb</option>',
                '<option value="jsp">jsp</option>',
                '<option value="asp">asp</option>',
                '<option value="aspx">aspx</option>',
                '</select></td>',
                '</tr>',
                '<tr>',
                '<td><label for="template">' + _("Publishing template") + '</label></td>',
                '<td><select id="template" class="asm-selectbox preset" data="style">',
                html.list_to_options(controller.styles),
                '</select></td>',
                '</tr>',
                '<tr>',
                '<td><label for="scale">' + _("Scale published animal images to") + '</label></td>',
                '<td><select id="scale" class="asm-selectbox preset" data="scaleimages">',
                '<option value="">' + _("Don\'t scale") + '</option>',
                '<option value="300x300">300 px</option>',
                '<option value="320x320">320 px</option>',
                '<option value="400x400">400 px</option>',
                '<option value="500x500">500 px</option>',
                '<option value="600x600">600 px</option>',
                '<option value="800x800">800 px</option>',
                '<option value="1024x1024">1024 px</option>',
                '</select></td>',
                '</tr>',
                '<tr id="publishdirrow">',
                '<td><label for="publishdir">' + _("Publish to folder") + '</label></td>',
                '<td><input id="publishdir" type="text" class="asm-textbox preset" data="publishdirectory" /></td>',
                '</tr>',
                '<tr id="publishdiroverride" style="display: none">',
                '<td>' + _("Publish to folder") + '</td>',
                '<td><a href="#"></a></td>',
                '</table>',
                '</td>',
                '<td>',
                '<table id="ftpuploadtable">',
                '<tr>',
                '<td><label for="uploaddirectly">' + _("Enable FTP uploading") + '</label></td>',
                '<td><select id="uploaddirectly" class="asm-selectbox pbool preset" data="uploaddirectly">',
                '<option value="0">' + _("No") + '</option>',
                '<option value="1">' + _("Yes") + '</option>',
                '</select></td>',
                '</tr>',
                '<tr>',
                '<td><label for="ftphost">' + _("FTP hostname") + '</label></td>',
                '<td><input id="ftphost" type="text" class="asm-textbox cfg" data="FTPURL" /></td>',
                '</tr>',
                '<tr>',
                '<td><label for="ftpuser">' + _("FTP username") + '</label></td>',
                '<td><input id="ftpuser" type="text" class="asm-textbox cfg" data="FTPUser" /></td>',
                '</tr>',
                '<tr>',
                '<td><label for="ftppass">' + _("FTP password") + '</label></td>',
                '<td><input id="ftppass" type="text" class="asm-textbox cfg" data="FTPPassword" /></td>',
                '</tr>',
                '<tr>',
                '<td><label for="ftproot">' + _("after connecting, chdir to") + '</label></td>',
                '<td><input id="ftproot" type="text" class="asm-textbox cfg" data="FTPRootDirectory" /></td>',
                '</tr>',
                '<tr>',
                '<td><label for="clearexisting">' + _("Remove previously published files before uploading") + '</label></td>',
                '<td><select id="clearexisting" class="asm-selectbox pbool preset" data="clearexisting">',
                '<option value="0">' + _("No") + '</option>',
                '<option value="1">' + _("Yes") + '</option>',
                '</select></td>',
                '</tr>',
                '</table>',
                '</td>',
                '</tr>',
                '</table>',
                '</div>'
            ].join("\n");
        },

        render_petfinder: function() {
            return [
                '<div id="tab-petfinder">',
                '<p><input id="enabledpf" type="checkbox" class="asm-checkbox enablecheck" /><label for="enabledpf">' + _("Enabled") + '</label></p>',
                '<div class="ui-state-highlight ui-corner-all" style="padding: 0 .7em;">',
                '<p><span class="ui-icon ui-icon-info" style="float: left; margin-right: .3em;">',
                '</span>',
                'The default PetFinder host is "members.petfinder.com".<br/>',
                'Make sure to notify the PetFinder helpdesk that you are using ASM to upload animals so that they can give you your FTP username and password.',
                '</p>',
                '</div>',
                '<table>',
                '<tr>',
                '<td><label for="pfftphost">PetFinder FTP host</label></td>',
                '<td><input id="pfftphost" type="text" class="asm-textbox cfg" data="PetFinderFTPURL" /></td>',
                '</tr>',
                '<tr>',
                '<td><label for="pfftpuser">PetFinder shelter ID</label></td>',
                '<td><input id="pfftpuser" type="text" class="asm-textbox cfg" data="PetFinderFTPUser" /></td>',
                '</tr>',
                '<tr>',
                '<td><label for="pfftppass">PetFinder FTP password</label></td>',
                '<td><input id="pfftppass" type="text" class="asm-textbox cfg" data="PetFinderFTPPassword" /></td>',
                '</tr>',
                '</table>',
                '</div>'
            ].join("\n");
        },

        render_rescuegroups: function() {
            return [
                '<div id="tab-rescuegroups">',
                '<p><input id="enabledrg" type="checkbox" class="asm-checkbox enablecheck" /><label for="enabledrg">' + _("Enabled") + '</label></p>',
                '<div class="ui-state-highlight ui-corner-all" style="padding: 0 .7em;">',
                '<p><span class="ui-icon ui-icon-info" style="float: left; margin-right: .3em;"></span>',
                'The default RescueGroups host is "ftp.rescuegroups.org".',
                '</p>',
                '</div>',
                '<table>',
                '<tr>',
                '<td><label for="rgtphost">RescueGroups FTP host</label></td>',
                '<td><input id="rgftphost" type="text" class="asm-textbox cfg" data="RescueGroupsFTPURL" /></td>',
                '</tr>',
                '<tr>',
                '<td><label for="rgftpuser">RescueGroups FTP username</label></td>',
                '<td><input id="rgftpuser" type="text" class="asm-textbox cfg" data="RescueGroupsFTPUser" /></td>',
                '</tr>',
                '<tr>',
                '<td><label for="rgftppass">RescueGroups FTP password</label></td>',
                '<td><input id="rgftppass" type="text" class="asm-textbox cfg" data="RescueGroupsFTPPassword" /></td>',
                '</tr>',
                '</table>',
                '</div>'
            ].join("\n");
        },

        render_adoptapet: function() {
            return [
                '<div id="tab-adoptapet">',
                '<p><input id="enabledap" type="checkbox" class="asm-checkbox enablecheck" /><label for="enabledap">' + _("Enabled") + '</label></p>',
                '<div class="ui-state-highlight ui-corner-all" style="padding: 0 .7em;">',
                '<p><span class="ui-icon ui-icon-info" style="float: left; margin-right: .3em;"></span>',
                'The default AdoptAPet host is "autoupload.adoptapet.com".',
                '</p>',
                '</div>',
                '<table>',
                '<tr>',
                '<td><label for="apftphost">AdoptAPet FTP host</label></td>',
                '<td><input id="apftphost" type="text" class="asm-textbox cfg" data="SaveAPetFTPURL" /></td>',
                '</tr>',
                '<tr>',
                '<td><label for="apftpuser">AdoptAPet FTP username</label></td>',
                '<td><input id="apftpuser" type="text" class="asm-textbox cfg" data="SaveAPetFTPUser" /></td>',
                '</tr>',
                '<tr>',
                '<td><label for="apftppass">AdoptAPet FTP password</label></td>',
                '<td><input id="apftppass" type="text" class="asm-textbox cfg" data="SaveAPetFTPPassword" /></td>',
                '</tr>',
                '<tr>',
                '<td><label for="includecolours">Include colors in column 9</label></td>',
                '<td><select id="includecolours" class="asm-selectbox pbool preset" data="includecolours">',
                '<option value="0">' + _("No") + '</option>',
                '<option value="1">' + _("Yes") + '</option>',
                '</select></td>',
                '</tr>',
                '<tr>',
                '<td><label for="noimportfile">Don\'t upload import.cfg</label></td>',
                '<td><select id="noimportfile" class="asm-selectbox pbool preset" data="noimportfile">',
                '<option value="0">' + _("No") + '</option>',
                '<option value="1">' + _("Yes") + '</option>',
                '</select></td>',
                '</tr>',
                '</table>',
                '</div>'
            ].join("\n");
        },

        render_meetapet: function() {
            return [
                '<div id="tab-meetapet">',
                '<p><input id="enabledmp" type="checkbox" class="asm-checkbox enablecheck" /><label for="enabledmp">' + _("Enabled") + '</label></p>',
                '<div class="ui-state-highlight ui-corner-all" style="padding: 0 .7em; display: none">',
                '<p><span class="ui-icon ui-icon-info" style="float: left; margin-right: .3em;">',
                '</span>',
                'The default MeetAPet Base URL is "meetapet.com/api_crud/".',
                '</p>',
                '</div>',
                '<table>',
                '<tr style="display: none">',
                '<td><label for="mpkey">MeetAPet Key</label></td>',
                '<td><input id="mpkey" type="text" class="asm-textbox cfg" data="MeetAPetKey" /></td>',
                '</tr>',
                '<tr>',
                '<td><label for="mpsecret">MeetAPet Secret</label></td>',
                '<td><input id="mpsecret" type="text" class="asm-textbox cfg" data="MeetAPetSecret" /></td>',
                '</tr>',
                '<tr>',
                '<td><label for="mpuserkey">MeetAPet Shelter Key</label></td>',
                '<td><input id="mpuserkey" type="text" class="asm-textbox cfg" data="MeetAPetUserKey" /></td>',
                '</tr>',
                '<tr style="display: none">',
                '<td><label for="mpbaseurl">MeetAPet Base URL</label></td>',
                '<td><input id="mpbaseurl" type="text" class="asm-textbox cfg" data="MeetAPetBaseURL" /></td>',
                '</tr>',
                '</table>',
                '</div>'
            ].join("\n");
        },

        render_helpinglostpets: function() {
            return [
                '<div id="tab-helpinglostpets">',
                '<p><input id="enabledhlp" type="checkbox" class="asm-checkbox enablecheck" /><label for="enabledhlp">' + _("Enabled") + '</label></p>',
                '<div class="ui-state-highlight ui-corner-all" style="padding: 0 .7em;">',
                '<p><span class="ui-icon ui-icon-info" style="float: left; margin-right: .3em;"></span>',
                'The default HelpingLostPets host is www.helpinglostpets.com.',
                '</p>',
                '</div>',
                '<table>',
                '<tr>',
                '<td><label for="hlpftphost">HelpingLostPets FTP host</label></td>',
                '<td><input id="hlpftphost" type="text" class="asm-textbox cfg" data="HelpingLostPetsFTPURL" /></td>',
                '</tr>',
                '<tr>',
                '<td><label for="hlpftpuser">HelpingLostPets FTP username</label></td>',
                '<td><input id="hlpftpuser" type="text" class="asm-textbox cfg" data="HelpingLostPetsFTPUser" /></td>',
                '</tr>',
                '<tr>',
                '<td><label for="hlpftppass">HelpingLostPets FTP password</label></td>',
                '<td><input id="hlpftppass" type="text" class="asm-textbox cfg" data="HelpingLostPetsFTPPassword" /></td>',
                '</tr>',
                '<tr>',
                '<td><label for="hlporgid">HelpingLostPets Organisation ID</label></td>',
                '<td><input id="hlporgid" type="text" class="asm-textbox cfg" data="HelpingLostPetsOrgID" /></td>',
                '</tr>',
                '<tr>',
                '<td><label for="hlppostal">Postal/Zip Code of your shelter</label></td>',
                '<td><input id="hlppostal" type="text" class="asm-textbox cfg" data="HelpingLostPetsPostal" /></td>',
                '</tr>',
                '</table>',
                '</div>'
            ].join("\n");
        },

        render_smarttag: function() {
            return [
                '<div id="tab-smarttag">',
                '<p><input id="enabledst" type="checkbox" class="asm-checkbox enablecheck" /><label for="enabledst">' + _("Enabled") + '</label></p>',
                '<table>',
                '<tr>',
                '<td><label for="stftphost">SmartTag FTP host</label></td>',
                '<td><input id="stftphost" type="text" class="asm-textbox cfg" data="SmartTagFTPURL" /></td>',
                '</tr>',
                '<tr>',
                '<td><label for="stftpuser">SmartTag FTP username</label></td>',
                '<td><input id="stftpuser" type="text" class="asm-textbox cfg" data="SmartTagFTPUser" /></td>',
                '</tr>',
                '<tr>',
                '<td><label for="stftppass">SmartTag FTP password</label></td>',
                '<td><input id="stftppass" type="text" class="asm-textbox cfg" data="SmartTagFTPPassword" /></td>',
                '</tr>',
                '</table>',
                '</div>'
            ].join("\n");
        },

        render: function() {
            return [
                html.content_header(_("Publishing Options")),
                '<div class="asm-toolbar">',
                '<button id="button-save" title="' + _("Update publishing options") + '">' + html.icon("save") + ' ' + _("Save") + '</button>',
                '</div>',
                '<div id="tabs">',
                this.render_tabs(),
                this.render_animalselection(),
                this.render_allpublishers(),
                this.render_avid(),
                this.render_petlink(),
                this.render_facebook(),
                this.render_htmlftp(),
                this.render_petfinder(),
                this.render_rescuegroups(),
                this.render_adoptapet(),
                this.render_meetapet(),
                this.render_helpinglostpets(),
                this.render_smarttag(),
                '</div>',
                html.content_footer()
            ].join("\n");
        },

        bind: function() {
            var change_checkbox = function() {
                $(".enablecheck").each(function() {
                    var enabled = $(this).is(":checked");
                    if (enabled) {
                        $(this).closest("div").find("select").select("enable");
                        $(this).closest("div").find(".asm-textbox").removeAttr("disabled");
                        $(this).closest("div").find("textarea").removeAttr("disabled");
                    }
                    else {
                        $(this).closest("div").find("select").select("disable");
                        $(this).closest("div").find(".asm-textbox").attr("disabled", "disabled");
                        $(this).closest("div").find("textarea").attr("disabled", "disabled");
                    }
                });
            };

            var cfg_presets = function() {
                // Read the controls tagged with preset and build an 
                // old style publisher command line string for storing as a
                // configuration option.
                var pr = "";
                $(".preset").each(function() {
                    if ($(this).is(".pbool")) {
                        if ($(this).val() == "1") { pr += " " + $(this).attr("data"); }
                    }
                    else {
                        pr += " " + $(this).attr("data") + "=" + $(this).val();
                    }
                });
                return encodeURIComponent($.trim(pr));
            };

            var cfg_enabled = function() {
                // Read the enable checkboxes and build a list of enabled publishers 
                // for storing as a configuration option.
                var ep = "";
                if ($("#enabledhtml").is(":checked")) { ep += " html"; }
                if ($("#enabledpf").is(":checked")) { ep += " pf"; }
                if ($("#enabledap").is(":checked")) { ep += " ap"; }
                if ($("#enabledrg").is(":checked")) { ep += " rg"; }
                if ($("#enabledmp").is(":checked")) { ep += " mp"; }
                if ($("#enabledhlp").is(":checked")) { ep += " hlp"; }
                if ($("#enabledpl").is(":checked")) { ep += " pl"; }
                if ($("#enabledst").is(":checked")) { ep += " st"; }
                return encodeURIComponent($.trim(ep));
            };

            // Disable publisher panels when the checkbox says they're disabled
            $(".enablecheck").change(change_checkbox);

            // Disable publishing to a folder if it was overridden
            if (controller.publishurl != "") {
                $("#publishdirrow").hide();
                $("#publishdiroverride").show();
                var url = controller.publishurl;
                url = url.replace("{alias}", asm.useraccountalias);
                url = url.replace("{database}", asm.useraccount);
                url = url.replace("{username}", asm.user);
                $("#publishdiroverride a").attr("href", url).text(url);
            }

            // Disable ftp upload controls if ftp has been overridden
            if (controller.hasftpoverride) {
                $("#ftpuploadtable").hide();
            }

            // Toolbar buttons
            $("#button-save").button().click(function() {
                $("#button-save").button("disable");
                var formdata = "mode=save&" + $(".cfg").toPOST();
                formdata += "&PublisherPresets=" + cfg_presets();
                formdata += "&PublishersEnabled=" + cfg_enabled();
                common.ajax_post("publish_options", formdata, function() { window.location="publish_options"; });
            });
            $("#button-save").button("disable");

            $(".localeus").hide();
            $(".localeca").hide();
            $(".localegb").hide();
            $(".facebook").hide();

            // Enable tabs for US only publishers
            if (asm.locale == "en") {
                $(".localeus").show();
            }

            // Enable tab sections for British publishers
            if (asm.locale == "en_GB") {
                $(".localegb").show();
            }
            // Enable tab sections for Canadian publishers
            if (asm.locale == "en_CA") {
                $(".localeca").show();
            }

            // Enable tab sections for facebook
            if (controller.hasfacebook) {
                $(".facebook").show();
            }

            // Components
            $("#tabs").tabs({ show: "slideDown", hide: "slideUp" });

            // Load default values from the config settings
            $(".cfg").each(function() {
                if ($(this).attr("data")) {
                    var d = $(this).attr("data");
                    if ($(this).is("input:text")) {
                        $(this).val( html.decode(config.str(d)));
                    }
                    else if ($(this).is("input:checkbox")) {
                        $(this).attr("checked", config.bool(d));
                    }
                    else if ($(this).is("select")) {
                        $(this).select("value", config.str(d));
                    }
                    else if ($(this).is("textarea")) {
                        $(this).val(config.str(d));
                    }
                }
            });

            // Set presets from command line configuration
            var cl = config.str("PublisherPresets");
            $.each(cl.split(" "), function(i, o) {
                // Deal with boolean flags in command line
                $.each( [ "includecase", "includereserved", "includefosters", "includewithoutimage", 
                    "includecolours", "includeretailer", "includehold", "includequarantine", "bondedassingle",
                    "clearexisting", "uploadall", "forcereupload", 
                    "generatejavascriptdb","thumbnails", "checksocket", "uploaddirectly", 
                    "htmlbychildadult", "htmlbyspecies", "noimportfile" ], 
                function(bi, bo) {
                    if (bo == o) { $("[data='" + bo + "']").select("value", "1"); }
                });
                // Deal with key/value pairs
                $.each( [ "order", "excludeunder", "animalsperpage", "limit", "style", "extension",
                    "scaleimages", "thumbnailsize", "includelocations", "ftproot", "publishdirectory", 
                    "childadultsplit" ],
                function(vi, vo) {
                    if (o.indexOf(vo) == 0) {
                        var v = o.split("=")[1];
                        var node = $("[data='" + vo + "']");
                        if (node.hasClass("asm-selectbox")) {
                            node.select("value", v);
                        }
                        else if (node.hasClass("asm-bsmselect")) {
                            var ls = v.split(",");
                            $.each(ls, function(li, lv) {
                                node.find("[value='" + lv + "']").prop("selected", "selected");
                            });
                            node.change();
                        }
                        else {
                            node.val(v);
                        }
                    }
                });
            });

            // Set enabled from enabled list
            var pe = config.str("PublishersEnabled");
            if (pe.indexOf("html") != -1) { $("#enabledhtml").attr("checked", true); }
            if (pe.indexOf("pf") != -1) { $("#enabledpf").attr("checked", true); }
            if (pe.indexOf("ap") != -1) { $("#enabledap").attr("checked", true); }
            if (pe.indexOf("rg") != -1) { $("#enabledrg").attr("checked", true); }
            if (pe.indexOf("mp") != -1) { $("#enabledmp").attr("checked", true); }
            if (pe.indexOf("hlp") != -1) { $("#enabledhlp").attr("checked", true); }
            if (pe.indexOf("pl") != -1) { $("#enabledpl").attr("checked", true); }
            if (pe.indexOf("st") != -1) { $("#enabledst").attr("checked", true); }

            // Disable publisher fields for those not active
            change_checkbox();

            validate.bind_dirty();

        }
    };

    common.module(publish_options, "publish_options", "options");

});


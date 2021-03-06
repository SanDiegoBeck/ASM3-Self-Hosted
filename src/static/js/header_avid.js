/*jslint browser: true, forin: true, eqeq: true, white: true, sloppy: true, vars: true, nomen: true */
/*global $, _, asm, common, config, format, header, html */
/*global avid: true */

$(function() {

    // If this is the login or database create page, don't do anything - they don't have headers, 
    // but for the sake of making life easy, they still include this file.
    if (common.current_url().indexOf("/login") != -1 ||
        common.current_url().indexOf("/database") != -1) {
        return;
    }

    avid = {

        /** Renders an avid form to post animal and owner data to
         *  their PetTRAC database.
         *  a: An animal object from get_animal
         *  p: A person object. If not supplied, a.CURRENTOWNER* will be used
         */
        render: function(a, p) {
            // If the locale isn't GB, abandon
            if (asm.locale != "en_GB") { 
                header.show_error("AVID submitting is only available for UK users.");
                return;
            }
            // If AVID isn't configured, bail out as well
            if (config.str("AvidOrgName") == "") { 
                header.show_error("AVID organisation configuration has not been set.");
                return;
            }
            // If the animal doesn't have a valid microchip number or date, abandon
            if (a.IDENTICHIPNUMBER.indexOf("977") != 0) {
                header.show_error("AVID chip numbers must start with 977.");
                return;
            }
            if (a.IDENTICHIPDATE == null) {
                header.show_error("Microchip date must not be blank.");
                return;
            }
            var breed = a.BREEDNAME;
            if (breed.indexOf("Domestic Long") == 0) { breed = "DLH"; }
            else if (breed.indexOf("Domestic Short") == 0) { breed = "DSH"; }
            else if (breed.indexOf("Domestic Medium") == 0) { breed = "DSLH"; }
            var neutered = a.NEUTERED == 1;
            var species = a.SPECIESNAME;
            if (species.indexOf("Dog") == 0) { species = "Canine"; }
            else if (species.indexOf("Cat") == 0) { species = "Feline"; }
            else if (species.indexOf("Bird") == 0) { species = "Avian"; }
            else if (species.indexOf("Horse") == 0) { species = "Equine"; }
            else if (species.indexOf("Reptile") == 0) { species = "Reptilian"; }
            else { species = "Other"; }
            var hf = function(name, value) {
                return "<input type='hidden' name='" + name + "' value='" + html.title(value) + "' />";
            };
            var tr = function(label, name, value) {
                return "<tr><td><label for='" + name + "'>" + label + "</label></td><td><input type='text' class='asm-textbox' id='" + 
                    name + "' name='" + name + "' value='" + html.title(value) + "' /></td></tr>";
            };
            var avid_date = function(iso) {
                var d = format.date_js(iso);
                if (d == null) { return ""; }
            };
            var h = [
                '<form target="_blank" method="post" action="https://online.pettrac.com/registration/onlineregistration.aspx">',
                hf("orgpostcode", config.str("AvidOrgPostcode")),
                hf("orgname", config.str("AvidOrgName")),
                hf("orgserial", config.str("AvidOrgSerial")),
                hf("orgpassword", config.str("AvidOrgPassword")),
                hf("version", "1.1"),
                '<p class="centered">',
                '<button class="avidsubmit" type="submit">Send to AVID PETtrac database</button>',
                '</p>',
                '<h2 class="asm-header">Chip Details</h2>',
                '<table>',
                tr("Chip number", "microchip", a.IDENTICHIPNUMBER),
                tr("Implant date", "implantdate", avid_date(a.IDENTICHIPDATE)),
                '</table>',
                '<h2 class="asm-header">Owner Details</h2>',
                '<table>',
                tr("Title", "prefix", (p ? p.OWNERTITLE : a.CURRENTOWNERTITLE)),
                tr("Surname", "surname", (p ? p.OWNERSURNAME : a.CURRENTOWNERSURNAME)),
                tr("Forenames", "firstname", (p ? p.OWNERFORENAMES : a.CURRENTOWNERFORENAMES)),
                tr("Address", "address1", (p ? p.OWNERADDRESS : a.CURRENTOWNERADDRESS)),
                tr("City", "city", (p ? p.OWNERTOWN : a.CURRENTOWNERTOWN)),
                tr("County", "county", (p ? p.OWNERCOUNTY : a.CURRENTOWNERCOUNTY)),
                tr("Postcode", "postcode", (p ? p.OWNERPOSTCODE : a.CURRENTOWNERPOSTCODE)),
                tr("Home Phone", "telhome", (p ? p.HOMETELEPHONE : a.CURRENTOWNERHOMETELEPHONE)),
                tr("Work Phone", "telwork", (p ? p.WORKTELEPHONE : a.CURRENTOWNERWORKTELEPHONE)),
                tr("Mobile Phone", "telmobile", (p ? p.MOBILETELEPHONE : a.CURRENTOWNERMOBILETELEPHONE)),
                tr("Alternative Phone", "telalternative", ""),
                tr("Email Address", "email", (p ? p.EMAILADDRESS : a.CURRENTOWNEREMAILADDRESS)),
                '</table>',
                '<h2 class="asm-header">Animal Details</h2>',
                '<table>',
                tr("Name", "petname", a.ANIMALNAME),
                tr("Gender", "petgender", a.SEXNAME.substring(0, 1)),
                tr("DOB", "petdob", avid_date(a.DATEOFBIRTH)),
                tr("Species", "petspecies", species),
                tr("Breed", "petbreed", breed),
                tr("Neutered", "petneutered", neutered),
                tr("Colour", "petcolour", a.BASECOLOURNAME),
                '</table>',
                '<p class="centered">',
                '<button class="avidsubmit" type="submit">Send to AVID PETtrac database</button>',
                '</p>',
                '</form>'
            ].join("\n");
            return h;
        }
    };

});

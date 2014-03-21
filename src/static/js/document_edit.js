/*jslint browser: true, forin: true, eqeq: true, white: true, sloppy: true, vars: true */
/*global $, baseurl, buildno, tinymce, tinyMCE */

$(function() {

    tinymce.init({
        selector: "#wp",
        theme: "modern",
        content_css: "css?v=asm-tinymce.css&k=" + buildno,
        plugins: [
            "advlist autolink lists link image charmap print preview hr anchor pagebreak",
            "searchreplace wordcount visualblocks visualchars code fullscreen",
            "insertdatetime media nonbreaking save table contextmenu directionality",
            "emoticons template paste textcolor save spellchecker"
            ],
        toolbar1: "save preview pdf print | undo redo | styleselect | bold italic forecolor backcolor | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent pagebreak | link image",
        spellchecker_rpc_url: baseurl + "/spellcheck",
        spellchecker_languages: "+English (US)=en,English (United Kingdom)=en_GB",
        save_enablewhendirty: true,

        setup: function(ed) {

            ed.addButton("pdf", {
                title: "PDF",
                image: "static/images/ui/pdf-wp-button.gif",
                onclick: function() {
                    $("input[name='savemode']").val("pdf");
                    $("form").submit();
                }
            });

            // Override normal page break behaviour. Note that there's a race condition
            // and the normal plugin command gets registered after this, so we have to
            // put it in a timer so that our command is added last to override everything else.
            setTimeout(function() {
                ed.addCommand("mcePageBreak", function() {
                    tinyMCE.execCommand("mceInsertContent", false, "<div class='mce-pagebreak' style='page-break-before: always; clear: both; border: 0'>&nbsp;</div>");
                });
            }, 1000);

        },

        oninit: function() {
            //tinyMCE.execCommand("mceFullScreen");
        }
    });

});

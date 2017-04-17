$(document).ready(function() {

    var isNotIE78 = jQuery.support.leadingWhitespace;
    var element = $("#id_description");
    if (isNotIE78 && element.length > 0){
        // IE7-8 explode with Ace editor <sigh>
        var description = element.hide();
        description.after(
            '<div style="height:100px; " id="description-editor" class="colM aligned vLargeTextField"></div>'
        );

        description.parents(".form-row").after('<div class="form-row"><div><label>Description Preview:</label><pre id="description-preview"></pre></div></div>');

        var descriptionEditor = ace.edit("description-editor");
        var descriptionSession = descriptionEditor.getSession();
        var preview = $("#description-preview");
        preview.html(description.val());

        descriptionEditor.setValue(description.val());
        descriptionSession.setMode( "ace/mode/html");
        descriptionSession.setTabSize(2)
        descriptionSession.setUseSoftTabs(true)
        descriptionEditor.on('blur', function(){
            description.val(descriptionEditor.getValue());
        });

        descriptionEditor.on('change', function(){
            preview.html(descriptionEditor.getValue());
        });
        descriptionEditor.resize();
    }
});

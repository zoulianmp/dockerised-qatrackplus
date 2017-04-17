"use strict";

var csrf_token = $("input[name=csrfmiddlewaretoken]").val();

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
            // Send the token to same-origin, relative URLs only.
            // Send the token only if the method warrants CSRF protection
            // Using the CSRFToken value acquired earlier
            xhr.setRequestHeader("X-CSRFToken", csrf_token);
        }
    }
});

/***************************************************************/
//Test statuse and Table context used to narrow down jQuery selectors.
//Improves performance in IE
var context;

var pass_fail_only;
var comment_on_skip;


// keeps track of latest composite call so we can
// ignore older ones f they comlete after the latest one
var latest_composite_call;

/***************************************************************/
//minimal Pub/Sub functionality
var topics = {};
jQuery.Topic = function( id ) {
    var callbacks,
        method,
        topic = id && topics[ id ];

    if ( !topic ) {
        callbacks = jQuery.Callbacks();
        topic = {
            publish: callbacks.fire,
            subscribe: callbacks.add,
            unsubscribe: callbacks.remove
        };
        if ( id ) {
            topics[ id ] = topic;
        }
    }
    return topic;
};

window.imageTemplate = _.template($("#attach-template").html());

function Test(data){
    _.extend(this,data);
}

function Reference(data){
    _.extend(this,data);
}

function Tolerance(data){
    _.extend(this,data);
    if (this.type === QAUtils.MULTIPLE_CHOICE){
        this.mc_pass_choices = this.mc_pass_choices ? this.mc_pass_choices.split(",") : [];
        this.mc_tol_choices = this.mc_tol_choices ? this.mc_tol_choices.split(",") : [];
    }
}

function Status(status, diff, message){
    this.status = status;
    this.diff = diff;
    this.message = message;
}
var NO_TOL = new Status(QAUtils.NO_TOL, "", QAUtils.NO_TOL_DISP);
var NOT_DONE = new Status(QAUtils.NOT_DONE, "", QAUtils.NOT_DONE_DISP);
var DONE = new Status(QAUtils.DONE, "", QAUtils.DONE_DISP);

function TestInfo(data){
    var self = this;
    this.id = data.id;
    this.test = new Test(data.test);
    this.reference = new Reference(data.reference);
    this.tolerance = new Tolerance(data.tolerance);


    this.check_value = function(value){
        var result = self.check_dispatch[self.test.type](value)
        if (pass_fail_only){
            if (result.status === QAUtils.ACTION){
                result.message = QAUtils.FAIL_DISP;
            }else if (result.status === QAUtils.TOLERANCE || result.status === QAUtils.NO_TOL){
                result.message = QAUtils.WITHIN_TOL_DISP;
                result.status = QAUtils.WITHIN_TOL;
            }else{
                result.message = QAUtils.WITHIN_TOL_DISP;
            }
        }
        return result;
    };

    this.check_bool = function(value){
        if (_.isEmpty(self.reference)){
            return NO_TOL;
        }else if (QAUtils.almost_equal(value,self.reference.value)){
            return new Status(QAUtils.WITHIN_TOL,0,QAUtils.WITHIN_TOL_DISP);
        }

        return new Status(QAUtils.ACTION,1,QAUtils.ACTION_DISP);
    };

    this.check_multi = function(value){

        var status, message;

        if (value === ""){
            return NOT_DONE;
        }

        if (_.isEmpty(self.tolerance) || self.tolerance.mc_pass_choices.length === 0){
            return NO_TOL;
        }
        if (_.indexOf(self.tolerance.mc_pass_choices,value) >= 0){
            status = QAUtils.WITHIN_TOL;
            message = QAUtils.WITHIN_TOL_DISP;
        }else if (_.indexOf(self.tolerance.mc_tol_choices,value) >= 0){
            status = QAUtils.TOLERANCE;
            message = QAUtils.TOLERANCE_DISP;
        }else{
            status = QAUtils.ACTION;
            message = QAUtils.ACTION_DISP;
        }

        return new Status(status,null,message);
    };

    this.check_upload = function(value){
        return value ? DONE : NOT_DONE;
    };

    this.check_numerical = function(value){

        if (_.isEmpty(self.reference) || _.isEmpty(self.tolerance)){
            return NO_TOL;
        }

        var diff = self.calculate_diff(value);
        var message = self.diff_display(diff);

        var al=self.tolerance.act_low,
            tl=self.tolerance.tol_low,
            th=self.tolerance.tol_high,
            ah=self.tolerance.act_high;

        al = !_.isNull(al) ? al : -1.E99;
        tl = !_.isNull(tl) ? tl : -1.E99;
        th = !_.isNull(th) ? th : 1.E99;
        ah = !_.isNull(ah) ? ah : 1.E99;

        var on_action_border = QAUtils.almost_equal(al, diff) || QAUtils.almost_equal(ah, diff);
        var on_tolerance_border = QAUtils.almost_equal(tl, diff) || QAUtils.almost_equal(th, diff);

        var inside_action = ((al <= diff) && (diff <= ah )) || on_action_border;
        var inside_tolerance = (tl < diff) && (diff < th ) || on_tolerance_border;


        var status;
        if (!inside_action){
            message = QAUtils.ACTION_DISP + message;
            status = QAUtils.ACTION;
        }else if (!inside_tolerance){
            status = QAUtils.TOLERANCE;
            message = QAUtils.TOLERANCE_DISP + message;
        }else{
            status = QAUtils.WITHIN_TOL;
            message = QAUtils.WITHIN_TOL_DISP + message;
        }

        return new Status(status,diff,message);

    };

    this.check_dispatch = {}
    this.check_dispatch[QAUtils.BOOLEAN]=this.check_bool;
    this.check_dispatch[QAUtils.MULTIPLE_CHOICE]=this.check_multi;
    this.check_dispatch[QAUtils.CONSTANT]=this.check_numerical;
    this.check_dispatch[QAUtils.SIMPLE]=this.check_numerical;
    this.check_dispatch[QAUtils.COMPOSITE]=this.check_numerical;
    this.check_dispatch[QAUtils.STRING_COMPOSITE]=this.check_multi;
    this.check_dispatch[QAUtils.STRING]=this.check_multi;
    this.check_dispatch[QAUtils.UPLOAD]=this.check_upload;

    this.calculate_diff = function(value){
        if (self.tolerance.type === QAUtils.PERCENT){
            return 100.*(value-self.reference.value)/self.reference.value;
        }
        return value - self.reference.value;
    };

    this.diff_display = function(diff){

        if (self.tolerance.type === QAUtils.PERCENT){
            return "(" + diff.toFixed(1)+"%)";
        }
        return "(" + diff.toFixed(2)+")";
    }

}

function TestInstance(test_info, row){
    var self = this;
    this.initialized = false;
    this.test_info = test_info;
    this.row = $(row);
    this.inputs = this.row.find("td.qa-value").find("input, textarea, select").not("[name$=user_attached]");
    this.user_attach_input = this.row.find("input[name$=user_attached]")

    this.comment = this.row.next();

    this.visible = true;

    this.status = this.row.find("td.qa-status");
    this.test_status = null;

    this.skip = this.row.find("td.qa-skip input");
    this.skipped = false;
    this.set_skip = function(skipped){
        self.skipped = skipped;
        self.skip.prop("checked",self.skipped);
    };
    this.skip.change(function(){
        self.skipped = self.skip.is(":checked");
        if (self.skipped){
            if (comment_on_skip && !self.test_info.test.skip_without_comment){
                self.comment.show(600);
            }
            if (self.test_info.test.type === QAUtils.BOOLEAN || self.test_info.test.type === QAUtils.UPLOAD){
                self.set_value(null);
            }
            $.Topic("valueChanged").publish();
        }else{
            self.comment.hide(600);
        }
    });

    this.show_comment = this.row.find("td.qa-showcmt a");
    this.comment_box = this.comment.find("textarea");
    this.comment_icon = this.row.find(".qa-showcmt i");

    this.show_comment.click(function(){

        self.comment.toggle('fast');
        self.comment.find('.comment-div').slideToggle('fast');

        return false;
    });
    this.set_comment_icon = function(){
        self.comment_icon.removeClass();
        if ( $.trim(self.comment_box.val()) != ''){
            self.comment_icon.addClass("fa fa-commenting");
        }else{
            self.comment_icon.addClass("fa fa-commenting-o");
        }
    };
    require(['autosize'], function(autosize) {
        autosize(self.comment.find('textarea'));
    });
    this.set_comment_icon(); //may already contain comment on initialization
    this.comment_box.blur(this.set_comment_icon);

    this.show_procedure = this.row.find("td.qa-showproc a");
    this.procedure = this.comment.next();
    this.show_procedure.click(function(){
        self.procedure.toggle('fast');
        self.procedure.find('.qa-procedure-text').slideToggle('fast');
        return false;
    });

    this.value = null;

    this.inputs.change(function(){
        self.update_value_from_input();
        if (self.skipped){
            self.set_skip(false);
        }
        $.Topic("valueChanged").publish();
        $.Topic("qaUpdated").publish();
    });

    this.set_value = function(value, user_attached){
        //set value manually and update inputs accordingly
        var tt = self.test_info.test.type;

        self.value = value;

        if (tt === QAUtils.BOOLEAN){
            if (_.isNull(value)){
                self.inputs.prop("checked",false);
            }else{
                self.inputs[0].checked = value === 0;
                self.inputs[1].checked = !self.inputs[0].checked;
            }
        }else if (tt=== QAUtils.STRING || tt === QAUtils.MULTIPLE_CHOICE || tt === QAUtils.STRING_COMPOSITE){
            self.inputs.val(value);
        }else if (tt === QAUtils.UPLOAD){
            if (_.isNull(value)){
                self.inputs.filter(".qa-input:hidden").val("");
            }else{
                self.inputs.filter(".qa-input:hidden").val(value["attachment_id"]);
                self.value = value.result;
            }
        }else if (tt === QAUtils.SIMPLE || tt === QAUtils.COMPOSITE){
            if (_.isNull(value)){
                self.inputs.val("");
            }else{
                self.inputs.val(QAUtils.format_float(value));
            }
        }

        var uploadAttached =  value && value.attachment;
        var uploadUserAttached = value && (value.user_attached && value.user_attached.length > 0);
        var compUserAttached = user_attached && user_attached.length > 0;
        var uattachs = [];
        if (uploadAttached){
            uattachs = uattachs.concat(value.attachment);
        }
        if (uploadUserAttached){
            uattachs = uattachs.concat(value.user_attached);
        }
        if (compUserAttached){
            uattachs = uattachs.concat(user_attached);
        }
        if (uattachs.length > 0){

            var attach_ids = _.map(uattachs, "attachment_id");
            self.user_attach_input.val(attach_ids.join(","));

            self.clear_images();

            _.each(uattachs, function(att){
                if (att.is_image){
                    self.display_image(att);
                }
            })

        }

        this.update_status();
    };

    this.update_value_from_input = function(){

        var tt = self.test_info.test.type;
        if (tt === QAUtils.BOOLEAN){
            var value = parseFloat(self.inputs.filter(":checked").val());
            self.value = _.isNaN(value) ? null : value;
        }else if (tt === QAUtils.MULTIPLE_CHOICE){
            var value = $.trim(self.inputs.find(":selected").text());
            self.value = value !== "" ? value : null;
        }else if (tt === QAUtils.UPLOAD){
            if (editing_tli && !this.initialized){
                var data = {
                    attachment_id: self.inputs.val(),
                    test_id: self.test_info.test.id,
                    test_list_instance: editing_tli,
                    meta: JSON.stringify(get_meta_data()),
                    refs: JSON.stringify(get_ref_data()),
                    tols: JSON.stringify(get_tol_data())
                };

                $.ajax({
                    type:"POST",
                    url: QAURLs.UPLOAD_URL,
                    data: $.param(data),
                    dataType:"json",
                    success: function (result) {
                        self.status.removeClass("btn-info btn-primary btn-danger btn-success");
                        if (result.errors.length > 0){
                            self.set_value(null);
                            self.status.addClass("btn-danger").text("Failed");
                            self.status.attr("title",result.errors[0]);
                        }else{
                            self.set_value(result);
                            self.status.addClass("btn-success").text("Success");
                            self.status.attr("title",result['url']);
                            $.Topic("valueChanged").publish();
                        }
                    },
                    traditional:true,
                    error: function(e,data){
                        self.set_value(null);
                        self.status.removeClass("btn-primary btn-danger btn-success");
                        self.status.addClass("btn-danger").text("Server Error");
                    }
                });
            }

        }else if (tt=== QAUtils.STRING){
            self.value = self.inputs.val();
        }else {
            self.inputs.val(QAUtils.clean_numerical_value(self.inputs.val()));
            var dots = self.inputs.val().match(/\./g);
            if (dots===null || dots.length <= 1) {
                var value = parseFloat(self.inputs.val());
            }else {
                var value = NaN
            }
            self.value = _.isNaN(value) ? null : value;
        }

        this.update_status();
        this.initialized = true;
    };
    this.update_status = function(){
        var status = _.isNull(self.value)? NOT_DONE : self.test_info.check_value(self.value);
        if (self.test_info.test.type === QAUtils.UPLOAD){
            if (status === DONE){
                self.status.attr("title", self.value);
            }else{
                self.status.attr("title","");
            }
        }
        self.set_status(status);
    };
    this.set_status = function(status){
        if (test_info.test.type != 'upload') {
            self.status.html(status.message);
            self.status.removeClass("btn-success btn-warning btn-danger btn-info");
            self.test_status = status.status;
            if (status.status === QAUtils.WITHIN_TOL) {
                self.status.addClass("btn-success");
            } else if (status.status === QAUtils.TOLERANCE) {
                self.status.addClass("btn-warning");
            } else if (status.status === QAUtils.ACTION) {
                self.status.addClass("btn-danger");
            } else if (status.status !== QAUtils.NOT_DONE) {
                self.status.addClass("btn-info");
            }
        }
    };

    this.NOT_PERFORMED = "Category not performed";

    this.show = function(){
        self.row.show();
        self.comment.hide();
        self.comment.find('.comment-div').hide();
        self.procedure.hide('fast');
        self.procedure.find('.qa-procedure-text').hide();
        self.set_skip(false);
        self.visible = true;
        self.comment_box.val(self.comment_box.val().replace(self.NOT_PERFORMED,""));
        if (self.test_info.test.type == QAUtils.BOOLEAN){
            self.set_value(self.value);
        }
    };

    this.hide = function(){
        self.row.hide();
        self.comment.hide();
        self.comment.find('.comment-div').hide();
        self.procedure.hide('fast');
        self.procedure.find('.qa-procedure-text').hide();
        self.visible = false;

        // skipping sets value to null but we want to presever value in case it
        // is unfiltered later. Filtered values will be nulled on submitt
        var tmp_val = self.value;
        self.set_skip(true);
        self.set_value(tmp_val);
        if (self.test_info.test.type == QAUtils.BOOLEAN){
            self.inputs.prop("checked", false);
        }

        self.comment_box.val(self.NOT_PERFORMED);
    };

    if (test_info.test.type == 'upload') {

        require(['jquery', 'dropzone'], function ($, Dropzone) {

            self.dropzone = new Dropzone('#upload-button-' + test_info.test.id, {

                url: QAURLs.UPLOAD_URL,
                previewsContainer: false,
                // previewTemplate: $('#preview-template')[0].innerHTML,
                // dropZone: self.row.children(),
                // singleFileUploads: true,
                uploadMultiple: false,
                paramName: "upload",
                replaceFileInput: false,
                params: {
                    'csrfmiddlewaretoken': csrf_token,
                    "test_id": self.test_info.test.id,
                    "meta": JSON.stringify(get_meta_data()),
                    "refs": JSON.stringify(get_ref_data()),
                    "tols": JSON.stringify(get_tol_data())
                }

            });

            self.dropzone.on('totaluploadprogress', function(progress) {
                self.status.removeClass("btn-primary btn-danger btn-success btn-info");
                self.status.addClass("btn-warning").text(progress + "%");
            });

            self.dropzone.on('error', function(file, data) {
                self.set_value(null);
                self.status.removeClass("btn-primary btn-danger btn-success");
                self.status.addClass("btn-danger").text("Server Error");
            });

            self.dropzone.on('success', function(file, data) {

                var response_data = JSON.parse(data);
                self.status.removeClass("btn-primary btn-info btn-warning btn-danger btn-success");
                if (response_data.errors.length > 0) {
                    self.set_value(null);
                    self.status.addClass("btn-danger").text("Failed");
                    self.status.attr("title", response_data.errors[0]);
                } else {
                    self.set_value(response_data);
                    self.status.addClass("btn-success").text("Success");
                    self.status.attr("title", response_data.url);

                    $.Topic("valueChanged").publish();
                }
            });

        });

    }

    // set initial skip state
    this.skip.trigger("change");

    //Set initial value
    this.update_value_from_input();

    // Display images
    self.display_image = function(attachment){
        var name = self.test_info.test.name;
        var html = imageTemplate({a: attachment, test: name});
        if (self.test_info.test.display_image){
          $("#qa-images").css({"display": "block"});
          $("#"+self.test_info.test.slug).append(html);
        }
    };

    self.clear_images = function(){
        if (self.test_info.test.display_image){
          $("#qa-images").css({"display": ""});
          $("#" + self.test_info.test.slug).removeClass("qa-image-box").html("");
        }
    }
}

function get_meta_data(){

    var meta = {
        test_list_name: $("#test-list-name").val(),
        unit_number: parseInt($("#unit-number").val()),
        cycle_day: parseInt($("#cycle-day-number").val()),
        work_completed: QAUtils.parse_date($("#id_work_completed").val()),
        work_started: QAUtils.parse_date($("#id_work_started").val()),
        username: $("#username").text()
    };

    return meta;

}

function get_ref_data(){
    var ref_values = _.map(tli.test_instances, function(ti){
        return ti.test_info.reference.value ? ti.test_info.reference.value : null;
    });

    return _.zipObject(tli.slugs, ref_values);
}

function get_tol_data(){

    var tol_properties = ["act_high", "act_low", "tol_high", "tol_low", "mc_pass_choices", "mc_tol_choices", "type"];

    var tol_values = _.map(tli.test_instances, function(ti){
        var tol = ti.test_info.tolerance;
        return !tol.id ? null : _.pick(tol, tol_properties);
    });
    return _.zipObject(tli.slugs, tol_values);
}

function TestListInstance(){
    var self = this;

    this.test_instances = [];
    this.tests_by_slug = {};
    this.slugs = [];
    this.composites = [];
    this.composite_ids = [];

    this.submit = $("#submit-qa");

    this.attachInput = $("#tli-attachments");

    /***************************************************************/
    //set the intitial values, tolerances & refs for all of our tests
    this.initialize = function(){
        var test_infos = _.map(window.unit_test_infos,function(e){ return new TestInfo(e)});

        self.test_instances = _.map(_.zip(test_infos, $("#perform-qa-table tr.qa-valuerow")), function(uti_row){return new TestInstance(uti_row[0], uti_row[1])});
        self.slugs = _.map(self.test_instances, function(ti){return ti.test_info.test.slug});
        self.tests_by_slug = _.zipObject(self.slugs,self.test_instances);
        self.composites = _.filter(self.test_instances,function(ti){return ti.test_info.test.type === QAUtils.COMPOSITE || ti.test_info.test.type === QAUtils.STRING_COMPOSITE;});
        self.composite_ids = _.map(self.composites,function(ti){return ti.test_info.test.id;});
        self.attachInput.on("change", function(){
            var fnames = _.map(this.files, "name").join(", ");
            $("#tli-attachment-names").html(fnames);
        });
        self.calculate_composites();
    };


    this.calculate_composites = function(){


        if (self.composites.length === 0){
            return;
        }


        var cur_values = _.map(self.test_instances,function(ti){return ti.value;});
        var qa_values = _.zipObject(self.slugs,cur_values);
        var meta = get_meta_data();
        var refs = get_ref_data();
        var tols = get_tol_data();

        var data = {
            qavalues:qa_values,
            composite_ids:self.composite_ids,
            meta: meta,
            refs: refs,
            tols: tols
        };

        var on_success = function(data, status, XHR){

            if (latest_composite_call !== XHR){
                return;
            }

            self.submit.attr("disabled", false);

            if (data.success){
                _.each(data.results,function(result, name){
                    var ti = self.tests_by_slug[name];
                    if (!ti.skipped){
                        ti.set_value(result.value, result.user_attached);
                    }
                });
            }
            $.Topic("qaUpdated").publish();
        };

        var on_error = function(){
            self.submit.attr("disabled", false);
            $.Topic("qaUpdated").publish();
        };

        self.submit.attr("disabled", true);

        latest_composite_call = $.ajax({
            type:"POST",
            url:QAURLs.COMPOSITE_URL,
            data:JSON.stringify(data),
            contentType:"application/json",
            dataType:"json",
            success: on_success,
            traditional:true,
            error:on_error
        });
    };

    this.has_failing = function(){
        return _.filter(self.test_instances, function(ti){
                return ti.test_status === QAUtils.ACTION
            }).length > 0;
    };

    $.Topic("categoryFilter").subscribe(function(categories){
        _.each(self.test_instances,function(ti){
            if (categories === "all" || _.includes(categories,ti.test_info.test.category.toString())){
                ti.show();
            }else{
                ti.hide();
            }
        });
        $.Topic("qaUpdated").publish();
    });

    $.Topic("valueChanged").subscribe(self.calculate_composites);
}

function set_tab_stops(){

    var user_inputs=  $('.qa-input',context).not("[readonly=readonly]").not("[type=hidden]");
    var visible_user_inputs = user_inputs;

    var tabindex = 1;
    user_inputs.each(function() {
        $(this).attr("tabindex", tabindex);
        tabindex++;
    });
    user_inputs.first().focus();

    $.Topic("categoryFilterComplete").subscribe(function(){
        visible_user_inputs = user_inputs.filter(":visible");
    });

    //allow arrow key and enter navigation
    $(document).on("keydown","input, select", function(e) {

        var to_focus;
        //rather than submitting form on enter, move to next value
        if (e.which == QAUtils.KC_ENTER  || e.which == QAUtils.KC_DOWN ) {
            var idx = visible_user_inputs.index(this);

            if (idx == visible_user_inputs.length - 1) {
                to_focus= visible_user_inputs.first();
            } else {
                to_focus = visible_user_inputs[idx+1];
            }
            to_focus.focus()
            if (to_focus.type === "text"){
                to_focus.select();
            }
            return false;
        }else if (e.which == QAUtils.KC_UP ){
            var idx = visible_user_inputs.index(this);

            if (idx == 0) {
                to_focus = visible_user_inputs.last();
            } else {
                to_focus = visible_user_inputs[idx-1];
            }
            to_focus.focus()
            if (to_focus.type === "text"){
                to_focus.select();
            }
            return false;
        }
    });

}

var tli;

$(document).ready(function(){

    tli = new TestListInstance();
    tli.initialize();

    context = $("#perform-qa-table")[0];

    pass_fail_only = $("#pass-fail-only").val() === "yes" ? true : false;
    comment_on_skip = $("#require-comment-on-skip").val() === "yes" ? true : false;

    $("#test-list-info-toggle").click(function(){
        $("#test-list-info").toggle(600);
    });

    // general comment
    require(['autosize'], function(autosize) {
        autosize($('#id_comment'));
    });
    $("#toggle-gen-comment").click(function(){
        $('#qa-tli-comment').slideToggle('fast');
    });

    //set link for cycle when user changes cycle day dropdown
    $(".radio-days").on('ifChecked', function(){
        var day = $(this).attr('id').replace('day-', '');
        var cur = document.location.href;
        document.location.href = cur.replace(/day=(next|[0-9]+)/,"day="+day);
    });

    ////////// Submit button
    //make sure user actually want's to go back
    //this is here to help mitigate the risk that a user hits back or backspace key
    //by accident and completely hoses all the information they've entered during
    //a qa session

    $(window).bind("beforeunload",function(){
        var non_read_only_tis = _.filter(tli.test_instances, function(ti){
            var tt = ti.test_info.test.type;
            return QAUtils.READ_ONLY_TEST_TYPES.indexOf(tt) < 0;
        });

        if (_.some(_.map(non_read_only_tis,"value"))){
            return  "If you leave this page now you will lose all entered values.";
        }
    });
    $("#qa-form").preventDoubleSubmit().submit(function(){
        $(window).off("beforeunload");
    });

    ///////// Category checkboxes:
    var categories = $('.check-category');
    var showall = $('#category-showall');
    showall.on('ifChecked ifUnchecked', function(e) {
        if (e.type == 'ifChecked') {
            categories.iCheck('check');
        } else {
            categories.iCheck('uncheck');
        }
    });
    categories.on('ifChanged', function(e){
        var cats = [];
        $.each(categories.filter(':checked'), function () {
            cats.push($(this).attr('id').replace('category-', ''));
        });
        if (categories.filter(':checked').length == categories.length) {
            showall.prop('checked', true);
        }
        else {
            showall.prop('checked', false);
        }
        $.Topic("categoryFilter").publish(cats);
        $.Topic("categoryFilterComplete");
        showall.iCheck('update');
    });

    ///////// Work time
    if (override_date) {
        require(['jquery', 'moment', 'jquery.inputmask'], function ($, moment) {

            var base_range_settings = {
                singleDatePicker: true,
                autoclose: true,
                keyboardNavigation: false,
                timePicker: true,
                timePicker24Hour: true,
                // timePickerIncrement: 5,
                locale: {
                    "format": "DD-MM-YYYY HH:mm"
                }
            };

            var start_picker = $('#id_work_started'),
                completed_picker = $('#id_work_completed'),
                duration_picker = $('#id_work_duration');

            var duration_change = true,
                end_date_change = true;

            function apply_completed() {
                if (duration_change) {
                    var start = $(start_picker).data('daterangepicker').startDate.clone(),
                        end = $(completed_picker).data('daterangepicker').startDate.clone(),
                        duration = moment.duration(end.diff(start)),
                        hours = Math.min(Math.floor(duration.asHours()), 99);
                    hours = hours > 9 ? hours.toString() : '0' + hours;
                    var mins = duration.minutes() > 9 ? duration.minutes().toString() : '0' + duration.minutes();
                    $(duration_picker).val(hours + mins);
                    duration_change = false;
                }
            }

            $(start_picker).daterangepicker(
                base_range_settings
            ).on('apply.daterangepicker', function (ev, picker) {
                var min_date = picker.startDate.clone();
                $(completed_picker).daterangepicker(
                    $.extend({},
                        base_range_settings,
                        {
                            minDate: min_date,
                            maxDate: min_date.clone().add(99, 'hours').add(59, 'minutes')
                        }
                    )
                ).on('apply.daterangepicker', apply_completed);
                duration_change = false;
                $(duration_picker).val('');
                $(completed_picker).data('daterangepicker').setStartDate(min_date);
                $(completed_picker).data('daterangepicker').setEndDate(min_date);
                $(completed_picker).trigger('apply.daterangepicker');
            });

            var min_date = $(start_picker).data('daterangepicker').startDate.clone();
            $(completed_picker).daterangepicker(
                $.extend({},
                    base_range_settings,
                    {
                        minDate: min_date,
                        maxDate: min_date.clone().add(99, 'hours').add(59, 'minutes')
                    }
                )
            ).on('apply.daterangepicker', apply_completed).focus(function () {
                duration_change = true;
            });

            $(duration_picker).inputmask({
                mask: "99hr : 'min",
                definitions: {
                    "'": {
                        validator: "[0-5][0-9]",
                        cardinality: 2,
                        prevalidator: [{
                            validator: "[0-5]",
                            cardinality: 1
                        }]
                    }
                },
                "oncomplete": function () {
                    if (end_date_change) {
                        var duration = this.inputmask.unmaskedvalue();
                        var start_time = $($(start_picker)).data('daterangepicker').startDate,
                            hours = duration[0] + duration[1],
                            mins = duration[2] + duration[3];
                        var end_time = start_time.clone().add(hours, 'hours').add(mins, 'minutes')/*.format('DD-MM-YYYY HH:mm')*/;
                        $(completed_picker).data('daterangepicker').setStartDate(end_time);
                        $(completed_picker).data('daterangepicker').setEndDate(end_time);
                        end_date_change = false;
                    }
                }
            }).on('keypress', function () {
                end_date_change = true;
            });
        });
    }

    //////// Warning message
    var box_perform = $('#box-perform .box'),
        box_perform_header = $(box_perform).find('.box-header, .box-footer'),
        // box_perform_footer = $(box_perform).find('.box-footer'),
        sub_button = $('#submit-qa'),
        do_not_treat = $('.do-not-treat');

    function display_fail(fail) {
        require(['jquery-ui'], function() {
            fail ? function() {
                do_not_treat.show();
                box_perform.switchClass('box-primary box-pho-borders', 'box-danger box-red-borders', 1000);
                sub_button.switchClass('btn-primary', 'btn-danger', 1000);
                box_perform_header.addClass('red-bg', 1000);


            }() : function() {
                box_perform.switchClass('box-danger box-red-borders', 'box-primary box-pho-borders', 1000);
                sub_button.switchClass('btn-danger', 'btn-primary', 1000);
                box_perform_header.removeClass('red-bg', 1000, function() {
                    do_not_treat.hide();
                });

            }();
        });
    }

    $.Topic("qaUpdated").subscribe(function(){
        if (self.tli.has_failing()){
            display_fail(true);
        }else{
            display_fail(false);
        }
    });

    set_tab_stops();

});

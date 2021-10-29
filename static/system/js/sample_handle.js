var form = new FormData();
form.append('id',$("#samples").find("option:selected").attr("data-id"));
var csrftoken_input = $("meta[name='csrf-token']");
var csrftoken = csrftoken_input.attr("content");
// console.log(csrftoken);
$.ajaxSetup({
    'beforeSend':function(xhr,settings) {
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type)) {
            var csrftoken = $('meta[name=csrf-token]').attr('content');
            xhr.setRequestHeader("X-CSRFToken", csrftoken)
        }
    }
});

$.ajax({
    url:'/system/api/v1/sample_query',
    type:'POST',
    processData: false,
    contentType: false,
    data:form,
    success:function (data) {
        // console.log(data);
        if (data['code'] == 200) {
            console.log(data['data']);
            $("#sample_place").val(data['data']['sample_place']);
            $("#collector").val(data['data']['collector']);
        }
    },
    fail:function (error) {
        console.log(error);
    }

});




function upload_done(){
    // console.log('done');
    $('#staticBackdrop').modal('toggle');
    $('.file_state').empty();
    var fileName = $("#fileupload").val();
    var strFileName = fileName.substring(fileName.lastIndexOf("\\")+1);
    var state = '<i class="fas fa-paperclip m-r-xxs"></i><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">'+strFileName+'</font></font>';
    $('.file_state').append(state);
}



$(function () {

    $("#samples").on("change",
    function() {
        $("#sample_place").empty();
        $("#collector").empty();

        var form1 = new FormData();

        form1.append('id',$("#samples").find("option:selected").attr("data-id"));
        var csrftoken_input = $("meta[name='csrf-token']");
        var csrftoken = csrftoken_input.attr("content");
        console.log(csrftoken);
        $.ajaxSetup({
            'beforeSend':function(xhr,settings) {
                if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type)) {
                    var csrftoken = $('meta[name=csrf-token]').attr('content');
                    xhr.setRequestHeader("X-CSRFToken", csrftoken)
                }
            }
        });

        $.ajax({
            url:'/system/api/v1/sample_query',
            type:'POST',
            processData: false,
            contentType: false,
            data:form1,
            success:function (data) {
                // console.log(data);
                if (data['code'] == 200) {
                    $("#sample_place").val(data['data']['sample_place']);
                    $("#collector").val(data['data']['collector']);
                }

            },
            fail:function (error) {

            }

        });



    });




    $("#send").click(function (event) {
        event.preventDefault();
        console.log(1);

        var csrftoken_meta = $("meta[name='csrf-token']");
        var csrftoken = csrftoken_meta.attr('content');

        var file = $("#fileupload")[0].files[0];
        var form = new FormData();
        form.append("file", file);
        form.append('csrf_token',csrftoken);
        form.append('id', $("#samples").find("option:selected").attr("data-id"));

        $.ajax({
            type: "POST",
            url: "/system/api/v1/sample_handle",
            data:form,
            processData: false,
            contentType: false,
            dataType: 'json',
            success: function (result) {
                if(result['code']==200) {

                    $("#draw_place").show(500);

                    $("#tzxz").hide(100);
                    $("#old_data").attr('src',"data:image/png;base64, "+result['data']['old']);
                    $("#pre_data").attr('src',"data:image/png;base64, "+result['data']['pre']);

                }
            }
        });
    })


    $("#ycl").click(function (event) {
        event.preventDefault();
        $("#old_data").hide(500);
        $("#pre_data").show(500);
    });

    $("#yuanxian").click(function (event) {
        event.preventDefault();
        $("#pre_data").hide(500);
        $("#old_data").show(500);
    });


});


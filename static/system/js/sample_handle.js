
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
    $("#send").click(function (event) {
        event.preventDefault();
        console.log(1);

        var csrftoken_meta = $("meta[name='csrf-token']");
        var csrftoken = csrftoken_meta.attr('content');

        var file = $("#fileupload")[0].files[0];
        var form = new FormData();
        form.append("file", file);
        form.append('csrf_token',csrftoken);

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


})

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
        var chart = echarts.init(document.getElementById('bar'), 'white', {renderer: 'canvas'});


        var csrftoken_meta = $("meta[name='csrf-token']");
        var csrftoken = csrftoken_meta.attr('content');

        var file = $("#fileupload")[0].files[0];
        var form = new FormData();
        form.append("file", file);
        form.append('first', $('#first').val());
        form.append('end', $('#end').val());
        form.append('csrf_token',csrftoken);

        $.ajax({
            type: "POST",
            url: "/system/api/v1/visualization",
            data:form,
            processData: false,
            contentType: false,
            dataType: 'json',
            success: function (result) {
                if(result['code']==400) {
                    mdalert.alertInfoToast(result['message']);
                }
                chart.setOption(result);
            }
        });
    })
})
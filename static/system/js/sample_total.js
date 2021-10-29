
$(function () {
    $("#send").click(function (event) {
        event.preventDefault();
        console.log(1);

        var csrftoken_meta = $("meta[name='csrf-token']");
        var csrftoken = csrftoken_meta.attr('content');

        var sample_name = $("#sample_name").val();
        var sample_place = $("#sample_place").val();
        var collector = $("#collector").val();
        var sample_time = $("#sample_time").val();


        var form = new FormData();
        form.append('csrf_token',csrftoken);
        form.append('sample_name',sample_name);
        form.append('sample_place',sample_place);
        form.append('collector',collector);
        form.append('sample_time',sample_time);

        $.ajax({
            type: "POST",
            url: "/system/api/v1/sample_create",
            data:form,
            processData: false,
            contentType: false,
            dataType: 'json',
            success: function (result) {
                if(result['code'] == 200) {
                    mdalert.alertSuccessToast("样本上传成功");
                    $('#staticBackdrop').modal('toggle');
                    console.log("success");
                    // window.location.reload();

                }
                else{
                    // mdalert.loading(result['message'], 'warning');
                    mdalert.alertInfoToast(result['message'])
                }
            }
        });
    })




})
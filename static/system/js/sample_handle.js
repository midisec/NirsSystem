
function upload_done(){
    // console.log('done');
    $('#staticBackdrop').modal('toggle');
    $('.file_state').empty();
    var fileName = $("#fileupload").val();
    var strFileName = fileName.substring(fileName.lastIndexOf("\\")+1);
    var state = '<i class="fas fa-paperclip m-r-xxs"></i><font style="vertical-align: inherit;"><font style="vertical-align: inherit;">'+strFileName+'</font></font>';
    $('.file_state').append(state);
}
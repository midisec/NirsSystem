

$(function () {
    var url = window.location.href;
    var span1 = "<span class=\"shape1\"></span>";
    var span2 = "<span class=\"shape2\"></span>";

    if(url.indexOf('index') >= 0){
        var profileLi = $("li[name='index']");
        profileLi.addClass('active');
        profileLi.children().eq(0).append(span1 + span2);
    } else if(url.indexOf('total') >= 0 && url.indexOf('sample') >= 0){
        var profileLi = $("li[name='sample']");
        profileLi.addClass('active');

        // profileLi.children().eq(0).append(span1 + span2);
        profileLi.children().eq(0).children().eq(-2).addClass("shape2");
        profileLi.children().eq(0).children().eq(-3).addClass("shape1");
        profileLi.children().eq(0).addClass("subdrop");
        profileLi.children().eq(1).css("display","block");
        profileLi.children().eq(1).children().eq(0).children().eq(0).addClass("active");
    }else if(url.indexOf('handle') >= 0 && url.indexOf('sample') >= 0){
        var profileLi = $("li[name='sample']");
        profileLi.addClass('active');
        profileLi.children().eq(0).children().eq(-2).addClass("shape2");
        profileLi.children().eq(0).children().eq(-3).addClass("shape1");
        profileLi.children().eq(0).addClass("subdrop");
        profileLi.children().eq(1).css("display","block");
        profileLi.children().eq(1).children().eq(1).children().eq(0).addClass("active");
    }else if(url.indexOf('result') >= 0 && url.indexOf('sample') >= 0){
        var profileLi = $("li[name='sample']");
        profileLi.addClass('active');
        profileLi.children().eq(0).children().eq(-2).addClass("shape2");
        profileLi.children().eq(0).children().eq(-3).addClass("shape1");
        profileLi.children().eq(0).addClass("subdrop");
        profileLi.children().eq(1).css("display","block");
        profileLi.children().eq(1).children().eq(2).children().eq(0).addClass("active");
    }

});
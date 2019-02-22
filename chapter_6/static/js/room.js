/**
 * Created by kingname on 2018/7/21.
 */
function generate_chat_list_html(chat_list) {
    var msg_list = '';
    for (i = 0; i < chat_list.length; i++) {
        msg = chat_list[i]['msg'];
        nick = chat_list[i]['nick'];
        post_time = chat_list[i]['post_time'];
        var line = '<div class="columns" style="margin-top: 5px">';
        line += '<div class="user_name">';
        if (nick === window.decodeURI(Cookies('name'))) {
            line += '<span class="label label-success centered">' + '我' + '</span>';
        } else {
            line += '<span class="label label-secondary">' + nick + '</span>';
        }
        line += '</div>';
        line += '<div class="text-gray">';
        line += '<span class="label">' + post_time + '</span>';
        line += '</div>';
        line += '<br />';
        line += '<div class="float-right">' + msg + '</div>';
        line += '</div>';
        msg_list += line;
    }
    return msg_list
}

function refresh() {
    $.ajax({
        url: '/get_chat_list',
        success: function (data) {
            var chat_list_html = generate_chat_list_html(JSON.parse(data));

            $(".panel-body").html(chat_list_html)
        }
    })
}

function post_data() {
    var msg = $('.form-input').val();
    if (msg === '') {
        alert('内容不能为空！');
        return
    }
    $.ajax({
        url: '/post_message',
        data: JSON.stringify({
            'nick': window.decodeURI(Cookies('name')),
            'msg': msg
        }),
        type: 'POST',
        contentType: 'application/json',
        dataType: 'json',
        success: function (data) {
            if (!data['success']) {
                alert(data['reason'])
            }
            else {
                $('.form-input').val('');
                refresh()
            }
        }
    })
}
$('#post').click(post_data);
refresh();
setInterval(refresh, 10000);
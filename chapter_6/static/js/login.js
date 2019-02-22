/**
 * Created by kingname on 2018/6/25.
 */
function login() {
    var nick = $('#nick').val();
    if (nick === '') {
        alert('昵称不能为空！');
        return
    }
    $.ajax({
        url: '/login',
        data: JSON.stringify({
            'nick': nick
        }),
        type: 'POST',
        contentType: 'application/json',
        dataType: 'json',
        success: function (data) {
            if (!data['success']) {
                alert(data['reason'])
            }
            else {
                window.location.replace('/room')
            }
        }
    })
}

$('#login').click(login);


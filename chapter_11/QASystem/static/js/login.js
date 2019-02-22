/**
 * Created by kingname on 2018/9/9.
 */
function log_in(){
    var user = $('#nick').val().trim();
    var password = $('#password').val().trim();
    if (user && password){
        $.ajax({
            type: "post",
            url: '/login',
            async: false, // 使用同步方式
            data: JSON.stringify({
                user: user,
                password: password
            }),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function(data) {
                if (data['success']){
                    window.location.href = '/'
                } else {
                    alert(data['reason'])
                }
            }
        });
    } else {
        alert('用户名和密码不能为空！')
    }
}


function register(){
    var user = $('#nick').val().trim();
    var password = $('#password').val().trim();
    if (user && password){
        $.ajax({
            type: "post",
            url: '/register',
            async: false, // 使用同步方式
            data: JSON.stringify({
                user: user,
                password: password
            }),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function(data) {
                if (data['success']){
                    window.location.href = '/'
                } else {
                    alert(data['reason'])
                }
            }
        });
    } else {
        alert('用户名和密码不能为空！');
    }
}

$('#login_button').click(log_in);
$('#register_button').click(register);
$('#login_or_register').click(function(){window.location.href = '/login'});
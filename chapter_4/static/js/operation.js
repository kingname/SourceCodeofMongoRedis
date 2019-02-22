/**
 * Created by kingname on 2018/6/25.
 */
function open_edit_info_modal() {
    $('#modal_edit_info').attr('class', 'modal active');
    var index = $(this).attr('rowindex').toString();
    $('#edit-id').attr('value', $('td[class="id"][rowindex="' + index + '"]').text());
    $('#edit-name').attr('value', $('td[class="name"][rowindex="' + index + '"]').text());
    $('#edit-age').attr('value', $('td[class="age"][rowindex="' + index + '"]').text());
    $('#edit-birthday').attr('value', $('td[class="birthday"][rowindex="' + index + '"]').text());
    $('#edit-origin-home').attr('value', $('td[class="origin-home"][rowindex="' + index + '"]').text());
    $('#edit-current-home').attr('value', $('td[class="current-home"][rowindex="' + index + '"]').text());
}

function close_edit_info_modal() {
    $('#modal_edit_info').attr('class', 'modal')
}

function open_add_info_modal() {
    $('#modal_add_info').attr('class', 'modal active')
}

function close_add_info_modal() {
    $('#modal_add_info').attr('class', 'modal')
}

function delete_people() {
    var url = '/delete/' + $(this).attr('rowIndex');
    console.log(url);
    $.ajax({
        url: url,
        success: function () {
            window.location.reload();
        }
    })
}

function post_info_to_add() {
    var name = $('#input-name').val();
    var age = $('#input-age').val();
    var birthday = $('#input-birthday').val();
    var origin_home = $('#input-origin-home').val();
    var current_home = $('#input-current-home').val();
    if (name.length <= 0) {
        alert('姓名不能为空')
        return
    }
    if (!birthday.match('\\d{4}-\\d{2}-\\d{2}')) {
        alert('生日的格式为：yyyy-mm-dd')
        return
    }
    age = parseInt(age);
    if (isNaN(age) || age < 0 || age > 120) {
        alert('年龄必需为一个范围在0-120之间数字。')
        return
    }
    $.ajax({
        url: '/add',
        data: JSON.stringify({
            'name': name, 'age': age, 'birthday': birthday,
            'origin_home': origin_home, 'current_home': current_home
        }),
        type: 'POST',
        contentType: 'application/json',
        dataType: 'json',
        success: function (data) {
            if (data['success']) {
                window.location.reload();
            }
        }
    })
}

function update_info() {
    var id = $('#edit-id').val();
    var name = $('#edit-name').val();
    var age = $('#edit-age').val();
    var birthday = $('#edit-birthday').val();
    var origin_home = $('#edit-origin-home').val();
    var current_home = $('#edit-current-home').val();
    if (name.length <= 0) {
        alert('姓名不能为空')
        return
    }
    if (!birthday.match('\\d{4}-\\d{2}-\\d{2}')) {
        alert('生日的格式为：yyyy-mm-dd')
        return
    }
    age = parseInt(age);
    if (isNaN(age) || age < 0 || age > 120) {
        alert('年龄必需为一个范围在0-120之间数字。')
        return
    }
    $.ajax({
        url: '/update',
        data: JSON.stringify({
            'people_id': id,
            'updated_info': {
                'name': name, 'age': age, 'birthday': birthday,
                'origin_home': origin_home, 'current_home': current_home
            }
        }),
        type: 'POST',
        contentType: 'application/json',
        dataType: 'json',
        success: function (data) {
            if (data['success']) {
                window.location.reload();
            } else {
                if ('reason' in data) {
                    alert(data['reason'])
                } else {
                    alert('更新失败')
                }
            }
        }
    })
}

function calc_age() {
    birthYear = parseInt(birthdayStr.split('-')[0]);
    if (birthYear === 2018) {
        return 1
    }
    thisYear = (new Date()).getFullYear();
    return thisYear - birthYear
}

function load() {
    $('button[name="edit_this_info"]').each(function () {
        $(this).click(open_edit_info_modal);
    });
    $('button[name="delete_this_info"]').each(function () {
        $(this).click(delete_people)
    });

    $('#close_edit_modal').click(close_edit_info_modal);
    $('#open_add_modal').click(open_add_info_modal);
    $('#close_add_modal').click(close_add_info_modal);
    $('#add_info').click(post_info_to_add);
    $('#update_info').click(update_info);
    $('#input-birthday').change(function () {
        birthdayStr = $(this).val();
        if (birthdayStr.match('\\d{4}-\\d{2}-\\d{2}')) {
            $('#input-age').val(calc_age())
        }
    });
    $('#edit-birthday').change(function () {
        birthdayStr = $(this).val();
        if (birthdayStr.match('\\d{4}-\\d{2}-\\d{2}')) {
            $('#edit-age').val(calc_age())
        }
    })
}

load();


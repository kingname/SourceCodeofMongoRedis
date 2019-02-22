/**
 * Created by kingname on 2018/9/2.
 */


function enable_ask_modal(){
    $('#ask-question-modal').attr('class', 'modal active')
}


function disable_ask_modal(){
    $('#ask-question-modal').attr('class', 'modal')
}

function enable_answer_modal() {
    $('#answer-question-modal').attr('class', 'modal active')
}

function disable_answer_modal() {
    $('#answer-question-modal').attr('class', 'modal')
}


function post_question() {
    title = $('#create_question_title').val().trim();
    detail = $('#create_question_detail').val().trim();
    if(title){
        $.ajax({
            type: "post",
            url: '/post_question',
            async: false, // 使用同步方式
            data: JSON.stringify({
                title: title,
                detail: detail,
                author: '匿名用户'
            }),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function(data) {
                console.log(data);
                doc_id = data['doc_id'];
                window.location.href = '/question/' + doc_id;
            }
        });
    } else {
        alert('标题不能为空！详情可以为空。')
    }
}


function post_answer(){
    answer = $('#answer').val().trim();
    if(answer){
        $.ajax({
            type: "post",
            url: '/post_answer',
            async: false, // 使用同步方式
            data: JSON.stringify({
                question_id: question_id,
                answer: answer,
                author: '匿名用户'
            }),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function(data) {
                console.log(data);
                window.location.reload()
            }
        });
    } else {
        alert('回答内容不能为空！')
    }
}


function vote(){
    doc_id = $(this).attr('doc_id');
    direction = $(this).attr('direction');
    doc_type = $(this).attr('doc_type');
    $.ajax({
            type: "post",
            url: '/vote',
            async: false, // 使用同步方式
            data: JSON.stringify({
                doc_id: doc_id,
                value: direction,
                doc_type: doc_type
            }),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function(data) {
                console.log(data);
                window.location.reload()
            }
        });

}

function change_question() {
    title = $("#question_title").text().trim();
    text = $('[name="my-question"]').map(function() {return $( this ).attr('value');}).get().join('\n');
    console.log(title, text);
    $('#update_question_detail').val(text);
    $('#update_question_title').val(title);

    $('#update-question-modal').attr('class', 'modal active');
}

function change_answer(){
    doc_id = $(this).attr('doc_id');
    text = $( '[name="my-answer"]' ).map(function() {return $( this ).attr('value');}).get().join( '\n' );

    $('#update-answer').val(text);
    $('#update-answer-modal').attr('class', 'modal active');
}

function post_changed_answer(){
    doc_id = $("[name='my-answer-div']").attr('doc_id');
    text = $('#update-answer').val();
    $.ajax({
            type: "post",
            url: '/update',
            async: false, // 使用同步方式
            data: JSON.stringify({
                doc_id: doc_id,
                text: text,
                update_type: 'answer'
            }),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function(data) {
                console.log(data);
                window.location.reload()
            }
        });
}

function post_changed_question(){
    doc_id = $("#question_text").attr('doc_id');
    title = $('#update_question_title').val();
    text = $('#update_question_detail').val();
    $.ajax({
            type: "post",
            url: '/update',
            async: false, // 使用同步方式
            data: JSON.stringify({
                doc_id: doc_id,
                text: text,
                title: title,
                update_type: 'question'
            }),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function(data) {
                console.log(data);
                window.location.reload()
            }
        });
}

$('#ask').click(enable_ask_modal);
$('#close-question-modal').click(disable_ask_modal);
$('#cancel-question').click(disable_ask_modal);
$('#open-answer-modal').click(enable_answer_modal);
$('#close-answer-modal').click(disable_answer_modal);
$('#cancel-answer-modal').click(disable_answer_modal);
$('#post-question').click(post_question);
$('#post-answer').click(post_answer);
$("[name='vote']").click(vote);
$("[name='change_question']").click(change_question);
$("[name='change_answer']").click(change_answer);
$('#cancel-update-answer-modal').click(function () {
    $('#update-answer-modal').attr('class', 'modal')
});

$('#close-update-answer-modal').click(function () {
    $('#update-answer-modal').attr('class', 'modal')
});

$('#post-update-answer').click(post_changed_answer);
$('#cancel-update-question').click(function () {$('#update-question-modal').attr('class', 'modal');
});
$('#close-update-question-modal').click(function () {$('#update-question-modal').attr('class', 'modal');
});
$('#post-update-question').click(post_changed_question);
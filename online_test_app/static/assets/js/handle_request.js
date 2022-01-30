

function handl_request(pagenum,qNum){
    var selected_option = "--Select--";
    try{
        selected_option = $("input[name='radio_btn']:checked").val();
        if(selected_option === undefined){
            selected_option = "--Select--";
        }
    }catch(e){
        console.log(e);
    }

    $.ajax({
    type: 'POST',
    url: '/exam/quiz/',
    data: { 
        'page':pagenum, 
        'answer':selected_option,
        'qNum':qNum
    },
    success:function(data,status){
        window.location.href= data;
    }
});

}


function clear_selection(current_page,qNum){
    $.ajax({
        type: 'POST',
        url: '/exam/quiz-clear/',
        data: { 
            'page':current_page,
            'qNum':qNum
        },
        success:function(data,status){
            window.location.href= data;
        }
    });

}
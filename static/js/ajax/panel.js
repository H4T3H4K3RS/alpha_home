var sURL = unescape(window.location.pathname);

function refresh()
{
    window.location.href = sURL;
}

function show_menu() {
    let menu = document.getElementById("menu");
    let menu_open = document.getElementById("menu_open");
    let menu_close = document.getElementById("menu_close");
    let main = document.getElementById("main");
    menu.style.display = 'block';
    menu_open.style.display = 'none';
    menu_close.style.display = 'block';
}


function close_menu(){
    let menu = document.getElementById("menu");
    let menu_open = document.getElementById("menu_open");
    let menu_close = document.getElementById("menu_close");
    let main = document.getElementById("main");
    menu.style.display = 'none';
    menu_open.style.display = 'block';
    menu_close.style.display = 'none';
}


function send_room_light(on, lamp_id) {
    let status = document.getElementById("status_"+lamp_id);
    let statusoff = document.getElementById("statusoff_"+lamp_id);
    let statuson = document.getElementById("statuson_"+lamp_id);
    if(parseInt(on) === 1){
        $.get("/lamp/room/"+ lamp_id + "/on/");
        status.innerText = "ВКЛЮЧЕНО";
        statuson.style.display = "none";
        statusoff.style.display = "inline";
    }
    else if(parseInt(on) === 2) {
        if (status.innerText === "ВКЛЮЧЕНО") {
            $.get("/lamp/room/" + lamp_id + "/off/");
            status.innerText = "ВЫКЛЮЧЕНО";
            statuson.style.display = "inline";
            statusoff.style.display = "none";
        }
        else {
            $.get("/lamp/room/"+ lamp_id + "/on/");
            status.innerText = "ВКЛЮЧЕНО";
            statuson.style.display = "none";
            statusoff.style.display = "inline";
        }
    }
    else{
        $.get("/lamp/room/" + lamp_id + "/off/");
        status.innerText = "ВЫКЛЮЧЕНО";
        statuson.style.display = "inline";
        statusoff.style.display = "none";
    }
}


function delete_room(room_id) {
    let room = document.getElementById("room_"+room_id);
    $.ajax({
        url: '/add/' + room_id.toString() + '/room/',
        type: 'GET',
        success: function(result) {
            show_notification("Комната будет окончательно удалена сразу после перезагрузки страницы.", 'success', 'bottom-right');
            setTimeout(refresh, 3000);
        },
        error: function(jqXHR, textStatus, errorThrown) {
            if(jqXHR.status === 404 || errorThrown === 'Not Found')
            {
                show_notification("Данной комнаты не существует.\n Перезагрузите страницу.", 'error', 'bottom-right');
                setTimeout(refresh, 3000);
            }
            else if(jqXHR.status === 403){
                show_notification("Доступ запрещён.", 'error', 'bottom-right');
            }
        }
    });
}


function add_room(home_id) {
    let send = {};
    let input1 = document.getElementById("input2_1");
    let input2 = document.getElementById("input2_2");
    send.name = input1.value;
    send.key = input2.value;
    let csrftoken = getCookie('csrftoken');
    $.ajax({
        beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        },
        url: '/add/' + home_id.toString() + '/room/',
        type: 'POST',
        contentType: 'application/json; charset=utf-8',
        data: JSON.stringify(send),
        dataType: 'text',
        success: function(result) {
            show_notification("Комната будет добавлена на панель сразу после перезагрузки страницы.", 'success', 'bottom-right');
            setTimeout(refresh, 3000);
        },
        error: function(jqXHR, textStatus, errorThrown) {
            if(jqXHR.status === 404 || errorThrown === 'Not Found')
            {
                show_notification("Внутренняя ошибка сервера.\n Перезагрузите страницу.", 'error', 'bottom-right');
                setTimeout(refresh, 3000);
            }
            else if(jqXHR.status === 403){
                show_notification("Неверный Ключ Активации.\n Повторите попытку.", 'error', 'bottom-right');
            }
        }
    });
}


function edit_house(home_id) {
    let send = {};
    let input1 = document.getElementById("input1_1");
    send.name = input1.value;
    let csrftoken = getCookie('csrftoken');
    $.ajax({
        beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        },
        url: '/edit/' + home_id.toString() + '/',
        type: 'POST',
        contentType: 'application/json; charset=utf-8',
        data: JSON.stringify(send),
        dataType: 'text',
        success: function(result) {
            show_notification("Изменения вступят в силу сразу после перезагрузки страницы.", 'success', 'bottom-right');
            setTimeout(refresh, 3000);
        },
        error: function(jqXHR, textStatus, errorThrown) {
            if(jqXHR.status === 404 || errorThrown === 'Not Found')
            {
                show_notification("Дом не найден.\n Перезагрузите страницу.", 'error', 'bottom-right');
                setTimeout(refresh, 3000);
            }
            else if(jqXHR.status === 403){
                show_notification("Доступ запрещён.", 'error', 'bottom-right');
            }
        }
    });
}


function edit_room(room_id) {
    let send = {};
    let input1 = document.getElementById("input1_1");
    send.name = input1.value;
    let csrftoken = getCookie('csrftoken');
    $.ajax({
        beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        },
        url: '/edit/room/' + room_id.toString() + '/',
        type: 'POST',
        contentType: 'application/json; charset=utf-8',
        data: JSON.stringify(send),
        dataType: 'text',
        success: function(result) {
            show_notification("Изменения вступят в силу сразу после перезагрузки страницы.", 'success', 'bottom-right');
            setTimeout(refresh, 3000);
        },
        error: function(jqXHR, textStatus, errorThrown) {
            if(jqXHR.status === 404 || errorThrown === 'Not Found')
            {
                show_notification("Комната не найдена.\n Перезагрузите страницу.", 'error', 'bottom-right');
                setTimeout(refresh, 3000);
            }
            else if(jqXHR.status === 403){
                show_notification("Доступ запрещён.", 'error', 'bottom-right');
            }
        }
    });
}


function modal_input_2_fields_setup(text, onclick, field1="", label1="", field2="", label2="", ok="Изменить", cancel="Отмена", ok_color="#0abf4c", ok_hover_color="#00ae44") {
    let modal_field1 = document.getElementById("input2_1");
    let modal_label1 = document.getElementById("label2_1");
    modal_label1.innerHTML = label1;
    modal_field1.setAttribute('placeholder', label1);
    modal_field1.setAttribute('value', field1);
    let modal_field2 = document.getElementById("input2_2");
    let modal_label2 = document.getElementById("label2_2");
    modal_label2.innerHTML = label2;
    modal_field2.setAttribute('placeholder', label2);
    modal_field2.setAttribute('value', field2);
    modal_field2.addEventListener("keyup", function(event) {
      // Number 13 is the "Enter" key on the keyboard
      if (event.keyCode === 13) {
        // Cancel the default action, if needed
        event.preventDefault();
        // Trigger the button element with a click
        document.getElementById("modal_input2_ok").click();
      }
    });
    let modal_text = document.getElementById("modal_input2_text");
    let modal_ok = document.getElementById("modal_input2_ok");
    modal_ok.style.backgroundColor = ok_color;
    let modal_cancel = document.getElementById("modal_input2_cancel");
    modal_ok.setAttribute("onclick", onclick);
    modal_ok.innerText = ok;
    modal_text.innerText = text;
    modal_cancel.innerText = cancel;
    $("#modal_input2_ok").hover(function(){
        $(this).css("background-color", ok_hover_color);
        }, function(){
        $(this).css("background-color", ok_color);
    });
}


function modal_input_1_fields_setup(text, onclick, field="", label="Имя", ok="Изменить", cancel="Отмена", ok_color="#0abf4c", ok_hover_color="#00ae44") {
    let modal_field = document.getElementById("input1_1");
    let modal_label = document.getElementById("label1_1");
    modal_label.innerHTML = label;
    modal_field.setAttribute('placeholder', label);
    modal_field.setAttribute('value', field);
    modal_field.addEventListener("keyup", function(event) {
      // Number 13 is the "Enter" key on the keyboard
      if (event.keyCode === 13) {
        // Cancel the default action, if needed
        event.preventDefault();
        // Trigger the button element with a click
        document.getElementById("modal_input1_ok").click();
      }
    });
    let modal_text = document.getElementById("modal_input1_text");
    let modal_ok = document.getElementById("modal_input1_ok");
    modal_ok.style.backgroundColor = ok_color;
    let modal_cancel = document.getElementById("modal_input1_cancel");
    modal_ok.setAttribute("onclick", onclick);
    modal_ok.innerText = ok;
    modal_text.innerText = text;
    modal_cancel.innerText = cancel;
    $("#modal_input1_ok").hover(function(){
        $(this).css("background-color", ok_hover_color);
        }, function(){
        $(this).css("background-color", ok_color);
    });
}


function modal_confirm_setup(text, onclick, ok="Удалить", cancel="Отмена") {
    let modal_text = document.getElementById("modal_confirm_text");
    let modal_ok = document.getElementById("modal_confirm_ok");
    let modal_cancel = document.getElementById("modal_confirm_cancel");
    modal_ok.setAttribute("onclick", onclick);
    modal_ok.innerText = ok;
    modal_text.innerText = text;
    modal_cancel.innerText = cancel;
}
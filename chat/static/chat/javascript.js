// # created with help of Django channels documentation: https://channels.readthedocs.io/en/latest/
document.addEventListener('DOMContentLoaded', function() {

    const roomName = JSON.parse(document.getElementById('room-name').textContent);

    function chat_scroll_down(){
        var roomChatContainer = document.getElementById("room_chat_container");
        roomChatContainer.style.overflowY = "hidden"
        roomChatContainer.scrollTop = roomChatContainer.scrollHeight;
        roomChatContainer.style.overflowY = "scroll"
    }
    chat_scroll_down();

    const chatSocket = new WebSocket(
        'ws://'
        + window.location.host
        + '/ws/chat/'
        + roomName
        + '/'
    );

    chatSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        user_auth = document.querySelector("#room_chat_container").dataset.user
        console.log(user_auth);

        //https://www.w3schools.com/js/js_htmldom_nodes.asp
        //username display 
        var p = document.createElement("p");
        var inner_text = document.createTextNode(data.username);
        p.appendChild(inner_text);
        p.style.fontWeight = "bold";
        p.style.marginBottom = 0;
        var element = document.getElementById("room_chat_container");
        element.appendChild(p);
        if (user_auth === data.username) {
            p.style.textAlign = "right";
        }
        else{
            p.style.textAlign = "left";
        }
        //text dispaly  
        var p = document.createElement("p");
        var inner_text = document.createTextNode(data.message);
        p.appendChild(inner_text);
        if (user_auth === data.username) {
            p.style.textAlign = "right";
        }
        else{
            p.style.textAlign = "left";
        }
        var element = document.getElementById("room_chat_container");
        element.appendChild(p); 
        chat_scroll_down();
    };

    chatSocket.onclose = function(e) {
        console.error('Chat socket closed unexpectedly');
    };

    document.querySelector('#chat-message-input').focus();
    document.querySelector('#chat-message-input').onkeyup = function(e) {
        if (e.key === 'Enter') {  // enter, return
            document.querySelector('#chat-message-submit').click();
        }
    };

    document.querySelector('#chat-message-submit').onclick = function(e) {
        const messageInputDom = document.querySelector('#chat-message-input');
        const message = messageInputDom.value;
        chatSocket.send(JSON.stringify({
            'message': message,
        }));
        messageInputDom.value = '';
    };

    document.querySelector("#room_add_member_form").onsubmit= function(event){
        event.preventDefault();

        let input = document.querySelector("#room_add_user");
        let new_member = input.value
        let room = input.dataset.room
        let path = input.dataset.path

        const csrftoken = Cookies.get('csrftoken');

        fetch(`${path}`, {
            method: 'POST',
            headers: {'X-CSRFToken': csrftoken},
            mode: 'same-origin',
            body: JSON.stringify({
                new_member:new_member,
                room:room
            })
        })
        .then(response => response.json())
        .then(result => {
            console.log(result);
             
            if (result["Message"] === "Success"){
                document.querySelector("#room_forloop_modal").innerHTML += 
                `<div class='d-flex justify-content-between'>
                    <p>${new_member}</p>
                    <i class='bi bi-trash3 room_bin_icon' data-user="${result["user_id"]}" data-path="${result["remove_path"]}" data-room="${result["room_name"]}"></i>
                </div>`;
            }
            document.querySelectorAll('.room_bin_icon').forEach(element => {
                element.addEventListener('click', event => remove_member(event));
            });
            document.querySelector("#room_add_user").value=""
            })
        .catch(() => {
            console.error("Failed to add member");
        });

        return false;
    };

    document.querySelectorAll('.room_bin_icon').forEach(element => {
        element.addEventListener('click', event => remove_member(event));
    });

    function remove_member(event){
        element = event.target
        user_id = element.dataset.user
        path = element.dataset.path
        room = element.dataset.room

        const csrftoken = Cookies.get('csrftoken');

        fetch(`${path}`, {
            method: 'POST',
            headers: {'X-CSRFToken': csrftoken},
            mode: 'same-origin',
            body: JSON.stringify({
                user_id:user_id,
                path:path,
                room:room
            })
        })
        .then(response => response.json())
        .then(result => {
            console.log(result);
           if (result["Message"] === "Success"){
            element.parentNode.remove();
            }
            })
        .catch(() => {
            console.error("Failed to remove member");
        });

        return false;

    }


});
var socket = io();
$(document).ready(function() {
    console.log("readyABC")
    // Connect to the Socket.IO server.
    // The connection URL has the following format, relative to the current page:
    //     http[s]://<domain>:<port>[/<namespace>]
    
    socket.on('connect', function() {
        ()=>console.log("connected")
        socket.emit('my_event', {data: 'I\'m connected!b4login'});
    });
})

AFRAME.registerComponent("login",{
    init:function(){
        var login_btn = document.getElementById("login_btn")  
        login_btn.addEventListener("click",function (){
            ()=>console.log("a")
            socket.emit('my_event',{data:'+886918622947'})
            socket.emit('connect_to_telegram', {data: '+886918622947'});
        })
        socket.on('my_response',function (msg){
            const spawnEl = document.createElement("a-entity");
        main_theme.appendChild(spawnEl);
        spawnEl.setAttribute("id", "profile");
        spawnEl.setAttribute("src", `#flower${i}`);
        spawnEl.setAttribute("position", { x: 0, y: 2, z: -2 });
        spawnEl.setAttribute("text",{msg})
        spawnEl.flushToDOM();
        })
        let keyboard = document.querySelector("a-keyboard");
keyboard.open();
keyboard.addEventListener('input', (e)=>{
  str += e.detail;
  console.log(str);
});
keyboard.addEventListener('enter', (e)=>{
  console.log("Enter key pressed!")
})
keyboard.addEventListener('dismiss', (e)=>{
  console.log("Dismiss: ", e);
  keyboard.dismiss();
});
keyboard.addEventListener('backspace', (e)=>{
  str = str.slice(0, -1);
  console.log(str);
});
    }

    
})
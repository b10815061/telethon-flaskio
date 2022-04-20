$(document).ready(function() {
    console.log("ready")
    // Connect to the Socket.IO server.
    // The connection URL has the following format, relative to the current page:
    //     http[s]://<domain>:<port>[/<namespace>]
    var socket = io();
    socket.on('connect', function() {
        ()=>console.log("connected")
        socket.emit('my_event', {data: 'I\'m connected! login'});
    });
})

AFRAME.registerComponent("main-theme", {
    init: function () {


    console.log("init")

      var z_dis = 5;
      var max_scale = 3.2;
  
      var mock_data_number = 30;
      var display_num = 10;
  
      var scaleUpbtn = document.getElementById("scaleUp");
      var scaleDownbtn = document.getElementById("scaleDown");
      var refetchbtn = document.getElementById("refetch");
      var profiles = document.querySelectorAll("#profile");    
  
      var main_theme = document.querySelector("a-scene");
  
      this.Resize = this.Resize.bind(this);
      this.ResizeEmit = this.ResizeEmit.bind(this);
  
      //console.log("main_theme", main_theme);
  
      for (let i = 0; i < 10; i++) {
        pos = compute_pos(3, 10, i);
        const spawnEl = document.createElement("a-curvedimage");
        main_theme.appendChild(spawnEl);
        spawnEl.setAttribute("id", "profile");
        spawnEl.setAttribute("src", `#flower${i}`);
        spawnEl.setAttribute("position", { x: pos.x, y: 2, z: pos.y });
        spawnEl.setAttribute("scale", { x: 1.4, y: 1.4, z: 1.4 });
        spawnEl.setAttribute("rotation",{x:0,y:140-36*i,z:0})
        spawnEl.setAttribute("radius", 1);
        spawnEl.setAttribute("theta-length", 90);
        
  
        spawnEl.addEventListener("resize", () =>{
          Vec = (spawnEl.getAttribute("position"));
          console.log(spawnEl)
          spawnEl.setAttribute("position", { x:Vec.x,y:2,z: Vec.z*z_dis })
          spawnEl.flushToDOM()
        });
  
        // this line is important
        spawnEl.flushToDOM();
        profiles = document.querySelectorAll("#profile")
        //console.log(spawnEl)
        //console.log("pos", spawnEl.attributes["position"]);
      }
  
      scaleDownbtn.addEventListener("click", function () {
        
        z_dis -= 0.2;
        for (let i = 0; i < profiles.length; i++) {
          profiles[i].emit("resize");
        }
      });
  
      scaleUpbtn.addEventListener("click", function () {
        if(z_dis<=1.6){
          z_dis += 0.2;
        }
        for (let i = 0; i < profiles.length; i++) {
          profiles[i].emit("resize");
        }
  
  
      });
  
      refetchbtn.addEventListener("click", () => {
        mock_data_number = 60;
      });
  
      /*for (let i = 0; i < profiles.length; i++) {
        profiles[i].addEventListener("resize", () => {
          if (scale < max_scale) {
            profiles[i].setAttribute("scale", { x: scale, y: scale, z: scale });
            profiles[i].flushToDOM();
          }
        });
      }*/
  
      this.backgroundEl = document.querySelector("#background");
  
      this.backgroundEl.addEventListener("click", function () {
        console.log("scaledown");
      });
  
      console.log(scaleDownbtn);
    },
  
    Resize: function (evt) {
      console.log(evt);
    },
    ResizeEmit: function () {
      var a = "A";
      console.log(a);
    },
  });
  
  function compute_pos(radius, total, index) {
  
    var angle = (((360 / total) * index )*Math.PI)/180;
  
    var target_x;
    var target_y;
  
    target_x =  radius * Math.sin(angle);
    target_y =  -radius * Math.cos(angle);
  
    return { x: target_x, y: target_y };
  }
  
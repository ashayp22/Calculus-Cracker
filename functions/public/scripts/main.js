function getCookie(cname) {
    var name = cname + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    for(var i = 0; i <ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}

function getData() {


    if(getCookie("uid") !== "") {
      clearCanvas();
      document.getElementById("welcomeText").innerHTML = "Welcome " + getCookie("name");
      document.getElementById("logoutBtn").style.display = "inline-block";
      document.getElementById("loginBtn").style.display = "none";

        $.ajax({
            url: '/loaddata',
            type: 'POST',
            data: {uid: getCookie("uid")},
            success: function (data) {
                if(data.error) {
                    logout();
                } else {
                    document.getElementById("previous").innerHTML = data.previous;
                }

            },
            error: function(err) {
                console.log(err);
            }
        });
    } else {
        gotosignin();
    }


}


function gotosignin() {
  window.location = "/signin";
}

function gotoportal() {
  window.location = "/portal";
}

function gotohome() {
  window.location = "/home";
}

function gotoresources() {
  window.location = "/resource";
}


function logout() {
    //delete cookie
    document.cookie = "uid=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
    document.cookie = "name=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";

    //go to login window

    window.location = "/";
}

function switchToButton() {
  document.getElementById("data4").style.display = "inline-block";
  document.getElementById("data2").style.display = "none";
}

function switchToDraw() {
  document.getElementById("data4").style.display = "none";
  document.getElementById("data2").style.display = "inline-block";
}

function showExtra() {
  var type = document.getElementById("type").value;
  if(type == "limit") {
    document.getElementById("bounds").style.display = "inline";
    document.getElementById("lower").style.display = "none";
    document.getElementById("upper").style.display = "none";
    document.getElementById("lowerText").style.display = "none";
    document.getElementById("upperText").style.display = "none";
    document.getElementById("boundsText").style.display = "inline";
    document.getElementById("lowerBtn").style.display = "none";
    document.getElementById("upperBtn").style.display = "none";
    document.getElementById("boundBtn").style.display = "inline";
  } else if (type == "derivative" || type == "integral") {
    document.getElementById("bounds").style.display = "none";
    document.getElementById("lower").style.display = "none";
    document.getElementById("upper").style.display = "none";
    document.getElementById("lowerText").style.display = "none";
    document.getElementById("upperText").style.display = "none";
    document.getElementById("boundsText").style.display = "none";
    document.getElementById("lowerBtn").style.display = "none";
    document.getElementById("upperBtn").style.display = "none";
    document.getElementById("boundBtn").style.display = "none";
  } else if (type == "definite integral" || type == "summation" || type == "product") {
    document.getElementById("lower").style.display = "inline";
    document.getElementById("upper").style.display = "inline";
    document.getElementById("bounds").style.display = "none";
    document.getElementById("lowerText").style.display = "inline";
    document.getElementById("upperText").style.display = "inline";
    document.getElementById("boundsText").style.display = "none";
    document.getElementById("lowerBtn").style.display = "inline";
    document.getElementById("upperBtn").style.display = "inline";
    document.getElementById("boundBtn").style.display = "none";
  }
}

function deleteEquation() {
  var s = document.getElementById("equation").value;
  document.getElementById("equation").value = s.substring(0, s.length-1);

}

function clearEquation() {
  document.getElementById("equation").value = "";
}

function addToEquation(char) {
  document.getElementById("equation").value += char;
}

function calculate() {
    var equation = document.getElementById("equation").value;
    var type = document.getElementById("type").value;
    var bounds = document.getElementById("bounds").value;

    var lower = document.getElementById("lower").value;
    var upper = document.getElementById("upper").value;

    if(equation == "" || (type == "limit" && bounds == "") || ((type == "definite integral" || type == "summation" || type == "product") && (lower == "" || upper == ""))) {
      document.getElementById("error").innerHTML = "you are missing some data";
      return;
    }

    lower = lower.replace(/π/g, "pi");
    lower = lower.replace(/e/g, "E");

    upper = upper.replace(/π/g, "pi");
    upper = upper.replace(/e/g, "E");

    bounds = bounds.replace(/π/g, "pi");
    bounds = bounds.replace(/e/g, "E");
    bounds = bounds.replace(/√/g, "sqrt");


    if(type == "definite integral" || type == "summation" || type == "product") {
      bounds = lower + "," + upper;
    }


    //format equation
    equation = equation.replace(/π/g, "p");
    equation = equation.replace(/×/g, "*");
    equation = equation.replace(/arc/g, "a");

    //for e, make sure there is no sec

    for(i = 0; i < equation.length; i++) {
      if(i == 0 || i == equation.length - 1) {
        if(equation.substring(i, i+1) == "e") {
          equation = equation.substring(0, i) + "E" + equation.substring(i+1, equation.length);
        }
      } else {
          if(equation.substring(i, i+1) == "e") {
            if(equation.substring(i-1,i) != "s" && equation.substring(i+1,i+2) != "c") {
              equation = equation.substring(0, i) + "E" + equation.substring(i+1, equation.length);
            }
          }
      }
    }


    console.log(equation);

    document.getElementById("error").innerHTML = "Calculating, please wait...";
    document.getElementById("overlay").style.display = "inline-block";

    $.ajax({
        url: '/calc',
        type: 'POST',
        data: {equation: equation, type: type, bounds: bounds, uid: getCookie("uid")},
        success: function (data) {
            if(data.error) {
                document.getElementById("error").innerHTML = data.message;
            } else {
                document.getElementById("answer").innerHTML = "Answer: " + data.answer;
                document.getElementById("previous").innerHTML = data.previous;
                document.getElementById("error").innerHTML = "";
                document.getElementById("equation").value = "";
                document.getElementById("bounds").value = "";
                document.getElementById("lower").value = "";
                document.getElementById("upper").value = "";
                document.getElementById("overlay").style.display = "none";

            }
        },
        error: function(err) {
            console.log(err);
        }
    });
}


function clearSaved() {
    $.ajax({
        url: '/clear',
        type: 'POST',
        data: {uid: getCookie("uid")},
        success: function () {
            getData();
        },
        error: function(err) {
            console.log(err);
        }
    });
}

function updatePen() {
  var val = document.getElementById("pen").value;
  if(val == "pencil") {
    eraser = false;
  } else if (val == "eraser") {
    eraser = true;
  }
}

var clickX = [];
var clickY = [];
var clickDrag = [];
var paint;

var eraser = false;

function addClick(x, y, dragging)
{
    clickX.push(x);
    clickY.push(y);
    clickDrag.push(dragging);
}
$(document).ready(function() {
    $('#canvas').mousedown(function(e){
        console.log("yes");
        var mouseX = e.pageX - this.offsetLeft;
        var mouseY = e.pageY - this.offsetTop;

        paint = true;
        addClick(e.pageX - this.offsetLeft, e.pageY - this.offsetTop);
        redraw();
    });

    $('#canvas').mousemove(function(e){
        // console.log("moved");
        if(paint){

            if(eraser) {
              erase(e.pageX - this.offsetLeft, e.pageY - this.offsetTop);
            } else {
              addClick(e.pageX - this.offsetLeft, e.pageY - this.offsetTop, true);
              redraw();
            }

        }
    });

    $('#canvas').mouseup(function(e){
        paint = false;
    });

    $('#canvas').mouseleave(function(e){
        paint = false;
    });

});

function erase(x, y) {
  var canvas = document.getElementById("canvas");
  var ctx = canvas.getContext("2d");

  ctx.fillStyle = "#ffffff";

  ctx.beginPath();
  ctx.arc(x, y, 20, 0, 2 * Math.PI);
  ctx.fill();
}

function redraw(){

    var canvas = document.getElementById("canvas");
    var ctx = canvas.getContext("2d");

    // ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height); // Clears the canvas
    //
    // ctx.fillStyle = "#ffffff";
    // ctx.fillRect(0, 0, canvas.width, canvas.height);

    ctx.strokeStyle = "#000000";
    ctx.lineJoin = "round";
    ctx.lineWidth = 5;

    for(var i=clickX.length - 1; i < clickX.length; i++) {
        ctx.beginPath();
        if(clickDrag[i] && i){
            ctx.moveTo(clickX[i-1], clickY[i-1]);
        }else{
            ctx.moveTo(clickX[i]-1, clickY[i]);
        }
        ctx.lineTo(clickX[i], clickY[i]);
        ctx.closePath();
        ctx.stroke();
    }
}

function updateEquation() { //updates the equation
  var canvas = document.getElementById("canvas");
  var image =  canvas.toDataURL("image/png");
  // $("#img").attr('src', image);

  var data = new FormData();
  data.append("img", image);
  data.append("name", "yeet");

  var object = {};
  data.forEach(function(value, key){
      object[key] = value;
  });
  let json = JSON.stringify(object);

  document.getElementById("data2p").innerHTML = "Adding, please wait..."
  document.getElementById("overlay").style.display = "inline-block";

  $.ajax({
      url: '/ml',
      type: 'POST',
      data: json,
      processData: false,
      contentType: false,
      success: function (data) {
          // alert("success");
          if(data.error) {
              document.getElementById("error").innerHTML = data.message;
          } else {
            document.getElementById("error").innerHTML = "";
            document.getElementById("equation").value += data.character;
            document.getElementById("data2p").innerHTML = "Only use the variables v, w, or z";
            document.getElementById("overlay").style.display = "none";

            clearCanvas();
          }
      },
      error: function(err) {
        document.getElementById("error").innerHTML = "there has been an error, please try again";
        document.getElementById("overlay").style.display = "none";
      }
  });
}

function updateBound() { //updates the bound for a limit
  var canvas = document.getElementById("canvas");
  var image =  canvas.toDataURL("image/png");
  // $("#img").attr('src', image);

  var data = new FormData();
  data.append("img", image);
  data.append("name", "yeet");

  var object = {};
  data.forEach(function(value, key){
      object[key] = value;
  });
  let json = JSON.stringify(object);

  document.getElementById("data2p").innerHTML = "Adding, please wait..."
  document.getElementById("overlay").style.display = "inline-block";


  $.ajax({
      url: '/ml',
      type: 'POST',
      data: json,
      processData: false,
      contentType: false,
      success: function (data) {
          // alert("success");
          if(data.error) {
              document.getElementById("error").innerHTML = data.message;
          } else {
            document.getElementById("error").innerHTML = "";
            document.getElementById("bounds").value += data.character;
            document.getElementById("data2p").innerHTML = "Only use the variables v, w, or z";
            document.getElementById("overlay").style.display = "none";

            clearCanvas();
          }
      },
      error: function(err) {
          console.log(err);
          document.getElementById("error").innerHTML = "there has been an error, please try again";
          document.getElementById("overlay").style.display = "none";
      }
  });
}

function updateLower() {
  var canvas = document.getElementById("canvas");
  var image =  canvas.toDataURL("image/png");
  // $("#img").attr('src', image);

  var data = new FormData();
  data.append("img", image);
  data.append("name", "yeet");

  var object = {};
  data.forEach(function(value, key){
      object[key] = value;
  });
  let json = JSON.stringify(object);

  document.getElementById("data2p").innerHTML = "Adding, please wait..."
  document.getElementById("overlay").style.display = "inline-block";


  $.ajax({
      url: '/ml',
      type: 'POST',
      data: json,
      processData: false,
      contentType: false,
      success: function (data) {
          // alert("success");
          if(data.error) {
              document.getElementById("error").innerHTML = data.message;
          } else {
            document.getElementById("error").innerHTML = "";
            document.getElementById("lower").value += data.character;
            document.getElementById("data2p").innerHTML = "Only use the variables v, w, or z";
            document.getElementById("overlay").style.display = "none";

            clearCanvas();
          }
      },
      error: function(err) {
        document.getElementById("error").innerHTML = "there has been an error, please try again";
        document.getElementById("overlay").style.display = "none";
      }
  });
}

function updateUpper() {
  var canvas = document.getElementById("canvas");
  var image =  canvas.toDataURL("image/png");
  // $("#img").attr('src', image);

  var data = new FormData();
  data.append("img", image);
  data.append("name", "yeet");

  var object = {};
  data.forEach(function(value, key){
      object[key] = value;
  });
  let json = JSON.stringify(object);

  document.getElementById("data2p").innerHTML = "Adding, please wait...";
  document.getElementById("overlay").style.display = "inline-block";


  $.ajax({
      url: '/ml',
      type: 'POST',
      data: json,
      processData: false,
      contentType: false,
      success: function (data) {
          // alert("success");
          if(data.error) {
              document.getElementById("error").innerHTML = data.message;
          } else {
            document.getElementById("error").innerHTML = "";
            document.getElementById("upper").value += data.character;
            document.getElementById("data2p").innerHTML = "Only use the variables v, w, or z";
            document.getElementById("overlay").style.display = "none";

            clearCanvas();
          }
      },
      error: function(err) {
        document.getElementById("error").innerHTML = "there has been an error, please try again";
        document.getElementById("overlay").style.display = "none";
      }
  });
}

function clearCanvas() {
    var canvas = document.getElementById("canvas");
    var ctx = canvas.getContext("2d");

    clickX = [];
    clickY = [];
    clickDrag = [];
    paint;

    ctx.fillStyle = "#ffffff";
    ctx.fillRect(0, 0, canvas.width, canvas.height);
}

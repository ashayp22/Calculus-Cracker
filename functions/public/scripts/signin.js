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

document.addEventListener("DOMContentLoaded", event => {
    if(getCookie("uid") !== "") {
        window.location = "/portal";
    }
});




function login() {

    var email = document.getElementById("email").value;
    var password = document.getElementById("password").value;


    $.ajax({
            url: '/login',
            type: 'POST',
            data: {email: email, password: password},
            success: function (data) {
                if(data.worked) {
                    //create cookie
                    document.cookie = "uid=" + data.uid;
                    document.cookie = "name=" + data.name;
                    window.location = "/portal";
                } else {
                    document.getElementById("message").innerHTML = data.message;
                }
            },
            error: function(err) {
                console.log(err);
            }
        });

}

function gotosignup() {
    window.location = "/signing";
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

function setup() {
  console.log(getCookie("uid"));
  if(getCookie("uid") !== "") {
    gotoportal();
  }
}


// function googleLogin() {
//     const provider = new firebase.auth.GoogleAuthProvider();
//
//     firebase.auth().signInWithPopup(provider).then(result => {
//         const user = result.user;
//         const token = googleUser.getAuthResponse().id_token;
//
//
//
//         // alert(token);
//
//         // $.ajax({
//         //     url: '/login',
//         //     type: 'post',
//         //     data: {credential: token},
//         //     success: function (data) {
//         //         alert("worked");
//         //     },
//         //     error: function(err) {
//         //         alert("error");
//         //     }
//         // });
//
//     }).catch(function(error) {
//         // Handle Errors here.
//         var errorCode = error.code;
//         var errorMessage = error.message;
//         console.log(errorCode);
//         // ...
//     });
// }

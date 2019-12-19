
function signup() {

    var email = document.getElementById("email").value;
    var password = document.getElementById("password").value;
    var name = document.getElementById("name").value;

    $.ajax({
        url: '/signup',
        type: 'POST',
        data: {email: email, password: password, name: name},
        success: function (data) {
            if(data.worked) {
                // alert(data.uid);
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

function gotoresources() {
  window.location = "/resource";
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

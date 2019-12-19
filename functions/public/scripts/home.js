function gotosignin() {
  window.location = "/signin";
}

function gotoportal() {
  window.location = "/portal";
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

function start() {
  if(getCookie("uid") != "") {
    document.getElementById("welcomeText").innerHTML = "Welcome " + getCookie("name");
    document.getElementById("logoutBtn").style.display = "inline-block";
    document.getElementById("loginBtn").style.display = "none";

  }
}

function logout() {
    //delete cookie
    document.cookie = "uid=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
    document.cookie = "name=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";

    //go to login window

    window.location = "/";
}

function showform(){
    var x = document.getElementById("register");
    var y = document.getElementById("login");
    var btn = document.getElementById("btn");
    if (x.style.display === "none") {
        x.style.display = "block";
        y.style.display = "none";
        btn.innerHTML = "Login";
    } else {
        x.style.display = "none";
        y.style.display = "block";
        btn.innerHTML = "Register";
    }
}
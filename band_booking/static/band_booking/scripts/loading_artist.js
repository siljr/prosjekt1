function loadingAnimation(){
    var animationElement = document.getElementById("loading_information_animation_dots");
    var numberOfDots = (animationElement.textContent.length + 1)%4;
    animationElement.textContent = ".".repeat(numberOfDots);
}

function loadEvents(){
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200){
            document.getElementById("events-list").innerHTML = this.responseText;
            window.clearInterval(animationInterval);
        } else if (this.readyState == 4) {
            window.clearInterval(animationInterval);
        }
    };

    xhttp.open("GET", "/event_information/" + artist_name, true);
    xhttp.send();
}

var animationInterval = window.setInterval(loadingAnimation, 500);


var artist_name = document.getElementById("artist").innerHTML;

var xhttp = new XMLHttpRequest();
xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200){
        window.document.getElementById("content").innerHTML = this.responseText;
        loadEvents();
    } else if (this.readyState == 4) {
        window.document.getElementById("loading_information").innerHTML = "Det oppstod et problem ved lasting av informasjon om " + artist_name + ". Prøv å oppdatere siden.";
        window.clearInterval(animationInterval);
    }
};

xhttp.open("GET", "/get_artist/" + artist_name, true);
xhttp.send();

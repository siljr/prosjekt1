function loadingAnimation(){
    var animationElement = document.getElementById("loading_information_animation_dots")
    var numberOfDots = (animationElement.textContent.length + 1)%4;
    animationElement.textContent = ".".repeat(numberOfDots);
}

var animationInterval = window.setInterval(loadingAnimation, 500);


var artist_name = document.getElementById("artist").innerHTML;

var xhttp = new XMLHttpRequest();
xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200){
        window.document.documentElement.innerHTML = this.responseText;
    } else if (this.readyState == 4) {
        window.document.getElementById("loading_information").innerHTML = "Ran into a problem while loading the information about " + artist_name + ". Please try refreshing the page, if that does not work contact the system administrator.";
    }
};

xhttp.open("GET", "/get_artist/" + artist_name, true);
xhttp.send();

function hideOnClick(elementId){
    var element = document.getElementById(elementId);

    if (element != null){
        element.addEventListener("click", function(){
            element.style.display = "none";
        })
    }
}

window.onload = function(){
    hideOnClick("error-message");
};

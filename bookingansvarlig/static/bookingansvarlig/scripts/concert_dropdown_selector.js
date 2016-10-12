function addEventListeners(className, inputFieldToChange){
    var elements = document.getElementsByClassName(className);
    for (var index = 0; index < elements.length; index++){
        elements[index].addEventListener("click", function(){
            if (this.classList.contains("dropdown-currently-selected-item")){
                inputFieldToChange.value = "";
            } else {
                inputFieldToChange.value = this.innerHTML;
            }
            document.getElementById("concert_filters").submit();
        });
    }
}

window.onload = function(){
    addEventListeners("scene-item", document.getElementById("scene_selector"));
    addEventListeners("genre-item", document.getElementById("genre_selector"));
};
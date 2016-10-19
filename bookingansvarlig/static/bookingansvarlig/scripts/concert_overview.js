function hideOnClick(elementId){
    var element = document.getElementById(elementId);

    if (element != null){
        element.addEventListener("click", function(){
            element.style.display = "none";
        })
    }
}

function addEventListeners(className, inputFieldToChange){
    var elements = document.getElementsByClassName(className);
    for (var index = 0; index < elements.length; index++){
        elements[index].addEventListener("click", function(){
            var select = this.classList.contains("dropdown-currently-selected-item");
            for (var index = 0; index < elements.length; index++){
                elements[index].classList.remove("dropdown-currently-selected-item");
            }
            if (select){
                inputFieldToChange.value = "";
                document.getElementById("currently-selected-scene").innerText = "Ingen valgt";
            } else {
                inputFieldToChange.value = this.innerHTML;
                document.getElementById("currently-selected-scene").innerText = this.innerText;
                this.classList.add("dropdown-currently-selected-item");
            }
        });
    }
}

function checkInput(){
    var scene_element = document.getElementById("scene_selector");
    if (scene_element.value == ""){
        alert("Scene ikke valgt!");
        return false;
    }
    var dato_element = document.getElementById("date_selector");
    if (!dato_element.value.match(new RegExp("^[0-9]{4}-(0[1-9]|1[0-2])-([0-2][0-9]|3[0-1])$"))){
        alert("Dato format er feil! Må være 'yyyy-mm-dd' hvor yyyy er årstallet, mm er måneden og dd er dagen");
        return false;
    }

    if (dato_element.innerText != "" && !dato_element.innerText.match(new RegExp("^[0-9]{4}-(0[1-9]|1[0-2])-([0-2][0-9]|3[0-1])$"))){
        alert("Dato format er feil! Må være 'yyyy-mm-dd' hvor yyyy er årstallet, mm er måneden og dd er dagen");
        return false;
    }
    return true;
}

window.onload = function(){
    hideOnClick("saved-message");
    hideOnClick("offer-status-message");
    hideOnClick("error-message");
    addEventListeners("scene-item", document.getElementById("scene_selector"));
};

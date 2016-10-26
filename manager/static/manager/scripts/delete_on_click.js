window.onload = function() {
	var elements = document.getElementsByClassName("equipment-add-delete-button");
	for(index = 0; index < elements.length; index++){
		var element = elements[index];
		element.addEventListener("click", function(){
            var childs = this.parentNode.childNodes;
            console.log(childs)
            if (childs[3].value == 0) {
				childs[3].value = "1";
				this.innerHTML = "Omgjør sletting";
				childs[1].setAttribute("readonly", "");
                childs[2].setAttribute("readonly", "");
			} else {
				childs[3].value = "0";
				this.innerHTML = "Slett utstyr";
                childs[1].removeAttribute("readonly");
                childs[2].removeAttribute("readonly");
			}
		});
	}
};
window.onload = function() {
	var elements = document.getElementsByClassName("equipment-add-delete-button");
	for(index = 0; index < elements.length; index++){
		var element = elements.get(index);
		element.addEventListener("onclick", function()){
			var deleteInput = parent.childNodes.get(2);
			if (deleteInput.value == "0") {
				deleteInput.value = "1";
				this.innerHTML = "Omgjør sletting";
				parent.childNodes.get(0).setAttribute("disabled", "true");
				parent.childNodes.get(1).setAttribute("disabled", "true");
			} else {
				deleteInput.value = "0";
				this.innerHTML = "Slett utstyr";
				parent.childNodes.get(0).removeAttribute("disabled");
				parent.childNodes.get(1).removeAttribute("disabled");
			}
		}
	}
};
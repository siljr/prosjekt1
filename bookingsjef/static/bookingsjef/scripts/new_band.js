window.onload = function() {
    document.getElementById("create_new_band").addEventListener("click", function(){
        var accepted = window.confirm("Du holder på å forlate siden, arbeidet vil bli tapt!");
        if (accepted) {
            var form = document.createElement("form");
            form.setAttribute("method", "post");
            form.setAttribute("action", "/booking/create/band/");

            var url_field = document.createElement("input");
            url_field.setAttribute("type", "text");
            url_field.setAttribute("name", "url");
            url_field.setAttribute("value", window.location.href);

            form.appendChild(document.getElementsByName("csrfmiddlewaretoken")[0]);
            form.appendChild(url_field);

            form.submit()
        }
    })
};
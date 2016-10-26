window.onload = function () {
    var dismiss_button = document.getElementById('dismiss_message_button');
    if (dismiss_button != null){
        dismiss_button.addEventListener("click", function(){
            document.getElementById('login_error').style.display = 'none';
        });
    }
    document.getElementById("username").focus();
};
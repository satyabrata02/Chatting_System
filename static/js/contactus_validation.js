function validation(){
    var firstname = document.getElementById('firstname').value.trim();
    var lastname = document.getElementById('lastname').value.trim();
    var phoneno = document.getElementById('phoneno').value.trim();
    var emailid = document.getElementById('emailid').value.trim();
    var messages = document.getElementById('messages').value.trim();

    if (firstname === "") {
        document.getElementById('error').innerHTML = "First name is empty.";
        document.getElementById('firstname').focus();
        return false;
    }

    if (lastname === "") {
        document.getElementById('error2').innerHTML = "Last name is empty.";
        document.getElementById('lastname').focus();
        return false;
    }
    
    if (emailid === "") {
        document.getElementById('error4').innerHTML = "Email is empty.";
        document.getElementById('emailid').focus();
        return false;
    }
    
    if (phoneno.length <= 9) {
        document.getElementById('error3').innerHTML = "Phone number must be a 10-digit number";
        document.getElementById('phoneno').focus();
        return false;
    }
    
    if (messages === "") {
        document.getElementById('msg').innerHTML = "Write some message";
        document.getElementById('messages').focus();
        return false;
    }

    return true;
}

function numbersonly(e){
    var unicode=e.charCode? e.charCode : e.keyCode;
    if (unicode !== 8){
        if (unicode<48||unicode>57)
            return false;
    }
}
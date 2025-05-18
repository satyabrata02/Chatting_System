function validation() {
    var letter = /^[A-Za-z\s]*$/;
    var letters = /^[A-Za-z]+$/; 
    var reg = /^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,5})$/;
    var firstname = document.getElementById('firstname').value.trim();
    var lastname = document.getElementById('lastname').value.trim();
    var phoneno = document.getElementById('phoneno').value.trim();
    var emailid = document.getElementById('emailid').value.trim();
    var password = document.getElementById('password').value.trim();
    var questionInputs = document.querySelectorAll('input[name="secure_question"]:checked');
    var genderInputs = document.querySelectorAll('input[name="gender"]:checked');

    if (!firstname.match(letter)) {
        document.getElementById('error').innerHTML = "First name should only contain letters and spaces";
        document.getElementById('firstname').focus();
        return false;
    }

    if (!lastname.match(letters)) {
        document.getElementById('error2').innerHTML = "Last name should only contain letters";
        document.getElementById('lastname').focus();
        return false;
    }

    if (phoneno.length !== 10 || isNaN(phoneno)) {
        document.getElementById('error3').innerHTML = "Phone number must be a 10-digit number";
        document.getElementById('phoneno').focus();
        return false;
    }

    if (!emailid.match(reg)) {
        document.getElementById('error4').innerHTML = "Enter a valid email address";
        document.getElementById('emailid').focus();
        return false;
    }

    if (password.length <= 7 || password.length >= 16) {
        document.getElementById('error5').innerHTML = "Password must be 8 to 15 character";
        document.getElementById('password').focus();
        return false;
    }

    if (questionInputs.length === 0) {
        alert("Please select your option");
        return false;
    }

    if (genderInputs.length === 0) {
        alert("Please select your gender");
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
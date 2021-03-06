/*accessing the buttons and message divs*/
var navSignin = document.getElementById('navSignin');
var navSignout = document.getElementById('navSignout');
var dropdown = document.getElementById('dropdown');

var snavSignin = document.getElementById('snavSignin');
var snavSignout = document.getElementById('snavSignout');

var successMsg = document.getElementById('success-msg');
var errorMsg = document.getElementById('error-msg');

var successMsgIn = document.getElementById('success-msg-in');
var errorMsgIn = document.getElementById('error-msg-in');

var snackbar = document.getElementById('snackbar');

/*initially hide signin/out buttons*/
navSignin.style.display='none';
dropdown.style.display='none';
snavSignin.style.display='none';
//snavSignout.style.display='none';

/*check if user is logged in and then show button*/
window.onload = function(){
    $.ajax({
        url: '/loggedin',
        type: 'POST',
        success: function(response) {
            if (response.status==true) {
                console.log('user logged in');
                navSignin.style.display='none';
                dropdown.style.display='block';
                navSignout.style.display='block';
                snavSignin.style.display='none';
                snavSignout.style.display='block';
            }else{
                onError(response.message)
            }
        },
        error: function(error) {
            onError(error);
        }
    });
    function onError(error){
        console.log('user not logged in');
        navSignin.style.display='block';
        dropdown.style.display='none';
        navSignout.style.display='none';
        snavSignin.style.display='block';
        snavSignout.style.display='none';
    };
    //flashShow();
};

// Modal Image Gallery
function onClick(element) {
  document.getElementById("img01").src = element.src;
  document.getElementById("modal01").style.display = "block";
  var captionText = document.getElementById("caption");
  captionText.innerHTML = element.alt;
}

//snackbar display function
function snackbarShow() {
    // Get the snackbar DIV
    var x = document.getElementById("snackbar")

    // Add the "show" class to DIV
    x.className = "show";

    // After 3 seconds, remove the show class from DIV
    setTimeout(function(){ x.className = x.className.replace("show", ""); }, 3000);
}

//flash message display function
function flashShow() {
    console.log("snacking!")
    // Get the flash DIV
    $('.flash').each(function() {
        // Add the "show" class to DIV
        $( this ).addClass("show");

        // After 3 seconds, remove the show class from DIV
        setTimeout(function(){ $( this ).removeClass("show"); }, 3000);
    });
}

//clear all input fields on modal close
function signupClose(){
    document.getElementById('id02').style.display='none';
    document.getElementById('uname').value='';
    document.getElementById('pwd').value='';
    document.getElementById('cpwd').value='';
    errorMsg.style.display='none';
    successMsg.style.display='none';
}

// Used to toggle the menu on small screens when clicking on the menu button
function toggleFunction() {
    var x = document.getElementById("navDemo");
    if (x.className.indexOf("w3-show") == -1) {
        x.className += " w3-show";
    } else {
        x.className = x.className.replace(" w3-show", "");
    }
}
// Get the modal
var modal = document.getElementById('id01');
	// When the user clicks anywhere outside of the modal close it
	window.onclick = function(event) {
	if (event.target == modal) {
		modal.style.display = "none";
	}
}
function validateSignUp() {
    var username = document.getElementById("uname").value;
    var password = document.getElementById("pwd").value;
    var confirm = document.getElementById("cpwd").value;
    errorMsg.innerHTML="";
    if (username == "") {
        errorMsg.innerHTML="Username field is empty";
        return false;
    }
    if(password==""){
        errorMsg.innerHTML = errorMsg.innerHTML + "&#13;&#10;"+"Password field is empty";
        return false;
    }
    if(password!=confirm || confirm==""){
        errorMsg.innerHTML = errorMsg.innerHTML + "&#13;&#10;" + "Password and confirm password do not match";
        return false;
    }
    return true;
}
function validateSignIn() {
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;
    errorMsgIn.innerHTML="";
    if (username == "") {
        errorMsgIn.innerHTML="Username field is empty";
        return false;
    }
    if(password==""){
        errorMsgIn.innerHTML = errorMsg.innerHTML + "&#13;&#10;"+"Password field is empty";
        return false;
    }
    return true;
}
//on sign out
function SignOut(){
    /* clear session */
    $.ajax({
        url: '/logout',
        type: 'POST',
        success: function(response) {
            if (response.status==true) {
                dropdown.style.display='none'
                navSignin.style.display='block';
                navSignout.style.display='none';
                snavSignin.style.display='block';
                snavSignout.style.display='none';
                snackbar.innerHTML ="User logged out!";
                snackbarShow();
                window.location='/';
            }else{
                onError(response.message)
            }
        },
        error: function(error) {
            onError(error);
        }
    });
    function onError(error){
        navSignin.style.display='block';
        navSignout.style.display='none';
        snavSignin.style.display='block';
        snavSignout.style.display='none';
        snackbar.innerHTML ="Error: "+ error +". Try again!";
        snackbarShow();
    };
}
//on sign in
function SignIn(){
    /* New session */
    if (validateSignIn()){
        errorMsgIn.style.display='none';
        successMsgIn.style.display='block';
        successMsgIn.innerHTML="Waiting...";


        $.ajax({
            url: '/login',
            data: $('#signinform').serialize(),
            type: 'POST',
            success: function(response) {
                if (response.status==true) {
                    console.log(response);
                    document.getElementById('id01').style.display='none';
                    navSignin.style.display='none';
                    navSignout.style.display='block';
                    snavSignin.style.display='none';
                    snavSignout.style.display='block';
                    snackbar.innerHTML = "User Logged In !";
                    snackbarShow();
                }else{
                    onError(response.message)
                }
            },
            error: function(error) {
                onError(error);
            }
        });
        function onError(error){
            console.log(error);
            successMsgIn.style.display='none';
            errorMsgIn.style.display='block';
            navSignin.style.display='block';
            navSignout.style.display='none';
            snavSignin.style.display='block';
            snavSignout.style.display='none';
            errorMsgIn.innerHTML ="Error: "+ error;
        };
    }
    else{
        errorMsgIn.style.display='block';
    }
};

//on sign up
function SignUp(){
    /* New session */
    if (validateSignUp()){
        errorMsg.style.display='none';
        successMsg.style.display='block';
        successMsg.innerHTML="Waiting...";

        $.ajax({
            url: '/register',
            data: $('#signupform').serialize(),
            type: 'POST',
            success: function(response) {
                if (response.status==true) {
                    document.getElementById('id02').style.display='none';
                    navSignin.style.display='none';
                    navSignout.style.display='block';
                    snavSignin.style.display='none';
                    snavSignout.style.display='block';
                    snackbar.innerHTML ="User created successfully!";
                    snackbarShow();
                }else{
                    onError(response.message)
                }
            },
            error: function(error) {
                onError(error);
            }
        });
        function onError(error){
            successMsg.style.display='none';
            errorMsg.style.display='block';
            navSignin.style.display='block';
            navSignout.style.display='none';
            snavSignin.style.display='block';
            snavSignout.style.display='none';
            errorMsg.innerHTML ="Error: "+ error +". Try again!";
        };
    }
    else{
        errorMsg.style.display='block';
    }
};
//Slideshow of images on index.html
var slideIndex = 0;
	showSlides();

function showSlides() {
    var i;
    var slides = document.getElementsByClassName("mySlides");
    var dots = document.getElementsByClassName("dot");
    if(slides.length>0){
        for (i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
        }
        slideIndex++;
        if (slideIndex> slides.length) {slideIndex = 1;}
        for (i = 0; i < dots.length; i++) {
        dots[i].className = dots[i].className.replace(" active", "");
        }
        slides[slideIndex-1].style.display = 'block';
        dots[slideIndex-1].className += " active";
        setTimeout(showSlides, 5000); // Change image every 10 seconds
    }
}
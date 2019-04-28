window.onload=checkAdv;
var org_name = document.getElementById('org_name');
var org_email = document.getElementById('org_email');
var org_sector = document.getElementById('sector');
var org_website = document.getElementById('org_website');
var address = document.getElementById('address');
var loc = document.getElementById('loc');
var zipcode = document.getElementById('zipcode');
var contact_name = document.getElementById('contact_name');
var contact_email = document.getElementById('contact_email');
var contact_position = document.getElementById('contact_position');
function validateAdvForm(){
    if (org_name.value == "")
    {
        snackbar.innerHTML="Please enter the organization name.";
        snackbarShow();
        org_name.focus();
        return false;
    }
    if ((!(/^\w+@\w+.\w+$/.test(org_email.value))))
    {
        snackbar.innerHTML="Please enter a valid e-mail address.";
        snackbarShow();
        org_email.focus();
        return false;
    }
    /*
    if (org_email=="" || org_email.value.indexOf("@", 0) < 0)
    {
        snackbar.innerHTML="Please enter a valid e-mail address.";
        snackbarShow();
        org_email.focus();
        return false;
    }
    if (org_email.value.indexOf(".", 0) < 0)
    {
        snackbar.innerHTML="Please enter a valid e-mail address.";
        snackbarShow();
        org_email.focus();
        return false;
    }*/
    if (org_sector.selectedIndex < 1)
    {
        snackbar.innerHTML="Please select a sector";
        snackbarShow();
        org_sector.focus();
        return false;
    }
    if (address.value == "")
    {
        snackbar.innerHTML="Please enter an address";
        snackbarShow();
        address.focus();
        return false;
    }
    if (loc.selectedIndex < 1)
    {
        snackbar.innerHTML="Please select a location";
        snackbarShow();
        loc.focus();
        return false;
    }
    if (!(/^7\d{5}$/.test(zipcode.value)))
    {
        snackbar.innerHTML="Please provide correct zipcode.";
        snackbarShow();
        zipcode.focus();
        return false;
    }
    if (contact_name.value == "")
    {
        snackbar.innerHTML="Please provide a contact name.";
        snackbarShow();
        contact_name.focus();
        return false;
    }
    if ((!(/^\w+@\w+.\w+$/.test(contact_email.value))))
    {
        snackbar.innerHTML="Please enter a valid contact e-mail address.";
        snackbarShow();
        contact_email.focus();
        return false;
    }
    return true;
}
function checkAdv(){
    $.ajax({
        url: '/loggedin',
        type: 'POST',
        success: function(response) {
            if (response.status==true) {
                console.log(response);
                window.location='/products';
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
        navSignout.style.display='none';
        snavSignin.style.display='block';
        snavSignout.style.display='none';
    };
}
function insertAdv(){
    checkAdv();
    if(validateAdvForm()){
        $.ajax({
            url: '/register',
            data: $('#advertiseform').serialize(),
            type: 'POST',
            success: function(response) {
                if (response.status==true) {
                    console.log(response);
                    snackbar.innerHTML="Advertiser details has been added. Redirecting...";
                    snackbarShow();
                    setTimeout(function(){window.location='/products';}, 2000);
                }else{
                    onError(response.message)
                }
            },
            error: function(error) {
                onError(error);
            }
        });
        function onError(error){
            console.log("Log in to view products");
            snackbar.innerHTML="Error: Advertiser details could not be added right now.";
            snackbarShow();
        };
    }
    /*
    if(validateAdvForm()){
        var obj={},arg={};
        obj["type"]="insert";
        arg["table"]="Advertiser";
        arg["objects"]=[{"id":hasura.user.id,
                        "org_name": org_name.value,
                        "org_email":org_email.value,
                        "org_sector":org_sector.value,
                        "org_website":org_website.value,
                        "address":address.value,
                        "zipcode":zipcode.value,
                        "contact_name":contact_name.value,
                        "contact_email":contact_email.value,
                        "contact_position":contact_position.value
                        }];
        arg["returning"]=["id"];
        obj["args"]=arg;
        console.log(obj);
        hasura.data.query(obj, function onSuccess(result){
            snackbar.innerHTML="Advertiser ID has been added. Redirecting...";
            snackbarShow();
            setTimeout(function(){window.location='/products';}, 2000);
        },
        function onError(err){
            console.error(err);
            snackbar.innerHTML="Error: Advertiser details could not be added right now.";
            snackbarShow();
        }, hasura.user.roles[0]);
    }*/
}
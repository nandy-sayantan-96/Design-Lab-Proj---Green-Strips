var successMsgIn = document.getElementById('success-msg-in');
var errorMsgIn = document.getElementById('error-msg-in');
var snackbar =document.getElementById('snackbar');
var cartButtons = document.getElementsByClassName('cart');
var err =document.getElementById("err");

window.onload = function(){
    checkAdv();
}

function checkAdv(){
    $.ajax({
        url: '/loggedin',
        type: 'POST',
        success: function(response) {
            if (response.status==true) {
                console.log('user logged in');
                navSignin.style.display='none';
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
        console.log("Log in to view products");
        window.location='/advertiseForm';
    };
}

function isPackageInCart(pckid,qty,callback){
    $.ajax({
        url: '/isPackageInCart',
        type: 'POST',
        success: function(response) {
            if (response.status==true) {
                console.log(result[0]);
                snackbar.innerHTML="Package already in cart!";
                snackbarShow();
            }else{
                console.log("Not found in cart. You can add package now.");
                callback(pckid,qty);
            }
        },
        error: function(error) {
            console.error(error);
        }
    });
}

function addToCart(item){
    var package = item.parentElement;
    var ip = package.getElementsByTagName("input");
    var id = package.getElementsByClassName("pid")[0].innerHTML;
    var qty=ip[0].value;

    $.ajax({
        url: '/loggedin',
        type: 'POST',
        success: function(response) {
            if (response.status==true) {
                console.log('user logged in');
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
        document.getElementById('id01').style.display='block';
        successMsgIn.innerHTML="Please sign in to add items to cart";
        successMsgIn.style.display='block';
        return;
    }
    //isPackageInCart(parseInt(id),qty,insertCart);
    insertCart(parseInt(id),qty)
}
function insertCart(pckid,qty){
    if(qty!="" && qty>=1 && qty<=100){
        console.log('/addToCartAdvertise/' + pckid);
        console.log({'qty': qty});
        $.ajax({
            url: '/addToCartAdvertise/' + pckid,
            data: {'qty': qty},
            type: 'POST',
            success: function(response) {
                if (response.status==true) {
                    console.log(response.message);
                    snackbar.innerHTML="Added to cart";
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
            snackbar.innerHTML="Error:" + error;
            snackbarShow();
            return;
        };
    }else{
        snackbar.innerHTML="Please enter correct quantity (1 to 100)";
        snackbarShow();
    }
}
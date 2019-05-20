//window.onload=loadPage;
function getPackage(id,qty,bool){
    var obj={},arg={};
    var desc,price;
    obj["type"]="select";
    arg["table"]="Package";
    arg["columns"]=["*"];
    arg["where"]={"id" : { "$eq" : id }};
    obj["args"]=arg;
    console.log(obj);
    hasura.data.query(obj, function onSuccess(result){
        if(result[0]){
            desc=result[0].description;
            price=result[0].price;
            addBox(id,desc,qty,price,bool);
            console.log("found package details: "+result[0].description);
        }
        else{
            console.log("no such package");
        }
    },
    function onError(err){
        console.error(err);
    }, hasura.user.roles[0]);
}
function checkCart(){
    var obj={},arg={};
    obj["type"]="select";
    arg["table"]="Cart_item";
    arg["columns"]=["*"];
    arg["where"]={"adv_id" : { "$eq" : hasura.user.id }};
    obj["args"]=arg;
    console.log(obj);
    hasura.data.query(obj, function onSuccess(result){
        if(result[0]){
            for (i = 0; i < result.length; i++) {
                console.log("found adv_id: "+result[i].adv_id + " and prd_id: " +result[i].package_id);
                getPackage(result[i].package_id,result[i].quantity,true);
            }
        }
        else{
            console.log("no items in cart");
            snackbar.innerHTML="No items in your cart";
            snackbarShow();
        }
    },
    function onError(err){
        console.error(err);
    }, hasura.user.roles[0]);
}
function checkOrder(){
    var obj={},arg={};
    obj["type"]="select";
    arg["table"]="Order";
    arg["columns"]=["*"];
    arg["where"]={"adv_id" : { "$eq" : hasura.user.id }};
    obj["args"]=arg;
    console.log(obj);
    hasura.data.query(obj, function onSuccess(result){
        if(result[0]){
            for (i = 0; i < result.length; i++) {
                console.log("found adv_id: "+result[i].adv_id + " and prd_id: " +result[i].package_id);
                getPackage(result[i].package_id,result[i].quantity,false);
            }
        }
        else{
            console.log("No result in Order table");
        }
    },
    function onError(err){
        console.error(err);
    }, hasura.user.roles[0]);
}
function loadPage(){
    checkCart();
    checkOrder();
    document.getElementById('pagecon').style.display='block';
    document.getElementsByClassName('loading')[0].style.display='none';
}
/*
function addBox(id,desc,qty,price,bool){
    var pagecon=document.getElementById('pagecon');
    var container = document.createElement("div");
    container.className="container";

    var image = document.createElement("img");
    image.src="./images/Planet_Earth.jpg";
    image.style="width:90px;";

    var p1 = document.createElement("p");
    var spn = document.createElement("span");
    spn.innerHTML=desc;
    var p2 = document.createElement("p");
    p2.innerHTML="Quantity: "+qty+", Price per piece: Rs."+price;

    var btn = document.createElement("button");
    btn.className="submit-btn";
    btn.setAttribute("value",qty);
    btn.setAttribute("id",id);
    btn.setAttribute("onclick","order(this);");
    btn.innerHTML="ORDER";

    var delbtn = document.createElement("button");
    delbtn.className="cancelbtn";
    delbtn.setAttribute("id",id);
    delbtn.setAttribute("onclick","deleteCart(this);");
    delbtn.innerHTML="DELETE";

    if(bool){
        btn.style.display="block";
        delbtn.style.display="block";
    }else{
        btn.style.display="none";
        delbtn.style.display="none";
    }

    var data = document.createTextNode("Total cost: Rs." + (qty*price));
    p1.appendChild(spn);
    p1.appendChild(data);

    container.appendChild(image);
    container.appendChild(p1);
    container.appendChild(p2);
    container.appendChild(btn);
    container.appendChild(delbtn);
    pagecon.appendChild(container);
}
*/
function order(ob){
    var obj={},arg={};
    obj["type"]="insert";
    arg["table"]="Order";
    arg["objects"]=[{"adv_id":hasura.user.id,
                     "package":ob.id,
                     "quantity":ob.value,
                     "status":"Placed",
                     "date_created":new Date(),
                     "total_price":(ob.id*ob.value)
                    }];
    obj["args"]=arg;
    obj["returning"]="id";
    console.log(obj);
    hasura.data.query(obj, function onSuccess(result){
        console.log(result);
        snackbar.innerHTML="Order placed successfully";
        snackbarShow();
        removeCart(ob);
    },
    function onError(err){
        console.error(err);
        snackbar.innerHTML="Error! Please try again later";
        snackbarShow();
    }, hasura.user.roles[0]);
}
function removeCart(ob){
    var obj={},arg={};
    obj["type"]="delete";
    arg["table"]="Cart_item";
    arg["where"]={"$and":[{"adv_id" : { "$eq" : hasura.user.id }},
                       {"package_id" : { "$eq" : ob.id }}]};
    obj["args"]=arg;
    console.log(obj);
    hasura.data.query(obj, function onSuccess(result){
        ob.style.display='none';
        ob.parentElement.lastChild.style.display="none";
    },
    function onError(err){
        console.error(err);
    }, hasura.user.roles[0]);
}
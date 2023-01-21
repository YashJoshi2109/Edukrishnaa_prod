function Login()
{
    
 var a = new Array();
 up1 = new Object();
 up2 = new Object();
 
up1={
 name:'abcd@gmail.com',
 password:btoa('abc@12')
};
up2={
 name:'bcd@gmail.com',
 password:btoa('bcd@12')
};

a.push(up1);
a.push(up2);

var username = document.getElementById('uname').value;
var password = document.getElementById('psw').value;
sessionStorage.setItem('currentloggedin',username);
localStorage.setItem('all_users',JSON.stringify(a));

a=JSON.parse((localStorage.getItem("all_users")));
a.push({name: username, password: password});
localStorage.setItem('name',JSON.stringify(a));
for(var i=0; i<a.length; i++)
  {
   var li = document.createElement("li");
   li.innerHTML=a[i]['name'];
   document.getElementById("listuser").appendChild(li);
  }
}


function Login()
{
    const hash = Object.fromEntries(
    a.map(e => [e.name, e.password])
         )
     var username = document.getElementById('uname').value;
     var password = document.getElementById('psw').value;
     for (let key of hash) 
     {
     
         if(key[0] === username && key[1]===atob(password))
         {
              alert('Login successful');
         }
  
     else
         {
             alert('Login fail');
         }
         var hashmap = a.reduce(function(map, obj) {
            map[obj.key] = obj.val;
            return map;
        }, {});
        const hashmap = Object.assign({}, ...(<{}>a.map(s => ({[s.key]:s.value}))));
    }
}

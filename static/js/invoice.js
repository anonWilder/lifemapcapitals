var socket = new WebSocket("wss://www.blockonomics.co/payment/"+ address);
socket.onmessage = function(event){
  response = JSON.parse(event.data);
  //This condition ensures that we reload only when we get a 
  //new payment status and don't go into a loop
    if (parseInt(response.status) > parseInt(status))
    setTimeout(function(){window.location.reload() }, 1000); 
  
}
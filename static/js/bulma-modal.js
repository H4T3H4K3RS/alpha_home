function show_modal(num) {
 var x = document.getElementById("modal" + String(num));
 x.className += " is-active";
}

function close_modal(num) {
 var x = document.getElementById("modal" + String(num));
 x.className = "modal";
}
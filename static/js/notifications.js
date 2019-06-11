function show_notification(text="LOREM", status="error", type="bottom-right") {
    let notification = document.getElementById("notification");
    notification.className = "";
    notification.setAttribute("data-notification-status", status);
    notification.className = type;
    notification.className += " notify  do-show";
    notification.innerHTML = text;
    setTimeout(function () { notification.classList.remove("do-show"); }, 3500);
}

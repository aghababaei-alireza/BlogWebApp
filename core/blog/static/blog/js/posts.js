function delete_post(action) {
    form = document.getElementById("delete_form");
    form.action = action;

    form.classList.remove("hidden");
    event.stopPropagation();
}

function close_delete_modal() {
    form = document.getElementById("delete_form");
    form.classList.add("hidden");
}

function show_detail(url) {
    window.location = url;
}

document.querySelectorAll("button.action_button").forEach(element => {
    element.addEventListener("click", e => {
        e.stopPropagation();
    })
});
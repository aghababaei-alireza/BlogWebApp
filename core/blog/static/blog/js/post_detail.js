function delete_post(action) {
    form = document.getElementById("delete_form");
    form.action = action;

    form.classList.remove("hidden");
}

function close_delete_modal() {
    form = document.getElementById("delete_form");
    form.classList.add("hidden");
}

function update_comment(action, content) {
    form = document.getElementById("update_comment");
    form.action = action;
    form.classList.remove("hidden");

    document.getElementById("update_content").value = content;
}

function close_update_modal() {
    form = document.getElementById("update_comment");
    form.classList.add("hidden");
}

function close_delete_comment_modal() {
    form = document.getElementById("delete_comment");
    form.classList.add("hidden");
}

function delete_comment(action) {
    form = document.getElementById("delete_comment");
    form.action = action;

    form.classList.remove("hidden");
}
function add_category(action) {
    form = document.getElementById("category_form")
    form.action = action

    overlay = document.getElementById("overlay")
    overlay.classList.remove("hidden")

    form.classList.remove("hidden")

    document.querySelector("#category_form>div>#name").value = null
    document.querySelector("#category_form>div>#color").value = null
    document.querySelector("#category_form>#submit").value = "Add"
}

function close_modal() {
    form = document.getElementById("category_form")
    form.classList.add("hidden")

    overlay = document.getElementById("overlay")
    overlay.classList.add("hidden")
}

function update_category(action, name, color) {
    form = document.getElementById("category_form")
    form.action = action

    overlay = document.getElementById("overlay")
    overlay.classList.remove("hidden")

    form.classList.remove("hidden")

    document.querySelector("#category_form>div>#name").value = name
    document.querySelector("#category_form>div>#color").value = color
    document.querySelector("#category_form>#submit").value = "Update"
}

function close_delete_modal() {
    form = document.getElementById("delete_form")
    form.classList.add("hidden")

    overlay = document.getElementById("overlay")
    overlay.classList.add("hidden")
}

function delete_category(action) {
    form = document.getElementById("delete_form")
    form.action = action

    overlay = document.getElementById("overlay")
    overlay.classList.remove("hidden")

    form.classList.remove("hidden")
}
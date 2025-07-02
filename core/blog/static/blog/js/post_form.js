function toggle_dropdown() {
    document.getElementById('category_dropdown').classList.toggle('hidden');
}

function select_item(id, name) {
    document.getElementById('category').value = id;
    document.getElementById('category_text').value = name;
    toggle_dropdown();
}

document.getElementById("delete_image")?.addEventListener("change", function () {
    if (this.checked) {
        document.getElementById("image_preview").style.display = "none";
        document.getElementById("image").style.display = "none";
    } else {
        document.getElementById("image_preview").style.display = "block";
        document.getElementById("image").style.display = "block";
    }
});


const imageInput = document.getElementById("image");
const imagePreview = document.getElementById("image_preview");
imageInput.addEventListener("change", function () {
    const file = this.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function (e) {
            imagePreview.src = e.target.result;
            // document.getElementById("image_data").value = imagePreview.src;
        };
        reader.readAsDataURL(file);
    }
});

// Intercept form submit and insert cropped image data
document.getElementById("form").addEventListener("submit", function (e) {
    document.getElementById("image_data").value = imagePreview.src;
    console.log("CHABGED");
});
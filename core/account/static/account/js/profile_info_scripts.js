// function showImage(input) {
//     if (input.files && input.files[0]) {
//         var reader = new FileReader();

//         reader.onload = function (e) {
//             img = document.getElementById("prof_img")
//             img.src = e.target.result;
//             img.style.display = "unset";
//         };

//         reader.readAsDataURL(input.files[0]);
//     }
// }

let cropper;
const imageInput = document.getElementById("image-input");
const cropPreview = document.getElementById("crop-preview");

imageInput.addEventListener("change", function () {
    const file = this.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function (e) {
            cropPreview.src = e.target.result;

            // Delay cropper init to make sure image is loaded
            cropPreview.onload = function () {
                if (cropper) cropper.destroy();
                cropper = new Cropper(cropPreview, {
                    aspectRatio: 1,
                    viewMode: 1,
                });
            };
        };
        reader.readAsDataURL(file);
    }
});

// Intercept form submit and insert cropped image data
document.querySelector("form").addEventListener("submit", function (e) {
    if (cropper) {
        const canvas = cropper.getCroppedCanvas({ width: 300, height: 300 });
        document.getElementById("cropped_image_data").value = canvas.toDataURL("image/png");
    }
    else {
        document.getElementById("cropped_image_data").value = cropPreview.src
    }
});

document.getElementById("delete_image")?.addEventListener("change", function () {
    if (this.checked) {
        document.getElementById("crop-preview").style.display = "none";
        document.getElementById("image-input").style.display = "none";
    } else {
        document.getElementById("crop-preview").style.display = "block";
        document.getElementById("image-input").style.display = "block";
    }
});
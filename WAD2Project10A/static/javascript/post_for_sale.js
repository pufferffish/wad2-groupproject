const uploadButton = document.getElementById("upload")
const priceInput = document.getElementById("price")
const picPreview = document.getElementById("pic")

function toggleForSale(element) {
    priceInput.disabled = !element.checked;
}

toggleForSale(document.getElementById("forSale"));

uploadButton.addEventListener("change", function () {
   files = uploadButton.files[0];
  if (files) {
    const fileReader = new FileReader();
    fileReader.readAsDataURL(files);
    fileReader.addEventListener("load", function () {
      picPreview.src = this.result;
    });
  }
});

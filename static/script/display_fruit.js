document.addEventListener("DOMContentLoaded", function () {

  const fruit_image = document.getElementById("fruitImage");

  window.addEventListener("load", function () {
    let imageData = this.localStorage.getItem("imageData");

    if (imageData) {
      fruit_image.src = imageData;
    } else {
      alert("No image data found.");
    }
  });
  
});
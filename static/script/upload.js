document.addEventListener("DOMContentLoaded", function () {
  const upload_button = document.getElementById("uploadButton");
  const camera_button = document.getElementById("cameraButton");
  const spinner = document.getElementById("spinner");
  const file_input = document.getElementById("fileInput");

  function disableButtons() {
    camera_button.disabled = true;
    upload_button.disabled = true;
  }

  function enableButtons() {
    camera_button.disabled = false;
    upload_button.disabled = false;
  }

  upload_button.addEventListener("click", function () {
    file_input.click();
  });

  file_input.addEventListener("change", function (ev) {
    const file = ev.target.files[0];

    if (file) {
      const reader = new FileReader();
      reader.onload = function (e) {
        let imageData = e.target.result;
        localStorage.setItem("imageData", imageData);

        // Show the spinner
        spinner.style.display = "block";

        // Disabled the camera and the upload buttons to prevent additional clicks
        disableButtons();

        fetch(detailspageUrl, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken,
          },
          body: JSON.stringify({ imageData: imageData }),
        })
          .then((response) => {
            if (response.ok) {
              return response.json();
            } else {
              throw new Error("Network response was not ok");
            }
          })
          .then((data) => {
            window.location.href = detailspageUrl; // Redirect to the details page
          })
          .catch((error) => {
            console.error("Error:", error);
            // Hide the spinner if an error occurs
            spinner.style.display = "none";
            // Re-enable the buttons if an error occurs
            enableButtons();
          });
      };
      reader.readAsDataURL(file);
    }
  });
});

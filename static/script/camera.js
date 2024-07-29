document.addEventListener("DOMContentLoaded", function () {
  const camera_button = document.getElementById("cameraButton");
  const upload_button = document.getElementById("uploadButton");
  const spinner = document.getElementById("spinner");

  function disableButtons() {
    camera_button.disabled = true;
    upload_button.disabled = true;
  }

  function enableButtons() {
    camera_button.disabled = false;
    upload_button.disabled = false;
  }

  if (camera_button) {
    camera_button.addEventListener("click", function () {
      if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices
          .getUserMedia({ video: true })
          .then(function (stream) {
            let video = document.createElement("video");
            video.srcObject = stream;
            video.play();
            document.getElementById("videoContainer").appendChild(video);

            let captureButton = document.createElement("button");
            captureButton.innerText = "Capture";
            let cancelButton = document.createElement("button");
            cancelButton.innerText = "Cancel";

            document.getElementById("btn-container").appendChild(captureButton);
            document.getElementById("btn-container").appendChild(cancelButton);

            // Disabled the camera and the upload buttons to prevent additional clicks
            disableButtons();

            captureButton.addEventListener("click", function () {
              let canvas = document.createElement("canvas");
              canvas.width = video.videoWidth;
              canvas.height = video.videoHeight;
              let context = canvas.getContext("2d");
              context.drawImage(video, 0, 0, canvas.width, canvas.height);

              // Stop the video stream
              stream.getTracks().forEach((track) => track.stop());

              // Remove video and buttons from the DOM
              video.remove();
              captureButton.remove();
              cancelButton.remove();

              let imageData = canvas.toDataURL("image/png");
              localStorage.setItem("imageData", imageData);

              // Show the spinner
              spinner.style.display = "block";

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
            });

            cancelButton.addEventListener("click", function () {
              stream.getTracks().forEach((track) => track.stop());
              video.remove();
              captureButton.remove();
              cancelButton.remove();

              // Re-enable the camera and upload button after canceling
              enableButtons();
            });
          })
          .catch(function (error) {
            console.log("An error occurred: " + error);
          });
      } else {
        alert("Your browser can't access camera");
      }
    });
  } else {
    console.error("Camera button not found");
  }
});

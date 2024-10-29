// Handle image upload and segmentation display
function uploadImage() {
  const input = document.getElementById('upload-image');
  const formData = new FormData();
  formData.append('file', input.files[0]);

  fetch('/upload_image', {
      method: 'POST',
      body: formData
  })
  .then(response => response.json())
  .then(data => {
      if (data.segmented_image) {
          document.getElementById('segmented-image').src = data.segmented_image;
      } else {
          alert('Failed to segment image');
      }
  })
  .catch(error => console.error('Error:', error));
}

// Real-time game preview update
function updateGamePreview() {
  const code = document.getElementById('code-editor').value;
  const gamePreview = document.getElementById('game-preview');
  gamePreview.innerHTML = '';  // Clear current preview
  
  try {
      const script = document.createElement('script');
      script.type = 'text/javascript';
      script.text = code;
      gamePreview.appendChild(script);
  } catch (error) {
      console.error("Error in preview code:", error);
  }
}

document.addEventListener("DOMContentLoaded", () => {
    const dropZone = document.getElementById("drop-zone");
    const fileInput = document.getElementById("upload-image");

    // Click on drop zone to trigger file input
    dropZone.addEventListener("click", () => fileInput.click());

    // Update UI on drag over
    dropZone.addEventListener("dragover", (e) => {
        e.preventDefault();
        dropZone.classList.add("dragover");
    });

    dropZone.addEventListener("dragleave", () => {
        dropZone.classList.remove("dragover");
    });

    // Handle file drop
    dropZone.addEventListener("drop", (e) => {
        e.preventDefault();
        dropZone.classList.remove("dragover");

        const files = e.dataTransfer.files;
        if (files.length > 0) {
            fileInput.files = files;  // Set files to the file input
            uploadImage();  // Trigger upload
        }
    });
});


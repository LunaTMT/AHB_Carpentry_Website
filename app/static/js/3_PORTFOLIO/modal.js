document.addEventListener('DOMContentLoaded', function() {
    // Get the modal
    const modal = document.getElementById("modal");
    const modalImg = document.getElementById("modal-image");
 
    const closeBtn = document.getElementsByClassName("close")[0];

    // Get all thumbnail images
    const thumbnails = document.querySelectorAll('.thumbnail');

    // Open the modal and show the clicked image
    thumbnails.forEach(img => {
        img.addEventListener('click', function() {
            modal.style.display = "flex";
            modal.style.alignItems = 'center';
            modal.style.justifyContent = 'center';
            modal.style.flexDirection = 'column';
            modalImg.src = this.dataset.largeSrc;


        });
    });

    // Close the modal
    closeBtn.addEventListener('click', function() {
        modal.style.display = "none";
    });

    // Close the modal when clicking outside the image
    window.addEventListener('click', function(event) {
        if (event.target === modal) {
            modal.style.display = "none";
        }
    });
});

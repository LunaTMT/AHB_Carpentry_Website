const button = document.getElementById('add_button');

button.addEventListener('click', function(event) {
    var form = document.getElementById('add_residency_form');
    if (form.style.display === 'none' || form.style.display === '') {
        // Show the form
        console.log("Making visible");
        button.style.marginBottom = 0;
        form.style.display = 'flex'; // or 'block' depending on your layout

    } else {
        // Hide the form
        console.log("Making hidden");
        button.style.marginBottom = '2.5%';
        form.style.display = 'none';
    }
});

document.addEventListener('DOMContentLoaded', function() {
    // Select all image elements within the #portfolio-container
    const images = document.querySelectorAll('#portfolio-container img');

    images.forEach(function(img) {
        // Add a single mouseover event listener
        img.addEventListener('mouseover', function() {
            console.log('Mouse over image with ID:', img.id);
            img.classList.add('selected', 'image-overlay');
        });

        // Add a single mouseout event listener
        img.addEventListener('mouseout', function() {
            img.classList.remove('selected', 'image-overlay');
        });

        // Add a single click event listener
        img.addEventListener('click', function() {
            // Confirm deletion with the user
            const photoContainer = document.getElementById('photo-container');
            const projectContainer = document.getElementById('project-container');

            // Get image details
            const imageName = img.getAttribute('data-image-name');
            const residencyName = img.getAttribute('data-residence-name');

            fetch('/delete-image', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    image_name: imageName,
                    residency_name: residencyName
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    switch (data.message) {
                        case "remove_project_container":
                            projectContainer.remove();
                            break;
                        case "remove_photo_container":
                            photoContainer.remove();
                            break;
                        default:
                            console.log('Unknown action:', data.message);
                            break;
                    }
                    if (data.refresh){
                        location.reload();
                    }
                } else {
                    console.error(data.message);
                }
            })
            .catch(error => console.error('Error:', error));
        });
    });
});

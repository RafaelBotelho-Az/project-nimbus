

// Dropdown meu


const profileImg = document.getElementById('profile-img');
const dropdownMenu = document.getElementById('profile-dropdown');
profileImg.addEventListener('click', function() {
    dropdownMenu.style.display = dropdownMenu.style.display === 'none' || dropdownMenu.style.display === '' ? 'block' : 'none';
});
document.addEventListener('click', function(event) {
    const isClickInside = profileImg.contains(event.target) || dropdownMenu.contains(event.target);
    if (!isClickInside) {
        dropdownMenu.style.display = 'none';
    }
});


// Message timer


setTimeout(function() {
    const messageContainer = document.getElementById('message-container');
    if (messageContainer) {
      messageContainer.style.display = 'none';
    }
  }, 5000);


// Image preview


$(document).ready(function() {
    $('#id_tags').select2({
        placeholder: "Selecione as tags",
        allowClear: true
    });

    $('#id_image').on('change', function(event) {
        var imagePreview = $('#imagePreview');
        var file = event.target.files[0];

        if (file) {
            var reader = new FileReader();

            reader.onload = function(e) {
                imagePreview.attr('src', e.target.result);
                imagePreview.show();
            };

            reader.readAsDataURL(file);
        } else {
            imagePreview.hide();
        }
    });
});
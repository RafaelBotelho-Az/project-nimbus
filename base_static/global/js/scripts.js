

// Dropdown meu


const profileImg = document.getElementById('profile-img');
const dropdownMenu = document.getElementById('profile-dropdown');

if (profileImg && dropdownMenu) {
    profileImg.addEventListener('click', function() {
        dropdownMenu.style.display = dropdownMenu.style.display === 'none' || dropdownMenu.style.display === '' ? 'block' : 'none';
    });

    document.addEventListener('click', function(event) {
        const isClickInside = profileImg.contains(event.target) || dropdownMenu.contains(event.target);
        if (!isClickInside) {
            dropdownMenu.style.display = 'none';
        }
    });
}

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


function ativarHoverSeVisivel() {
    const gridItems = document.querySelectorAll('.grid-item');

    if (window.innerWidth <= 768) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                const postInfo = entry.target.querySelector('.post-info');
                const interaction = entry.target.querySelector('.interactions');
                const c_date = entry.target.querySelector('.c-date');

                if (entry.isIntersecting) {
                    if (postInfo) postInfo.style.opacity = '1';
                    if (interaction) interaction.style.opacity = '1';
                    if (c_date) c_date.style.opacity = '1';
                    console.log('Script carregado');
                } else {
                    if (postInfo) postInfo.style.opacity = '0';
                    if (interaction) interaction.style.opacity = '0';
                    if (c_date) c_date.style.opacity = '0';
                }
            });
        }, { threshold: 0.98 });

        gridItems.forEach(item => {
            observer.observe(item);
        });
    }
}
window.addEventListener('load', ativarHoverSeVisivel);
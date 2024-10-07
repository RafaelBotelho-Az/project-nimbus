

// desktop dropdown perfil


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

// hover dos posts para mobile

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

// mobile dropdown menu

document.addEventListener("DOMContentLoaded", function() {
    var menuIcon = document.querySelector(".menu-icon");
    var dropdown = document.getElementById("dropdown");

    if (menuIcon && dropdown) {
        menuIcon.onclick = function() {
            dropdown.classList.toggle("show");
            if (dropdown.classList.contains("show")) {
                menuIcon.textContent = "✖";
            } else {
                menuIcon.textContent = "☰";
            }
        };

        window.onclick = function(event) {
            if (!event.target.matches('.menu-icon')) {
                if (dropdown.classList.contains('show')) {
                    dropdown.classList.remove('show');
                    menuIcon.textContent = "☰";
                }
            }
        };
    }
});

// mobile dropdown perfil

const imgPerfil = document.getElementById("profile-img2");
const dropdownPerfil = document.getElementById("profile-dropdown2");

if (imgPerfil && dropdownPerfil) {
    imgPerfil.addEventListener('click', function() {
        dropdownPerfil.style.display = dropdownPerfil.style.display === 'none' || dropdownPerfil.style.display === '' ? 'block' : 'none';
    });
    document.addEventListener('click', function(event) {
        const isClickInside = imgPerfil.contains(event.target) || dropdownPerfil.contains(event.target);
        if (!isClickInside) {
            dropdownPerfil.style.display = 'none';
        }
    });
}

// ocutar ou exibir form update user

document.getElementById("edit-info-link").addEventListener("click", function() {
    var form = document.getElementById("profile-form");
    if (form.style.display === "none" || form.style.display === "") {
        form.style.display = "block";  // Exibe o formulário
    } else {
        form.style.display = "none";   // Oculta o formulário se já estiver visível
    }
});

document.getElementById("edit-image-link").addEventListener("click", function() {
    var form = document.getElementById("image-form");
    if (form.style.display === "none" || form.style.display === "") {
        form.style.display = "block";  // Exibe o formulário
    } else {
        form.style.display = "none";   // Oculta o formulário se já estiver visível
    }
});
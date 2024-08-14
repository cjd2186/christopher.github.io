$(document).on('click', function (event) {
    var clickOver = $(event.target);
    var opened = $(".navbar-collapse").hasClass("show");

    // Collapse the navbar if the menu is open and a click occurs outside the navbar
    if (opened === true && !clickOver.closest('.navbar').length) {
        $('.navbar-toggler').click(); // Triggers the toggle action to close the menu
    }
});

$(document).ready(function () {
    // Attach a click event to all links within the .navbar-collapse except dropdown toggles
    $('.navbar-collapse a:not(.dropdown-toggle)').click(function (e) {
        // Collapse the navbar
        $('.navbar-collapse').collapse('hide');

        // Allow the default behavior of the anchor tag to navigate to the section
        var target = $(this).attr('href');
        if (target && target.startsWith('#')) {
            e.preventDefault(); // Prevent the default action to avoid interfering with the jump
            setTimeout(function () {
                window.location.href = target; // Navigate to the section
            }, 300); // Adjust this delay if needed to allow the collapse animation to complete
        }
    });
});
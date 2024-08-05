$(document).ready(function () {
    var lastScrollTop = 0;
    $(window).on('scroll', function () {
        var currentScrollTop = $(this).scrollTop();
        if (currentScrollTop > lastScrollTop) {
            // Scrolling down
            $('.navbar').css('top', '-60px'); // Adjust height to the navbar height
        } else {
            // Scrolling up
            $('.navbar').css('top', '0');
        }
        lastScrollTop = currentScrollTop;
    });
});
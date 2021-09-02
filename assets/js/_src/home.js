$(document).ready(function () {
    const loadWidth = $(window).width();
    console.log(loadWidth);
    if (loadWidth > 768) {
        $('.carousel-container').flickity({
            wrapAround: $('.carousel-container').length > 2 ? true : false,
            autoPlay: 8000,
            pageDots: false,
        });
    } else {
        $('.carousel-container').flickity({
            wrapAround: $('.carousel-container').length > 2 ? true : false,
            autoPlay: 8000,
            pageDots: true,
            prevNextButtons: false,
        });
    }

});
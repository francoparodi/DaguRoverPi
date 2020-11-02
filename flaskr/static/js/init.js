function speedSliderEvents(speedSlider) {
    var slide = document.getElementById(speedSlider);
    slide.onchange = function() {
        $.post({
                url: '/',
                data: $('form').serialize(),
                success: function(response){
                    console.log(response);
                },
                error: function(error){
                    console.log(error);
                }
            });
    }
}
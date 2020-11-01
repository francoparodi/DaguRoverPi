function speedSliderEvents(speedSlider, speedSliderDiv) {
    var slide = document.getElementById(speedSlider),
    sliderDiv = document.getElementById(speedSliderDiv);
    slide.onchange = function() {
        sliderDiv.innerHTML = this.value;
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
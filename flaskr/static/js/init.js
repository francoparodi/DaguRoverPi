function sliderEvents(elementId, toUrl) {
    var element = document.getElementById(elementId);
    element.onchange = function() {
        $.post({
                url: toUrl,
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

function buttonEvents(elementId, toUrl) {
    var element = document.getElementById(elementId);
    element.onclick = function() {
        $.post({
                url: toUrl,
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
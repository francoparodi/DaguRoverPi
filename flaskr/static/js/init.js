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
            $("#divStatusId").load(" #divStatusId > *");
        }
}

function buttonEvents(elementId, toUrl, command) {
    var element = document.getElementById(elementId);
    element.onclick = function() {
        $.post({
                url: toUrl,
                data: 'command='+command,
                success: function(response){
                    console.log(response);
                },
                error: function(error){
                    console.log(error);
                }
            });
            $("#divStatusId").load(" #divStatusId > *");
    }
}
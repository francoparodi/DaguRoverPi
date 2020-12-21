function sliderEvents(elementId, toUrl) {
    var element = document.getElementById(elementId);
    element.onchange = function() {
        $.post({
                url: toUrl,
                data: $('form').serialize(),
                success: function(response){
                    //console.log(response);
                },
                complete: function (data) {
                    $("#divStatusId").load(" #divStatusId > *");
                },
                error: function(error){
                    console.log(error);
                }
            });
        }
}

function buttonEvents(elementId, toUrl, command) {
    var element = document.getElementById(elementId);
    element.onclick = function() {
        $.post({
                url: toUrl,
                data: 'command='+command,
                success: function(response){
                    //console.log(response);
                },
                complete: function (data) {
                    $("#divStatusId").load(" #divStatusId > *");
                },
                error: function(error){
                    console.log(error);
                }
            });
    }
}

function keepAlive() {
    $.post({
            type: 'POST',
            url: '/clientConnected',
            data: 'clientConnected=True',
            dataType: 'json',
            success: function (response) {
                //console.log(response);   
            },
            complete: function (data) {
                // Schedule the next
            },
            error: function(error){
                //console.log(error);
            }
        });
        $("#divStatusId").load(" #divStatusId > *");
}

var intervalId;

function startKeepAlive(seconds){
    if(!intervalId) { 
        intervalId = setInterval(keepAlive, seconds*1000);
    }
}

function stopKeepAlive(){
    clearInterval(intervalId);
}


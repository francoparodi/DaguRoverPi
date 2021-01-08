function sliderEvents(elementId, toUrl) {
    var element = document.getElementById(elementId);
    element.onchange = function() {
        $.post({
                url: toUrl,
                data: $('form').serialize(),
                success: function(response){
                },
                complete: function (data) {
                    $("#divPowerId").load(" #divPowerId > *");
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
                    console.log('success');
                },
                complete: function (data) {
                    console.log('complete');
                    $("#divStatusId").load(" #divStatusId > *");
                },
                error: function(error){
                    console.log(error);
                }
            });
    }
}

function keepAlive() {
    $.post('/clientConnected', {
            clientConnected: 'True'
        }).done(function(data) {
            $("#divConnectionId").removeClass('form-group hidden').addClass('form-group');
            $("#divLostConnectionId").removeClass('form-group').addClass('form-group hidden');
            $("#divGpsConnectionId").removeClass('form-group hidden').addClass('form-group');
            $("#divGpsLostConnectionId").removeClass('form-group').addClass('form-group hidden');
            $("#divStatusId").load(" #divStatusId > *");
            $("#divGpsConnectionId").load(" #divGpsConnectionId > *");  
        }).fail(function(data) {
            $("#divConnectionId").removeClass('form-group').addClass('form-group hidden');
            $("#divLostConnectionId").removeClass('form-group hidden').addClass('form-group');
            $("#divGpsConnectionId").removeClass('form-group').addClass('form-group hidden');
            $("#divGpsLostConnectionId").removeClass('form-group hidden').addClass('form-group');
        }).always(function(data) {
        });
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


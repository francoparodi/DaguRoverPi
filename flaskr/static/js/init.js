function sliderEvents(elementId, toUrl) {
    var element = document.getElementById(elementId);
    element.onchange = function() {
        $.post({
                url: toUrl,
                data: $('form').serialize(),
                success: function(response){
                    console.log('success onchange on sliderEvent id ' + elementId);
                },
                complete: function (data) {
                    console.log('complete onchange on sliderEvent id ' + elementId);
                    $("#divPowerId").load(" #divPowerId > *");
                },
                error: function(error){
                    console.log('error onchange on sliderEvent id ' + elementId + ' ' + error);
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
                    console.log('success onclick on button id ' + elementId + ' command='+command);
                },
                complete: function (data) {
                    console.log('complete onclick on button id ' + elementId + ' command='+command);
                    $("#divStatusId").load(" #divStatusId > *");
                },
                error: function(error){
                    console.log('error onclick on button id ' + elementId + ' command='+command);
                }
            });
    }
}

function keepAlive() {
    $.post('/clientConnected', {
            clientConnected: 'True'
        }).done(function(data) {
            console.log('done post on keepAlive of clientConnected');
            $("#divConnectionId").removeClass('form-group hidden').addClass('form-group');
            $("#divLostConnectionId").removeClass('form-group').addClass('form-group hidden');
            $("#divGpsConnectionId").removeClass('form-group hidden').addClass('form-group');
            $("#divGpsLostConnectionId").removeClass('form-group').addClass('form-group hidden');
            $("#divStatusId").load(" #divStatusId > *");
            $("#divGpsConnectionId").load(" #divGpsConnectionId > *");  
        }).fail(function(data) {
            console.log('fail post on keepAlive of clientConnected');
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


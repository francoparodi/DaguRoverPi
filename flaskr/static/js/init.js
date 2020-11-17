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
            stopAllButtonsBlinking();
            if(command != "STOP"){
                startBlinking(elementId);
            }
    }
}

function stopAllButtonsBlinking(){
    console.log('stopAll');
    var elementIds = ['buttonForwardId', 'buttonBackwardId', 'buttonClockwiseId', 'buttonCounterClockwiseId'];
    for (i = 0; i < elementIds.length; i++) {
        var element = document.getElementById(elementIds[i]);
        var classElement = element.getAttribute("class");
        classElement = classElement.replace("blinking", ""); 
        element.setAttribute("class", classElement); 
      } 
}

function startBlinking(elementId){
    var element = document.getElementById(elementId);
    classElement = element.getAttribute("class");
    if (!classElement.includes("blinking")){
        classElement = classElement + " blinking";
        element.setAttribute("class", classElement);  
    }
}
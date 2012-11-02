
$(document).ready(function() {
    var b2width = $("#boxTwo").width();
    var b2height = $("#boxTwo").height();
    var b3width = $("#boxThree").width();
    var b3height = $("#boxThree").height();
    
    $("#boxTwoDims").html("" + b2width + " x " + b2height);
    $("#boxThreeDims").html("" + b3width + " x " + b3height);
    
});

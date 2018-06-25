/*
    Script for handling record button functions
    Thanks: https://codepen.io/aeewhite/pen/BjzbOL
*/

// Message displayed when not recording
var not_rec_message = $(".record_elapsed").html()

// Initialise to not recording
$('.record').addClass("notRec");

// Function to update the elapsed time text
var start_time = new Date();
var timer;
var timer_fun = function(){
    // Time in seconds
    var elapsed =  Math.round((new Date() - start_time)/1000);

    $(".record_elapsed").html("RECORDING " + elapsed.toString() + "s elapsed");
}

// Record button click functions
$('.record').click(function() {
    // Start a recording
    if($('.record').hasClass('notRec')){
        // Switch up classes
        $('.record').removeClass("notRec");
        $('.record').addClass("Rec");

        // Start the timer
        start_time = new Date();
        timer_fun();
        timer = setInterval(timer_fun, 1000);

        // Update server
        $.get("/start_record")
    }
    // Stop a recording
    else {
        // Switch up classes
        $('.record').removeClass("Rec");
        $('.record').addClass("notRec");

        // Stop the timer
        clearInterval(timer);
        $(".record_elapsed").html(not_rec_message)

        // Update server
        $.get("/stop_record")
    }
}); 
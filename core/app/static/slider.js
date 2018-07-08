/*
    Sliders for changing parmeters
    expects a devices variable to defined externally that has the fields
    {
        "name": str,
        "animations": {
            "params": [{
                "name": str,
                "min": num,
                "max": num,
                "step": num
            }]
        }
    }
*/

// Select animation box
$(".ani_selector").change(function(){
    // Server request for animation switch
    $.post("/switch_animation", {
        device_name: this.name,
        new_animation: this.value
    }, 
    // Replace the sliders with response data
    function(response_data){
        replace_slider(response_data);
    })
})

// Update the server as the slider is dragged
$(".slider").on("input", function(){
    // Update text that displays current value
    $(this).parent().find(".param_value").html(this.value);

    // Update Server
    $.post("/set_param", {
        device_name: $(this).closest(".device").find(".device_name").html(),
        param_name: $(this).closest(".slidecontainer").find(".param_name").html(),
        param_value: this.value
    })
})

// Replaces the set of animation parameter sliders.
// device arg should be as defined above
var replace_slider = function(device){
    // Element to update
    var device_element = $("#"+device["name"])

    // Remove old sliders
    device_element.find(".slidecontainer").remove()

    // Add new sliders
    for(var j=0; j<device['animation']['params'].length; j++) 
    {
        // Get param name
        var param = device['animation']['params'][j]

        // Clone the prototypical slider and display it
        var slider = $("body").find("#slider_prototype").clone(true)
        slider.css("display", "block");

        // Assign slider attributed
        slider.find(".param_name").html(param["name"])
        slider.find(".param_value").html(param["value"])
        slider.find(".slider").attr({
            min: param["min"],
            max: param["max"],
            step: param["step"]
        })
        slider.find(".slider").attr({value: param["value"]})

        // Add to device list
        device_element.append(slider);
    }
}
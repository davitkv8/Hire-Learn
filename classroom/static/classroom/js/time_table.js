var userTimeGraph = JSON.parse(document.getElementById('days_data').textContent);
const request_user_id = JSON.parse(document.getElementById('request_user_id').textContent);
const requested_user_id = JSON.parse(document.getElementById('requested_user_id').textContent);
var allDays = {
  "availableDays": [],
  "unavailableDays": [],
};

const submit_button = document.getElementsByClassName("save-schedule")[0];


function draw_time_table(){
  let week_days = document.getElementsByClassName("day");
  let hours = document.getElementsByClassName("hour");

  // Looping through all days (monday to sunday).
  // And creating new inputs for them (from 00:00 to 12:00)
  for (let i = 1; i < week_days.length; i++) {
      for (let j = 0; j < 12; j++) {
          let div = document.createElement("div");
          let input = document.createElement("input");
          let week_day = week_days[i].className.split(' ')[1];
          let hour_range = hours[j].textContent.replace(/\s/g, '');
          input.setAttribute("type", "button");

          // Setting up input ids --- >
          // monday_0:00-1:00, monday_1:00-2:00, monday_2:00-3:00.......
          // Everything is clear, if you look at row-column pair in the front side,
          // Where columns are days of week and rows are hours
          let input_id = `${week_day}_${hour_range}`
          input.setAttribute("id", input_id);
          // input.setAttribute("style", "background-color: #949494;");

          // If requested user is itself request user.
          // Another words, if user checking his time graph
          if(request_user_id === requested_user_id) {
            if (!userTimeGraph) {
                // If teacher has not set his timetable case.
                input.setAttribute("data-status", "false");
            }

            else {
                var get_data_status_value = userTimeGraph[week_day][hour_range];
                input.setAttribute("data-status", get_data_status_value);
            }

          }

          week_days[i].appendChild(div);
          div.appendChild(input);
      }
  }
}


 document.addEventListener('click', element =>{
    let clickedElement = element.target;

    // Parsing ID, getting appropriate keys for userTimeGraph object.
    let weekday, time = clickedElement.id.split("_");

    if (request_user_id === requested_user_id) {
        if (clickedElement.getAttribute("data-status") == 'false') {
            clickedElement.setAttribute("data-status", 'true');
        }
        else if (clickedElement.getAttribute("data-status")) {
            clickedElement.setAttribute("data-status", 'false');
        }
    }
    // if (userTimeGraph['weekday']['time']){
    //     {% if request.user.pk == object %}
    //         document.getElementById(clickedElementID).style.backgroundColor = "#949494";
    //     {% else %}
    //         document.getElementById(clickedElementID).style.backgroundColor = "green";
    //     {% endif %}
    //     let index = allDays.availableDays.indexOf(clickedElement.id);
    //     allDays.availableDays.splice(index, 1);
    //     allDays.unavailableDays.push(clickedElementID);
    // }
    // else{
    //     document.getElementById(clickedElementID).style.backgroundColor="green";
    //     allDays.availableDays.push(clickedElementID);
    // }
  })

submit_button.addEventListener("click", function() {

  globalThis.inputs = document.getElementsByTagName("input");

  let days_data = {

  }

    for (let i = 1; i < inputs.length; i++) {
      let weekday = inputs[i].id.split("_")[0];
      let time = inputs[i].id.split("_")[1];

      let status = inputs[i].getAttribute("data-status");

      if (!days_data[weekday]) {
          days_data[weekday] = [];
      }

      let obj = {};
      obj[time] = status

      days_data[weekday].push(obj);

  }
  $.ajax(
    {
        url: `/classroom/time_table/${requested_user_id}/`,
        type: 'POST',
        data: {
        days_data: JSON.stringify(days_data),
        csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
    },
    success: function (response){
            let resp = JSON.parse(response);
            alert(resp.message);
    }
  });

});


function heightResizer(){
    var hour_div_height = document.getElementsByClassName("hour")[0].clientHeight;

    // It makes inputs responsive
    $("input" ).each(function(){
        $(this).css("height", hour_div_height);
        $(this).css("display", "flex");
        $(this).css("border-bottom", "1px solid white");
    });
}

draw_time_table();
heightResizer();
window.addEventListener('resize', heightResizer);

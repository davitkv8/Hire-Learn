var userTimeGraph = JSON.parse(document.getElementById('days_data').textContent);
const request_user_id = JSON.parse(document.getElementById('request_user_id').textContent);
const requested_user_id = JSON.parse(document.getElementById('requested_user_id').textContent);

const url = window.location.href;

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
          div.className = "weekXhour-div";
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

          if (url.includes("booking_pk")) {
              var get_data_status_value = userTimeGraph[week_day][hour_range]

              if (get_data_status_value == true){
                    input = document.createElement("img");
                    input.src = "../../static/classroom/images/marked_v3.png";
                    div.style = "background-color: #949494;";
                    input.style = "height: 100%; display: flex; margin: auto"
                }

              else {
                  input.setAttribute("data-status", get_data_status_value);
              }

              input.disabled = true;

          }

          else {
              if (request_user_id === requested_user_id) {
                  if (!userTimeGraph) {
                      // If teacher has not set his timetable case.
                      input.setAttribute("data-status", "false");
                  } else {
                      var get_data_status_value = userTimeGraph[week_day][hour_range];
                      input.setAttribute("data-status", get_data_status_value);
                  }

              }


              // if one user checking other user's time graph (student booking for teacher)
              // then, student is able to choose only fields where teacher has available times.
              else {
                  var get_data_status_value = userTimeGraph[week_day][hour_range];

                  if (get_data_status_value === true) {
                      input.setAttribute("data-status", "false");
                  } else {
                      input.setAttribute("data-status", "false");
                      input.style = "background-color: #f59f9f !important;"
                      input.disabled = true;
                  }
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

    // if (request_user_id === requested_user_id) {
        if (clickedElement.getAttribute("data-status") == 'false') {
            clickedElement.setAttribute("data-status", 'true');
        }
        else if (clickedElement.getAttribute("data-status")) {
            clickedElement.setAttribute("data-status", 'false');
        }
  })

submit_button.addEventListener("click", function() {

  globalThis.inputs = document.getElementsByTagName("input");

  let days_data = {

  }

    for (let i = 1; i < inputs.length; i++) {
      let weekday = inputs[i].id.split("_")[0];
      let time = inputs[i].id.split("_")[1];

      let status = inputs[i].getAttribute("data-status");

      if (status === "false") {
          continue;
      }

      if (!days_data[weekday]) {
          days_data[weekday] = [];
      }

      days_data[weekday].push(time);

  }

  if (request_user_id === requested_user_id) {
      $.ajax(
          {
              url: `/classroom/time_table/`,
              type: 'POST',
              data: {
                  days_data: JSON.stringify(days_data),
                  csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
              },
              success: function (response) {
                  let resp = JSON.parse(response);
                  alert(resp.message);
              }
          });
  }

  else {

      var data = {
          "requested_user_id": requested_user_id,
          "request_user_id": request_user_id,
          "days_data": days_data,
      }

      $.ajax(
          {
              url: `/classroom/send_booking_request/`,
              type: 'POST',
              data: {
                  data: JSON.stringify(data),
                  csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
              },
              success: function (response) {
                  let resp = JSON.parse(response);
                  alert(resp.message);
              }
          });
  }

});


function heightResizer(){
    var hour_div_height = document.getElementsByClassName("hour")[0].clientHeight;
    console.log(hour_div_height);
    // It makes inputs responsive
    $(".weekXhour-div" ).each(function(){
        $(this).css("height", hour_div_height-1);
        $(this).css("display", "flex");
        $(this).css("border-bottom", "1px solid white");
    });
}

draw_time_table();
heightResizer();
window.addEventListener('resize', heightResizer);

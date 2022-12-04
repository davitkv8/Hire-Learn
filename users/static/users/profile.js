const user_id = JSON.parse(document.getElementById('user_id').textContent);

function email_verification(user){

            console.log(user.itemid)
            $.ajax(
                    {
                        url: "{% url 'userProfile' request.user.pk%}",
                        type: 'POST',
                        data: {
                            type: "verify_request",
                            user: user.id,
                            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
                    },
                        success: function (response){
                    }
           });
        }

        function func(arg){
        parentDiv = arg.parentNode
        parentDiv.remove()

          $.ajax(
                    {
                        url: "{% url 'userProfile' request.user.pk%}",
                        type: 'POST',
                        data: {
                            type: arg.value,
                            user: arg.id,
                            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
                    },
                        success: function (response){
                    }
           });

        }


function draw_profile_page(){
    const fields_data = JSON.parse(document.getElementById('fields_data').textContent);

    console.log(fields_data);

    const obj = JSON.parse(fields_data);

    const user_fields_div = document.getElementById('user-fields');

    obj.forEach(function (item, index) {
        let key = Object.keys(item);

        let row = document.createElement("div");
        row.className = "row";

        let column_div = document.createElement("div");
        column_div.className = "col-sm-3";

        let column_name = document.createElement("h6")
        column_name.className = "mb-0";
        column_name.textContent = item[key]['name_in_front'];

        let column_value_div = document.createElement("div");
        column_value_div.className = "col-sm-9 text-secondary";
        column_value_div.textContent = item[key]['value'];

        let hr = document.createElement("hr")
        column_div.appendChild(column_name);
        row.appendChild(column_div);
        row.appendChild(column_value_div);

        user_fields_div.appendChild(row);
        user_fields_div.appendChild(hr);

    });

}

// function get_ui() {
//   $.ajax({
//     type: 'GET',
//     url: "/user/profile/" + user_id + '/',
//     contentType: "text/plain",
//     success: function (data) {
//         const fields_data = JSON.parse(document.getElementById('fields_data').textContent);
//         console.log(fields_data);
//     }
//   }
//   )
// }


draw_profile_page();

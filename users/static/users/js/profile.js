const request_user_id = JSON.parse(document.getElementById('request_user_id').textContent);
const requested_user_id = JSON.parse(document.getElementById('requested_user_id').textContent);
const user_fields_div_rows = ["full_name", 'birth_date', 'email',
        'lecture_price', 'platform', 'hashTag', "title"];

const user_feedback_fields = ["all_students", "feedbacks", "rating", "record_creation_datetime"];

var editable_fields = [];
var autocomplete_fields = [];


function email_verification(user){

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

    const obj = JSON.parse(fields_data);

    const user_fields_div = document.getElementById('user-fields');

    obj.forEach(function (item, index) {

        let key = Object.keys(item);

        if (item[key]['editable']) {
                editable_fields.push(key[0]);
            }

        if(user_fields_div_rows.includes(key[0])) {

            let row = document.createElement("div");
            row.className = "row";
            row.style = "width: 715px";

            let column_div = document.createElement("div");
            column_div.className = "col-sm-3";

            let column_name = document.createElement("h6")
            column_name.className = "mb-0";
            column_name.textContent = item[key]['name_in_front'];

            if(item[key]['field_type'] === 'selection') {
                var column_value_input = document.createElement("div");
                column_value_input.className = "autocomplete";
                column_value_input.id = key[0] + "-autocomplete";


                let autoCompleteInput = document.createElement("input");
                autoCompleteInput.className = "autocomplete-input";
                autoCompleteInput.value = item[key]['value'];
                autoCompleteInput.id = key[0];

                let choicesUl = document.createElement("ul");
                choicesUl.className = "autocomplete-result-list";
                choicesUl.style = "border: none;";

                column_value_input.appendChild(autoCompleteInput);
                column_value_input.appendChild(choicesUl);

            }

            else {
                var column_value_input = document.createElement("input");
                column_value_input.className = "col-sm-9";
                column_value_input.style = "border: none; outline: none; background: none";
                column_value_input.value = item[key]['value'];
                column_value_input.id = key[0];
            }

            if (item[key]['field_type'] === "date") {
                column_value_input.type = "date";
            }

            if (!item[key]['editable']) {
                column_value_input.disabled = true;
            }

            let hr = document.createElement("hr")
            column_div.appendChild(column_name);
            row.appendChild(column_div);
            row.appendChild(column_value_input);

            user_fields_div.appendChild(row);
            user_fields_div.appendChild(hr);

        }

        else if (user_feedback_fields.includes(key[0])) {

            const feedbacks_ul = document.getElementById('feedbacks_ul');

            let li = document.createElement("li");
            li.className = "list-group-item d-flex justify-content-between align-items-center flex-wrap";

            let field_name = document.createElement("h6")
            field_name.className = "mb-0";
            field_name.textContent = item[key]['name_in_front'];

            let field_value = document.createElement("span");
            field_value.className = "text-secondary";
            field_value.textContent = item[key]['value'];

            li.appendChild(field_name);
            li.appendChild(field_value);
            feedbacks_ul.appendChild(li);

        }

        else if (key[0] === "image"){
            const profile_img_div = document.getElementById('profile_img');

            let profile_img = document.createElement("img");
            profile_img.className = "rounded-circle";
            profile_img.src = item[key]['value'];
            profile_img.width = 250;
            profile_img.height = 250;

            profile_img_div.appendChild(profile_img);

        }

        else if (key[0] === "description") {
            const description_div = document.getElementById("textarea-description");

            let text_area = document.createElement("textarea");
            text_area.style = "width: 690px; border: none; resize: none; outline:none;" +
                " overflow-x: hidden; overflow-y: auto;  text-align: center"
            text_area.cols = 85;
            text_area.rows = 11;
            text_area.textContent = item[key]['value'];
            text_area.id = key[0];

            description_div.appendChild(text_area);

        }

    });

    // If users who'is requesting actual profile is not the same
        if (request_user_id !== requested_user_id){
         let inputs = document.getElementsByTagName('input');
            for (index = 0; index < inputs.length; ++index) {
                inputs[index].disabled = true;
            }

         document.getElementById("description").disabled = true;

        }

}


function send_changes(data){
  data['csrfmiddlewaretoken'] = $('[name=csrfmiddlewaretoken]').val();

  $.ajax({
    type: "POST",
    // url: `user/profile/${user_id}/`,
    data: data,
    success: function(result){
        result = JSON.parse(result);
        $("#alert").remove();

        var message_div = document.getElementById("bootstrap-messages");
        var crispy_message_div = document.createElement("div");
        crispy_message_div.textContent = result.message;
        crispy_message_div.id = "alert";
        crispy_message_div.role = "alert";

        if (result.status === 200) {
            crispy_message_div.className = "alert alert-success";
        }

        else {
            crispy_message_div.className = "alert alert-danger";
        }

        message_div.appendChild(crispy_message_div);

        $("#alert").fadeTo(2000, 500).slideUp(500, function() {
          $("#alert").slideUp(500);
        });
    }
  });
}



function save_changes() {
    let column_row_pair = {};

    editable_fields.forEach(function (field) {
        let row = document.getElementById(field);

        try {
            column_row_pair[field] = row.value;
        }
        catch (error) {
            console.log(field);
            console.log(error);
        }

    });

    send_changes(column_row_pair);

}

draw_profile_page();


document.querySelectorAll('.autocomplete').forEach(item => {
  item.addEventListener('click', event => {

    function parseResponse(obj){
        let names = []
        obj.forEach(item => {
            names.push(item['name']);
        })
        return names;
    }

    new Autocomplete(item, {
        search : input => {

            const url = `/user/auto-complete/?field=${item.id}&search=${input}`;
            return new Promise(resolve => {
                fetch(url)
                    .then(response=>response.json())
                    .then(data=>{
                    data = parseResponse(data.payload);
                    resolve(data);
                })
            })
        },
    })


  })
})

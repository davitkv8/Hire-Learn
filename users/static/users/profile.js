const user_id = JSON.parse(document.getElementById('user_id').textContent);
const user_fields_div_rows = ['full_name', 'birth_date', 'email',
        'lecture_price', 'platform', 'hashTag'];

const user_feedback_fields = ["all_students", "feedbacks", "rating", "record_creation_datetime"]


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

        // console.log(key[0]);

        if(user_fields_div_rows.includes(key[0])) {

            let row = document.createElement("div");
            row.className = "row";
            row.style = "width: 715px";

            let column_div = document.createElement("div");
            column_div.className = "col-sm-3";

            let column_name = document.createElement("h6")
            column_name.className = "mb-0";
            column_name.textContent = item[key]['name_in_front'];

            let column_value_input = document.createElement("input");
            column_value_input.className = "col-sm-9 text-secondary";
            column_value_input.style = "border: none; outline: none; background: none";
            column_value_input.value = item[key]['value'];
            column_value_input.id = key[0];

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

            console.log(item[key]['value'])

            description_div.appendChild(text_area);

        }

    });

}


draw_profile_page();

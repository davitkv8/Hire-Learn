const user_id = JSON.parse(document.getElementById('user_id').textContent);
var fields = {};
var url = window.location

function getFieldNamings() {
  $.ajax({
    type: 'GET',
    url: "/users/get_field_namings",
    contentType: "text/plain",
    dataType: "json",
    success: function (data) {
        console.log("AJAX")
        fields = data;
    },
    error: function (e) {
      console.log("There was an error with your request")
    }

  },
  );
}


function onFormSubmit(event) {
    event.preventDefault();

    var formData=new FormData();

    // csrf = {csrfmiddlewaretoken: $('[name=csrfmiddlewaretoken]').val()}

    formData.append(
        "csrfmiddlewaretoken", $('[name=csrfmiddlewaretoken]').val()
    );

    formData.append("file1", document.getElementById("file1").files[0]);


    for (const [key, value] of Object.entries(fields)) {
          console.log(value);
          formData.append(`${key}`, document.getElementById(`${value}`).value);
        }

    var xhr=new XMLHttpRequest();

    xhr.onreadystatechange = function() {
        var json = JSON.parse(this.responseText);
        window.location.href = json.success;
    };

    xhr.open("POST",url.pathname,false);
    xhr.send(formData);

}

getFieldNamings();
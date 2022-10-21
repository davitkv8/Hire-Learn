const user_id = JSON.parse(document.getElementById('user_id').textContent);
var fields = {};
var url = window.location

function getFieldNamings() {
  $.ajax({
    type: 'GET',
    url: "/get_field_namings",
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

    formData.append("file1", document.getElementById("file1").files[0]);
    for (const [key, value] of Object.entries(fields)) {
          console.log(value);
          formData.append(`${key}`, document.getElementById(`${value}`).value);
          console.log(document.getElementById(`${value}`));
        }

    var xhr=new XMLHttpRequest();
    xhr.open("POST",url.pathname,true);
    xhr.send(formData);

}

getFieldNamings();
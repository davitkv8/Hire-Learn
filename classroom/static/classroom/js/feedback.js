let feedbackRating;
let receiver_id;
let request_user_id = JSON.parse(document.getElementById('request_user_id').textContent);

document.querySelectorAll('.rating').forEach(item => {
  item.addEventListener('click', event => {
    feedbackRating = item.className[7];
  })
})
function getReceiver(receiver){
    receiver_id = receiver;
}

function leaveFeedback() {
    document.getElementsByClassName('fa-times')[0].click()
    var feedbackText = $('textarea#feedback-text').val();

  $.ajax(
            {
                url: "/classroom/leave_feedback/",
                type: 'POST',
                data: {
                    receiver_id: receiver_id,
                    sender_id: request_user_id,
                    textFeedback: feedbackText,
                    rating: feedbackRating,
                    csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
            },
                success: function (response){
            }
       });
}


function heightResizer(){
    var content_div_width = document.getElementsByClassName("content")[0].clientWidth;
    console.log(content_div_width);
    // It makes inputs responsive
    $("#feedback-text" ).each(function(){
        $(this).css("width", content_div_width * 0.8);
    });
}
heightResizer();
window.addEventListener('resize', heightResizer);
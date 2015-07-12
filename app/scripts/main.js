$(document).ready(function(e) {

  var source = $("#post").html();
  var template = Handlebars.compile(source);
  var placeholder = $('#results');

  // this is the id of the form
  $("#idForm").submit(function(event) {
    event.preventDefault();

    var url = "http://45.55.253.92/post";

    $.ajax({
        type: "POST",
        url: url,
        data: $("#idForm").serialize(),
    }).done(function(response) {
        console.log(response)
        data = JSON.parse(response);
        console.log(data);

        placeholder.html(template(data));


    }).fail(function(e) {
        console.log(e);
        console.log("fail");
      })
      .always(function() {
        console.log("always");
      });

    return false;
  });
});

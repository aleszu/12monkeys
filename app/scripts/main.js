$(document).ready(function(e) {

  var context = [{
    name: 'Mercury',
    description: '1st to Sun'
  }, {
    name: 'Venus',
    description: '2nd to Sun'
  }, {
    name: 'Earth',
    description: '3rd to Sun'
  }, {
    name: 'Mars',
    description: '4th to Sun'
  }, {
    name: 'Jupiter',
    description: '5th to Sun'
  }, {
    name: 'Saturn',
    description: '6th to Sun'
  }, {
    name: 'Uranus',
    description: '7th to Sun'
  }, {
    name: 'Neptune',
    description: '8th to Sun'
  }, ];

  var source = $("#post").html();
  var template = Handlebars.compile(source);

  $('#results')
    .append(template(context));

  $('.post')
    .css('background-image', 'url("https://placehold.it/1600x1600")');

  // $.get('http://45.55.253.92/post', function(data) {
  //   console.log(data);
  // });

  var data = {
    "url": "http://www.nbcnews.com/storyline/confederate-flag-furor/confederate-flag-lowered-forever-south-carolina-capitol-n389996"
  };

  $.ajax({
    method: "POST",
    url: "http://45.55.253.92/",
    data: data.url,
  }).done(function() {
    console.log("done");
  }).fail(function() {
    console.log("fail");
  })
  .always(function() {
    console.log("always");
  });
});

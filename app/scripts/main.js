$(document).ready(function(e){

    var source   = $("#post").html();
    var template = Handlebars.compile(source);
    console.log(template)

    $('#results')
        .append(template)
        .addClass('covers')
        .css('background-image', 'url("https://placehold.it/1600x1600")');

});

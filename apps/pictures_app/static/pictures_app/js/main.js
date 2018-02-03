$(document).ready(function(){
  var obj = document.createElement("audio");
          obj.src=mp3;
          obj.volume=0.10;
          obj.autoPlay=false;
          obj.preLoad=true;

  $("img").click(function(){
    if ($(this).attr('id') == correct_answer) {
      $("blockquote").html("<p><h3>"+response+"<h3></p>");
      $(this).css("border", "10px solid #f3961c");
      obj.play();
    } else {
      $("blockquote").html("<p><h3>Not quite right! Try Again!<h3></p>");
    }
  });

});

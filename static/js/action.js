// imageList = ['1.jpg','2.jpg','3.jpg']
// for(var i = 0; i < imageList.length; i++){
// 	$('#imgBox').append('<img class="mySlides" src=images/'+imageList[i]+' alt="image" width="400" height="280"/>')
// }

var limit = 2;
$('myCheckbox').on('change', function(evt) {
   if($(this).siblings(':checked').length >= limit) {
       this.checked = false;
   }
});

function showDivs(n) {
  var i;
  var x = document.getElementsByClassName("mySlides");

  for (i = 0; i < x.length; i++) {
  	if(i != n){
  		x[i].style.display = "none";  
  	}
  }
  x[n].style.display = "block";

//  Update the number div
    $("#number").text((n+1).toString() + ' / ' + LEN)
}



// var LEN = 2;
var LEN = $('img.mySlides').length;
var questionCounter = 0; //Tracks question number
var selections = []; //Array containing user choices
for(var i = 0; i < LEN; i++){
	selections[i] = []
}
var quiz = $('#quiz'); //Quiz div object

// Display initial question
displayNext();

// Click handler for the 'next' button
$('#next').on('click', function (e) {
    e.preventDefault();

    // Suspend click listener during fade animation
    if(quiz.is(':animated')) {
      return false;
    }
    choose();

    // If no user selection, progress is stopped
    if (selections[questionCounter].length == 0) {
      alert('Please make a selection!');
    } else {
      questionCounter++;
      displayNext();
    }
});

// Click handler for the 'prev' button
$('#prev').on('click', function (e) {
    e.preventDefault();

    if(quiz.is(':animated')) {
      return false;
    }
    choose();
    questionCounter--;
    displayNext();
});

// Click handler for the 'Start Over' button
$('#start').on('click', function (e) {
    e.preventDefault();

    if(quiz.is(':animated')) {
      return false;
    }
    questionCounter = 0;
    selections = [];
    for(var i = 0; i < LEN; i++){
            selections[i] = []
        }
    displayNext();
    $('#start').hide();


    window.location.href='evaluation';
});

// Animates buttons on hover
$('.button').on('mouseenter', function () {
    $(this).addClass('active');
});
$('.button').on('mouseleave', function () {
    $(this).removeClass('active');
});

// Creates and returns the div that contains the questions and 
// the answer selections
function createQuestionElement(index) {
 	showDivs(index);

	var qElement = $('<div>', {
	  id: 'question'
	});
	var radioButtons = createCheckbox(index);
	qElement.append(radioButtons);

	return qElement;
}

function createCheckbox(index){
var checkboxList = $('<ul>');
var item;
boxes = ['<input class="myCheckbox" type="checkbox" name="choice" value="anger" />Anger',
'<input class="myCheckbox" type="checkbox" name="choice" value="sad" />Sad',
'<input class="myCheckbox" type="checkbox" name="choice" value="disgust" />Disgust',
'<input class="myCheckbox" type="checkbox" name="choice" value="excitement" />Excitement',
'<input class="myCheckbox" type="checkbox" name="choice" value="fear" />Fear',
'<input class="myCheckbox" type="checkbox" name="choice" value="happy" />Happy']

for(var i = 0; i < boxes.length; i++){
	item = $('<li>');
	var box = boxes[i];
	item.append(box);
	checkboxList.append(item)
}
return checkboxList
}
// Reads the user selection and pushes the value to an array
function choose() {
// selections[questionCounter] = +$('input[name="answer"]:checked').val();
var boxList = document.getElementsByName("choice");
var tList= [];
for(var i = 0; i < boxList.length; i++){
	if(boxList[i].checked){
		tList.push(boxList[i].value)	
	}
}
selections[questionCounter] = tList;
}

// Displays next requested element
function displayNext() {
quiz.fadeOut(function() {
  $('#question').remove();
  
  if(questionCounter < LEN){
    var nextQuestion = createQuestionElement(questionCounter);
    quiz.append(nextQuestion).fadeIn();
    if (!(selections[questionCounter].length == 0)) {
    	for (var i = 0; i < selections[questionCounter].length; i++){
 			$('input[value='+selections[questionCounter][i]+']').prop('checked', true);
    	}
    }
    
    // Controls display of 'prev' button
    if(questionCounter === 1){
      $('#prev').show();
    } else if(questionCounter === 0){
      
      $('#prev').hide();
      $('#next').show();
    }
  }else {// The end of questionnaire, start to post form to flask
    // var scoreElem = displayScore();
    // quiz.append(scoreElem).fadeIn();
    var resDic = {};
    for(var i = 0; i < selections.length; i++){
    	resDic[i] = selections[i]
    }

    // alert(resDic.toString());

    $.ajax({
        type: "POST",
        url: "http://127.0.0.1:5000/evaluation",
        contentType: "application/json;charset=utf-8",
        // data:{"name":"yd","pwd":"123456"},
        data: JSON.stringify({"data": resDic}),
        dataType: "json",
        success:function (message) {
//            alert("提交成功"+JSON.stringify(message));
        },
        error:function (message) {
//            alert("提交失败"+JSON.stringify(message));
        }
    });
//    alert(selections)
    alert("Thank you for your participation!");
    $('#next').hide();
    $('#prev').hide();
    $('#start').show();
  }
});
}
  
  // Computes score and returns a paragraph element to be displayed
  // function displayScore() {
  //   var score = $('<p>',{id: 'question'});
  //   var numCorrect = 0;
  //   for (var i = 0; i < selections.length; i++) {
  //     if (selections[i] === questions[i].correctAnswer) {
  //       numCorrect++;
  //     }
  //   }
  //   score.append(' Albert Einstein says : Υου got ' + numCorrect + ' questions out of ' +
  //                10 + ' right !!');
	  
  //   return score ;
  // }
/**
 * Created by raeste on 09.03.17.
 */
function showAnswer() {
    var right_answer = document.getElementById('right_answer');
    var wrong_answer = document.getElementById('wrong_answer');
    var right_link = document.getElementById('right_link');
    var wrong_link = document.getElementById('wrong_link');

    var response = document.getElementById('response');
    var answer = document.getElementById('answer')
    var answer_txt = document.getElementById('answer_text')
    var ans = answer_txt.textContent;
    ans = ans.replace(/\s/g,'');
    user_response = response.value.replace(/\s/g,'');

    
    console.log(ans + ", " +user_response);
    if (ans.toUpperCase() === user_response.toUpperCase()) {
        right_answer.style.display = 'block';
        answer_txt.className += ' green';
    } else {
        wrong_answer.style.display = 'block';
        answer_txt.className += ' red';
    }

    if (answer.style.display == 'block') {
        if (ans.toUpperCase() === user_response.toUpperCase()) {
            right_link.click();
        } else {
            wrong_link.click();
        }
    }
    answer.style.display = 'block';

}
function focusTextBox(){
    document.getElementById('response').focus();
}
function detect(event) {
    var char = event.which || event.keyCode;
    if (char == 13) {
        showAnswer();
    }
}
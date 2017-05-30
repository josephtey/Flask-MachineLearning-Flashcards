/**
 * Created by raeste on 09.03.17.
 */

function showAnswer() {
    stopTimer()
    var right_answer = document.getElementById('right_answer');
    var wrong_answer = document.getElementById('wrong_answer');
    var right_link = document.getElementById('right_link');
    var wrong_link = document.getElementById('wrong_link');
    var buttons = document.getElementById('buttons')

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
    buttons.style.display = 'none'

}
function stopTimer(){
    timer.stop()
    var duration = parseInt(document.getElementById('my-stopwatch').innerText)

    return duration
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

var Stopwatch = function(elem, options) {

  var timer       = createTimer(),
      offset,
      clock,
      interval;

  // default options
  options = options || {};
  options.delay = options.delay || 1;

  // append elements     
  elem.appendChild(timer);

  // initialize
  reset();
  start();
  // private functions
  function createTimer() {
    return document.createElement("span");
  }

  function createButton(action, handler) {
    var a = document.createElement("a");
    a.href = "#" + action;
    a.innerHTML = action;
    a.addEventListener("click", function(event) {
      handler();
      event.preventDefault();
    });
    return a;
  }

  function start() {
    if (!interval) {
      offset   = Date.now();
      interval = setInterval(update, options.delay);
    }
  }

  function stop() {
    if (interval) {
      clearInterval(interval);
      interval = null;
    }
  }

  function reset() {
    clock = 0;
    render();
  }

  function update() {
    clock += delta();
    render();
  }

  function render() {
    timer.innerHTML = Math.round(clock/1000);
  }

  function delta() {
    var now = Date.now(),
        d   = now - offset;

    offset = now;
    return d;
  }

  // public API
  this.start  = start;
  this.stop   = stop;
  this.reset  = reset;
}
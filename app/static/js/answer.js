/**
 * Created by raeste on 09.03.17.
 */
function ld(a, b) {
    if(a.length == 0) return b.length;
    if(b.length == 0) return a.length;

    var matrix = [];

    // increment along the first column of each row
    var i;
    for(i = 0; i <= b.length; i++){
      matrix[i] = [i];
    }

    // increment each column in the first row
    var j;
    for(j = 0; j <= a.length; j++){
      matrix[0][j] = j;
    }

    // Fill in the rest of the matrix
    for(i = 1; i <= b.length; i++){
      for(j = 1; j <= a.length; j++){
        if(b.charAt(i-1) == a.charAt(j-1)){
          matrix[i][j] = matrix[i-1][j-1];
        } else {
          matrix[i][j] = Math.min(matrix[i-1][j-1] + 1, // substitution
                                  Math.min(matrix[i][j-1] + 1, // insertion
                                           matrix[i-1][j] + 1)); // deletion
        }
      }
    }

    return matrix[b.length][a.length];
  }

function showAnswer() {
    stopTimer()
    var right_answer = document.getElementById('right_answer');
    var wrong_answer = document.getElementById('wrong_answer');
    var right_link = document.getElementById('right_link');
    var wrong_link = document.getElementById('wrong_link');
    var buttons = document.getElementById('buttons');

    var response = document.getElementById('response');
    var answer = document.getElementById('answer');
    var answer_txt = document.getElementById('answer_text');
    var ans = answer_txt.textContent;

    ans = ans.replace(/\s/g,'');
    user_response = response.value.replace(/\s/g,'');

    if (answer.style.display != 'block'){
      if (ld(ans.toUpperCase(), user_response.toUpperCase()) <= 2) {
          // right_answer.style.display = 'block';
          answer_txt.className += ' green';
          localStorage.setItem('outcome', true)
      } else {
          // wrong_answer.style.display = 'block';
          answer_txt.className += ' red';
          localStorage.setItem('outcome', false)
      }
    }

    // if (answer.style.display == 'block') {
    //     if (localStorage.getItem('outcome') == 'true') {
    //         console.log('correct');
    //         right_link.click();
    //     } else {
    //         console.log('wrong')
    //         wrong_link.click();
    //
    //     }
    // }
    if (localStorage.getItem('outcome') == 'true') {
      setTimeout(function(){
        console.log('correct');
        right_link.click();
      }, 500);
    } else {
      setTimeout(function(){
        console.log('wrong')
        wrong_link.click();
      }, 3000);
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
    if (timer.innerText == '15'){
      showAnswer();
    }
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
var SecondStopwatch = function(elem, options) {

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
    if (timer.innerText == '5'){
      document.getElementById('next').click();
    }
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

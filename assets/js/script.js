"use strict";
//selecting all required elements
const start_btn = document.querySelector(".start_btn button");
const info_box = document.querySelector(".info_box");
const exit_btn = info_box.querySelector(".buttons .quit");
const continue_btn = info_box.querySelector(".buttons .restart");
const quiz_box = document.querySelector(".quiz_box");
const option_list = document.querySelectorAll(".option_list");
const options = document.querySelectorAll(".option_list .option")
const timeText = document.querySelector(".timer .time_left_txt");
const timeCount = document.querySelector(".timer .timer_sec");
const total_que = document.querySelector("footer .total_que");


// if startQuiz button clicked
start_btn.onclick = () => {
    info_box.classList.add("activeInfo"); //show info box
    console.log(options.length)
}

// if exitQuiz button clicked
exit_btn.onclick = () => {
    info_box.classList.remove("activeInfo"); //hide info box
}

// if continue Quiz button clicked
continue_btn.onclick = () => {
    info_box.classList.remove("activeInfo"); //hide info box
    let seconds = option_list.length * 10
    time(seconds)
    quiz_box.classList.add("activeQuiz"); //show quiz box
    total_que.textContent = `${option_list.length} Questions`

}

// set onclick attribute to all available options
for (let i = 0; i < options.length; i++) {
    options[i].setAttribute("onclick", "optionSelected(this)");
}

function optionSelected(answer) {
    console.log(answer)
    let radioButton = answer.querySelector('#radios');
    radioButton.checked = true;
}

function time(second) {
    const counter = setInterval(timer, 1000)

    function timer() {
        timeCount.textContent = second;
        second--;
        if (second < 9) { //if timer is less than 9
            let addZero = timeCount.textContent;
            timeCount.textContent = "0" + addZero; //add a 0 before time value
        }
        if (second < 0) { //if timer is less than 0
            clearInterval(counter); //clear counter
            timeText.textContent = 'Time off'
            for (let i = 0; i < options.length; i++) {
                options[i].classList.add('disabled'); //once user select an option then disabled all options
            }
        }
    }
}

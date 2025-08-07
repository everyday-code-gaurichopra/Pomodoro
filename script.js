let sessionLength = 25;
let breakLength = 5;
let timeLeft = sessionLength * 60;
let isRunning = false;
let isSession = true;
let timerInterval = null;

const timeLeftDisplay = document.getElementById("time-left");
const timerLabel = document.getElementById("timer-label");
const sessionLengthDisplay = document.getElementById("session-length");
const breakLengthDisplay = document.getElementById("break-length");

const startBtn = document.getElementById("start-stop");
const resetBtn = document.getElementById("reset");

const sessionInc = document.getElementById("session-increment");
const sessionDec = document.getElementById("session-decrement");
const breakInc = document.getElementById("break-increment");
const breakDec = document.getElementById("break-decrement");

function updateDisplays() {
  sessionLengthDisplay.textContent = sessionLength;
  breakLengthDisplay.textContent = breakLength;
  if (!isRunning) {
    timeLeft = (isSession ? sessionLength : breakLength) * 60;
    updateTimeDisplay();
  }
}

function updateTimeDisplay() {
  let minutes = Math.floor(timeLeft / 60);
  let seconds = timeLeft % 60;
  timeLeftDisplay.textContent =
    `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
}

function toggleButtons(disable) {
  sessionInc.disabled = disable;
  sessionDec.disabled = disable;
  breakInc.disabled = disable;
  breakDec.disabled = disable;
}

function startTimer() {
  toggleButtons(true);
  timerInterval = setInterval(() => {
    timeLeft--;
    if (timeLeft < 0) {
      isSession = !isSession;
      timerLabel.textContent = isSession ? "Session" : "Break";
      timeLeft = (isSession ? sessionLength : breakLength) * 60;
    }
    updateTimeDisplay();
  }, 1000);
}

function stopTimer() {
  clearInterval(timerInterval);
  toggleButtons(false);
}

startBtn.addEventListener("click", () => {
  if (!isRunning) {
    startTimer();
    startBtn.textContent = "Pause";
  } else {
    stopTimer();
    startBtn.textContent = "Start";
  }
  isRunning = !isRunning;
});

resetBtn.addEventListener("click", () => {
  stopTimer();
  isRunning = false;
  isSession = true;
  sessionLength = 25;
  breakLength = 5;
  timerLabel.textContent = "Session";
  startBtn.textContent = "Start";
  updateDisplays();
});

sessionInc.addEventListener("click", () => {
  sessionLength++;
  updateDisplays();
});
sessionDec.addEventListener("click", () => {
  if (sessionLength > 0) sessionLength--;
  updateDisplays();
});
breakInc.addEventListener("click", () => {
  breakLength++;
  updateDisplays();
});
breakDec.addEventListener("click", () => {
  if (breakLength > 0) breakLength--;
  updateDisplays();
});

updateDisplays();
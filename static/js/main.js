const constraints = {video: true};

navigator.mediaDevices.getUserMedia(constraints)
.then(function(mediaStream) {
  var video = document.querySelector('video');
  video.srcObject = mediaStream;
  video.onloadedmetadata = function(e) {
    video.play();
  };
})
.catch(function(err) { console.log(err.name + ": " + err.message); }); 


function record() {
  let timersecs = document.getElementById('timer-seconds').value;
}
  
var timerbutton = document.getElementById("timer-button");
const uploadbutton = document.getElementById("upload-video");

var timerform = document.getElementById("timer-form");
timerform.addEventListener("submit", record(), false);


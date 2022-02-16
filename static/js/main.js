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

function paddedFormat(x){
  return x;
}
  
  
var timerbutton = document.getElementById("timer-button");
const uploadbutton = document.getElementById("upload-video");
var form = document.getElementById('timer-form')

form.addEventListener("submit", function(e) {
    let timersecs = parseInt(document.getElementById('timer-seconds').value);
    let videooverlay = document.getElementById('countdown-text');
    var mins = 0;
    var secs = 0;
  
    let countInterval = setInterval (function() {
      mins = parseInt(timersecs / 60);
      secs = parseInt(timersecs % 60); 
  
      videooverlay.textContent = `${paddedFormat(mins)}:${paddedFormat(secs)}`;
      timersecs = timersecs - 1;
      if (timersecs < 0) { clearInterval(countInterval) };
  }, 1000);
})

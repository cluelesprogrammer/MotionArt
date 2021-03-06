const constraints = {video: true};

if (navigator.mediaDevices === undefined) {
  navigator.mediaDevices = {};
}

// Some browsers partially implement mediaDevices. We can't just assign an object
// with getUserMedia as it would overwrite existing properties.
// Here, we will just add the getUserMedia property if it's missing.
if (navigator.mediaDevices.getUserMedia === undefined) {

  
  navigator.mediaDevices.getUserMedia = function(constraints) {


    // First get ahold of the legacy getUserMedia, if present
    var getUserMedia = navigator.webkitGetUserMedia || navigator.mozGetUserMedia;
    alert(getUserMedia);

    // Some browsers just don't implement it - return a rejected promise with an error
    // to keep a consistent interface
    if (!getUserMedia) {
     
      return Promise.reject(new Error('getUserMedia is not implemented in this browser'));
    }
  
    // Otherwise, wrap the call to the old navigator.getUserMedia with a Promise
    return new Promise(function(resolve, reject) {
      getUserMedia.call(navigator, constraints, resolve, reject);
    });
  }
}

navigator.mediaDevices.getUserMedia(constraints)
.then(function(stream) {
  var video = document.querySelector('video');
  // Older browsers may not have srcObject
  if ("srcObject" in video) {
    video.srcObject = stream;
    
  } else {
    // Avoid using this in new browsers, as it is going away.
    video.src = window.URL.createObjectURL(stream);
  }
  
  video.onloadedmetadata = function(e) {
    video.play();
  };
})
.catch(function(err) {
  alert('catch error');
  console.log(err.name + ": " + err.message);
});

function paddedFormat(x){
  return x;
}
  
var timerbutton = document.getElementById("timer-button");
let uploadbutton = document.getElementById("upload-video");
var form = document.getElementById('timer-form')

form.addEventListener("submit", function(e) {
    let timersecs = parseInt(document.getElementById('timer-seconds').value);
    setTimeout(() => {
      


      }
    ,timersecs);

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

const fileSelect = document.getElementById("upload-video"),
fileElem = document.getElementById("fileElem");

fileSelect.addEventListener("click", function (e) {
  if (fileElem) {
    fileElem.click();
  }
}, false);

fileElem.addEventListener("change", handleFiles, false);
function handleFiles() {
  const fileList = this.files; /* now you can work with the file list */
  vid = fileList[0]
}
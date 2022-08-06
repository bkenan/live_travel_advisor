URL = window.URL || window.webkitURL;

var gumStream;                  
var rec;                         
var input;                         

var AudioContext = window.AudioContext || window.webkitAudioContext;
var audioContext //audio context to help us record
var recordButton = document.getElementById("recordButton");
var stopButton = document.getElementById("stopButton");

//add events to those 2 buttons
recordButton.addEventListener("click", startRecording);
stopButton.addEventListener("click", stopRecording);


function startRecording() {
    console.log("recordButton clicked");

    var constraints = { audio: true, video:false }

    recordButton.disabled = true;
    stopButton.disabled = false
 
    navigator.mediaDevices.getUserMedia(constraints).then(function(stream) {
        console.log("getUserMedia() success, stream created, initializing Recorder.js ...");

        audioContext = new AudioContext();

        /*  assign to gumStream for later use  */
        gumStream = stream;

        /* use the stream */
        input = audioContext.createMediaStreamSource(stream);

        rec = new Recorder(input,{numChannels:1})

        //start the recording process
        rec.record()

        console.log("Recording started");

    }).catch(function(err) {
        recordButton.disabled = false;
        stopButton.disabled = true
    });
}

function stopRecording() {
    console.log("stopButton clicked");

    //disable the stop button, enable the record too allow for new recordings
    stopButton.disabled = true;
    recordButton.disabled = false;


    //tell the recorder to stop the recording
    rec.stop();

    //stop microphone access
    gumStream.getAudioTracks()[0].stop();

    rec.exportWAV(createResultLink);
}

function createResultLink(blob) {

    var xhr=new XMLHttpRequest();
    var fd=new FormData();
    fd.append("audio_data",blob);
    xhr.open("POST","/",true);
    xhr.send(fd);

    function submit() {
        setTimeout(
          function() {
            document.getElementById("disable").classList.remove('disabled');

          }, 15000);
      }
      submit();
}
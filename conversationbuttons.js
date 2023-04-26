const recordButton = document.getElementById('record-btn');
const playButton = document.getElementById('play-btn');
const sendButton = document.getElementById('send-btn');

let mediaRecorder;
let recordedChunks = [];

const handleDataAvailable = (event) => {
    console.log('data available');
    recordedChunks.push(event.data);
}

const handleStop = (event) => {
    console.log('stop');
    const recordedBlob = new Blob(recordedChunks, { type: 'audio/wav' });
    playButton.disabled = false;
    sendButton.disabled = false;
    playButton.onclick = () => {
        const audioElement = document.createElement('audio');
        audioElement.src = URL.createObjectURL(recordedBlob);
        audioElement.play();
    }
    sendButton.onclick = () => {
        // TODO: Send the recording data to another user or server
    }
}

recordButton.onclick = () => {
    if (recordButton.textContent === 'Record') {
        recordButton.textContent = 'Stop';
        recordedChunks = [];
        navigator.mediaDevices.getUserMedia({ audio: true })
            .then(stream => {
                mediaRecorder = new MediaRecorder(stream);
                mediaRecorder.addEventListener('dataavailable', handleDataAvailable);
                mediaRecorder.addEventListener('stop', handleStop);
                mediaRecorder.start();
                console.log('started recording');
            });
    } else {
        recordButton.textContent = 'Record';
        mediaRecorder.stop();
        console.log('stopped recording');
    }
}

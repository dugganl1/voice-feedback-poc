let mediaRecorder;
let audioChunks = [];
let isRecording = false;
let timerInterval;
let startTime;

const recordButton = document.getElementById("recordButton");
const timer = document.getElementById("timer");
const fileUpload = document.getElementById("fileUpload");
const loading = document.getElementById("loading");
const resultContent = document.getElementById("resultContent");

// Recording functionality
recordButton.addEventListener("click", async () => {
  if (!isRecording) {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorder = new MediaRecorder(stream);

      mediaRecorder.ondataavailable = (event) => {
        audioChunks.push(event.data);
      };

      mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(audioChunks, { type: "audio/webm" });
        await uploadAudio(audioBlob);
      };

      audioChunks = [];
      mediaRecorder.start();
      isRecording = true;
      recordButton.classList.add("recording");
      recordButton.querySelector(".record-text").textContent = "Stop Recording";
      startTimer();
    } catch (err) {
      console.error("Error accessing microphone:", err);
      alert("Error accessing microphone. Please ensure you have given permission.");
    }
  } else {
    stopRecording();
  }
});

// File upload functionality
fileUpload.addEventListener("change", async (event) => {
  const file = event.target.files[0];
  if (file) {
    await uploadAudio(file);
  }
});

async function uploadAudio(audioData) {
  loading.classList.remove("hidden");
  resultContent.textContent = "";

  const formData = new FormData();
  formData.append("file", audioData);

  try {
    const response = await fetch("/upload-audio", {
      method: "POST",
      body: formData,
    });

    const result = await response.json();

    if (response.ok) {
      displayResults(result);
    } else {
      throw new Error(result.detail || "Upload failed");
    }
  } catch (error) {
    console.error("Error:", error);
    resultContent.textContent = `Error: ${error.message}`;
  } finally {
    loading.classList.add("hidden");
  }
}

function displayResults(result) {
  const transcription = result.transcription.text;
  const analysis = result.analysis.summary;

  resultContent.innerHTML = `
        <h3>Transcription:</h3>
        <p>${transcription}</p>
        <h3>Analysis:</h3>
        <div class="analysis-content">
            ${analysis.replace(/\*\*/g, "<strong>").replace(/\n/g, "<br>")}
        </div>
    `;
}

function stopRecording() {
  mediaRecorder.stop();
  mediaRecorder.stream.getTracks().forEach((track) => track.stop());
  isRecording = false;
  recordButton.classList.remove("recording");
  recordButton.querySelector(".record-text").textContent = "Start Recording";
  stopTimer();
}

function startTimer() {
  startTime = Date.now();
  updateTimer();
  timerInterval = setInterval(updateTimer, 1000);
}

function stopTimer() {
  clearInterval(timerInterval);
  timer.textContent = "00:00";
}

function updateTimer() {
  const elapsed = Math.floor((Date.now() - startTime) / 1000);
  const minutes = Math.floor(elapsed / 60)
    .toString()
    .padStart(2, "0");
  const seconds = (elapsed % 60).toString().padStart(2, "0");
  timer.textContent = `${minutes}:${seconds}`;
}

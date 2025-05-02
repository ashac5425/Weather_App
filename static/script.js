
// function fetchWeather() {
//     const city = document.getElementById('city').value;
//     fetch(`/getweather?city=${city}`)
//         .then(response => response.json())
//         .then(data => {
//             const resultDiv = document.getElementById('weatherResult');
//             if (data.error) {
//                 resultDiv.innerHTML = `<p>Error: ${data.error}</p>`;
//             } else {
//                 resultDiv.innerHTML = `
//                     <p><strong>City:</strong> ${data.city}</p>
//                     <p><strong>Temperature:</strong> ${data.temperature}</p>
//                     <p><strong>Humidity:</strong> ${data.humidity}</p>
//                     <p><strong>Wind:</strong> ${data.wind}</p>
//                 `;
//             }
//         })
//         .catch(error => console.error('Error:', error));
// }


// Fetch weather for a city
function fetchWeather(cityFromSpeech = null) {
    const city = cityFromSpeech || document.getElementById('city').value;
    fetch(`/getweather?city=${city}`)
        .then(response => response.json())
        .then(data => {
            const resultDiv = document.getElementById('weatherResult');
            if (data.error) {
                resultDiv.innerHTML = `<p>Error: ${data.error}</p>`;
            } else {
                resultDiv.innerHTML = `
                    <p><strong>City:</strong> ${data.city}</p>
                    <p><strong>Temperature:</strong> ${data.temperature}</p>
                    <p><strong>Humidity:</strong> ${data.humidity}</p>
                    <p><strong>Wind:</strong> ${data.wind}</p>
                `;
                textToSpeech(
                    `The weather in ${data.city} is ${data.temperature}, humidity is ${data.humidity}, and wind speed is ${data.wind}.`
                );
            }
        })
        .catch(error => console.error('Error:', error));
}

// Variables for recording
let mediaRecorder;
let audioChunks;

// Start recording microphone
function startRecording() {
    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
            mediaRecorder = new MediaRecorder(stream);
            audioChunks = [];

            mediaRecorder.ondataavailable = event => {
                audioChunks.push(event.data);
            };
            mediaRecorder.onstop = function() {
                const blob = new Blob(audioChunks, { type: 'audio/webm' });
                console.log("Sending audio blob, size:", blob.size);
            
                const formData = new FormData();
                formData.append('audio', blob, 'speech.webm'); // MUST use 'audio' to match Flask
            
                fetch('/speechtotext', {
                    method: 'POST',
                    body: formData,
                })
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Speech recognition failed');
                    }
                    return response.json();
                })
                .then(data => {
                    console.log('City:', data.city);
                    fetchWeather(data.city); // use city from voice
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('Could not recognize your speech. Please try again.');
                });
            };
            
            

            mediaRecorder.start();

            // Automatically stop recording after 3 seconds
            setTimeout(() => {
                mediaRecorder.stop();
            }, 6000);
        })
        .catch(error => console.error('Error accessing microphone:', error));
}

// Convert text to speech
function textToSpeech(text) {
    fetch('/texttospeech', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text })
    })
    .then(response => response.blob())
    .then(blob => {
        const url = URL.createObjectURL(blob);
        const audioPlayer = document.getElementById('audioPlayer');
        audioPlayer.src = url;
        audioPlayer.style.display = 'block';
    })
    .catch(error => console.error('Error in text-to-speech:', error));
}

// Play the audio response
function playAudio() {
    const audioPlayer = document.getElementById('audioPlayer');
    audioPlayer.play();
}

import speech_recognition as sr
from faster_whisper import WhisperModel
import urllib.request
import json

print("Loading Dhwani Mitra AI...")

# Load Whisper model
model = WhisperModel(
    "base",
    device="cpu",
    compute_type="int8"
)

# ==========================================
# RECORD VOICE
# ==========================================

recognizer = sr.Recognizer()

with sr.Microphone() as source:

    print("\nDhwani Mitra is listening...")
    print("Please speak your complaint...")

    recognizer.adjust_for_ambient_noise(source, duration=1)

    audio = recognizer.listen(source)

# Save recorded audio
with open("voice_input.wav", "wb") as file:
    file.write(audio.get_wav_data())

print("\nProcessing speech...")

# ==========================================
# SPEECH TO TEXT
# ==========================================

segments, info = model.transcribe(
    "voice_input.wav",
    beam_size=5
)

text = " ".join(segment.text for segment in segments).strip()
if not text:
    print("\nNo speech detected.")
    print("Please run Dhwani Mitra again and speak your complaint.")
    exit()

print("\n================================")
print("      DHWANI MITRA RESULT")
print("================================")

print("Detected Language:", info.language)
print("Complaint:", text)

# ==========================================
# SEND COMPLAINT TO AQUASHIELD AI API
# ==========================================

print("\nSending complaint to AquaShield AI...")

data = json.dumps({
    "complaint": text
}).encode("utf-8")

request = urllib.request.Request(
    "http://127.0.0.1:8000/predict",
    data=data,
    headers={
        "Content-Type": "application/json"
    },
    method="POST"
)

try:

    with urllib.request.urlopen(request) as response:

        result = json.loads(response.read().decode("utf-8"))

    print("\n================================")
    print("       AI ANALYSIS")
    print("================================")

    print("Category  :", result.get("category"))
    print("Department:", result.get("department"))
    print("Priority  :", result.get("priority"))
    print("Severity  :", result.get("severity"))

    print("\n================================")
    print("Dhwani Mitra + AquaShield AI")
    print("Integration Successful!")
    print("================================")

except Exception as e:

    print("\nCould not connect to AquaShield AI API.")
    print("Make sure api_service.py server is running.")
    print("Error:", e)
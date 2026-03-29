# NeuroBin

**An AI-Assisted Real-Time Multimodal Cognitive Support System for Dementia Patients Aging in Place**

NeuroBin is a comprehensive software suite built to enhance the safety, dignity, and independence of dementia patients living in their own homes. It connects patients with an entire care network, facilitating seamless symptom tracking, location geofencing, telemedicine, proactive medication management, and AI-powered memory aids.

## Main Features

1. **AI Face Recognition**: Live WebRTC camera integration helping dementia patients interact with familiar faces using OpenCV and DeepFace.
2. **AI Emotion Recognition**: Real-time affective state scanning and logging for caregiver monitoring via secure WebRTC feeds.
3. **Secure Authentication**: AES-256 equivalent encrypted login with JWT-based role authorization for clinical practitioners, families, caretakers, and patients.
4. **Proactive Medication Management**: Dashboard integration to track medicine regimens including dosages, frequencies, and visual pill identifiers. Includes an automated countdown timer and adherence logging.
5. **Advanced Geofencing module**: Establish defined "Safe Zones" using geographic coordinates and monitor live patient telemetry and deviation events.
6. **Care Network Linkage**: Fully linked data structures tying multiple caretakers and primary doctors to a central patient profile, enabling seamless collaboration.
7. **Telemedicine Meetings**: Direct online scheduling of checkups and clinical consultations directly from the web interface, organized by timeline.
8. **WebRTC Emergency Intercom**: Immediate one-click voice and video call interfacing directly between caregivers and patients during fall alerts or cognitive distress.
9. **Premium Glassmorphic UI**: A responsive, calming, and highly accessible user interface built entirely with Vanilla CSS for zero-dependency high-performance operation on edge devices and patient tablets.

## Quick Start Instructions

### 1. Database Setup
Use Docker Compose to start the PostgreSQL database (which includes `pgvector` and `postgis` support).

From the root directory:
```bash
docker compose up -d
```

### 2. Environment Configuration
Ensure `Backend/.env` exists. You can copy `Backend/.env.example` as a template:

**Linux / macOS:**
```bash
cp Backend/.env.example Backend/.env
```

**Windows (PowerShell):**
```powershell
Copy-Item Backend/.env.example Backend/.env
```
*Note: Update `POSTGRES_DB=test_db` in the `.env` file if using the default `db_test` service from `docker-compose.yml`. Ensure the username and password match.*

### 3. Backend Setup
Navigate to the `Backend/` directory and set up the virtual Python environment.

**Linux / macOS:**
```bash
cd Backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
fastapi dev src/main.py
```

**Windows:**
```powershell
cd Backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
fastapi dev src/main.py
```

Find the auto-generated interactive OpenAPI docs at `http://localhost:8000/docs`.

### 4. Frontend Setup
The frontend requires no build steps or bundlers. Simply serve the `Frontend/` folder using Python's built-in HTTP server in a new terminal.

**Linux / macOS:**
```bash
cd Frontend
python3 -m http.server 3000
```

**Windows:**
```powershell
cd Frontend
python -m http.server 3000
```

### 5. Accessing the Application (Important!)
Open your web browser and navigate exactly to:

👉 **http://localhost:3000** 👈

⚠️ **CRITICAL: Do NOT use `127.0.0.1:3000`, `0.0.0.0:3000`, or your local network IP (like `192.168.x.x`).**
Modern web browsers aggressively block camera and microphone access (`getUserMedia` permissions) unless the site is served over standard HTTPS *or* exactly on `localhost`. If you see "Camera permission denied" or a blank gray box in the AI recognition tabs, verify your URL bar says `localhost:3000`.

## Troubleshooting

- **Camera Not Connecting / Permission Errors:** Ensure you are accessing the app explicitly via `http://localhost:3000`. Browsers strictly require `localhost` (or HTTPS) for WebRTC APIs. Additionally, verify that no other application (like Zoom or Teams) is currently using and locking the webcam.
- **Initial AI Lag / Frozen Video:** The first time you execute the Face Recognition or Emotion Recognition tools, the `deepface` library will automatically download required pre-trained model weights (such as VGG-Face or facial expression models). This may take a few minutes depending on your internet connection speed. The UI will appear frozen during this background download.
- **Database Connection Refused:** Make sure Docker Desktop daemon or Docker Engine is running on your machine and that `docker compose up -d` completed successfully without errors. Verify your `Backend/.env` variables match the Postgres configurations defined in `docker-compose.yml`.
- **Missing Demo Data / Empty Tables:** If you don't see any patients or caretakers after logging in during a fresh install, ensure you run the seeding script. Activate your virtual environment and execute the following from the Backend directory: `python src/scripts/seed_demo_users.py`.
- **Login Failing:** Make sure the backend server (FastAPI) is running at `http://localhost:8000`. The frontend `api.js` connects directly to this port by default.

## Testing and Validation
- See `context.md` in the root repository to review the full feature accomplishment checklist.
- Log in utilizing the `admin` credentials to review geofences, patient relationships, and backend analytics.
- Log in utilizing a `caretaker` account to test the native UI workflow for the specialized Face Recognition and Emotion Tracking tabs.

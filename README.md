# NeuroBin

**An AI-Assisted Real-Time Multimodal Cognitive Support System for Dementia Patients Aging in Place**

NeuroBin is a comprehensive software suite built to enhance the safety, dignity, and independence of dementia patients living in their own homes. It connects patients with an entire care network, facilitating seamless symptom tracking, location geofencing, telemedicine, and proactive medication management.

## Main Features

1. **Secure Authentication**: AES-256 equivalent encrypted login with JWT-based role authorization for clinical practitioners, families, and caretakers.
2. **Proactive Medication Management**: Dashboard integration to track medicine regimens including dosages, frequencies, and visual pill identifiers. Includes an automated countdown timer and adherence logging.
3. **Advanced Geofencing module**: Establish defined "Safe Zones" using geographic coordinates and monitor live patient telemetry and deviation events.
4. **Care Network Linkage**: Fully linked data structures tying multiple caretakers and primary doctors to a central patient profile, enabling seamless collaboration.
5. **Telemedicine Meetings**: Direct online scheduling of checkups and clinical consultations directly from the web interface, organized by timeline.
6. **WebRTC Emergency Intercom**: Immediate one-click voice and video call interfacing directly between caregivers and patients during fall alerts or cognitive distress.
7. **Premium Glassmorphic UI**: A responsive, calming, and highly accessible user interface built entirely with Vanilla CSS for zero-dependency high-performance operation on edge devices and patient tablets.

## Quick Start Instructions

### Running the Backend

1. **Database Setup**: Use Docker Compose to start the PostgreSQL database (with `pgvector` and `postgis` support).
   From the root directory:
   ```bash
   docker compose up -d
   ```

2. **Environment Configuration**:
   Ensure `Backend/.env` exists. You can copy `Backend/.env.example` as a template:
   ```bash
   cp Backend/.env.example Backend/.env
   ```
   *Note: Update `POSTGRES_DB=test_db` if using the default `db_test` service from `docker-compose.yml`.*

3. **Python Environment**:
   Navigate to the `Backend/` directory and set up the virtual environment:
   ```bash
   cd Backend
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

4. **Start the Server**:
   Launch the FastAPI development server:
   ```bash
   fastapi dev src/main.py
   ```

5. **Interactive Docs**:
   Find the auto-generated interactive OpenAPI docs at `http://localhost:8000/docs` or `http://localhost:8000/redoc`.

### Running the Frontend

1. The frontend requires no build steps or bundlers.
2. Simply open `Frontend/index.html` in any modern web browser or use a quick static file server from the Frontend/ directory:
   ```bash
   # From Frontend/ directory
   cd Frontend
   python3 -m http.server 3000
   ```
   Navigate your browser to `http://localhost:3000/index.html`.

### Testing and Validation
- See `context.md` in the root repository to review the full accomplishment checklist.
- When evaluating the Frontend, try `admin` credentials to log into the main dashboard, configure geofences, and use the simulated WebRTC interphone.

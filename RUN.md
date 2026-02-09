# How to Run DocWeaver

Follow these steps to run the DocWeaver application (Backend + Frontend).

## Prerequisites

1.  **Backend**: Python installed with dependencies (`pip install -r requirements.txt` in `clinical_orchestrator`).
2.  **Frontend**: Node.js installed with dependencies (`npm install` in `frontend`).

## 1. Start the Backend API (FastAPI)

Open a new terminal window and navigate to the `clinical_orchestrator` directory:

```bash
cd clinical_orchestrator
python app.py
```

This will start the backend server at `http://localhost:8000`.
You can verify it's running by visiting `http://localhost:8000/api/health`.

## 2. Start the Frontend (Next.js)

Open a **separate** terminal window and navigate to the `frontend` directory:

```bash
cd frontend
npm run dev
```

This will start the frontend development server at `http://localhost:3000`.

## 3. Access the Application

Open your web browser and go to:
**[http://localhost:3000](http://localhost:3000)**

---

### Troubleshooting

-   **Port Conflicts**: If you see errors about ports being in use (8000 or 3000), make sure to stop any existing python or node processes using `taskkill /F /IM python.exe` and `taskkill /F /IM node.exe` (Windows) or `pkill -f python` / `pkill -f node` (Mac/Linux).
-   **API Connection**: If the frontend shows "Network Error", ensure the backend is running and accessible at `http://localhost:8000`.

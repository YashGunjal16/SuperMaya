# 🚀 SuperMaya: The Agentic AI Workspace

SuperMaya is a next-generation, multi-modal, and agentic AI platform designed to power intelligent digital experiences. This full-stack application features a sophisticated FastAPI backend and a dynamic React frontend, creating a seamless and interactive AI workspace.

The core innovation of SuperMaya lies in its **agentic architecture**, where a central "MetaAgent" intelligently classifies user intent and routes tasks to specialized sub-agents. This allows the system to handle diverse and complex queries, from real-time financial data analysis to generative data visualization and multi-modal image understanding.

**[▶️ Watch the Live Demo on Loom](https://www.loom.com/your-video-link-here)**

---

## ✨ Key Features

*   **Multi-Modal Interaction:** Communicate via text or upload images for analysis.
*   **Agentic Routing:** A smart MetaAgent delegates tasks to the best agent for the job (Financial, Vision, or General AI).
*   **Dynamic Data Visualization:** Ask for any kind of chart (`pie chart of...`, `bar graph of...`) and the AI will generate the data and visualization spec on-the-fly using a universal **Vega-Lite** engine.
*   **Real-Time Financial Analysis:** Get live stock market data for indices like Nifty 50 and Sensex, rendered as beautiful, responsive charts.
*   **Advanced Image Understanding:** Perform OCR on menus, describe scenes, and identify objects with the powerful Gemini 1.5 Flash vision model.
*   **Rich Content Generation:** Responses are enriched with relevant images and reference links, sourced in real-time.
*   **Secure & Personalized:** Full user authentication with JWT, with a foundation for user-specific AI personas and settings.
*   **Interactive UI:** A clean, modern React interface with clickable tags for follow-up queries and a built-in feedback system.

---

## 🛠️ Tech Stack & Architecture

This project is a monorepo containing a distinct backend and frontend.

### **Backend (`/backend`)**

| Component      | Technology                                                              | Purpose                                                                                                                                                                 |
| -------------- | ----------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Framework**  | **FastAPI**                                                             | High-performance, asynchronous API services.                                                                                                                            |
| **AI Brain**   | **`instructor` + Pydantic**                                             | Ensures all AI outputs are structured, validated JSON.                                                                                                                  |
| **Agents**     | **Groq (Llama3-70B)**, **Google (Gemini 1.5 Flash)**                      | A multi-provider, multi-model approach for text, vision, and data generation.                                                                                           |
| **Tools**      | **`yfinance`**                                                          | A robust library for fetching real-time financial data, replacing fragile web APIs.                                                                                     |
| **Database**   | **SQLAlchemy** (Async) with **SQLite**                                  | Manages user accounts, chat history, and feedback.                                                                                                                      |
| **Security**   | **JWT** (via `python-jose`) & **`passlib`**                               | Secure token-based authentication for all user-facing endpoints.                                                                                                        |

### **Frontend (`/frontend`)**

| Component      | Technology                                                              | Purpose                                                                                                                                                                 |
| -------------- | ----------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Framework**  | **React** with **Vite**                                                 | A fast, modern, and component-based user interface.                                                                                                                     |
| **Routing**    | **`react-router-dom`**                                                  | Manages navigation between the login/registration pages and the main chat workspace.                                                                                    |
| **API Client** | **`axios`**                                                             | A robust HTTP client with an interceptor for seamless JWT token management.                                                                                             |
| **Charting**   | **`react-vega`** with **Vega-Lite**                                       | A universal visualization engine. The UI can render **any** chart spec the AI generates, from line and pie charts to complex plots, without needing new frontend code. |
| **Styling**    | **CSS Modules / `index.css`**                                           | Clean, modern, and responsive design for a professional look and feel.                                                                                                  |

---

## 🚀 Getting Started

### **Prerequisites**

*   Python 3.8+
*   Node.js & npm
*   API keys for Groq, Google AI (Gemini), and Alpha Vantage (or any financial API).

### **Backend Setup**

1.  **Navigate to the backend directory:**
    ```bash
    cd backend
    ```
2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Configure environment variables:**
    *   Rename `.env.example` to `.env`.
    *   Fill in your API keys in the `.env` file.
5.  **Run the server:**
    ```bash
    uvicorn app.main:app --reload
    ```
    The backend will be running at `http://localhost:8000`.

### **Frontend Setup**

1.  **Navigate to the frontend directory:**
    ```bash
    cd frontend
    ```
2.  **Install dependencies:**
    ```bash
    npm install
    ```
3.  **Run the development server:**
    ```bash
    npm run dev
    ```
    The frontend will be running at `http://localhost:5173`.

---

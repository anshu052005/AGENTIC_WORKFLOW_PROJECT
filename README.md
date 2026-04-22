# 🤖 Lead Capture Chatbot (LangGraph-Based)

## 📌 Overview

This project implements a conversational AI chatbot that captures user leads through an interactive dialogue. The bot collects key user details such as **name, email, and preferred content platform (YouTube/Instagram)** while ensuring proper validation and structured flow.

The system is designed to simulate a real-world lead generation assistant that can later be deployed on messaging platforms like WhatsApp.

---

## 🚀 How to Run the Project Locally

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/lead-chatbot.git
cd lead-chatbot
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the root directory:

```
OPENAI_API_KEY=your_api_key_here
```

### 5. Run the Application

```bash
python app.py
```

The chatbot will start in your terminal and guide you through the lead capture flow.

---

## 🏗️ Architecture Explanation

This project uses **LangGraph** to design the conversational workflow because it provides a graph-based abstraction for building stateful, multi-step AI agents. Unlike traditional sequential chatbot logic, LangGraph allows defining conversation steps as nodes and transitions as edges, making the system more modular and easier to extend.

LangGraph was chosen over alternatives like AutoGen because this use case requires **deterministic flow control and structured state transitions**, rather than multi-agent collaboration. The problem is essentially a guided form-filling interaction, which aligns well with LangGraph’s state machine paradigm.

State is managed using a centralized state object that persists user inputs across steps. Each node updates specific fields such as `name`, `email`, or `platform`. Conditional transitions ensure robustness—for example, if an invalid email is detected, the flow loops back to the email input step instead of progressing. This guarantees data correctness and prevents incomplete submissions.

Overall, the architecture is **scalable, maintainable, and production-friendly**, making it suitable for real-world chatbot deployments.

---

## 📱 WhatsApp Deployment (Using Webhooks)

To deploy this chatbot on WhatsApp, we would integrate it using the **WhatsApp Business API** (via Meta Cloud API or Twilio) and a webhook-based backend.

### 1. Webhook Endpoint Setup

* Host the backend on a public server (AWS / Render / Railway).
* Expose an endpoint (e.g., `/webhook`) to receive incoming messages.

### 2. Incoming Message Handling

* WhatsApp sends user messages to the webhook via HTTP POST.
* Extract:

  * User phone number (acts as unique ID)
  * Message content

### 3. State Management

* Store user state in a database (Redis for fast access or PostgreSQL for persistence).
* Map each phone number to its conversation state.

### 4. Agent Processing

* Pass the user message and stored state into the LangGraph workflow.
* The agent determines:

  * Next question
  * Validation
  * Updated state

### 5. Sending Response

* Send the generated reply back using WhatsApp API.
* Continue this loop for every user message.

This architecture enables **real-time, multi-user, persistent conversations**, making it suitable for production-scale deployment.

---

## ✅ Features

* Structured conversational flow
* Robust state management
* Input validation (email, platform)
* Easy integration with messaging platforms
* Scalable architecture using LangGraph

---

## 📦 Future Improvements

* Database integration for persistent lead storage
* Admin dashboard for viewing leads
* Multi-platform deployment (WhatsApp, Telegram, Web)
* Lead scoring & qualification system
* Analytics and tracking

---

## 👨‍💻 Author

Anshu Rani

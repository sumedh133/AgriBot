# 🌾 AgriAssist AI

AgriAssist AI is a conversational AI assistant designed to help farmers access agricultural knowledge and real-time farming information through natural language interaction.

The system combines a **Large Language Model (LLM)** with external APIs such as weather services, market price datasets, and web search tools to provide context-aware farming advice.

The application is currently being developed as a **Streamlit-based chat interface** with a Python backend that orchestrates tools using **LangChain**.

This repository contains the **development version** of the system.

---

# Key Features

### Conversational Agricultural Assistant

Users can ask farming-related questions such as:

* Which crop grows well in sandy soil?
* How do I control aphids in cotton?
* Should I spray pesticide tomorrow?
* What is the tomato price today in Nashik?

The assistant uses a Large Language Model to understand queries and determine which external tools should be used to generate an answer.

---

### Tool-Augmented AI

Instead of relying only on pretrained knowledge, the system retrieves real-time information using tools such as:

* Web search
* Weather APIs
* Market price datasets

The AI decides when to use these tools and integrates the results into responses.

---

### Weather-Based Farming Advice

Weather forecasts can be used to generate practical recommendations such as:

Example:
Rain expected tomorrow. Avoid pesticide spraying as rain may wash away chemicals.

---

### Market Price Lookup

Users can check mandi prices for crops.

Example:
Tomato Prices Today
Nashik Mandi: ₹1800 per quintal
Pune Mandi: ₹2000 per quintal

---

### Multi-Language Support

The system is designed to support multiple languages:

* English
* Hindi
* Marathi

User queries can be translated to English for processing and translated back for responses.

---

### Voice Input

Users may optionally interact using voice through browser-based speech recognition.

---

### Persistent User Profiles

Users will be able to create accounts and maintain personalized farming profiles containing information such as:

* Location
* Crop type
* Soil type

This enables the system to generate **personalized agricultural advice**.

---

### Automatic Farmer Profile Extraction

The system can automatically learn information about the farmer from conversations.

Example:

User message
"I grow tomatoes and onions in Nashik."

Extracted information

Location: Nashik
Crops: Tomatoes, Onions

This information is stored and used to improve future recommendations.

---

# Technology Stack

Language
Python

Frontend
Streamlit

AI Orchestration
LangChain

Large Language Model
Google Gemini API

Database
MongoDB - cloud 

External APIs

Weather
OpenWeather API

Market Price Data
Agmarknet
Data.gov.in agricultural datasets

Search APIs
Tavily Search API
DuckDuckGo Search
SerpAPI

Voice Recognition
Web Speech API
Google Speech-to-Text (optional)

---

# Repository Structure

```
agriassist-ai/
│
├── app/
│
│   ├── main.py
│   │   Entry point of the Streamlit application.
│   │   Handles the chat interface and user interaction.
│
│   ├── config.py
│   │   Loads environment variables and global configuration.
│
│
│   ├── agent/
│   │
│   │   ├── agent.py
│   │   │   Creates and configures the LangChain LLM agent.
│   │
│   │   └── tools_registry.py
│   │       Registers all available tools used by the agent.
│
│
│   ├── auth/
│   │
│   │   ├── auth_service.py
│   │   │   Handles user login and registration logic.
│   │
│   │   ├── jwt_handler.py
│   │   │   Handles authentication tokens.
│   │
│   │   └── password_utils.py
│   │       Password hashing and verification utilities.
│
│
│   ├── database/
│   │
│   │   ├── mongodb.py
│   │   │   MongoDB connection setup.
│   │
│   │   ├── user_repository.py
│   │   │   Database operations related to users.
│   │
│   │   ├── chat_repository.py
│   │   │   Stores and retrieves chat conversations.
│   │
│   │   └── profile_repository.py
│   │       Stores farmer profile information.
│
│
│   ├── tools/
│   │
│   │   ├── weather_tool.py
│   │   │   LangChain tool for weather queries.
│   │
│   │   ├── market_price_tool.py
│   │   │   Tool for retrieving mandi prices.
│   │
│   │   └── search_tool.py
│   │       Tool for agricultural web search.
│
│
│   ├── services/
│   │
│   │   ├── weather_service.py
│   │   │   Handles OpenWeather API integration.
│   │
│   │   ├── market_service.py
│   │   │   Retrieves agricultural market prices.
│   │
│   │   └── search_service.py
│   │       Performs web search queries.
│
│
│   ├── memory/
│   │
│   │   └── conversation_memory.py
│   │       Manages conversation context for the LLM.
│
│
│   ├── translation/
│   │
│   │   └── translator.py
│   │       Handles language translation logic.
│
│
│
│   ├── models/
│   │
│   │   ├── user_model.py
│   │   ├── chat_model.py
│   │   └── profile_model.py
│   │
│   │   Data models used across the application.
│
│
├── docker/
│   Docker configuration files for containerization.
│
├── tests/
│   Unit tests for the system.
│
├── requirements.txt
│   Python dependencies for the project.
│
├── .env.example
│   Example environment variable configuration.
│
└── README.md
    Project documentation.
```

---

# Development Setup

The project uses **uv** for dependency and environment management instead of `venv` and `pip`.

---

## 1. Install uv

Install uv using pip:

```bash
pip install uv
```

Or using the official installer:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

---

## 2. Clone the Repository

```bash
git clone <repository-url>
cd AgriBot
```

---

## 3. Install Dependencies

Install all project dependencies listed in `pyproject.toml`:

```bash
uv sync
```

This will create the project environment and install all required packages.

---

## 4. Configure Environment Variables

Create a `.env` file in the project root.

Example configuration:

```
GOOGLE_API_KEY=your_gemini_api_key
OPENWEATHER_API_KEY=your_openweather_key
MONGODB_URI=your_mongodb_connection_string
JWT_SECRET=random_secret_key
```

---

## 5. Run the Application

Start the development server:

```bash
uv run python -m streamlit run app/main.py
```

The application will run at:

```
http://localhost:8501
```

---

# Managing Dependencies

This project uses **uv** for dependency management.  
Do **not** use `pip install` directly.

---

## Add a New Dependency

To install a new package:

```bash
uv add package-name
```

Example:

```bash
uv add pandas
```

This will automatically:

- install the package
- update `pyproject.toml`
- update `uv.lock`

---

## Add a Development Dependency

For development tools such as testing, linting, or formatting:

```bash
uv add --dev package-name
```

Example:

```bash
uv add --dev pytest ruff black
```

# Development Workflow

Each developer should work on a separate branch.

Example branches:

```
feature/weather-tool
feature/market-price-tool
feature/search-tool
feature/auth-system
feature/profile-extraction
```

Basic workflow:

```
git checkout -b feature/your-feature
git add .
git commit -m "Implemented feature"
git push origin feature/your-feature
```

Then open a Pull Request.

---

# Notes

PRD: https://docs.google.com/document/d/11DXDp9vAXH1Urvy0y095684OVI2Y3Cl-pgVKN2qtQoE/edit?usp=sharing

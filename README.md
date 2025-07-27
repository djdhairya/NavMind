
# 🧠 NavMind

**NavMind** is an **agentic AI-powered trip planner** that uses **CrewAI**, **Groq LLMs**, and **LangChain** to dynamically generate customized travel plans based on your preferences. Whether you're planning a leisure vacation, an adventurous escape, or a cultural tour, NavMind uses specialized agents to craft the perfect itinerary, city guide, and budget—all in real time.

---

## ✨ Features

- 🔍 **City Recommendation**: Based on travel type, interests, and season
- 🧠 **AI Agents**: Modular roles like city selector, itinerary planner, and budget manager
- 🌆 **Destination Research**: Attractions, culture, cuisine, tips, and hidden gems
- 🗓️ **Smart Itinerary Generator**: Day-by-day plans with meals, transport, and activities
- 💸 **Budget Breakdown**: Detailed cost estimates in INR, based on user-selected range
- 📄 **Download Trip Plan**: Save your personalized plan in text format

---

## 🧠 Agentic Design

NavMind uses a **multi-agent architecture** via **CrewAI**:

| Agent | Role |
|-------|------|
| 🏙 **City Selector Agent** | Recommends cities aligned with your preferences |
| 🧭 **Local Expert Agent** | Provides local travel insights for chosen city |
| 🧳 **Trip Planner Agent** | Builds a daily itinerary |
| 💰 **Budget Manager Agent** | Calculates an optimized trip budget |

Each agent has a distinct role, runs independently, and collaborates to produce a cohesive trip plan.

---

## 🏗️ Tech Stack

- **Frontend**: Streamlit
- **LLM Framework**: LangChain + Groq (LLaMA 3.3 70B)
- **Agents**: CrewAI
- **Environment Config**: dotenv

---

## 🚀 How to Run

### 1. Clone the Repository

```bash
git clone https://github.com/djdhairya/NavMind.git
cd NavMind
```

### 2. Set Up Environment

```bash
python -m venv venv
On Windows: venv\Scripts\activate

```

### 3. Add `.env` File

Create a `.env` file in the root directory:

```
GROQ_API_KEY=your_groq_api_key_here
```

### 4. Launch the App

```bash
streamlit run app.py
```

Visit [http://localhost:8501](http://localhost:8501) in your browser.

---
## 📁 Project Structure

```
├── app.py              
├── trip_agent.py       
├── .env                
└── README.md           
```
## 🔧 Configuration Notes

- Budget ranges are interpreted from INR to USD internally
- City can be selected automatically or entered manually
- Default exchange rate: `1 USD = ₹83` (can be modified in `app.py`)

---

## 🧠 Powered By

- [Streamlit](https://streamlit.io)
- [Groq](https://groq.com)
- [CrewAI](https://docs.crewai.com)
- [LangChain](https://www.langchain.com)
- Model: **LLaMA 3.3 70B Instruct** (via Groq)

---

## 🧾 Example Output

- **Recommended Cities**: Based on preferences like “Adventure in Summer”
- **Itinerary Plan**: 7-day schedule with activities and meals
- **Budget Table**: INR conversion of AI-estimated expenses
- **Download**: Export as `.txt` for offline use

---
<img width="1910" height="915" alt="Screenshot 2025-07-27 101219" src="https://github.com/user-attachments/assets/07fea1cc-7801-4a32-8f8b-d70d4aa24f36" />
<img width="1919" height="914" alt="Screenshot 2025-07-27 101243" src="https://github.com/user-attachments/assets/67c526a7-2092-4ddf-bdd3-8bb2097279bc" />
<img width="1353" height="184" alt="Screenshot 2025-07-27 101313" src="https://github.com/user-attachments/assets/7e1cb1e2-50ae-4906-9d68-e3cbce5c220c" />
<img width="1366" height="671" alt="Screenshot 2025-07-27 101325" src="https://github.com/user-attachments/assets/4dee0f03-894b-4bc1-b47a-7669860e51e8" />
<img width="1381" height="835" alt="Screenshot 2025-07-27 101409" src="https://github.com/user-attachments/assets/4b0b9f56-dea9-4ed8-b1dd-2f6b680ef6d0" />
<img width="1287" height="678" alt="Screenshot 2025-07-27 101439" src="https://github.com/user-attachments/assets/c5573d23-1eb1-49d5-a887-f98253168200" />










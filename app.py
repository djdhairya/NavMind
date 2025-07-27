import streamlit as st
import pandas as pd
import re
from trip_agent import TripCrew
from dotenv import load_dotenv
import os

load_dotenv()

USD_TO_INR = 83.0  # Example exchange rate

def get_budget_estimate_inr(range_str):
    mapping = {
        "$500-$1000": "around INR 43,000 – INR 87,000",
        "$1000-$2000": "around INR 87,000 – INR 1,74,000",
        "$2000-$3000": "around INR 1,74,000 – INR 2,61,000",
        "$3000+": "above INR 2,61,000",
        "Luxury": "above INR 4,30,000 with premium accommodations"
    }
    return mapping.get(range_str, "Estimate not available")

def convert_usd_to_inr(usd_str):
    try:
        return f"INR {int(float(usd_str) * USD_TO_INR):,}"
    except:
        return usd_str

def clean_budget_text(text):
    # Basic formatting cleanup for malformed AI responses
    text = text.replace(".Total", ".\nTotal")
    text = re.sub(r'(?<=[a-z])(?=[A-Z])', '\n', text)  # add newline before capital letters following lowercase
    text = re.sub(r'(\d)([a-zA-Z])', r'\1 \2', text)  # add space between number and letter
    text = re.sub(r'([a-zA-Z])(\d)', r'\1 \2', text)  # add space between letter and number
    return text

def main():
    st.set_page_config(page_title="NavMind", layout="wide")
    st.title("\U0001F9ED NavMind")

    with st.sidebar:
        st.header("\u2708\ufe0f Trip Preferences")
        travel_type = st.selectbox("Travel Type", ["Leisure", "Business", "Adventure", "Cultural"])
        interests = st.multiselect("Interests", ["Nature", "History", "Food", "Adventure", "Culture", "Art", "Shopping", "Relaxation", "Nightlife"])
        season = st.selectbox("Preferred Season", ["Spring", "Summer", "Autumn", "Winter"])
        duration = st.slider("Trip Duration (days)", 1, 30, 7)
        budget = st.selectbox("Budget Range (INR)", ["₹41,500 - ₹83,000", "₹83,000 - ₹1,66,000", "₹1,66,000 - ₹2,49,000", "₹2,49,000+", "Luxury"]
)

        custom_city = st.text_input("\U0001F4CD Custom City / State / Country (optional)")

    if st.button("\U0001F9E0 Generate My Trip Plan"):
        user_input = {
            "travel_type": travel_type,
            "interests": interests,
            "season": season,
            "trip_duration": duration,
            "budget": budget
        }

        with st.spinner("\U0001F30D Planning your dream trip with AI agents..."):
            try:
                crew_output = TripCrew(user_input, custom_city=custom_city).execute()

                st.subheader("\U0001F310 Your AI-Powered Trip Plan")

                city_selection = crew_output.get("city_selection_task", "No city selection found.")
                city_research = crew_output.get("city_research_task", "No city research found.")
                itinerary = crew_output.get("itinerary_creation_task", "No itinerary found.")
                raw_budget = crew_output.get("budget_management_task", "No budget found.")
                budget_text = clean_budget_text(raw_budget)

                with st.expander("\U0001F4CC Recommended Cities"):
                    st.markdown(city_selection)

                with st.expander("\U0001F4D6 Destination Insights"):
                    st.markdown(city_research)

                with st.expander("\U0001F5D3\ufe0f Itinerary Plan"):
                    st.markdown(itinerary)

                with st.expander("\U0001F4B0 Budget Breakdown"):
                    st.markdown(budget_text)

                    estimated_range = get_budget_estimate_inr(user_input["budget"])
                    st.info(f"\U0001F4A1 Estimated Total Trip Budget (in INR): {estimated_range}")

                    if "Accommodation" in budget_text and "Transportation" in budget_text:
                        try:
                            data = []
                            for line in budget_text.splitlines():
                                match = re.match(r"\*?\s*([\w\s]+):\s*\$?([0-9,]+)", line)
                                if match:
                                    item = match.group(1).strip()
                                    cost_usd = match.group(2).replace(",", "")
                                    cost_inr = convert_usd_to_inr(cost_usd)
                                    data.append({"Item": item, "Cost (INR)": cost_inr})

                            if data:
                                df = pd.DataFrame(data)
                                st.table(df)
                        except Exception as ex:
                            st.warning("Could not format budget as table.")

                txt_content = f"""Recommended Cities
{city_selection}

Destination Insights
{city_research}

Itinerary Plan
{itinerary}

Budget Breakdown
{budget_text}

Estimated Total Budget (INR): {estimated_range}
"""
                st.download_button("📄 Download Trip Plan as TXT", data=txt_content, file_name="trip_plan.txt", mime="text/plain")

                st.success("✅ Trip plan generated successfully!")

            except Exception as e:
                st.error(f"\u274C An error occurred while processing your trip: {e}")

if __name__ == "__main__":
    main()

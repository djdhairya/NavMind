from crewai import Agent, Crew, Task
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
import re

load_dotenv()

class TripAgent:
    def __init__(self):
        self.llm = ChatGroq(
            model="groq/llama-3.3-70b-versatile",
            temperature=0.1,
            api_key=os.getenv("GROQ_API_KEY"),
            additional_kwargs={"litellm_provider": "groq"}
        )

    def city_selector_agent(self):
        return Agent(
            role="City Selection Agent",
            goal="Identify the best cities for a trip based on user preferences.",
            backstory="An expert travel agent with global travel knowledge and client-first approach.",
            llm=self.llm,
            verbose=True
        )

    def local_expert_agent(self):
        return Agent(
            role="Local Destination Agent",
            goal="Provide detailed city insights: food, culture, travel tips, and hidden gems.",
            backstory="A cultural insider with deep city-specific knowledge and recommendations.",
            llm=self.llm,
            verbose=True
        )

    def trip_planner_agent(self):
        return Agent(
            role="Itinerary Planner Agent",
            goal="Build a detailed trip plan with travel, stay, meals, and activities.",
            backstory="A logistic planner that optimizes time, convenience, and excitement.",
            llm=self.llm,
            verbose=True
        )

    def budget_manager_agent(self):
        return Agent(
            role="Budget Planner Agent",
            goal="Ensure trip costs align with user budget and maximize experiences.",
            backstory="A cost-efficient travel manager who finds the best deals and value.",
            llm=self.llm,
            verbose=True
        )


class Triptask:
    def city_selection_task(self, agent, inputs):
        return Task(
            name="City Selection Task",
            description=(
                f"Analyze user preferences and select the best destinations for a trip:\n"
                f"- Travel Type: {inputs['travel_type']}\n"
                f"- Interests: {inputs['interests']}\n"
                f"- Season: {inputs['season']}\n"
                "Output: Provide a list of recommended cities with brief descriptions and reasons for selection."
            ),
            agent=agent,
            expected_output="Bullet points of recommended cities with brief descriptions and reasons for selection.",
        )

    def city_research_task(self, agent, city):
        return Task(
            name="City Research Task",
            description=(
                f"Provide detailed information about {city}, including:\n"
                "- Top attractions and landmarks\n"
                "- Dining options and local cuisine\n"
                "- Cultural experiences and events\n"
                "- Recommended accommodation areas\n"
                "- Travel tips and local customs\n"
                "- Hidden gems and off-the-beaten-path suggestions"
            ),
            agent=agent,
            expected_output="Organized sections with headings and bullet points for each category.",
        )

    def itinerary_creation_task(self, agent, inputs, city):
        return Task(
            name="Itinerary Creation Task",
            description=(
                f"Create a {inputs['trip_duration']} day itinerary for a trip to {city} based on the following:\n"
                "- Daily schedule with time allocations for activities\n"
                "- Transportation arrangements (e.g., flights, local transport)\n"
                "- Activity sequences and time optimization\n"
                "- Meal planning suggestions"
            ),
            agent=agent,
            expected_output="Day-to-day table format itinerary with time slots and activities.",
        )

    def budget_management_task(self, agent, inputs, itinerary):
        return Task(
            name="Budget Management Task",
            description=(
                f"The user selected a budget range of {inputs['budget']} for their trip. "
                "Estimate the total cost of the trip by breaking it down into:\n"
                "- Accommodation\n"
                "- Transportation\n"
                "- Meals\n"
                "- Activities\n"
                "- Miscellaneous (tips, shopping, etc.)\n\n"

                "Instructions:\n"
                "- First, convert the given budget range string into numerical bounds.\n"
                "  For example: '$500-$1000' means min = 500, max = 1000.\n"
                "- Create an approximate cost breakdown such that the total is within the max, "
                "or at most 10% over the upper bound (e.g., up to $1100 if the range is $500-$1000).\n"
                "- If the user selected 'Luxury', assume a total budget of ~$4000.\n"
                "- Return the breakdown in markdown table format.\n"
                "- At the end, summarize the total and whether it's within or slightly above the user's range."
            ),
            agent=agent,
            context=[itinerary],
            expected_output="A clean markdown table with estimated costs per category and total, followed by a brief summary.",
        )



class TripCrew:
    def __init__(self, inputs, custom_city=None):
        self.inputs = inputs
        self.custom_city = custom_city
        self.agents = TripAgent()
        self.tasks = Triptask()

    def execute(self):
        # Create agents
        city_selector = self.agents.city_selector_agent()
        local_expert = self.agents.local_expert_agent()
        trip_planner = self.agents.trip_planner_agent()
        budget_manager = self.agents.budget_manager_agent()

        # Step 1: Get city selection result
        if self.custom_city:
            selected_city = self.custom_city
            city_selection_output = f"User manually entered destination: **{selected_city}**"
        else:
            select_city_task = self.tasks.city_selection_task(city_selector, self.inputs)
            city_crew = Crew(
                agents=[city_selector],
                tasks=[select_city_task],
                verbose=True
            )
            city_result = city_crew.kickoff()
            if hasattr(city_result, "tasks_output"):
                city_selection_output = city_result.tasks_output[0].raw
            else:
                city_selection_output = str(city_result)

            # Extract first city from bullet points
            match = re.search(r"•\s*([A-Za-z\s]+)", city_selection_output)
            selected_city = match.group(1).strip() if match else "Paris"

        # Step 2–4: Run main trip planning
        city_research_task = self.tasks.city_research_task(local_expert, selected_city)
        itinerary_task = self.tasks.itinerary_creation_task(trip_planner, self.inputs, selected_city)
        budget_task = self.tasks.budget_management_task(budget_manager, self.inputs, itinerary_task)

        main_crew = Crew(
            agents=[local_expert, trip_planner, budget_manager],
            tasks=[city_research_task, itinerary_task, budget_task],
            verbose=True
        )
        main_result = main_crew.kickoff()

        return {
            "city_selection_task": city_selection_output,
            "city_research_task": main_result.tasks_output[0].raw,
            "itinerary_creation_task": main_result.tasks_output[1].raw,
            "budget_management_task": main_result.tasks_output[2].raw
        }

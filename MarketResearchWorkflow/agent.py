from google.adk import Workflow,Event,Agent,Context
from google.adk.workflow import node

# The first Event writes to the state (shared memory between agents) and the second Event sends a message to the user
# The second Event overrides the initial message provided by the user when they asked their question
# The third Event overrides the second Event and the initial message from the user
async def store_input(ctx):
    user_message = ctx.session.events[-1].message
    yield Event(state={"topic": "user_message"})
    yield Event(message=f"Received topic: tell me about New York")
    yield Event(message=f"Received topic: tell me about Paris")

async def fake_search():
    yield Event(message="Researching the topic...")
    for i in range(1,10000):
        if i % 1000 == 0:
            yield Event(message=f"Research progress: {i/10000*100:.2f}%")
    yield Event(message="Research completed.")

research_agent = Agent(
    name="ResearchAgent",
    model="gemini-2.5-flash-lite",
    instruction="You are a research expert. Analyze the following topic in depth, providing key findings, sources, and insights: {topic}",
    mode="single_turn",
)

market_agent = Agent(
    name="MarketAgent",
    model="gemini-2.5-flash-lite",
    instruction="You are a market analyst. Provide detailed market analysis for: {topic}. Include market size, trends, opportunities, and challenges.",
    mode="single_turn",
)

tech_agent = Agent(
    name="TechAgent",
    model="gemini-2.5-flash-lite",
    instruction="You are a technology expert. Analyze the technical aspects and implications of: {topic}. Include technologies, innovations, and technical challenges.",
    mode="single_turn",
)

report_agent = Agent(
    name="ReportAgent",
    model="gemini-2.5-flash-lite",
    instruction="You are a synthesis expert. Combine the insights from the research, market, and tech analyses to create a comprehensive report on: {topic}. Provide a clear summary, key insights, and actionable recommendations.",
    mode="single_turn",
)

from google.adk.workflow import JoinNode
join = JoinNode(name="JoinResults")

# There are multiple Event types: message, state, route, node_path:
# state: dict -> actions.state_delta
# route: value -> actions.route
# node_path: str -> node_info.path

async def synthesizer(node_input):
    results = node_input
    # node_input is a dict with keys "ResearchAgent", "MarketAgent", and "TechAgent"
    combined = "\n".join(f"[{k}]: {v}\n" for k, v in results.items())
    yield Event(message=f"Combined Analysis:\n{combined}")
    
workflow = Workflow(
    name="MarketResearchWorkflow",
    # edges=[
    #     ("START", store_input),
    #     (store_input, research_agent),
    #     (store_input, market_agent),
    #     (store_input, tech_agent),
        
    #     (research_agent, join),
    #     (market_agent, join),
    #     (tech_agent, join),

    #     (join, synthesizer),
    # ]
    edges=[
        ("START", fake_search,store_input, (research_agent, market_agent, tech_agent),join),
        (join, synthesizer,report_agent),
    ]
)


root_agent = workflow
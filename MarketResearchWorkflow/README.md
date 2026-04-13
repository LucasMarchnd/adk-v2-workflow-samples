# Market Research Workflow Architecture

This module showcases the graph-based approach in **ADK v2**. It performs a multi-dimensional analysis in parallel.

## System Architecture

The `MarketResearchWorkflow` executes as follows:

1. **Initialization (`START` -> `recherche` & `store_input`)**: Captures the user query, sets up the global shared state, and simulates background research loading.
2. **Parallel Execution**: The state triggers 3 specialized AI agents simultaneously (powered by `gemini-2.5-flash-lite`):
   - `ResearchAgent`: Deep-dive research and sourcing.
   - `MarketAgent`: Analyzes market size, trends, and opportunities.
   - `TechAgent`: Analyzes technologies, innovations, and tech hurdles.
3. **Synchronization (`JoinNode`)**: A join node waits until all three agents complete their tasks to unify the results.
4. **Final Synthesis (`synthesizer` & `ReportAgent`)**: Compiles the unified results and generates a final report for the user.

## Understanding Events and Overriding

An important mechanism demonstrated in `agent.py`'s `store_input` function is the usage of multiple `yield Event(...)` in sequence.

```python
async def store_input(ctx):
    user_message = ctx.session.events[-1].message
    yield Event(state={"topic": "user_message"})
    yield Event(message=f"Received topic: tell me about nintendo")
    yield Event(message=f"Received topic: tell me about apple")
```

By intentionally yielding two sequential `Event(message=...)` outputs, we overwrite the initial topic provided by the user. 
- The **first** `yield` replaces the actual user's question with "tell me about nintendo".
- The **second** `yield` immediately overrides the previous one with "tell me about apple".

This mechanism forces the entire graph pipeline to process the final overriding topic ("apple"). It stands as a clear example of how Events can be yielded to dynamically update the pipeline's state and steer the inputs directly into the downstream nodes.

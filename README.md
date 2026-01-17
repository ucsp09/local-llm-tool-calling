# local-llm-tool-calling-agent
Basic LLM Agent Which Calls Tools Dynamically And Answers Question

## Running
1. single tool calling
```
python main.py -p "What is weather in London?" -f "single_tool_calling"
```
2. parallel tool calling
```
python main.py -p "What is weather in London and temperature in Paris?" -f "parallel_tool_calling"
```
3. agent loop tool calling
```
python main.py -p "What is (11434+12341)*412?" -f "agent_loop_tool_calling"
```
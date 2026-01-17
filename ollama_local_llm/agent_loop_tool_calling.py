from config.constants import ModelProvider
from core.function_registry import register_function
from core.tool_registry import get_tool
from ollama import chat
from ollama import ChatResponse

@register_function(ModelProvider.OLLAMA.value, 'agent_loop_tool_calling')
def agent_loop_tool_calling(model: str, prompt: str):
    messages = [
        {
            "role": "system",
            "content": (
                "You are a maths expert who loves solving problems in a step by step manner.\n"
                "Given a math question, you first create a plan or todo-list in a step by step manner.\n"
                "Once the plan or todo-list is made, you execute the plan or todo-list and execute each step. \n"
                "For executing each step, you can use any of the available tools if required. \n"
                "After each step execution, you re-check the plan or todo-list and update it accordingly if required. \n"
                "Based on the latest plan or todo-list after each step, you again start executing the next steps.\n"
                "Since u are executing in a step by step manner, for every step execution you returns its intermediate result. \n"
                "Once all steps are executed, you recheck the final answer and if everyting looks good, you return the final answer. \n"
                "If u feel the final answer could not be correct and you need to re-create the plan then u can start from the plan again.\n"
                "Note: The last response that u return should have the final answer only in the format shown below and nothing else\n"
                "final-answer: <final answer>"
            )
        },
        {
            "role": "user",
            "content": prompt
        }
    ]

    print("\n----USER PROMPT----")
    print(prompt)

    add_tool = get_tool('add')
    multiply_tool = get_tool('multiply')

    iteration_count = 1
    while True:
        response: ChatResponse = chat(
            model=model,
            messages=messages,
            tools=[add_tool, multiply_tool],
            stream=False
        )
        assistant_msg = response.message
        messages.append(assistant_msg)

        print(f"\n--- MODEL RESPONSE (ITERATION {iteration_count}) ---")
        print("Content:", assistant_msg.content)
        print("Tool calls:", assistant_msg.tool_calls)

        if assistant_msg.tool_calls:
            for call in assistant_msg.tool_calls:
                tool_name = call.function.name
                tool_args = call.function.arguments
                print("\n--- TOOL DECISION TRACE ---")
                print("Tool selected:", tool_name)
                print("Arguments:", tool_args)

                if tool_name == 'add':
                    result = add_tool(**tool_args)
                elif tool_name == 'multiply':
                    result = multiply_tool(**tool_args)
                else:
                    result = 'unknown tool'
                
                print("\n--- TOOL RESULT ---")
                print(result)

                # Append tool result
                messages.append({
                    "role": "tool",
                    "tool_name": tool_name,
                    "content": str(result)
                })
        else:
            print(assistant_msg.content)
            
        if "final-answer" in assistant_msg.content:
            break
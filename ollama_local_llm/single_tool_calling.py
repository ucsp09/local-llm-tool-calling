from config.constants import ModelProvider
from core.function_registry import register_function
from core.tool_registry import get_tool
from ollama import chat

@register_function(ModelProvider.OLLAMA.value, 'single_tool_calling')
def single_tool_calling(model: str, prompt: str):
    messages = [
        {
            "role": "system",
            "content": (
                "You are an assistant that may use tools when needed.\n"
                "If you use a tool, briefly explain WHY in one sentence.\n"
                "Then provide the final answer.\n"
                "Do not expose chain-of-thought."
            )
        },
        {
            "role": "user",
            "content": prompt
        }
    ]
    get_weather_tool = get_tool('get_weather')

    print("\n--- USER PROMPT ---")
    print(prompt)

    # ----------------------------
    # First model call
    # ----------------------------
    response = chat(
        model=model,
        messages=messages,
        tools=[get_weather_tool],
        stream=False
    )

    assistant_msg = response.message
    messages.append(assistant_msg)

    print("\n--- MODEL RESPONSE (STEP 1) ---")
    print("Content:", assistant_msg.content)
    print("Tool calls:", assistant_msg.tool_calls)

    # ----------------------------
    # Tool execution (if requested)
    # ----------------------------
    if assistant_msg.tool_calls:
        call = assistant_msg.tool_calls[0]

        tool_name = call.function.name
        tool_args = call.function.arguments

        print("\n--- TOOL DECISION TRACE ---")
        print("Tool selected:", tool_name)
        print("Arguments:", tool_args)

        # Execute tool
        result = get_weather_tool(**tool_args)

        print("\n--- TOOL RESULT ---")
        print(result)

        # Append tool result
        messages.append({
            "role": "tool",
            "tool_name": tool_name,
            "content": str(result)
        })

        # ----------------------------
        # Final model response
        # ----------------------------
        final_response = chat(
            model=model,
            messages=messages,
            tools=[get_weather_tool],
            stream=False
        )

        print("\n--- FINAL RESPONSE ---")
        print(final_response.message.content)

    else:
        print("\n--- NO TOOL USED ---")
        print(assistant_msg.content)

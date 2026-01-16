import argparse
from config.constants import DEFAULT_MODEL_PROVIDER, DEFAULT_MODEL
from core import function_registry
from core import tool_registry
from core import tools
from ollama_local_llm import single_tool_calling, parallel_tool_calling, agent_loop_tool_calling
import sys


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--prompt', type=str, required=True, help='The prompt to pass to the llm')
    parser.add_argument('-mp', '--model-provider', type=str, default=DEFAULT_MODEL_PROVIDER, help='The name of model provider to use')
    parser.add_argument('-m', '--model', type=str, default=DEFAULT_MODEL, help='The name of model to use')
    parser.add_argument('-f', '--function-name', type=str, required=True, help='The name of function to execute')

    args = parser.parse_args()
    prompt = args.prompt
    model_provider = args.model_provider
    model = args.model
    function_name = args.function_name

    func = function_registry.get_function(model_provider=model_provider, func_name=function_name)
    if func is None:
        print(f"Could not find a registered function with name:{function_name}")
        sys.exit(1)
    else:
        func(model, prompt)

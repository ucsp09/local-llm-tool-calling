from config.constants import ModelProvider
from core.function_registry import register_function

@register_function(ModelProvider.OLLAMA.value, 'agent_loop_tool_calling')
def agent_loop_tool_calling(model: str, prompt: str):
    pass

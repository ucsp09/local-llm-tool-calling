from typing import Dict, Callable

TOOLS: Dict[str, Callable] = {}

def register_tool():
    global TOOLS

    def decorator(func: Callable):
        TOOLS[func.__name__] = func
        return func
    return decorator

def get_tool(name: str):
    global TOOLS

    return TOOLS.get(name)

def get_all_tools():
    global TOOLS
    
    return TOOLS

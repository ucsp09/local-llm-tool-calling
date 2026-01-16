from typing import Callable, Dict

FUNCTIONS: Dict[str, Callable] = {}

def register_function(model_provider: str, func_name: str):
    global FUNCTIONS

    def decorator(func: Callable) -> Callable:
        key = f"{model_provider}:{func_name}"
        FUNCTIONS[key] = func
        return func  # IMPORTANT: return the original function
    return decorator


def get_function(model_provider: str, func_name: str) -> Callable | None:
    global FUNCTIONS
    
    key = f"{model_provider}:{func_name}"
    return FUNCTIONS.get(key)

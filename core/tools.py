from core.tool_registry import register_tool

@register_tool()
def get_weather(city: str):
    """
    Get the weather for a city
    Args:
        city: the name of the city
    Returns: the weather for the city
    """
    weathers = {
        'Paris': 'Sunny',
        'Delhi': 'Cloudy',
        'London': 'Rainy'
    }
    return weathers.get(city)

@register_tool()
def get_temperature(city: str):
    """
    Get the temperature for a city
    Args:
        city: the name of the city
    Returns: the temperature for the city
    """
    temperatures = {
        'Paris': '30C',
        'Delhi': '25C',
        'London': '20C'
    }
    return temperatures.get(city)

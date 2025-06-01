"""
Function Registry Module

This module contains all available functions and their registry mapping.
This can be imported and used by any function calling system.
"""

import json
from typing import Dict, Any, Callable

# ============================================================================
# AVAILABLE FUNCTIONS - Add your functions here
# ============================================================================

def get_weather(location: str, unit: str = "celsius") -> Dict[str, Any]:
    """Get weather information for a location"""
    # Simulate weather API call
    weather_data = {
        "new york": {"temp": 22, "condition": "sunny"},
        "london": {"temp": 15, "condition": "rainy"},
        "tokyo": {"temp": 28, "condition": "cloudy"},
        "paris": {"temp": 18, "condition": "partly cloudy"}
    }
    
    location_lower = location.lower()
    if location_lower in weather_data:
        data = weather_data[location_lower]
        return {
            "location": location,
            "temperature": data["temp"],
            "unit": unit,
            "condition": data["condition"],
            "status": "success"
        }
    else:
        return {
            "location": location,
            "error": "Weather data not available for this location",
            "status": "error"
        }

def calculate_tip(bill_amount: float, tip_percentage: float = 15.0) -> Dict[str, Any]:
    """Calculate tip amount and total bill"""
    tip_amount = bill_amount * (tip_percentage / 100)
    total = bill_amount + tip_amount
    
    return {
        "bill_amount": bill_amount,
        "tip_percentage": tip_percentage,
        "tip_amount": round(tip_amount, 2),
        "total_amount": round(total, 2),
        "status": "success"
    }

def convert_currency(amount: float, from_currency: str, to_currency: str) -> Dict[str, Any]:
    """Convert currency (simplified with fake rates)"""
    # Fake exchange rates for demo
    rates = {
        "USD": {"EUR": 0.85, "GBP": 0.73, "JPY": 110},
        "EUR": {"USD": 1.18, "GBP": 0.86, "JPY": 129},
        "GBP": {"USD": 1.37, "EUR": 1.16, "JPY": 150}
    }
    
    if from_currency == to_currency:
        converted_amount = amount
    elif from_currency in rates and to_currency in rates[from_currency]:
        rate = rates[from_currency][to_currency]
        converted_amount = round(amount * rate, 2)
    else:
        return {
            "error": f"Conversion from {from_currency} to {to_currency} not supported",
            "status": "error"
        }
    
    return {
        "original_amount": amount,
        "from_currency": from_currency,
        "to_currency": to_currency,
        "converted_amount": converted_amount,
        "status": "success"
    }

def send_notification(message: str, recipient: str, channel: str = "email") -> Dict[str, Any]:
    """Send a notification (simulated)"""
    return {
        "message": message,
        "recipient": recipient,
        "channel": channel,
        "sent_at": "2024-01-15 10:30:00",
        "status": "sent"
    }

def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> Dict[str, Any]:
    """Calculate distance between two coordinates (simplified)"""
    # Simplified distance calculation (not accurate, just for demo)
    import math
    
    # Convert to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    
    # Simplified calculation
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    
    # Rough distance in km
    distance = math.sqrt(dlat**2 + dlon**2) * 111  # Rough conversion
    
    return {
        "point1": {"lat": lat1, "lon": lon1},
        "point2": {"lat": lat2, "lon": lon2},
        "distance_km": round(distance, 2),
        "status": "success"
    }

# ============================================================================
# FUNCTION REGISTRY - Maps string names to function objects
# ============================================================================

AVAILABLE_FUNCTIONS: Dict[str, Callable] = {
    "get_weather": get_weather,
    "calculate_tip": calculate_tip,
    "convert_currency": convert_currency,
    "send_notification": send_notification,
    "calculate_distance": calculate_distance
}

# ============================================================================
# FUNCTION SCHEMAS - Tells LLM how to call each function
# ============================================================================

FUNCTION_SCHEMAS = [
    {
        "name": "get_weather",
        "description": "Get current weather information for a specific location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city name, e.g. 'New York', 'London'"
                },
                "unit": {
                    "type": "string",
                    "enum": ["celsius", "fahrenheit"],
                    "description": "Temperature unit (default: celsius)"
                }
            },
            "required": ["location"]
        }
    },
    {
        "name": "calculate_tip",
        "description": "Calculate tip amount and total bill",
        "parameters": {
            "type": "object",
            "properties": {
                "bill_amount": {
                    "type": "number",
                    "description": "The bill amount in dollars"
                },
                "tip_percentage": {
                    "type": "number",
                    "description": "Tip percentage (default: 15%)"
                }
            },
            "required": ["bill_amount"]
        }
    },
    {
        "name": "convert_currency",
        "description": "Convert amount from one currency to another",
        "parameters": {
            "type": "object",
            "properties": {
                "amount": {
                    "type": "number",
                    "description": "Amount to convert"
                },
                "from_currency": {
                    "type": "string",
                    "description": "Source currency code (USD, EUR, GBP)"
                },
                "to_currency": {
                    "type": "string",
                    "description": "Target currency code (USD, EUR, GBP)"
                }
            },
            "required": ["amount", "from_currency", "to_currency"]
        }
    },
    {
        "name": "send_notification",
        "description": "Send a notification to a recipient",
        "parameters": {
            "type": "object",
            "properties": {
                "message": {
                    "type": "string",
                    "description": "The notification message"
                },
                "recipient": {
                    "type": "string",
                    "description": "Recipient identifier (email, phone, etc.)"
                },
                "channel": {
                    "type": "string",
                    "enum": ["email", "sms", "push"],
                    "description": "Notification channel (default: email)"
                }
            },
            "required": ["message", "recipient"]
        }
    },
    {
        "name": "calculate_distance",
        "description": "Calculate distance between two geographic coordinates",
        "parameters": {
            "type": "object",
            "properties": {
                "lat1": {"type": "number", "description": "Latitude of first point"},
                "lon1": {"type": "number", "description": "Longitude of first point"},
                "lat2": {"type": "number", "description": "Latitude of second point"},
                "lon2": {"type": "number", "description": "Longitude of second point"}
            },
            "required": ["lat1", "lon1", "lat2", "lon2"]
        }
    }
]

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def get_available_function_names() -> list:
    """Get list of all available function names"""
    return list(AVAILABLE_FUNCTIONS.keys())

def get_function_by_name(function_name: str) -> Callable:
    """Get function object by name"""
    return AVAILABLE_FUNCTIONS.get(function_name)

def is_function_available(function_name: str) -> bool:
    """Check if a function is available"""
    return function_name in AVAILABLE_FUNCTIONS

def get_function_schema(function_name: str) -> Dict[str, Any]:
    """Get schema for a specific function"""
    for schema in FUNCTION_SCHEMAS:
        if schema["name"] == function_name:
            return schema
    return None

# ============================================================================
# REGISTRY INFO
# ============================================================================

def print_registry_info():
    """Print information about the function registry"""
    print("🔧 FUNCTION REGISTRY INFO")
    print("=" * 50)
    print(f"Total functions available: {len(AVAILABLE_FUNCTIONS)}")
    print("\nAvailable functions:")
    for name, func in AVAILABLE_FUNCTIONS.items():
        print(f"  • {name}: {func.__doc__ or 'No description'}")
    print("\n" + "=" * 50)

if __name__ == "__main__":
    print_registry_info() 
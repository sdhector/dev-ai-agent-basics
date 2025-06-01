"""
Minimal Example: OpenAI Function Calling with Host Execution

This example demonstrates:
1. How to define functions that the LLM can call
2. How the LLM returns function call requests (JSON format)
3. How the HOST executes these functions
4. How to send results back to the LLM for final response

The key insight: The LLM doesn't execute functions directly. It returns
a JSON specification of what function to call, and YOUR CODE executes it.
"""

import json
import os
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")  # Set your API key as environment variable
)

# ============================================================================
# STEP 1: Define the actual functions that can be executed
# ============================================================================

def get_weather(location: str, unit: str = "celsius") -> dict:
    """
    Simulated weather function - in real app, this would call a weather API
    """
    # This is where YOU implement the actual logic
    weather_data = {
        "new york": {"temp": 22, "condition": "sunny"},
        "london": {"temp": 15, "condition": "rainy"},
        "tokyo": {"temp": 28, "condition": "cloudy"}
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

def calculate_tip(bill_amount: float, tip_percentage: float = 15.0) -> dict:
    """
    Calculate tip amount and total bill
    """
    tip_amount = bill_amount * (tip_percentage / 100)
    total = bill_amount + tip_amount
    
    return {
        "bill_amount": bill_amount,
        "tip_percentage": tip_percentage,
        "tip_amount": round(tip_amount, 2),
        "total_amount": round(total, 2),
        "status": "success"
    }

# ============================================================================
# STEP 2: Create a registry of available functions
# ============================================================================

# This is how YOUR CODE knows which functions can be executed
AVAILABLE_FUNCTIONS = {
    "get_weather": get_weather,
    "calculate_tip": calculate_tip
}

# ============================================================================
# STEP 3: Define function schemas for the LLM
# ============================================================================

# This tells the LLM what functions are available and how to call them
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
                    "description": "Temperature unit"
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
    }
]

# ============================================================================
# STEP 4: Function to execute LLM-requested function calls
# ============================================================================

def execute_function_call(function_name: str, arguments: dict) -> dict:
    """
    This is the KEY PART: How the host executes functions requested by the LLM
    
    Args:
        function_name: Name of function to execute (from LLM response)
        arguments: Arguments to pass to function (from LLM response)
    
    Returns:
        Result of function execution
    """
    print(f"🔧 HOST EXECUTING: {function_name}({arguments})")
    
    # Look up the actual function in our registry
    if function_name not in AVAILABLE_FUNCTIONS:
        return {
            "error": f"Function '{function_name}' not found",
            "status": "error"
        }
    
    try:
        # Get the actual Python function
        function_to_call = AVAILABLE_FUNCTIONS[function_name]
        
        # Execute it with the LLM-provided arguments
        result = function_to_call(**arguments)
        
        print(f"✅ FUNCTION RESULT: {result}")
        return result
        
    except Exception as e:
        return {
            "error": f"Error executing {function_name}: {str(e)}",
            "status": "error"
        }

# ============================================================================
# STEP 5: Main conversation handler
# ============================================================================

def chat_with_function_calling(user_message: str) -> str:
    """
    Complete example of function calling workflow
    """
    print(f"👤 USER: {user_message}")
    print("=" * 60)
    
    # Initial conversation with function definitions
    messages = [
        {
            "role": "system", 
            "content": "You are a helpful assistant. Use the provided functions when needed to answer user questions."
        },
        {
            "role": "user", 
            "content": user_message
        }
    ]
    
    # STEP 5.1: Send request to LLM with available functions
    print("📤 SENDING REQUEST TO LLM...")
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        functions=FUNCTION_SCHEMAS,  # Tell LLM what functions are available
        function_call="auto"  # Let LLM decide when to call functions
    )
    
    assistant_message = response.choices[0].message
    print(f"🤖 LLM RESPONSE TYPE: {assistant_message.role}")
    
    # STEP 5.2: Check if LLM wants to call a function
    if assistant_message.function_call:
        print("🎯 LLM WANTS TO CALL A FUNCTION!")
        
        # Extract function call details from LLM response
        function_name = assistant_message.function_call.name
        function_args = json.loads(assistant_message.function_call.arguments)
        
        print(f"📋 FUNCTION NAME: {function_name}")
        print(f"📋 FUNCTION ARGS: {function_args}")
        
        # STEP 5.3: HOST EXECUTES THE FUNCTION (This is what you were asking about!)
        function_result = execute_function_call(function_name, function_args)
        
        # STEP 5.4: Add function call and result to conversation
        messages.append(assistant_message)  # Add LLM's function call request
        messages.append({
            "role": "function",
            "name": function_name,
            "content": json.dumps(function_result)  # Add function result
        })
        
        # STEP 5.5: Send updated conversation back to LLM for final response
        print("📤 SENDING FUNCTION RESULT BACK TO LLM...")
        final_response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        
        final_answer = final_response.choices[0].message.content
        print(f"🤖 FINAL LLM RESPONSE: {final_answer}")
        return final_answer
        
    else:
        # No function call needed, return direct response
        direct_answer = assistant_message.content
        print(f"🤖 DIRECT LLM RESPONSE: {direct_answer}")
        return direct_answer

# ============================================================================
# STEP 6: Example usage
# ============================================================================

def main():
    """
    Run examples to demonstrate function calling
    """
    print("🚀 FUNCTION CALLING EXAMPLE")
    print("=" * 60)
    
    # Example 1: Weather query (should trigger function call)
    print("\n" + "="*60)
    print("EXAMPLE 1: Weather Query")
    print("="*60)
    chat_with_function_calling("What's the weather like in New York?")
    
    # Example 2: Tip calculation (should trigger function call)
    print("\n" + "="*60)
    print("EXAMPLE 2: Tip Calculation")
    print("="*60)
    chat_with_function_calling("I have a bill of $85.50, what's a 20% tip?")
    
    # Example 3: General question (should NOT trigger function call)
    print("\n" + "="*60)
    print("EXAMPLE 3: General Question")
    print("="*60)
    chat_with_function_calling("What is the capital of France?")

if __name__ == "__main__":
    # Check if API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Please set OPENAI_API_KEY environment variable")
        print("   Example: export OPENAI_API_KEY='your-api-key-here'")
    else:
        main() 
"""
SUPER SIMPLE Function Calling Demo

This shows EXACTLY what the LLM returns when it wants to call a function.
No fancy formatting - just the raw JSON so you can see what's happening.
"""

import json
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Simple function that could be called
def add_numbers(a: float, b: float) -> float:
    """Add two numbers together"""
    return a + b

# Function schema for the LLM
function_schema = {
    "name": "add_numbers",
    "description": "Add two numbers together",
    "parameters": {
        "type": "object",
        "properties": {
            "a": {"type": "number", "description": "First number"},
            "b": {"type": "number", "description": "Second number"}
        },
        "required": ["a", "b"]
    }
}

def demo_raw_function_call():
    """Show the raw JSON that LLM returns when it wants to call a function"""
    
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    # Send a request that should trigger function calling
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": "What is 15 + 27?"}
        ],
        functions=[function_schema],
        function_call="auto"
    )
    
    message = response.choices[0].message
    
    print("=" * 60)
    print("WHAT THE LLM RETURNS:")
    print("=" * 60)
    print(f"Role: {message.role}")
    print(f"Content: {message.content}")
    print(f"Function Call: {message.function_call}")
    
    if message.function_call:
        print("\n" + "=" * 60)
        print("FUNCTION CALL DETAILS:")
        print("=" * 60)
        print(f"Function Name: {message.function_call.name}")
        print(f"Arguments (raw): {message.function_call.arguments}")
        
        # Parse the arguments
        args = json.loads(message.function_call.arguments)
        print(f"Arguments (parsed): {args}")
        
        print("\n" + "=" * 60)
        print("NOW YOUR CODE EXECUTES THE FUNCTION:")
        print("=" * 60)
        
        # This is what YOUR code does:
        if message.function_call.name == "add_numbers":
            result = add_numbers(args["a"], args["b"])
            print(f"add_numbers({args['a']}, {args['b']}) = {result}")
        
        print("\n" + "=" * 60)
        print("SEND RESULT BACK TO LLM FOR FINAL ANSWER:")
        print("=" * 60)
        
        # Continue conversation with function result
        messages = [
            {"role": "user", "content": "What is 15 + 27?"},
            message,  # The LLM's function call
            {
                "role": "function",
                "name": "add_numbers",
                "content": str(result)
            }
        ]
        
        final_response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        
        print(f"Final Answer: {final_response.choices[0].message.content}")

if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Please set OPENAI_API_KEY in your .env file")
        print("   Create a .env file with: OPENAI_API_KEY=your-api-key-here")
    else:
        demo_raw_function_call() 
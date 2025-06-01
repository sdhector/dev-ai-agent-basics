"""
Complete Demonstration: How to Use function_registry.py and function_executor.py

This script demonstrates all the ways you can use the modular function calling system.
Perfect for understanding how the components work together!
"""

import os
from dotenv import load_dotenv

# Import our modular components
from function_registry import (
    AVAILABLE_FUNCTIONS, 
    FUNCTION_SCHEMAS,
    get_available_function_names,
    get_function_by_name,
    is_function_available,
    get_function_schema,
    print_registry_info
)

from function_executor import (
    FunctionExecutor,
    LLMFunctionCaller,
    create_function_caller_from_registry,
    test_function_execution
)

def demo_1_basic_registry_usage():
    """Demonstrate basic function registry usage"""
    print("🔧 DEMO 1: BASIC FUNCTION REGISTRY USAGE")
    print("=" * 60)
    
    # Show what's available in the registry
    print("Available functions:")
    for name in get_available_function_names():
        print(f"  • {name}")
    
    # Get a specific function
    weather_func = get_function_by_name("get_weather")
    print(f"\nGot function: {weather_func}")
    print(f"Function docstring: {weather_func.__doc__}")
    
    # Check if functions exist
    print(f"\nIs 'get_weather' available? {is_function_available('get_weather')}")
    print(f"Is 'nonexistent_func' available? {is_function_available('nonexistent_func')}")
    
    # Get function schema
    weather_schema = get_function_schema("get_weather")
    print(f"\nWeather function schema: {weather_schema}")
    
    # Print full registry info
    print("\n")
    print_registry_info()

def demo_2_direct_function_execution():
    """Demonstrate direct function execution without LLM"""
    print("\n🔧 DEMO 2: DIRECT FUNCTION EXECUTION")
    print("=" * 60)
    
    # Method 1: Call functions directly
    print("Method 1: Direct function calls")
    weather_func = get_function_by_name("get_weather")
    result = weather_func("Tokyo", "celsius")
    print(f"Direct call result: {result}")
    
    # Method 2: Use the test_function_execution helper
    print("\nMethod 2: Using test_function_execution helper")
    result = test_function_execution(
        AVAILABLE_FUNCTIONS,
        "calculate_tip", 
        {"bill_amount": 85.50, "tip_percentage": 20}
    )
    print(f"Test execution result: {result}")
    
    # Method 3: Use FunctionExecutor directly
    print("\nMethod 3: Using FunctionExecutor class")
    executor = FunctionExecutor(AVAILABLE_FUNCTIONS, FUNCTION_SCHEMAS)
    result = executor.execute_function_call(
        "convert_currency",
        {"amount": 1000, "from_currency": "USD", "to_currency": "EUR"}
    )
    print(f"Executor result: {result}")

def demo_3_llm_function_calling():
    """Demonstrate full LLM function calling workflow"""
    print("\n🤖 DEMO 3: LLM FUNCTION CALLING")
    print("=" * 60)
    
    # Check if API key is available
    load_dotenv()
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  OPENAI_API_KEY not found in environment variables.")
        print("   This demo requires an OpenAI API key to work.")
        print("   Please add OPENAI_API_KEY to your .env file.")
        return
    
    # Method 1: Create function caller manually
    print("Method 1: Manual creation")
    executor = FunctionExecutor(AVAILABLE_FUNCTIONS, FUNCTION_SCHEMAS)
    llm_caller = LLMFunctionCaller(executor)
    
    # Test with a simple query
    print("\n--- Testing weather query ---")
    response = llm_caller.chat_with_functions("What's the weather in London?")
    
    # Method 2: Use convenience function
    print("\nMethod 2: Using convenience function")
    quick_caller = create_function_caller_from_registry(
        AVAILABLE_FUNCTIONS, 
        FUNCTION_SCHEMAS
    )
    
    print("\n--- Testing tip calculation ---")
    response = quick_caller.chat_with_functions(
        "I have a restaurant bill of $67.80. What would be a 15% tip and the total?"
    )

def demo_4_error_handling():
    """Demonstrate error handling in the system"""
    print("\n❌ DEMO 4: ERROR HANDLING")
    print("=" * 60)
    
    executor = FunctionExecutor(AVAILABLE_FUNCTIONS, FUNCTION_SCHEMAS)
    
    # Test 1: Non-existent function
    print("Test 1: Calling non-existent function")
    result = executor.execute_function_call("nonexistent_function", {})
    print(f"Result: {result}")
    
    # Test 2: Invalid arguments
    print("\nTest 2: Invalid arguments")
    result = executor.execute_function_call("calculate_tip", {"invalid_arg": 123})
    print(f"Result: {result}")
    
    # Test 3: Missing required arguments
    print("\nTest 3: Missing required arguments")
    result = executor.execute_function_call("get_weather", {})
    print(f"Result: {result}")

def demo_5_extending_the_system():
    """Demonstrate how to extend the system with new functions"""
    print("\n🔧 DEMO 5: EXTENDING THE SYSTEM")
    print("=" * 60)
    
    # Define new custom functions
    def calculate_area_circle(radius: float) -> dict:
        """Calculate area of a circle"""
        import math
        area = math.pi * radius ** 2
        return {
            "radius": radius,
            "area": round(area, 2),
            "formula": "π × r²",
            "status": "success"
        }
    
    def generate_password(length: int = 12, include_symbols: bool = True) -> dict:
        """Generate a random password"""
        import random
        import string
        
        chars = string.ascii_letters + string.digits
        if include_symbols:
            chars += "!@#$%^&*"
        
        password = ''.join(random.choice(chars) for _ in range(length))
        return {
            "password": password,
            "length": length,
            "includes_symbols": include_symbols,
            "status": "success"
        }
    
    # Create extended registry
    extended_functions = AVAILABLE_FUNCTIONS.copy()
    extended_functions.update({
        "calculate_area_circle": calculate_area_circle,
        "generate_password": generate_password
    })
    
    # Create schemas for new functions
    new_schemas = [
        {
            "name": "calculate_area_circle",
            "description": "Calculate the area of a circle given its radius",
            "parameters": {
                "type": "object",
                "properties": {
                    "radius": {
                        "type": "number",
                        "description": "Radius of the circle"
                    }
                },
                "required": ["radius"]
            }
        },
        {
            "name": "generate_password",
            "description": "Generate a random password",
            "parameters": {
                "type": "object",
                "properties": {
                    "length": {
                        "type": "integer",
                        "description": "Length of password (default: 12)"
                    },
                    "include_symbols": {
                        "type": "boolean",
                        "description": "Include symbols in password (default: true)"
                    }
                },
                "required": []
            }
        }
    ]
    
    extended_schemas = FUNCTION_SCHEMAS + new_schemas
    
    # Test the extended system
    print(f"Original functions: {len(AVAILABLE_FUNCTIONS)}")
    print(f"Extended functions: {len(extended_functions)}")
    print(f"New functions added: {list(set(extended_functions.keys()) - set(AVAILABLE_FUNCTIONS.keys()))}")
    
    # Test new functions directly
    print("\nTesting new functions:")
    result = test_function_execution(extended_functions, "calculate_area_circle", {"radius": 5})
    print(f"Circle area: {result}")
    
    result = test_function_execution(extended_functions, "generate_password", {"length": 16, "include_symbols": False})
    print(f"Password generation: {result}")
    
    # Create caller with extended system
    extended_caller = create_function_caller_from_registry(extended_functions, extended_schemas)
    print(f"\n✅ Extended system ready with {len(extended_functions)} functions!")

def demo_6_multiple_specialized_systems():
    """Demonstrate creating multiple specialized function calling systems"""
    print("\n🎯 DEMO 6: MULTIPLE SPECIALIZED SYSTEMS")
    print("=" * 60)
    
    # System 1: Math operations
    def add(a: float, b: float) -> dict:
        return {"result": a + b, "operation": "addition"}
    
    def subtract(a: float, b: float) -> dict:
        return {"result": a - b, "operation": "subtraction"}
    
    math_functions = {"add": add, "subtract": subtract}
    math_schemas = [
        {
            "name": "add",
            "description": "Add two numbers",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "First number"},
                    "b": {"type": "number", "description": "Second number"}
                },
                "required": ["a", "b"]
            }
        },
        {
            "name": "subtract",
            "description": "Subtract two numbers",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "First number"},
                    "b": {"type": "number", "description": "Second number"}
                },
                "required": ["a", "b"]
            }
        }
    ]
    
    # System 2: Text operations
    def count_words(text: str) -> dict:
        return {"word_count": len(text.split()), "text": text}
    
    def reverse_text(text: str) -> dict:
        return {"original": text, "reversed": text[::-1]}
    
    text_functions = {"count_words": count_words, "reverse_text": reverse_text}
    text_schemas = [
        {
            "name": "count_words",
            "description": "Count words in text",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "Text to count words in"}
                },
                "required": ["text"]
            }
        },
        {
            "name": "reverse_text",
            "description": "Reverse text",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "Text to reverse"}
                },
                "required": ["text"]
            }
        }
    ]
    
    # Create specialized systems
    math_system = create_function_caller_from_registry(math_functions, math_schemas)
    text_system = create_function_caller_from_registry(text_functions, text_schemas)
    general_system = create_function_caller_from_registry(AVAILABLE_FUNCTIONS, FUNCTION_SCHEMAS)
    
    print("✅ Created 3 specialized systems:")
    print(f"  • Math system: {list(math_functions.keys())}")
    print(f"  • Text system: {list(text_functions.keys())}")
    print(f"  • General system: {list(AVAILABLE_FUNCTIONS.keys())}")
    
    # Test each system
    print("\nTesting math system:")
    test_function_execution(math_functions, "add", {"a": 15, "b": 27})
    
    print("\nTesting text system:")
    test_function_execution(text_functions, "count_words", {"text": "Hello world from AI"})

def main():
    """Run all demonstrations"""
    print("🚀 COMPLETE FUNCTION SYSTEM DEMONSTRATION")
    print("=" * 80)
    print("This script shows you everything you can do with the modular function system!")
    print("=" * 80)
    
    # Run all demos
    demo_1_basic_registry_usage()
    demo_2_direct_function_execution()
    demo_3_llm_function_calling()
    demo_4_error_handling()
    demo_5_extending_the_system()
    demo_6_multiple_specialized_systems()
    
    print("\n" + "=" * 80)
    print("🎉 DEMONSTRATION COMPLETE!")
    print("=" * 80)
    print("Key takeaways:")
    print("• function_registry.py contains your functions and schemas")
    print("• function_executor.py provides the execution engine")
    print("• You can easily extend the system with new functions")
    print("• You can create specialized systems for different domains")
    print("• Error handling is built-in")
    print("• Both direct execution and LLM integration are supported")
    print("=" * 80)

if __name__ == "__main__":
    main() 
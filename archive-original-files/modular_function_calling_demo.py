"""
Modular Function Calling Demo

This demonstrates how you can import and use the function calling system
with any set of functions. This is the power of modular design!
"""

# Import our modular components
from function_registry import AVAILABLE_FUNCTIONS, FUNCTION_SCHEMAS
from function_executor import create_function_caller_from_registry, test_function_execution

def main():
    """Demonstrate the modular function calling system"""
    
    print("🚀 MODULAR FUNCTION CALLING DEMO")
    print("=" * 60)
    
    # Create a function caller using our registry
    function_caller = create_function_caller_from_registry(
        function_registry=AVAILABLE_FUNCTIONS,
        function_schemas=FUNCTION_SCHEMAS
    )
    
    print(f"✅ Function caller created with {len(AVAILABLE_FUNCTIONS)} functions")
    print(f"Available functions: {list(AVAILABLE_FUNCTIONS.keys())}")
    
    # Test individual function execution (without LLM)
    print("\n🧪 TESTING INDIVIDUAL FUNCTIONS")
    print("=" * 60)
    
    # Test weather function
    weather_result = test_function_execution(
        AVAILABLE_FUNCTIONS, 
        "get_weather", 
        {"location": "Tokyo"}
    )
    print(f"Weather test: {weather_result}")
    
    # Test currency conversion
    currency_result = test_function_execution(
        AVAILABLE_FUNCTIONS,
        "convert_currency",
        {"amount": 100, "from_currency": "USD", "to_currency": "EUR"}
    )
    print(f"Currency test: {currency_result}")
    
    # Test with LLM (full workflow)
    print("\n🤖 TESTING WITH LLM")
    print("=" * 60)
    
    # Example 1: Weather query
    print("\n--- Example 1: Weather Query ---")
    function_caller.chat_with_functions("What's the weather like in Paris?")
    
    # Example 2: Currency conversion
    print("\n--- Example 2: Currency Conversion ---")
    function_caller.chat_with_functions("Convert 500 USD to EUR")
    
    # Example 3: Tip calculation
    print("\n--- Example 3: Tip Calculation ---")
    function_caller.chat_with_functions("I have a dinner bill of $120, what's a good 18% tip?")
    
    # Example 4: Distance calculation
    print("\n--- Example 4: Distance Calculation ---")
    function_caller.chat_with_functions("What's the distance between coordinates 40.7128, -74.0060 and 34.0522, -118.2437?")
    
    # Example 5: Notification
    print("\n--- Example 5: Send Notification ---")
    function_caller.chat_with_functions("Send a notification to john@example.com saying 'Meeting at 3 PM'")

def demonstrate_extensibility():
    """Show how easy it is to add new functions"""
    
    print("\n🔧 DEMONSTRATING EXTENSIBILITY")
    print("=" * 60)
    
    # Define a new function
    def calculate_bmi(weight_kg: float, height_m: float) -> dict:
        """Calculate Body Mass Index"""
        bmi = weight_kg / (height_m ** 2)
        
        if bmi < 18.5:
            category = "Underweight"
        elif bmi < 25:
            category = "Normal weight"
        elif bmi < 30:
            category = "Overweight"
        else:
            category = "Obese"
        
        return {
            "weight_kg": weight_kg,
            "height_m": height_m,
            "bmi": round(bmi, 2),
            "category": category,
            "status": "success"
        }
    
    # Create extended registry
    extended_functions = AVAILABLE_FUNCTIONS.copy()
    extended_functions["calculate_bmi"] = calculate_bmi
    
    # Create schema for new function
    bmi_schema = {
        "name": "calculate_bmi",
        "description": "Calculate Body Mass Index (BMI)",
        "parameters": {
            "type": "object",
            "properties": {
                "weight_kg": {
                    "type": "number",
                    "description": "Weight in kilograms"
                },
                "height_m": {
                    "type": "number", 
                    "description": "Height in meters"
                }
            },
            "required": ["weight_kg", "height_m"]
        }
    }
    
    extended_schemas = FUNCTION_SCHEMAS + [bmi_schema]
    
    # Create new function caller with extended registry
    extended_caller = create_function_caller_from_registry(
        function_registry=extended_functions,
        function_schemas=extended_schemas
    )
    
    print(f"✅ Extended function caller created with {len(extended_functions)} functions")
    print(f"New function added: calculate_bmi")
    
    # Test the new function
    print("\n--- Testing New BMI Function ---")
    extended_caller.chat_with_functions("Calculate my BMI if I weigh 70 kg and I'm 1.75 meters tall")

def demonstrate_custom_registry():
    """Show how to create a completely custom function registry"""
    
    print("\n🎨 CUSTOM FUNCTION REGISTRY")
    print("=" * 60)
    
    # Define custom functions for a specific domain (e.g., math operations)
    def add(a: float, b: float) -> dict:
        return {"result": a + b, "operation": "addition"}
    
    def multiply(a: float, b: float) -> dict:
        return {"result": a * b, "operation": "multiplication"}
    
    def power(base: float, exponent: float) -> dict:
        return {"result": base ** exponent, "operation": "exponentiation"}
    
    # Custom registry
    math_functions = {
        "add": add,
        "multiply": multiply,
        "power": power
    }
    
    # Custom schemas
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
            "name": "multiply", 
            "description": "Multiply two numbers",
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
            "name": "power",
            "description": "Raise a number to a power",
            "parameters": {
                "type": "object", 
                "properties": {
                    "base": {"type": "number", "description": "Base number"},
                    "exponent": {"type": "number", "description": "Exponent"}
                },
                "required": ["base", "exponent"]
            }
        }
    ]
    
    # Create math-specific function caller
    math_caller = create_function_caller_from_registry(
        function_registry=math_functions,
        function_schemas=math_schemas
    )
    
    print(f"✅ Math function caller created with {len(math_functions)} functions")
    print(f"Math functions: {list(math_functions.keys())}")
    
    # Test math operations
    print("\n--- Testing Math Operations ---")
    math_caller.chat_with_functions("What is 15 + 27?")
    math_caller.chat_with_functions("Calculate 8 times 9")
    math_caller.chat_with_functions("What is 2 to the power of 10?")

if __name__ == "__main__":
    main()
    demonstrate_extensibility()
    demonstrate_custom_registry()
    
    print("\n" + "="*60)
    print("🎉 MODULAR FUNCTION CALLING COMPLETE!")
    print("You can now create any function registry and use it with the executor!")
    print("="*60) 
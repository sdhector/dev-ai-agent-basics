"""
Simple Function Caller - No Executor Needed!

This demonstrates that you don't need a complex executor class.
The entire "function calling system" is just a dictionary lookup and function call!
"""

import json

# ============================================================================
# STEP 1: Define some functions
# ============================================================================

def get_weather(location: str, unit: str = "celsius") -> dict:
    """Get weather information for a location"""
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

def calculate_tip(bill_amount: float, tip_percentage: float = 15.0) -> dict:
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

def add_numbers(a: float, b: float) -> dict:
    """Add two numbers"""
    return {
        "a": a,
        "b": b,
        "result": a + b,
        "operation": "addition"
    }

def multiply_numbers(a: float, b: float) -> dict:
    """Multiply two numbers"""
    return {
        "a": a,
        "b": b,
        "result": a * b,
        "operation": "multiplication"
    }

# ============================================================================
# STEP 2: Create the function registry (THE ENTIRE "EXECUTOR"!)
# ============================================================================

FUNCTIONS = {
    "get_weather": get_weather,
    "calculate_tip": calculate_tip,
    "add_numbers": add_numbers,
    "multiply_numbers": multiply_numbers
}

# ============================================================================
# STEP 3: The "magic" function execution (THIS IS ALL YOU NEED!)
# ============================================================================

def call_function(function_name: str, arguments: dict):
    """
    Execute a function by name with arguments.
    
    This is the ENTIRE function calling system - just 2 lines of actual logic!
    """
    print(f"🔧 Calling: {function_name}({arguments})")
    
    # Check if function exists
    if function_name not in FUNCTIONS:
        result = {"error": f"Function '{function_name}' not found", "status": "error"}
        print(f"❌ Error: {result}")
        return result
    
    try:
        # THE MAGIC: Get function and call it
        function_to_call = FUNCTIONS[function_name]  # Dictionary lookup
        result = function_to_call(**arguments)       # Function call with unpacked args
        
        print(f"✅ Result: {result}")
        return result
        
    except Exception as e:
        result = {"error": str(e), "status": "error"}
        print(f"❌ Error: {result}")
        return result

# ============================================================================
# STEP 4: Simple interactive interface
# ============================================================================

def interactive_mode():
    """Simple interactive interface for testing"""
    print("🚀 SIMPLE FUNCTION CALLER")
    print("=" * 50)
    print("Available functions:")
    for name, func in FUNCTIONS.items():
        print(f"  • {name}: {func.__doc__ or 'No description'}")
    
    print("\nExamples:")
    print("  get_weather {\"location\": \"Tokyo\"}")
    print("  calculate_tip {\"bill_amount\": 50, \"tip_percentage\": 18}")
    print("  add_numbers {\"a\": 15, \"b\": 27}")
    print("\nType 'quit' to exit\n")
    
    while True:
        try:
            user_input = input("Enter function_name arguments: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            
            if not user_input:
                continue
            
            # Parse input: "function_name {json_arguments}"
            parts = user_input.split(' ', 1)
            if len(parts) != 2:
                print("❌ Format: function_name {\"arg1\": value1, \"arg2\": value2}")
                continue
            
            function_name = parts[0]
            try:
                arguments = json.loads(parts[1])
            except json.JSONDecodeError:
                print("❌ Invalid JSON arguments. Use: {\"key\": \"value\"}")
                continue
            
            # Call the function!
            call_function(function_name, arguments)
            print()
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

# ============================================================================
# STEP 5: Demo functions for testing
# ============================================================================

def demo_basic_usage():
    """Demonstrate basic usage"""
    print("🧪 DEMO: Basic Function Calling")
    print("=" * 40)
    
    # Test cases
    test_cases = [
        ("get_weather", {"location": "Tokyo"}),
        ("calculate_tip", {"bill_amount": 85.50, "tip_percentage": 20}),
        ("add_numbers", {"a": 15, "b": 27}),
        ("multiply_numbers", {"a": 8, "b": 9}),
    ]
    
    for function_name, arguments in test_cases:
        call_function(function_name, arguments)
        print()

def demo_error_handling():
    """Demonstrate error handling"""
    print("🧪 DEMO: Error Handling")
    print("=" * 40)
    
    # Error test cases
    error_cases = [
        ("nonexistent_function", {}),
        ("calculate_tip", {"invalid_arg": 123}),
        ("get_weather", {}),  # Missing required argument
    ]
    
    for function_name, arguments in error_cases:
        call_function(function_name, arguments)
        print()

def demo_adding_functions():
    """Demonstrate adding new functions"""
    print("🧪 DEMO: Adding New Functions")
    print("=" * 40)
    
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
    
    # Add it to the registry
    FUNCTIONS["calculate_bmi"] = calculate_bmi
    
    print(f"✅ Added new function! Registry now has {len(FUNCTIONS)} functions:")
    print(list(FUNCTIONS.keys()))
    print()
    
    # Test the new function
    call_function("calculate_bmi", {"weight_kg": 70, "height_m": 1.75})

def show_the_magic():
    """Show exactly what's happening under the hood"""
    print("🔍 THE MAGIC EXPLAINED")
    print("=" * 40)
    
    # Simulate what an LLM would send
    function_name = "calculate_tip"
    arguments = {"bill_amount": 50, "tip_percentage": 15}
    
    print(f"1. LLM says: Call '{function_name}' with {arguments}")
    print()
    
    print("2. We look up the function in our registry:")
    function_to_call = FUNCTIONS[function_name]
    print(f"   function_to_call = FUNCTIONS['{function_name}']")
    print(f"   function_to_call = {function_to_call}")
    print(f"   Type: {type(function_to_call)}")
    print(f"   Is it the same as calculate_tip? {function_to_call is calculate_tip}")
    print()
    
    print("3. We execute it with the arguments:")
    print(f"   result = function_to_call(**{arguments})")
    print("   The ** unpacks the dict into keyword arguments")
    print(f"   So this becomes: function_to_call(bill_amount=50, tip_percentage=15)")
    
    result = function_to_call(**arguments)
    print(f"   Result: {result}")
    print()
    
    print("💡 THAT'S IT! The entire 'executor' is just:")
    print("   function_to_call = FUNCTIONS[function_name]")
    print("   result = function_to_call(**arguments)")
    print()
    print("   No classes, no complex architecture - just Python basics!")

# ============================================================================
# MAIN INTERFACE
# ============================================================================

def main():
    """Main interface with options"""
    print("🚀 SIMPLE FUNCTION CALLING SYSTEM")
    print("=" * 50)
    print("This demonstrates that you don't need a complex executor!")
    print("The entire system is just a dictionary and 2 lines of code.")
    print("=" * 50)
    
    while True:
        print("\nChoose an option:")
        print("1. Interactive mode (call functions manually)")
        print("2. Demo basic usage")
        print("3. Demo error handling")
        print("4. Demo adding new functions")
        print("5. Show the magic (explain how it works)")
        print("6. Quit")
        
        choice = input("\nEnter choice (1-6): ").strip()
        
        if choice == "1":
            interactive_mode()
        elif choice == "2":
            demo_basic_usage()
        elif choice == "3":
            demo_error_handling()
        elif choice == "4":
            demo_adding_functions()
        elif choice == "5":
            show_the_magic()
        elif choice == "6":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please enter 1-6.")

if __name__ == "__main__":
    main() 
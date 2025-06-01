"""
The Absolute Minimal Function Calling System

This is the CORE of function calling - just 10 lines of actual code!
"""

# Step 1: Define some functions
def add(a, b):
    return {"result": a + b}

def multiply(a, b):
    return {"result": a * b}

def greet(name):
    return {"message": f"Hello, {name}!"}

# Step 2: Create the registry (THE ENTIRE "EXECUTOR"!)
FUNCTIONS = {
    "add": add,
    "multiply": multiply,
    "greet": greet
}

# Step 3: The "magic" execution function (THIS IS ALL YOU NEED!)
def execute(function_name, arguments):
    """The entire function calling system in 2 lines!"""
    function_to_call = FUNCTIONS[function_name]  # Dictionary lookup
    return function_to_call(**arguments)         # Function call

# That's it! Let's test it:
if __name__ == "__main__":
    print("🚀 MINIMAL FUNCTION CALLING DEMO")
    print("=" * 40)
    
    # Simulate what an LLM would send us
    test_calls = [
        ("add", {"a": 10, "b": 20}),
        ("multiply", {"a": 6, "b": 7}),
        ("greet", {"name": "Alice"}),
    ]
    
    for function_name, arguments in test_calls:
        print(f"Calling: {function_name}({arguments})")
        result = execute(function_name, arguments)
        print(f"Result: {result}")
        print()
    
    print("💡 THE ENTIRE SYSTEM:")
    print("   FUNCTIONS = {'name': function_object}")
    print("   function_to_call = FUNCTIONS[function_name]")
    print("   return function_to_call(**arguments)")
    print()
    print("   That's literally it! No classes, no complex architecture!") 
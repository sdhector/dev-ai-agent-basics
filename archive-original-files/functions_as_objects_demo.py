"""
MIND-BLOWING CONCEPT: Functions are Objects in Python!

This explains how you can store functions in dictionaries and variables.
"""

# ============================================================================
# STEP 1: Functions are Objects (This might blow your mind!)
# ============================================================================

def say_hello():
    return "Hello!"

def say_goodbye():
    return "Goodbye!"

print("🤯 FUNCTIONS ARE OBJECTS IN PYTHON!")
print("=" * 50)

# You can treat functions like any other value!
print(f"say_hello function object: {say_hello}")
print(f"Type of say_hello: {type(say_hello)}")
print(f"Is it callable? {callable(say_hello)}")

# You can store functions in variables
my_function = say_hello  # No parentheses! We're not calling it, just storing it
print(f"\nStored in variable: {my_function}")
print(f"Are they the same object? {my_function is say_hello}")

# Now my_function IS the say_hello function
result1 = say_hello()    # Call original
result2 = my_function()  # Call through variable
print(f"say_hello() = {result1}")
print(f"my_function() = {result2}")
print(f"Same result? {result1 == result2}")

# ============================================================================
# STEP 2: Functions in Dictionaries (The Registry Pattern)
# ============================================================================

print("\n🗂️ STORING FUNCTIONS IN DICTIONARIES")
print("=" * 50)

# You can put functions in dictionaries just like any other value!
function_registry = {
    "greet": say_hello,      # Key: string, Value: function object
    "farewell": say_goodbye  # Key: string, Value: function object
}

print(f"Dictionary contents: {function_registry}")
print(f"Type of 'greet' value: {type(function_registry['greet'])}")

# ============================================================================
# STEP 3: The Magic Lookup and Call
# ============================================================================

print("\n✨ THE MAGIC LOOKUP AND CALL")
print("=" * 50)

# Simulate what happens in function calling
function_name = "greet"  # This comes from LLM (as a string)

print(f"1. We want to call function named: '{function_name}'")

# This is the line you were confused about!
function_to_call = function_registry[function_name]
print(f"2. Looking up '{function_name}' in registry...")
print(f"3. function_to_call is now: {function_to_call}")

# At this point, function_to_call IS the say_hello function!
print(f"4. Is function_to_call the same as say_hello? {function_to_call is say_hello}")

# Now we can call it
result = function_to_call()
print(f"5. Calling function_to_call(): {result}")

# ============================================================================
# STEP 4: Step-by-Step Breakdown
# ============================================================================

print("\n🔍 STEP-BY-STEP BREAKDOWN")
print("=" * 50)

def add(a, b):
    return a + b

def multiply(a, b):
    return a * b

# Create the registry
math_functions = {
    "add": add,
    "multiply": multiply
}

print("Registry created:")
for name, func in math_functions.items():
    print(f"  '{name}' -> {func}")

# Simulate LLM request
operation = "add"  # LLM wants to call "add"
args = {"a": 5, "b": 3}  # LLM provides these arguments

print(f"\nLLM request: Call '{operation}' with {args}")

# The confusing line!
function_to_call = math_functions[operation]
print(f"After lookup: function_to_call = {function_to_call}")
print(f"This is literally the 'add' function: {function_to_call is add}")

# Call it
result = function_to_call(**args)
print(f"Result: {result}")

# ============================================================================
# STEP 5: Proving It's the Same Function
# ============================================================================

print("\n🧪 PROVING IT'S THE SAME FUNCTION")
print("=" * 50)

def test_function():
    return "I am the test function!"

# Store in variable
stored_func = test_function

# Store in dictionary
func_dict = {"test": test_function}

# All three are the SAME function object
print(f"Original function: {test_function}")
print(f"Stored in variable: {stored_func}")
print(f"Stored in dict: {func_dict['test']}")

print(f"\nAre they all the same object?")
print(f"stored_func is test_function: {stored_func is test_function}")
print(f"func_dict['test'] is test_function: {func_dict['test'] is test_function}")

print(f"\nCalling all three:")
print(f"test_function(): {test_function()}")
print(f"stored_func(): {stored_func()}")
print(f"func_dict['test'](): {func_dict['test']()}")

# ============================================================================
# STEP 6: Real-World Example
# ============================================================================

print("\n🌍 REAL-WORLD EXAMPLE")
print("=" * 50)

def get_weather(location):
    return f"Weather in {location}: Sunny, 25°C"

def calculate_tip(amount, percentage):
    return amount * (percentage / 100)

def send_email(to, subject):
    return f"Email sent to {to} with subject: {subject}"

# This is exactly what happens in function calling!
AVAILABLE_FUNCTIONS = {
    "get_weather": get_weather,
    "calculate_tip": calculate_tip,
    "send_email": send_email
}

# Simulate LLM responses
llm_requests = [
    {"name": "get_weather", "args": {"location": "Paris"}},
    {"name": "calculate_tip", "args": {"amount": 100, "percentage": 15}},
    {"name": "send_email", "args": {"to": "user@example.com", "subject": "Hello"}}
]

for request in llm_requests:
    function_name = request["name"]
    arguments = request["args"]
    
    print(f"\nLLM wants: {function_name}({arguments})")
    
    # The magic lookup!
    function_to_call = AVAILABLE_FUNCTIONS[function_name]
    print(f"Found function: {function_to_call.__name__}")
    
    # Execute it
    result = function_to_call(**arguments)
    print(f"Result: {result}")

print("\n" + "="*60)
print("🎉 NOW YOU UNDERSTAND THE FUNCTION REGISTRY PATTERN!")
print("Functions are just objects that can be stored and retrieved!")
print("="*60) 
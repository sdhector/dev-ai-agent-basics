# Function Calling System Usage Guide

This guide shows you how to use the modular function calling system with `function_registry.py` and `function_executor.py`.

## Quick Start

### 1. Basic Usage - Import and Use Existing Functions

```python
from function_registry import AVAILABLE_FUNCTIONS, FUNCTION_SCHEMAS
from function_executor import create_function_caller_from_registry

# Create a function caller
caller = create_function_caller_from_registry(AVAILABLE_FUNCTIONS, FUNCTION_SCHEMAS)

# Use it with LLM
response = caller.chat_with_functions("What's the weather in Tokyo?")
```

### 2. Test Functions Without LLM

```python
from function_executor import test_function_execution
from function_registry import AVAILABLE_FUNCTIONS

# Test a function directly
result = test_function_execution(
    AVAILABLE_FUNCTIONS,
    "calculate_tip", 
    {"bill_amount": 50.0, "tip_percentage": 18}
)
print(result)  # {'bill_amount': 50.0, 'tip_percentage': 18, 'tip_amount': 9.0, 'total_amount': 59.0, 'status': 'success'}
```

### 3. Add Your Own Functions

```python
from function_registry import AVAILABLE_FUNCTIONS, FUNCTION_SCHEMAS
from function_executor import create_function_caller_from_registry

# Define your custom function
def calculate_bmi(weight_kg: float, height_m: float) -> dict:
    bmi = weight_kg / (height_m ** 2)
    return {"bmi": round(bmi, 2), "status": "success"}

# Add to registry
extended_functions = AVAILABLE_FUNCTIONS.copy()
extended_functions["calculate_bmi"] = calculate_bmi

# Create schema
bmi_schema = {
    "name": "calculate_bmi",
    "description": "Calculate Body Mass Index",
    "parameters": {
        "type": "object",
        "properties": {
            "weight_kg": {"type": "number", "description": "Weight in kg"},
            "height_m": {"type": "number", "description": "Height in meters"}
        },
        "required": ["weight_kg", "height_m"]
    }
}

extended_schemas = FUNCTION_SCHEMAS + [bmi_schema]

# Create caller with your functions
caller = create_function_caller_from_registry(extended_functions, extended_schemas)
```

### 4. Create Specialized Systems

```python
# Math-only system
math_functions = {
    "add": lambda a, b: {"result": a + b},
    "multiply": lambda a, b: {"result": a * b}
}

math_schemas = [
    {
        "name": "add",
        "description": "Add two numbers",
        "parameters": {
            "type": "object",
            "properties": {
                "a": {"type": "number"},
                "b": {"type": "number"}
            },
            "required": ["a", "b"]
        }
    }
    # ... more schemas
]

math_caller = create_function_caller_from_registry(math_functions, math_schemas)
```

## Available Functions in Registry

The default registry includes:

- **get_weather(location, unit)** - Get weather for a location
- **calculate_tip(bill_amount, tip_percentage)** - Calculate tip and total
- **convert_currency(amount, from_currency, to_currency)** - Convert currencies
- **send_notification(message, recipient, channel)** - Send notifications
- **calculate_distance(lat1, lon1, lat2, lon2)** - Calculate distance between coordinates

## Key Components

### function_registry.py
- Contains `AVAILABLE_FUNCTIONS` dictionary (function name → function object)
- Contains `FUNCTION_SCHEMAS` list (OpenAI function schemas)
- Utility functions: `get_function_by_name()`, `is_function_available()`, etc.

### function_executor.py
- `FunctionExecutor` class - Core execution engine
- `LLMFunctionCaller` class - Complete LLM integration
- `create_function_caller_from_registry()` - Convenience function
- `test_function_execution()` - Test without LLM

## Error Handling

The system handles:
- Non-existent functions
- Invalid arguments
- Missing required parameters
- Function execution errors

All errors return structured error responses with `status: "error"`.

## Environment Setup

1. Create `.env` file with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

2. Install dependencies:
   ```bash
   pip install openai python-dotenv
   ```

## Examples

Run the demonstration script to see all features:

```bash
python demo_function_system.py
```

This shows:
- Basic registry usage
- Direct function execution
- LLM integration
- Error handling
- System extension
- Specialized systems

## The Magic Explained

The core of the system is this simple pattern:

```python
# 1. LLM returns function name and arguments
function_name = "calculate_tip"
arguments = {"bill_amount": 50, "tip_percentage": 15}

# 2. Look up the actual function object
function_to_call = AVAILABLE_FUNCTIONS[function_name]

# 3. Execute it with LLM's arguments
result = function_to_call(**arguments)
```

The `**arguments` unpacks the dictionary into keyword arguments, so `function_to_call(**{"a": 1, "b": 2})` becomes `function_to_call(a=1, b=2)`.

That's it! The LLM provides the function name and arguments, and Python's dynamic features handle the rest. 
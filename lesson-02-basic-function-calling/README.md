# Lesson 2: Basic Function Calling

## 🎯 Learning Objectives

By the end of this lesson, you will:
- Run your first working function calling example
- See the complete LLM → Function → Result workflow
- Understand the basic structure of a function calling system

## 📁 Files in This Lesson

- **`simple_function_call_demo.py`** - Bare-bones example showing raw JSON responses
- **`function_calling_example.py`** - Complete production-ready example

## 🚀 Start Here: Simple Demo

Run the simple demo first to see the basic concept:

```bash
python simple_function_call_demo.py
```

This shows you:
- How the LLM returns function call JSON
- How to parse that JSON
- How to execute the function
- **The confusing part**: How `AVAILABLE_FUNCTIONS[function_name]` works

## 🔍 What You'll See

The demo will show you output like this:

```
🤖 LLM Response (raw JSON):
{
  "function_call": {
    "name": "get_weather",
    "arguments": "{\"location\": \"Paris\"}"
  }
}

🔧 Executing function: get_weather
📋 Arguments: {'location': 'Paris'}
✅ Result: {'location': 'Paris', 'temperature': 18, 'condition': 'partly cloudy'}
```

## 🧩 The Key Lines (Don't Worry, We'll Explain These!)

You'll see these "magic" lines in the code:

```python
# This line confused many people (including you!)
function_to_call = AVAILABLE_FUNCTIONS[function_name]

# This line too!
result = function_to_call(**arguments)
```

**Don't worry if this looks confusing!** Lesson 3 will explain exactly how this works.

## 🏗️ Complete Example

After running the simple demo, try the complete example:

```bash
python function_calling_example.py
```

This shows a production-ready system with:
- Multiple functions (weather, tip calculator)
- Proper error handling
- Real OpenAI integration
- Complete conversation flow

## 🤔 Questions You Might Have

**Q: How does `AVAILABLE_FUNCTIONS[function_name]` work?**
A: Great question! This is covered in detail in Lesson 3.

**Q: What is `**arguments` doing?**
A: Another excellent question for Lesson 3!

**Q: How do I add my own functions?**
A: You'll learn this in Lesson 4 and beyond.

**Q: This seems complex - is there a simpler way?**
A: Yes! Lesson 4 shows the minimal version.

## 💡 Key Insights from This Lesson

1. **Function calling works!** You can actually execute functions based on LLM responses
2. **The pattern exists**: There's a clear structure to function calling systems
3. **It's not magic**: There are specific lines of code that make it work
4. **You can build this**: It's not as complex as it first appears

## 🎯 The Core Pattern

You've now seen the basic pattern:

```python
# 1. Define functions
def get_weather(location):
    # ... implementation

# 2. Create a registry
AVAILABLE_FUNCTIONS = {
    "get_weather": get_weather
}

# 3. LLM tells you what to call
function_name = "get_weather"  # From LLM
arguments = {"location": "Paris"}  # From LLM

# 4. Execute it (the "magic" lines)
function_to_call = AVAILABLE_FUNCTIONS[function_name]
result = function_to_call(**arguments)
```

## ✅ What's Next?

You've seen function calling in action, but you probably have questions about how those "magic" lines work.

**Next lesson** will demystify the execution mechanism and show you exactly what's happening under the hood.

---

**Previous:** [Lesson 1: Understanding the Problem](../lesson-01-understanding-the-problem/README.md)  
**Next:** [Lesson 3: Understanding the Execution Mechanism](../lesson-03-understanding-execution/README.md) 
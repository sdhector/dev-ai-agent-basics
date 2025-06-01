"""
Test the Simple Function Caller - Automated Demo

This shows how simple function calling really is!
"""

from simple_function_caller import call_function, FUNCTIONS, show_the_magic

def main():
    print("🚀 TESTING SIMPLE FUNCTION CALLER")
    print("=" * 50)
    
    print("Available functions:")
    for name, func in FUNCTIONS.items():
        print(f"  • {name}: {func.__doc__ or 'No description'}")
    print()
    
    # Test basic function calls
    print("🧪 BASIC FUNCTION CALLS:")
    print("-" * 30)
    
    call_function("get_weather", {"location": "Tokyo"})
    print()
    
    call_function("calculate_tip", {"bill_amount": 85.50, "tip_percentage": 20})
    print()
    
    call_function("add_numbers", {"a": 15, "b": 27})
    print()
    
    call_function("multiply_numbers", {"a": 8, "b": 9})
    print()
    
    # Test error handling
    print("🧪 ERROR HANDLING:")
    print("-" * 30)
    
    call_function("nonexistent_function", {})
    print()
    
    call_function("calculate_tip", {"invalid_arg": 123})
    print()
    
    call_function("get_weather", {})  # Missing required argument
    print()
    
    # Show the magic
    print("🔍 THE CORE INSIGHT:")
    print("-" * 30)
    show_the_magic()
    
    print("\n" + "=" * 50)
    print("💡 KEY TAKEAWAY:")
    print("The entire 'function calling system' is just:")
    print("  1. A dictionary: FUNCTIONS = {'name': function_object}")
    print("  2. Two lines: function_to_call = FUNCTIONS[name]")
    print("                result = function_to_call(**arguments)")
    print("=" * 50)

if __name__ == "__main__":
    main() 
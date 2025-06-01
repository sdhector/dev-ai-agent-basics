"""
Generic Function Executor

This module provides a reusable function execution system that can work
with any function registry. Import this and use it with any set of functions!
"""

import json
from typing import Dict, Any, Callable, List
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

class FunctionExecutor:
    """
    Generic function executor that can work with any function registry.
    
    This is the reusable component you can import anywhere!
    """
    
    def __init__(self, function_registry: Dict[str, Callable], function_schemas: List[Dict]):
        """
        Initialize with a function registry and schemas
        
        Args:
            function_registry: Dictionary mapping function names to function objects
            function_schemas: List of OpenAI function schemas
        """
        self.function_registry = function_registry
        self.function_schemas = function_schemas
    
    def execute_function_call(self, function_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a function call - this is the core magic!
        
        Args:
            function_name: Name of function to execute (from LLM)
            arguments: Arguments to pass to function (from LLM)
        
        Returns:
            Result of function execution
        """
        print(f"🔧 EXECUTING: {function_name}({arguments})")
        
        # Check if function exists
        if function_name not in self.function_registry:
            return {
                "error": f"Function '{function_name}' not found",
                "available_functions": list(self.function_registry.keys()),
                "status": "error"
            }
        
        try:
            # Get the actual function object (the magic line!)
            function_to_call = self.function_registry[function_name]
            
            # Execute it with LLM-provided arguments (the other magic line!)
            result = function_to_call(**arguments)
            
            print(f"✅ RESULT: {result}")
            return result
            
        except Exception as e:
            error_result = {
                "error": f"Error executing {function_name}: {str(e)}",
                "function_name": function_name,
                "arguments": arguments,
                "status": "error"
            }
            print(f"❌ ERROR: {error_result}")
            return error_result
    
    def get_available_functions(self) -> List[str]:
        """Get list of available function names"""
        return list(self.function_registry.keys())
    
    def get_function_schemas(self) -> List[Dict]:
        """Get function schemas for LLM"""
        return self.function_schemas
    
    def is_function_available(self, function_name: str) -> bool:
        """Check if a function is available"""
        return function_name in self.function_registry

class LLMFunctionCaller:
    """
    Complete LLM function calling system using the generic executor.
    
    This handles the full workflow: LLM -> Function Call -> Result -> LLM
    """
    
    def __init__(self, function_executor: FunctionExecutor, openai_client=None):
        """
        Initialize with a function executor and optional OpenAI client
        
        Args:
            function_executor: FunctionExecutor instance
            openai_client: OpenAI client (will create one if not provided)
        """
        self.executor = function_executor
        
        if openai_client is None:
            from openai import OpenAI
            self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        else:
            self.client = openai_client
    
    def chat_with_functions(self, user_message: str, model: str = "gpt-3.5-turbo") -> str:
        """
        Complete function calling workflow
        
        Args:
            user_message: User's message
            model: OpenAI model to use
        
        Returns:
            Final response from LLM
        """
        print(f"👤 USER: {user_message}")
        print("=" * 60)
        
        # Initial conversation
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
        
        # Send to LLM with available functions
        print("📤 SENDING TO LLM...")
        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
            functions=self.executor.get_function_schemas(),
            function_call="auto"
        )
        
        assistant_message = response.choices[0].message
        
        # Check if LLM wants to call a function
        if assistant_message.function_call:
            print("🎯 LLM WANTS TO CALL A FUNCTION!")
            
            # Extract function call details
            function_name = assistant_message.function_call.name
            function_args = json.loads(assistant_message.function_call.arguments)
            
            print(f"📋 FUNCTION: {function_name}")
            print(f"📋 ARGUMENTS: {function_args}")
            
            # Execute the function using our generic executor!
            function_result = self.executor.execute_function_call(function_name, function_args)
            
            # Continue conversation with function result
            messages.append(assistant_message)
            messages.append({
                "role": "function",
                "name": function_name,
                "content": json.dumps(function_result)
            })
            
            # Get final response from LLM
            print("📤 SENDING RESULT BACK TO LLM...")
            final_response = self.client.chat.completions.create(
                model=model,
                messages=messages
            )
            
            final_answer = final_response.choices[0].message.content
            print(f"🤖 FINAL RESPONSE: {final_answer}")
            return final_answer
        
        else:
            # No function call needed
            direct_answer = assistant_message.content
            print(f"🤖 DIRECT RESPONSE: {direct_answer}")
            return direct_answer

# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def create_function_caller_from_registry(function_registry: Dict[str, Callable], 
                                       function_schemas: List[Dict]) -> LLMFunctionCaller:
    """
    Convenience function to create a complete function calling system
    from a registry and schemas.
    
    Args:
        function_registry: Dictionary of functions
        function_schemas: List of OpenAI schemas
    
    Returns:
        Ready-to-use LLMFunctionCaller
    """
    executor = FunctionExecutor(function_registry, function_schemas)
    return LLMFunctionCaller(executor)

def test_function_execution(function_registry: Dict[str, Callable], 
                          function_name: str, 
                          arguments: Dict[str, Any]) -> Dict[str, Any]:
    """
    Test function execution without LLM (for debugging)
    
    Args:
        function_registry: Dictionary of functions
        function_name: Function to test
        arguments: Arguments to pass
    
    Returns:
        Function result
    """
    executor = FunctionExecutor(function_registry, [])
    return executor.execute_function_call(function_name, arguments) 
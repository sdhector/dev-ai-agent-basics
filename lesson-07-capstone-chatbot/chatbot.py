"""
Markdown File Chatbot - Main Implementation

A secure chatbot that can manage markdown files within a dedicated folder using OpenAI function calling.
"""

import os
import json
from typing import Dict, List, Optional
from openai import OpenAI
from dotenv import load_dotenv

from file_operations import (
    AVAILABLE_FUNCTIONS, 
    FUNCTION_SCHEMAS, 
    get_function_info,
    DOCUMENTS_ROOT
)

# Load environment variables
load_dotenv()

class MarkdownChatbot:
    """
    A chatbot that can manage markdown files using OpenAI function calling.
    
    Features:
    - Secure file operations within documents/ folder only
    - Natural language interface for file management
    - Intelligent function selection based on user intent
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the chatbot.
        
        Args:
            api_key: OpenAI API key (optional, will use environment variable if not provided)
        """
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        self.conversation_history = []
        
        # Initialize with system message
        self.conversation_history.append({
            "role": "system",
            "content": self._get_system_prompt()
        })
        
        print("🤖 Markdown Chatbot initialized!")
        print(f"📁 Working directory: {DOCUMENTS_ROOT}")
        print(f"🛠️ Available functions: {len(AVAILABLE_FUNCTIONS)}")
    
    def _get_system_prompt(self) -> str:
        """Get the system prompt that defines the chatbot's behavior."""
        function_list = "\n".join([f"- {name}" for name in AVAILABLE_FUNCTIONS.keys()])
        
        return f"""You are a helpful markdown file management assistant. You can help users manage their markdown files within a secure documents folder.

AVAILABLE FUNCTIONS:
{function_list}

SECURITY CONSTRAINTS:
- You can ONLY work with files in the documents/ folder
- You cannot access files outside this folder
- All file operations are restricted to this sandbox

CAPABILITIES:
- List files and folders in the documents directory
- Read, create, update, and delete markdown files
- Create directories and organize files
- Rename and move files within the documents folder

BEHAVIOR GUIDELINES:
- Always be helpful and clear in your responses
- Use functions when the user requests file operations
- Explain what you're doing before calling functions
- Provide clear feedback about the results
- If a function fails, explain why and suggest alternatives
- For destructive operations (delete), confirm the action was successful

RESPONSE STYLE:
- Be conversational and friendly
- Use emojis to make responses more engaging
- Provide helpful suggestions for next actions
- When showing file contents, format them nicely

Remember: You are a file management assistant focused on helping users organize and manage their markdown documents safely and efficiently."""

    def execute_function_call(self, function_name: str, arguments: Dict) -> Dict:
        """
        Execute a function call safely.
        
        Args:
            function_name: Name of the function to call
            arguments: Arguments to pass to the function
            
        Returns:
            Dict with function result
        """
        print(f"🔧 Executing: {function_name}({arguments})")
        
        if function_name not in AVAILABLE_FUNCTIONS:
            return {
                "error": f"Function '{function_name}' not available",
                "available_functions": list(AVAILABLE_FUNCTIONS.keys()),
                "status": "error"
            }
        
        try:
            function_to_call = AVAILABLE_FUNCTIONS[function_name]
            result = function_to_call(**arguments)
            
            print(f"✅ Result: {result.get('status', 'unknown')}")
            return result
            
        except Exception as e:
            error_result = {
                "error": f"Function execution failed: {str(e)}",
                "function_name": function_name,
                "arguments": arguments,
                "status": "execution_error"
            }
            print(f"❌ Error: {error_result}")
            return error_result

    def chat(self, user_message: str) -> str:
        """
        Process a user message and return the chatbot's response.
        
        Args:
            user_message: The user's input message
            
        Returns:
            The chatbot's response
        """
        # Add user message to conversation history
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        try:
            # Call OpenAI with function calling enabled
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=self.conversation_history,
                functions=FUNCTION_SCHEMAS,
                function_call="auto",
                temperature=0.7
            )
            
            message = response.choices[0].message
            
            # Check if the model wants to call a function
            if message.function_call:
                # Execute the function call
                function_name = message.function_call.name
                function_args = json.loads(message.function_call.arguments)
                
                print(f"\n🎯 LLM wants to call: {function_name}")
                print(f"📋 Arguments: {function_args}")
                
                # Execute the function
                function_result = self.execute_function_call(function_name, function_args)
                
                # Add the function call and result to conversation history
                self.conversation_history.append({
                    "role": "assistant",
                    "content": None,
                    "function_call": {
                        "name": function_name,
                        "arguments": message.function_call.arguments
                    }
                })
                
                self.conversation_history.append({
                    "role": "function",
                    "name": function_name,
                    "content": json.dumps(function_result)
                })
                
                # Get the final response from the model
                final_response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=self.conversation_history,
                    temperature=0.7
                )
                
                final_message = final_response.choices[0].message.content
                
            else:
                # No function call needed, just return the response
                final_message = message.content
            
            # Add assistant response to conversation history
            self.conversation_history.append({
                "role": "assistant",
                "content": final_message
            })
            
            return final_message
            
        except Exception as e:
            error_message = f"❌ Sorry, I encountered an error: {str(e)}"
            print(f"Error in chat: {e}")
            return error_message

    def get_conversation_summary(self) -> Dict:
        """Get a summary of the current conversation."""
        return {
            "total_messages": len(self.conversation_history),
            "user_messages": len([msg for msg in self.conversation_history if msg["role"] == "user"]),
            "assistant_messages": len([msg for msg in self.conversation_history if msg["role"] == "assistant"]),
            "function_calls": len([msg for msg in self.conversation_history if msg["role"] == "function"])
        }

    def reset_conversation(self):
        """Reset the conversation history."""
        self.conversation_history = [{
            "role": "system",
            "content": self._get_system_prompt()
        }]
        print("🔄 Conversation reset!")

def main():
    """
    Simple command-line interface for testing the chatbot.
    """
    print("🚀 MARKDOWN FILE CHATBOT")
    print("=" * 50)
    print("I can help you manage markdown files in your documents folder!")
    print("Try commands like:")
    print("  • 'List all my files'")
    print("  • 'Create a file called notes.md'")
    print("  • 'Read the welcome.md file'")
    print("  • 'Create a folder called projects'")
    print("\nType 'quit' to exit, 'reset' to start over, or 'help' for more info.\n")
    
    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  Warning: No OPENAI_API_KEY found in environment variables.")
        print("Please set your API key or create a .env file with:")
        print("OPENAI_API_KEY=your-api-key-here")
        return
    
    try:
        chatbot = MarkdownChatbot()
        
        while True:
            user_input = input("👤 You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            elif user_input.lower() == 'reset':
                chatbot.reset_conversation()
                continue
            elif user_input.lower() == 'help':
                print("\n📚 HELP:")
                print("Available commands:")
                for func_name in AVAILABLE_FUNCTIONS.keys():
                    print(f"  • {func_name}")
                print("\nExample requests:")
                print("  • 'Show me all my files'")
                print("  • 'Create a new file with some content'")
                print("  • 'Read my notes file'")
                print("  • 'Move my file to a different folder'")
                print("  • 'Delete that old file'\n")
                continue
            elif not user_input:
                continue
            
            print(f"\n🤖 Assistant: ", end="")
            response = chatbot.chat(user_input)
            print(response)
            print()
            
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main() 
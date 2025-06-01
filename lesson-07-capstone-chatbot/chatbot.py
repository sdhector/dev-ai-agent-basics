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

# Available OpenAI models with their details
AVAILABLE_MODELS = {
    "gpt-4o-mini": {
        "name": "GPT-4o Mini",
        "input_cost": 0.15,  # per million tokens
        "output_cost": 0.60,  # per million tokens
        "context_window": "128K",
        "description": "Best cost-efficient option - excellent performance at low cost",
        "recommended": True
    },
    "gpt-3.5-turbo": {
        "name": "GPT-3.5 Turbo",
        "input_cost": 0.50,  # per million tokens (legacy pricing)
        "output_cost": 1.50,  # per million tokens (legacy pricing)
        "context_window": "16K",
        "description": "Legacy model - consider upgrading to GPT-4o Mini",
        "recommended": False
    },
    "gpt-4-turbo": {
        "name": "GPT-4 Turbo",
        "input_cost": 10.00,  # per million tokens
        "output_cost": 30.00,  # per million tokens
        "context_window": "128K",
        "description": "High performance but expensive - use for complex tasks only",
        "recommended": False
    },
    "gpt-4": {
        "name": "GPT-4",
        "input_cost": 30.00,  # per million tokens
        "output_cost": 60.00,  # per million tokens
        "context_window": "8K",
        "description": "Most expensive option - use only when maximum quality needed",
        "recommended": False
    }
}

class MarkdownChatbot:
    """
    A chatbot that can manage markdown files using OpenAI function calling.
    
    Features:
    - Secure file operations within documents/ folder only
    - Natural language interface for file management
    - Intelligent function selection based on user intent
    - Model selection for cost optimization
    """
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4o-mini"):
        """
        Initialize the chatbot.
        
        Args:
            api_key: OpenAI API key (optional, will use environment variable if not provided)
            model: OpenAI model to use (default: gpt-4o-mini for best cost efficiency)
        """
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        self.model = model
        self.conversation_history = []
        
        # Validate model
        if model not in AVAILABLE_MODELS:
            print(f"⚠️  Warning: Model '{model}' not recognized. Using gpt-4o-mini instead.")
            self.model = "gpt-4o-mini"
        
        # Initialize with system message
        self.conversation_history.append({
            "role": "system",
            "content": self._get_system_prompt()
        })
        
        model_info = AVAILABLE_MODELS[self.model]
        print("🤖 Markdown Chatbot initialized!")
        print(f"📁 Working directory: {DOCUMENTS_ROOT}")
        print(f"🛠️ Available functions: {len(AVAILABLE_FUNCTIONS)}")
        print(f"🧠 Model: {model_info['name']} ({self.model})")
        print(f"💰 Cost: ${model_info['input_cost']:.2f}/${model_info['output_cost']:.2f} per million tokens")
        if model_info['recommended']:
            print("✅ Recommended model for cost efficiency")
    
    def get_available_models(self) -> Dict:
        """Get information about available models."""
        return AVAILABLE_MODELS
    
    def switch_model(self, new_model: str) -> bool:
        """
        Switch to a different OpenAI model.
        
        Args:
            new_model: Model identifier (e.g., 'gpt-4o-mini', 'gpt-4-turbo')
            
        Returns:
            True if switch was successful, False otherwise
        """
        if new_model not in AVAILABLE_MODELS:
            print(f"❌ Model '{new_model}' not available.")
            print("Available models:")
            for model_id, info in AVAILABLE_MODELS.items():
                status = "✅ RECOMMENDED" if info['recommended'] else ""
                print(f"  • {model_id}: {info['name']} - ${info['input_cost']:.2f}/${info['output_cost']:.2f} per M tokens {status}")
            return False
        
        old_model = self.model
        self.model = new_model
        model_info = AVAILABLE_MODELS[new_model]
        
        print(f"🔄 Switched from {AVAILABLE_MODELS[old_model]['name']} to {model_info['name']}")
        print(f"💰 New cost: ${model_info['input_cost']:.2f}/${model_info['output_cost']:.2f} per million tokens")
        if model_info['recommended']:
            print("✅ You're now using the recommended cost-efficient model!")
        elif not model_info['recommended'] and new_model != "gpt-4o-mini":
            print("💡 Tip: Consider 'gpt-4o-mini' for the best cost efficiency")
        
        return True
    
    def get_model_info(self) -> Dict:
        """Get information about the currently selected model."""
        return {
            "current_model": self.model,
            "model_info": AVAILABLE_MODELS[self.model],
            "available_models": AVAILABLE_MODELS
        }

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
            error_result = {
                "error": f"Function '{function_name}' not available",
                "available_functions": list(AVAILABLE_FUNCTIONS.keys()),
                "status": "error"
            }
            print(f"❌ Function not found: {error_result}")
            return error_result
        
        try:
            function_to_call = AVAILABLE_FUNCTIONS[function_name]
            result = function_to_call(**arguments)
            
            # Display the detailed function output for debugging
            print(f"📤 Function Output:")
            self._print_function_result(result)
            print(f"✅ Status: {result.get('status', 'unknown')}")
            
            return result
            
        except Exception as e:
            error_result = {
                "error": f"Function execution failed: {str(e)}",
                "function_name": function_name,
                "arguments": arguments,
                "status": "execution_error"
            }
            print(f"❌ Execution Error: {error_result}")
            return error_result

    def _print_function_result(self, result: Dict):
        """
        Print function result in a formatted, readable way for debugging.
        
        Args:
            result: The function result dictionary
        """
        if not isinstance(result, dict):
            print(f"  {result}")
            return
        
        status = result.get('status', 'unknown')
        
        if status == 'success':
            print(f"  ✅ Success")
            
            # Handle different types of successful results
            if 'files' in result and 'folders' in result:
                # list_directory result
                print(f"  📁 Found {result.get('total_files', 0)} files, {result.get('total_folders', 0)} folders")
                if result.get('files'):
                    print(f"  📄 Files: {[f['name'] for f in result['files'][:3]]}")
                if result.get('folders'):
                    print(f"  📂 Folders: {[f['name'] for f in result['folders'][:3]]}")
                    
            elif 'content' in result:
                # read_file result
                content_preview = result['content'][:100] + "..." if len(result['content']) > 100 else result['content']
                print(f"  📖 Content ({result.get('size', 0)} chars): {content_preview}")
                
            elif 'filename' in result and 'content_length' in result:
                # create_file result
                print(f"  📝 Created: {result['filename']} ({result['content_length']} chars)")
                
            elif 'mode' in result and 'new_content_length' in result:
                # update_file result
                print(f"  ✏️  Updated: {result['filename']} using {result['mode']} mode ({result['new_content_length']} chars)")
                
            elif 'deleted_size' in result:
                # delete_file result
                print(f"  🗑️  Deleted: {result['filename']} ({result['deleted_size']} bytes)")
                
            elif 'dirname' in result:
                # create_directory result
                print(f"  📁 Created directory: {result['dirname']}")
                
            elif 'old_name' in result and 'new_name' in result:
                # rename_file result
                print(f"  🏷️  Renamed: {result['old_name']} → {result['new_name']}")
                
            elif 'source' in result and 'destination' in result:
                # move_file or copy_file result
                action = "Moved" if "move" in str(result.get('message', '')).lower() else "Copied"
                print(f"  📦 {action}: {result['source']} → {result['destination']}")
                
            elif 'query' in result and 'results' in result:
                # search_files result
                print(f"  🔍 Search '{result['query']}': {result['total_matches']} matches in {result['total_files_searched']} files")
                if result['results']:
                    print(f"  📄 Found in: {[r['file'] for r in result['results'][:3]]}")
                    
            elif 'words' in result and 'lines' in result:
                # get_file_info result
                print(f"  📊 {result['filename']}: {result['words']} words, {result['lines']} lines, {result['headers']} headers")
                
            elif 'backup_file' in result:
                # create_backup result
                print(f"  💾 Backup created: {result['backup_file']} ({result['backup_size']} bytes)")
                
            elif 'days_back' in result and 'files' in result:
                # list_recent_files result
                print(f"  📅 Recent files ({result['days_back']} days): {result['total_found']} found")
                if result['files']:
                    print(f"  📄 Recent: {[f['file'] for f in result['files'][:3]]}")
                    
            else:
                # Generic success message
                message = result.get('message', 'Operation completed successfully')
                print(f"  💬 {message}")
                
        elif status == 'error':
            print(f"  ❌ Error: {result.get('error', 'Unknown error')}")
            
        elif status == 'security_error':
            print(f"  🔒 Security Error: {result.get('error', 'Security violation')}")
            
        else:
            print(f"  ❓ Unknown status: {status}")
            if 'error' in result:
                print(f"  ❌ Error: {result['error']}")
            if 'message' in result:
                print(f"  💬 Message: {result['message']}")

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
                model=self.model,
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
                    model=self.model,
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
            "function_calls": len([msg for msg in self.conversation_history if msg["role"] == "function"]),
            "current_model": self.model,
            "model_info": AVAILABLE_MODELS[self.model]
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
    print("\nSpecial commands:")
    print("  • 'models' - Show available AI models")
    print("  • 'switch to gpt-4o-mini' - Change AI model")
    print("  • 'model info' - Show current model details")
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
            elif user_input.lower() == 'models':
                print("\n🧠 AVAILABLE MODELS:")
                for model_id, info in chatbot.get_available_models().items():
                    current = "← CURRENT" if model_id == chatbot.model else ""
                    recommended = "✅ RECOMMENDED" if info['recommended'] else ""
                    print(f"  • {model_id}: {info['name']}")
                    print(f"    💰 ${info['input_cost']:.2f}/${info['output_cost']:.2f} per million tokens")
                    print(f"    📏 {info['context_window']} context")
                    print(f"    📝 {info['description']} {recommended} {current}")
                    print()
                continue
            elif user_input.lower().startswith('switch to '):
                model_name = user_input[10:].strip()
                chatbot.switch_model(model_name)
                continue
            elif user_input.lower() in ['model info', 'model']:
                info = chatbot.get_model_info()
                model_info = info['model_info']
                print(f"\n🧠 CURRENT MODEL: {model_info['name']} ({info['current_model']})")
                print(f"💰 Cost: ${model_info['input_cost']:.2f}/${model_info['output_cost']:.2f} per million tokens")
                print(f"📏 Context: {model_info['context_window']}")
                print(f"📝 {model_info['description']}")
                if model_info['recommended']:
                    print("✅ This is the recommended cost-efficient model!")
                print()
                continue
            elif user_input.lower() == 'help':
                print("\n📚 HELP:")
                print("Available commands:")
                for func_name in AVAILABLE_FUNCTIONS.keys():
                    print(f"  • {func_name}")
                print("\nModel commands:")
                print("  • 'models' - Show all available AI models")
                print("  • 'switch to MODEL_NAME' - Change AI model")
                print("  • 'model info' - Show current model details")
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
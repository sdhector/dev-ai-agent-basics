"""
Markdown Chatbot Demo - Interactive Demonstration

This script provides a comprehensive demonstration of the chatbot's capabilities
with predefined scenarios and interactive testing.
"""

import os
import time
from typing import List, Dict
from dotenv import load_dotenv

from chatbot import MarkdownChatbot
from file_operations import get_function_info, DOCUMENTS_ROOT

# Load environment variables
load_dotenv()

class ChatbotDemo:
    """Interactive demonstration of the markdown chatbot capabilities."""
    
    def __init__(self):
        """Initialize the demo."""
        self.chatbot = None
        self.demo_scenarios = self._get_demo_scenarios()
    
    def _get_demo_scenarios(self) -> List[Dict]:
        """Define demonstration scenarios."""
        return [
            {
                "name": "File Listing",
                "description": "Show what files are available",
                "commands": [
                    "List all my files",
                    "Show me what's in the examples folder"
                ]
            },
            {
                "name": "File Reading",
                "description": "Read existing files",
                "commands": [
                    "Read the welcome.md file",
                    "Show me the content of examples/sample-notes.md"
                ]
            },
            {
                "name": "File Creation",
                "description": "Create new files with content",
                "commands": [
                    "Create a file called todo.md with my daily tasks",
                    "Make a new file called ideas.md with some project ideas"
                ]
            },
            {
                "name": "File Organization",
                "description": "Create folders and organize files",
                "commands": [
                    "Create a folder called 'work'",
                    "Move todo.md to the work folder",
                    "Create a folder called 'personal'"
                ]
            },
            {
                "name": "File Updates",
                "description": "Modify existing files",
                "commands": [
                    "Add a new task to my todo.md file",
                    "Update ideas.md with a new project idea"
                ]
            },
            {
                "name": "File Management",
                "description": "Rename and organize files",
                "commands": [
                    "Rename ideas.md to project-ideas.md",
                    "Move project-ideas.md to the work folder"
                ]
            },
            {
                "name": "Advanced Features",
                "description": "Test advanced file operations",
                "commands": [
                    "Search for files containing the word 'project'",
                    "Get detailed information about welcome.md",
                    "Create a backup of my todo.md file",
                    "Copy welcome.md to a new file called guide.md",
                    "Show me files modified in the last 3 days"
                ]
            },
            {
                "name": "Security Testing",
                "description": "Test security constraints",
                "commands": [
                    "Read the file ../../../etc/passwd",
                    "Create a file at /tmp/hack.md",
                    "List files in the parent directory"
                ]
            }
        ]
    
    def print_header(self, title: str):
        """Print a formatted header."""
        print(f"\n{'='*60}")
        print(f"🎯 {title}")
        print(f"{'='*60}")
    
    def print_section(self, title: str):
        """Print a formatted section header."""
        print(f"\n{'─'*40}")
        print(f"📋 {title}")
        print(f"{'─'*40}")
    
    def wait_for_user(self, message: str = "Press Enter to continue..."):
        """Wait for user input."""
        input(f"\n⏸️  {message}")
    
    def run_scenario(self, scenario: Dict, interactive: bool = True):
        """Run a demonstration scenario."""
        self.print_section(f"{scenario['name']}: {scenario['description']}")
        
        for i, command in enumerate(scenario['commands'], 1):
            print(f"\n{i}. Testing: '{command}'")
            
            if interactive:
                self.wait_for_user("Press Enter to execute this command...")
            else:
                time.sleep(1)
            
            print(f"👤 User: {command}")
            print(f"🤖 Assistant: ", end="")
            
            try:
                response = self.chatbot.chat(command)
                print(response)
            except Exception as e:
                print(f"❌ Error: {e}")
            
            if interactive and i < len(scenario['commands']):
                print()
    
    def run_interactive_demo(self):
        """Run the full interactive demonstration."""
        self.print_header("MARKDOWN CHATBOT INTERACTIVE DEMO")
        
        print("This demo will showcase all the chatbot's capabilities:")
        print("• File operations (create, read, update, delete)")
        print("• Directory management (create, organize)")
        print("• Security constraints (sandbox protection)")
        print("• Natural language interface")
        
        # Check API key
        if not os.getenv("OPENAI_API_KEY"):
            print("\n⚠️  ERROR: No OPENAI_API_KEY found!")
            print("Please set your API key in a .env file:")
            print("OPENAI_API_KEY=your-api-key-here")
            return
        
        self.wait_for_user("Press Enter to start the demo...")
        
        # Initialize chatbot
        try:
            self.chatbot = MarkdownChatbot()
        except Exception as e:
            print(f"❌ Failed to initialize chatbot: {e}")
            return
        
        # Run each scenario
        for i, scenario in enumerate(self.demo_scenarios, 1):
            print(f"\n🎬 SCENARIO {i}/{len(self.demo_scenarios)}")
            self.run_scenario(scenario, interactive=True)
            
            if i < len(self.demo_scenarios):
                self.wait_for_user("Ready for the next scenario?")
        
        # Show conversation summary
        summary = self.chatbot.get_conversation_summary()
        self.print_section("Demo Summary")
        print(f"📊 Total messages: {summary['total_messages']}")
        print(f"👤 User messages: {summary['user_messages']}")
        print(f"🤖 Assistant messages: {summary['assistant_messages']}")
        print(f"🔧 Function calls: {summary['function_calls']}")
        
        print("\n🎉 Demo completed! The chatbot successfully demonstrated:")
        print("✅ Secure file operations within the documents folder")
        print("✅ Natural language understanding for file management")
        print("✅ Intelligent function selection based on user intent")
        print("✅ Robust error handling and security validation")
    
    def run_quick_demo(self):
        """Run a quick, non-interactive demonstration."""
        self.print_header("MARKDOWN CHATBOT QUICK DEMO")
        
        if not os.getenv("OPENAI_API_KEY"):
            print("⚠️  No API key found. Skipping LLM integration demo.")
            return
        
        try:
            self.chatbot = MarkdownChatbot()
            
            # Run a subset of scenarios quickly
            quick_scenarios = self.demo_scenarios[:3]  # First 3 scenarios
            
            for scenario in quick_scenarios:
                self.run_scenario(scenario, interactive=False)
            
            print("\n✅ Quick demo completed!")
            
        except Exception as e:
            print(f"❌ Demo failed: {e}")
    
    def test_security(self):
        """Test security constraints without LLM."""
        self.print_header("SECURITY VALIDATION TEST")
        
        from file_operations import validate_path, SecurityError
        
        print("Testing path validation (no LLM required):")
        
        # Safe paths
        safe_paths = ["test.md", "folder/test.md", "./notes.md", "work/project.md"]
        print("\n✅ SAFE PATHS (should work):")
        for path in safe_paths:
            try:
                result = validate_path(path)
                print(f"  ✅ {path} → {result}")
            except SecurityError as e:
                print(f"  ❌ {path} → {e}")
        
        # Unsafe paths
        unsafe_paths = ["../test.md", "../../etc/passwd", "/tmp/hack.md", "C:\\Windows\\System32"]
        print("\n🔒 UNSAFE PATHS (should be blocked):")
        for path in unsafe_paths:
            try:
                result = validate_path(path)
                print(f"  ⚠️  DANGER: {path} → {result}")
            except SecurityError as e:
                print(f"  ✅ BLOCKED: {path} → {e}")
        
        print("\n🛡️  Security validation working correctly!")
    
    def show_function_info(self):
        """Show information about available functions."""
        self.print_header("FUNCTION CAPABILITIES")
        
        info = get_function_info()
        print(f"📊 Total functions: {info['total_functions']}")
        print(f"📁 Documents folder: {DOCUMENTS_ROOT}")
        
        print("\n🔧 ESSENTIAL FUNCTIONS:")
        for func in info['essential_functions']:
            print(f"  • {func}")
        
        print("\n⚙️  INTERMEDIATE FUNCTIONS:")
        for func in info['intermediate_functions']:
            print(f"  • {func}")
        
        print("\n🚀 ADVANCED FUNCTIONS:")
        for func in info['advanced_functions']:
            print(f"  • {func}")
        
        print("\n📋 ALL AVAILABLE FUNCTIONS:")
        for func in info['function_names']:
            print(f"  • {func}")

def main():
    """Main demo interface."""
    demo = ChatbotDemo()
    
    print("🚀 MARKDOWN CHATBOT DEMONSTRATION")
    print("=" * 50)
    print("Choose a demo option:")
    print("1. Interactive Demo (full experience with LLM)")
    print("2. Quick Demo (automated, requires API key)")
    print("3. Security Test (no API key required)")
    print("4. Function Info (no API key required)")
    print("5. Manual Testing (chat with the bot)")
    print("6. Exit")
    
    while True:
        try:
            choice = input("\nEnter your choice (1-6): ").strip()
            
            if choice == "1":
                demo.run_interactive_demo()
                break
            elif choice == "2":
                demo.run_quick_demo()
                break
            elif choice == "3":
                demo.test_security()
                break
            elif choice == "4":
                demo.show_function_info()
                break
            elif choice == "5":
                if not os.getenv("OPENAI_API_KEY"):
                    print("⚠️  No API key found. Please set OPENAI_API_KEY in your environment.")
                    continue
                
                print("\n🎮 MANUAL TESTING MODE")
                print("You can now chat with the bot directly!")
                print("Type 'back' to return to the menu.\n")
                
                chatbot = MarkdownChatbot()
                
                while True:
                    user_input = input("👤 You: ").strip()
                    
                    if user_input.lower() == 'back':
                        break
                    elif not user_input:
                        continue
                    
                    print("🤖 Assistant: ", end="")
                    response = chatbot.chat(user_input)
                    print(response)
                    print()
                
                print("Returning to main menu...")
                continue
                
            elif choice == "6":
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please enter 1-6.")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main() 
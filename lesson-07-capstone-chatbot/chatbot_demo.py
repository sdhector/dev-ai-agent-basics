"""
Markdown File Chatbot - Interactive Demo

This script demonstrates the chatbot's capabilities including:
- File management operations
- Natural language interface
- Model selection and cost optimization
- Security constraints
"""

import os
import time
from dotenv import load_dotenv
from chatbot import MarkdownChatbot

# Load environment variables
load_dotenv()

def print_section(title: str):
    """Print a formatted section header."""
    print("\n" + "=" * 60)
    print(f"🎯 {title}")
    print("=" * 60)

def demo_chat(chatbot: MarkdownChatbot, message: str, description: str = ""):
    """Demonstrate a chat interaction."""
    if description:
        print(f"\n💡 {description}")
    print(f"👤 User: {message}")
    print("🤖 Assistant: ", end="")
    response = chatbot.chat(message)
    print(response)
    time.sleep(1)  # Brief pause for readability

def main():
    """Run the interactive chatbot demo."""
    print("🚀 MARKDOWN FILE CHATBOT - INTERACTIVE DEMO")
    print("=" * 60)
    print("This demo showcases the chatbot's capabilities including:")
    print("• File management operations")
    print("• Natural language interface") 
    print("• Model selection and cost optimization")
    print("• Security constraints")
    print("• Enhanced debugging features")
    
    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print("\n⚠️  ERROR: No OPENAI_API_KEY found!")
        print("Please set your API key in a .env file:")
        print("OPENAI_API_KEY=your-api-key-here")
        return
    
    try:
        # Initialize chatbot with default cost-efficient model
        print_section("INITIALIZATION & MODEL SELECTION")
        print("Initializing chatbot with cost-efficient GPT-4o Mini...")
        chatbot = MarkdownChatbot()
        
        # Show model information
        print("\n📊 Model Information:")
        model_info = chatbot.get_model_info()
        current_model = model_info['model_info']
        print(f"Current: {current_model['name']} ({model_info['current_model']})")
        print(f"Cost: ${current_model['input_cost']:.2f}/${current_model['output_cost']:.2f} per million tokens")
        print(f"Context: {current_model['context_window']}")
        
        # Demo 1: Model Comparison
        print_section("DEMO 1: MODEL COMPARISON & COST OPTIMIZATION")
        print("Let's explore the available models and their costs:")
        
        print("\n🧠 Available Models:")
        for model_id, info in chatbot.get_available_models().items():
            current = "← CURRENT" if model_id == chatbot.model else ""
            recommended = "✅ RECOMMENDED" if info['recommended'] else ""
            print(f"  • {model_id}: {info['name']}")
            print(f"    💰 ${info['input_cost']:.2f}/${info['output_cost']:.2f} per million tokens")
            print(f"    📏 {info['context_window']} context")
            print(f"    📝 {info['description']} {recommended} {current}")
            print()
        
        print("💡 Cost Comparison Example:")
        print("For 1 million input tokens + 200K output tokens:")
        for model_id, info in chatbot.get_available_models().items():
            total_cost = (1.0 * info['input_cost']) + (0.2 * info['output_cost'])
            print(f"  • {info['name']}: ${total_cost:.2f}")
        
        # Demo 2: Basic File Operations
        print_section("DEMO 2: BASIC FILE OPERATIONS")
        
        demo_chat(chatbot, "List all my files", 
                 "Starting with a simple directory listing")
        
        demo_chat(chatbot, "Create a file called demo-notes.md with some sample content about AI", 
                 "Creating a new file with content")
        
        demo_chat(chatbot, "Read the demo-notes.md file", 
                 "Reading the file we just created")
        
        demo_chat(chatbot, "Update demo-notes.md by adding a section about machine learning", 
                 "Updating existing file content")
        
        # Demo 3: Advanced Operations
        print_section("DEMO 3: ADVANCED FILE OPERATIONS")
        
        demo_chat(chatbot, "Create a folder called 'ai-research'", 
                 "Creating a new directory")
        
        demo_chat(chatbot, "Move demo-notes.md to the ai-research folder", 
                 "Moving files between directories")
        
        demo_chat(chatbot, "Search for files containing 'AI' or 'machine learning'", 
                 "Searching file contents")
        
        demo_chat(chatbot, "Get detailed information about the demo-notes.md file in ai-research", 
                 "Analyzing file statistics")
        
        demo_chat(chatbot, "Create a backup of ai-research/demo-notes.md", 
                 "Creating backup copies")
        
        # Demo 4: Model Switching
        print_section("DEMO 4: MODEL SWITCHING DEMONSTRATION")
        
        print("🔄 Let's try switching to a different model...")
        print("Current model cost for this conversation:")
        summary = chatbot.get_conversation_summary()
        current_cost = current_model['input_cost'] * 0.001  # Rough estimate
        print(f"Estimated cost so far: ~${current_cost:.4f}")
        
        # Try switching to GPT-4 (expensive model)
        print("\n🔄 Switching to GPT-4 (expensive model)...")
        success = chatbot.switch_model("gpt-4")
        if success:
            demo_chat(chatbot, "List recent files from the last 7 days", 
                     "Testing with the expensive model")
            
            # Switch back to cost-efficient model
            print("\n🔄 Switching back to cost-efficient GPT-4o Mini...")
            chatbot.switch_model("gpt-4o-mini")
        
        # Demo 5: Security Testing
        print_section("DEMO 5: SECURITY CONSTRAINT TESTING")
        
        demo_chat(chatbot, "List files in the parent directory", 
                 "Testing security: trying to access parent directory")
        
        demo_chat(chatbot, "Read the file ../../../etc/passwd", 
                 "Testing security: trying to access system files")
        
        demo_chat(chatbot, "Create a file at /tmp/hack.txt", 
                 "Testing security: trying to write outside sandbox")
        
        # Demo 6: Natural Language Understanding
        print_section("DEMO 6: NATURAL LANGUAGE UNDERSTANDING")
        
        demo_chat(chatbot, "Show me what I've been working on lately", 
                 "Natural language request for recent files")
        
        demo_chat(chatbot, "I need to organize my files better - what do you suggest?", 
                 "Asking for organizational advice")
        
        demo_chat(chatbot, "Clean up by removing the demo file we created", 
                 "Natural language deletion request")
        
        # Final Summary
        print_section("DEMO SUMMARY")
        
        final_summary = chatbot.get_conversation_summary()
        print("📊 Conversation Statistics:")
        print(f"  • Total messages: {final_summary['total_messages']}")
        print(f"  • User messages: {final_summary['user_messages']}")
        print(f"  • Assistant responses: {final_summary['assistant_messages']}")
        print(f"  • Function calls executed: {final_summary['function_calls']}")
        print(f"  • Final model: {final_summary['model_info']['name']}")
        print(f"  • Model cost: ${final_summary['model_info']['input_cost']:.2f}/${final_summary['model_info']['output_cost']:.2f} per million tokens")
        
        print("\n✅ Demo completed successfully!")
        print("\n💡 Key Takeaways:")
        print("  • GPT-4o Mini provides excellent performance at low cost")
        print("  • Model switching allows cost optimization for different tasks")
        print("  • Security constraints prevent unauthorized file access")
        print("  • Natural language interface makes file management intuitive")
        print("  • Enhanced debugging shows detailed function execution")
        
        # Interactive mode option
        print("\n🎮 INTERACTIVE MODE")
        print("Would you like to try the chatbot yourself? (y/n): ", end="")
        choice = input().strip().lower()
        
        if choice in ['y', 'yes']:
            print("\n🚀 Entering interactive mode...")
            print("Type 'quit' to exit, 'models' to see available models, or 'help' for commands.")
            print("Try commands like:")
            print("  • 'switch to gpt-4o-mini' - Change model")
            print("  • 'model info' - Show current model")
            print("  • 'create a file called test.md' - File operations")
            print()
            
            while True:
                try:
                    user_input = input("👤 You: ").strip()
                    
                    if user_input.lower() in ['quit', 'exit', 'q']:
                        print("👋 Thanks for trying the demo!")
                        break
                    elif user_input.lower() == 'models':
                        print("\n🧠 AVAILABLE MODELS:")
                        for model_id, info in chatbot.get_available_models().items():
                            current = "← CURRENT" if model_id == chatbot.model else ""
                            recommended = "✅ RECOMMENDED" if info['recommended'] else ""
                            print(f"  • {model_id}: {info['name']}")
                            print(f"    💰 ${info['input_cost']:.2f}/${info['output_cost']:.2f} per million tokens")
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
                        print(f"📝 {model_info['description']}")
                        if model_info['recommended']:
                            print("✅ This is the recommended cost-efficient model!")
                        print()
                        continue
                    elif not user_input:
                        continue
                    
                    print("🤖 Assistant: ", end="")
                    response = chatbot.chat(user_input)
                    print(response)
                    print()
                    
                except KeyboardInterrupt:
                    print("\n👋 Thanks for trying the demo!")
                    break
        else:
            print("👋 Thanks for watching the demo!")
            
    except Exception as e:
        print(f"\n❌ Demo error: {e}")
        print("Please check your API key and try again.")

if __name__ == "__main__":
    main() 
# Lesson 7: Capstone Project - Markdown File Chatbot

## 🎯 Project Overview

Build a **secure markdown file chatbot** that can read, write, and manage markdown files within a dedicated folder. This capstone project demonstrates real-world function calling with file operations, security constraints, and practical AI applications.

## 🎓 Learning Objectives

By completing this capstone, you will:
- Apply function calling to real file operations
- Implement security constraints (folder-restricted access)
- Build a practical AI assistant for document management
- Combine all previous lessons into a working application

## 🔒 Security Model

**Critical Constraint**: The chatbot can **ONLY** operate within the `documents/` folder. Any attempt to access files outside this folder will result in an error.

### Why This Matters
- **Prevents data breaches**: LLM can't access sensitive system files
- **Sandbox environment**: Safe to experiment without risk
- **Real-world pattern**: Production AI systems need strict boundaries

## 📁 Files in This Lesson

- **`README.md`** - This project guide
- **`file_operations.py`** - Secure file function registry
- **`chatbot.py`** - Main chatbot implementation
- **`chatbot_demo.py`** - Interactive demonstration
- **`requirements.txt`** - Dependencies
- **`documents/`** - Chatbot's sandbox folder
  - **`welcome.md`** - Sample file
  - **`examples/`** - Sample subfolder

## 🛠️ Function Set

### Essential Functions (5)
1. **`list_directory`** - Show files and folders
2. **`read_file`** - Read markdown file content
3. **`create_file`** - Create new markdown file
4. **`update_file`** - Modify existing file content
5. **`delete_file`** - Remove file (with confirmation)

### Intermediate Functions (3)
6. **`create_directory`** - Create new folders
7. **`rename_file`** - Change filename
8. **`move_file`** - Change file location

### Advanced Functions (5)
9. **`search_files`** - Find files by content or filename
10. **`copy_file`** - Duplicate files to new locations
11. **`get_file_info`** - Analyze file statistics and structure
12. **`create_backup`** - Create timestamped backup copies
13. **`list_recent_files`** - Show recently modified files

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Interactive Demo
```bash
python chatbot_demo.py
```

### 3. Try These Commands
```
"List all my files"
"Create a file called notes.md with some initial content"
"Read the welcome.md file"
"Create a folder called 'projects'"
"Move notes.md to the projects folder"
"Search for files containing 'project'"
"Get detailed information about welcome.md"
"Create a backup of my notes file"
```

## 🔧 Implementation Details

### Path Security
```python
import os
from pathlib import Path

DOCUMENTS_ROOT = Path(__file__).parent / "documents"

def validate_path(file_path: str) -> Path:
    """Ensure path is within documents folder"""
    full_path = (DOCUMENTS_ROOT / file_path).resolve()
    if not str(full_path).startswith(str(DOCUMENTS_ROOT.resolve())):
        raise SecurityError("Access denied: Path outside documents folder")
    return full_path
```

### Function Signatures
```python
def list_directory(path: str = ".") -> dict:
    """List files and folders in the documents directory"""

def read_file(filename: str) -> dict:
    """Read content of a markdown file"""

def create_file(filename: str, content: str = "") -> dict:
    """Create a new markdown file with optional content"""

def update_file(filename: str, content: str, mode: str = "replace") -> dict:
    """Update file content (replace/append/prepend)"""

def delete_file(filename: str) -> dict:
    """Delete a markdown file (with safety checks)"""

def create_directory(dirname: str) -> dict:
    """Create a new directory"""

def rename_file(old_name: str, new_name: str) -> dict:
    """Rename a file or directory"""

def move_file(source: str, destination: str) -> dict:
    """Move a file to a different location"""
```

## 🎮 Demo Scenarios

### Scenario 1: Note Taking
```
User: "Create a file called meeting-notes.md"
Bot: ✅ Created meeting-notes.md

User: "Add some content about today's project discussion"
Bot: ✅ Updated meeting-notes.md with content

User: "Show me what's in the file"
Bot: 📄 [displays file content]
```

### Scenario 2: Organization
```
User: "Create a folder called 'work'"
Bot: ✅ Created directory 'work'

User: "Move meeting-notes.md to the work folder"
Bot: ✅ Moved meeting-notes.md to work/

User: "List everything in the work folder"
Bot: 📁 work/meeting-notes.md
```

### Scenario 3: Security Test
```
User: "Read the file ../../../etc/passwd"
Bot: ❌ Access denied: Path outside documents folder
```

## 🔍 Key Features

### 1. **Intelligent File Operations**
- LLM decides when to use file functions based on user intent
- Natural language commands translate to function calls
- Context-aware responses

### 2. **Security First**
- All paths validated against sandbox folder
- No access to system files or parent directories
- Safe error handling for invalid operations

### 3. **Markdown Focus**
- Optimized for markdown file operations
- Content formatting and structure awareness
- Easy integration with documentation workflows

### 4. **User-Friendly**
- Natural language interface
- Clear success/error messages
- Helpful suggestions for next actions

### 5. **Enhanced Debugging**
- Detailed function execution logs
- Formatted output display for each function type
- Clear status indicators and error messages
- Real-time visibility into function results

## 🧪 Testing Your Implementation

### Basic Operations Test
```python
# Test in chatbot_demo.py
test_commands = [
    "List all files",
    "Create a test file",
    "Read the test file", 
    "Update the test file with new content",
    "Create a new folder",
    "Move the test file to the new folder",
    "Rename the test file",
    "Delete the test file"
]
```

### Security Test
```python
# These should all fail safely
security_tests = [
    "Read ../../../etc/passwd",
    "Create a file at /tmp/hack.md",
    "Delete C:\\Windows\\System32",
    "List files in .."
]
```

## 💡 Extension Ideas

After completing the basic implementation, consider adding:

1. **File Search**: Find files containing specific text
2. **Backup System**: Automatic backups before destructive operations
3. **Version History**: Track file changes over time
4. **Template System**: Create files from predefined templates
5. **Export Features**: Convert markdown to other formats

## 🎉 Success Criteria

You've successfully completed the capstone when:

✅ **All 13 functions work correctly**  
✅ **Security constraints are enforced**  
✅ **LLM makes intelligent function choices**  
✅ **Natural language interface feels intuitive**  
✅ **Error handling is robust and helpful**  
✅ **File operations are safe and reliable**  
✅ **Advanced features enhance productivity**  

## 🚀 Ready to Build?

Start with the file operations implementation:

**Next:** Explore `file_operations.py` to see the secure function registry

---

**Previous:** [Lesson 6: Modular Architecture](../lesson-06-modular-architecture/README.md)  
**🎓 Capstone Project** - Apply everything you've learned! 
"""
Secure File Operations for Markdown Chatbot

This module provides file operation functions that are restricted to the documents/ folder.
All functions include security validation to prevent access outside the sandbox.
"""

import os
import shutil
from pathlib import Path
from typing import Dict, List

# Security: Define the sandbox root
DOCUMENTS_ROOT = Path(__file__).parent / "documents"

class SecurityError(Exception):
    """Raised when attempting to access files outside the documents folder"""
    pass

def validate_path(file_path: str) -> Path:
    """
    Validate that a file path is within the documents folder.
    
    Args:
        file_path: Relative path from documents root
        
    Returns:
        Absolute Path object if valid
        
    Raises:
        SecurityError: If path attempts to escape documents folder
    """
    try:
        # Convert to absolute path and resolve any .. or . components
        full_path = (DOCUMENTS_ROOT / file_path).resolve()
        
        # Ensure the resolved path is still within documents folder
        if not str(full_path).startswith(str(DOCUMENTS_ROOT.resolve())):
            raise SecurityError(f"Access denied: Path '{file_path}' is outside documents folder")
            
        return full_path
    except Exception as e:
        raise SecurityError(f"Invalid path '{file_path}': {str(e)}")

def ensure_markdown_extension(filename: str) -> str:
    """Ensure filename has .md extension"""
    if not filename.endswith('.md'):
        filename += '.md'
    return filename

# ============================================================================
# ESSENTIAL FUNCTIONS (5)
# ============================================================================

def list_directory(path: str = ".") -> Dict:
    """
    List files and folders in the documents directory.
    
    Args:
        path: Relative path within documents folder (default: root)
        
    Returns:
        Dict with files, folders, and status information
    """
    try:
        target_path = validate_path(path)
        
        if not target_path.exists():
            return {
                "error": f"Directory '{path}' does not exist",
                "status": "error"
            }
            
        if not target_path.is_dir():
            return {
                "error": f"'{path}' is not a directory",
                "status": "error"
            }
        
        files = []
        folders = []
        
        for item in target_path.iterdir():
            relative_path = item.relative_to(DOCUMENTS_ROOT)
            if item.is_file():
                files.append({
                    "name": item.name,
                    "path": str(relative_path),
                    "size": item.stat().st_size,
                    "is_markdown": item.suffix == '.md'
                })
            elif item.is_dir():
                folders.append({
                    "name": item.name,
                    "path": str(relative_path)
                })
        
        return {
            "current_path": path,
            "files": files,
            "folders": folders,
            "total_files": len(files),
            "total_folders": len(folders),
            "status": "success"
        }
        
    except SecurityError as e:
        return {"error": str(e), "status": "security_error"}
    except Exception as e:
        return {"error": f"Failed to list directory: {str(e)}", "status": "error"}

def read_file(filename: str) -> Dict:
    """
    Read content of a markdown file.
    
    Args:
        filename: Name or path of the markdown file
        
    Returns:
        Dict with file content and metadata
    """
    try:
        filename = ensure_markdown_extension(filename)
        file_path = validate_path(filename)
        
        if not file_path.exists():
            return {
                "error": f"File '{filename}' does not exist",
                "status": "error"
            }
            
        if not file_path.is_file():
            return {
                "error": f"'{filename}' is not a file",
                "status": "error"
            }
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return {
            "filename": filename,
            "content": content,
            "size": len(content),
            "lines": len(content.splitlines()),
            "status": "success"
        }
        
    except SecurityError as e:
        return {"error": str(e), "status": "security_error"}
    except Exception as e:
        return {"error": f"Failed to read file: {str(e)}", "status": "error"}

def create_file(filename: str, content: str = "") -> Dict:
    """
    Create a new markdown file with optional content.
    
    Args:
        filename: Name or path of the new file
        content: Initial content for the file (default: empty)
        
    Returns:
        Dict with creation status and file info
    """
    try:
        filename = ensure_markdown_extension(filename)
        file_path = validate_path(filename)
        
        # Create parent directories if they don't exist
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        if file_path.exists():
            return {
                "error": f"File '{filename}' already exists",
                "status": "error"
            }
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return {
            "filename": filename,
            "content_length": len(content),
            "message": f"Successfully created '{filename}'",
            "status": "success"
        }
        
    except SecurityError as e:
        return {"error": str(e), "status": "security_error"}
    except Exception as e:
        return {"error": f"Failed to create file: {str(e)}", "status": "error"}

def update_file(filename: str, content: str, mode: str = "replace") -> Dict:
    """
    Update file content with different modes.
    
    Args:
        filename: Name or path of the file to update
        content: New content to add
        mode: Update mode - "replace", "append", or "prepend"
        
    Returns:
        Dict with update status and file info
    """
    try:
        filename = ensure_markdown_extension(filename)
        file_path = validate_path(filename)
        
        if not file_path.exists():
            return {
                "error": f"File '{filename}' does not exist",
                "status": "error"
            }
        
        if mode not in ["replace", "append", "prepend"]:
            return {
                "error": f"Invalid mode '{mode}'. Use 'replace', 'append', or 'prepend'",
                "status": "error"
            }
        
        if mode == "replace":
            new_content = content
        else:
            # Read existing content
            with open(file_path, 'r', encoding='utf-8') as f:
                existing_content = f.read()
            
            if mode == "append":
                new_content = existing_content + "\n" + content
            elif mode == "prepend":
                new_content = content + "\n" + existing_content
        
        # Write updated content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return {
            "filename": filename,
            "mode": mode,
            "new_content_length": len(new_content),
            "message": f"Successfully updated '{filename}' using {mode} mode",
            "status": "success"
        }
        
    except SecurityError as e:
        return {"error": str(e), "status": "security_error"}
    except Exception as e:
        return {"error": f"Failed to update file: {str(e)}", "status": "error"}

def delete_file(filename: str) -> Dict:
    """
    Delete a markdown file with safety checks.
    
    Args:
        filename: Name or path of the file to delete
        
    Returns:
        Dict with deletion status
    """
    try:
        filename = ensure_markdown_extension(filename)
        file_path = validate_path(filename)
        
        if not file_path.exists():
            return {
                "error": f"File '{filename}' does not exist",
                "status": "error"
            }
            
        if not file_path.is_file():
            return {
                "error": f"'{filename}' is not a file",
                "status": "error"
            }
        
        # Get file info before deletion
        file_size = file_path.stat().st_size
        
        # Delete the file
        file_path.unlink()
        
        return {
            "filename": filename,
            "deleted_size": file_size,
            "message": f"Successfully deleted '{filename}'",
            "status": "success"
        }
        
    except SecurityError as e:
        return {"error": str(e), "status": "security_error"}
    except Exception as e:
        return {"error": f"Failed to delete file: {str(e)}", "status": "error"}

# ============================================================================
# INTERMEDIATE FUNCTIONS (3)
# ============================================================================

def create_directory(dirname: str) -> Dict:
    """
    Create a new directory.
    
    Args:
        dirname: Name or path of the new directory
        
    Returns:
        Dict with creation status
    """
    try:
        dir_path = validate_path(dirname)
        
        if dir_path.exists():
            return {
                "error": f"Directory '{dirname}' already exists",
                "status": "error"
            }
        
        dir_path.mkdir(parents=True, exist_ok=False)
        
        return {
            "dirname": dirname,
            "message": f"Successfully created directory '{dirname}'",
            "status": "success"
        }
        
    except SecurityError as e:
        return {"error": str(e), "status": "security_error"}
    except Exception as e:
        return {"error": f"Failed to create directory: {str(e)}", "status": "error"}

def rename_file(old_name: str, new_name: str) -> Dict:
    """
    Rename a file or directory.
    
    Args:
        old_name: Current name or path
        new_name: New name (just the name, not full path)
        
    Returns:
        Dict with rename status
    """
    try:
        old_path = validate_path(old_name)
        
        if not old_path.exists():
            return {
                "error": f"'{old_name}' does not exist",
                "status": "error"
            }
        
        # For files, ensure .md extension
        if old_path.is_file():
            new_name = ensure_markdown_extension(new_name)
        
        # Create new path in same directory
        new_path = old_path.parent / new_name
        
        # Validate the new path is still in documents folder
        validate_path(str(new_path.relative_to(DOCUMENTS_ROOT)))
        
        if new_path.exists():
            return {
                "error": f"'{new_name}' already exists",
                "status": "error"
            }
        
        old_path.rename(new_path)
        
        return {
            "old_name": old_name,
            "new_name": new_name,
            "message": f"Successfully renamed '{old_name}' to '{new_name}'",
            "status": "success"
        }
        
    except SecurityError as e:
        return {"error": str(e), "status": "security_error"}
    except Exception as e:
        return {"error": f"Failed to rename: {str(e)}", "status": "error"}

def move_file(source: str, destination: str) -> Dict:
    """
    Move a file to a different location.
    
    Args:
        source: Current file path
        destination: Destination directory or full path
        
    Returns:
        Dict with move status
    """
    try:
        source_path = validate_path(source)
        
        if not source_path.exists():
            return {
                "error": f"Source '{source}' does not exist",
                "status": "error"
            }
        
        # If destination is a directory, keep the same filename
        dest_path = validate_path(destination)
        if dest_path.exists() and dest_path.is_dir():
            dest_path = dest_path / source_path.name
        elif source_path.is_file():
            # Ensure destination has .md extension for files
            dest_path = validate_path(ensure_markdown_extension(destination))
        
        # Validate final destination path
        validate_path(str(dest_path.relative_to(DOCUMENTS_ROOT)))
        
        # Create parent directories if needed
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        
        if dest_path.exists():
            return {
                "error": f"Destination '{dest_path.relative_to(DOCUMENTS_ROOT)}' already exists",
                "status": "error"
            }
        
        shutil.move(str(source_path), str(dest_path))
        
        return {
            "source": source,
            "destination": str(dest_path.relative_to(DOCUMENTS_ROOT)),
            "message": f"Successfully moved '{source}' to '{dest_path.relative_to(DOCUMENTS_ROOT)}'",
            "status": "success"
        }
        
    except SecurityError as e:
        return {"error": str(e), "status": "security_error"}
    except Exception as e:
        return {"error": f"Failed to move file: {str(e)}", "status": "error"}

# ============================================================================
# ADVANCED FUNCTIONS (5)
# ============================================================================

def search_files(query: str, search_type: str = "content") -> Dict:
    """
    Search for files containing specific text or matching filename patterns.
    
    Args:
        query: Text to search for
        search_type: "content" to search file contents, "filename" to search filenames
        
    Returns:
        Dict with search results
    """
    try:
        if search_type not in ["content", "filename"]:
            return {
                "error": f"Invalid search_type '{search_type}'. Use 'content' or 'filename'",
                "status": "error"
            }
        
        results = []
        total_searched = 0
        
        def search_directory(dir_path: Path):
            nonlocal total_searched
            for item in dir_path.rglob("*.md"):
                if item.is_file():
                    total_searched += 1
                    relative_path = item.relative_to(DOCUMENTS_ROOT)
                    
                    if search_type == "filename":
                        if query.lower() in item.name.lower():
                            results.append({
                                "file": str(relative_path),
                                "match_type": "filename",
                                "match_text": item.name
                            })
                    
                    elif search_type == "content":
                        try:
                            with open(item, 'r', encoding='utf-8') as f:
                                content = f.read()
                                if query.lower() in content.lower():
                                    # Find the line containing the match
                                    lines = content.splitlines()
                                    matching_lines = []
                                    for i, line in enumerate(lines, 1):
                                        if query.lower() in line.lower():
                                            matching_lines.append({
                                                "line_number": i,
                                                "line_content": line.strip()
                                            })
                                    
                                    results.append({
                                        "file": str(relative_path),
                                        "match_type": "content",
                                        "matches": matching_lines[:5]  # Limit to first 5 matches
                                    })
                        except Exception:
                            continue  # Skip files that can't be read
        
        search_directory(DOCUMENTS_ROOT)
        
        return {
            "query": query,
            "search_type": search_type,
            "results": results,
            "total_matches": len(results),
            "total_files_searched": total_searched,
            "status": "success"
        }
        
    except Exception as e:
        return {"error": f"Search failed: {str(e)}", "status": "error"}

def copy_file(source: str, destination: str) -> Dict:
    """
    Copy a file to a new location.
    
    Args:
        source: Source file path
        destination: Destination file path
        
    Returns:
        Dict with copy status
    """
    try:
        source_path = validate_path(source)
        
        if not source_path.exists():
            return {
                "error": f"Source file '{source}' does not exist",
                "status": "error"
            }
            
        if not source_path.is_file():
            return {
                "error": f"'{source}' is not a file",
                "status": "error"
            }
        
        # Ensure destination has .md extension
        destination = ensure_markdown_extension(destination)
        dest_path = validate_path(destination)
        
        # Create parent directories if needed
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        
        if dest_path.exists():
            return {
                "error": f"Destination '{destination}' already exists",
                "status": "error"
            }
        
        # Copy the file
        shutil.copy2(str(source_path), str(dest_path))
        
        return {
            "source": source,
            "destination": destination,
            "size": dest_path.stat().st_size,
            "message": f"Successfully copied '{source}' to '{destination}'",
            "status": "success"
        }
        
    except SecurityError as e:
        return {"error": str(e), "status": "security_error"}
    except Exception as e:
        return {"error": f"Failed to copy file: {str(e)}", "status": "error"}

def get_file_info(filename: str) -> Dict:
    """
    Get detailed information about a file.
    
    Args:
        filename: Name or path of the file
        
    Returns:
        Dict with file information
    """
    try:
        filename = ensure_markdown_extension(filename)
        file_path = validate_path(filename)
        
        if not file_path.exists():
            return {
                "error": f"File '{filename}' does not exist",
                "status": "error"
            }
            
        if not file_path.is_file():
            return {
                "error": f"'{filename}' is not a file",
                "status": "error"
            }
        
        # Get file stats
        stat = file_path.stat()
        
        # Read content for analysis
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        lines = content.splitlines()
        words = len(content.split())
        characters = len(content)
        
        # Analyze markdown structure
        headers = [line for line in lines if line.strip().startswith('#')]
        links = [line for line in lines if '[' in line and '](' in line]
        code_blocks = content.count('```')
        
        return {
            "filename": filename,
            "size_bytes": stat.st_size,
            "created": stat.st_ctime,
            "modified": stat.st_mtime,
            "lines": len(lines),
            "words": words,
            "characters": characters,
            "headers": len(headers),
            "links": len(links),
            "code_blocks": code_blocks // 2,  # Pairs of ```
            "is_empty": len(content.strip()) == 0,
            "status": "success"
        }
        
    except SecurityError as e:
        return {"error": str(e), "status": "security_error"}
    except Exception as e:
        return {"error": f"Failed to get file info: {str(e)}", "status": "error"}

def create_backup(filename: str) -> Dict:
    """
    Create a backup copy of a file with timestamp.
    
    Args:
        filename: Name or path of the file to backup
        
    Returns:
        Dict with backup status
    """
    try:
        filename = ensure_markdown_extension(filename)
        file_path = validate_path(filename)
        
        if not file_path.exists():
            return {
                "error": f"File '{filename}' does not exist",
                "status": "error"
            }
            
        if not file_path.is_file():
            return {
                "error": f"'{filename}' is not a file",
                "status": "error"
            }
        
        # Create backup filename with timestamp
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{file_path.stem}_backup_{timestamp}.md"
        backup_path = file_path.parent / backup_name
        
        # Validate backup path
        validate_path(str(backup_path.relative_to(DOCUMENTS_ROOT)))
        
        # Copy the file
        shutil.copy2(str(file_path), str(backup_path))
        
        return {
            "original_file": filename,
            "backup_file": str(backup_path.relative_to(DOCUMENTS_ROOT)),
            "backup_size": backup_path.stat().st_size,
            "timestamp": timestamp,
            "message": f"Successfully created backup of '{filename}'",
            "status": "success"
        }
        
    except SecurityError as e:
        return {"error": str(e), "status": "security_error"}
    except Exception as e:
        return {"error": f"Failed to create backup: {str(e)}", "status": "error"}

def list_recent_files(days: int = 7, limit: int = 10) -> Dict:
    """
    List recently modified files.
    
    Args:
        days: Number of days to look back (default: 7)
        limit: Maximum number of files to return (default: 10)
        
    Returns:
        Dict with recent files list
    """
    try:
        import datetime
        
        if days < 1 or days > 365:
            return {
                "error": "Days must be between 1 and 365",
                "status": "error"
            }
            
        if limit < 1 or limit > 100:
            return {
                "error": "Limit must be between 1 and 100",
                "status": "error"
            }
        
        cutoff_time = datetime.datetime.now() - datetime.timedelta(days=days)
        recent_files = []
        
        for file_path in DOCUMENTS_ROOT.rglob("*.md"):
            if file_path.is_file():
                stat = file_path.stat()
                modified_time = datetime.datetime.fromtimestamp(stat.st_mtime)
                
                if modified_time >= cutoff_time:
                    relative_path = file_path.relative_to(DOCUMENTS_ROOT)
                    recent_files.append({
                        "file": str(relative_path),
                        "modified": modified_time.isoformat(),
                        "size": stat.st_size,
                        "days_ago": (datetime.datetime.now() - modified_time).days
                    })
        
        # Sort by modification time (newest first)
        recent_files.sort(key=lambda x: x["modified"], reverse=True)
        
        # Apply limit
        recent_files = recent_files[:limit]
        
        return {
            "days_back": days,
            "total_found": len(recent_files),
            "files": recent_files,
            "status": "success"
        }
        
    except Exception as e:
        return {"error": f"Failed to list recent files: {str(e)}", "status": "error"}

# ============================================================================
# FUNCTION REGISTRY AND SCHEMAS
# ============================================================================

# Function registry for the chatbot
AVAILABLE_FUNCTIONS = {
    "list_directory": list_directory,
    "read_file": read_file,
    "create_file": create_file,
    "update_file": update_file,
    "delete_file": delete_file,
    "create_directory": create_directory,
    "rename_file": rename_file,
    "move_file": move_file,
    "search_files": search_files,
    "copy_file": copy_file,
    "get_file_info": get_file_info,
    "create_backup": create_backup,
    "list_recent_files": list_recent_files,
}

# OpenAI function schemas
FUNCTION_SCHEMAS = [
    {
        "name": "list_directory",
        "description": "List files and folders in the documents directory",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Relative path within documents folder (default: root)",
                    "default": "."
                }
            }
        }
    },
    {
        "name": "read_file",
        "description": "Read the content of a markdown file",
        "parameters": {
            "type": "object",
            "properties": {
                "filename": {
                    "type": "string",
                    "description": "Name or path of the markdown file to read"
                }
            },
            "required": ["filename"]
        }
    },
    {
        "name": "create_file",
        "description": "Create a new markdown file with optional initial content",
        "parameters": {
            "type": "object",
            "properties": {
                "filename": {
                    "type": "string",
                    "description": "Name or path of the new markdown file"
                },
                "content": {
                    "type": "string",
                    "description": "Initial content for the file",
                    "default": ""
                }
            },
            "required": ["filename"]
        }
    },
    {
        "name": "update_file",
        "description": "Update the content of an existing markdown file",
        "parameters": {
            "type": "object",
            "properties": {
                "filename": {
                    "type": "string",
                    "description": "Name or path of the file to update"
                },
                "content": {
                    "type": "string",
                    "description": "New content to add to the file"
                },
                "mode": {
                    "type": "string",
                    "enum": ["replace", "append", "prepend"],
                    "description": "How to update the file: replace all content, append to end, or prepend to beginning",
                    "default": "replace"
                }
            },
            "required": ["filename", "content"]
        }
    },
    {
        "name": "delete_file",
        "description": "Delete a markdown file",
        "parameters": {
            "type": "object",
            "properties": {
                "filename": {
                    "type": "string",
                    "description": "Name or path of the file to delete"
                }
            },
            "required": ["filename"]
        }
    },
    {
        "name": "create_directory",
        "description": "Create a new directory for organizing files",
        "parameters": {
            "type": "object",
            "properties": {
                "dirname": {
                    "type": "string",
                    "description": "Name or path of the new directory"
                }
            },
            "required": ["dirname"]
        }
    },
    {
        "name": "rename_file",
        "description": "Rename a file or directory",
        "parameters": {
            "type": "object",
            "properties": {
                "old_name": {
                    "type": "string",
                    "description": "Current name or path of the file/directory"
                },
                "new_name": {
                    "type": "string",
                    "description": "New name for the file/directory"
                }
            },
            "required": ["old_name", "new_name"]
        }
    },
    {
        "name": "move_file",
        "description": "Move a file to a different location within the documents folder",
        "parameters": {
            "type": "object",
            "properties": {
                "source": {
                    "type": "string",
                    "description": "Current path of the file to move"
                },
                "destination": {
                    "type": "string",
                    "description": "Destination directory or full path"
                }
            },
            "required": ["source", "destination"]
        }
    },
    {
        "name": "search_files",
        "description": "Search for files by content or filename patterns",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Text to search for"
                },
                "search_type": {
                    "type": "string",
                    "enum": ["content", "filename"],
                    "description": "Search in file contents or filenames",
                    "default": "content"
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "copy_file",
        "description": "Copy a file to a new location",
        "parameters": {
            "type": "object",
            "properties": {
                "source": {
                    "type": "string",
                    "description": "Source file path to copy"
                },
                "destination": {
                    "type": "string",
                    "description": "Destination file path"
                }
            },
            "required": ["source", "destination"]
        }
    },
    {
        "name": "get_file_info",
        "description": "Get detailed information about a file including size, word count, and structure",
        "parameters": {
            "type": "object",
            "properties": {
                "filename": {
                    "type": "string",
                    "description": "Name or path of the file to analyze"
                }
            },
            "required": ["filename"]
        }
    },
    {
        "name": "create_backup",
        "description": "Create a timestamped backup copy of a file",
        "parameters": {
            "type": "object",
            "properties": {
                "filename": {
                    "type": "string",
                    "description": "Name or path of the file to backup"
                }
            },
            "required": ["filename"]
        }
    },
    {
        "name": "list_recent_files",
        "description": "List recently modified files within a specified time period",
        "parameters": {
            "type": "object",
            "properties": {
                "days": {
                    "type": "integer",
                    "description": "Number of days to look back (1-365)",
                    "default": 7,
                    "minimum": 1,
                    "maximum": 365
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximum number of files to return (1-100)",
                    "default": 10,
                    "minimum": 1,
                    "maximum": 100
                }
            }
        }
    }
]

# Utility functions
def get_function_info() -> Dict:
    """Get information about available functions"""
    return {
        "total_functions": len(AVAILABLE_FUNCTIONS),
        "function_names": list(AVAILABLE_FUNCTIONS.keys()),
        "essential_functions": ["list_directory", "read_file", "create_file", "update_file", "delete_file"],
        "intermediate_functions": ["create_directory", "rename_file", "move_file"],
        "advanced_functions": ["search_files", "copy_file", "get_file_info", "create_backup", "list_recent_files"]
    }

if __name__ == "__main__":
    # Test the security validation
    print("🔒 Testing Security Validation")
    print("=" * 40)
    
    # These should work
    safe_tests = ["test.md", "folder/test.md", "./test.md"]
    for test in safe_tests:
        try:
            path = validate_path(test)
            print(f"✅ SAFE: {test} -> {path}")
        except SecurityError as e:
            print(f"❌ BLOCKED: {test} -> {e}")
    
    print()
    
    # These should be blocked
    unsafe_tests = ["../test.md", "../../etc/passwd", "/tmp/hack.md", "C:\\Windows\\System32"]
    for test in unsafe_tests:
        try:
            path = validate_path(test)
            print(f"⚠️  DANGER: {test} -> {path}")
        except SecurityError as e:
            print(f"✅ BLOCKED: {test} -> {e}")
    
    print(f"\n📊 Function Registry: {len(AVAILABLE_FUNCTIONS)} functions available")
    print(f"📋 Function Schemas: {len(FUNCTION_SCHEMAS)} schemas defined") 
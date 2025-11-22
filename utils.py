"""
Utility functions for file operations
Helper functions for saving JSON and error files
"""

import json


def save_json(data, filepath):
    """
    Save data to JSON file with proper formatting
    
    Args:
        data (list or dict): Data to save as JSON
        filepath (str): Path where JSON file should be saved
        
    Raises:
        Exception: If file writing fails
    """
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"✓ Valid flights saved to: {filepath}")
    except Exception as e:
        raise Exception(f"Error saving JSON: {e}")


def save_errors(errors, filepath):
    """
    Save error records to text file with human-readable format
    
    Args:
        errors (list): List of error dictionaries with keys:
            - line_number: Line number where error occurred
            - content: Original line content
            - reason: Error description
            - filename (optional): Source filename for directory parsing
        filepath (str): Path where error file should be saved
        
    Raises:
        Exception: If file writing fails
    """
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            for error in errors:
                line_num = error['line_number']
                content = error['content']
                reason = error['reason']
                
                # Include filename if present (for directory parsing)
                if 'filename' in error:
                    f.write(f"File: {error['filename']}, ")
                
                # Write error in format: Line X: content → reason
                f.write(f"Line {line_num}: {content} → {reason}\n")
    except Exception as e:
        raise Exception(f"Error saving errors: {e}")
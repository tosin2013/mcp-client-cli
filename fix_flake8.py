#!/usr/bin/env python3
"""
Quick fix script for critical flake8 issues
"""
import re
import os

def fix_line_lengths(file_path):
    """Fix line length issues by breaking long lines"""
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    modified = False
    new_lines = []
    
    for i, line in enumerate(lines):
        if len(line.rstrip()) > 79:
            # Try to break long lines at logical points
            if 'help=' in line and len(line) > 79:
                # Break help strings
                match = re.match(r'(\s*.*help=")([^"]+)(".*)', line)
                if match:
                    indent, help_text, suffix = match.groups()
                    if len(help_text) > 50:
                        # Split help text
                        words = help_text.split()
                        line1_words = []
                        line2_words = []
                        current_len = len(indent) + 6  # 'help="'
                        
                        for word in words:
                            if current_len + len(word) + 1 < 75:
                                line1_words.append(word)
                                current_len += len(word) + 1
                            else:
                                line2_words.append(word)
                        
                        if line2_words:
                            new_line1 = f'{indent}"{" ".join(line1_words)} "\n'
                            new_line2 = f'{" " * (len(indent) + 4)}"{" ".join(line2_words)}"{suffix}'
                            new_lines.extend([new_line1, new_line2])
                            modified = True
                            continue
            
            # For other long lines, try simple breaks
            if ',' in line and len(line) > 79:
                # Try to break at commas
                parts = line.split(',')
                if len(parts) > 1:
                    indent = len(line) - len(line.lstrip())
                    new_line = parts[0] + ',\n'
                    for part in parts[1:-1]:
                        new_line += ' ' * (indent + 4) + part.strip() + ',\n'
                    new_line += ' ' * (indent + 4) + parts[-1].strip()
                    if len(new_line.split('\n')[-1]) < 79:
                        new_lines.extend(new_line.split('\n'))
                        modified = True
                        continue
        
        new_lines.append(line)
    
    if modified:
        with open(file_path, 'w') as f:
            f.writelines(new_lines)
        print(f"Fixed line lengths in {file_path}")

def remove_unused_variables(file_path):
    """Remove unused variable assignments"""
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Remove the specific unused prompt variable
    pattern = r'\s*prompt = ChatPromptTemplate\.from_messages\(\s*\[.*?\]\s*\)\s*\n'
    new_content = re.sub(pattern, '', content, flags=re.DOTALL)
    
    if new_content != content:
        with open(file_path, 'w') as f:
            f.write(new_content)
        print(f"Removed unused variables in {file_path}")

def main():
    """Main function to fix flake8 issues"""
    cli_file = 'src/mcp_client_cli/cli.py'
    
    if os.path.exists(cli_file):
        remove_unused_variables(cli_file)
        fix_line_lengths(cli_file)
    
    print("Flake8 fixes completed!")

if __name__ == '__main__':
    main() 
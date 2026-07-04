import subprocess
import json
import os

def label_buggy_files():
    """Git history එක analyze කරලා buggy files හොයනවා"""
    
    try:
        # Git log එකෙන් හැම commit එකේම hash, message, files ගන්න
        result = subprocess.run(
            ['git', 'log', '--pretty=format:%H|%s', '--name-only'],
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        
        if result.returncode != 0 or not result.stdout:
            print("⚠️ No git history found or this is not a git repo.")
            return {}
        
        lines = result.stdout.split('\n')
        buggy_files = {}
        current_commit = None
        current_message = ""
        
        bug_keywords = ['fix', 'bug', 'resolve', 'issue', 'error', 'crash', 'hotfix', 'patch']
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # අලුත් commit එකක්ද? (hash|message format එක)
            if '|' in line and not line.startswith(' '):
                parts = line.split('|', 1)
                if len(parts) == 2:
                    current_commit = parts[0]
                    current_message = parts[1].lower()
            else:
                # මේ commit එකේ modified file එකක්
                if current_commit and line:
                    # අපි හිතනවා මේ commit එක bug fix එකක් නම්
                    is_bug_related = any(keyword in current_message for keyword in bug_keywords)
                    
                    if is_bug_related:
                        # .py files විතරක් ගන්න
                        if line.endswith('.py'):
                            # Windows paths handle කරන්න (\ instead of /)
                            file_path = line.replace('\\', '/')
                            if file_path not in buggy_files:
                                buggy_files[file_path] = 0
                            buggy_files[file_path] += 1
        
        return buggy_files
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return {}

if __name__ == "__main__":
    print("🔍 Labeling buggy files from git history...")
    buggy_files = label_buggy_files()
    
    if buggy_files:
        print(f"✅ Found {len(buggy_files)} potentially buggy files.")
        with open('buggy_labels.json', 'w') as f:
            json.dump(buggy_files, f, indent=2)
        print("💾 Saved labels to buggy_labels.json")
    else:
        print("⚠️ No buggy files found. Make sure you have commit history.")
import subprocess
import json
import os
import glob

def extract_features_from_pylint_direct(file_path):
    """
    Pylint එක Python එකෙන්ම run කරලා JSON output එක parse කරනවා
    """
    try:
        result = subprocess.run(
            ['pylint', file_path, '--output-format=json'],
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        
        # Pylint එකට code එක parse කරන්න බැරි උනොත් (syntax error) empty list එකක් return කරන්න
        if result.returncode != 0 and "syntax-error" in result.stdout:
            print(f"   ⚠️ Skipping {file_path} due to syntax error.")
            return None
            
        try:
            data = json.loads(result.stdout)
        except json.JSONDecodeError:
            # No output or invalid JSON
            return None
        
        if not data:
            # No issues found
            return {
                'file_path': file_path,
                'total_issues': 0,
                'total_errors': 0,
                'total_warnings': 0,
                'total_conventions': 0,
                'has_undefined_variable': 0,
                'has_unused_import': 0,
                'has_docstring_issues': 0,
                'has_formatting_issues': 0,
                'unique_message_ids_count': 0
            }
        
        # Initialize counters
        features = {
            'file_path': file_path,
            'total_issues': len(data),
            'total_errors': 0,
            'total_warnings': 0,
            'total_conventions': 0,
            'has_undefined_variable': 0,
            'has_unused_import': 0,
            'has_docstring_issues': 0,
            'has_formatting_issues': 0,
            'unique_message_ids_count': 0
        }
        
        unique_ids = set()
        
        for issue in data:
            msg_id = issue['message-id']
            unique_ids.add(msg_id)
            
            if issue['type'] == 'error':
                features['total_errors'] += 1
            elif issue['type'] == 'warning':
                features['total_warnings'] += 1
            elif issue['type'] == 'convention':
                features['total_conventions'] += 1
            
            if msg_id == 'E0602':
                features['has_undefined_variable'] = 1
            elif msg_id == 'W0611':
                features['has_unused_import'] = 1
            elif msg_id in ['C0114', 'C0116']:
                features['has_docstring_issues'] = 1
            elif msg_id in ['C0303', 'C0304']:
                features['has_formatting_issues'] = 1
        
        features['unique_message_ids_count'] = len(unique_ids)
        return features
        
    except FileNotFoundError:
        print("❌ Pylint not found! Run: pip install pylint")
        return None
    except Exception as e:
        print(f"❌ Error processing {file_path}: {e}")
        return None


def scan_all_python_files():
    """වත්මන් directory එකේ තියෙන හැම .py file එකක්ම scan කරනවා"""
    
    # හැම .py file එකක්ම හොයාගන්න (current directory + subdirectories)
    python_files = glob.glob('**/*.py', recursive=True)
    
    # 'venv', 'env', '__pycache__' වගේ folders exclude කරන්න
    exclude_dirs = ['venv', 'env', '__pycache__', '.git', 'node_modules']
    python_files = [f for f in python_files if not any(excluded in f for excluded in exclude_dirs)]
    
    if not python_files:
        print("❌ No Python files found in the current directory!")
        return
    
    print(f"🔍 Found {len(python_files)} Python files to scan...\n")
    
    all_features = []
    error_count = 0
    
    for idx, file in enumerate(python_files, 1):
        print(f"📄 [{idx}/{len(python_files)}] Scanning: {file}")
        features = extract_features_from_pylint_direct(file)
        
        if features:
            all_features.append(features)
        else:
            error_count += 1
    
    print(f"\n✅ Successfully scanned {len(all_features)} files. ({error_count} files skipped)")
    
    # Save to JSON
    with open('all_features.json', 'w') as f:
        json.dump(all_features, f, indent=2)
    
    # Save to CSV (ඒක ML train කරන්න පහසුයි)
    try:
        import pandas as pd
        df = pd.DataFrame(all_features)
        df.to_csv('dataset_features.csv', index=False)
        print(f"\n💾 Saved features to dataset_features.csv ({len(df)} rows)")
    except ImportError:
        print("\n💾 Saved features to all_features.json (pandas not installed, install with 'pip install pandas')")


if __name__ == "__main__":
    scan_all_python_files()
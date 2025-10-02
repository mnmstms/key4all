import platform
from pathlib import Path
from typing import Dict, List, Any
import json
import glob

TOOL_NAME = "vscode"

def find_keybindings_files() -> list[str]:
    system = platform.system()
    home = Path.home()
    results = []

    if system == 'Windows':
        appdata = Path.home() / 'AppData' / 'Roaming'
        vscode_glob = str(appdata / 'Code' / 'User' / 'keybindings*.json')
        for p in glob.glob(vscode_glob):
            results.append(str(Path(p).resolve()))
    elif system == 'Darwin':  # macOS
        vscode_glob = str(home / 'Library' / 'Application Support' / 'Code' / 'User' / 'keybindings*.json')
        for p in glob.glob(vscode_glob):
            results.append(str(Path(p).resolve()))
    else:  # Assume Linux or other Unix-like
        vscode_glob = str(home / '.config' / 'Code' / 'User' / 'keybindings*.json')
        for p in glob.glob(vscode_glob):
            results.append(str(Path(p).resolve()))

    return results

def generate(master_config: Dict) -> str:
    # Generate the json content for VS Code keybindings based on the master config
    
    entires: List[Dict[str, Any]] = []
    for entry in master_config:
        if '_tool' in entry and entry['_tool'] != TOOL_NAME:
            continue
        
        keys = entry.get('key')
        if not isinstance(keys, list):
            keys = [keys]
        for key in keys:
            binding = {
                "key": key,
                "command": entry['command']
            }
            if 'when' in entry:
                binding["when"] = entry['when']
            entires.append(binding)
    
    return json.dumps(entires, indent=2, ensure_ascii=False) + "\n"


if __name__ == '__main__':
    print(find_keybindings_files())

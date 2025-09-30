import platform
from pathlib import Path
from typing import Dict, List, Any
import json
import glob

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
    cfg: Any = master_config
    return json.dumps(list(cfg), indent=2, ensure_ascii=False) + "\n"


if __name__ == '__main__':
    print(find_keybindings_files())

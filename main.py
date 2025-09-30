import argparse
import json
import re
from pathlib import Path

import intellij
import vscode


def generate(master_config_path: str):
    master_config = json.load(open(master_config_path, 'r', encoding='utf-8'))
    vscode_file_content = vscode.generate(master_config)
    print("Writing VS Code keybindings files:")
    for path in vscode.find_keybindings_files():
        print(f" - {path}")
        with open(path, 'w', encoding='utf-8') as f:
            f.write(vscode_file_content)

    intellij_file_content = intellij.generate(master_config)
    print("Writing IntelliJ keymap files:")
    for path in intellij.get_target_keymap_files():
        print(f" - {path}")
        with open(path, 'w', encoding='utf-8') as f:
            f.write(intellij_file_content)            

def debug(master_config_path: str):
    print("Discovered VS Code keybindings files:")
    for path in vscode.find_keybindings_files():
        print(f" - {path}")
    print("Discovered IntelliJ keymap files:")
    for path in intellij.get_target_keymap_files():
        print(f" - {path}")

    master_config = json.load(open(master_config_path, 'r', encoding='utf-8'))

    vscode_file_content = vscode.generate(master_config)
    with open(master_config_path+'.debug_vscode.json', 'w', encoding='utf-8') as f:
        f.write(vscode_file_content)
    
    intellij_file_content = intellij.generate(master_config)
    with open(master_config_path+'.debug_intellij.xml', 'w', encoding='utf-8') as f:
        f.write(intellij_file_content)

def main():
    parser = argparse.ArgumentParser(description='Synchronize key shortcuts between different IDEs')
    subparsers = parser.add_subparsers(dest='command')

    gen_parser = subparsers.add_parser('generate', help='Generate keymap from master config')
    gen_parser.add_argument('--master', default="example/master.json", help='Master config JSON file')

    debug_parser = subparsers.add_parser('debug', help='Write discovered vscode config info to _debug_vscode.json')
    debug_parser.add_argument('--master', default="example/master.json", help='Master config JSON file')

    args = parser.parse_args()

    if args.command == 'generate':
        generate(args.master)
    elif args.command == 'debug':
        debug(args.master)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()

import glob
from pathlib import Path
from typing import Dict, Any

CLEAR_OUT_ACTION_IDS = [
    "Console.TableResult.CopyAggregatorResult",
    "CopyAbsolutePath",
    "CopyPaths",
    "EditorLookupDown",
    "EditorLookupUp",
    "EditorScrollDown",
    "EditorScrollUp",
    "MethodOverloadSwitchDown",
    "MethodOverloadSwitchUp",
    "NotebookSelectCellAboveAction",
    "NotebookSelectCellBelowAction",
    "RemoteHostView.CopyPaths",
    "Terminal.LineDown",
    "Terminal.LineUp",
    "Terminal.SelectLastBlock",
    "Terminal.SelectPrompt",
    "WelcomeScreen.CopyProjectPath",
    "copilot.chat.show",
    "org.intellij.plugins.markdown.ui.actions.styling.ToggleCodeSpanAction",
    "CloseActiveTab",
    "CollapseSelection",
    "DatabaseView.PropertiesAction",
    "EditorChooseLookupItemDot",
    "FileChooser.TogglePathBar",
    "Jdbc.OpenConsole.New",
    "Jdbc.OpenConsole.New.Generate",
    "Print",
    "UsageFiltering.WriteAccess",
    "context.save"
]

def find_user_keymap_dirs() -> list[str]:
    home = Path.home()
    results = []

    # Generic .config JetBrains locations
    cfg_glob = str(home / '.config' / 'JetBrains' / '*' / 'keymaps')
    for p in glob.glob(cfg_glob):
        results.append(str(Path(p).resolve()))

    return results

def get_target_keymap_files() -> list[str]:
    return [ dir+'/key4all.xml' for dir in find_user_keymap_dirs() ]

def _convert_key_to_intellij_format(key: str) -> str:
    # This is a simplified conversion, real-world usage may require more comprehensive mapping
    key = key.replace('+', ' ')
    return key

def _convert_action_id(action: str) -> str:
    case_map = {
        "editor.action.triggerParameterHints": "ParameterInfo",
        "workbench.action.closeActiveEditor": "CloseContent",
        "editor.action.commentLine": "CommentByLineComment",
        "editor.action.deleteLines": "EditorDeleteLine",
        "editor.action.moveLinesUpAction": "MoveLineUp",
        "editor.action.moveLinesDownAction": "MoveLineDown",
        "workbench.action.navigateBack": "Back",
        "workbench.action.navigateForward": "Forward",
        "editor.action.joinLines": "EditorJoinLines",
        "editor.action.toggleWordWrap": "EditorToggleUseSoftWraps",
        "editor.action.copyLinesDownAction": "DuplicateLines",
        "workbench.action.terminal.toggleTerminal": "ActivateTerminalToolWindow",
        "workbench.action.focusActiveEditorGroup": "FocusEditor",
        "workbench.view.explorer": "ActivateProjectToolWindow",
        "actions.find": "Find"
    }
    return case_map.get(action, None)


def generate(master_config: Dict) -> str:
    # Generate the json content for VS Code keybindings based on the master config
    intellij_actions = []

    for action_id in CLEAR_OUT_ACTION_IDS:
        intellij_actions.append(f'  <action id="{action_id}">\n  </action>')

    for shortcut in master_config:
        action_id = _convert_action_id(shortcut.get("command"))
        if not action_id:
            print(f"Warning: No IntelliJ action mapping for VS Code action '{shortcut.get('command')}', skipping...")
            continue
        intellij_shortcut = _convert_key_to_intellij_format(shortcut.get("key"))
        intellij_actions.append(f'  <action id="{action_id}">\n    <keyboard-shortcut first-keystroke="{intellij_shortcut}"/>\n  </action>')
        
    return '<keymap version="1" name="key4all" parent="Eclipse">\n' + "\n".join(intellij_actions) + '\n</keymap>\n'

if __name__ == '__main__':
    print(get_target_keymap_files())

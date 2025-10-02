import glob
import platform
from pathlib import Path
from typing import Dict, Any

TOOL_NAME = "intellij"

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
    system = platform.system()

    if system == 'Windows':
        # Windows locations for JetBrains IDEs
        appdata = home / 'AppData' / 'Roaming' / 'JetBrains'
        if appdata.exists():
            # Look for all JetBrains IDE directories
            cfg_glob = str(appdata / '*' / 'keymaps')
            for p in glob.glob(cfg_glob):
                results.append(str(Path(p).resolve()))
        
        # Also check Local AppData (some versions use this)
        local_appdata = home / 'AppData' / 'Local' / 'JetBrains'
        if local_appdata.exists():
            cfg_glob = str(local_appdata / '*' / 'keymaps')
            for p in glob.glob(cfg_glob):
                results.append(str(Path(p).resolve()))
    else:
        # Generic .config JetBrains locations (Linux/macOS)
        cfg_glob = str(home / '.config' / 'JetBrains' / '*' / 'keymaps')
        for p in glob.glob(cfg_glob):
            results.append(str(Path(p).resolve()))
    return results

def get_target_keymap_files() -> list[str]:
    return [ dir+'/key4all.xml' for dir in find_user_keymap_dirs() ]

def _convert_key_to_intellij_format(key: str) -> str:
    if key.startswith('mousebutton'):
        return key.replace('mousebutton', 'button')
    
    key = key.replace('+', ' ')
    return key

def _convert_action_id(action: str) -> str:
    case_map = {
        "editor.action.triggerParameterHints": "ParameterInfo",        
        
        "editor.action.copyLinesDownAction": "DuplicateLines",
        "editor.action.commentLine": "CommentByLineComment",
        "editor.action.deleteLines": "EditorDeleteLine",
        "editor.action.moveLinesUpAction": "MoveLineUp",
        "editor.action.moveLinesDownAction": "MoveLineDown",
        
        "workbench.action.closeActiveEditor": "CloseContent",
        "workbench.action.reopenClosedEditor": "ReopenClosedTab",
        "workbench.action.navigateBack": "Back",
        "workbench.action.navigateForward": "Forward",
        "editor.action.goToImplementation": "GotoImplementation",
        
        "editor.action.joinLines": "EditorJoinLines",
        "editor.action.rename": "RenameElement",
        
        "editor.action.toggleWordWrap": "EditorToggleUseSoftWraps",
        
        "workbench.action.terminal.toggleTerminal": "ActivateTerminalToolWindow",
        "workbench.action.focusActiveEditorGroup": "FocusEditor",
        "workbench.view.explorer": "ActivateProjectToolWindow",
        "workbench.files.action.showActiveFileInExplorer": "SelectInProjectView",
        "actions.find": "Find",
        "workbench.action.findInFiles": "FindInPath",
        
        "editor.action.jumpToBracket": "EditorMatchBrace",
        "workbench.action.showCommands": "GotoAction",
        "editor.action.formatDocument": "ReformatCode",
        "workbench.panel.chat.view.copilot.focus": "copilot.chat.show",
    }
    return case_map.get(action, None)


def generate(master_config: Dict) -> str:
    # Generate the json content for VS Code keybindings based on the master config
    intellij_actions = []

    for action_id in CLEAR_OUT_ACTION_IDS:
        intellij_actions.append(f'  <action id="{action_id}">\n  </action>')

    for entry in master_config:
        if '_tool' in entry and entry['_tool'] != TOOL_NAME:
            continue
        
        action_id = _convert_action_id(entry.get("command"))
        if not action_id:
            print(f"Warning: No IntelliJ action mapping for VS Code action '{entry.get('command')}', skipping...")
            continue
        keys = entry.get("key")
        if not isinstance(keys, list):
            keys = [keys]
        
        intellij_actions.append(f'  <action id="{action_id}">')
        for key in keys:
            intellij_shortcut = _convert_key_to_intellij_format(key)      
            if key.startswith('mousebutton'):                
                intellij_actions.append(f'    <mouse-shortcut keystroke="{intellij_shortcut}"/>')
            else:
                intellij_actions.append(f'    <keyboard-shortcut first-keystroke="{intellij_shortcut}"/>')
            
        intellij_actions.append(f'  </action>')
        
        
    return '<keymap version="1" name="key4all" parent="Eclipse">\n' + "\n".join(intellij_actions) + '\n</keymap>\n'

if __name__ == '__main__':
    print(get_target_keymap_files())

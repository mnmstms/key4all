# key4all

A tool to manage and synchronize keyboard shortcuts across different applications and platforms.

## What it does

key4all reads a master JSON describing keyboard shortcuts and writes platform/editor-specific
keybinding/keymap files so you can keep shortcuts consistent across VS Code and JetBrains IDEs.

## Features

- Generate VS Code keybindings JSON files
- Generate IntelliJ keymap XML files
- Simple master config format (see below)

## Requirements

- Python 3

## Usage

Run in debug mode to see what files would be written and what changes would be made:

```fish
python main.py debug --master master.json
```

Generate keymaps from a master config:

```fish
python main.py generate --master master.json
```

By default the script uses `example/master.json` if `--master` is not provided.

## Master config format

The master config is a JSON array of shortcut objects. The same format what VS Code uses for keybindings.
The commands are also VS Code command identifiers, for example `editor.action.commentLine`, might be extended in the future if needed.

```json
[
	{
		"command": "editor.action.commentLine",
		"key": "ctrl+/"
	},
	{
		"command": "workbench.action.closeActiveEditor",
		"key": "ctrl+w"
	}
]
```

## Where outputs are written

- VS Code keybindings are written to discovered user config directories, for example:
  - Linux: `~/.config/Code/User/keybindings.json`
  - Windows: `%APPDATA%\Code\User\keybindings.json`
  - macOS: `~/Library/Application Support/Code/User/keybindings.json`
- IntelliJ keymap files are written to all discovered JetBrains IDE config directories, for example:
  - Linux: `~/.config/JetBrains/<IDE><VERSION>/keymaps/Key4All.xml`
  - Windows: `%APPDATA%\JetBrains\<IDE><VERSION>\keymaps\Key4All.xml`
  - macOS: `~/Library/Application Support/JetBrains/<IDE><VERSION>/keymaps/Key4All.xml`

## Contributing

Contributions welcome — open an issue or submit a PR.

## License

This project is licensed under the GNU General Public License v3.0 (GPL-3.0).

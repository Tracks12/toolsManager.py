# **WSLBuilder**

[Back to index](../README.md)

## Summary

- [**WSLBuilder**](#wslbuilder)
  - [Summary](#summary)
  - [I. Preview](#i-preview)
  - [II. Command Prompt](#ii-command-prompt)

## I. Preview

![preview](previews/wslbuilder.gif)

[Summary](#summary)

## II. Command Prompt

Usage in shell: `$ python main.py -t wslbuilder <argument>`

Usage in script: `wslbuilder <argument>`

| Arguments             | Values ​ ​      | Descriptions                                                |
| --------------------- | --------------- | ----------------------------------------------------------- |
| `-d`, `--delete`      | `<distro>`, `*` | Remove a wsl distribution image and disk                    |
| `-D`, `--full-delete` | `<distro>`, `*` | Remove a wsl distribution image and disk with docker traces |
| `-e`, `--export`      | `<distro>`      | Export a wsl distribution into a tar image                  |
| `-i`, `--install`     | `<distro>`      | Install a wsl distribution to workspace                     |
| `-I`, `--init`        |                 | Init a wsl builder instance with docker                     |
| `-l`, `--list`        |                 | List all wsl distributions                                  |
| `-n`, `--new`         | `<distro>`      | Create a wsl distribution                                   |
| `-S`, `--stat`        | `<distro>`      | Show statistics about a wsl distributions                   |
| `-s`, `--start`       | `<distro>`      | Launch a wsl instance                                       |
| `-h`, `--help`        |                 | Show the helper commands menu                               |
| `-v`, `--version`     |                 | Show version of tool                                        |

[Summary](#summary)

[Back to index](../README.md)

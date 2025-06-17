# **ToolsManager.py**

A multi-tool with a generic template for developing management tools like WSLBuilder for managing WSL instances built using images exported from Docker.

## Summary

- [**ToolsManager.py**](#toolsmanagerpy)
  - [Summary](#summary)
  - [I. Preview](#i-preview)
  - [II. Prerequisites](#ii-prerequisites)
    - [II.1 Dependencies](#ii1-dependencies)
    - [II.2 WSL / Docker](#ii2-wsl--docker)
  - [III. Uses](#iii-uses)
    - [III.1 Tool Management](#iii1-tool-management)
    - [III.2 WSL Management with WSLBuilder](#iii2-wsl-management-with-wslbuilder)
  - [IV. Options \& Configurations](#iv-options--configurations)
  - [V. Contributing](#v-contributing)
  - [VI. License](#vi-license)

## I. Preview

![preview](preview.gif)

[Summary](#summary)

## II. Prerequisites

> [!Warning]
> Installing **[Python 3](https://www.python.org/downloads/)** is recommended to run this script on Windows.

[Summary](#summary)

### II.1 Dependencies

- [base64.b64decode](https://docs.python.org/3/library/base64.html#base64.b64decode), [base64.b64encode](https://docs.python.org/3/library/base64.html#base64.b64encode)
- [json.loads](https://docs.python.org/3/library/json.html#json.loads), [json.dumps](https://docs.python.org/3/library/json.html#json.dumps), [json.load](https://docs.python.org/3/library/json.html#json.load), [json.dump](https://docs.python.org/3/library/json.html#json.dump)
- [os.listdir](https://docs.python.org/3/library/os.html#os.listdir), [os.mkdir](https://docs.python.org/3/library/os.html#os.mkdir), [os.remove](https://docs.python.org/3/library/os.html#os.remove), [os.rmdir](https://docs.python.org/3/library/os.html#os.rmdir), [os.system](https://docs.python.org/3/library/os.html#os.system), [os.path](https://docs.python.org/3/library/os.path.html#os.path)
- [platform.system](https://docs.python.org/3/library/platform.html#platform.system)
- [re.split](https://docs.python.org/3/library/re.html#re.split)
- [random.shuffle](https://docs.python.org/3/library/random.html#random.shuffle)
- [readline](https://docs.python.org/3/library/readline.html)
- [shutil.rmtree](https://docs.python.org/3/library/shutil.html#shutil.rmtree)
- [sys.argv](https://docs.python.org/3/library/sys.html#sys.argv), [sys.version_info](https://docs.python.org/3/library/sys.html#sys.version_info)
- [time.sleep](https://docs.python.org/3/library/time.html#time.sleep)
- [traceback.format_exc](https://docs.python.org/3/library/traceback.html#traceback.format_exc)

> [!Note]
> [readline](https://docs.python.org/3/library/readline.html) is for multiline finder in linux system

[Summary](#summary)

### II.2 WSL / Docker

[Summary](#summary)

## III. Uses

Command prompt: `$python main.py <argument>`

| Arguments             | Values ​             ​| Descriptions                                |
| --------------------- | ------------------- | ------------------------------------------- |
| `-g`, `--generate`    | -                   | Generate a tool with interactive inputs     |
| `-l`, `--list`        | -                   | Display the list of Python tools            |
| `-s`, `--set`         | `<prop>`, `<value>` | Apply new configuration value to a property |
| `-t <tool>`, `--tool` | `<tool>`            | Launch a tool                               |
| `-h`, `--help`        | -                   | Display the help menu                       |
| `-D`, `--debug`       | -                   | Run in debugger mode                        |
| `-v`, `--version`     | -                   | Display the program version                 |

[Summary](#summary)

### III.1 Tool Management

[Summary](#summary)

### III.2 WSL Management with WSLBuilder

[Summary](#summary)

## IV. Options & Configurations

The program is configured from the **[config.json](config.json)** file in **json** format. In this file, you can set the **character encoding** and the splash screen display.

```json
{
  "colors": false,
  "encoding": "utf-8",
  "splash": true
}
```

You can modify it directly (which is not recommended) or use the configuration program with **all possible parameter choices in the "Parameters" option in the main menu**.

[Summary](#summary)

## V. Contributing

If you to contribute to the project, you access to the coding guideline at [CONTRIBUTING.md](CONTRIBUTING.md)

## VI. License

Code licensed under [GPL v3](LICENSE)

[Summary](#summary)

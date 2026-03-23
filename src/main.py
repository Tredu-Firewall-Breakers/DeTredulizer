from EasyMenu3 import easymenu, print_table, colors
from pathlib import Path

import os
import sys
import winreg
import importlib.util

# Config
APP_NAME = "DeTredulizer"

# Setup menu stuff using EasyMenu3
# Create menu objects
main_menu = easymenu(
    name=APP_NAME,
    author="Tredu Firewall Breakers",
    make_screen=True,
    url="https://github.com/Tredu-Firewall-Breakers/DeTredulizer",
    url_label="Github",
    print_ascii_title=True,
    print_ascii_title_each_time=False
)

plugins_menu = easymenu(name="Plugins", print_ascii_title=False)

# Add static menu items/paths
main_menu.add_menu_option("Plugins", plugins_menu, item_key="1")

# Plugin loading
plugins = []

def get_plugin_dir():
    if getattr(sys, "frozen", False):
        base_dir = Path(sys.executable).parent
    else:
        base_dir = Path(__file__).parent

    plugins_dir = base_dir / "plugins"

    if not plugins_dir.exists():
        print(f"Plugins directory not found at {plugins_dir}. Creating it.")
        plugins_dir.mkdir(parents=True, exist_ok=True)

    return plugins_dir

def load_plugins():
    plugins_folder = get_plugin_dir()

    for file_path in plugins_folder.glob("*.py"):
        print(file_path)
        if file_path.name == "__init__.py":
            continue

        module_name = file_path.stem

        try:
            spec = importlib.util.spec_from_file_location(module_name, str(file_path))
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            plugins.append(module)

            colors.colored(f"Loaded plugin: {module_name}", colors.OKGREEN)
        except:
            # Add red color
            colors.fail(f"Error loading plugin: {module_name}")

def main():
    colors.colored("Loading plugins...", colors.YELLOW)
    load_plugins()

    for plugin in plugins:
        name = getattr(plugin, "NAME", plugin.__name__)
        desc = getattr(plugin, "DESC", "No description provided.")

        if hasattr(plugin, "run"):
            plugins_menu.add_menu_option(item_name=f"{name} | {desc}", action=plugin.run)
        else:
            colors.fail(f"Plugin {name} does not have a run() function, skipping.")

    colors.colored("Plugins loaded!", colors.OKGREEN)

    main_menu.start()

if __name__ == "__main__":
    main()
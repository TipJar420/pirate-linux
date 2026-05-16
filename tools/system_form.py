#!/usr/bin/env python3
import yaml
import os
import sys

# Define the location of your main system profile configuration
SYSTEM_YAML_PATH = "/system.yaml"

# An absolute catalog of components you might want to easily check / uncheck
AVAILABLE_PACKAGES = ["micro", "chromium", "firefox", "git", "fastfetch", "nvidia-dkms", "linux-zen"]
AVAILABLE_AUR = ["visual-studio-code-bin", "spotify", "discord"]
AVAILABLE_SERVICES = ["caddy", "docker", "switcheroo-control", "bluetooth"]
AVAILABLE_TRACKS = ["blendos-base", "default-gnome", "gnome", "plasma", "xfce", "cosmic"]

def load_config():
    if not os.path.exists(SYSTEM_YAML_PATH):
        # Default fallback baseline if empty or fresh template setup
        return {
            "repo": "https://pkg-repo.blendos.co",
            "arch-repo": "https://geo.mirror.pkgbuild.com",
            "impl": "https://github.com/blend-os/tracks/raw/main",
            "track": "blendos-base",
            "packages": [],
            "aur-packages": [],
            "services": []
        }
    try:
        with open(SYSTEM_YAML_PATH, "r") as f:
            data = yaml.safe_load(f)
            return data if data else {}
    except Exception as e:
        print(f"\u001b[31mError loading configuration file: {e}\u001b[0m")
        sys.exit(1)

def interactive_checklist(title, target_list, available_items):
    while True:
        os.system("clear")
        print(f"\u001b[34m=== Toggle Checklist: {title} ===\u001b[0m")
        print("Use the numbers to toggle items on/off. Press 'd' when done.\n")
        
        # Display current status
        for idx, item in enumerate(available_items, 1):
            checked = " [X] " if item in target_list else " [ ] "
            color = "\u001b[32m" if item in target_list else "\u001b[0m"
            print(f"{idx}.{checked}{color}{item}\u001b[0m")
            
        choice = input("\nEnter number to toggle (or 'd' for done): ").strip().lower()
        if choice == 'd':
            break
        try:
            num = int(choice)
            if 1 <= num <= len(available_items):
                selected = available_items[num - 1]
                if selected in target_list:
                    target_list.remove(selected)
                else:
                    target_list.append(selected)
        except ValueError:
            pass

def choose_track(config):
    os.system("clear")
    print("\u001b[34m=== Choose Your Base Desktop Track ===\u001b[0m\n")
    for idx, track in enumerate(AVAILABLE_TRACKS, 1):
        active = " (Active)" if config.get("track") == track else ""
        print(f"{idx}. {track}{active}")
    
    choice = input("\nSelect track number (or press Enter to skip): ").strip()
    try:
        num = int(choice)
        if 1 <= num <= len(AVAILABLE_TRACKS):
            config["track"] = AVAILABLE_TRACKS[num - 1]
    except ValueError:
        pass

def save_config(config):
    try:
        # Sort internal array elements to keep the file highly legible
        config["packages"] = sorted(list(set(config.get("packages", []))))
        config["aur-packages"] = sorted(list(set(config.get("aur-packages", []))))
        config["services"] = sorted(list(set(config.get("services", []))))
        
        with open(SYSTEM_YAML_PATH, "w") as f:
            yaml.dump(config, f, default_flow_style=False, sort_keys=False)
        print("\n\u001b[32m✔ Host system.yaml written successfully!\u001b[0m")
        print("To apply changes run: \u001b[33msudo akshara update\u001b[0m")
    except PermissionError:
        print("\n\u001b[31mError: Writing to root files requires permissions. Run with 'sudo'.\u001b[0m")

def main():
    config = load_config()
    
    # Initialize list categories if missing entirely
    for key in ["packages", "aur-packages", "services"]:
        if key not in config or not isinstance(config[key], list):
            config[key] = []

    while True:
        os.system("clear")
        print("\u001b[35m⚡ blendOS System Declarative Form Modifier ⚡\u001b[0m")
        print("================================================")
        print(f"Current Track  :  \u001b[36m{config.get('track')}\u001b[0m")
        print(f"Host Packages  :  {len(config['packages'])} active items")
        print(f"AUR Packages   :  {len(config['aur-packages'])} active items")
        print(f"System Services:  {len(config['services'])} active items")
        print("================================================")
        print("1. Modify Base Desktop Track")
        print("2. Check / Uncheck Native Arch Packages")
        print("3. Check / Uncheck AUR Target Packages")
        print("4. Check / Uncheck System Core Services")
        print("5. Save Changes and Exit")
        print("6. Abandon Changes and Exit")
        
        main_choice = input("\nSelect an operation [1-6]: ").strip()
        
        if main_choice == "1":
            choose_track(config)
        elif main_choice == "2":
            interactive_checklist("Host Packages", config["packages"], AVAILABLE_PACKAGES)
        elif main_choice == "3":
            interactive_checklist("AUR Packages", config["aur-packages"], AVAILABLE_AUR)
        elif main_choice == "4":
            interactive_checklist("System Services", config["services"], AVAILABLE_SERVICES)
        elif main_choice == "5":
            save_config(config)
            break
        elif main_choice == "6":
            print("\nExiting. No modifications were written to disk.")
            break

if __name__ == "__main__":
    main()

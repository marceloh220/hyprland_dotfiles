#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess
from shutil import which
import sys
import argparse
from pathlib import Path


PACKAGE_GROUPS = [
    (
        "audio",
        ["pamixer", "pavucontrol", "pipewire-alsa", "pipewire-jack", "pipewire-pulse", "wireplumber"],
    ),
    (
        "compression",
        ["7zip", "unrar", "unzip"],
    ),
    (
        "display manager",
        ["plasma-login-manager"],
    ),
    (
        "firewall",
        ["ufw", "ufw-extras"],
    ),
    (
        "fonts",
        ["noto-fonts", "otf-fira-sans", "otf-font-awesome", "ttf-dejavu", "ttf-liberation", 
         "ttf-meslo-nerd"],
    ),
    (
        "hyprland",
        ["hyprland-git", "hypridle-git", "hyprlock-git", "hyprpaper-git", "hyprpicker-git"],
    ),
    (
        "hyprland-extras",
        ["blueman", "brightnessctl", "cliphist", "dunst", "grimblast-git", "power-profiles-daemon",
         "rofi", "waybar-git", "wlogout"],
    ),
    (
        "kde",
        ["ark", "dolphin", "dolphin-plugins", "kate", "kde-cli-tools", "kio-admin", "kompare"],
    ),
    (
        "multimedia",
        ["ffmpegthumbnailer", "gst-libav", "gst-plugins-bad", "gst-plugins-base", "gst-plugins-good",
         "gst-plugins-ugly", "mpc", "mpd", "mpv", "qview", "rmpc"],
    ),
    (
        "network",
        ["networkmanager", "network-manager-applet"],
    ),
    (
        "polkit agent",
        ["polkit-kde-agent", "hyprpolkitagent"],
    ),
    (
        "python",
        ["ipython", "python-matplotlib", "python-numpy", "python-pandas", "python-pillow", 
         "python-pyqt6", "python-scikit-learn", "python-scipy", "python-sympy"],
    ),
    (
        "terminal",
        ["imagemagick", "kitty", "kitty-shell-integration", "kitty-terminfo", "ueberzug"],
    ),
    (
        "terminal-extra",
        ["bat", "btop", "cava", "curl", "eza", "fastfetch", "fish", "fzf", "git",
         "nano", "neovim", "openssh", "ranger", "rsync", "thefuck", "trash-cli",
         "wget", "zoxide"],
    ),
    (
        "system",
        ["mission-center"],
    ),
    (
        "themes",
        ["bibata-cursor-theme", "nwg-look", "qt5-wayland", "qt5ct", "qt6-wayland", "qt6ct-kde"],
    ),
    (
        "web browser",
        ["falkon"],
    ),
    (
        "xdg",
        ["archlinux-xdg-menu", "xdg-desktop-portal-hyprland", "xdg-desktop-portal-kde", "xdg-user-dirs"],
    ),
]


def ask_confirmation(message: str) -> None:
    response = input(message).strip()
    if response not in {"Y", "y", "YES", "yes"}:
        print("Operation aborted by the user.")
        sys.exit(0)


def list_all_packages() -> list[str]:
    packages = []
    for _, pkg_group in PACKAGE_GROUPS:
        packages.extend(pkg_group)
    return packages


def print_packages_with_categories(group: str) -> None:
    print("Packages to be processed:")
    for category, pkg_group in PACKAGE_GROUPS:
        if group == "all" or category == group:
            print(f" - {' '.join(pkg_group)} ({category})")

def verify_distribution() -> None:
    base_supported = ("cachyos", "arch", "manjaro", "endeavouros", "arcolinux", "garuda", 
                      "archcraft")
    base = 'none'
    try:
        result = subprocess.run(["cat", "/etc/os-release"], text=True, capture_output=True)
        for line in result.stdout.splitlines():
            if line.startswith("ID="):
                base = line.split('=')[1].strip().strip('"')
                print(f"Base distribution detected: {base}")
                return
    except subprocess.CalledProcessError:
        print("Failed to determine the base distribution.")
        sys.exit(1)
    if base.lower() not in base_supported:
        print("Warning: Your system is not based on Arch, this script will not work.")
        sys.exit(1)
    


def ensure_yay_installed() -> None:
    if which("yay") is not None:
        print("yay is already installed.")
        return
    print("Trying to install yay from the official Arch repositories...")
    yay_in_repo = subprocess.run(["sudo", "pacman", "-Sy", "--noconfirm", "yay"], text=True)
    if yay_in_repo.returncode == 0:
        print("yay is installed.")
        return

    print("Failed to install yay from official repositories. Installing yay from AUR...")
    aur_dir = Path("yay")
    if aur_dir.exists():
        subprocess.run(["rm", "-rf", str(aur_dir)], check=True)

    subprocess.run(["git", "clone", "https://aur.archlinux.org/yay.git"], check=True)
    subprocess.run(["makepkg", "-si", "--noconfirm"], check=True, cwd=str(aur_dir))
    subprocess.run(["rm", "-rf", str(aur_dir)], check=True)
    print("yay installed successfully.")


def install_packages(group: str) -> None:
    
    verify_distribution()

    print(
        "Warning: Some packages may not be available in official Arch repos, "
        "so they may be installed from AUR using yay."
    )
    print("Make sure to review the package list and the installation process for any errors.")
    ask_confirmation("Type YES to continue if you understand the risks and want to proceed: ")

    if which("base-devel") is None:
        print("base-devel is not installed. Installing base-devel...")
        subprocess.run(["sudo", "pacman", "-Sy", "--noconfirm", "base-devel"], check=True)

    ensure_yay_installed()

    packages = list_all_packages()
    if group != "all":
        packages = []
        for category, pkg_group in PACKAGE_GROUPS:
            if category == group:
                packages.extend(pkg_group)
                break
        if not packages:
            print(f"No packages found for group '{group}'.")
            sys.exit(1)

    print_packages_with_categories(group=group)
    print("WARNING: Pay attention to the output for any errors during package installation.")
    ask_confirmation("Type YES to continue if you understand the risks and want to proceed: ")
    print("Installing packages...")
    print(f"Installing packages: {' '.join(packages)}")
    subprocess.run(["yay", "-S", *packages], check=True)


def install_cachy_repository() -> None:
    print("Adding CachyOS repository...")
    subprocess.run(["curl", "https://mirror.cachyos.org/cachyos-repo.tar.xz", "-o", "cachyos-repo.tar.xz"], check=True)
    subprocess.run(["tar", "xvf", "cachyos-repo.tar.xz"], check=True)
    subprocess.run(["sudo", "./install.sh"], check=True, cwd="cachyos-repo")


def remove_cachy_repository() -> None:
    print("Removing CachyOS repository...")
    subprocess.run(["sudo", "rm", "-rf", "/etc/pacman.d/cachyos-mirrorlist"], check=True)
    subprocess.run(["sudo", "rm", "-rf", "/etc/pacman.conf.d/cachyos.conf"], check=True)
    subprocess.run(["sudo", "rm", "-rf", "/etc/pacman.d/cachyos-repo-keyring"], check=True)


def remove_packages() -> None:
    print("Removing packages...")
    print("WARNING: This will remove a large number of packages, including some that may be essential for your system.")
    print("Make sure to review the package list and the removal process for any errors.")
    print_packages_with_categories()
    print(" - yay (AUR helper)")
    ask_confirmation("Type YES to continue if you understand the risks and want to proceed: ")
    packages = list_all_packages()
    print(f"Removing packages: {' '.join(packages)}")
    subprocess.run(["yay", "-Rdns", *packages], check=True)
    subprocess.run(["yay", "-Yc"], check=True)
    subprocess.run(["sudo", "pacman", "-Rns", "yay"], check=True)


def install_omf() -> None:
    print("Installing Oh My Fish...")
    subprocess.run(
        [
            "fish",
            "-c",
            "curl -L https://raw.githubusercontent.com/oh-my-fish/oh-my-fish/master/bin/install | fish",
        ],
        check=True,
    )


def remove_omf() -> None:
    print("Removing Oh My Fish...")
    subprocess.run(["omf", "uninstall"], check=True)


def _update_mpd_music_directory(mpd_conf_path: Path, music_path: str) -> None:
    if not mpd_conf_path.exists():
        return

    lines = mpd_conf_path.read_text(encoding="utf-8").splitlines()
    new_lines = []
    updated = False
    for line in lines:
        if line.strip().startswith("music_directory"):
            new_lines.append(f'music_directory    "{music_path}"')
            updated = True
        else:
            new_lines.append(line)

    if not updated:
        new_lines.append(f'music_directory    "{music_path}"')

    mpd_conf_path.write_text("\n".join(new_lines) + "\n", encoding="utf-8")


def copy_dotfiles(lua: bool) -> None:
    print("Copying dotfiles...")
    home_dir = Path.home()
    dotfiles_dir = Path("./config")
    if lua:
        dotfiles_dir = Path("./config_lua")
        print("""Using Hyprland Lua configuration files from './config_lua' directory.
              This is an experimental feature, and things may not work correctly.
              Make sure to review the configuration files and adjust them as needed before copying.""")
        confirmation = input("Type YES to continue if you understand the risks and want to proceed: ").strip()
        if confirmation not in {"Y", "y", "YES", "yes"}:
            print("Operation aborted by the user.")
            sys.exit(0)
    config_dir = home_dir / ".config"

    print("WARNING: This may overwrite your existing Hyprland configuration.")
    print("Old configuration files will be backed up if they exist, but make sure to back up important files.")
    ask_confirmation("Type YES to continue if you understand the risks and want to proceed: ")

    config_dir.mkdir(parents=True, exist_ok=True)
    backup_needed = False

    subprocess.run(["xdg-user-dirs-update"], check=True)

    for item in dotfiles_dir.iterdir():
        src = item
        dst = config_dir / item.name
        if dst.exists():
            backup_needed = True
            backup_dir = home_dir / ".config_backup"
            backup_dir.mkdir(parents=True, exist_ok=True)
            print("Moving old configuration to backup if it exists...")
            subprocess.run(["mv", "-f", str(dst), str(backup_dir)], check=False)

        if src.is_dir():
            print(f"Copying directory '{src}' to '{dst}'...")
            subprocess.run(["cp", "-rf", str(src), str(dst)], check=True)
        else:
            print(f"Copying file '{src}' to '{dst}'...")
            subprocess.run(["cp", "-f", str(src), str(dst)], check=True)

    user = os.getlogin()
    subprocess.run(["chown", "-R", f"{user}:{user}", str(config_dir)], check=True)

    hypr_scripts_dir = config_dir / "hypr" / "scripts"
    if hypr_scripts_dir.exists() and hypr_scripts_dir.is_dir():
        for script in hypr_scripts_dir.iterdir():
            if script.is_file():
                current_mode = script.stat().st_mode
                script.chmod(current_mode | 0o111)

    mpd_state_dir = home_dir / ".local" / "state" / "mpd"
    mpd_config_dir = config_dir / "mpd"
    if not mpd_state_dir.exists():
        mpd_state_dir.mkdir(parents=True, exist_ok=True)
        subprocess.run(["chown", "-R", f"{user}:{user}", str(mpd_state_dir)], check=True)
        subprocess.run(["touch", str(mpd_state_dir / "state")], check=True)
    if mpd_config_dir.exists() and mpd_config_dir.is_dir():
        subprocess.run(["chown", "-R", f"{user}:{user}", str(mpd_config_dir)], check=True)
        subprocess.run(["touch", str(mpd_config_dir / "database")], check=True)
        subprocess.run(["touch", str(mpd_config_dir / "sticker.sqlite")], check=True)
        subprocess.run(["mkdir", "-p", str(mpd_config_dir / "playlists")], check=True)

    music_path = subprocess.run(["xdg-user-dir", "MUSIC"], check=True, text=True, capture_output=True).stdout.strip()
    _update_mpd_music_directory(mpd_config_dir / "mpd.conf", music_path)

    pictures_path = subprocess.run(
        ["xdg-user-dir", "PICTURES"], check=True, text=True, capture_output=True
    ).stdout.strip()
    pictures_dir = Path(pictures_path)
    pictures_dir.mkdir(parents=True, exist_ok=True)

    print(f"Copying wallpapers to '{pictures_path}'...")
    subprocess.run(["cp", "-r", "./Pictures/wallpapers", str(pictures_dir)], check=True)
    print("Updating XDG user directories...")

    if backup_needed:
        print("Old configuration files were moved to a backup directory at '~/.config_backup'.")
        print("You can review the backup directory and restore any necessary files if needed.")


def restore_dotfiles() -> None:
    print("Restoring dotfiles from backup...")
    home_dir = Path.home()
    backup_dir = home_dir / ".config_backup"
    if not backup_dir.exists():
        print("No backup directory found. Cannot restore dotfiles.")
        sys.exit(1)

    for item in backup_dir.iterdir():
        src = item
        dst = home_dir / ".config" / item.name
        if src.is_dir():
            print(f"Restoring directory '{src}' to '{dst}'...")
            subprocess.run(["cp", "-rf", str(src), str(dst)], check=True)
        else:
            print(f"Restoring file '{src}' to '{dst}'...")
            subprocess.run(["cp", "-f", str(src), str(dst)], check=True)

    user = os.getlogin()
    subprocess.run(["chown", "-R", f"{user}:{user}", str(home_dir / ".config")], check=True)
    subprocess.run(["xdg-user-dirs-update"], check=True)
    print("Dotfiles restored from backup successfully.")


def sddm_theme_config() -> None:
    print("Configuring SDDM theme...")
    sddm_conf_path = Path("/etc/sddm.conf")
    if not sddm_conf_path.exists():
        print("SDDM configuration file not found. Skipping SDDM theme configuration.")
        return

    lines = sddm_conf_path.read_text(encoding="utf-8").splitlines()
    new_lines = []
    in_theme_section = False
    theme_set = False

    for line in lines:
        stripped_line = line.strip()
        if stripped_line.startswith("[Theme]"):
            in_theme_section = True
            new_lines.append(line)
            continue

        if in_theme_section:
            if stripped_line.startswith("Current="):
                new_lines.append("Current=sugar-candy")
                theme_set = True
            elif stripped_line.startswith("[") and not stripped_line.startswith("[Theme]"):
                in_theme_section = False
                new_lines.append(line)
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)

    if not theme_set:
        new_lines.append("[Theme]")
        new_lines.append("Current=sugar-candy")

    sddm_conf_path.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
    print("SDDM theme configured successfully.")


def connect_to_wifi(ssid: str, password: str) -> None:
    print(f"Connecting to Wi-Fi network '{ssid}'...")
    devices = subprocess.run(["iwctl", "device", "list"], check=True, text=True, capture_output=True)
    device = None
    for line in devices.stdout.splitlines():
        if "wlan" in line:
            device = line.split()[0]
            break
    if device is None:
        print("No wireless device found.")
        sys.exit(1)
    subprocess.run(["iwctl", "device", device, "set-property", "Powered", "on"], check=True)
    subprocess.run(["iwctl", "station", device, "connect", ssid, "password", password], check=True)

if __name__ == "__main__":
    username = os.getlogin()
    if username == "root":
        print("This script should not be run as root. Please run it as a regular user with sudo privileges.")
        sys.exit(1)
    parser = argparse.ArgumentParser(description="Install Hyprland and related packages on Arch Linux.")
    parser.add_argument("--add-wheel", action="store_true", help="Add the user to the wheel group for sudo access")
    parser.add_argument("--install-repository", action="store_true", help="Install the CachyOS repository")
    parser.add_argument("--install-packages", action="store_true", help="Install the list of packages")
    parser.add_argument("--install-packages-group", type=str, default="all", help="Install a specific group of packages (e.g., 'audio', 'hyprland', 'kde', etc.)")
    parser.add_argument("--install-omf", action="store_true", help="Install Oh My Fish")
    parser.add_argument("--copy-dotfiles", action="store_true", help="Copy dotfiles to the user's home directory")
    parser.add_argument("--copy-dotfiles-lua", action="store_true", help="Copy dotfiles using the new lua configs to the user's home directory (Experimental)")
    parser.add_argument("--sddm-theme-config", action="store_true", help="Configure SDDM theme to sugar-candy")
    parser.add_argument("--remove-repository", action="store_true", help="Remove the CachyOS repository")
    parser.add_argument("--remove-packages", action="store_true", help="Remove the list of packages")
    parser.add_argument("--remove-omf", action="store_true", help="Remove Oh My Fish")
    parser.add_argument("--restore-dotfiles", action="store_true", help="Restore dotfiles from backup")
    parser.add_argument("--connect-wifi", action="store_true", help="Connect to a Wi-Fi network")
    parser.add_argument("--wifi-ssid", help="SSID of the Wi-Fi network to connect to")
    parser.add_argument("--wifi-password", help="Password for the Wi-Fi network")
    args = parser.parse_args()

    if args.connect_wifi:
        if not args.wifi_ssid or not args.wifi_password:
            print("To use --connect-wifi you must provide --wifi-ssid and --wifi-password.")
            sys.exit(1)
        connect_to_wifi(args.wifi_ssid, args.wifi_password)
    elif args.add_wheel:
        print(f"Adding user '{username}' to the wheel group for sudo access...")
        subprocess.run(["su"])
        subprocess.run(["usermod", "-aG", "wheel", username], check=True)
        subprocess.run(["echo", "%wheel ALL=(ALL) ALL", ">>", "/etc/sudoers"], check=True)
        subprocess.run(["exit"])
        print(f"User '{username}' added to the wheel group successfully.")
    elif args.install_repository:
        install_cachy_repository()
    elif args.install_packages:
        install_packages(args.install_packages_group)
    elif args.copy_dotfiles:
        copy_dotfiles(lua=False)
    elif args.copy_dotfiles_lua:
        copy_dotfiles(lua=True)
    elif args.sddm_theme_config:
        sddm_theme_config()
    elif args.install_omf:
        install_omf()
    elif args.remove_repository:
        remove_cachy_repository()
    elif args.remove_packages:
        remove_packages()
    elif args.remove_omf:
        remove_omf()
    elif args.restore_dotfiles:
        restore_dotfiles()
    else:
        print("No valid arguments provided. Use --help for more information.")
        sys.exit(1)

    sys.exit(0)

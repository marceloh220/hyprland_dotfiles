#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess
import sys
import argparse
from pathlib import Path


PACKAGE_GROUPS = [
    (
        "network",
        ["networkmanager"],
    ),
    (
        "display manager",
        ["sddm"],
    ),
    (
        "audio",
        ["pamixer", "pavucontrol", "pipewire-alsa", "pipewire-jack", "pipewire-pulse", "wireplumber"],
    ),
    (
        "kde",
        ["ark", "dolphin", "dolphin-plugins", "kate", "kompare", "kde-cli-tools", "kio-admin"],
    ),
    (
        "web browser",
        ["falkon"],
    ),
    (
        "multimedia",
        [
            "ffmpegthumbnailer",
            "qview",
            "mpc",
            "mpd",
            "mpv",
            "rmpc",
            "gst-libav",
            "gst-plugins-base",
            "gst-plugins-bad",
            "gst-plugins-good",
            "gst-plugins-ugly",
        ],
    ),
    (
        "hyprland",
        ["hyprland", "hyprcursor", "hypridle", "hyprlock", "hyprpaper", "hyprpicker"],
    ),
    (
        "hyprland-extras",
        [
            "waybar",
            "wlogout",
            "rofi",
            "blueman",
            "brightnessctl",
            "cliphist",
            "dunst",
            "grimblast-git",
            "power-profiles-daemon",
        ],
    ),
    (
        "terminal",
        ["kitty", "kitty-shell-integration", "kitty-terminfo", "imagemagick", "ueberzug"],
    ),
    (
        "terminal-extra",
        [
            "ranger",
            "nano",
            "neovim",
            "bat",
            "btop",
            "cava",
            "rsync",
            "git",
            "wget",
            "curl",
            "thefuck",
            "trash-cli",
            "eza",
            "fastfetch",
            "fish",
            "fzf",
            "openssh",
            "zoxide",
        ],
    ),
    (
        "polkit agent",
        ["polkit-kde-agent", "hyprpolkitagent"],
    ),
    (
        "python",
        [
            "ipython",
            "python-matplotlib",
            "python-numpy",
            "python-pandas",
            "python-pillow",
            "python-pyqt6",
            "python-scikit-learn",
            "python-sympy",
            "python-scipy",
        ],
    ),
    (
        "themes",
        ["nwg-look", "bibata-cursor-theme", "qt5-wayland", "qt5ct", "qt6-wayland", "qt6ct-kde"],
    ),
    (
        "fonts",
        ["noto-fonts", "ttf-dejavu", "ttf-liberation", "ttf-meslo-nerd", "otf-fira-sans", "otf-font-awesome"],
    ),
    (
        "firewall",
        ["ufw", "ufw-extras"],
    ),
    (
        "compression",
        ["unrar", "unzip", "7zip"],
    ),
    (
        "xdg",
        ["xdg-desktop-portal-kde", "xdg-desktop-portal-hyprland", "xdg-user-dirs", "archlinux-xdg-menu"],
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


def print_packages_with_categories() -> None:
    print("Packages to be processed:")
    for category, pkg_group in PACKAGE_GROUPS:
        print(f" - {' '.join(pkg_group)} ({category})")


def ensure_yay_installed() -> None:
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


def install_packages() -> None:
    print(
        "Warning: Some packages may not be available in official Arch repos, "
        "so they may be installed from AUR using yay."
    )
    print("Make sure to review the package list and the installation process for any errors.")
    ask_confirmation("Type YES to continue if you understand the risks and want to proceed: ")

    ensure_yay_installed()

    print_packages_with_categories()
    print("WARNING: Pay attention to the output for any errors during package installation.")
    ask_confirmation("Type YES to continue if you understand the risks and want to proceed: ")

    packages = list_all_packages()
    print("Installing packages...")
    subprocess.run(["yay", "-S", *packages], check=True)


def intall_packages() -> None:
    # Backward-compatible alias for the original misspelled function name.
    install_packages()


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


def copy_dotfiles() -> None:
    print("Copying dotfiles...")
    home_dir = Path.home()
    dotfiles_dir = Path("./config")
    config_dir = home_dir / ".config"

    print("WARNING: This may overwrite your existing Hyprland configuration.")
    print("Old configuration files will be backed up if they exist, but make sure to back up important files.")
    ask_confirmation("Type YES to continue if you understand the risks and want to proceed: ")

    config_dir.mkdir(parents=True, exist_ok=True)
    backup_needed = False

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

    subprocess.run(["xdg-user-dirs-update"], check=True)

    mpd_state_dir = home_dir / ".local" / "state" / "mpd"
    if not mpd_state_dir.exists():
        mpd_state_dir.mkdir(parents=True, exist_ok=True)
        subprocess.run(["chown", "-R", f"{user}:{user}", str(mpd_state_dir)], check=True)
        subprocess.run(["touch", str(mpd_state_dir / "state")], check=True)

    music_path = subprocess.run(["xdg-user-dir", "MUSIC"], check=True, text=True, capture_output=True).stdout.strip()
    _update_mpd_music_directory(config_dir / "mpd" / "mpd.conf", music_path)

    subprocess.run(["systemctl", "enable", "--now", "--user", "mpd"], check=True)
    pictures_path = subprocess.run(
        ["xdg-user-dir", "PICTURES"], check=True, text=True, capture_output=True
    ).stdout.strip()
    pictures_dir = Path(pictures_path)
    pictures_dir.mkdir(parents=True, exist_ok=True)

    print(f"Copying wallpapers to '{pictures_path}'...")
    subprocess.run(["cp", "-r", ".Pictures/wallpapers", str(pictures_dir)], check=True)
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
    parser = argparse.ArgumentParser(description="Install Hyprland and related packages on Arch Linux.")
    parser.add_argument("--install-repository", action="store_true", help="Install the CachyOS repository")
    parser.add_argument("--install-packages", action="store_true", help="Install the list of packages")
    parser.add_argument("--install-omf", action="store_true", help="Install Oh My Fish")
    parser.add_argument("--copy-dotfiles", action="store_true", help="Copy dotfiles to the user's home directory")
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

    elif args.install_repository:
        install_cachy_repository()
    elif args.install_packages:
        install_packages()
    elif args.copy_dotfiles:
        copy_dotfiles()
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

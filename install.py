#!/usr/bin/env python


import __main__
import os
import subprocess
import sys
import argparse

def intall_packages():
    print("Warning: Some PKGS are not avaliable in official Arch repos, so they will be installed from AUR using yay.")
    print("Make sure to review the PKGS list and the installation process for any errors.")
    print("Type YES (Y/y) to continue if you understand the risks and want to proceed with the installation:")
    response = input("Type YES to continue: ")
    if response != "Y" and response != "y" and response != "YES" and response != "yes":
        print("Installation aborted by the user.")
        sys.exit(0)
    pkg_list = "archlinux-xdg-menu ark bat bibata-cursor-theme blueman brightnessctl btop cava clang cliphist coolercontrol " +\
               "dolphin dolphin-plugins dunst eza fastfetch ffmpegthumbnailer falkon fish fzf git grimblast " +\
               "gst-libav gst-plugins-bad gst-plugins-base gst-plugins-good gst-plugins-ugly " +\
               "hyprcursor hypridle hyprland hyprlock hyprpaper hyprpicker " +\
                "imagemagick ipython jq kate kde-cli-tools kio-admin kitty kitty-shell-integration kitty-terminfo kompare " +\
                "linux linux-firmware sddm mpc mpd mpv nano neovim networkmanager noto-fonts npm nwg-look " +\
                "openssh otf-fira-sans pamixer pavucontrol pipewire-alsa pipewire-jack pipewire-pulse " +\
                "polkit-kde-agent power-profiles-daemon python-matplotlib python-numpy python-pandas python-pillow python-pyqt6 python-scikit-learn python-sympy " +\
                "qt5-wayland qt5ct qt6-wayland qt6ct-kde qview ranger rmpc-git rofi-wayland " +\
                "rsync thefuck tk trash-cli ttf-dejavu ttf-font-awesome otf-font-awesome ttf-liberation ttf-meslo-nerd " +\
                "ueberzug ufw ufw-extras unrar unzip waybar wget wireplumber wlogout " +\
                "xdg-desktop-portal-gtk xdg-desktop-portal-hyprland xdg-user-dirs-gtk zoxide "
    print(f"Trying to install yay from the official Arch repositories...")
    yay_in_repo = subprocess.run(["sudo", "pacman", "-S", "--noconfirm", "yay"], text=True)
    if yay_in_repo.returncode != 0:
        print("Failed to install yay. Installing yay from AUR...")
        subprocess.run(["git", "clone", "https://aur.archlinux.org/yay.git"], check=True)
        os.chdir("yay")
        subprocess.run(["makepkg", "-si", "--noconfirm"], check=True)
        os.chdir("..")
        print("yay installed successfully. Cleaning up...")
        subprocess.run(["rm", "-rf", "yay"], check=True)
    print("yay is installed. Installing packages from the list...")
    print(" Pay attention to the output for any errors during package installation.")
    subprocess.run(["sleep", "5"], check=True)
    print(f"Installing packages...")
    subprocess.run(["yay", "-S"] + pkg_list.split(), check=True)

def install_cachy_repository():
    print("Adding CachyOS repository...")
    subprocess.run(["curl", "https://mirror.cachyos.org/cachyos-repo.tar.xz", "-o", "cachyos-repo.tar.xz"], check=True)
    subprocess.run(["tar", "xvf", "cachyos-repo.tar.xz", "&&", "cd", "cachyos-repo"], check=True)
    subprocess.run(["sudo", "./install.sh"], check=True)

def remove_cachy_repository():
    print("Removing CachyOS repository...")
    subprocess.run(["sudo", "rm", "-rf", "/etc/pacman.d/cachyos-mirrorlist"], check=True)
    subprocess.run(["sudo", "rm", "-rf", "/etc/pacman.conf.d/cachyos.conf"], check=True)
    subprocess.run(["sudo", "rm", "-rf", "/etc/pacman.d/cachyos-repo-keyring"], check=True)

def remove_packages():
    print("Removing packages...")
    pkg_list = "archlinux-xdg-menu ark bat bibata-cursor-theme blueman brightnessctl btop cava clang cliphist coolercontrol " +\
               "dolphin dolphin-plugins dunst eza fastfetch ffmpegthumbnailer falkon fish fzf git grimblast " +\
               "gst-libav gst-plugins-bad gst-plugins-base gst-plugins-good gst-plugins-ugly " +\
               "hyprcursor hypridle hyprland hyprlock hyprpaper hyprpicker " +\
                "imagemagick ipython jq kate kde-cli-tools kio-admin kitty kitty-shell-integration kitty-terminfo kompare " +\
                "linux linux-firmware sddm mpc mpd mpv nano neovim networkmanager noto-fonts npm nwg-look " +\
                "openssh otf-fira-sans pamixer pavucontrol pipewire-alsa pipewire-jack pipewire-pulse " +\
                "polkit-kde-agent power-profiles-daemon python-matplotlib python-numpy python-pandas python-pillow python-pyqt6 python-scikit-learn python-sympy " +\
                "qt5-wayland qt5ct qt6-wayland qt6ct-kde qview ranger rmpc-git rofi-wayland " +\
                "rsync thefuck tk trash-cli ttf-dejavu ttf-font-awesome otf-font-awesome ttf-liberation ttf-meslo-nerd " +\
                "ueberzug ufw ufw-extras unrar unzip waybar wget wireplumber wlogout " +\
                "xdg-desktop-portal-gtk xdg-desktop-portal-hyprland xdg-user-dirs-gtk zoxide "
    subprocess.run(["yay", "-Rns"] + pkg_list.split(), check=True)

def install_omf():
    print("Installing Oh My Fish...")
    subprocess.run(["curl", "-L", "https://get.oh-my.fish", "|", "fish"], check=True)

def remove_omf():
    print("Removing Oh My Fish...")
    subprocess.run(["omf", "uninstall"], check=True)

def copy_dotfiles():
    print("Copying dotfiles...")
    home_dir = os.path.expanduser("~")
    dotfiles_dir = f"./config"
    print("warning: This will overwrite your existing Hyprland configuration if it exists. Make sure to back up any important files before proceeding.")
    print("Type YES (Y/y) to continue if you understand the risks and want to proceed with copying the dotfiles:")
    response = input("Type YES to continue: ")
    if response != "Y" and response != "y" and response != "YES" and response != "yes":
        print("Copying dotfiles aborted by the user.")
        sys.exit(0)
    backup_needed = False
    for item in os.listdir(dotfiles_dir):
        src = os.path.join(dotfiles_dir, item)
        dst = os.path.join(home_dir, f"config/{item}")
        if os.path.exists(dst):
            backup_needed = True
            if not os.path.isdir(f"{home_dir}/.config_backup"):
                 os.makedirs(f"{home_dir}/.config_backup")
            print("Moving old configuration to backup if it exists...")
            subprocess.run(["mv", "-f", dst, f"{home_dir}/.config_backup"], check=False)
        if os.path.isdir(src):
            print(f"Copying directory '{src}' to '{dst}'...")
            subprocess.run(["cp", "-rf", src, dst], check=True)
        else:
            print(f"Copying file '{src}' to '{dst}'...")
            subprocess.run(["cp", "-f", src, dst], check=True)
    subprocess.run(["chown", "-R", f"{os.getlogin()}:{os.getlogin()}", os.path.join(home_dir, ".config")], check=True)
    subprocess.run(["xdg-user-dirs-update"], check=True)
    if backup_needed:
        print("Old configuration files were moved to a backup directory at '~/.config_backup'.")
        print("You can review the backup directory and restore any necessary files if needed.")

def restore_dotfiles():
    print("Restoring dotfiles from backup...")
    home_dir = os.path.expanduser("~")
    backup_dir = os.path.join(home_dir, ".config_backup")
    if not os.path.exists(backup_dir):
        print("No backup directory found. Cannot restore dotfiles.")
        sys.exit(1)
    for item in os.listdir(backup_dir):
        src = os.path.join(backup_dir, item)
        dst = os.path.join(home_dir, f".config/{item}")
        if os.path.isdir(src):
            print(f"Restoring directory '{src}' to '{dst}'...")
            subprocess.run(["cp", "-rf", src, dst], check=True)
        else:
            print(f"Restoring file '{src}' to '{dst}'...")
            subprocess.run(["cp", "-f", src, dst], check=True)
    subprocess.run(["chown", "-R", f"{os.getlogin()}:{os.getlogin()}", os.path.join(home_dir, ".config")], check=True)
    subprocess.run(["xdg-user-dirs-update"], check=True)
    print("Dotfiles restored from backup successfully.")

def connect_to_wifi(ssid, password):
    print(f"Connecting to Wi-Fi network '{ssid}'...")
    devices = subprocess.run(["iwd", "device", "list"], check=True, text=True)
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

    if args.wifi_ssid and args.wifi_password:
        connect_to_wifi(args.wifi_ssid, args.wifi_password)

    elif args.install_repository:
        install_cachy_repository()
    elif args.install_packages:
        intall_packages()
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

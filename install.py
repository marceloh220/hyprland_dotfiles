#!/usb/bin/env python3


import __main__
import os
import subprocess
import sys
import argparse

def intall_packages():
    pkg_list = "archlinux-xdg-menu ark bat bibata-cursor-theme blueman brightnessctl btop cava clang cliphist coolercontrol" +\
               "dolphin dolphin-plugins dunst eza fastfetch ffmpegthumbnailer falkon fish fzf git grimblast" +\
               "gst-libav gst-plugins-bad gst-plugins-base gst-plugins-good gst-plugins-ugly" +\
               "hyprcursor hypridle hyprland hyprlock hyprpaper hyprpicker" +\
                "imagemagick ipython jq kate kde-cli-tools kio-admin kitty kitty-shell-integration kitty-terminfo kompare" +\
                "linux linux-firmware sddm mpc mpd mpv nano neovim networkmanager noto-fonts npm nwg-look" +\
                "openssh otf-fira-sans pamixer pavucontrol pipewire-alsa pipewire-jack pipewire-pulse" +\
                "polkit-kde-agent power-profiles-daemon python-matplotlib python-numpy python-pandas python-pillow python-pyqt6 python-scikit-learn python-sympy" +\
                "qt5-wayland qt5ct qt6-wayland qt6ct-kde qview ranger rmpc-git rofi-wayland" +\
                "rsync thefuck tk trash-cli ttf-dejavu ttf-font-awesome ttf-liberation ttf-meslo-nerd" +\
                "ueberzug ufw ufw-extras unrar unzip waybar wget wireplumber wlogout" +\
                "xdg-desktop-portal-gtk xdg-desktop-portal-hyprland xdg-user-dirs-gtk yay zoxide"
    print(f"Installing packages...")
    subprocess.run(["sudo", "pacman", "-S", "--noconfirm"] + pkg_list.split(), check=True)

def install_cachy_repository():
    print("Adding CachyOS repository...")
    subprocess.run(["curl", "https://mirror.cachyos.org/cachyos-repo.tar.xz", "-o", "cachyos-repo.tar.xz"], check=True)
    subprocess.run(["tar", "xvf", "cachyos-repo.tar.xz", "&&", "cd", "cachyos-repo"], check=True)
    subprocess.run(["sudo", "./install.sh"], check=True)

def copy_dotfiles():
    print("Copying dotfiles...")
    home_dir = os.path.expanduser("~")
    dotfiles_dir = os.path.join(os.path.dirname(__main__.__file__), "config")
    for item in os.listdir(dotfiles_dir):
        src = os.path.join(dotfiles_dir, item)
        dst = os.path.join(home_dir, f".config/{item}")
        if os.path.isdir(src):
            subprocess.run(["cp", "-r", src, dst], check=True)
        else:
            subprocess.run(["cp", src, dst], check=True)

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
    parser.add_argument("-r", "--install-repository", action="store_true", help="Install the CachyOS repository")
    parser.add_argument("-i", "--install-packages", action="store_true", help="Install the list of packages")
    parser.add_argument("-d", "--copy-dotfiles", action="store_true", help="Copy dotfiles to the user's home directory")
    parser.add_argument("-c", "--connect-wifi", action="store_true", help="Connect to a Wi-Fi network")
    parser.add_argument("--wifi-ssid", help="SSID of the Wi-Fi network to connect to")
    parser.add_argument("--wifi-password", help="Password for the Wi-Fi network")
    args = parser.parse_args()

    if args.wifi_ssid and args.wifi_password:
        connect_to_wifi(args.wifi_ssid, args.wifi_password)

    if args.install_repository:
        install_cachy_repository()
    if args.install_packages:
        intall_packages()
    if args.copy_dotfiles:
        copy_dotfiles()
        
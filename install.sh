#!/usr/bin/env bash

set -euo pipefail

# Package groups mirrored from install.py
CATEGORIES=(
  "audio"
  "base"
  "compression"
  "display manager"
  "firewall"
  "fonts"
  "hyprland"
  "hyprland-extras"
  "kde"
  "multimedia"
  "network"
  "polkit agent"
  "python"
  "terminal"
  "terminal-extra"
  "system"
  "themes"
  "web browser"
  "xdg"
)

declare -A GROUP_PACKAGES=(
  ["audio"]="pamixer pavucontrol pipewire-alsa pipewire-jack pipewire-pulse wireplumber"
  ["base"]="base-devel git nano sudo"
  ["compression"]="7zip unrar unzip"
  ["display manager"]="plasma-login-manager"
  ["firewall"]="ufw ufw-extras"
  ["fonts"]="noto-fonts otf-fira-sans otf-font-awesome ttf-dejavu ttf-liberation ttf-meslo-nerd"
  ["hyprland"]="hyprland hypridle hyprlock hyprpaper hyprpicker"
  ["hyprland-extras"]="blueman brightnessctl cliphist dunst grimblast-git power-profiles-daemon rofi waybar-git wlogout"
  ["kde"]="ark dolphin dolphin-plugins kate kde-cli-tools kio-admin kompare"
  ["multimedia"]="ffmpegthumbnailer gst-libav gst-plugins-bad gst-plugins-base gst-plugins-good gst-plugins-ugly mpc mpd mpv qview rmpc"
  ["network"]="networkmanager iwd nmtui wireless-regdb"
  ["polkit agent"]="polkit-kde-agent hyprpolkitagent"
  ["python"]="ipython python-matplotlib python-numpy python-pandas python-pillow python-pyqt6 python-scikit-learn python-scipy python-sympy"
  ["terminal"]="imagemagick kitty kitty-shell-integration kitty-terminfo ueberzug"
  ["terminal-extra"]="bat btop cava curl eza fastfetch fish fzf git neovim openssh ranger rsync thefuck trash-cli wget zoxide"
  ["system"]="mission-center"
  ["themes"]="bibata-cursor-theme nwg-look qt5-wayland qt5ct qt6-wayland qt6ct-kde"
  ["web browser"]="falkon"
  ["xdg"]="archlinux-xdg-menu xdg-desktop-portal-hyprland xdg-desktop-portal-kde xdg-user-dirs"
)

ask_confirmation() {
  local message="$1"
  read -r -p "$message" response
  case "$response" in
    Y|y|YES|yes) ;;
    *)
      echo "Operation aborted by the user."
      exit 0
      ;;
  esac
}

list_all_packages() {
  local all=()
  local category
  for category in "${CATEGORIES[@]}"; do
    # shellcheck disable=SC2206
    local group=( ${GROUP_PACKAGES["$category"]} )
    all+=("${group[@]}")
  done
  printf '%s\n' "${all[@]}"
}

print_packages_with_categories() {
  local group="${1:-all}"
  local category
  echo "Packages to be processed:"
  for category in "${CATEGORIES[@]}"; do
    if [[ "$group" == "all" || "$category" == "$group" ]]; then
      echo " - ${GROUP_PACKAGES["$category"]} ($category)"
    fi
  done
}

list_packages_groups() {
  local category
  echo "Available package groups:"
  for category in "${CATEGORIES[@]}"; do
    echo " - $category"
  done
}

verify_distribution() {
  local base_supported="cachyos arch manjaro endeavouros arcolinux garuda archcraft"
  local base="none"

  if [[ -f /etc/os-release ]]; then
    # shellcheck disable=SC1091
    source /etc/os-release
    base="${ID:-none}"
    echo "Base distribution detected: $base"
  else
    echo "Failed to determine the base distribution."
    exit 1
  fi

  if ! grep -qw "${base,,}" <<< "$base_supported"; then
    echo "Warning: Your system is not based on Arch, this script will not work."
    exit 1
  fi
}

ensure_yay_installed() {
  if command -v yay >/dev/null 2>&1; then
    echo "yay is already installed."
    return
  fi

  echo "Trying to install yay from the official Arch repositories..."
  if sudo pacman -Sy --noconfirm yay; then
    echo "yay is installed."
    return
  fi

  echo "Failed to install yay from official repositories. Installing yay from AUR..."
  rm -rf yay
  git clone https://aur.archlinux.org/yay.git
  (
    cd yay
    makepkg -si --noconfirm
  )
  rm -rf yay
  echo "yay installed successfully."
}

install_packages() {
  local group="$1"
  local packages=()

  verify_distribution

  echo "Warning: Some packages may not be available in official Arch repos, so they may be installed from AUR using yay."
  echo "Make sure to review the package list and the installation process for any errors."
  ask_confirmation "Type YES to continue if you understand the risks and want to proceed: "

  if ! pacman -Qi base-devel >/dev/null 2>&1; then
    echo "base-devel is not installed. Installing base-devel..."
    sudo pacman -Sy --noconfirm base-devel
  fi

  ensure_yay_installed

  if [[ "$group" == "all" ]]; then
    mapfile -t packages < <(list_all_packages)
  else
    if [[ -z "${GROUP_PACKAGES["$group"]+x}" ]]; then
      echo "No packages found for group '$group'."
      exit 1
    fi
    # shellcheck disable=SC2206
    packages=( ${GROUP_PACKAGES["$group"]} )
  fi

  print_packages_with_categories "$group"
  echo "WARNING: Pay attention to the output for any errors during package installation."
  ask_confirmation "Type YES to continue if you understand the risks and want to proceed: "
  echo "Installing packages..."
  echo "Installing packages: ${packages[*]}"
  yay -S "${packages[@]}"
}

install_cachy_repository() {
  echo "Adding CachyOS repository..."
  curl https://mirror.cachyos.org/cachyos-repo.tar.xz -o cachyos-repo.tar.xz
  tar xvf cachyos-repo.tar.xz
  (
    cd cachyos-repo
    sudo ./install.sh
  )
}

remove_cachy_repository() {
  echo "Removing CachyOS repository..."
  sudo rm -rf /etc/pacman.d/cachyos-mirrorlist
  sudo rm -rf /etc/pacman.conf.d/cachyos.conf
  sudo rm -rf /etc/pacman.d/cachyos-repo-keyring
}

remove_packages() {
  local packages=()

  echo "Removing packages..."
  echo "WARNING: This will remove a large number of packages, including some that may be essential for your system."
  echo "Make sure to review the package list and the removal process for any errors."
  print_packages_with_categories "all"
  echo " - yay (AUR helper)"
  ask_confirmation "Type YES to continue if you understand the risks and want to proceed: "

  mapfile -t packages < <(list_all_packages)
  echo "Removing packages: ${packages[*]}"
  yay -Rdns "${packages[@]}"
  yay -Yc
  sudo pacman -Rns yay
}

install_omf() {
  echo "Installing Oh My Fish..."
  fish -c "curl -L https://raw.githubusercontent.com/oh-my-fish/oh-my-fish/master/bin/install | fish"
}

remove_omf() {
  echo "Removing Oh My Fish..."
  omf uninstall
}

update_mpd_music_directory() {
  local mpd_conf_path="$1"
  local music_path="$2"

  [[ -f "$mpd_conf_path" ]] || return 0

  if grep -qE '^[[:space:]]*music_directory' "$mpd_conf_path"; then
    sed -E -i "s|^[[:space:]]*music_directory.*$|music_directory    \"$music_path\"|" "$mpd_conf_path"
  else
    printf 'music_directory    "%s"\n' "$music_path" >> "$mpd_conf_path"
  fi
}

copy_dotfiles() {
  local lua="$1"
  local home_dir config_dir dotfiles_dir backup_needed user_name

  home_dir="$HOME"
  config_dir="$home_dir/.config"
  dotfiles_dir="./config"
  backup_needed=0
  user_name="$(id -un)"

  echo "Copying dotfiles..."

  if [[ "$lua" == "true" ]]; then
    dotfiles_dir="./config_lua"
    echo "Using Hyprland Lua configuration files from './config_lua' directory."
    echo "This is an experimental feature, and things may not work correctly."
    echo "Make sure to review the configuration files and adjust them as needed before copying."
    ask_confirmation "Type YES to continue if you understand the risks and want to proceed: "
  fi

  echo "WARNING: This may overwrite your existing Hyprland configuration."
  echo "Old configuration files will be backed up if they exist, but make sure to back up important files."
  ask_confirmation "Type YES to continue if you understand the risks and want to proceed: "

  mkdir -p "$config_dir"
  xdg-user-dirs-update

  shopt -s dotglob nullglob
  local item
  for item in "$dotfiles_dir"/*; do
    local name src dst backup_dir
    src="$item"
    name="$(basename "$item")"
    dst="$config_dir/$name"

    if [[ -e "$dst" ]]; then
      backup_needed=1
      backup_dir="$home_dir/.config_backup"
      mkdir -p "$backup_dir"
      echo "Moving old configuration to backup if it exists..."
      mv -f "$dst" "$backup_dir" || true
    fi

    if [[ -d "$src" ]]; then
      echo "Copying directory '$src' to '$dst'..."
      cp -rf "$src" "$dst"
    else
      echo "Copying file '$src' to '$dst'..."
      cp -f "$src" "$dst"
    fi
  done
  shopt -u dotglob nullglob

  chown -R "$user_name:$user_name" "$config_dir"

  local hypr_scripts_dir
  hypr_scripts_dir="$config_dir/hypr/scripts"
  if [[ -d "$hypr_scripts_dir" ]]; then
    local script
    for script in "$hypr_scripts_dir"/*; do
      [[ -f "$script" ]] && chmod +x "$script"
    done
  fi

  local mpd_state_dir mpd_config_dir
  mpd_state_dir="$home_dir/.local/state/mpd"
  mpd_config_dir="$config_dir/mpd"

  if [[ ! -d "$mpd_state_dir" ]]; then
    mkdir -p "$mpd_state_dir"
    chown -R "$user_name:$user_name" "$mpd_state_dir"
    touch "$mpd_state_dir/state"
  fi

  if [[ -d "$mpd_config_dir" ]]; then
    chown -R "$user_name:$user_name" "$mpd_config_dir"
    touch "$mpd_config_dir/database"
    touch "$mpd_config_dir/sticker.sqlite"
    mkdir -p "$mpd_config_dir/playlists"
  fi

  local music_path
  music_path="$(xdg-user-dir MUSIC | tr -d '\n')"
  update_mpd_music_directory "$mpd_config_dir/mpd.conf" "$music_path"

  local pictures_path pictures_dir
  pictures_path="$(xdg-user-dir PICTURES | tr -d '\n')"
  pictures_dir="$pictures_path"
  mkdir -p "$pictures_dir"

  echo "Copying wallpapers to '$pictures_path'..."
  cp -r ./Pictures/wallpapers "$pictures_dir"
  echo "Updating XDG user directories..."

  if [[ "$backup_needed" -eq 1 ]]; then
    echo "Old configuration files were moved to a backup directory at '~/.config_backup'."
    echo "You can review the backup directory and restore any necessary files if needed."
  fi
}

restore_dotfiles() {
  local home_dir backup_dir src dst user_name

  echo "Restoring dotfiles from backup..."
  home_dir="$HOME"
  backup_dir="$home_dir/.config_backup"
  user_name="$(id -un)"

  if [[ ! -d "$backup_dir" ]]; then
    echo "No backup directory found. Cannot restore dotfiles."
    exit 1
  fi

  shopt -s dotglob nullglob
  local item
  for item in "$backup_dir"/*; do
    src="$item"
    dst="$home_dir/.config/$(basename "$item")"
    if [[ -d "$src" ]]; then
      echo "Restoring directory '$src' to '$dst'..."
      cp -rf "$src" "$dst"
    else
      echo "Restoring file '$src' to '$dst'..."
      cp -f "$src" "$dst"
    fi
  done
  shopt -u dotglob nullglob

  chown -R "$user_name:$user_name" "$home_dir/.config"
  xdg-user-dirs-update
  echo "Dotfiles restored from backup successfully."
}

sddm_theme_config() {
  local sddm_conf_path
  sddm_conf_path="/etc/sddm.conf"

  echo "Configuring SDDM theme..."
  if [[ ! -f "$sddm_conf_path" ]]; then
    echo "SDDM configuration file not found. Skipping SDDM theme configuration."
    return
  fi

  if grep -q '^\[Theme\]' "$sddm_conf_path"; then
    if grep -q '^Current=' "$sddm_conf_path"; then
      sudo sed -i '/^\[Theme\]/,/^\[/ s/^Current=.*/Current=sugar-candy/' "$sddm_conf_path"
    else
      sudo sed -i '/^\[Theme\]/a Current=sugar-candy' "$sddm_conf_path"
    fi
  else
    {
      echo "[Theme]"
      echo "Current=sugar-candy"
    } | sudo tee -a "$sddm_conf_path" >/dev/null
  fi

  echo "SDDM theme configured successfully."
}

connect_to_wifi() {
  local ssid="$1"
  local password="$2"
  local device

  echo "Connecting to Wi-Fi network '$ssid'..."
  device="$(iwctl device list | awk '/wlan/ {print $1; exit}')"

  if [[ -z "$device" ]]; then
    echo "No wireless device found."
    exit 1
  fi

  iwctl device "$device" set-property Powered on
  iwctl station "$device" connect "$ssid" password "$password"
}

usage() {
  cat <<'EOF'
Usage: ./install.sh [OPTIONS]

Options:
  --list-packages-groups        List available package groups
  --add-wheel                  Add the user to wheel group for sudo access
  --install-repository         Install the CachyOS repository
  --install-packages           Install package list
  --install-packages-group G   Install specific package group (default: all)
  --install-omf                Install Oh My Fish
  --copy-dotfiles              Copy dotfiles to ~/.config
  --copy-dotfiles-lua          Copy dotfiles from config_lua (experimental)
  --sddm-theme-config          Configure SDDM theme to sugar-candy
  --remove-repository          Remove CachyOS repository
  --remove-packages            Remove package list
  --remove-omf                 Remove Oh My Fish
  --restore-dotfiles           Restore dotfiles from ~/.config_backup
  --connect-wifi               Connect to Wi-Fi (requires ssid/password)
  --wifi-ssid SSID             Wi-Fi SSID used with --connect-wifi
  --wifi-password PASS         Wi-Fi password used with --connect-wifi
  -h, --help                   Show this help
EOF
}

main() {
  local username action group connect_wifi wifi_ssid wifi_password

  username="$(id -un)"
  action=""
  group="all"
  connect_wifi="false"
  wifi_ssid=""
  wifi_password=""

  if [[ "$username" == "root" ]]; then
    echo "This script should not be run as root. Please run it as a regular user with sudo privileges."
    exit 1
  fi

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --add-wheel)
        action="add-wheel"
        shift
        ;;
      --list-packages-groups)
        action="list-packages-groups"
        shift
        ;;
      --install-repository)
        action="install-repository"
        shift
        ;;
      --install-packages)
        action="install-packages"
        shift
        ;;
      --install-packages-group)
        group="${2:-all}"
        shift 2
        ;;
      --install-omf)
        action="install-omf"
        shift
        ;;
      --copy-dotfiles)
        action="copy-dotfiles"
        shift
        ;;
      --copy-dotfiles-lua)
        action="copy-dotfiles-lua"
        shift
        ;;
      --sddm-theme-config)
        action="sddm-theme-config"
        shift
        ;;
      --remove-repository)
        action="remove-repository"
        shift
        ;;
      --remove-packages)
        action="remove-packages"
        shift
        ;;
      --remove-omf)
        action="remove-omf"
        shift
        ;;
      --restore-dotfiles)
        action="restore-dotfiles"
        shift
        ;;
      --connect-wifi)
        connect_wifi="true"
        action="connect-wifi"
        shift
        ;;
      --wifi-ssid)
        wifi_ssid="${2:-}"
        shift 2
        ;;
      --wifi-password)
        wifi_password="${2:-}"
        shift 2
        ;;
      -h|--help)
        usage
        exit 0
        ;;
      *)
        echo "Unknown argument: $1"
        usage
        exit 1
        ;;
    esac
  done

  case "$action" in
    list-packages-groups)
      list_packages_groups
      ;;
    connect-wifi)
      if [[ "$connect_wifi" != "true" || -z "$wifi_ssid" || -z "$wifi_password" ]]; then
        echo "To use --connect-wifi you must provide --wifi-ssid and --wifi-password."
        exit 1
      fi
      connect_to_wifi "$wifi_ssid" "$wifi_password"
      ;;
    add-wheel)
      echo "Adding user '$username' to the wheel group for sudo access..."
      sudo usermod -aG wheel "$username"
      if ! sudo grep -q '^%wheel ALL=(ALL) ALL' /etc/sudoers; then
        echo '%wheel ALL=(ALL) ALL' | sudo tee -a /etc/sudoers >/dev/null
      fi
      echo "User '$username' added to the wheel group successfully."
      ;;
    install-repository)
      install_cachy_repository
      ;;
    install-packages)
      install_packages "$group"
      ;;
    copy-dotfiles)
      copy_dotfiles "false"
      ;;
    copy-dotfiles-lua)
      copy_dotfiles "true"
      ;;
    sddm-theme-config)
      sddm_theme_config
      ;;
    install-omf)
      install_omf
      ;;
    remove-repository)
      remove_cachy_repository
      ;;
    remove-packages)
      remove_packages
      ;;
    remove-omf)
      remove_omf
      ;;
    restore-dotfiles)
      restore_dotfiles
      ;;
    *)
      echo "No valid arguments provided. Use --help for more information."
      exit 1
      ;;
  esac
}

main "$@"

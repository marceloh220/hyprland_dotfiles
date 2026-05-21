--    ___       __           __           __
--   / _ |__ __/ /____  ___ / /____ _____/ /_
--  / __ / // / __/ _ \(_-</ __/ _ `/ __/ __/
-- /_/ |_\_,_/\__/\___/___/\__/\_,_/_/  \__/

hl.on("hyprland.start", function()

    -- Set Cursor
    hl.exec_cmd("hyprctl setcursor Bibata-Modern-Ice 24")

    -- Start hyprctl monitor for autostart
    hl.exec_cmd("hyprctl --watch reload")

    -- Start xdg-desktop-portal and xdg-desktop-portal-hyprland for screen sharing
    hl.exec_cmd("systemctl --user start xdg-desktop-portal")
    hl.exec_cmd("systemctl --user start xdg-desktop-portal-hyprland")

    -- Start kde files open configuration
    hl.exec_cmd("kbuildsycoca6")

    -- Start hypridle for screen locking and power management
    hl.exec_cmd("systemctl --user start hypridle")

    -- Start Polkit
    -- hl.exec_cmd("/usr/lib/polkit-kde-authentication-agent-1")
    hl.exec_cmd("systemctl --user start hyprpolkitagent")

    -- Load Wallpaper
    hl.exec_cmd("systemctl --user start hyprpaper")

    -- Load waybar
    hl.exec_cmd("systemctl --user start waybar")

    -- Load wireplumber for audio management
    hl.exec_cmd("systemctl --user start pipewire")
    hl.exec_cmd("systemctl --user start wireplumber")

    -- Load mpd for music management
    hl.exec_cmd("systemctl --user start mpd")

    -- Load Notification Daemon (aaargh, I don't like notifications ¬¬)
    -- hl.exec_cmd("swaync")

    -- Load GTK settings and theme
    hl.exec_cmd("~/.config/hypr/scripts/gtk.sh")

    -- Load cliphist history
    hl.exec_cmd("wl-paste --type text --watch cliphist store")
    hl.exec_cmd("wl-paste --type image --watch cliphist store")

    -- Start dbus-update-activation-environment for xdg-desktop-portal-hyprland
    hl.exec_cmd("dbus-update-activation-environment --systemd WAYLAND_DISPLAY XDG_CURRENT_DESKTOP")

    -- A personal project monitor for desktop computer
    -- hl.exec_cmd("streamDeco-monitor")

end)

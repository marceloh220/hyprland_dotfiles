
-- Ignore maximize requests from all apps. You'll probably like this.
local suppressMaximizeRule = hl.window_rule({
    name  = "suppress-maximize-events",
    match = { class = ".*" },
    suppress_event = "maximize",
})
-- suppressMaximizeRule:set_enabled(false)

-- Fix some dragging issues with XWayland
hl.window_rule({
    name  = "fix-xwayland-drags",
    match = {
        class      = "^$",
        title      = "^$",
        xwayland   = true,
        float      = true,
        fullscreen = false,
        pin        = false,
    },
    no_focus = true,
})

-- Layer rules also return a handle.
local overlayLayerRule = hl.layer_rule({
     name  = "no-anim-overlay",
     match = { namespace = "^my-overlay$" },
     no_anim = true,
})
-- overlayLayerRule:set_enabled(false)

-- Hyprland-run windowrule
hl.window_rule({
    name  = "move-hyprland-run",
    match = { class = "hyprland-run" },
    move  = "20 monitor_h-120",
    float = true,
})

-- Blueman Manager
hl.window_rule({
  name = "windowrule-blueman",
  float = true,
  size = { 800, 600 },
  center = true,
  match = { class = "blueman-manager" }
})

-- nm-connection-editor floating
hl.window_rule({
  name = "windowrule-nm-connection-editor",
  float = true,
  match = { title = "^nm-connection-editor$" }
})

-- Pavucontrol floating
hl.window_rule({
  name = "windowrule-pavucontrol",
  float = true,
  match = { title = "^pavucontrol$" }
})

-- Pavucontrol floating
hl.window_rule({
  name = "windowrule-pavucontrol-10",
  float = true,
  size = { 700, 600 },
  center = true,
  pin = true,
  match = { class = ".*org.pulseaudio.pavucontrol.*" }
})

-- nwg-look
hl.window_rule({
  name = "windowrule-nwg-look",
  float = true,
  size = { 700, 600 },
  move = { "(monitor_w*0.1)", "(monitor_h*0.2)" },
  pin = true,
  match = { class = "nwg-look" }
})

-- nwg-displays
hl.window_rule({
  name = "windowrule-nwg-displays",
  float = true,
  size = { 900, 600 },
  move = { "(monitor_w*0.1)", "(monitor_h*0.2)" },
  pin = true,
  match = { class = "nwg-displays" }
})

-- System Mission Center Preference Window
hl.window_rule({
  name = "windowrule-mission-center",
  float = true,
  pin = true,
  center = true,
  size = { 900, 600 },
  match = { class = "io.missioncenter.MissionCenter" }
})

-- Hyprland Share Picker
hl.window_rule({
  name = "windowrule-hyprland-share-picker",
  float = true,
  pin = true,
  size = { 600, 400 },
  center = true,
  match = { class = "hyprland-share-picker" }
})

-- General floating
hl.window_rule({
  name = "windowrule-dotfiles-floating",
  float = true,
  size = { 1000, 700 },
  center = true,
  match = { class = "dotfiles-floating" }
})

-- Private window
hl.window_rule({
  name = "windowrule-private",
  no_screen_share = true,
  match = { class = "private" }
})

-- Showcase window
hl.window_rule({
  name = "windowrule-showcase",
  float = true,
  opacity = 0.8,
  pin = true,
  size = { 700, 450 },
  move = { "(monitor_w-705)", "(monitor_h-455)" },
  match = { class = "showcase" }
})

-- ipython calc window
hl.window_rule({
  name = "windowrule-ipython-calc",
  float = true,
  opacity = 0.5,
  pin = true,
  size = { 350, 450 },
  move = { "(monitor_w-355)", "(monitor_h-455)" },
  match = { class = "calc" }
})

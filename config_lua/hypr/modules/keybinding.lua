local mainMod     = "SUPER"
local SCRIPTS     = "~/.config/hypr/scripts"

local terminal    = "kitty"
local filemanager = "dolphin"
local browser     = "falkon"

hl.bind(mainMod .. " + SPACE",          
		hl.dsp.exec_cmd("pkill rofi || rofi -show drun -replace -i"),
		{description = "Open app launcher"}
)

hl.bind(mainMod .. " + RETURN",         
		hl.dsp.exec_cmd(terminal), 
		{description = "Open terminal"}
)

hl.bind(mainMod .. " + CTRL + RETURN",  
		hl.dsp.exec_cmd(terminal .. " --class showcase"), 
		{description = "Open showcase"}
)

hl.bind(mainMod .. " + SHIFT + RETURN", 
		hl.dsp.exec_cmd(terminal .. " --class private"), 
		{description = "Open terminal in private mode"}
)

hl.bind(mainMod .. " + C",              
		hl.dsp.exec_cmd(terminal .. " --class calc ipython --no-banner"), 
		{description = "Open terminal with ipython"}
)

hl.bind(mainMod .. " + M",              
		hl.dsp.exec_cmd(terminal .. " --class showcase rmpc"),
		{description = "Open terminal with rmpc"}
)

hl.bind(mainMod .. " + W",              
		hl.dsp.exec_cmd(browser), 
		{description = "Open the browser"}
)

hl.bind(mainMod .. " + SHIFT + W",              
		hl.dsp.exec_cmd(browser .. " --class private"), 
		{description = "Open the browser in private mode"}
)

hl.bind(mainMod .. " + E",              
		hl.dsp.exec_cmd(filemanager), 
		{description = "Open the filemanager"}
)

hl.bind(mainMod .. " + SHIFT + E",      
		hl.dsp.exec_cmd(filemanager .. " --class private"), 
		{description = "Open the filemanager in private mode"}
)

hl.bind(mainMod .. " + R",              
		hl.dsp.exec_cmd("code"), 
		{description = "Open vscode"}
)

hl.bind("Print",                         
		hl.dsp.exec_cmd(SCRIPTS .. "/screenshot.sh"),
		{description = "Take screenshot"}
)

hl.bind(mainMod .. " + ALT + F",        
		hl.dsp.exec_cmd(SCRIPTS .. "/screenshot.sh --instant"),
		{description = "Take instant fullscreen screenshot"}
)

hl.bind(mainMod .. " + ALT + S",        
		hl.dsp.exec_cmd(SCRIPTS .. "/screenshot.sh --instant-area"),
		{description = "Take instant area screenshot"}
)

hl.bind(mainMod .. " + V",              
		hl.dsp.exec_cmd(SCRIPTS .. "/cliphist.sh"),
		{description = "Open clipboard history"}
)

hl.bind(mainMod .. " + Q",              
		hl.dsp.window.close(), 
		{description = "Kill active window"}
)

hl.bind(mainMod .. " + SHIFT + Q",      
		hl.dsp.exec_cmd(SCRIPTS .. "/wlogout.py"), 
		{description = "Quit active window and all open instances"}
)

hl.bind(mainMod .. " + L",              
		hl.dsp.exec_cmd("hyprlock"), 
		{description = "Lock session"}
)

hl.bind(mainMod .. " + CTRL + R",       
		hl.dsp.exec_cmd("hyprctl reload"),
		{description = "Reload Hyprland config"}
)

hl.bind("CTRL + SHIFT + Escape",     
		hl.dsp.exec_cmd("missioncenter"), 
		{description = "Quit active window and all open instances"}
)

hl.bind("CTRL + ALT + Delete",     
		hl.dsp.exec_cmd("missioncenter"), 
		{description = "Quit active window and all open instances"}
)

hl.bind(mainMod .. " + left",           
		hl.dsp.focus({ direction = "l" }), 
		{description = "Move focus left"}
)

hl.bind(mainMod .. " + right",          
		hl.dsp.focus({ direction = "r" }), 
		{description = "Move focus right"}
)

hl.bind(mainMod .. " + up",             
		hl.dsp.focus({ direction = "u" }), 
		{description = "Move focus up"}
)

hl.bind(mainMod .. " + down",           
		hl.dsp.focus({ direction = "d" }), 
		{description = "Move focus down"}
)

hl.bind(mainMod .. " + mouse:272",      
		hl.dsp.window.drag(), 
		{ mouse = true }, 
		{description = "Move window with the mouse right button"}
)

hl.bind(mainMod .. " + CTRL + right",   
		hl.dsp.window.resize({ x = 100,  y = 0,    relative = true }), 
		{description = "Increase window width with keyboard"}
)

hl.bind(mainMod .. " + CTRL + left",    
		hl.dsp.window.resize({ x = -100, y = 0,    relative = true }), 
		{description = "Reduce window width with keyboard"}
)

hl.bind(mainMod .. " + CTRL + down",    
		hl.dsp.window.resize({ x = 0,    y = 100,  relative = true }), 
		{description = "Increase window height with keyboard"}
)

hl.bind(mainMod .. " + CTRL + up",      
		hl.dsp.window.resize({ x = 0,    y = -100, relative = true }), 
		{description = "Reduce window height with keyboard"}
)

hl.bind(mainMod .. " + mouse:273",      
		hl.dsp.window.resize(), 
		{ mouse = true }, 
		{description = "Resize window with the mouse right button"}
)

hl.bind(mainMod .. " + F",              
		hl.dsp.window.fullscreen({ mode = "fullscreen" }),
		{description = "Toggle fullscreen mode"}
)

hl.bind(mainMod .. " + T",              
		hl.dsp.window.float(),
		{description = "Toggle floating mode"}
)

hl.bind(mainMod .. " + J",              
		hl.dsp.layout("togglesplit"),
		{description = "Toggle split layout"}
)

hl.bind(mainMod .. " + G",              
		hl.dsp.group.toggle(),
		{description = "Toggle window group"}
)

hl.bind(mainMod .. " + K",              
		hl.dsp.layout("swapsplit"),
		{description = "Swap split orientation"}
)

hl.bind(mainMod .. " + ALT + left",     
		hl.dsp.window.swap({ direction = "l" }),
		{description = "Swap window to the left"}
)

hl.bind(mainMod .. " + ALT + right",    
		hl.dsp.window.swap({ direction = "r" }),
		{description = "Swap window to the right"}
)

hl.bind(mainMod .. " + ALT + up",       
		hl.dsp.window.swap({ direction = "u" }),
		{description = "Swap window upward"}
)

hl.bind(mainMod .. " + ALT + down",     
		hl.dsp.window.swap({ direction = "d" }),
		{description = "Swap window downward"}
)

hl.bind("ALT + Tab",                     
		function()
			hl.dispatch(hl.dsp.window.cycle_next())
			hl.dispatch(hl.dsp.window.bring_to_top())
		end,
		{description = "Cycle to next window"}
)

hl.bind(mainMod .. " + 1",              
		hl.dsp.focus({ workspace = 1  }),
		{description = "Switch to workspace 1"}
)

hl.bind(mainMod .. " + 2",              
		hl.dsp.focus({ workspace = 2  }),
		{description = "Switch to workspace 2"}
)

hl.bind(mainMod .. " + 3",              
		hl.dsp.focus({ workspace = 3  }),
		{description = "Switch to workspace 3"}
)

hl.bind(mainMod .. " + 4",              
		hl.dsp.focus({ workspace = 4  }),
		{description = "Switch to workspace 4"}
)

hl.bind(mainMod .. " + 5",              
		hl.dsp.focus({ workspace = 5  }),
		{description = "Switch to workspace 5"}
)

hl.bind(mainMod .. " + 6",              
		hl.dsp.focus({ workspace = 6  }),
		{description = "Switch to workspace 6"}
)

hl.bind(mainMod .. " + 7",              
		hl.dsp.focus({ workspace = 7  }),
		{description = "Switch to workspace 7"}
)

hl.bind(mainMod .. " + 8",              
		hl.dsp.focus({ workspace = 8  }),
		{description = "Switch to workspace 8"}
)

hl.bind(mainMod .. " + 9",              
		hl.dsp.focus({ workspace = 9  }),
		{description = "Switch to workspace 9"}
)

hl.bind(mainMod .. " + 0",              
		hl.dsp.focus({ workspace = 10 }),
		{description = "Switch to workspace 10"}
)

hl.bind(mainMod .. " + SHIFT + 1",      
		hl.dsp.window.move({ workspace = 1  }),
		{description = "Move window to workspace 1"}
)

hl.bind(mainMod .. " + SHIFT + 2",      
		hl.dsp.window.move({ workspace = 2  }),
		{description = "Move window to workspace 2"}
)

hl.bind(mainMod .. " + SHIFT + 3",      
		hl.dsp.window.move({ workspace = 3  }),
		{description = "Move window to workspace 3"}
)

hl.bind(mainMod .. " + SHIFT + 4",      
		hl.dsp.window.move({ workspace = 4  }),
		{description = "Move window to workspace 4"}
)

hl.bind(mainMod .. " + SHIFT + 5",      
		hl.dsp.window.move({ workspace = 5  }),
		{description = "Move window to workspace 5"}
)

hl.bind(mainMod .. " + SHIFT + 6",      
		hl.dsp.window.move({ workspace = 6  }),
		{description = "Move window to workspace 6"}
)

hl.bind(mainMod .. " + SHIFT + 7",      
		hl.dsp.window.move({ workspace = 7  }),
		{description = "Move window to workspace 7"}
)

hl.bind(mainMod .. " + SHIFT + 8",      
		hl.dsp.window.move({ workspace = 8  }),
		{description = "Move window to workspace 8"}
)

hl.bind(mainMod .. " + SHIFT + 9",      
		hl.dsp.window.move({ workspace = 9  }),
		{description = "Move window to workspace 9"}
)

hl.bind(mainMod .. " + SHIFT + 0",      
		hl.dsp.window.move({ workspace = 10 }),
		{description = "Move window to workspace 10"}
)

hl.bind(mainMod .. " + SHIFT + mouse:272", 
		hl.dsp.window.move({ workspace = "empty" }),
		{description = "Move window to empty workspace"}
)

hl.bind(mainMod .. " + mouse_down",     
		hl.dsp.focus({ workspace = "e+1" }),
		{description = "Switch to next workspace"}
)

hl.bind(mainMod .. " + mouse_up",       
		hl.dsp.focus({ workspace = "e-1" }),
		{description = "Switch to previous workspace"}
)

hl.bind(mainMod .. " + CTRL + right",   
		hl.dsp.focus({ workspace = "m+1" }),
		{description = "Switch to next monitor workspace"}
)

hl.bind(mainMod .. " + CTRL + left",    
		hl.dsp.focus({ workspace = "m-1" }),
		{description = "Switch to previous monitor workspace"}
)

hl.bind(mainMod .. " + Tab",            
		hl.dsp.focus({ workspace = "m+1" }),
		{description = "Switch to next monitor workspace"}
)

hl.bind(mainMod .. " + SHIFT + Tab",    
		hl.dsp.focus({ workspace = "m-1" }),
		{description = "Switch to previous monitor workspace"}
)

hl.bind(mainMod .. " + CTRL + down",    
		hl.dsp.focus({ workspace = "empty" }),
		{description = "Switch to next empty workspace"}
)

hl.bind("XF86MonBrightnessUp",           
		hl.dsp.exec_cmd("brightnessctl -q s +10%"),
		{description = "Increase brightness"}
)

hl.bind("XF86MonBrightnessDown",         
		hl.dsp.exec_cmd("brightnessctl -q s 10%-"),
		{description = "Decrease brightness"}
)

hl.bind("XF86AudioRaiseVolume",          
		hl.dsp.exec_cmd("wpctl set-volume -l 1 @DEFAULT_AUDIO_SINK@ 2%+"), 
		{ repeating = true },
		{description = "Increase volume"}
)

hl.bind("XF86AudioLowerVolume",          
		hl.dsp.exec_cmd("wpctl set-volume @DEFAULT_AUDIO_SINK@ 2%-"), 
		{ repeating = true },
		{description = "Decrease volume"}
)

hl.bind("XF86AudioMute",                 
		hl.dsp.exec_cmd("pactl set-sink-mute @DEFAULT_SINK@ toggle"),
		{description = "Toggle audio mute"}
)

hl.bind("XF86AudioPlay",                 
		hl.dsp.exec_cmd("playerctl play-pause"),
		{description = "Play or pause media"}
)

hl.bind("XF86AudioPause",                
		hl.dsp.exec_cmd("playerctl pause"),
		{description = "Pause media"}
)

hl.bind("XF86AudioNext",                 
		hl.dsp.exec_cmd("playerctl next"),
		{description = "Next media track"}
)

hl.bind("XF86AudioPrev",                 
		hl.dsp.exec_cmd("playerctl previous"),
		{description = "Previous media track"}
)

hl.bind("XF86AudioMicMute",              
		hl.dsp.exec_cmd("pactl set-source-mute @DEFAULT_SOURCE@ toggle"),
		{description = "Toggle microphone mute"}
)

hl.bind("XF86Calculator",                
		hl.dsp.exec_cmd("gnome-calculator"),
		{description = "Open calculator"}
)

hl.bind("code:238",                      
		hl.dsp.exec_cmd("brightnessctl -d smc::kbd_backlight s +10"),
		{description = "Increase keyboard backlight"}
)

hl.bind("code:237",                      
		hl.dsp.exec_cmd("brightnessctl -d smc::kbd_backlight s 10-"),
		{description = "Decrease keyboard backlight"}
)

hl.bind("switch:on:Lid Switch",          
		hl.dsp.exec_cmd("hyprctl dispatch dpms off && hyprlock"), 
		{ locked = true },
		{description = "Turn screen off and lock when lid closes"}
)

hl.bind("switch:off:Lid Switch",         
		hl.dsp.exec_cmd("hyprctl dispatch dpms on"), 
		{ locked = true },
		{description = "Turn screen on when lid opens"}
)

if status is-interactive
    # Commands to run in interactive sessions can go here
		kitty @ set-colors -a ~/.config/kitty/theme.conf
		zoxide init fish | source
    thefuck --alias | source
		#fastfetch
		#~/.config/hypr/scripts/whatthedouchesays.py
end

if status is-interactive && test -f ~/.config/fish/custom/git_fzf.fish
	source ~/.config/fish/custom/git_fzf.fish
	git_fzf_key_bindings
end

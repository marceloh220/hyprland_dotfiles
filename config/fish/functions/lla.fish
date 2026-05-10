function lla --wraps='exa --color=always --group-directories-first --icons=always -la' --wraps='ll -a' --description 'alias lla=ll -a'
    ll -a $argv
end

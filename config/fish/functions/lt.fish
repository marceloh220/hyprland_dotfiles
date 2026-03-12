function lt --wraps='exa --color=always --group-directories-first --icons=always -T' --wraps='exa --color=always --group-directories-first --icons=always -TL 1' --wraps='exa --color=always --group-directories-first --icons=always -TL 2' --description 'alias lt=exa --color=always --group-directories-first --icons=always -TL 2'
  exa --color=always --group-directories-first --icons=always -TL 2 $argv
        
end

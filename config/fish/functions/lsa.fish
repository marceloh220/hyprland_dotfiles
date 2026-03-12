function lsa --wraps='exa --color=always --group-directories-first --icons=always -a' --description 'alias la=exa --color=always --group-directories-first --icons=always -a'
  exa --color=always --group-directories-first --icons=always -a $argv
        
end

function ll --wraps=ls --wraps='exa --color=always --group-directories-first --icons=always -l' --description 'alias ll=exa --color=always --group-directories-first --icons=always -l'
  exa --color=always --group-directories-first --icons=always -l $argv
        
end

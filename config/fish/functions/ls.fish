function ls --wraps='exa --color=always --group-directories-first --icons=always' --description 'alias ls=exa --color=always --group-directories-first --icons=always'
  exa --color=always --group-directories-first --icons=always $argv
        
end

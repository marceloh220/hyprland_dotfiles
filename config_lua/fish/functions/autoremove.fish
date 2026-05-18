function autoremove --wraps='yay -Yc' --description 'alias autoremove=yay -Yc'
    yay -Yc $argv
end

function upgrade --wraps='yay -Syu' --description 'alias upgrade=yay -Syu'
    yay -Syu $argv
end

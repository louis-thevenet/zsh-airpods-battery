function airpods_battery() {
local DATA=$(cat /tmp/airpods_battery.out)
    RPROMPT=$DATA
}

autoload -Uz add-zsh-hook
add-zsh-hook precmd airpods_battery
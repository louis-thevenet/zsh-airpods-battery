function airpods_battery() {
#AIRPODS_BATTERY_CUSTOM_DATA=$(cat $ZSH_CUSTOM/plugins/airpods-battery/battery_data)
local DATA=$(cat $ZSH_CUSTOM/plugins/airpods-battery/battery_data)
    RPROMPT=$DATA
}

autoload -Uz add-zsh-hook
add-zsh-hook precmd airpods_battery
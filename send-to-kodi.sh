#!/bin/bash

# Required settings
host="192.168.199.145"
port="8080"

# Optional login for Kodi
#user=
#pass=

# Settings for netcat (local file)
local_hostname=$(hostname)
local_port=12345



show_help()
{
    cat<<EOF
Sends a video URL to Kodi
Usage: send-to-kodi.sh [URL]

If no URL is given, a dialog window is shown (requires zenity).

Supports:
Common file formats (mp4,flv,mp3,jpg and more)
Youtube (requires the Youtube plugin in Kodi)
Local media streaming (via netcat)
Manny more sites (requires youtube-dl)

Configuration is done in the head of the script.

EOF
}

error()
{
    if type zenity &>/dev/null; then
     	zenity --error --ellipsize --text "$*"
    else
	echo "$*" 1>&2
    fi
    
    exit 1
}

send_json()
{
    curl \
	${user:+--user "$user:$pass"} \
	-X POST \
	-H "Content-Type: application/json" \
	-d '{"jsonrpc":"2.0","method":"Player.Open","params":{"item":{"file":"'"$1"'"}},"id":1}' \
	http://$host:$port/jsonrpc \
	|| error "Failed to send link - is Kodi running?"
}

# 16:45:58 T:123145476141056 WARNING: [plugin.video.youtube] DEPRECATED "plugin://plugin.video.youtube/?action=play_video&videoid=https://www.youtube.com/watch?v=bjUoQbSJDJs"
# 16:45:58 T:123145476141056 WARNING: [plugin.video.youtube] USE INSTEAD "plugin://plugin.video.youtube/play/?video_id=https://www.youtube.com/watch?v=bjUoQbSJDJs"


[[ $host && $port ]] || error "Please set host and port in configuration"
[[ "$1" = --help ]] && show_help

# Dialog box?
url="$1"
url=$(./youtube-dl -g $url)
[[ $url ]] && send_json "$url"

# Wait for netcat to exit
wait
# Don't kill netcat
trap - EXIT

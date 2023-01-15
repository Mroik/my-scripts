#!/bin/bash
MONITOR=$(swaymsg -t get_outputs -p | grep Output | cut -d \  -f 2 | dmenu -p "Choose monitor")
IMAGE="/home/mroik/Pictures/wallpapers/$(ls ~/Pictures/wallpapers | dmenu -p "Image")"
IS_LOCK="$(echo -e "yes\nno" | dmenu -p "Is lockscreen?")"
if [[ $MONITOR == "DVI-D-1" && $IS_LOCK == "no" ]]
then
	rm "/home/mroik/Pictures/wallpaper.jpg"
	ln -s $IMAGE "/home/mroik/Pictures/wallpaper.jpg"
elif [[ $MONITOR == "HDMI-A-1" && $IS_LOCK == "no" ]]
then
	rm "/home/mroik/Pictures/wallpaper2.jpg"
	ln -s $IMAGE "/home/mroik/Pictures/wallpaper2.jpg"
elif [[ $MONITOR == "DVI-D-1" && $IS_LOCK == "yes" ]]
then
	rm "/home/mroik/Pictures/lock.jpg"
	ln -s $IMAGE "/home/mroik/Pictures/lock.jpg"
else
	rm "/home/mroik/Pictures/lock2.jpg"
	ln -s $IMAGE "/home/mroik/Pictures/lock2.jpg"
fi

if [[ $IS_LOCK == "no" ]]
then
	pkill swaybg
	swaybg -o DVI-D-1 -i /home/mroik/Pictures/wallpaper.jpg -o HDMI-A-1 -i /home/mroik/Pictures/wallpaper2.jpg
fi

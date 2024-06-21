#!/bin/bash

error(){
    echo $1 >&2
    exit $2
}

#setting global variables
FOLDER_ROUTE=$HOME 
ROS2_WRK="ros_tfg"
STATS_FOLDER="sim_stats"
STATS_BACKUP="${HOME}/stats_backup"

#check quantity of arguments
if [ $# -ne 2 ]
then
    error "bad arguments" 1
fi

#check if first parameter is a directory
test -d $1 || test $1 = "IMDSUT"
isdir=$?
if [ $isdir -ne 0 ]
then
    error "first argument isnt a directory" 2
fi 

#check if STATS_BACKUP folder exists, if not create it
ls $STATS_BACKUP >& /dev/null || mkdir $STATS_BACKUP

#save previous sim_stats
if [ $2 != "NOACTION" ]
then
    mv "$HOME/$STATS_FOLDER" "$STATS_BACKUP/$2" >& /dev/null
    cp "$HOME/$ROS2_WRK/src/scenariovis/rviz/rosviz-conf.rviz" "$STATS_BACKUP/$2/" >& /dev/null
    rm "$STATS_BACKUP/$2/area.yaml" >& /dev/null
    cp "$HOME/$ROS2_WRK/src/planner/config/perimeter.yaml" "$STATS_BACKUP/$2/area.yaml" >& /dev/null || echo "fallo perimeter"
fi

#set new sim_stats
if [ $1 = "IMDSUT" ]
then
    mkdir "$HOME/$STATS_FOLDER" >& /dev/null
else
    newdir=$1
    [ "${1: -1}" == '/' ] || newdir="$1/"
    cp "$newdir"* "$HOME/$STATS_FOLDER/"
    mv "$HOME/$STATS_FOLDER/rosviz-conf.rviz" "$HOME/$ROS2_WRK/src/scenariovis/rviz/"
fi

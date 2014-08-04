#!/usr/bin/zsh
# backup_mc.sh - paws
# takes incremental backups using cpio and/or rsyn (based on cron) 
# Last Modified 07/27/2014

## Change these to relative server locations,
# TODO: MOdularize functoins, take input options, handle config file, allow parent dir OR specific weekly or monthly
minecraft_home="/opt/MC"  # where the minecraft install is based. script won't run unless server.prroperties is here.
backup_location="/opt/MCbackup_test"
title=minecraft_server

## should probably leave these alone
timestamp=`date +'%Y%m%d%H%M%S'`
runtime=`date +%s`
backdir="${backup_location}/incremental/${timestamp}"
backname="${backdir}/${title}.${timestamp}.cpio.gz"
backup_loc_relative=$(basename "${backup_location}")
daily_clean_flag="${backup_location}/.daily.stamp"
weekly_clean_flag="${backup_location}/.weekly.stamp"
daily_location="${backup_location}/daily"
weekly_location="${backup_location}/weekly"
incremental_location="${backup_location}/regular"
daily_comp=0
weekly_comp=0

## backup management functions
manage_backups() {
last_daily=$(check_flag "daily")
# 86400 sec = 24 hr
if [ `math "${last_daily}+86400"` -le ${runtime} ]; then
  echo "  -Creating daily backup ..."
  create_copy "daily"
  daily_comp=1
fi

if [ ${last_daily} -eq ${runtime} ]; then
  echo "[WARN]: Created daily last run file.  Ignore warning if first run."
  create_copy "daily"
fi

# 604800 sec = 7 days
last_weekly=`check_flag "weekly"`
if [ $((${last_weekly}+604800)) -le ${runtime} ]; then 
  echo "  -Creating weekly backup ..."
  create_copy "weekly"
  weekly_comp=1
fi

if [ ${last_weekly} -eq ${runtime} ]; then
  echo "[WARN]: Created weekly last run file.  Ignore warning if first run."
  create_copy "weekly"
fi

echo "  -Performing incremental cleanup process ..."
roll_runtime
echo "[INFO]: Incremental backups older than 24 hours have been removed."

if [ ${daily_comp} -eq 1 ]; then
  echo "[INFO]: Backup (daily) created at (${daily_location}/`echo ${backname} | awk -F\/ '{print $NF}'`)."
fi
if [ ${weekly_comp} -eq 1 ]; then
  echo "[INFO]: Backup (weekly) created at (${weekly_location}/`echo ${backname} | awk -F\/ '{print $NF}'`)."
fi

}

check_flag() {
if [ "${*}" = "daily" ]; then
  flagfile="${daily_clean_flag}"
  dir="${daily_location}"
elif [ "${*}" = "weekly" ]; then
  flagfile="${weekly_clean_flag}"
  dir="${weekly_location}"
fi
if [ ! -f "${flagfile}" ]; then
  echo "${runtime}" > ${flagfile}
fi
if [ ! -d "${dir}" ]; then
  mkdir -p "${dir}" 
fi

cat "${flagfile}"
}

create_copy() {
if [ "${*}" = "daily" ]; then
  newloc="${daily_location}"
elif [ "${*}" = "weekly" ]; then
  newloc="${weekly_location}"
fi
cp -ipR ${backname} ${newloc}
rval=$?
if [ ${rval} -ne 0 ]; then
  echo "[ERROR]: Could not sync backup ("${*}"). (cp -ipR ${backname} ${newloc})."
  exit 4
fi
}

## regardless of cron, everything older than 24 hours is gone
roll_runtime() {
if [ ! -d ${incremental_location} -o ${incremental_location} = "/" -o ${incremental_location} = "" ]; then
  echo "[ERROR]: Unable to safely remove incremental files.  Script is broken."
  exit 5
fi
find ${incremental_location}/* -type d -prune -mtime +1 -exec rm -r {} \;
rval=$?
if [ ${rval} -ne 0 ]; then
  echo "[ERROR]: Unable to clean up incremental backup files."
  exit 6
fi
}

check_back_root() {
if [ ! -d ${backup_location} ]; then
  echo "[WARN]: -Backup directory (${backup_location}) does not exist. Creating."
  out=$(mkdir -p ${backup_location}) || echo "FAILED: $out." && exit 3
fi
}

create_back_dir() {
echo "  -Creating backup dir (${backdir})."
mkdir -p ${backdir}
rval=$?
if [ ${rval} != 0 ]; then
  echo "[ERROR]: Could not create backup directory (${backdir}). Exiting."
  exit 1
fi
}

do_backup() {
echo "  -Backing up Minecraft server (${minecraft_home}) ..."
cd ${minecraft_home}
find . | grep -v "./${backup_loc_relative}" | cpio --quiet -o | gzip -c - > ${backname}
rval=$?
if [ ${rval} -ne 0 ]; then
  echo "[ERROR]: Backup exited with return value (${rval}).  FAILED."
  exit 2
fi
}

## helper functions
math() {
echo "${*}" | bc
}

## main Main MAIN

check_back_root
create_back_dir
do_backup
manage_backups 

echo "[INFO}: Incremental backup created at (${backname})."
echo "Normal Termination."
exit 0

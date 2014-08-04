#!/usr/bin/zsh
# backup - mrpaws
# takes incremental backups using cpio and/or rsyn (based on cron) 
# Last Modified 08/04/2014

prog=$(basename ${0})

usage() { 
  printf "Backup location(s)  on a regular interval via cron or live syncing (rsync wrapper)\n\
with built-in  (D)aily, (W)eekly, (M)onthly and (Y)early backup management, plus\n\
support for any number of user-specified pools with custom frequencies and retention.\n\n" 
  printf "%1sUsage: ${prog} [OPTIONS] <src> <storage root>\n"
  printf "%3sor%3s${prog} -i <config file> <src> <storage root>\n"
  printf "%3sor%3s${prog} -d [USER@][HOST]:<src> <live sync location>\n"
  printf "%3sor%3s${prog} -C custom -r5d -f12h <src> <storage root>\n\n"
  printf "%1sOptions:\n"
  printf "%3sGeneral:\n"
  printf "%4s[-i,--include]\tspecify configuration file\n"
  printf "%4s[-d,--daemon] \tbackup changing files in realtime\n"
  printf "%4s[-r,--retention]\tspecify retention for 'regular'  backups\n"
  printf "%4s[-f,--frequency]\tspecify frequency for 'regular' backups\n"
  printf "%4s[-m,--mode] <rsync|cpio> => <1:1 snapshot|compressed archive>\n\n"
  printf "\n%3sCustom:\n"
  printf "%4s[-C,--custom] \tspecifies a custom backup pool\n"
  printf "%6s[-r,--retention]\tspecify retention for 'custom'  backups\n"
  printf "%6s[-f,--frequency]\tspecify frequency for 'custom' backups\n\n"
  printf "\n%3sDisable Defaults:\n"
  printf "%4s[-N,--none]\t\tskip ALL builtin pools (daily, etc..)\n"
  printf "%4s[-D,--no-daily]\tskip 'daily' backup\n"
  printf "%4s[-W,--no-weekly]\tskip 'weekly' backup\n"
  printf "%4s[-M,--no-monthly]\tskip 'monthly' backup\n"
  printf "%4s[-Y,--no-yearly]\tskip 'yearly' backup\n"
}

usage

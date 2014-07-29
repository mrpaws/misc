#!/usr/bin/env bash 
# september 2013 - mrpaws
# build latest kernel

## Assign variables

PROG_NAME="${0}"
BUILDOUT="kernel_update.log"
BUILD_DIR="/kernel-source/latest-automatic"
GITURL="git://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git"
KERNELVERSION="derp"
NPROCESSES=8
# $(echo $(grep -c "^processor" /proc/cpuinfo | awk '{print $NF}')*2 | bc)
BRAND="mawpaw"
FORCE=0
FRESH=0

usage() { 
cat << EOF
usage: ${PROG_NAME} [hf] [d <build dir>] [b <branding>]

  --build-dir, -d <build-dir>   specify build directory
  --brand, -b <branding>    	specify build branding
  --force, -f 			build even if no code diffs
  --help, -h  			this message
EOF
exit 1
}

argparse() {
TEMP=$(getopt -o fhd:,b: --longoptions build-dir:,brand:,help,force -- "$@") \
   || usage

eval set -- "$TEMP"

while true ; do
  case "$1" in
    -d|--build-dir) 
      BUILD_DIR=$2;  
      shift 2;;
    -b|--brand)
      BRAND=$2;
      shift 2;;
    -h|--help)
      usage;
      shift;;
    -f|--force)
      FORCE=1;
      shift;;
    --) 
      shift ; 
      break;;
    *) 
      echo "${PROG_NAME}: Unknown argument ($1)" && \
        usage ;
      exit 1 ;;
  esac
done
}

build() {
  ## we use a stack for code reduction and ease of addition
CMDS="C:make clean
C:make oldconfig 
C:make -j${NPROCESSES} 
C:make modules -j${NPROCESSES}
C:make install 
C:make modules_install 
C:mkinitramfs -o /boot/initrd.img-${KERNELVERSION}+ ${KERNELVERSION}+"

while IFS= read
do
  run_cmd "${REPLY}"
done <<< "${CMDS}"
}

update_bootloader() {
## save time and let the os update grub 
## we're probably using debian so we can
## rely on  kernel build tools. 

if [[ $(cat /etc/issue) =~ Debian ]];
then
  run_cmd "C:/etc/kernel/postinst.d/zz-update-grub"
else 
  if [ -f "/boot/grub/grub.cfg" ]; 
  then
    run_cmd "C:${EDITOR:-vi} /boot/grub/grub.cfg"
   else
    echo "Warning: Couldn't update boot loader."
  fi

fi
}

validate_sanity() {
## validate the build_dir.  odds are we are runnign as 
## root and are likely running dangerous commands on this dir
if [ ! -d "${BUILD_DIR}" ];
then
    if [ ! -e "${BUILD_DIR}" ];
    then
      mkdir -p $BUILD_DIR || \
      echo -e "$(date) -  ERROR: Unable to create dir!" && \
      exit 2
    else
      echo -e "$(date) - ERROR: Build dir is insane!" && \
      exit 2
    fi
fi
}

fresh_build() {
## see if we need to create a new dir for the build
if [ ! -f "MAINTAINERS" ];
then
  FRESH=1
  echo "  No source in ($BUILD_DIR).  Clearing and downloading."
  rm -rf ${BUILD_DIR}/*
  cd $BUILD_DIR
  run_cmd "C:git clone "${GITURL}""
  mv $BUILD_DIR/linux/* $BUILD_DIR 
  mv $BUILD_DIR/linux/.[a-zA-Z0-9]* $BUILD_DIR 
  make defconfig
else
  git checkout .
fi
}

check_pull() {
## check for new source code, exit if none
if [[ $(git pull)  =~ up-to-date && ${FRESH} -eq 0 ]];
then
  echo "$(date) - No diffs."
  if [ ${FORCE} -eq 0 ];
  then 
    exit 0
  fi
fi
}

kern_version() {
## check, update and record kernel version
if [ $(grep EXTRAVERSION Makefile | grep -c "$BRAND") -eq 0 ];   
then
  run_cmd "C:sed -i \"s/^EXTRAVERSION = \(.*$\)/EXTRAVERSION = -${BRAND}/\" Makefile"
fi
KERNELVERSION=$(make kernelversion)
}

build_dir() {
  ## add anything you need to do with the build dir here
  run_cmd "B:cd ${BUILD_DIR}"
}

run_cmd() {
## use this for the important commands
## which are worth outputting for debug
## purposes
rcmd=$1
cmd_type=$(expr substr "$rcmd" 1 1)
cmd=$(expr substr "${rcmd}" 3 $(echo "$(echo "$rcmd" | wc -m)-3" | bc))

if [ ${cmd_type} == "C" ];
then
  echo -ne "  $(date) - EXEC (${cmd}) ... "
  eval nice -20 ${cmd} >> ${BUILDOUT}
  if [ $? -ne 0 ];
  then
    echo -e "\n$(date) - ERROR: Build Error during '${cmd}'!"
    exit $?
  fi
  echo " OK."
elif [ ${cmd_type} == "B" ];
then
  echo -ne "  $(date) - BASH (${cmd}) ... "
  ${cmd}
  echo " DONE"
fi
}

#
# main Main MAIN
#

argparse ${*}
validate_sanity
build_dir
fresh_build
check_pull
kern_version
build
update_bootloader

exit 0

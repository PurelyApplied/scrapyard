#!/usr/bin/bash
# A script for temporary ssh key identification

if [ $# -ne 1 ] ;
   echo "Usage: ./ssh_key.sh [time active string] [unmount=true (enter any for false)]"
   exit 1
fi

KEYCHAIN="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
APP=${KEYCHAIN}/Applications/VeraCrypt.app/Contents/MacOS
VOLUME=${KEYCHAIN}/VeraVolume
MOUNT_LOCATION=/tmp/psr_key_mount
KEYS_LOCATION=${MOUNT_LOCATION}/Keys/

pushd ${APP}
  mkdir -p ${MOUNT_LOCATION}
  ./VeraCrypt --mount ${VOLUME} ${MOUNT_LOCATION}
  pushd ${KEYS_LOCATION}
    ssh-add -t ${1} id_rsa
    STATUS=$?
  popd
  ./VeraCrypt -d ${VOLUME}
  test ''
  rm -rf ${MOUNT_LOCATION}
popd

if [ $STATUS -ne 0 ] ; then
    if test ${2} ; then
        diskutil unmountDisk force ${KEYCHAIN}/
    fi
fi


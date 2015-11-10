#!/bin/python

from subprocess import check_output as run
import os
import argparse

def mountSnapshotRW(path, enableWrite):
    run("btrfs property set -ts " + path + " ro " + str(not enableWrite).lower(), shell=True)

if not os.geteuid() == 0:
    print "You must run this script as root"
    exit(1)

parser = argparse.ArgumentParser(description='snapper-delete: Delete a file from all previous snapshots. ')
parser.add_argument('-f','--filename', help='Location of the file you want to delete. ', required=True)
args = parser.parse_args()

for snapshot in os.listdir('/.snapshots/'):
    mountSnapshotRW("/.snapshots/" + snapshot + "/snapshot/", True)
    try:
        run("rm /.snapshots/" + snapshot + "/snapshot" + args.filename, shell=True)
        print "Deleted from /.snapshots/" + snapshot
    except:
        pass
    mountSnapshotRW("/.snapshots/" + snapshot + "/snapshot/", False)

mountSnapshotRW("/", True)

# vim: set fileencoding=utf-8 :
# Mount and print functions
import os
import subprocess

camera_mount = "/mnt/camera"
printer = 'Kodak-ESP-5250-usb'
do_camera = True
do_print = True

def mount_camera():
    if do_camera:
        if os.path.exists(camera_mount) and os.path.ismount(camera_mount):
            mounted = True
        else:
            mounted = not subprocess.call(['mount', camera_mount])
        return mounted
    else:
        return True

def umount_camera():
    if do_camera:
        if os.path.exists(camera_mount) and os.path.ismount(camera_mount):
            umounted = not subprocess.call(['umount', camera_mount])
        else:
            umounted = True
        return umounted
    else:
        return True

def print_image(filename):
    if do_print:
        success = not subprocess.call(['lp', '-d' + printer, '-o', 'media=a4', '-o', 'scaling=100', filename])
        return success
    else:
        return True

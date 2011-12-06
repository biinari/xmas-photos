# vim: set fileencoding=utf-8 :
# Mount and print functions
import os
import shutil
import subprocess

camera_mount = "/mnt/camera"
camera_src = camera_mount + "/DCIM/100OLYMP"
printer = 'Kodak-ESP-5250-usb'
#printer = 'Brother-MFC-5840CN-USB'
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

def get_camera_files():
    if os.path.exists(camera_src):
        for src_file in os.listdir(camera_src):
            shutil.move(camera_src + '/' + src_file, 'infiles/')

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

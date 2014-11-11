# vim: set fileencoding=utf-8 :
# Mount and print functions
import os
import shutil
import subprocess
import time

CAMERA_MOUNT = "/mnt/camera"
CAMERA_SRC = CAMERA_MOUNT + "/DCIM/101___12"
PRINTER = 'HP-Photosmart-C5280'
#PRINTER = 'Kodak_ESP_5200_Series_AiO'
#PRINTER = 'Brother-MFC-5840CN-USB'
DO_CAMERA = True
DO_PRINT = True

def detect_gphoto():
    output = subprocess.check_output(['gphoto2', '--auto-detect'])
    return output.find('USB PTP Class Camera') != -1

USE_GPHOTO = detect_gphoto()
#USE_GPHOTO = False

class UnboundCallbackError(UnboundLocalError):
    """ Callback function not set error. """
    pass

class Logger(object):
    _callback = None

    def set_callback(self, callback=None):
        type(self)._callback = callback

    def log(self, message):
        if self._callback != None:
            self._callback(message)
        else:
            raise UnboundCallbackError("Callback function not set")

def mount_camera():
    if DO_CAMERA and not USE_GPHOTO:
        if os.path.exists(CAMERA_MOUNT) and os.path.ismount(CAMERA_MOUNT):
            mounted = True
        else:
            mounted = not subprocess.call(['mount', CAMERA_MOUNT])
        return mounted
    else:
        return True

def get_camera_files():
    if DO_CAMERA:
        if USE_GPHOTO:
            old_cwd = os.getcwd()
            os.chdir('infiles')
            try:
                subprocess.check_call(['gphoto2', '--get-all-files'])
                subprocess.check_call(['gphoto2', '--delete-all-files', '--recurse'])
            finally:
                os.chdir(old_cwd)
        else:
            if os.path.exists(CAMERA_SRC):
                for src_file in os.listdir(CAMERA_SRC):
                    shutil.move(CAMERA_SRC + '/' + src_file, 'infiles/')

def umount_camera():
    if DO_CAMERA and not USE_GPHOTO:
        if os.path.exists(CAMERA_MOUNT) and os.path.ismount(CAMERA_MOUNT):
            umounted = not subprocess.call(['umount', CAMERA_MOUNT])
        else:
            umounted = True
        return umounted
    else:
        return True

def print_image(filename, copies=1):
    if DO_PRINT:
        success = not subprocess.call([
            'lp',
            '-d', PRINTER,
            '-o', 'media=a4',
            '-o', 'scaling=100',
            '-n', str(int(copies)), filename
        ])
        return success
    else:
        return True

def get_day():
    return time.strftime('%a', time.localtime())

def get_year():
    return time.strftime('%Y', time.localtime())

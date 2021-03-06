# vim: set fileencoding=utf-8 :
# Mount and print functions
import errno
import os
import re
import shutil
import subprocess
import time
import dotenv

dotenv.load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

def env_to_bool(value):
    return value.lower() in ['true', 't', 'yes', 'y']

CAMERA_MOUNT = os.environ.get('CAMERA_MOUNT')
CAMERA_SRC = os.environ.get('CAMERA_SRC')

PRINTER = os.environ.get('PRINTER')

DO_CAMERA = env_to_bool(os.environ.get('DO_CAMERA'))
DO_PRINT = env_to_bool(os.environ.get('DO_PRINT'))

SUPPORTED_FILES = re.compile('\\.jpe?g$', re.IGNORECASE)

def detect_gphoto():
    output = subprocess.check_output(['gphoto2', '--auto-detect'])
    return output.find('USB PTP Class Camera') != -1

USE_OR_DETECT_GPHOTO = os.environ.get('USE_GPHOTO').lower()
if USE_OR_DETECT_GPHOTO == 'detect':
    USE_GPHOTO = detect_gphoto()
else:
    USE_GPHOTO = env_to_bool(USE_OR_DETECT_GPHOTO)

class UnboundCallbackError(UnboundLocalError):
    """ Callback function not set error. """
    pass

class Logger(object):
    _callback = None

    def set_callback(self, callback=None):
        type(self)._callback = callback # pylint: disable=protected-access

    def log(self, message):
        if self._callback != None:
            self._callback(message) # pylint: disable=not-callable
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
            load_photos_from_path(CAMERA_SRC)

def load_photos_from_path(path):
    if os.path.exists(path):
        for entry in os.listdir(path):
            entry_path = os.path.join(path, entry)
            if os.path.isdir(entry_path):
                load_photos_from_path(entry_path)
            elif re.search(SUPPORTED_FILES, entry) is not None:
                shutil.move(entry_path, 'infiles')

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
    if not DO_PRINT:
        return True

    success = not subprocess.call([
        'lp',
        '-d', PRINTER,
        '-o', 'media=a4',
        '-o', 'scaling=100',
        '-n', str(int(copies)), filename
    ])
    return success

def get_day():
    return time.strftime('%a', time.localtime())

def get_year():
    return time.strftime('%Y', time.localtime())

def safe_filename(name):
    return re.sub('[^A-Za-z0-9-]', '_', name)

def mkdir_p(path, mode=0775):
    try:
        os.makedirs(path, mode)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

import subprocess
import sys
import os
import shutil
import tempfile
import ctypes


def main():
    command = sys.argv[3]
    args = sys.argv[4:]
    
    dir_path = tempfile.mkdtemp()
    shutil.copy2(command, dir_path)
    os.chroot(dir_path)
    
    libc = ctypes.cdll.LoadLibrary("libc.so.6")
    libc.unshare(0x20000000)
    
    command = os.path.join("/", os.path.basename(command))
    completed_process = subprocess.run([command, *args], capture_output=True)
    sys.stdout.buffer.write(completed_process.stdout)
    sys.stderr.buffer.write(completed_process.stderr)
    sys.exit(completed_process.returncode)


if __name__ == "__main__":
    main()

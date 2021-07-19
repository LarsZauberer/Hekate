import os
import shutil
import logging
from pathlib import Path
from rich.logging import RichHandler
from rich.progress import track


FORMAT = "%(message)s"
logging.basicConfig(
    level="INFO", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)

log = logging.getLogger()

log.info(f"Start Auto packaging")

if os.path.exists(Path("build")):
    log.info(f"Build Directory already exists -> Deleting it")
    try:
        shutil.rmtree(Path("build"))
    except Exception:
        log.exception(f"Error while removing build directory")
        exit(1)
    

# Execute setup.py
try:
    os.system("python setup.py build_apps")
except Exception:
    log.exception(f"Error in setup.py")
    exit(1)

try:
    files = [
        Path("config"),
        Path("data"),
        Path("effects"),
        Path("panda3d"),
        Path("rpcore"),
        Path("rplibs"),
        Path("rpplugins"),
    ]
    
    for i in track(files, description="Copying the packagingTemplate Directory"):
        shutil.copytree(Path("packagingTemplate") / i, Path("build") / i)
except Exception:
    log.exception(f"Error in copying packagingTemplate to build")
    exit(1)

try:
    shutil.copy(Path("packagingTemplate/install.flag"), Path("build/win_amd64"))
    shutil.copy(Path("packagingTemplate/use_cxx.flag"), Path("build/win_amd64"))
except PermissionError:
    log.warning(f"Couldn't copy flags due to permission error. Please move them manually to the win_amd64 folder. They are located in the packagingTemplate")
    shutil.copy(Path("packagingTemplate/install.flag"), Path("build"))
    shutil.copy(Path("packagingTemplate/use_cxx.flag"), Path("build"))
except Exception:
    log.exception(f"Error while copying flags")
    exit(1)

try:
    shutil.rmtree(Path("build/__whl_cache__"))
except Exception:
    log.exception(f"Error while removing __whl_cache__")

log.info(f"Successfully Finished packaging")

# Try opening the folder
try:
    import subprocess
    path = Path("build/win_amd64")
    subprocess.Popen(f'explorer /select, "{path}"')
except Exception:
    log.exception(f"Error opening the explorer")

import tempfile
import os

BASE_DIR = tempfile.mkdtemp()
PKG_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

__version__ = '0.1.108'

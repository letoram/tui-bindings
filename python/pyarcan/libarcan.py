import ctypes
import os

library_path = os.getenv('LIBACRAN_TUI_PATH', 'libarcan_tui.so')
libarcan_tui = ctypes.CDLL(library_path, use_errno=True)

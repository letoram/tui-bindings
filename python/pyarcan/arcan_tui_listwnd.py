import ctypes

from pyarcan.arcan_tui import TuiContext
from pyarcan.libarcan import libarcan_tui


class TuiListEntityAttributes:
    LIST_CHECKED = ctypes.c_uint8(1)
    LIST_HAS_SUB = ctypes.c_uint8(2)
    LIST_SEPARATOR = ctypes.c_uint8(4)
    LIST_PASSIVE = ctypes.c_uint8(8)
    LIST_LABEL = ctypes.c_uint8(16)
    LIST_HIDE = ctypes.c_uint8(32)


class TuiListEntry(ctypes.Structure):
    _fields_ = [
        ('label', ctypes.c_char_p),
        ('shortcut', ctypes.c_char_p),
        ('attributes', ctypes.c_uint8),
        ('indent', ctypes.c_uint8),
        ('tag', ctypes.c_void_p),
    ]


TuiListEntry_pointer = ctypes.POINTER(TuiListEntry)

arcan_tui_listwnd_setup = libarcan_tui.arcan_tui_listwnd_setup
arcan_tui_listwnd_setup.argtypes = [ctypes.POINTER(TuiContext),
                                    ctypes.POINTER(TuiListEntry),
                                    ctypes.c_size_t]
arcan_tui_listwnd_setup.restype = ctypes.c_bool


arcan_tui_listwnd_status = libarcan_tui.arcan_tui_listwnd_status
arcan_tui_listwnd_status.argtypes = [ctypes.POINTER(TuiContext),
                                     ctypes.POINTER(
                                        ctypes.POINTER(TuiListEntry)
                                     )]
arcan_tui_listwnd_status.restype = ctypes.c_bool

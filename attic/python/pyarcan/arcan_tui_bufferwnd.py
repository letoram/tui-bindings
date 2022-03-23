import ctypes

from pyarcan.arcan_tui import (
    TuiContext,
    TuiContext_pointer,
    TuiScreenAttr
)
from pyarcan.libarcan import libarcan_tui


class BufferwndDisplayModes:
    BUFFERWND_VIEW_ASCII = ctypes.c_int(0)
    BUFFERWND_VIEW_UTF8 = ctypes.c_int(1)
    BUFFERWND_VIEW_HEX = ctypes.c_int(2)
    BUFFERWND_VIEW_HEX_DETAIL = ctypes.c_int(3)


ATTR_LOOKUP_FN = ctypes.CFUNCTYPE(ctypes.c_void_p, TuiContext_pointer,
                                  ctypes.c_void_p, ctypes.c_uint8,
                                  ctypes.c_size_t,
                                  ctypes.POINTER(TuiScreenAttr))

COMMIT_WRITE_FN = ctypes.CFUNCTYPE(ctypes.c_bool, TuiContext_pointer,
                                   ctypes.c_void_p,
                                   ctypes.POINTER(ctypes.c_uint8),
                                   ctypes.c_size_t, ctypes.c_size_t)


class TuiBufferwndOpts(ctypes.Structure):
    _fields_ = [
        ('read_only', ctypes.c_bool),
        ('allow_exit', ctypes.c_bool),
        ('hide_cursor', ctypes.c_bool),
        ('view_mode', ctypes.c_int),
        ('wrap_mode', ctypes.c_int),
        ('color_mode', ctypes.c_int),
        ('custom_attr', ATTR_LOOKUP_FN),
        ('commit', COMMIT_WRITE_FN),
        ('cbtag', ctypes.c_void_p),
        ('offset', ctypes.c_uint64),
    ]


arcan_tui_bufferwnd_setup = libarcan_tui.arcan_tui_bufferwnd_setup
arcan_tui_bufferwnd_setup.argtypes = [TuiContext_pointer,
                                      ctypes.c_char_p,
                                      ctypes.c_size_t,
                                      ctypes.POINTER(TuiBufferwndOpts),
                                      ctypes.c_size_t]
arcan_tui_bufferwnd_setup.restype = ctypes.c_void_p

arcan_tui_bufferwnd_status = libarcan_tui.arcan_tui_bufferwnd_status
arcan_tui_bufferwnd_status.argtypes = [TuiContext_pointer]
arcan_tui_bufferwnd_status.restype = ctypes.c_int

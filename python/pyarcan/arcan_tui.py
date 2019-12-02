import ctypes

from pyarcan.libarcan import libarcan_tui


# Opaque pointer
class TuiConn(ctypes.Structure):
    pass


# Opaque pointer
class TuiContext(ctypes.Structure):
    pass


TuiContext_pointer = ctypes.POINTER(TuiContext)


# TODO: Opaque?
class ArcanIoevent(ctypes.Structure):
    pass


# TODO: Opaque?
class ShmifPixel(ctypes.Structure):
    pass


# TODO: Opaque?
class ShmifAsample(ctypes.Structure):
    pass


class _ForegroundColorComponents(ctypes.Structure):
    _fields_ = [
        ('fr', ctypes.c_uint8),
        ('fg', ctypes.c_uint8),
        ('fb', ctypes.c_uint8)
    ]


class _ForegroundColors(ctypes.Union):
    _anonymous_ = ('_fcc',)
    _fields_ = [
        ('fc', ctypes.c_uint8 * 3),
        ('_fcc', _ForegroundColorComponents),
    ]


class _BackgroundColorComponents(ctypes.Structure):
    _fields_ = [
        ('br', ctypes.c_uint8),
        ('bg', ctypes.c_uint8),
        ('bb', ctypes.c_uint8)
    ]


class _BackgroundColors(ctypes.Union):
    _anonymous_ = ('_bcc',)
    _fields_ = [
        ('bc', ctypes.c_uint8 * 3),
        ('_bcc', _BackgroundColorComponents),
    ]


class TuiScreenAttr(ctypes.Structure):
    _anonymous_ = ('_fc', '_bc')

    _fields_ = [
        ('_fc', _ForegroundColors),
        ('_bc', _BackgroundColors),
        ('bold', ctypes.c_uint),  # default: 1
        ('underline', ctypes.c_uint),  # default: 1
        ('italic', ctypes.c_uint),  # default: 1
        ('inverse', ctypes.c_uint),  # default: 1
        ('protect', ctypes.c_uint),  # default: 1
        ('blink', ctypes.c_uint),  # default: 1
        ('strikethrough', ctypes.c_uint),  # default: 1
        ('shape_break', ctypes.c_uint),  # default: 1
        ('custom_id', ctypes.c_uint8),
    ]


class TuiCell(ctypes.Structure):
    _fields_ = [
        ('attr', TuiScreenAttr),
        ('ch', ctypes.c_uint32),
        ('draw_ch', ctypes.c_uint32),
        ('real_x', ctypes.c_uint32),
        ('cell_w', ctypes.c_uint8),
        ('fstamp', ctypes.c_uint8),
    ]


class TuiProcessRes(ctypes.Structure):
    _fields_ = [
        ('ok', ctypes.c_uint32),
        ('bad', ctypes.c_uint32),
        ('errc', ctypes.c_int),
    ]


class TuiProcessErrc:
    TUI_ERRC_OK = 0
    TUI_ERRC_BAD_ARG = -1
    TUI_ERRC_BAD_FD = -2
    TUI_ERRC_BAD_CTX = -3


class TuiCbcfgHandlers:
    QUERY_LABEL = ctypes.CFUNCTYPE(ctypes.c_bool, TuiContext_pointer,
                                   ctypes.c_size_t, ctypes.c_char_p,
                                   ctypes.c_char_p, ctypes.c_void_p,
                                   ctypes.c_void_p)

    INPUT_LABEL = ctypes.CFUNCTYPE(ctypes.c_bool, TuiContext_pointer,
                                   ctypes.c_char_p, ctypes.c_bool,
                                   ctypes.c_void_p)

    INPUT_ALABEL = ctypes.CFUNCTYPE(ctypes.c_bool, TuiContext_pointer,
                                    ctypes.c_char_p,
                                    ctypes.POINTER(ctypes.c_int16),
                                    ctypes.c_size_t, ctypes.c_bool,
                                    ctypes.c_uint8, ctypes.c_void_p)

    INPUT_MOUSE_MOTION = ctypes.CFUNCTYPE(ctypes.c_void_p, TuiContext_pointer,
                                          ctypes.c_bool, ctypes.c_int,
                                          ctypes.c_int, ctypes.c_int,
                                          ctypes.c_void_p)

    INPUT_MOUSE_BUTTON = ctypes.CFUNCTYPE(ctypes.c_void_p, TuiContext_pointer,
                                          ctypes.c_int, ctypes.c_int,
                                          ctypes.c_int, ctypes.c_bool,
                                          ctypes.c_int, ctypes.c_void_p)

    INPUT_UTF8 = ctypes.CFUNCTYPE(ctypes.c_bool, TuiContext_pointer,
                                  ctypes.c_char_p, ctypes.c_size_t,
                                  ctypes.c_void_p)

    INPUT_KEY = ctypes.CFUNCTYPE(ctypes.c_void_p, TuiContext_pointer,
                                 ctypes.c_uint32, ctypes.c_uint8,
                                 ctypes.c_uint8, ctypes.c_uint8,
                                 ctypes.c_uint16, ctypes.c_void_p)

    INPUT_MISC = ctypes.CFUNCTYPE(ctypes.c_void_p, TuiContext_pointer,
                                  ctypes.POINTER(ArcanIoevent),
                                  ctypes.c_void_p)

    STATE = ctypes.CFUNCTYPE(ctypes.c_void_p, TuiContext_pointer,
                             ctypes.c_bool, ctypes.c_int, ctypes.c_void_p)

    BCHUNK = ctypes.CFUNCTYPE(ctypes.c_void_p, TuiContext_pointer,
                              ctypes.c_bool, ctypes.c_uint64, ctypes.c_int,
                              ctypes.c_void_p)

    VPASTE = ctypes.CFUNCTYPE(ctypes.c_void_p, TuiContext_pointer,
                              ctypes.POINTER(ShmifPixel), ctypes.c_size_t,
                              ctypes.c_size_t, ctypes.c_size_t,
                              ctypes.c_void_p)

    APASTE = ctypes.CFUNCTYPE(ctypes.c_void_p, TuiContext_pointer,
                              ctypes.POINTER(ShmifAsample), ctypes.c_size_t,
                              ctypes.c_size_t, ctypes.c_size_t,
                              ctypes.c_void_p)

    TICK = ctypes.CFUNCTYPE(ctypes.c_void_p, TuiContext_pointer,
                            ctypes.c_void_p)

    UTF8 = ctypes.CFUNCTYPE(ctypes.c_void_p, TuiContext_pointer,
                            ctypes.POINTER(ctypes.c_uint8), ctypes.c_size_t,
                            ctypes.c_bool, ctypes.c_void_p)

    RESIZED = ctypes.CFUNCTYPE(ctypes.c_void_p, TuiContext_pointer,
                               ctypes.c_size_t, ctypes.c_size_t,
                               ctypes.c_size_t, ctypes.c_size_t,
                               ctypes.c_void_p)

    RESET = ctypes.CFUNCTYPE(ctypes.c_void_p, TuiContext_pointer,
                             ctypes.c_int, ctypes.c_void_p)

    GEOHINT = ctypes.CFUNCTYPE(ctypes.c_void_p, TuiContext_pointer,
                               ctypes.c_float, ctypes.c_float, ctypes.c_float,
                               ctypes.c_char_p, ctypes.c_char_p,
                               ctypes.c_void_p)

    RECOLOR = ctypes.CFUNCTYPE(ctypes.c_void_p, TuiContext_pointer,
                               ctypes.c_void_p)

    SUBWINDOW = ctypes.CFUNCTYPE(ctypes.c_bool, TuiContext_pointer,
                                 ctypes.POINTER(TuiConn), ctypes.c_uint32,
                                 ctypes.c_uint8, ctypes.c_void_p)

    SUBSTITUTE = ctypes.CFUNCTYPE(ctypes.c_bool, TuiContext_pointer,
                                  ctypes.POINTER(TuiCell), ctypes.c_size_t,
                                  ctypes.c_size_t, ctypes.c_void_p)

    RESIZE = ctypes.CFUNCTYPE(ctypes.c_void_p, TuiContext_pointer,
                              ctypes.c_size_t, ctypes.c_size_t,
                              ctypes.c_size_t, ctypes.c_size_t,
                              ctypes.c_void_p)

    VISIBILITY = ctypes.CFUNCTYPE(ctypes.c_void_p, TuiContext_pointer,
                                  ctypes.c_bool, ctypes.c_bool,
                                  ctypes.c_void_p)

    EXEC_STATE = ctypes.CFUNCTYPE(ctypes.c_void_p, TuiContext_pointer,
                                  ctypes.c_int, ctypes.c_void_p)


class TuiCbcfg(ctypes.Structure):
    _fields_ = [
        ('tag', ctypes.c_void_p),
        ('query_label', TuiCbcfgHandlers.QUERY_LABEL),
        ('input_label', TuiCbcfgHandlers.INPUT_LABEL),
        ('input_alabel', TuiCbcfgHandlers.INPUT_ALABEL),
        ('input_mouse_motion', TuiCbcfgHandlers.INPUT_MOUSE_MOTION),
        ('input_mouse_button', TuiCbcfgHandlers.INPUT_MOUSE_BUTTON),
        ('input_utf8', TuiCbcfgHandlers.INPUT_UTF8),
        ('input_key', TuiCbcfgHandlers.INPUT_KEY),
        ('input_misc', TuiCbcfgHandlers.INPUT_MISC),
        ('state', TuiCbcfgHandlers.STATE),
        ('bchunk', TuiCbcfgHandlers.BCHUNK),
        ('vpaste', TuiCbcfgHandlers.VPASTE),
        ('apaste', TuiCbcfgHandlers.APASTE),
        ('tick', TuiCbcfgHandlers.TICK),
        ('utf8', TuiCbcfgHandlers.UTF8),
        ('resized', TuiCbcfgHandlers.RESIZED),
        ('reset', TuiCbcfgHandlers.RESET),
        ('geohint', TuiCbcfgHandlers.GEOHINT),
        ('recolor', TuiCbcfgHandlers.RECOLOR),
        ('subwindow', TuiCbcfgHandlers.SUBWINDOW),
        ('substitute', TuiCbcfgHandlers.SUBSTITUTE),
        ('resize', TuiCbcfgHandlers.RESIZE),
        ('visibility', TuiCbcfgHandlers.VISIBILITY),
        ('exec_state', TuiCbcfgHandlers.EXEC_STATE),

    ]


arcan_tui_open_display = libarcan_tui.arcan_tui_open_display
arcan_tui_open_display.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
arcan_tui_open_display.restype = ctypes.POINTER(TuiConn)

arcan_tui_setup = libarcan_tui.arcan_tui_setup
arcan_tui_setup.argtypes = [ctypes.POINTER(TuiConn), ctypes.c_void_p,
                            ctypes.POINTER(TuiCbcfg), ctypes.c_size_t]
arcan_tui_setup.restype = ctypes.POINTER(TuiContext)

arcan_tui_process = libarcan_tui.arcan_tui_process
arcan_tui_process.argtypes = [ctypes.POINTER(ctypes.POINTER(TuiContext)),
                              ctypes.c_int, ctypes.c_void_p, ctypes.c_int,
                              ctypes.c_int]
arcan_tui_process.restype = TuiProcessRes

arcan_tui_refresh = libarcan_tui.arcan_tui_refresh
arcan_tui_refresh.argtypes = [TuiContext_pointer]
arcan_tui_refresh.restype = ctypes.c_int

arcan_tui_writeu8 = libarcan_tui.arcan_tui_writeu8
arcan_tui_writeu8.argtypes = [TuiContext_pointer, ctypes.c_char_p,
                              ctypes.c_size_t, ctypes.c_void_p]
arcan_tui_writeu8.restype = ctypes.c_int

arcan_tui_erase_screen = libarcan_tui.arcan_tui_erase_screen
arcan_tui_erase_screen.argtypes = [TuiContext_pointer, ctypes.c_bool]
arcan_tui_erase_screen.restype = ctypes.c_int

arcan_tui_move_line_home = libarcan_tui.arcan_tui_move_line_home
arcan_tui_move_line_home.argtypes = [TuiContext_pointer]
arcan_tui_move_line_home.restype = ctypes.c_int

arcan_tui_destroy = libarcan_tui.arcan_tui_destroy
arcan_tui_destroy.argtypes = [TuiContext_pointer, ctypes.c_void_p]
arcan_tui_destroy.restype = ctypes.c_int

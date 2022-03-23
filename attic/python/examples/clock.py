import ctypes
import datetime
import errno
import time

from pyarcan import arcan_tui


def query_label(*args):
    print('query_label', args)


def input_label(*args):
    print('input_label', args)


def input_alabel(*args):
    print('input_alabel', args)


def input_mouse_motion(*args):
    print('input_mouse_motion', args)


def input_mouse_button(*args):
    print('input_mouse_button', args)


def input_utf8(*args):
    print('input_utf8', args)


def input_key(*args):
    print('input_key', args)


def input_misc(*args):
    print('input_misc', args)


def state(*args):
    print('state', args)


def bchunk(*args):
    print('bchunk', args)


def vpaste(*args):
    print('vpaste', args)


def apaste(*args):
    print('apaste', args)


def tick(*args):
    print('tick', args)


def utf8(*args):
    print('utf8', args)


def resized(*args):
    print('resized', args)


def reset(*args):
    print('reset', args)


def geohint(*args):
    print('geohint', args)


def recolor(*args):
    print('recolor', args)


def subwindow(*args):
    print('subwindow', args)


def substitute(*args):
    print('substitute', args)


def resize(*args):
    print('resize', args)


def visibility(*args):
    print('visibility', args)


def exec_state(*args):
    print('exec_state', args)


handlers = {
    'query_label': arcan_tui.TuiCbcfgHandlers.QUERY_LABEL(query_label),
    'input_label': arcan_tui.TuiCbcfgHandlers.INPUT_LABEL(input_label),
    'input_alabel': arcan_tui.TuiCbcfgHandlers.INPUT_ALABEL(input_alabel),
    'input_mouse_motion': arcan_tui.TuiCbcfgHandlers.INPUT_MOUSE_MOTION(
        input_mouse_motion),
    'input_mouse_button': arcan_tui.TuiCbcfgHandlers.INPUT_MOUSE_BUTTON(
        input_mouse_button),
    'input_utf8': arcan_tui.TuiCbcfgHandlers.INPUT_UTF8(input_utf8),
    'input_key': arcan_tui.TuiCbcfgHandlers.INPUT_KEY(input_key),
    'input_misc': arcan_tui.TuiCbcfgHandlers.INPUT_MISC(input_misc),
    'state': arcan_tui.TuiCbcfgHandlers.STATE(state),
    'bchunk': arcan_tui.TuiCbcfgHandlers.BCHUNK(bchunk),
    'vpaste': arcan_tui.TuiCbcfgHandlers.VPASTE(vpaste),
    'apaste': arcan_tui.TuiCbcfgHandlers.APASTE(apaste),
    'tick': arcan_tui.TuiCbcfgHandlers.TICK(tick),
    'utf8': arcan_tui.TuiCbcfgHandlers.UTF8(utf8),
    'resized': arcan_tui.TuiCbcfgHandlers.RESIZED(resized),
    'reset': arcan_tui.TuiCbcfgHandlers.RESET(reset),
    'geohint': arcan_tui.TuiCbcfgHandlers.GEOHINT(geohint),
    'recolor': arcan_tui.TuiCbcfgHandlers.RECOLOR(recolor),
    'subwindow': arcan_tui.TuiCbcfgHandlers.SUBWINDOW(subwindow),
    'substitute': arcan_tui.TuiCbcfgHandlers.SUBSTITUTE(substitute),
    'resize': arcan_tui.TuiCbcfgHandlers.RESIZE(resize),
    'visibility': arcan_tui.TuiCbcfgHandlers.VISIBILITY(visibility),
    'exec_state': arcan_tui.TuiCbcfgHandlers.EXEC_STATE(exec_state),
}
    

connection = arcan_tui.arcan_tui_open_display('Clock'.encode(), ''.encode())
config = arcan_tui.TuiCbcfg(**handlers)
context = arcan_tui.arcan_tui_setup(connection, None, ctypes.byref(config),
                                    ctypes.sizeof(config))

if not context:
    print('failed to setup TUI connection')
    exit(1)

# &context
context_address = arcan_tui.TuiContext_pointer.from_address(
    ctypes.addressof(context)
)

while True:
    res = arcan_tui.arcan_tui_process(context_address, 1, None, 0, -1)

    if res.errc == arcan_tui.TuiProcessErrc.TUI_ERRC_OK:
        if -1 == arcan_tui.arcan_tui_refresh(context) and \
                ctypes.get_errno() == errno.EINVAL:
            break
    else:
        break

    arcan_tui.arcan_tui_erase_screen(context, False)
    arcan_tui.arcan_tui_move_line_home(context)

    now = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S").encode()

    arcan_tui.arcan_tui_writeu8(context, now, len(now), None)

    time.sleep(1)


arcan_tui.arcan_tui_destroy(context, None)

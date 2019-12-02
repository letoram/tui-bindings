import ctypes
import errno

from pyarcan import arcan_tui
from pyarcan import arcan_tui_bufferwnd

connection = arcan_tui.arcan_tui_open_display('Bufferwnd'.encode(),
                                              ''.encode())
config = arcan_tui.TuiCbcfg()
context = arcan_tui.arcan_tui_setup(connection, None, ctypes.byref(config),
                                    ctypes.sizeof(config))

if not context:
    print('failed to setup TUI connection')
    exit(1)

# &context
context_address = arcan_tui.TuiContext_pointer.from_address(
    ctypes.addressof(context)
)

tui_bufferwnd_opts = arcan_tui_bufferwnd.TuiBufferwndOpts(
    read_only=False,
    view_mode=arcan_tui_bufferwnd.BufferwndDisplayModes.BUFFERWND_VIEW_HEX_DETAIL
)

text_buffer = "There once was this\n weird little test case that we wondered" \
              "\n to see if it could be used to \r\n show with the help of" \
              " my little friend".encode()

arcan_tui_bufferwnd.arcan_tui_bufferwnd_setup(
    context, text_buffer,
    len(text_buffer),
    ctypes.byref(tui_bufferwnd_opts),
    ctypes.sizeof(tui_bufferwnd_opts)
)

while True:
    res = arcan_tui.arcan_tui_process(context_address, 1, None, 0, -1)

    if res.errc == arcan_tui.TuiProcessErrc.TUI_ERRC_OK:
        if -1 == arcan_tui.arcan_tui_refresh(context) and \
                ctypes.get_errno() == errno.EINVAL:
            break
    else:
        break

arcan_tui.arcan_tui_destroy(context, None)

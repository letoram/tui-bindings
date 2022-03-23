import ctypes
import errno

from pyarcan import arcan_tui
from pyarcan import arcan_tui_listwnd

connection = arcan_tui.arcan_tui_open_display('Listwnd'.encode(), ''.encode())
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

entries = (arcan_tui_listwnd.TuiListEntry * 4)()

entries[0].label = b'hi'
entries[0].attributes = arcan_tui_listwnd.TuiListEntityAttributes.LIST_CHECKED
entries[0].tag = 0

entries[1].label = b'there'
entries[1].attributes = arcan_tui_listwnd.TuiListEntityAttributes.LIST_PASSIVE
entries[1].shortcut = b't'
entries[1].tag = 1

entries[2].attributes = arcan_tui_listwnd.TuiListEntityAttributes.\
    LIST_SEPARATOR

entries[3].label = b'lolita'
entries[3].attributes = arcan_tui_listwnd.TuiListEntityAttributes.LIST_HAS_SUB
entries[3].shortcut = b'l'
entries[3].tag = 2

arcan_tui_listwnd.arcan_tui_listwnd_setup(context, entries, 4)

while True:
    res = arcan_tui.arcan_tui_process(context_address, 1, None, 0, -1)

    if res.errc == arcan_tui.TuiProcessErrc.TUI_ERRC_OK:
        if -1 == arcan_tui.arcan_tui_refresh(context) and \
                ctypes.get_errno() == errno.EINVAL:
            break
    else:
        break

    picked = arcan_tui_listwnd.TuiListEntry_pointer()
    # &picked
    picked_address = arcan_tui_listwnd.TuiListEntry_pointer.from_address(
        ctypes.addressof(picked)
    )

    if arcan_tui_listwnd.arcan_tui_listwnd_status(context, picked_address):
        if picked:
            print('User picked: {}'.format(picked.contents.label))
        else:
            print('User cancelled')

        break


arcan_tui.arcan_tui_destroy(context, None)


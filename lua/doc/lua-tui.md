# Arcan-TUI - Lua API

# Introduction

These bindings expose the Arcan TUI API for creating text oriented
user-interfaces. They are provided as normal Lua-Rocks compatible modules for
Lua 5.1 and above.

See the 'examples' folder for documented examples on the available features
and their recommended use.

A note of caution while exploring the API, always make sure to check if
something is expressed in rows and columns or as x, y positions on the grid.
Typically positions are expressed as x,y coordinates while as dimensions are
expressed through rows and columns.

# Setting up a connection

You create a new connection with the following function:

    tui = require('arcantui')
    wnd = tui:open(title_string, identity_string, (option_table))

The title string is the immutable title of your application, while-as the
identity string can reflect some dynamic state, e.g. the name of a file being
edited, the current path for a shell and so on.

When the function call returns, you either have a connection represented by the
context table, or nil as an indication of failure.

The (option\_table) carries additional configuration for how the window is
supposed to behave. The main key in that table should be 'handlers' with the
event handlers that the context should have currently. These can be swapped out
via a call to 'set\_handlers', and intercepted/overloaded by high-level
widgets.

The API is almost exclusively event-driven, the handler table supports a number
of entry points you can match to functions. The simplest pattern is thus:

    wnd = tui:open("hi", "there")
    while wnd:process() do
      wnd:refresh()
    end

Process will flush event queues and run handlers for all contexts tied to a
primary one (your connection), while refresh will only synch changes to the
canvas for each context it is invoked on. The reason for the split is that
there is likely other actions you might want to take, e.g. processing data from
an external source, that would affect the current output.

The reason for the 'reverse' refresh order here is to safeguard against event
handlers that would :close a context in response to the user closing a window
or a window becoming useless (completion popups and so on), and remove any
existing tracking references (e.g. table.remove(tbl, context\_index).

If the identity part has changed, due to the program opening some document
or external connection or something else that would distinguish it from other
instances of the same program, this can be updated with:

    context:update_identity("myfile.pdf")

The acccepted prototypes for the process method looks like this:

    process(ctx) => bool
    process(ctx, timeout) => bool

If process ever returns 'false' it implies that the connection has died for
some user- or server- initiated reason. If there are any subwindows mapped
to the context (see the _subwindows_ section further below), those too will
be covered by the process call.

This function acts very much like a poll, and if there is data on the
connection itself, it is flushed into the event-loop. For each matching event
that is triggered, the corresponding callback in the handler table is
activated. These handlers covers information about the screen size changing,
updates to the color palette, user input and so on. The added poll behavior is
to allow multiplexing without exposing connection mechanism, and cover the
common usecase of reacting to some externally driven data flow, interpreting
and presenting it interactively without forcing in additional dependencies.

When finished working with a context, you deallocate it by calling the method
_close_ which takes an optional "last\_words" string that may tell the user
*why* you decided to close. This is to communicate an error, in a normal path
it should be left empty.

## Context Flags

There are some generic window controls that are provided as flags that can be
changed with `wnd:set_flags(val1, val2, ...)` where the possible values are
defined in the table provided in tui.flags.

The supported flags are:

    auto_wrap   - writes across the edge of the window will wrap to the start of
                  the next row

    mouse       - mouse input will be forwarded to the input handler and ignore
                  the default click-drag to select

    mouse_full  - like 'mouse' but the user cannot override the mouse input by
                  holding a modifier button

    hide_cursor - prevents drawing the cursor

# Drawing

Drawing in the TUI API means picking 'attributes' one or several unicode
characters (utf8) and writing them to a location.

    mycontext:dimensions() => w, h

Drawing is targetting a currently active output abstract screen. The abstract
screen is a grid of cells that carry a character and optional formatting
attributes. The screen has a cursor, which is the current position output will
be written to unless the draw call used explicitly manipulates the cursor.

    write
    write_to
    erase
    erase_region

For any drawing, positioning and sizing operation - make special note if the
source call specifies an x,y position coordinate with 0,0 origo in the upper
left corner, or if it specifies in rows, cols. This is a very common pitfall.

## Specialized Attributes

When writing into a cell, both the data (character) and the formatting
attributes will be added to the contents of a cell. The attributes can be
specified explicitly or implicitly by setting a default attribute.

The default attribute can be set and retreived via:

    wnd:set_default(attrtbl) => attrtbl

The attrtbl argument can be constructed via the global function:

    tui:get_attribute(tui_attr(optional:context, optional:table) => attrtbl

If provided, the context argument _must_ point to a context retrieved from
tui\_open and will take its properties from the defaults in that context.
The accepted fields in \_table\_ are as follows:

    bold : bool
    underline : bool
    inverse : bool
    protect : bool
    strikethrough : bool
    fr : integer (0..255)
    fg : integer (0..255)
    fb : integer (0..255)
    br : integer (0..255)
    bg : integer (0..255)
    bb : integer (0..255)
    id : integer
    fg_id : integer
    bg_id : integer
    shape_break : integer

All of these, except for id and shape\_break, directly control the text drawing
routine. Id is a custom number tag that can be used to associate with
application specific metadata, as a way of mapping to more complex types.

If the color\_id field is set, it is expected to use a value from the builtin
table 'colors'.

Shape break is used to control text hinting engines for non-monospace
rendering. Though this goes against the traditional cell-grid structure, it is
useful for internationalisation and for ligature substitutions (where a
specific sequence of characters may map to an entirely different representation
and you want subsequent cells to break word or other group selections. For
shaped rendering, this might also cause realignment to the grid.

## Colors

There is an event handler with the name 'recolor' which provides no arguments.
When activated, this indicates that the desired palette has changed.

If you have been using the 'color\_id' method when setting cell attributes, you
can ignore this handler. If you use custom colors however, you will want to
pick colors that match the primary, secondary, background colors.

The possible values for index are provided in the global lookup table
'colors' and are thus accessed like:

    attrtbl.fr, attrtbl.fg, attrtbl.fb = get_color(tui_color.label)
    attrtbl.br, attrtbl.bg, attrtbl.bb = get_color(tui_color.background)
    set_default_attr(attrtbl)

The available semantic labels in the module-global tui\_color table are:

    text       - expected color for generic 'text'
    background - expected color to match text background
    highlight  - color to use for dynamic emphasis rather than bold attribute
    label      - color to indicate some non-modifiable UI element or hint
    inactive   - color to indicate an element that might be interactive normally
                 but is for some reason not active or used
    warning    - color to indicate some subtle danger
    error      - color to indicate something that is dangerous or broken
    alert      - color to indicate something that needs immediate attention
    primary    - primary color for normal output, can be used to pick matching
                 schemes.
    secondary  - secondary to indicate a separate group from normal test.
    cursor     - the currently set color of the cursor, this is handled internally
    altcursor  - the currently set color in alt- scrolling mode, this is handled
                 internally
    reference  - navigation links and data references
    ui         - user-interface elements like statusbars

Note that it is your responsibility to update on recolor events, the backend
does not track the semantic label associated with some cell. This is one of the
reasons you have access to a custom-set id as cell attribute.

After 'ui', the legacy ansi color palette starts.

## Cursor Control

The following functions are used to explicitly control the cursor position:

    cursor_to(x, y)
    cursor_tab(dt)
    cursor_step_col(dx)
    cursor_step_row(dy)

The cursor position is also automatically incremented with write calls relative
to the number of cells consumed and based on the state the screen is currently
in.

## Scrolling

If there is more content than what can be shown on the screen, it is recommended
that you provide controls for seeking and for indicating roughly how much content
there is. This allows the lower layers of the stack to provide decorations that
fit user preferences and needs.

In order for this feature to be enabled, you need to continously provide
information about content state as it changes.

    wnd:content_size(ofs_row, tot_row, [ofs_col], [tot_col])

Where the 'ofs' specifies the number of rows and columns that come before the
current window.

There are two event handlers:

    seek_absolute(n) - 0 <= n <= 1
    seek_relative(row, col)

The absolute form requests that the contents is scrolled to start at 'n'
percent completion, with 0 indiciating the beginning of all contents and 1
at the end (subtracting the number of rows that fits the screen size).

The relative form requests that the window is panned +- rows and +- cols.

## Screen Resizing

It is not uncommon for an outer display system to communicate that the current
output dimensions have changed for whatever reason. When that occurs, the
contents of the current screen is invalidate entirely in a screen that is in
alternate mode, while populated with contents from the scrollback buffer in
normal mode.

You are always expected to be able to handle any non-negative, non-zero amount
of rows and columns.

# Subwindows

While it is entirely possible to open additional tui connections that will act
independent of eachother, it is also possible to create special subconnections
that operate under slightly different circumstances.

These requests are asynchronous as they require feedback from the outer display
system which can take a lot of time. To create a subwindow, you first need to
have an event handler for the _subwindow_ event.

Then you can use the following function to request a new window to be created:

    new_window(optional:type) => bool

Where type is one of (default) "tui", "popup", "handover". It returns true or
false depending on the number of permitted subwindows and pending requests.

When a subwindow has arrived, the special event handler "subwindow" is called
with its first argument being either nil or a new context that reflects the
subwindow to be used.

## Force-Push

There is also the chance that the outer server can decide and push a window
without a pending request in beforehand as a means of requesting/negotiating
capability. There are two cases where this is relevant.

1. Accessibility - If you receive a subwindow with the type 'accessibility' it
   is an indication that the user wants data provided here in a linear and
   text-to-speech accessible form. Lines that are written on this subwindow
   will be forwarded in order. You can think of it more of a streaming output
   device with low bandwidth than as a 'screen' as such.

2. Debug - This window requests a debug representation of the contents of the
   context it is pushed into. This encourages a separation between 'error'
   outputs and 'debug' outputs and tries to deal away with command-line debug
   arguments to try and squeeze more information out of your program.

## Tui subwindow

This act as just another window, but with its life-span, processing and refresh
cycle tied to that of its parent and thus needs no extra work for multiplexing.

It also gets another hinting feature,

    spatial_hint(direction)

where direction is one of the 8 corners (n, nw, w, sw, s, se, e, ne) and is a
hint to the outer window management system (if any) that relative window
positioning should be biased in that direction.

## Popup subwindow

The "popup" subwindow is a more common occurence where you want to show some
direct- feedback visuals related to the current menu, either with input focus
or without. When mapped, you get access to another context function:

    anchor(x, y, ref_y, input_grab)

This hints that the popup should be anchored to cell @ x, y and
sized/positioned so that it does not occlude the content row at ref\_y.

## Handover subwindow

The "handover" subwindow type is special and is used to create a connection to
the display system that has a trust relationship to the requester, but the
actual behavior is outside the scope and definition of this API. The primary
purpose is to be able to write a TUI application that act as a shell that need
to spawn a detachable process.

# Shutting Down

A window can be closed by invoking the close([msg]) method on the window, where
[msg], if set, will convey some user-presentable error message explaining the
reason for termination and should only be used as part of error handling.

Closing the root window will also cause any subwindows to terminate.

# Input

A lot of the work involved is retrieving and reacting to inputs from the user.
The following input event handlers are present:

    utf8 (string)  : bool
    key            : (subid, keysym, scancode, modifiers)
    mouse_motion   : (relative, x, y, modifiers)
    mouse_button   : (subid, x, y, modifiers)
    label(string)  : bool
    query_label()  : bool

Some of these act as a chain with an early out and flow from a high-level of
abstraction to a low one. Your handler is expected to return 'true' if the event
was consumed and further processing should be terminated.

Note that key events are not treated with a rising/falling edge for keyboard
input, repeats/ on-release triggers have been deliberately excluded from this
model.

For text input, the most relevant is 'utf8' which implies that the a single
unicode codepoint has been provided in a utf8 encoded string and you likely
always want to handle this event.

For all the event handlers where there is a modifiers argument supplied, you
have access to both a global tuimods(modifiers) function that gives you a
textual representation of the active set of modifiers when the event was
triggered.

## Symbols

For working with raw key inputs, you have a number of options in the key event
handler, but the most important is likely the subid and the modifiers combined.

The module-global table 'keys' has a bidirectional mapping between symbol
names (keysym) and their numeric form, e.g. tui.keys.F1.

## Labels

As a response to a change in language settings or at the initial startup, the
'query\_label' handler will be invoked. A label is a string tag that takes
priority over other forms of inputs, and comes with a user targeted short
description about its use, along with information about its suggested default
symbol and modifier binding. This is provided as a means of making the physical
inputs more discoverable, letting the outer display system provide options for
binding, override and visual feedback.

When this callback is invoked, you are expected to return 0 or 4 values though
the pattern can be condensed like this:

    local mybindings = {
    -- other supported languages like this
      swe = {
        {'SOME_LABEL', 'Beskrivning till anvandaren', TUIK_A, TUIM_CTRL}
      }

    -- and default (english)
      {'SOME_LABEL', 'Description for the user', TUIK_A, TUIM_CTRL}
    }

    function myhandler(ctx, displang, index)
      btbl = mybindings[displang] and mybindings[displang] or mybindings
        if (mybindings[index]) then
            return table.unpack(mybindings[index])
        end
    end

This covers communicating all available bindings for the requested language,
which is also a hint as to the output language.

## Mouse Controls

By default, the inner implementation of TUI takes care of mouse input and uses
it to manage select-to-copy and scrolling without any intervention. You can
disable this behavior and receive mouse input yourself by:

    wnd:set_flags(tui.flags.mouse)

When set, the corresponding mouse\_motion and mouse\_button events will be
delivered to your set of event handlers. The extended flags, mouse\_full blocks
the user from holding a modifier to access the builtin screen
selection/clipboard action completely.

# Data Transfers

Another part of expected application behavior is to deal with anciliary data
transfers, where the more common one is the clipboard. There are also 'bchunk'
(blog data transfers) and state which is a contract where the client should
be able to export/import current settings so the user can resume previous work.

## State-in/State-out

A feature addition that has not been part of traditional TUI API designs is
that we explicitly provide a serialization helper. This is activated by first
providing a serialization state size estimate, where the upper bounds may be
enforced by the outer display system.

    mycontext:state_size(4096)

The outer display system is then free, at any time, to provide an event to a
state\_in event handler or a state\_out event handler, expecting you to
pack/unpack enough state to be able to revert to an earlier state.

Implementing this properly unlocks a number of desired features, e.g. device
mobility, crash recovery, data mobility and so on. For how to deal with the
data in a state\_in/out handler, see bchunk below.

You can also disable the feature after enabling it by setting the size to 0.

## Clipboard

Though technically these can be seen as inputs, the special relationship is
that they are used for larger block- or streaming- transfers.

Three event handlers deal with clipboard contents. Those are:

1. paste(str) - a string with utf8- encoded text contents.
2. vpaste(vh) - a pixel buffer transfer - [special]
3. apaste(ah) - an audio buffer transfer - [special]
4. bchunk(bh) - a generic binary blob transfer

Where the most common one, paste, is similar to a bounded set of utf8 inputs.

## Bchunk

Bchunk or 'blob' transfers,  come as a generic 'here is a stream of bytes,
do something with it', possible as a response to an announcement that your
application understands a certain extension pattern:

    mycontext:announce_io("png;bmp", "png")

This would tell the other end that this context support arbitrary opening
'png' and 'bmp' files, and saving to 'png' ones. The user can invoke this
via any implementation defined means exist on their end.

    mycontext:request_io(nil, "*")

This would tell the other end that we would really like the user to be queried
for something to store with any kind of type. This is still not guaranteed to
be honored.

This assumes that you also provide an bchunk\_in, bchunk\_out handler.
Both of these have the prototype:

    bchunk_in(self, blob, id)

The blob is a user-data that can be used in a few ways. Internally it
encapsulates a file descriptor wrapped around some buffering. For input,
you can use 'data\_handler' to assign a callback that will receive buffers
as they arrive. This is handled as part of the 'process' call.

For bchunk\_out the 'data\_handler' can also take a string buffer itself,
and sending / closing / management will be handled internally entirely.

These methods are preferred they are asynchronous and non-blocking, though it
is also possible to call read/write directly as part if the normal processing.

For more information on blobio, see 'binary IO' further below.

# System

The last category is about other system integration related features, that only
indirectly contribute to the content that is to be presented. Some of these
functions are not strictly part of arcan-tui but rather added to not avoid
heavier dependencies (e.g. luaposix) but still be able to write something like
a command-line shell or terminal emulator. These functions are covered in the
system integration section further below.

There are a few calls that can be used directly to communicate that some event
has occured. These are:

    alert(msg), notification(msg), failure(msg).

The effect of these depend on the outer windowing system, and the message
provided is expected to match the currently set geohint locale - if possible.

There are also a number of system- class events that can be delivered to a
window itself.

## Reset

The event handler named 'reset(level)' indicates that the user, directly or
indirectly, wants the application to revert to some program- defined initial
state, where the level of severity (number argument) goes from:

0. User-initated, soft.
1. User-initated, hard.
2. Crash-recovery, wm- state lost.
3. Crash-recovery, system-state lost.

The third level is also used if the underlying display system has been remapped
to some other device, local or non-local. The normal tactic is to trigger
whatever 'redraw from clean slate' function you might have, as well as to re-
announce any supported input/output formats.

You can also call 'reset' on a context, but this has the effect of undoing other
hints on bchunk, state and input\_labels.

## Visibility

The 'visibility' event handler is triggered whenever the window it is associated
with changed visibility or focus state. The prototype is:

    visibility(self, visible, focused)

This information is intended to influence polling and rendering behaviour for
clients where this information can be costly to produce.

## Geohint

The 'geohint' event handler is triggered when information about position and
local has been provided and changed. This is to allow ISO-3166-1/ISO-639-2
style information coupled with GPS coordinates to influence localisation.

The prototype is:

    geohint(self, country, language, lat, long, elev)

## Exec-State

The 'exec\_state' event handler indicates if the context is changing from
'normal' to being suspended or 'terminating'. The later is mainly important for
subwindows where a window might be destroyed, but others keep on living.

The protype is:

    exec_state(self, state)

With 'state' being 'suspend', 'resume', 'shutdown'.

The suspend state is an indicator that calls to refresh and similar ones will
be a waste of time until the next exec-state call has indicated that normal
operations will resume. This is provided to allow timing sensitive network
protocols to clean up and save enough state that a connection can be resumed at
a later time.

## Timers

There is a coarse grained timer that is enabled if you implement the 'tick'
handler in your table. It has low resolution and low accuracy (~25Hz) and is
meant for low maintenance periodic tasks, e.g. driving a data backup timer
or 'blink' like UI state.

# Widgets

Some basic building blocks are also provided as widgets. The generic pattern
behind them is that they act as modal state changes on a window, e.g.

    wnd:readline(function(self, line) print(line); end)

This would change the context to a readline state, and call the provided
callback function when completed. This will temporarily alter the state of the
handler table for the window, and revert back when completed. This means that
your normal processing will be blocked until the user signals completion or,
for some widgets, until you explicitly ask it to stop.

Not all events are necessarily blocked while in this state, the actual set
depends on which widget is being used. Trying to activate a new or same widget
while already in a widget state is a terminal state transition -- you either
first need to wnd:revert() it back to a regular window, or wait for the
widget's closure to run.

## Readline

The purpose of readline is to provide the user with all the support needed to
query for one or several lines of input. This includes editing, completion,
validation, history, quick-keys and so on.

To set it up, you simply call readline on the window in question:

    local ref = wnd:readline(closure, [options])

The closure callback will be invoked when readline is finished and provides
the added string.

There is a lot of options that can be added to readline on the other hand.

The calls that are permitted on the returned reference table are:

   ref:set_prompt(messagetbl)

Messagetbl is an n-indexed table where each entry can be either an attrtbl
signifying a change in attribute used, or a string of characters that the
previous attrtbl applies to:

   ref:set_prompt({"hi ", tui:attr({bold = true}), "there >"})

would write "hi there >" with **there** being in bold.

It is also possible to provide a completion history that the user can step
through:

  ref:set_history({"hi", "there", "you"})

It is up to the caller to track/update history in order to not mix history
domains/buffers between calls, or keep/leak sensitive information. Readline
will index and scan this history, but will maintain a reference rather than a
copy for performance reasons. If you modify the table, do call set\_history
again in order to not corrupt possible indexes and search trees.

The prototype for closure is:

   (self, resstr)

with resstr being the final user provided input, or nil if readline was
cancelled. You can also manually cancel readline by:

    wnd:revert()

This widget forwards _all_ events to the established event handler, but will
draw itself over existing content on refresh.

The widget accepts a whole lot of options that change its behaviour or is used
to query dynamic feedback. The properties in the options table can be:

    int rows (1)            : number of grid rows that will be used to draw.
    int margin_left (0)     : number of cells to pad from the left.
    int margin_right (0)    : number of cells to pad from the right.
    bool cancellable (true) : if the user is allowed to cancel input or not.
    string mask_character   : a single copdepoint that will mask input (for password entry)
    bool multiline (false)  : if linefeed should act as completing readline.
    int anchor_row (0)      : offset from top (>=0) or bottom (<0) where the contents will be drawn.
    bool tab_input          : is the tab key/character permitted or used for completion.

There are also a number of callbacks that are used to provide context information
and feedback (if provided):

autocomplete(self, str) => str or nil is used to provide a single complete
result that the user can commit to. This is used for the case where, based on
msg, there is a desired outcome and will be drawn in the user prompt.

suggest(self, str) => strtbl or nil is used to provide a tab-completion like
set of possible inputs to step from and possibly pick, this might draw outside
the normal anchor, or spawn a popup depending on window management preferences.

verify(self, str) => or offset, msgstr is used to indicate that the current
string is lacking in some way, e.g. can't be parsed because some content
constraint. If a message is returned, it might be presented to the user as a
hint to why the input currently fails.

filter(self, ch, len) => true or false, used to determine if 'ch' is permitted to
be added to the current input buffer based on what it is or the current length of
the string.

## Listwnd

## Bufferwnd

# System Integration

This section covers functions that are not strictly arcan-tui but added to make
necessary system integration features less painful when it comes to I/O,
process creation and so on. These are still namespaced within the tui window,
and piggyback on window resource management and processing.

## IO / Process execution

The TUI bindings shares non-blocking I/O implementation with open\_nonblock in
Arcan with a few changes. One is that the blob userdata is created from calling
open on a tui window context. This will tie the life-cycle to the root of that
window, and asynchronous processing will be mixed in with the window
:processing() multiplexation stage.

There are multiple ways of initiating this:

    local blobio = root:fopen("myfile", "w")

Would create/open myfile for writing, which can then be called with read() and
write() depending on the mode. When there is a lot of data to read, the
source is a FIFO or other forms of streaming, it is better to attach a callback:

    local data_in
    on_data =
    function()
        buffer = blobio:read()
        return true
    end

    blobio:data_handler(on_data)

If the callback handler returns true, it will be re-armed, meaning that the
function will fire again next time there is data. It is also possible to
instead swap handler with another data\_handler call. The reason that the
default behaviour is to drop the callback after firing is to prevent a
live-/spin if you happen to ignore reading from the source when there is data.

The read function is line-buffered by default, and will strip the triggering
linefeed. By passing 'true' as the argument to read, it will instead provide a
raw bytestring with as many bytes that could be read capped by an internal
buffer size.

The write function adds its argument to an outbound queue and might not write
all of it immediately. This means that if its owning window is closed before
the queue has been completed, pending outbound data will be lost.

To prevent this, there is also an explicit flush([timeout-ms]) function that
will not return until either all pending jobs (=true) have been completed, or
[timeout-ms] has elapsed while trying.

The normal write calls are prioritised for interactivity/responsiveness and are
meant as a background / low- bandwidth protocol, not fast transfers of large
amounts of data. Transfer callback/flushes may well be deferred until there is
input to trigger it (though that happens quite often).

For larger background transfers, e.g. a clipboard or bchunk event to filesystem
transfer, bgcopy is used:

    local blobio = root:bgcopy(src, dst)
    if not blobio then
        error("copy failed")
    end

    while (root:process() and root:alive()) do
        if blobio then
            local code = blobio:read(true)
            if code then
                if code == string.char(0) then
                    print("bg copy completed")
                else
                    error("copy failed")
                end
                blobio = nil
            end
        end
    end

This will mark src/dst as closed and prevent them from being used again, and
the returned blobio will instead be used to notify when the contents of src has
been written to dst. When there is data to be read from blobio, the copy has
finished or otherwise terminated.

The read values from blobio behaves a little bit odd in order to not deviate
from how it works on the C level or to define a separate userdata type. A
negative value is written once (then the underlying signalling pipe is
terminated) on failure.

## Popen

It is also possible to launch another process and have its stdio be mapped to
individual blobios (as per Binary IO above). The following example would spawn
a 'find /usr' in a subshell, map stdio and wait for it completion.

    local in, out, err, pid = root:popen("find /usr", "r")

    while (root:process() and root:alive()) do
        local running, code = root:pwait(pid)
        local line = in:read()

        if line then
            print(line)
        end

        if not running then
            print("process exited with code", code)
            break
        end
    end

In order to build a zero-copy pipeline, you might also want the linked form:

    local in, _, _, pid = wnd:popen("find /tmp", "r")
		in, _, _, pid = wnd:popen("rev", in, "r")

This would create two jobs, where the output of the first will be set to the
input of the second. The [in] nbio argument to popen will be marked closed and
will only be usable by the new job.

## Environment and current directory

Environment variables can be retrieved by calling getenv on a window, either
for a specific key-value:

    local val = wnd:getenv("PATH")
		print("path is ", val)

Or the entire current environment:

    local env = wnd:getenv()
		for key, val in pairs(env) do
		    print(key, val)
		end

This will create a full copy of the environment, but any modification of it
will not affect the environment of the current process.

The popen function, covered above, can take a custom environment:

    local in, _, _, pid = wnd:popen("echo $ME", "r", {ME = "example"})
    while (wnd:process() and wnd:alive() and wnd:pwait(pid)) do
		end
		print(in:read())

Setting or querying the current directory can be done through chdir:

    print(wnd:chdir())
		print(wnd:chdir("../"))

This will affect calls to fopen, popen and so on. The working directory
is tracked per window. If the chdir fails to switch directory, the current
path will be returned, along with an error message:

    local path, status = wnd:chdir("../")
		if status then
			print("chdir failed")
		end


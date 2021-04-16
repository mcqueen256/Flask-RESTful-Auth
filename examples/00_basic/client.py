#
# Client
#
# Example 0: Global and User Text Editor
# ======================================
#

import os
import urwid

palette = [
    ('title', '', '', '', 'g50', '#60a'),
    ('banner', '', '', '', '#ffa', '#60d'),
    ('inside', '', '', '', 'g38', '#808'),
    ('outside', '', '', '', 'g27', '#a06'),
    ('bg', '', '', '', 'g7', '#d06'),]

class ClientApplication(urwid.Frame):
    def __init__(self, *args, **kwargs):
        # Init with an empty widget
        super().__init__(urwid.Text(''), *args, **kwargs)
        self._last_key_pressed = None
        # Default display is the welcome form.
        self._current_display_function = self.to_welcome_form
        self._current_display_function()
    
    def keypress(self, size, key):
        self._last_key_pressed = key
        if key == 'ctrl x':
            raise urwid.ExitMainLoop()
        self._current_display_function()

    def to_welcome_form(self):
        title = urwid.Padding(urwid.Text(('title', u'Welcome Form'), align='center'))
        header = urwid.AttrMap(title, 'banner')
        self.header = header
        self.body = self._build_welcome_form()
        self.footer = self._build_footer()

    def _build_welcome_form(self) -> urwid.Overlay:
        body = [urwid.Text('Welcome to Text Editor Online!'), urwid.Divider()]
        list_box = urwid.ListBox(urwid.SimpleFocusListWalker(body))
        top = urwid.Overlay(list_box, urwid.SolidFill(u'\N{MEDIUM SHADE}'),
            align='center', width=('relative', 30),
            valign='middle', height=('relative', 60),
            min_width=20, min_height=9)
        return top

    def _build_footer(self) -> urwid.Columns:
        columns = [
            urwid.Text(('', u'Quit: Ctrl-x')),
            urwid.Text(f'last key: {repr(self._last_key_pressed)}'),

        ]
        return urwid.Columns(columns)


# Build and run the main application 
client_app = ClientApplication()
loop = urwid.MainLoop(client_app, palette)
loop.screen.set_terminal_properties(colors=256)
loop.run()

# Clear the terminal
os.system('cls' if os.name == 'nt' else 'clear')
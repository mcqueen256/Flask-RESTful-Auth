#
# Client
#
# Example 0: Global and User Text Editor
# ======================================
#

import os
import urwid

palette = [
    ('reversed', 'standout', ''),
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
        """
        urwid.Frame function. All urwid wigets have this function.

        Using it to handle some key press behaviour. (quit)
        """
        self._last_key_pressed = key
        if key != 'ctrl x':
            return super().keypress(size, key)
        else:
            self.quit()
        self._current_display_function()


    def to_welcome_form(self):
        title = urwid.Padding(urwid.Text(('title', u'Welcome Form'), align='center'))
        header = urwid.AttrMap(title, 'banner')
        self.header = header
        self.body = self._build_welcome_form()
        self.footer = self._build_footer()
    

    def to_login_form(self):
        title = urwid.Padding(urwid.Text(('title', u'Login Form'), align='center'))
        header = urwid.AttrMap(title, 'banner')
        self.header = header
        self.body = self._build_login_form()
        self.footer = self._build_footer()
    

    def to_signup_form(self):
        title = urwid.Padding(urwid.Text(('title', u'Signup Form'), align='center'))
        header = urwid.AttrMap(title, 'banner')
        self.header = header
        self.body = self._build_signup_form()
        self.footer = self._build_footer()
    
    
    def quit(self):
        raise urwid.ExitMainLoop()


    def _build_welcome_form(self) -> urwid.Overlay:
        login = self._make_btn('Login', lambda: self.to_login_form())
        signup = self._make_btn('Signup', lambda: self.to_signup_form())
        quit = self._make_btn('Quit', lambda: self.quit())
        button_list = [login, signup, quit]
        list_box = urwid.ListBox(urwid.SimpleFocusListWalker(button_list))
        layout = urwid.Filler(
            # Row Start
            urwid.Pile([
                urwid.Padding(urwid.Text('Welcome to Text Editor Online!', align='center'), align='center'),
                urwid.Divider(),
                urwid.Divider(),
                # Column Start
                urwid.Columns([
                    urwid.BoxAdapter(urwid.SolidFill(), height=1),
                    (11, urwid.BoxAdapter(list_box, height=3)), # (11, ...) is width
                    urwid.BoxAdapter(urwid.SolidFill(), height=1),
                ]),
                # Column End
            ])
            # Row End
        )
        return self._wrap_in_overlay(layout)


    def _build_login_form(self) -> urwid.Overlay:
        login = self._make_btn('Login', lambda: self.to_welcome_form())
        back = self._make_btn('Back', lambda: self.to_welcome_form())
        layout = urwid.Filler(
            urwid.Pile([
                urwid.Padding(urwid.Text('Login', align='center'), align='center'),
                urwid.Divider(),
                urwid.Columns([
                    (4, urwid.BoxAdapter(urwid.SolidFill(), height=1)),
                    urwid.Pile([urwid.Edit("Username: "), urwid.Edit("Password: ")]),
                    (4, urwid.BoxAdapter(urwid.SolidFill(), height=1)),
                ]),
                urwid.Divider(),
                urwid.Columns([
                    urwid.BoxAdapter(urwid.SolidFill(), height=1),
                    (11, urwid.Pile([login, back])),
                    urwid.BoxAdapter(urwid.SolidFill(), height=1),
                ]),
            ])
        )
        return self._wrap_in_overlay(layout)


    def _build_signup_form(self) -> urwid.Overlay:
        login = self._make_btn('Signup', lambda: self.to_welcome_form())
        back = self._make_btn('Back', lambda: self.to_welcome_form())
        layout = urwid.Filler(
            urwid.Pile([
                urwid.Padding(urwid.Text('Create Account', align='center'), align='center'),
                urwid.Divider(),
                urwid.Columns([
                    (4, urwid.BoxAdapter(urwid.SolidFill(), height=1)),
                    urwid.Pile([urwid.Edit("Username: "), urwid.Edit("Password: ")]),
                    (4, urwid.BoxAdapter(urwid.SolidFill(), height=1)),
                ]),
                urwid.Divider(),
                urwid.Columns([
                    urwid.BoxAdapter(urwid.SolidFill(), height=1),
                    (11, urwid.Pile([login, back])),
                    urwid.BoxAdapter(urwid.SolidFill(), height=1),
                ]),
            ])
        )
        return self._wrap_in_overlay(layout)
    
    def _wrap_in_overlay(self, widget):
        top = urwid.Overlay(widget, urwid.SolidFill(u'\N{MEDIUM SHADE}'),
            align='center', width=('relative', 30),
            valign='middle', height=('relative', 8),
            min_width=20, min_height=9)
        return top
    
    def _make_btn(self, label, callback):
        button = urwid.Button(label)
        urwid.connect_signal(button, 'click', lambda btn: callback())
        button = urwid.AttrMap(button, None, focus_map='reversed')
        return button



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
import sublime, sublime_plugin
import subprocess
from os.path import isfile

# Default settings.
styles        = ["LLVM", "Google", "Chromium", "Mozilla", "WebKit", "File"]
settings_file = 'clang_format.sublime-settings'


def clangFormatSetPath():
    pass

def set_path(path):
    settings = sublime.load_settings(settings_file)
    settings.set('binary', path)
    print("Done")

def update_path():
    w = sublime.active_window()
    w.show_input_panel("Path to clang-format: ", binary, set_path, None, None)

def check_binary():
    if (not isfile(binary)):
        msg = "The clang-format binary was not found. Set a new path?"
        if sublime.ok_cancel_dialog(msg):
            update_path()
        return False
    return True

def load_settings():
    print("load settings")
    # We set these globals.
    global binary
    global style
    settings = sublime.load_settings(settings_file)

    # Load settings, with defaults.
    binary   = settings.get('binary', 'clang-format')
    style    = settings.get('style',   styles[0]    )

class ClangFormatCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        load_settings()

        # Check that we found the binary.
        if not check_binary():
            return
        
        # Status message.
        sublime.status_message("Clang format (style: '"+ style + "'')." )

        # The below code has been taken and tweaked from llvm.
        encoding = self.view.encoding()
        if encoding == 'Undefined':
            encoding = 'utf-8'
        regions = []
        command = [binary, '-style', style]

        for region in self.view.sel():
            regions.append(region)
            region_offset = min(region.a, region.b)
            region_length = abs(region.b - region.a)
            command.extend(['-offset', str(region_offset),
                            '-length', str(region_length),
                            '-assume-filename', str(self.view.file_name())])
        old_viewport_position = self.view.viewport_position()


        buf = self.view.substr(sublime.Region(0, self.view.size()))
        p = subprocess.Popen(command, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        output, error = p.communicate(buf.encode(encoding))
        if error:
            print(error)
        self.view.replace(
            edit, sublime.Region(0, self.view.size()),
            output.decode(encoding))
        self.view.sel().clear()
        for region in regions:
            self.view.sel().add(region)
        # FIXME: Without the 10ms delay, the viewport sometimes jumps.
        sublime.set_timeout(lambda: self.view.set_viewport_position(
            old_viewport_position, False), 10)

class clangFormatSetPathCommand(sublime_plugin.WindowCommand):
    def run(self):
        update_path()

class clangFormatSelectStyleCommand(sublime_plugin.WindowCommand):
    def done(self, i):
        settings = sublime.load_settings(settings_file)
        print (styles[i])
        settings.set("style", styles[i])

    def run(self):
        load_settings()
        active_window = sublime.active_window()

        # Get current style
        try:
            sel = styles.index(style)
        except ValueError:
            sel = 0

        active_window.show_quick_panel(styles, self.done, 0, sel)

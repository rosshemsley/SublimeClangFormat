import sublime, sublime_plugin
import subprocess

# Default settings.
styles  = ["LLVM", "Google", "Chromium", "Mozilla", "WebKit", "Custom", "File"]
settings_file         = 'clang_format.sublime-settings'
custom_style_settings = 'clang_format_custom.sublime-settings'

# Hacky, but there doesn't seem to be a cleaner way to do this for now.
# We need to be able to load all these settings from the settings file.
all_settings  = [ 
    "BasedOnStyle", "AccessModifierOffset", "AlignEscapedNewlinesLeft",
    "AlignTrailingComments", "AllowAllParametersOfDeclarationOnNextLine",
    "AllowShortFunctionsOnASingleLine", "AllowShortIfStatementsOnASingleLine",
    "AllowShortLoopsOnASingleLine", "AlwaysBreakBeforeMultilineStrings",
    "AlwaysBreakTemplateDeclarations", "BinPackParameters",
    "BreakBeforeBinaryOperators", "BreakBeforeBraces",
    "BreakBeforeTernaryOperators", "BreakConstructorInitializersBeforeComma",
    "ColumnLimit", "CommentPragmas",
    "ConstructorInitializerAllOnOneLineOrOnePerLine",
    "ConstructorInitializerIndentWidth", "ContinuationIndentWidth",
    "Cpp11BracedListStyle", "DerivePointerBinding",
    "ExperimentalAutoDetectBinPacking", "IndentCaseLabels",
    "IndentFunctionDeclarationAfterType", "IndentWidth",
    "KeepEmptyLinesAtTheStartOfBlocks", "Language", "MaxEmptyLinesToKeep",
    "NamespaceIndentation", "ObjCSpaceAfterProperty",
    "ObjCSpaceBeforeProtocolList", "PenaltyBreakBeforeFirstCallParameter",
    "PenaltyBreakComment", "PenaltyBreakFirstLessLess", "PenaltyBreakString",
    "PenaltyExcessCharacter", "PenaltyReturnTypeOnItsOwnLine",
    "PointerBindsToType", "SpaceBeforeAssignmentOperators", "SpaceBeforeParens",
    "SpaceInEmptyParentheses", "SpacesBeforeTrailingComments", "SpacesInAngles",
    "SpacesInCStyleCastParentheses", "SpacesInContainerLiterals",
    "SpacesInParentheses", "Standard", "TabWidth", "UseTab"
]

# This function taken from Stack Overflow response:
# http://stackoverflow.com/questions/377017/test-if-executable-exists-in-python
def which(program):
    import os
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)
    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file        
    return None


def set_path(path):
    settings = sublime.load_settings(settings_file)
    settings.set('binary', path)
    # Make sure the globals are set.
    load_settings()


# Avoid dependencies on yaml.
def dic_to_yaml_simple(d):
    output = ""
    n=len(d)
    for k in d:
        output += str(k)
        output += ": "
        if type(d[k]) is bool:
            output += str(d[k]).lower()
        else:
            output += str(d[k])
        n-=1
        if (n!=0):
            output += ', '
    return output

# We store a set of customised values in a sublime settings file, so that it is
# possible to very quickly customise the output.
def load_custom():
    custom_settings = sublime.load_settings(custom_style_settings)
    keys = dict()

    for v in all_settings:
        result = custom_settings.get(v, None)
        if result != None:
            keys[v] = result
    out = "-style={" + dic_to_yaml_simple(keys) + "}"

    return out

def update_path():
    w = sublime.active_window()
    w.show_input_panel("Path to clang-format: ", binary, set_path, None, None)

def check_binary():
    if (which(binary) == None):

        # Try to guess the correct setting.
        if (which("clang-format") != None):
            # Looks like clang-format is in the path, remember that.
            set_path('clang-format')

        msg = "The clang-format binary was not found. Set a new path?"
        if sublime.ok_cancel_dialog(msg):
            update_path()
        return False
    return True

def load_settings():
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




        # Check that the binary exists.
        if not check_binary():
            return
        
        # Status message.
        sublime.status_message("Clang format (style: "+ style + ")." )

        # The below code has been taken and tweaked from llvm.
        encoding = self.view.encoding()
        if encoding == 'Undefined':
            encoding = 'utf-8'
        regions = []

        # We use 'file' not 'File' when passing to the binary.
        _style = style
        if style == "File":
            _style = "file"

        command = []

        if style == "Custom":
            command = [binary, load_custom()]
        else:
            command = [binary, '-style', _style]

        max_r=0;

        for region in self.view.sel():
            regions.append(region)
            region_offset = region.begin()# min(region.a, region.b)
            region_length = region.size() # abs(region.b - region.a)

            view = sublime.active_window().active_view()

            # If you run the command at the end of the line, we assume
            # You wanted to run it from the beginning instead.
            # if view.classify(region_offset) & sublime.CLASS_LINE_END >0:
            region = view.line(region_offset)
            region_offset = region.begin()
            region_lenth = region.size()

            command.extend(['-offset', str(region_offset),
                            '-length', str(region_length),
                            '-assume-filename', str(self.view.file_name())])

            # command.extend(['-output-replacements-xml'])
        old_viewport_position = self.view.viewport_position()

        # pirnt(old_viewport_position)

        buf = self.view.substr(sublime.Region(0, self.view.size()))
        p = subprocess.Popen(command, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        output, error = p.communicate(buf.encode(encoding))
        
        # Display any errors returned by clang-format.
        if error:
            # We don't want to do anything by default.
            # If the error message tells us it is doing that, truncate it.
            default_message = ", using LLVM style"
            msg = error.decode("utf-8")          
            if msg.strip().endswith(default_message):
                msg = msg[:-len(default_message)-1]
            sublime.error_message("Clang format: " + msg)
            # Don't do anything.
            return

        self.view.replace(
            edit, sublime.Region(0, self.view.size()),
            output.decode(encoding))

        # self.view.sel().clear()
        # self.view.sel().add(sublime.Region(max_r,max_r))
        # for region in regions:
            # self.view.sel().add(region)

        # FIXME: Without the 10ms delay, the viewport sometimes jumps.
        # sublime.set_timeout(lambda: self.view.set_viewport_position(
            # old_viewport_position, False), 10)

class clangFormatSetPathCommand(sublime_plugin.WindowCommand):
    def run(self):
        update_path()

class clangFormatSelectStyleCommand(sublime_plugin.WindowCommand):
    def done(self, i):
        settings = sublime.load_settings(settings_file)
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

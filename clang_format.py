import sublime, sublime_plugin
import subprocess, os

# The styles available by default. We add one option: "Custom". This tells
# the plugin to look in an ST settings file to load the customised style.
styles  = ["LLVM", "Google", "Chromium", "Mozilla", "WebKit", "Custom", "File"]

# Settings file locations.
settings_file         = 'clang_format.sublime-settings'
custom_style_settings = 'clang_format_custom.sublime-settings'

# Hacky, but there doesn't seem to be a cleaner way to do this for now.
# We need to be able to load all these settings from the settings file.
all_settings  = [
    "BasedOnStyle", "AccessModifierOffset", "AlignAfterOpenBracket",
    "AlignConsecutiveAssignments", "AlignEscapedNewlinesLeft",
    "AlignTrailingComments", "AllowAllParametersOfDeclarationOnNextLine",
    "AllowShortBlocksOnASingleLine", "AllowShortCaseLabelsOnASingleLine",
    "AllowShortFunctionsOnASingleLine", "AllowShortIfStatementsOnASingleLine",
    "AllowShortLoopsOnASingleLine", "AlwaysBreakAfterDefinitionReturnType",
    "AlwaysBreakBeforeMultilineStrings", "AlwaysBreakTemplateDeclarations",
    "BinPackArguments", "BinPackParameters",
    "BreakBeforeBinaryOperators", "BreakBeforeBraces",
    "BreakBeforeTernaryOperators", "BreakConstructorInitializersBeforeComma",
    "ColumnLimit", "CommentPragmas",
    "ConstructorInitializerAllOnOneLineOrOnePerLine",
    "ConstructorInitializerIndentWidth", "ContinuationIndentWidth",
    "Cpp11BracedListStyle", "DerivePointerBinding", "DisableFormat",
    "ExperimentalAutoDetectBinPacking", "IndentCaseLabels",
    "IndentFunctionDeclarationAfterType", "IndentWidth", "IndentWrappedFunctionNames",
    "KeepEmptyLinesAtTheStartOfBlocks", "Language", "MacroBlockBegin", "MacroBlockEnd",
    "MaxEmptyLinesToKeep", "NamespaceIndentation", "ObjCBlockIndentWidth",
    "ObjCSpaceAfterProperty", "ObjCSpaceBeforeProtocolList",
    "PenaltyBreakBeforeFirstCallParameter", "PenaltyBreakComment",
    "PenaltyBreakFirstLessLess", "PenaltyBreakString",
    "PenaltyExcessCharacter", "PenaltyReturnTypeOnItsOwnLine", "PointerAlignment",
    "PointerBindsToType", "SpaceBeforeAssignmentOperators", "SpaceBeforeParens",
    "SpaceInEmptyParentheses", "SpacesBeforeTrailingComments", "SpacesInAngles",
    "SpacesInCStyleCastParentheses", "SpacesInContainerLiterals",
    "SpacesInParentheses", "SpacesInSquareBrackets", "Standard", "TabWidth", "UseTab"
]

# Check if we are running on a Windows operating system
os_is_windows = os.name == 'nt'

# The default name of the clang-format executable
default_binary = 'clang-format.exe' if os_is_windows else 'clang-format'

# This function taken from Stack Overflow response:
# http://stackoverflow.com/questions/377017/test-if-executable-exists-in-python
def which(program):
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


# Set the path to the binary in the settings file.
def set_path(path):
    settings = sublime.load_settings(settings_file)
    settings.set('binary', path)
    sublime.save_settings(settings_file)
    # Make sure the globals are updated.
    load_settings()


# We avoid dependencies on yaml, since the output we need is very simple.
def dic_to_yaml_simple(d):
    output = ""
    n      = len(d)
    for k in d:
        output += str(k)
        output += ": "
        if type(d[k]) is bool:
            output += str(d[k]).lower()
        else:
            output += str(d[k])
        n -= 1
        if (n!=0):
            output += ', '
    return output

# We store a set of customised values in a sublime settings file, so that it is
# possible to very quickly customise the output.
# This function returns the correct customised style tag.
def load_custom():
    custom_settings = sublime.load_settings(custom_style_settings)
    keys = dict()
    for v in all_settings:
        result = custom_settings.get(v, None)
        if result != None:
            keys[v] = result
    out = "-style={" + dic_to_yaml_simple(keys) + "}"

    return out

# Display input panel to update the path.
def update_path():
    load_settings()
    w = sublime.active_window()
    w.show_input_panel("Path to clang-format: ", binary, set_path, None, None)

# Check that the binary can be found and is executable.
def check_binary():
    # If we couldn't find the binary.
    if (which(binary) == None):
        # Try to guess the correct setting.
        if (which(default_binary) != None):
            # Looks like clang-format is in the path, remember that.
            set_path(default_binary)
            return True
        # We suggest setting a new path using an input panel.
        msg = "The clang-format binary was not found. Set a new path?"
        if sublime.ok_cancel_dialog(msg):
            update_path()
            return True
        else:
            return False
    return True

# Load settings and put their values into global scope.
# Probably a nicer way of doing this, but it's simple enough and it works fine.
def load_settings():
    # We set these globals.
    global binary
    global style
    global format_on_save
    global languages
    settings = sublime.load_settings(settings_file)
    # Load settings, with defaults.
    binary         = settings.get('binary', default_binary)
    style          = settings.get('style',   styles[0]    )
    format_on_save = settings.get('format_on_save', False  )
    languages      = settings.get('languages', ['C', 'C++', 'C++11', 'JavaScript'])

def is_supported(lang):
    # TODO: Add Objective-C and Objective-C++ here.
    load_settings()
    return any((lang.endswith((l + '.tmLanguage', l + '.sublime-syntax')) for l in languages))

# Triggered when the user runs clang format.
class ClangFormatCommand(sublime_plugin.TextCommand):
    def run(self, edit, whole_buffer=False):

        # Update the settings.
        load_settings()

        # Check that the binary exists.
        if not check_binary():
            return

        # Status message.
        sublime.status_message("Clang format (style: "+ style + ")." )

        #----------------------------------------------------------------------#
        # The below code has been taken and tweaked from llvm.
        #----------------------------------------------------------------------#

        encoding = self.view.encoding()
        if encoding == 'Undefined':
            encoding = 'utf-8'

        # We use 'file' not 'File' when passing to the binary.
        # But all the other styles are in all caps.
        _style = style
        if style == "File":
            _style = "file"

        # This is the command we will run, we build it incrementally.
        command = []

        if style == "Custom":
            command = [binary, load_custom()]
        else:
            command = [binary, '-style', _style]

        regions = []
        if whole_buffer:
            regions = [sublime.Region(0, self.view.size())]
        else:
            regions = self.view.sel()

        # Deal with all selected regions.
        for region in regions:
            region_offset = region.begin()
            region_length = region.size()

            view = sublime.active_window().active_view()

            # If the command is run at the end of the line,
            # Run the command on the whole line.
            if view.classify(region_offset) & sublime.CLASS_LINE_END > 0:
                region        = view.line(region_offset)
                region_offset = region.begin()
                region_lenth  = region.size()

            # Add this region to the set of offsets.
            command.extend(['-offset', str(region_offset),
                            '-length', str(region_length)])

        # We only set the offset once, otherwise CF complains.
        command.extend(['-assume-filename', str(self.view.file_name())] )

        # TODO: Work out what this does.
        # command.extend(['-output-replacements-xml'])

        # Run CF, and set buf to its output.
        buf = self.view.substr(sublime.Region(0, self.view.size()))
        startupinfo = None
        if os_is_windows:
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        p   = subprocess.Popen(command, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, stdin=subprocess.PIPE,
                               startupinfo=startupinfo)
        output, error = p.communicate(buf.encode(encoding))

        # Display any errors returned by clang-format using a message box,
        # instead of just printing them to the console. Also, we halt on all
        # errors: e.g. We don't just settle for using using a default style.
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

        # If there were no errors, we replace the view with the outputted buf.
        self.view.replace(
            edit, sublime.Region(0, self.view.size()),
            output.decode(encoding))

        # TODO: better semantics for re-positioning cursors!

        # TODO: decide if this is really needed. It seems not?
        # FIXME: Without the 10ms delay, the viewport sometimes jumps.
        # sublime.set_timeout(lambda: self.view.set_viewport_position(
            # old_viewport_position, False), 10)

# Hook for on-save event, to allow application of clang-format on save.
class clangFormatEventListener(sublime_plugin.EventListener):
    def on_pre_save(self, view):

        # Only do this for C or C++. TODO: we should consider adding support
        # For Objective-C at some point.
        syntax = view.settings().get('syntax')
        if is_supported(syntax):
            # Ensure that settings are up to date.
            load_settings()
            if format_on_save:
                print("Auto-applying Clang Format on save.")
                view.run_command("clang_format", {"whole_buffer": True})

# Called from the UI to update the path in the settings.
class clangFormatSetPathCommand(sublime_plugin.WindowCommand):
    def run(self):
        update_path()

# Called from the UI to set the current style.
class clangFormatSelectStyleCommand(sublime_plugin.WindowCommand):
    def done(self, i):
        settings = sublime.load_settings(settings_file)
        settings.set("style", styles[i])
        sublime.save_settings(settings_file)

    def run(self):
        load_settings()
        active_window = sublime.active_window()
        # Get current style
        try:
            sel = styles.index(style)
        except ValueError:
            sel = 0
        active_window.show_quick_panel(styles, self.done, 0, sel)

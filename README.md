Clang Format
============

[![Package Control](https://packagecontrol.herokuapp.com/downloads/Clang%20Format.svg?style=flat-square)](https://packagecontrol.io/packages/Clang%20Format)


What it does
------------
Clang-format is a tool for formatting C++, built on LLVM. This is a
package that allows you to run it easily from within Sublime Text.

![demo](https://raw.githubusercontent.com/rosshemsley/demos/master/clang_format.gif)

About
-----
In this package, we provide an alternative wrapper around clang-format
for use within Sublime Text 3. Whilst LLVM does provide a very simple plugin
to work with Sublime Text [here](https://llvm.org/svn/llvm-project/cfe/trunk/tools/clang-format/clang-format-sublime.py),
it doesn't really exploit any of the Sublime Text package functionality.
We add new features such as customising the style from a settings file,
selecting styles using the Command Palette, and easier installation.

Installing
----------
- Install `clang-format` in one of the following ways:
  - Install using your package manager, e.g. `sudo apt-get install clang-format` or `sudo apt-get install clang-format-5.0`.
  - Download the [entire LLVM toolchain](http://llvm.org/releases/)
    and extract the `clang-format` binary. Just extract the `.tar.xz`
    file and copy `bin/clang-format` into your PATH (e.g. `/usr/local/bin`).
- Install this package through Package Control in the usual way.
- Set the path to the clang-format binaries. You can do this from within Sublime
  Text by choosing `Clang Format - Set Path` from the command palette.  Hint:
  the path should look something like this `[path/to/clang]/clang/bin/clang-format`.
  If clang-format is in your system path, you shouldn't need to do anything.

Use
---
- Default shortcut is `super+option+a` on OSX and `option+cmd+a` otherwise.
  This will apply clang-format to the selection.
- From the command palette, you can select the formatting type by using
  `Clang Format: Select Style`. You will find the small number of defaults,
  and also a new 'Custom' entry. Selecting this entry allows you to customise
  the style through a settings file. You can access it from the main menu,
  under `Package Settings`. In this file you can add custom rules, such
  as `Allmen` style braces, and different indents. For examples see
  http://clang.llvm.org/docs/ClangFormatStyleOptions.html.
- Settings for the 'Custom' format and others are available through the Sublime
  Text preferences.
- It is possible to run the formatter on every save to a file, change settings
  to `"format_on_save": true`.
- To run the formatter in one stroke, press `ctrl+e` for windows and linux
  or `super+e` for OSX. You can always change the keybinding in the
  keymap to your liking.
- To change settings on a per-package basis, add them under `ClangFormat` key,
  example project.sublime-settings:

```json
{
  "folders": [],
  "settings": {
    "ClangFormat": {
      "format_on_save": true
    }
  }
}
```


If You Liked This
-----------------
- ... And want to contribute, PR's gladly accepted!

- Maybe you'll like my other plugin, [iOpener](https://github.com/rosshemsley/iOpener).
It lets you open files by path, with completion, history, and other goodies.

- Otherwise, why not pop on over and star this repo on GitHub?

Credits
-------
Thanks to the LLVM project for doing the hard work, including writing clang
format, and also the original Sublime Text plugin on which this package is
based.

Also thanks to [y0ssar1an](https://github.com/y0ssar1an), [Bendtherules](https://github.com/bendtherules)
and other contributors for their improvements!

Finally
--------
Why not go and watch the video that got me interested in clang-format in
the first place?

[The Care and Feeding of C++'s Dragons](http://channel9.msdn.com/Events/GoingNative/2013/The-Care-and-Feeding-of-C-s-Dragons)

Clang Format
============

***Updates:***
Preliminary support for JavaScript has been added! Update to latest version
of clang-format provided with LLVM 3.6 to avoid known [bugs](https://github.com/rosshemsley/SublimeClangFormat/pull/4).

What it does
------------
Clang-format is a tool for re-formatting C++, built on LLVM. This is a
package that allows you to run it easily from within Sublime Text.

![demo](https://raw.githubusercontent.com/rosshemsley/demos/master/clang_format.gif)

About
-----
In this package, we provide an alternative wrapper around clang-format
for use within Sublime Text 3. Whilst LLVM does provide a very simple plugin
to work with Sublime Text already:
https://llvm.org/svn/llvm-project/cfe/trunk/tools/clang-format/clang-format-sublime.py,
it doesn't really exploit any of the Sublime Text package functionality.
We add new features such as customising the style from a settings file,
selecting styles using the Command Palette, and easier installation.

Installing
----------
- Install this package through Package Control in the usual way.
- Get the clang-format binary for your platform. All binaries provided below are from
  the LLVM 3.6 release. They are for **64-bit platforms only**:
  - [Fedora 21](http://107.170.192.246:8001/llvm3.6/fedora21/clang-format)
  - [FreeBSD 10](http://107.170.192.246:8001/llvm3.6/freebsd10/clang-format)
  - [OS X](http://107.170.192.246:8001/llvm3.6/osx/clang-format)
  - [openSUSE 13.2](http://107.170.192.246:8001/llvm3.6/opensuse13.2/clang-format)
  - [Ubuntu 14.04](http://107.170.192.246:8001/llvm3.6/ubuntu14.04/clang-format)
  - [Windows](http://107.170.192.246:8001/llvm3.6/windows/clang-format.exe)

  If you prefer, you can download the [entire LLVM toolchain](http://llvm.org/releases/download.html)
  and extract the `clang-format` binary yourself. Just extract the `.tar.xz`
  file and copy `bin/clang-format` into your PATH (e.g. `/usr/local/bin`).
- Set the path to the clang-format binaries. You can do this from within Sublime
  Text by choosing `Clang Format - Set Path` from the command palette.  Hint:
  the path should look something like this `[path/to/clang]/clang/bin/clang-format`.
  If clang-format is in your system path, you shouldn't need to do anything.

Use
---
- Default shortcut is `super+option+a` on OSX and `ctrl+option+a` otherwise.
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

Also thanks to [y0ssar1an](https://github.com/y0ssar1an) and [Bendtherules](https://github.com/bendtherules) for their improvements!

Finally
--------
Why not go and watch the video that got me interested in clang-format in
the first place?

[The Care and Feeding of C++'s Dragons](http://channel9.msdn.com/Events/GoingNative/2013/The-Care-and-Feeding-of-C-s-Dragons)

Clang Format
============

What it does
------------
Clang-format is a tool for re-formatting C++, built on llvm. This is a
package that allows you to run it easily from within Sublime Text.

![demo](https://raw.githubusercontent.com/rosshemsley/demos/master/clang_format.gif)

About
-----
In this package, we provide an alternative wrapper around clang-format
for use within Sublime Text 3. (llvm provides a very simple wrapper
to work with Sublime Text already:
https://llvm.org/svn/llvm-project/cfe/trunk/tools/clang-format/clang-format-sublime.py).

Why Wrap the Old Wrapper?
----------------------------
The simple llvm plugin works fine, but in this package we add the following new
features:

- You can install this package form Package Control.
- You can set the path to clang-format from within Sublime Text.
- You can choose the style from within Sublime Text.
- This version checks the current syntax is actually C/C++ before running
  the formatter.

Installing
----------
- Install this package through Package Control in the usual way.
- Get the clang-format binary. If you don't already have it, you can download
  binaries from llvm: http://llvm.org/releases/download.html.
- Set the path to the clang-format binaries. You can do this from within Sublime
  Text by choosing `Clang Format - Set Path` from the command palette.  Hint: 
  the path should look something like this `[path/to/clang]/clang/bin/clang-format`.
  If clang-format is in your path, you shouldn't need to do anything.

Use
---
- Default shortcut is `super+option+a` on OSX and `ctrl+option+a` otherwise.
  This will apply clang-format to the selection.
- From the command palette, you can select the formatting type by using
  `Clang Format: Select Style`.

Credits
-------
Thanks to the llvm project for doing the hard work, including writing clang
format, and also the original Sublime Text plugin on which this package is
based.

Why not go and watch the video that got me interested in clang-format in the 
first place:

http://channel9.msdn.com/Events/GoingNative/2013/The-Care-and-Feeding-of-C-s-Dragons

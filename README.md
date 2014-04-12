Clang Format
============

What it does
------------
Clang-format is a tool for re-formatting C++ using llvm. This plugin allows you to run it
more easily from within Sublime Text.

About
-----
In this package, we provide an alternative wrapper around clang-format
for use within Sublime Text 3.
(https://llvm.org/svn/llvm-project/cfe/trunk/tools/clang-format/clang-format-sublime.py). 
The llvm team already did a great job of writing a Sublime Text
plugin for clang-format, but it's not that easy to install through the usual
channels, and it doesn't provide options to update the settings from within
Sublime Text. This package is intended to help more people find out about clang-
format, and make it easier to use; though we underline that all the hard work
has already been done by the llvm team. This plugin just wraps their code and
makes it easier to use.

Why Wrap the Old Wrapper?
----------------------------
The llvm wrapper works fine, but here are some reasons for using this wrapper
around their wrapper.

- You can install this package form Package Control.
- You can set the path from within Sublime Text.
- You can choose the style from within Sublime Text.
- This version checks the current scope is actually C/C++ before running
  the formatter.

Installing
----------
- Install this package through Package Control in the usual way.
- Get hold of the clang-format binary, if you don't already have it
  (http://llvm.org/releases/download.html).
- Set the path to the clang-format binaries. You can do this from within
  Sublime Text by choosing `Clang Format - Set Path` form the command
  palette.  Hint: it probably ends like this `clang/bin/clang-format`.

Use
---
- Default shortcut is `super+option+a` on OSX and `cntrl+option+a` otherwise.
This will apply clang-format to the selection.
- From the command palette, you can select the formatting by using
`Clang Format: Select Style`.

Credits
-------
Thanks to the llvm project for doing the hard work, including writing clang
foramt, and writing the original Sublime Text plugin on which this package is
based.

Why not go and watch the video that got me interested in clang-format in the 
first place:

http://channel9.msdn.com/Events/GoingNative/2013/The-Care-and-Feeding-of-C-s-Dragons
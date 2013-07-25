Sublime2Ginger
==========
Simple English grammar checker plugin for [Sublime Text 2](http://www.sublimetext.com/2).
This grammar checker will fix spelling errors and grammatical mistakes using ***unofficial*** [Ginger](http://www.getginger.jp/) API.

Installation
----------
**With Git:** Clone the repository in your Sublime Text "Packages" directory:
```
$ git clone https://github.com/zoncoen/Sublime2Ginger.git
```
**Without Git:** Download the latest source from [GitHub](https://github.com/zoncoen/Sublime2Ginger) and copy the Sublime2Ginger directory to your Sublime Text "Packages" directory.

The "Packages" directory is located at:

- **OSX:** ```~/Library/Application Support/Sublime Text 2/Packages/```
- **Linux:** ```~/.config/sublime-text-2/Packages/```
- **Windows:** ```%APPDATA%/Sublime Text 2/Packages/```

Usage
----------
You can control Sublime2Ginger via the Command Palette (<kbd>⇧⌘P</kbd>  on OS X, <kbd>Ctrl+Shift+P</kbd> on Linux/Windows).
The available command is:

- **Sublime2Ginger: Grammar Check** - Find spelling errors and grammatical mistakes on the cursor line.

You can also use a keyboard shortcut to run Sublime2Ginger.

- **Sublime2Ginger: Grammar Check** - <kbd>⌃⇧G</kbd> (OS X) / <kbd>Ctrl+Shift+G</kbd> (Linux/Windows)

Settings
----------
To check the default settings, select the menu item `Preferences->Package Settings->Sublime2Ginger->Settings - Default`.

Do not edit the default Sublime2Ginger settings. Your changes will be lost when Sublime2Ginger is updated. Always edit the user Sublime2Ginger settings by selecting `Preferences->Package Settings->Sublime2Ginger->Settings - User`.

If you don't want to replace your text automatically, modify the user setting:
```
"auto_replace" : false
```

Animated screenshot
----------
This is the animated screenshot of Sublime2Ginger.

![Sublime2Ginger animated screenshot](http://zoncoen.github.io/images/Sublime2Ginger-example.gif)

Reference
----------
[Ginger API を試してみた - にひりずむ::しんぷる (http://blog.livedoor.jp/xaicron/archives/54466736.html)](http://blog.livedoor.jp/xaicron/archives/54466736.html)

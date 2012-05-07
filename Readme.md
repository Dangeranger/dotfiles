Obmarg's Dotfiles
===

This repository contains my dotfiles and a python script that takes care of moving everything into place and downloading my various vim plugins.

Currently the dotfiles consist of my vimrc and my bashrc.  Most of the vimrc contains inline documentation, so feel free to have a browse and steal ideas.

Setup.py
---
The setup.py script included in this repository can be used to automatically configure a PC to make use of the dotfiles from this repository. Currently, it can:

- Optionally link _vimrc & _bashrc to the appropriate dotfiles in the users home directory.  The original files (if there are any) will be stored as ~/.bashrc.back etc.
- Install the vim pathogen plugin from vim.org to allow easy management of vim plugins.
- Install or update vim plugins from vim.org & git repositories as configured in dotfiles.conf

Usage
-
Running `python setup.py` should start the process.  You will be asked if you want to install _vimrc & _bashrc, and then the vim plugins as listed in dotfiles.conf will be installed.

The command can be repeated at a later date, and it will ensure that all git based vim plugins are kept up to date.

If you decide you no longer want a vim plugin, simply remove it from dotfiles.conf and run `python setup.py -c` to have setup.py delete it.
# ai-workspace

Collection of AI tools and scripts to sync between things.

Since each tool has its own environment, it is recommended to have separate activation script evs.

## Install

1. Pull all the submodules with `git submodule update --init --recursive`.
1. Git LFS wasn't working out of the box for me so I needed to run `git config --global core.sshCommand "C:/Windows/System32/OpenSSH/ssh.exe"` to set up on windows.

## TODO

- Script to bootstrap all apps.
- Script to update all.
- Set up some kind of shared data directory so I can share input data such as training images and caption files.

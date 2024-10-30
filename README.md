# ai-workspace

Collection of AI tools and scripts to sync between things.

Since each tool has its own environment, it is recommended to have separate activation script evs.

## Install

Windows Git LFS wasn't working out of the box for me so I needed to run `git config --global core.sshCommand "C:/Windows/System32/OpenSSH/ssh.exe"` to set up on windows.

1. Pull all the submodules with `git submodule update --init --recursive`.
1. Setup a python venv with `python -m venv .venv`.
1. Install torch with cuda `pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu124`.
1. Run `.venv/bin/activate`
1. Install non torch deps `pip install -r requirements.txt`

## TODO

- Script to bootstrap all apps.
- Script to update all.
- Set up some kind of shared data directory so I can share input data such as training images and caption files.

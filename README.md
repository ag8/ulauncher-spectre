Works with [https://github.com/spectre-app/cli](spectre-cli).

Assumes you have `ssh-askpass` installed. If not, run `sudo apt-get install ssh-askpass`. If you have your own favorite askpass, set the 'SPECTRE_ASKPASS' environment variable yourself, and get rid of line 23 in main.py.

Requires `xclip`. `sudo apt-get install xclip` on ubuntu.

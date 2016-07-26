## Vim-Dropbox

This is a fork of the [NetRw](https://github.com/vim-scripts/netrw.vim) project
which allows vim to support URL's of the type `dbx:///Path/Inside/Dropbox`.

At the moment, it supports only reading files, creating files, and browsing
directories. It cannot perform file deletions or renames.

## Installation

Installation is currently manual, but should not be too difficult for users
versed in the ways of the shell.

1. Install the [Dropbox Python
   SDK](https://github.com/dropbox/dropbox-sdk-python) if you do not already
   have it installed.

2. Go to https://www.dropbox.com/developers/apps and create a new app with any
   name.

3. Click into the App's settings page and click on the `Generate` button under
   the label `Generated Access Token`.

4. Copy this token and replace the string `INSERT_TOKEN_HERE` in the file `bin/dbx.py` with the token.

5. Run the `make install` from this directory, which will simply append a line
   to your `.vimrc` and `.bashrc` files to enable this plugin.

If you run into any trouble with these steps, please open an issue on GitHub or contact the author out-of-band.

## Usage

    vim dbx:///
    vim dbx:///TestFolder/Example.txt

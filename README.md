# Le Poop
Undo your pip commands, inspired by [nvbn](http://github.com/nvbn/)'s [The Fuck](github.com/nvbn/thefuck) (no affiliation). Why use `Le Poop`? `pip install` can come with a slew of dependencies, and `pip uninstall` only removes the package you specified. `Le Poop` cleans up *all* the mess, in style.

# Installation

Simply install using pip. Note this installation only supports undo functionality for `pip install`s.

```
pip install lepoop
```

To support undo functionality for other pip commands, amend your `~/.bashrc` and reload it using `source`.

```
echo "export PROMPT_COMMAND=\"history -a; history -c; history -r; \$PROMPT_COMMAND\"" >> ~/.bashrc
source ~/.bashrc
```
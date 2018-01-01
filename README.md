# Le Poop 💩
An undo for your pip commands. Why use `Le Poop` instead of `uninstall`? Take any `install`. It can come with a slew of dependencies, and `pip uninstall` graciously allows you to remove your new package, and all its friends, one by one. `Le Poop` cleans up *all* the mess with a single command, `poop`. To get started, install using pip.

```
pip install lepoop
```

Then, run `poop` after any `pip` command you regret.

![lepoop](https://user-images.githubusercontent.com/2068077/34466900-e5b6f8f0-ee97-11e7-9d16-c4e7a5abf0d4.gif)

Examples in text:

```
→ $ pip install datascience
Collecting datascience
Requirement already satisfied: setuptools in /Users/alvinwan/miniconda3/envs/py36/lib/python3.6/site-packages (from datascience)
Collecting folium==0.1.5 (from datascience)
...
Successfully installed coveralls-0.5 datascience-0.10.3 folium-0.1.5 sphinx-1.6.5

→ $ poop
pip uninstall -y sphinx folium datascience [enter/ctrl+c]
Uninstalling Sphinx-1.6.5:
  Successfully uninstalled Sphinx-1.6.5
Uninstalling folium-0.1.5:
  Successfully uninstalled folium-0.1.5
Uninstalling datascience-0.10.3:
  Successfully uninstalled datascience-0.10.3
```

```
→ $ ls
donttouchme.tar.gz

→ $ pip download md2py
Collecting md2py
  Using cached md2py-0.0.1.tar.gz
  Saved ./md2py-0.0.1.tar.gz
Collecting markdown (from md2py)
  Using cached Markdown-2.6.10.zip
  Saved ./Markdown-2.6.10.zip
Collecting beautifulsoup4 (from md2py)
  Using cached beautifulsoup4-4.6.0-py3-none-any.whl
  Saved ./beautifulsoup4-4.6.0-py3-none-any.whl
Successfully downloaded md2py markdown beautifulsoup4

→ $ ls
Markdown-2.6.10.zip			donttouchme.tar.gz
beautifulsoup4-4.6.0-py3-none-any.whl	md2py-0.0.1.tar.gz

→ $ poop
rm md2py-0.0.1.tar.gz Markdown-2.6.10.zip beautifulsoup4-4.6.0-py3-none-any.whl [enter/ctrl+c]

→ $ ls
donttouchme.tar.gz
```

```
→ $ pip uninstall texsoup
Uninstalling TexSoup-0.1:
  /Users/alvinwan/miniconda3/envs/py36/lib/python3.6/site-packages/TexSoup-0.1.dist-info/DESCRIPTION.rst
...
/Users/alvinwan/miniconda3/envs/py36/lib/python3.6/site-packages/TexSoup/tex.py
  /Users/alvinwan/miniconda3/envs/py36/lib/python3.6/site-packages/TexSoup/utils.py
Proceed (y/n)? y
  Successfully uninstalled TexSoup-0.1

→ $ poop
pip install texsoup [enter/ctrl+c]
Collecting texsoup
Requirement already satisfied: coverage==3.7.1 in /Users/alvinwan/miniconda3/envs/py36/lib/python3.6/site-packages (from texsoup)
...
Successfully installed coveralls-1.1 texsoup-0.1
```

`Le Poop` supports undos for the only three `pip` commands it makes sense to undo:

- `pip install`: Uninstall packages that were *just* installed. Leaves older packages intact, unless `poop` is run successively.
- `pip download`: Removes tarballs and wheels for the just-downloaded package and all its dependencies.
- `pip uninstall`: Reinstall the package in question.

Inspired by [nvbn](http://github.com/nvbn/)'s [The Fuck](http://github.com/nvbn/thefuck) (no affiliation).

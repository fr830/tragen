#!/bin/bash

sudo pip install -U Sphinx
#git clone https://github.com/rtfd/sphinx_rtd_theme
sudo pip install sphinx_rtd_theme
cd ..
mkdir docs 2>/dev/null
cd docs
#sphinx-quickstart << doc-config
cat ../doc-config | sphinx-quickstart
sphinx-apidoc -f -o . ../tragen
sed -r -i "s/^(html_theme = )(.*)/\1\'sphinx_rtd_theme\'/" conf.py
sed -r -i "15,18 s/^(.{2})(.*)/\2/" conf.py
sed -r -i "18 i\sys.path.insert(0, os.path.abspath('..'))" conf.py
cp ../index.rst -t .
make html

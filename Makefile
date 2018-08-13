LOC := $(shell pwd)
DOC_DIR := ${LOC}"/docs"
SETUP_DIR := ${LOC}/"setup_files"
DOC_CONFIG_FILE := ${DOC_DIR}/"conf.py"
DOC_CONFIG := ${SETUP_DIR}"/doc-config"
DOC_IDX_PAGE := ${SETUP_DIR}"/index.rst"
PKG_FILES := ${LOC}"/package-files.txt"


all: install doc

.PHONY: all install uninstall clean_all doc 

help:
	@echo "**		Tragen Makefile help			**\n"
	@echo "Setting up:"
	@echo " make all 		Will install Tragen and generate documentation."
	@echo " make install 		Will install Tragen."
	@echo " make doc 		Generated HTML documentation under 'docs/_build/html'."
	@echo "\nCleaning:"
	@echo " make uninstall 	Uninstalls Tragen."
	@echo " make clean_all 	Uninstalls Tragen and removes all the generated files for installation and documentation."
	@echo "\n make help 		Displays this help message."


install:
	@echo "\n[*] Installing Python OPC-UA...\n"
	@sudo pip install opcua
	@echo "\n[*] Installing the Tragen package...\n"
	@sudo python ${LOC}/setup.py install --record ${PKG_FILES}
	@echo "\n[+] Tragen successfully installed."


uninstall:
	@echo "\n[*] Uninstalling Python OPC-UA...\n"
	@sudo pip uninstall opcua
	@echo "\n[*] Uninstalling Tragen...\n"
	@if [ -e "${PKG_FILES}" ]; \
	then \
		sudo rm -r $(shell cat ${PKG_FILES}); \
	else \
		sudo python ${LOC}/setup.py install --record ${PKG_FILES}; \
	        sudo rm -r $(shell cat ${PKG_FILES}); \
	fi
	@echo "[+] Tragen successfully uninstalled."


clean_all: uninstall
	@echo "[*] Removing remaining installation files ..."
	@sudo rm -r ${PKG_FILES} dist build *egg-info 2>/dev/null
	@echo "[*] Removing sphinx' insalled packages and documentation files..."
	@sudo pip uninstall Sphinx
	@sudo pip uninstall sphinx_rtd_theme
	@rm -r ${DOC_DIR}
	@echo "\n[+] Cleaning has been successfull."


doc:
	@echo "\n[*] Installing required packages for documentation generation...\n"
	@sudo pip install -U Sphinx
	@sudo pip install sphinx_rtd_theme
	@if [ ! -e ${DOC_DIR} ]; \
	then \
		mkdir ${DOC_DIR} 2>/dev/null; \
	fi
	@echo "\n[*] Configuring the auto-generated documentation...\n"
	@cd ${DOC_DIR} && cat ${SETUP_DIR}/doc-config | sphinx-quickstart
	@cd ${DOC_DIR} && sphinx-apidoc -f -o . ${LOC}/tragen 
	@sed -r -i "s/^(html_theme = )(.*)/\1\'sphinx_rtd_theme\'/" ${DOC_CONFIG_FILE}
	@sed -r -i "15,18 s/^(.{2})(.*)/\2/" ${DOC_CONFIG_FILE}
	@sed -r -i "18 i\sys.path.insert(0, os.path.abspath('..'))" ${DOC_CONFIG_FILE}
	@cp ${SETUP_DIR}/index.rst -t ${DOC_DIR}
	@cd ${DOC_DIR} && make html 
	@echo "\n[+] Doc successfully generated under 'docs/_build/html'."


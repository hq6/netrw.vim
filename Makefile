install:
	@echo 'export PATH=$$PATH:$(shell pwd)/bin' >>  $(HOME)/.bashrc
	@echo "let &runtimepath='$(shell pwd),'.&runtimepath" >>  $(HOME)/.vimrc

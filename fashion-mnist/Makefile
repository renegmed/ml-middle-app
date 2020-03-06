install:
	pip install virtualenv
	pip install chalice opencv-python
	pip install Pillow
.PHONY: install

create:
	virtualenv ~/.virtualenvs/chalice-fashion-mnist
.PHONY: create

source:
	source ~/.virtualenvs/chalice-fashion-mnist/bin/activate
.PHONY: source


create-project: 
	chalice new-project project
.PHONY: create-project



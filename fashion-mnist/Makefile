install:
	pip install virtualenv
	pip install chalice opencv-python
	pip install Pillow
	pip install boto3
	pip install numpy
	pip install opencv-python
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



# EVSE Makefile

# VARIABLES {{{1

EVSE-PATH = ./evse
API-KEY = YOUR_API_KEY

PYTHON3 = python3

# EVSE {{{1

evse:
	cd $(EVSE-PATH); echo "$(API-KEY)" > .env; $(PYTHON3) init.py; cd .. 
	sudo gnome-terminal --window-with-profile=rootshell --sh -c 'cd $(EVSE); flask app.py'
	sleep 5
	xdg-open http://127.0.0.1:5000/

# CLEAN {{{1

clean:

# }}}
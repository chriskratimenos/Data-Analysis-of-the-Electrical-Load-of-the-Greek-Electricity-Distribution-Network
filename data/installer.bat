@ECHO OFF
pip install pipreqs
pipreqs .
pip install -r requirements.txt
del requirements.txt
ECHO Hello you have just downloaded all the dependecies of the program have fun!
PAUSE
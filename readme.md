## How to install Fabric3 on Red Hat distribution ##

1. First, be sure that Python 3.4+ is installed on your computer.
2. Run ```sudo python3 -m pip install Fabric3```
3. Once it's done, be sure it's well installed by simply running ```fab -V```

## How to run Fabric3 ##

1. Clone the repo for automatic deployment ```git clone https://github.com/CSester/automatic-deployment```
2. Go in the repo ```cd automatic-deployment```
3. Edit the examples/config.json file and change the 'hosts', user' and 'password' fields to target your remote machine(s). (field 'hosts' can be either a string or a list of string)
4. Run ```fab -f src/main.py main:examples/config.json```

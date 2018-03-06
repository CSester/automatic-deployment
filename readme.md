## How to install Fabric3 on Red Hat distribution ##

1. First, be sure that Python 3.4+ is installed on your computer.
2. Run "sudo python3 -m pip install Fabric3"
3. Once it's done, be sure it's well installed by simply running "fab -V"

## How to run Fabric3 ##

1. Clone the repo https://github.com/CSester/automatic-deployment
2. Create a new folder examples/ in the root directory
3. Create a new exemples/config.json file with following content:
    {
    "source-commit": "test-branch",
    "source-repository": "git@github.com:CSester/dummy-repo1.git",
    "tmpFolder": ""
    }
4. Run "fab -f src/main.py main:exemples/config.json"

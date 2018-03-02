##How to install Fabric3##

1. First, be sure that Python 3.4+ is installed on your computer.
2. Run "sudo python3 -m pip install Fabric3"
3. Once it's done, be sure it's well installed by simply running "fab -V"

##How to run Fabric3##

1. Go in your project folder
2. Clone the file https://github.com/CSester/automatic-deployment/blob/master/src/main.py in a src/ folder
3. Clone the repo http://idz-admin-app:7990/projects/DPLY/repos/deployment-configurations
4. Create a new folder that respect the following standards: http://idz-admin-app:7990/projects/DPLY/repos/deployment-configurations/browse/readme.md
5. Run "fab -f src/main.py main:/path/to/config/file"

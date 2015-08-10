# Getting Started on Amazon EC2
Use ami-1ecae776 which is the default linux instance provided by AWS. 
You need an instance that has at least 4 cores. I chose c4.xlarge but anything with 4 or more cores will work. Open up the security settings of the EC2 instances to allow HTTP connections on port 80
## After SSH
First update yum and install development tools needed to clone git repos among other things
```sh
$ sudo yum -y update
$ sudo yum -y groupinstall 'Development Tools'
```
Now clone the git repo which contains a setup script to help with the configuration. We'll move that into the home directory and make it executable.
```sh
$ git clone https://github.com/tecmobo/grokplus
$ cd grokplus/setup.sh .
$ chmod +x setup.sh
```
Using the setup.sh helper script we'll do some initial configuration which requires a reboot afterwards
```sh
$ sudo ./setup.sh config
$ sudo reboot
```
After the reboot we'll run the helper script again which will download and install all the prereqs for nupic, couchbase, and for grokplus itself
```sh
$ sudo ./setup.sh nupic
$ sudo ./setup.sh couchbase
$ ./setup.sh env
```
Now we just have to start the server!
```sh
$ ./rungrokplus.sh
```

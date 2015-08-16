# Getting Started on Amazon EC2
Use ami-1ecae776 which is the default linux instance provided by AWS. 
You need an instance that has at least 4 cores. I chose c4.xlarge but anything with 4 or more cores will work. Open up the security settings of the EC2 instances to allow HTTP connections on port 80
## After SSH
Grab the setup script from the repo and make it executable.
```sh
$ wget https://raw.githubusercontent.com/tecmobo/grokplus/master/setup.sh.
$ chmod +x setup.sh
```
Using the setup.sh helper script we'll do some initial configuration which requires a reboot afterwards
```sh
$ sudo ./setup.sh config
$ sudo reboot
```
After the reboot we'll run the helper script again which will download and install all the prereqs for nupic, couchbase, and for grokplus itself
```sh
$ sudo ./setup.sh prereqs
$ ./setup.sh grokplus
```
Now we just have to start the server!
```sh
$ ????
```

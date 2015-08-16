#!/bin/bash

if [ $1 == "config" ]
	then
	#this has to be run as sudo
	if [ $EUID -ne 0 ]
		then echo "Please run as root"
		exit
	fi

	#Setting up the envirnoment so that huge pages are disabled
	echo "if test -f /sys/kernel/mm/transparent_hugepage/enabled; then" >> /etc/rc.local
	echo " echo never > /sys/kernel/mm/transparent_hugepage/enabled" >> /etc/rc.local
	echo "fi" >> /etc/rc.local

	echo "if test -f /sys/kernel/mm/transparent_hugepage/defrag; then" >> /etc/rc.local
	echo "   echo never > /sys/kernel/mm/transparent_hugepage/defrag" >> /etc/rc.local
	echo "fi" >> /etc/rc.local

	# Set the value for the running system
	echo 0 > /proc/sys/vm/swappiness

	# Set the value in /etc/sysctl.conf so swappiness stays after reboot.
	echo '' >> /etc/sysctl.conf
	echo '#Set swappiness to 0 to avoid swapping' >> /etc/sysctl.conf
	echo 'vm.swappiness = 0' >> /etc/sysctl.conf

	echo "Finished configuring system for couchbase. Reboot for configuration to take effect."
	echo "sudo reboot"
fi

if [ $1 == "prereqs" ]
then
	#this has to be run as sudo
	if [ $EUID -ne 0 ]
		then echo "Please run as root"
		exit
	fi
	
	#Make sure development tools are up to date
	yum -y update
	yum -y groupinstall 'Development Tools'
	yum -y install python-devel
	yum -y install openssl-devel
	yum -y install make automake gcc gcc-c++ kernel-devel git-core
	yum -y install cmake
	easy_install numpy

	#Install SQL
	yum install mysql-server -y
	chkconfig mysqld on
	service mysqld start

	#Clone the nupic repository
	git clone https://github.com/numenta/nupic.git
	
	#Build and install NUPIC
	cd nupic
	python setup.py install

	#Return to the root folder
	cd ~

	#Download and install Couchbase
	wget http://packages.couchbase.com/releases/3.0.3/couchbase-server-enterprise-3.0.3-centos6.x86_64.rpm
	rpm --install couchbase-server-enterprise-3.0.3-centos6.x86_64.rpm

	#Download and install C library for Python Couchbase interface
	wget http://packages.couchbase.com/clients/c/couchbase-csdk-setup
	sudo perl couchbase-csdk-setup
fi


if [ $1 == "grokplus" ]
then
	git clone https://github.com/tecmobo/grokplus.git
	cd grokplus/GrokPlus
	pip install couchbase
	pip install pyzmq

	#Return to the root directory
	cd ~
	
	#Configure couchbase
	/opt/couchbase/bin/couchbase-cli cluster-init -c 127.0.0.1:8091  --cluster-init-username=Administrator --cluster-init-password=Password --cluster-init-port=8091 --cluster-init-ramsize=1024
	/opt/couchbase/bin/couchbase-cli bucket-create -c 127.0.0.1:8091 --bucket=default --bucket-type=couchbase --bucket-ramsize=500 --bucket-replica=1 --user=Administrator --password=Password
	
	#Set up path variables for NUPIC and Python
	echo "export NUPIC='/home/ec2-user/nupic'" >> /home/ec2-user/.bashrc
	echo "export NTA=\$NUPIC/build/release" >> /home/ec2-user/.bashrc
	echo "export PYTHONPATH=\$PYTHONPATH:\$NTA/lib/python2.7/site-packages" >> /home/ec2-user/.bashrc
	source ~/.bashrc
fi

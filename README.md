# keyrace_ssh
A couple of utils to host keyrace challenge accessible via ssh 

# Installation example(Ubuntu 14.04)
	# Use this on distinct host only!
	
	apt-get update
	apt-get install inotify-tools
	
	useradd keyrace --create-home
	useradd k --no-create-home
	usermod -aG keyrace
	
	# copy files to /home/keyrace
	
	chown -R keyrace:keyrace /home/keyrace
	chmod g+w /home/keyrace/progress
	
	usermod -s /home/keyrace/shell.sh k
	usermod -d /home/keyrace k
	
	# suid killall
	cp "$(which killall)" /home/keyrace/
	chown k /home/keyrace/killall 
	chmod u+s /home/keyrace/killall
	
	# zsh shared libraries
	mkdir /usr/local/lib/zsh/5.0.7-dev-1/zsh/ -p
	cp /home/keyrace/zsh_modules/* /usr/local/lib/zsh/5.0.7-dev-1/zsh/
	
	# k login without pass
	passwd --delete k
	
	# in /etc/ssh/sshd_config: PermitEmptyPasswords yes
	#                          UseDNS no (optional, makes login faster)
	#                          PrintLastLog no (optional)
	
	echo /home/keyrace/shell.sh >> /etc/shells
	service ssh restart
	# /etc/pam.d/common-auth: add pam_unix.so nullok in the auth string
	# /etc/pam.dpam_unix.so nullok: remove pam_motd.so


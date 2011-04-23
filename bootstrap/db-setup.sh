yes | sudo yum install -y git mysql{,-devel,-server} gcc screen nginx zsh
yes | sudo yum groupinstall "Development Libraries"
sudo service mysqld start
sudo service nginx start
sudo /usr/bin/mysql_secure_installation
sudo easy_install pip virtualenv{,wrapper}
mkdir ~/.virtualenvs
sudo chsh ec2-user -s /bin/zsh
git clone git://github.com/jbalogh/dotfiles.git .dotfiles
cd .dotfiles
for f in * .*; do
    ln -s ~/.dotfiles/$f ~/$f
done

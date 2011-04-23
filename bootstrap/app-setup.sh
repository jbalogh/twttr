yes | sudo yum install -y git mysql{,-devel,-server} gcc screen nginx zsh make
yes | sudo yum groupinstall "Development Libraries"
sudo mv nginx.conf /etc/nginx/
sudo service nginx start
sudo easy_install pip virtualenv{,wrapper}
mkdir ~/.virtualenvs
sudo chsh ec2-user -s /bin/zsh
git clone git://github.com/jbalogh/dotfiles.git .dotfiles
cd .dotfiles
for f in * .*; do
    ln -s ~/.dotfiles/$f ~/$f
done
cd ~

wget ftp://ftp.joedog.org/pub/siege/siege-latest.tar.gz
tar xf siege-latest.tar.gz
cd siege-2.70
./configure
make
sudo make install

mkdir ~/dev/
cd ~/dev
git clone git://github.com/jbalogh/twttr.git camelot
source `which virtualenvwrapper.sh`
mkvirtualenv camelot
cd camelot
cp ~/settings_local.py .
pip install -r reqs.txt
./manage.py run_gunicorn -pgunicorn.pid -w8 --daemon

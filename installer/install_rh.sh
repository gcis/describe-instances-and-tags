sudo yum install git -y
git clone git://github.com/ansible/ansible.git --recursive
cd ./ansible
sudo make
sudo sudo make install
ansible-playbook -i "localhost," -c local ../playbook.yml
sudo yum install git -y
git clone git://github.com/ansible/ansible.git --recursive
cd ./ansible
make rpm
sudo rpm -Uvh ./rpm-build/ansible-*.noarch.rpm
ansible-playbook -i "localhost," -c local playbook.yml
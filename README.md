ansible_db2
===========

db2 modules for use with Ansible

# Installation/usage

Just put the "library" directory in your playbooks directory when executing from a playbook or make sure it is in your local directory when executing with "ansible".
Alternatively you can add the location to your ansible.cfg to use it in playbooks which are in a different directory like so:

```
[defaults]
library = ./library:/usr/share/ansible
```

assuming the rest of your modules reside in /usr/share/ansible.

To check the available options, you can use the provided ***ansible-doc*** program:

```
ansible-doc db2
```
```
ansible-doc db2_instances
```
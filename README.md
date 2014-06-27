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

To check the available options, you can use the provided ***ansible-doc*** program.

## db2

```
> DB2

  Executes db2 commands on databases. When "dbname" is passed, the
  command is executed after connecting to the database as the instance
  user.If not, no connection is made but then command is still
  executed as the instanceuser. The output is returned if no
  outputfile is given.

Options (= is mandatory):

= command
        The command to execute

- dbname
        Name of the database to connect to prior to executing the
        command. If no database is given, the command is executed
        without first connectingto the database. In both cases to
        command is executed as "instanceuser" if it is given or
        "instance" if not.

= instance
        The name of the instance in which to execute the given
        commands.

- instanceuser
        The owner of the instance. The command will get executed as
        this (OS) user.

- outputfile
        Name of the file to save the output of the command to in json
        format. If the file exists and resides in /tmp it is
        overwritten. Else theaction fails. If no outputfile is given,
        the output is returned to ansible.

Requirements:  python > 2.6

- action: db2 instance=my_instance command='db2 list db directory' outputfile=/tmp/output.txt
- action: db2 instance=my_instance dbname=my_cool_db command='db2 get db cfg'
```

## db2_instances

```
> DB2_INSTANCES

  Makes all db2 instances available as ansible facts for later use.
  All the db2 installations are used, provided theyreside in the same
  base directory (see "db2dir" and "db2dirprefix").

Options (= is mandatory):

- db2dir
        Path in which db2 is installed.

- db2dirprefix
        String with which the db2 dirs must start. Useful when the
        "db2dir" not only contains db2 installations.

Requirements:  python > 2.6

- action: db2_instances
- action: db2_instances db2dir=/opt/custom_db2_install db2dirprefix="Version*"
```
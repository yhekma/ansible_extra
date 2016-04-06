#!/usr/bin/python

import os
import re

# -*- coding: utf-8 -*-

# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

DOCUMENTATION = '''
---
module: restore_backup
short_description: Restores a backup created with 'backup=true' using, for instance, the lineinfile module
description:
  - looks for a backup file in the same dir as the file to be restored and renames it to the original.
author: "Yoram Hekma (@yhekma)"
version_added: "2.0"
requirements:
  - python > 2.4
options:
  dest:
    description:
      - The name of the file that needs to be restored.
    required: true
  backup:
    description:
      - Create a backup file including the timestamp information so you can get
        the original file back if you somehow clobbered it incorrectly.
    required: false
    choices: ["yes", "no"]
    default: "no"
  version:
    description:
      - The version of the backup to restore. Can either be "latest" or "earliest". When only 1 backup exists it comes down to the same thing.
    required: false
    choices: ["latest", "earliest"]
    default: "latest"
'''

EXAMPLES = '''
# Restore a backup of /etc/samba/smb.conf, created with, for instance, lineinfile. Prior to restoring, back up the current version
  - name: restore previous state of smb.conf
    restore_backup: dest=/etc/samba/smb.conf backup=yes

# Restore the first made backup of /etc/ntp.conf without making a backup first
  - name: restore first state of /etc/ntp.conf
    restore_backup: dest=/etc/ntp.conf version=earliest
'''


def restore_backup(module, dest, version, original=None):
    dirpath = os.path.dirname(dest)
    filename = os.path.basename(dest)
    file_dict = dict()
    time_regexp = re.compile('^%s\.(\d{4}(:?-\d\d){2}@(:?\d\d:){2}\d\d~$)' % filename)

    for f in os.listdir(dirpath):
        # This will match: "<filename>.2015-05-26@11:50:47~" for instance
        try:
            if original and f == os.path.basename(original):
                continue
            timestring = re.match(time_regexp, f).group(1)
            mtime = time.strptime(timestring, '%Y-%m-%d@%H:%M:%S~')
            file_dict[mtime] = f
        except AttributeError:
            continue

    mtime_list = [i for i in file_dict.keys()]
    mtime_list.sort()
    try:
        if version == 'latest':
            backup_file = file_dict[mtime_list[-1]]
        else:
            backup_file = file_dict[mtime_list[0]]

    except (IndexError, KeyError):
        module.exit_json(stderr='No backup found', changed=False)

    backup_path = os.path.join(dirpath, backup_file)

    try:
        module.atomic_move(backup_path, dest)
    except Exception, e:
        module.fail_json(stderr="%s (renaming %s to %s)" % (e, backup_path, dest), changed=False)

    return dict(changed=True, stderr=str())


def main():
    module = AnsibleModule(
        argument_spec=dict(
            dest=dict(required=True),
            backup=dict(default=False, type='bool'),
            version=dict(default='latest', choices=['latest', 'earliest']),
        )
    )

    dest = module.params['dest']
    version = module.params['version']

    if module.params['backup']:
        original = module.backup_local(dest)

        res_args = restore_backup(module, dest, version, original)

    else:
        res_args = restore_backup(module, dest, version)

    module.exit_json(**res_args)

from ansible.module_utils.basic import *

main()

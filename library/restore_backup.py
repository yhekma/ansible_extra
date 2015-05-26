#!/usr/bin/env python

import os
import re
import json

DOCUMENTATION = '''
---
module: restore_backup
short_description: restores a backup created with 'backup=true' using, for instance, the lineinfile module
description:
  - looks for a backup file in the same dir as the file to be restored and renames it to the original.
author: Yoram Hekma
requirements:
  - python > 2.6
options:
  dest:
    description:
      - The name of the file that needs to be restored.
    required: true
'''

EXAMPLES = '''
  - action: restore_backup dest=/etc/samba/smb.conf
'''

def restore_backup(dest):
    dirpath = os.path.dirname(dest)
    filename = os.path.basename(dest)
    file_dict = dict()

    for f in os.listdir(dirpath):
        # This will match: "<filename>.2015-05-26@11:50:47~" for instance
        if re.match('^%s\.\d{4}(:?-\d\d){2}@(:?\d\d:){2}\d\d~' % filename, f):
            mtime = os.stat(os.path.join(dirpath, f)).st_mtime
            file_dict[str(mtime)] = f

    mtime_list = [float(i) for i in file_dict.keys()]
    mtime_list.sort()
    try:
        latest_backup = file_dict[str(mtime_list[-1])]
    except (IndexError, KeyError):
        return {
            'changed': False,
            'stderr': 'No backup found',
        }

    backup_path = os.path.join(dirpath, latest_backup)

    try:
        os.rename(backup_path, dest)
    except Exception, e:
        return {
            'changed': False,
            'stderr': json.dumps("%s (renaming %s to %s)" % (e, backup_path, dest)),
        }

    return {'changed': True}


def main():
    module = AnsibleModule(
        argument_spec=dict(
            dest=dict(required=True),
        )
    )

    dest = module.params['dest']
    res_args = restore_backup(dest)
    module.exit_json(**res_args)


from ansible.module_utils.basic import *
main()
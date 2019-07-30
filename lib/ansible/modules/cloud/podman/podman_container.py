#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright (c) 2019 Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import json

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.podman.common import run_podman_command

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = """
"""

EXAMPLES = """
"""

RETURN = """
"""


class PodmanContainerManager(object):

    def __init__(self, module, results):

        self.module = module
        self.results = results

        for key, value in module.params.items():
            setattr(self, key, value)

        state = self.state
        if state in ['stopped', 'started', 'present']:
            self.present()
        elif state == 'absent':
            self.absent()

    def present(self):
        self.module.exit_json(msg='present')

    def absent(self):
        container = self._get_container(self.name)
        if container:
            self.remove_container(container['ID'])

    def remove_container(self, container_id, force=False):
        self.results['actions'].append(
            {
                'removed': container_id,
                'force': force,
            }
        )
        self.results['changed'] = True
        if not self.module.check_mode:
            args = ['rm', '--force', container_id]
            rc, out, err = run_podman_command(
                self.module, self.executable, args)

    def inspect_container(self, container=None):
        if container is None:
            container = self.name
        args = ['inspect', container, '--format', 'json']
        rc, container_data, err = run_podman_command(
            self.module, self.executable, args)
        if len(container_data) > 0:
            return json.loads(container_data)
        else:
            return None

    def _get_container(self, name=None):
        if name is None:
            return None
        args = ['ps', '-a', '--format', 'json']
        rc, out, err = run_podman_command(self.module, self.executable, args)
        containers = json.loads(out)

        result = None
        for container in containers:
            if self.name in container['names']:
                result = container
                break

        if result is not None:
            result = self.inspect_container(result['id'])[0]

        return result

        return containers


def main():
    module = AnsibleModule(
        argument_spec={
            'add_host': {'type': 'str'},
            'annotation': {'type': 'str'},
            'attach': {'type': 'str'},
            'blkio_weight': {'type': 'str'},
            'blkio_weight_device': {'type': 'str'},
            'cap_add': {'type': 'str'},
            'cap_drop': {'type': 'str'},
            'cgroup_parent': {'type': 'str'},
            'cidfile': {'type': 'str'},
            'conmon_pidfile': {'type': 'str'},
            'cpu_period': {'type': 'str'},
            'cpu_quota': {'type': 'str'},
            'cpu_rt_period': {'type': 'str'},
            'cpu_rt_runtime': {'type': 'str'},
            'cpu_shares': {'type': 'str'},
            'cpus': {'type': 'str'},
            'cpuset_cpus': {'type': 'str'},
            'cpuset_mems': {'type': 'str'},
            'detach': {'type': 'bool', 'default': False},
            'detach_keys': {'type': 'str'},
            'device': {'type': 'str'},
            'device_read_bps': {'type': 'str'},
            'device_read_iops': {'type': 'str'},
            'device_write_bps': {'type': 'str'},
            'device_write_iops': {'type': 'str'},
            'dns': {'type': 'str'},
            'dns_opt': {'type': 'str'},
            'dns_search': {'type': 'str'},
            'entrypoint': {'type': 'str'},
            'env': {'type': 'str'},
            'env_file': {'type': 'str'},
            'executable': {'type': 'str', 'default': 'podman'},
            'expose': {'type': 'str'},
            'gidmap': {'type': 'str'},
            'group_add': {'type': 'str'},
            'hostname': {'type': 'str'},
            'image_volume': {'type': 'str'},
            'builtin_volume': {'type': 'str'},
            'interactive': {'type': 'bool', 'default': False},
            'image': {'type': 'str'},
            'ipc': {'type': 'str'},
            'kernel_memory': {'type': 'str'},
            'label': {'type': 'str'},
            'label_file': {'type': 'str'},
            'log_driver': {'type': 'str'},
            'log_opt': {'type': 'str'},
            'mac_address': {'type': 'str'},
            'memory': {'type': 'str'},
            'memory_reservation': {'type': 'str'},
            'memory_swap': {'type': 'str'},
            'memory_swappiness': {'type': 'str'},
            'name': {'type': 'str'},
            'net': {'type': 'str'},
            'network': {'type': 'str'},
            'oom_kill_disable': {'type': 'bool', 'default': False},
            'oom_score_adj': {'type': 'str'},
            'pid': {'type': 'str'},
            'pids_limit': {'type': 'str'},
            'pod': {'type': 'str'},
            'privileged': {'type': 'bool', 'default': False},
            'publish': {'type': 'str'},
            'publish_all': {'type': 'bool', 'default': False},
            'quiet': {'type': 'bool', 'default': False},
            'read_only': {'type': 'bool', 'default': False},
            'rm': {'type': 'bool', 'default': False},
            'rootfs': {'type': 'bool', 'default': False},
            'security_opt': {'type': 'str'},
            'shm_size': {'type': 'str'},
            'state': {
                'type': 'str',
                'choices': ['present', 'absent', 'started', 'stapped'],
                'default': 'started'},
            'stop_signal': {'type': 'str'},
            'stop_timeout': {'type': 'str'},
            'storage_opt': {'type': 'str'},
            'subgidname': {'type': 'str'},
            'subuidname': {'type': 'str'},
            'sysctl': {'type': 'str'},
            'systemd': {'type': 'bool', 'default': False},
            'tmpfs': {'type': 'list'},
            'tty': {'type': 'bool', 'default': False},
            'uidmap': {'type': 'str'},
            'ulimits': {'type': 'list'},
            'user': {'type': 'str'},
            'userns': {'type': 'str'},
            'uts': {'type': 'str'},
            'mount': {'type': 'str'},
            'volumes': {'type': 'list'},
            'volumes_from': {'type': 'str'},
            'workdir': {'type': 'str'},
            'sig_proxy': {'type': 'str'},
        },
        required_if=[
            ('state', 'present', ['image']),
        ]
    )

    results = {
        'changed': False,
        'actions': [],
    }

    PodmanContainerManager(module, results)
    module.exit_json(**results)


if __name__ == '__main__':
    main()

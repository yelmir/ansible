{
    "plays": [
        {
            "play": {
                "id": "0050b6da-a27f-7874-25d4-000000000016", 
                "name": "Callback Demo"
            }, 
            "tasks": [
                {
                    "hosts": {
                        "localhost": {
                            "_ansible_no_log": false, 
                            "_ansible_parsed": true, 
                            "changed": true, 
                            "cmd": [
                                "ls", 
                                "-l", 
                                "/tmp"
                            ], 
                            "delta": "0:00:00.013758", 
                            "end": "2018-03-21 14:53:10.643373", 
                            "invocation": {
                                "module_args": {
                                    "_raw_params": "ls -l /tmp", 
                                    "_uses_shell": false, 
                                    "chdir": null, 
                                    "creates": null, 
                                    "executable": null, 
                                    "removes": null, 
                                    "stdin": null, 
                                    "warn": true
                                }
                            }, 
                            "rc": 0, 
                            "start": "2018-03-21 14:53:10.629615", 
                            "stderr": "", 
                            "stderr_lines": [], 
                            "stdout": "lrwxr-xr-x@ 1 root  wheel  11 Jan 10 11:52 /tmp -> private/tmp", 
                            "stdout_lines": [
                                "lrwxr-xr-x@ 1 root  wheel  11 Jan 10 11:52 /tmp -> private/tmp"
                            ]
                        }
                    }, 
                    "task": {
                        "id": "0050b6da-a27f-7874-25d4-000000000018", 
                        "name": "Run a command"
                    }
                }, 
                {
                    "hosts": {
                        "localhost": {
                            "_ansible_no_log": false, 
                            "_ansible_parsed": true, 
                            "changed": true, 
                            "dest": "/tmp/test", 
                            "diff": {
                                "after": {
                                    "path": "/tmp/test", 
                                    "state": "touch"
                                }, 
                                "before": {
                                    "path": "/tmp/test", 
                                    "state": "file"
                                }
                            }, 
                            "gid": 0, 
                            "group": "wheel", 
                            "invocation": {
                                "module_args": {
                                    "attributes": null, 
                                    "backup": null, 
                                    "content": null, 
                                    "delimiter": null, 
                                    "diff_peek": null, 
                                    "directory_mode": null, 
                                    "follow": false, 
                                    "force": false, 
                                    "group": null, 
                                    "mode": null, 
                                    "original_basename": null, 
                                    "owner": null, 
                                    "path": "/tmp/test", 
                                    "recurse": false, 
                                    "regexp": null, 
                                    "remote_src": null, 
                                    "selevel": null, 
                                    "serole": null, 
                                    "setype": null, 
                                    "seuser": null, 
                                    "src": null, 
                                    "state": "touch", 
                                    "unsafe_writes": null, 
                                    "validate": null
                                }
                            }, 
                            "mode": "0644", 
                            "owner": "sdoran", 
                            "size": 0, 
                            "state": "file", 
                            "uid": 501
                        }
                    }, 
                    "task": {
                        "id": "0050b6da-a27f-7874-25d4-00000000001a", 
                        "name": "Create a temp file"
                    }
                }, 
                {
                    "hosts": {
                        "localhost": {
                            "_ansible_no_log": false, 
                            "_ansible_verbose_always": true, 
                            "changed": false, 
                            "failed_when_result": true, 
                            "msg": "This will always fail"
                        }
                    }, 
                    "task": {
                        "id": "0050b6da-a27f-7874-25d4-00000000001c", 
                        "name": "Fail"
                    }
                }
            ]
        }
    ], 
    "stats": {
        "localhost": {
            "changed": 2, 
            "failures": 1, 
            "ok": 2, 
            "skipped": 0, 
            "unreachable": 0
        }
    }
}

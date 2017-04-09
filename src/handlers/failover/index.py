from __future__ import print_function
import base64
import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'vendored'))
import paramiko

private_key_file = '/tmp/id_rsa'


def handler(event, context):
    with open(private_key_file, 'w') as f:
        f.write(base64.b64decode(os.environ['PrivateKeyBase64Encoded']))

    res = {}
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect(
                os.environ['GHEHostName'],
                port=122,
                username='admin',
                key_filename=private_key_file)
        stdin, stdout, stderr = client.exec_command('ghe-repl-promote')
    except Exception as e:
        print(e)
        res.update({'Error': str(e)})
    else:
        res.update({
            'Stdout': stdout.read(),
            'Stderr': stderr.read()})
    finally:
        client.close()
        print(res)
        return res

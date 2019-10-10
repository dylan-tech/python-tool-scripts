import paramiko


def ssh_scp_put(ip, port, user,password,local_file,remote_file):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, 22, 'root', password)
    a = ssh.exec_command('date')
    stdin, stdout, stderr = a
    print(stdout.read())
    sftp = paramiko.SFTPClient.from_transport(ssh.get_transport())
    sftp = ssh.open_sftp()
    sftp.put(local_file, remote_file)


def ssh_scp_get(ip, port, user, password, remote_file, local_file):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, 22, 'root', password)
    a = ssh.exec_command('date')
    stdin, stdout, stderr = a
    # print(stdout.read())
    sftp = paramiko.SFTPClient.from_transport(ssh.get_transport())
    sftp = ssh.open_sftp()
    sftp.get(remote_file, local_file)



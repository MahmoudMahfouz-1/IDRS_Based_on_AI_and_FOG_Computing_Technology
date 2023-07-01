import paramiko


def KillFile(name):
    ip_address = "192.168.1.2"
    username = "pi"
    password = "12345"
    file_name = name

    # Connect to the Raspberry Pi via SSH
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip_address, username=username, password=password)

    # Find the process ID (PID) of the file that is running
    stdin, stdout, stderr = ssh.exec_command("pgrep -f " + file_name)
    pid = stdout.readlines()[0].strip()

    # Kill the process
    ssh.exec_command("kill " + pid)
    print (f"Killed the file with the name {name}")
    # Close the SSH connection
    ssh.close()

flaskName = "app.py"
selfDrivingName = "enhancedLaneDetection.py"

KillFile(selfDrivingName)
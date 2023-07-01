import paramiko


def RunFile(path):
    # SSH connection details
    hostname = '192.168.1.2' # Raspberry Pi's hostname or IP address
    username = 'pi'           # Raspberry Pi's username
    password = '12345'        # Raspberry Pi's password

    # Remote Python file path on the Raspberry Pi
    remote_file_path = path

    # Connect to the Raspberry Pi via SSH
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname, username=username, password=password)

    # Execute the remote Python file on the Raspberry Pi in the background with nohup
    command = f'nohup python {remote_file_path} > /dev/null 2>&1 &'
    stdin, stdout, stderr = client.exec_command(command)
    print(f"Running file with path {path}") 

    # Close the SSH connection
    client.close()
     
slefDrivingPath = '/home/pi/Desktop/Final_Distination/enhancedLaneDetection.py'
flaskPath = '/home/pi/Desktop/Flask/app.py'
RunFile(slefDrivingPath)    


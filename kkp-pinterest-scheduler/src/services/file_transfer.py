import os
import paramiko
from dotenv import load_dotenv

load_dotenv()

class FileTransferService:
    def __init__(self):
        self.hostname = os.getenv('RASPBERRY_PI_HOST')
        self.username = os.getenv('RASPBERRY_PI_USER')
        self.password = os.getenv('RASPBERRY_PI_PASSWORD')
        self.remote_path = os.getenv('RASPBERRY_PI_IMAGE_DIR')

    def transfer_file(self, local_path, remote_filename):
        """
        Transfer a file to the Raspberry Pi using SFTP
        """
        try:
            transport = paramiko.Transport((self.hostname, 22))
            transport.connect(username=self.username, password=self.password)
            
            sftp = paramiko.SFTPClient.from_transport(transport)
            
            remote_path = os.path.join(self.remote_path, remote_filename)
            sftp.put(local_path, remote_path)
            
            sftp.close()
            transport.close()
            
            return remote_path
        except Exception as e:
            print(f"Error transferring file: {str(e)}")
            raise
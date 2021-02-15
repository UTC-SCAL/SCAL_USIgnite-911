"Module to interface with the Exavault FTP servers."

# Standard library
import os
import re

# third party imports
import pysftp
import requests


class ConnectFTPServer:
    """Class to interface with FTP servers using FTP/SFTP protocols.

    Attributes:
        host (string): FTP server path.
        username (string): Username for authentication.
        password (string): Password for authentication.
        host_keys(string): Keys provided by the server host.
    """

    CNOPTS = pysftp.CnOpts()

    def __init__(self,
                 host,
                 username,
                 password=None,
                 host_keys=None,
                 key_file=None,
                 port=22):
        """Initialize ConnectFTP object"""
        self.host = host
        self.username = username
        self.password = password
        self.host_keys = host_keys
        self.key_file = key_file
        self.port = port

    def _connect_to_sftp(self):
        """Create a sftp connection object using environment variables"""
        cnopts = ConnectFTPServer.CNOPTS
        cnopts.hostkeys = self.host_keys
        if self.key_file:
            sftp = pysftp.Connection(self.host,
                                     username=self.username,
                                     private_key=self.key_file,
                                     port=self.port,
                                     cnopts=cnopts)
        else:
            sftp = pysftp.Connection(self.host,
                                     username=self.username,
                                     password=self.password,
                                     port=self.port,
                                     cnopts=cnopts)
        return sftp

    def get_file_from_sftp(self, file_name):
        """Download a file from an sftp server

        Args:
            file_name (string): Full path for target file
        """
        sftp = self._connect_to_sftp()
        sftp.get(file_name)
        sftp.close()

    def upload_file_to_sftp(self, local_path, remote_path):
        """Upload a file to sftp server

        Args:
            local_path (string): local filepath of file to upload
            remote_path (string): remote filepath to put file
        """
        sftp = self._connect_to_sftp()
        sftp.put(local_path, remote_path)
        sftp.close()

    def delete_file_from_sftp(self, directory, file_name):
        """Delete a file from sftp directory
        Args:
            directory (string): ftp directory
            file_name (string): name of file to delete
        """
        sftp = self._connect_to_sftp()
        sftp.chdir(directory)
        sftp.remove(file_name)
        sftp.close()

    def list_sftp_directory(self, dir_name):
        """List files on specified sftp dir

        Args:
            dir_name (string): Full path to directory
        """
        sftp = self._connect_to_sftp()
        sftp.cwd(dir_name)
        dir_contents = sftp.listdir()
        sftp.close()
        return dir_contents

    def list_sftp_directory_attributes(self, dir_name):
        """List files and file attributes on specified sftp dir

        Args:
            dir_name (string): Full path to directory
        """
        sftp = self._connect_to_sftp()
        sftp.cwd(dir_name)
        dir_contents = sftp.listdir_attr()
        sftp.close()
        return dir_contents


class Exavault:
    "Class to interface with the Exavault FTP API."

    ROOT_URL = 'https://api.exavault.com'

    ACTIONS = {
        'authenticate': f'{ROOT_URL}/v1.2/authenticateUser',
        'download_file': f'{ROOT_URL}/v1/getDownloadFileUrl',
        'check_file_exists': f'{ROOT_URL}/v1/checkFilesExist',
        'list_files_in_directory': f'{ROOT_URL}/v1/getResourceList'
    }

    def __init__(self,
                 host=os.environ.get('EXAVAULT_HOST'),
                 api_key=os.environ.get('EXAVAULT_API_KEY'),
                 username=os.environ.get('EXAVAULT_USERNAME'),
                 password=os.environ.get('EXAVAULT_PASSWORD')):
        self.host = host
        self.api_key = api_key
        self.username = username
        self.password = password

    def _build_header(self):
        HEADER = {
            "host": self.host,
            "api_key": self.api_key
        }
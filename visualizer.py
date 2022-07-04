from io import BytesIO
from smb.SMBConnection import SMBConnection

userID = 'airvisual'
password = 'rr4twmgm'
client_machine_name = 'localhost'

server_name = 'AirVisual'
server_ip = '192.168.156.225'

domain_name = ''

conn = SMBConnection(userID, password, client_machine_name, server_name, domain=domain_name, use_ntlm_v2=True,
                     is_direct_tcp=True)

conn.connect(server_ip, 445)

temp_file = BytesIO()

conn.retrieveFile('airvisual', 'latest_config_measurements.json', temp_file)

print(temp_file.getvalue())


conn.close()

# with open('pysmb.py', 'rb') as file:
#     conn.storeFile('remotefolder', 'pysmb.py', file)

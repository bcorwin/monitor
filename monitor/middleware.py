def handler(signum, frame):
    raise Exception()

def send2middleware(message, testMode = False):
    import socket
    import platform
    import signal    
 
    if platform.system() != 'Windows': 
        signal.signal(signal.SIGALRM, handler)
        signal.alarm(10)
 
    r = None
    msg = None
 
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if testMode == False:
        server_ip = socket.gethostbyname('benjeye.ddns.net')
        server_address = (server_ip, 6005)
    else: server_address = ('192.168.1.111', 6005)
    
    try: 
        sock.connect(server_address)
    except: 
        r = 'Timeout'

    if not bool(r):
        try:
            # Send data
            sock.sendall(message.encode())
            # Look for the response
            data = sock.recv(32).decode()
            sock.close()
            r,msg = data.split("|")
        except:
            sock.close()
            r= 'No response'
            
    if not bool(r):
        r = 'Unknown'
    
    if platform.system() != 'Windows': 
        signal.alarm(0)
        
    return((r, msg))

# messages:
## F - force a log or attempt to rerun main loop (depends on state)
## M=1 - set the log period to 1 minutes (value required)
## C - turns off server permanently
## R=var_name - get the averages that are currently in memory for var_name

# Example usage:
## response, msg = send2middleware("f")
## response, msg = send2middleware("m=1")

'''
+-----------------------------------------------+
|send2middleware(msg, testMode = False)        |
| -msg (command) to send to middleware        |
| -testMode = True means you're running locally    |
+-----------------------------------------------+


Msg - Description

Example call = Response

----------------------------------------------------------------

F - Force a log or attempt to rerun main loop (depends on state)

send2middleware("f") = ('Success', 'Forcing log...')

----------------------------------------------------------------

M=n - Set the log period to n minutes

send2middleware("m=1")    = ('Success', 'Changed now minLog=1')    #Returns new minLog value
send2middleware("m")    = ('Fail', 'Number needed. minLog=15')    #Returns current minLog value
send2middleware("m=")    = ('Fail', 'Number needed. minLog=15')    #Returns current minLog value

----------------------------------------------------------------

R=var_name - Get the averages that are currently in memory for var_name

send2middleware("r=temp_amb")    = ('Success', 'temp_amb:75.8')
send2middleware("r")        = ('Success', "{'temp_unit': 'F', 'inst")    #Attempts to return all vars; will come back truncated
send2middleware("r=light_beer")    = ('Fail', 'light_beer is not valid.')
send2middleware("r=")        = ('Fail', ' is not valid.')

----------------------------------------------------------------
!!DEFUNCT!!
C - Turns off server permanently, will require access to the server to turn it back on

send2middleware("c", True)    = ('Success', 'Cancelled.')

----------------------------------------------------------------
'''

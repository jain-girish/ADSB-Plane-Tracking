import socket, select, sys, time
s_to_receive = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port=int(sys.argv[2])
ip=str(sys.argv[1])
s_to_receive.connect((ip,port))
while True:
    msg1=s_to_receive.recv(2048)
    msg1=msg1.decode("utf-8")
    t=str(time.perf_counter())
    t = t+"           " + msg1
    print(t,flush=True)
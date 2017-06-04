#the modules required
import socket, struct, sys

#Connects to the server using TCP protocol,
#negotiates extra features and encryption keys
#and receives the server's UDP port and an identity token
#After that, calls talk_with_server()
#
#Parameters: server_host = target server hostname/IP address
#            server_tcpport = target server TCP port
def start_connection(server_host, server_tcpport):

    #create a tuple that contains host and port
    address = (server_host, server_tcpport)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(address)
    s.sendall("HELLO")
    data = s.recv(64)
    s.close()

    print 'Received: \r\n', repr(data)

    #remove '\r' and '\n' (the last 2 characters)
    data = data[:-2]
    #split the string to its substrings
    data = data.split(" ")
    #now data is contains something like ['HELLO', 'abcde' 12345']
    
    #talk_with_server() requires identity token and UDP address
    talk_with_server(data[1], server_host, int(data[2]))

    return


#This function is used for communication with the server.
#First, this function initiates UDP messaging by sending the first message.
#After the server has replied, this function replies with the same words in reverse order.
#Next, a random number of messages and are received from the server.
#And finally, a message which tells the exchange is finished, is received.
#
#Parameters: token = CID
#            server_host = target server hostname/IP address
#            server_udpport = target server UDP port
def talk_with_server(token, server_host, server_udpport):

    #target address for messaging
    address = (server_host, server_udpport)
	
    #create an UDP socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	
    #the first UDP message
    message_out = "Hello from " + token
 
    #Structure of UDP message = CID     ACK  EOM  Data remaining  Content length Content
    #              data types:  char[8] Bool Bool unsigned short  unsigned short char[64]

    #create a packed UDP message with all the required information as shown above
    data_out = struct.pack('>8s??HH64s', token, True, False, 0, len(message_out), message_out)
    
    s.sendto(data_out, address)

    while True:

        #receive a message from addr
        data_in, addr = s.recvfrom(1024)
        print 'Received a message from %s:' % str(addr)

        #unpack the message
        token, ack, eom, remaining, length, message_in = struct.unpack('>8s??HH64s', data_in)
        print(message_in)

        #if the last message (end of message = true), break the loop
        if eom == True:
            break
        
        #remove the null padding
        message_in = message_in.strip('\x00')
        
        #create a list containing all the words from the received message
        message_out = message_in.split(' ')
        #reverse their order
        message_out = reversed(message_out)
        #and create a string from the list
        message_out = ' '.join(message_out)

        #show the target IP address and port + the message
        print("Sending message to %s: \n%s" % ((socket.gethostbyname(server_host), server_udpport), message_out))

        #pack the message and send it
        data_out = struct.pack('>8s??HH64s', token, True, False, 0, len(message_out), message_out)
        s.sendto(data_out, address)
    

def main():
    #shows the required sequence of information this program requires
    USAGE = 'usage: %s <server address> <server port>' % sys.argv[0]

    #try to get the host and port from command line arguments
    try:
        server_host = str(sys.argv[1])
        server_tcpport = int(sys.argv[2])
    except (IndexError, ValueError):
        sys.exit(USAGE) #if something fails, show USAGE and exit

    start_connection(server_host, server_tcpport)

    print 'Everything worked as expected! Good bye!'


#if and when this module is executed as the main program, start main().
if __name__ == '__main__':
    main()

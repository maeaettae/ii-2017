#the modules required
import socket, sys


#Prints help
def display_help():
    print '\nhelp :('

#Asks the required inputs from user
#This function is used if hostname and port number are not provided as command line arguments.
#Returns the hostname and the port number given by the user.
def set_host_and_port():
    
    #ask the necessary information politely from user (use a loop!) :) 
    #if user reluctant: sys.exit(0)
    #if user confused: display_help()
    #if user done: break 
    #if user clumsy or idiotic: print what went wrong and ask again

    #OPTIONAL: ask if the user wants to use default values = the right values for this project

    return host, port

#Connects to the server using TCP protocol,
#negotiates extra features and encryption keys
#and receives the server's UDP port and an identity token
#
#Parameters: address = a tuple containing the values of host and port
#[more parameters will be added later]
#Returns the server's UDP port, identity token and encryption key
def start_connection(address):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(address)
    s.sendall("HELLO")
    data = s.recv(64)
    print 'Received r\n', repr(data)
    s.close()
    #return port_udp_server, token, enc_key


#This function is used for communication with the server.
#First, this function initiates UDP messaging by sending the first message.
#After the server has replied, this function replies with the same words in reverse order.
#Next, a random number of messages and are received from the server.
#And finally, a message which tells the exchange is finished, is received.
#
#Parameters: address = a tuple containing server IP address and UDP port
#[parameters will be updated later]
def talk_with_server(address):

    return

    #communicate
    #end communication

    #no need to return anything, possibly
    

def main():
    #shows the required sequence of information this program requires
    USAGE = 'usage: %s <server address> <server port>' % sys.argv[0]

    #try to get the host and port from command line arguments
    try:
        server_host = str(sys.argv[1])
        server_tcpport = int(sys.argv[2])
    except (IndexError, ValueError):
        sys.exit(USAGE) #if something fails, show USAGE and exit

    #create a tuple that contains host and port
    address = (server_host, server_tcpport)


    start_connection(address)

    print 'Everything worked as expected! Good bye!'


#if and when this module is executed as the main program, start main().
if __name__ == '__main__':
    main()

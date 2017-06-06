#the modules required
import random, socket, struct, sys

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

    print 'Establishing connection to %s.' % str((server_host, server_tcpport))

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(address)

    print 'Connection successful.'

    message = "HELLO ENC\r\n"

    #generate a list of keys
    key_list = key_generator()
    
    #covert the list into a string and add it to the message
    message += ''.join(key_list)
    message += '.\r\n'

    s.sendall(message)
    data = s.recv(2048)
    s.close()

    #split the received string to its substrings
    data = data.split('\r\n')

    hello = data[0].split(' ')

    #now hello contains something like ['HELLO', 'abcde' 12345']
    del data[0]

    #add '\r\n' to each key
    for k in range(0,len(data)):
        data[k] = data[k] + "\r\n"

    #data contains now a list of decryption keys received from the server

    #talk_with_server() requires identity token (hello[1]), server host address 
    #and UDP port(hello[2]) and both sent and received keylists
    talk_with_server(hello[1], server_host, int(hello[2]), key_list, data)

    return

#This function is responsible for creating a list of randomly generated 
#encryption keys for the server. The encryption exists only for the
#purposes of this course work and is inefficient in real life,
#beacause the connection is insecure and the keys are sent in plaintext.
def key_generator():

    #create a new list with space for 20 keys
    new_list = []

    key = ""
    
    #20 keys are needed
    for i in range(0,20):
        #and each has 64 characters (bytes)
        for j in range(0,64):
            #hexadecimal letters are required
            choose = random.randint(0,2)
            if choose == 0: #use a random number 0-9
                key+=chr(random.randint(48,57)) #ASCII 48-57
            elif choose == 1: #use a lowercase letter a-f
                key+=chr(random.randint(97,102)) #ASCII 97-102
            else: #use an uppercase letter A-F
                key+=chr(random.randint(65,70)) #ASCII 65-90
        
        key += '\r\n'
        #add the generated key to the list
        new_list.append(key)
        #erase key
        key = ""

    return new_list


#This function is used for communication with the server.
#First, this function initiates UDP messaging by sending the first message.
#After the server has replied, this function replies with the same words in reverse order.
#Next, a random number of messages and are received from the server.
#And finally, a message which tells the exchange is finished, is received.
#
#Parameters: token = CID
#            server_host = target server hostname/IP address
#            server_udpport = target server UDP port
#            key_list = list of encryption keys
def talk_with_server(token, server_host, server_udpport, enc_keys, dec_keys):

    #target address for messaging
    address = (server_host, server_udpport)
	
    #create an UDP socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	
    #the first UDP message
    message_out = "Hello from " + token

    #encrypt the message
    message_out = cipher(message_out, enc_keys)
 
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
        
        #remove the null padding
        message_in = message_in.strip('\x00')

        if eom == False:
            #decrypt the message
            message_in = cipher(message_in, dec_keys)
        print(message_in)

        #if the last message (end of message = true), break the loop
        if eom == True:
            break
                
        #create a list containing all the words from the received message
        message_out = message_in.split(' ')
        #reverse their order
        message_out = reversed(message_out)
        #and create a string from the list
        message_out = ' '.join(message_out)

        #show the target IP address and port + the message
        print("Sending message to %s: \n%s" % ((socket.gethostbyname(server_host), server_udpport), message_out))

        #encrypt the message
        message_out = cipher(message_out, enc_keys)

        #pack the message and send it
        data_out = struct.pack('>8s??HH64s', token, True, False, 0, len(message_out), message_out)
        s.sendto(data_out, address)
    
#This function encrypts or decrypts the received plaintext with the received key using 
#one-time pad encryption. The encryption/decryption is done by XORing the numeric value 
#of each character in the plaintext/ciphertext with the numeric value of the corresponding 
#character in the key.
#Returns the resulting ciphertext.
def cipher(text, key_list):
    
    #for k in key_list:
    #    print(len(repr(k)))    
    #print(repr(key_list[0]))
    #print(len(key_list[0]))

    #convert the string into a list
    text = list(text)

    #take the first key    
    key = key_list[0]

    #and discard it from the list
    del key_list[0]   

    #encrypt/decrypt
    for c in range(0,len(text)):
        text[c] = chr(ord(text[c]) ^ ord(key[c]))
    
    text = ''.join(text)

    return text

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

    print 'Good bye!'


#if and when this module is executed as the main program, start main().
if __name__ == '__main__':
    main()

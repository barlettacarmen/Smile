 #       ___
 #      /   /\
 #     /___/  \
 #     \___\  /_      \_\_\_
 #    /   /\\/ /|    \_
 #   /___/  \_/ |   \_\_\_    \_ \_   \_  \_     \_\_\_
 #   \   \  / \ |        \_  \_\_\_  \_  \_     \_\_
 #    \___\//\_\|  \_\_\_   \_   \_ \_  \_\_\_ \_\_\_
 #     /___/  \
 #     \   \  /
 #      \___\/
 #
 # Copyright 2017 Fabiola Casasopra, Carmen Barletta, Gabriele Iannone, Guido Lanfranchi, Francesco Maio
 #
 # Licensed under the Apache License, Version 2.0 (the "License");
 # you may not use this file except in compliance with the License.
 # You may obtain a copy of the License at
 #
 # 	http://www.apache.org/licenses/LICENSE-2.0
 #
 # Unless required by applicable law or agreed to in writing, software
 # distributed under the License is distributed on an "AS IS" BASIS,
 # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 # See the License for the specific language governing permissions and
 # limitations under the License.

import socket
import firstapp as ft 

def Main():
		host = '10.79.3.204'
		port = 5001
		
		mySocket = socket.socket()
		mySocket.connect((host,port))
		
		mySocket.send("ciao".encode())
		#message = input(" ? ")
		message=""
		while message != 'q':
				
				data = mySocket.recv(1024).decode()
				
				if data=="gente":
					event=ft.lookForEvent()
				
				print ('Received from server: ' + data)
				
				#message = input(event)
				mySocket.send(event.encode())
		mySocket.close()
 
if __name__ == '__main__':
	Main()










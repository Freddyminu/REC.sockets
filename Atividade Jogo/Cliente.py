from socket import *

class Client: 
   def __init__(self) -> None:
      self.score = 0
      self.state_num = 0
      self.health = 100
      self.client = None
      self.connection = None

   def start_client(self):
      host = 'localhost'
      port = 12002
      connection = socket(AF_INET, SOCK_STREAM)
      connection.connect( (host,port) )
      

      
      

   


if __name__ == '__main__':
   Client().start_client()
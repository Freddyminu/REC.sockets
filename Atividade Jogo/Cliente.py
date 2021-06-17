from socket import *
from enum import Enum
import time
from NameGenerator import NameGenerator
class Messages(Enum):
   START = "START"

class GameMessage():
   def __init__(self, args):
      self.points = args[-1]
      self.life = args[-2]
      self.message = args[0]
      
      if len(args) == 4:
         self.arg = args[1]

class GameClient():
   host = 'localhost'
   port = 12007
   client = None
   running = False

   def __init__(self):
      self.connect()
      self.name_generator = NameGenerator()
      self.game_loop()

   def connect(self):
      tries = 5
      self.client = socket(AF_INET, SOCK_STREAM)

      while tries > 0:
         try:
            self.client.connect((self.host, self.port))
            return
         except Exception:
            tries -= 1
            time.sleep(1)
   
   def send_message(self, msg):
      msg_bytes = bytes(msg, encoding='utf8')
      
      self.client.sendall(msg_bytes)

   def receive_message(self):
      text = self.client.recv(1024)
      
      if len(text) > 0:
         text = str(text, "utf-8")
         splitted_text = text.split(";")
         print(splitted_text)

         if len(text) > 3:
            return GameMessage(splitted_text)
         elif len(text) == 2:
            return text[1]
         
            
   def game_loop(self):
      commands = {
         "NOTHING_HAPPENED": self.nothing_happened,
         "MONSTER_ATTACK": self.monster_attack,
         "TAKE_CHEST": self.take_chest,
         "BOSS_EVENT": self.boss_event
      }

      while True:
         # Inicializar 
         if not self.running:
            print("Você quer iniciar o jogo?(S/N)")
            response = str(input())

            if response.lower() == 's':
               print("O jogo começou!")

               self.send_message("START")
               self.running = True

         payload = self.receive_message()

         print(payload.message);

         commands[payload.message]()
   
   
   def nothing_happened(self):
      self.walk()

   def monster_attack(self):
      
      print("monster attack")

   def take_chest(self):
      print("Voce deseja pegar o bau: s or n")
      
      msg = "NO"
      response = str(input()).lower()

      if response == 's':
         self.send_message("YES")
         treasure = self.receive_message()
         print('Você %s %s pontos' % (treasure, "recebeu" if treasure > 0 else "perdeu"))
      else:
         self.send_message("NO")

      self.walk()
         
      print("take chest")
      
   def boss_event(self):
      print("Um terrivel monstro aparece na sua frente!")
      print("E O SEU NOME É ", self.name_generator.generate())
      
      
      
   def walk(self):
      print("Andando para proxima sala")
      self.send_message("WALK")

def menu():
   
   return 0;


if __name__ == '__main__':
   GameClient()
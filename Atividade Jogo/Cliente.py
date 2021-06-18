from socket import *
from enum import Enum
import time
from NameGenerator import NameGenerator
class Messages(Enum):
   START = "START"

class GameMessage():
   arg = None
   def __init__(self, args):
      self.points = args[-1]
      self.life = args[-2]
      self.message = args[0]
      
      if len(args) == 4:
         self.arg = args[1]

   def __str__(self):
        return "[{},{},{},{}]".format(self.message, self.arg, self.life, self.points)

class GameClient():
   host = 'localhost'
   port = 12003
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
            print("Trying to connect with server in port {} ".format(self.port))
            self.client.connect((self.host, self.port))
            return
         except Exception:
            tries -= 1
            time.sleep(1)
      
      raise Exception("Impossible to reach server game")
   
   def send_message(self, msg):
      msg_bytes = bytes(msg, encoding='utf8')
      
      self.client.sendall(msg_bytes)

   def receive_message(self):
      text = self.client.recv(1024)
      
      if len(text) > 0:
         text = str(text, "utf-8")
         splitted_text = text.split(";")

         if len(text) > 3:
            game_message = GameMessage(splitted_text)
            
            if game_message.message == "WIN":
               print("Parabens voce ganhou o jogo do seculo")
               self.client.close()
               exit()
            elif game_message.message == "GAME_OVER":
               print("GAME OVER")
               self.client.close()
               exit()
               
            return game_message
            
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

         if payload is not None:
            print("[VIDA: {} | PONTOS: {}]".format(payload.life, payload.points));

            commands[payload.message](payload)

         time.sleep(1.5)
   
   
   def nothing_happened(self, payload):
      print("Você entra no quarto e nada acontece")
      self.walk()

   def monster_attack(self, payload):
      monster_killed=True
      current_life= int(payload.life)
      door_amount = int(payload.arg)
      print("Você entra em uma sala com {} portas, escolha uma porta para atacar(0-{})".format(int(door_amount)+1, door_amount))
      
      door = int(input())

      while door < 0 or door > door_amount:
         print("Escolha uma porta valida")
         door = int(input())
      
      print("Você escolhe a porta {} e ...".format(door))

      self.send_message(str(door))
      result = self.receive_message()

      if result.message == "MONSTER_ATTACKED":
         print("O monstro te ataca e perde {} pontos de vida".format(current_life-int(result.life)))
         print("Escolha mais uma porta")
      else:
         print("O monstro foi derrotado")
         monster_killed=False

      current_life=result.life

       
      self.walk()

   def take_chest(self, payload):
      print("Voce deseja pegar o bau: s or n")
      
      msg = "NO"
      choose = str(input()).lower()

      if choose == 's':
         self.send_message("YES")
         treasure = self.receive_message()
         print('Você %s %s pontos' % ("recebeu" if int(treasure.arg) > 0 else "perdeu", treasure.arg))
      else:
         print("Você é rico demais para isso e deixa o bau de lado")
         self.send_message("NO")
         self.receive_message()

      self.walk()
      
   def boss_event(self, payload):
      current_life= int(payload.life)
      boss_name = self.name_generator.generate()
      print('Um terrivel {} aparece na sua frente!'.format(boss_name))

      print('Você deseja atacar(a) ou fugir(f)')

      choose = str(input()).lower()

      if choose == 'a':
         print("Você ataca tenta atacar o {}".format(boss_name))
         self.send_message("FIGHT")
         result = self.receive_message()

         life_diff = current_life-int(result.life)
         if result.message == "BOSS_DEFEATED":
            print("Você ESMAGOU o {}!".format(boss_name))
         else:
            print("Você perdeu o esquerdo braço mas ficou bem :) ... [-{} VIDA]".format(life_diff))

      else:
         self.send_message("RUN")
         result = self.receive_message()
         print("Você corre do monstro mas você pisou em um lego e perdeu ", current_life-int(result.life))
      
      self.walk()
      
   def walk(self):
      print("Andando para proxima sala")
      self.send_message("WALK")

def menu():
   
   return 0;


if __name__ == '__main__':
   GameClient()
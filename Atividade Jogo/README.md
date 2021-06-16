# RecPG - Jogo da Aula de Redes

Nesta aventura você precisará implementar um cliente TCP que se conecte com o servidor do jogo já pronto. Pode utilizar a linguagem que quiser, mas recomendo alguma linguagem script (Python, Ruby, JavaScript, ...) para facilitar o desenvolvimento.

O jogo é uma aventura do herói, que começa com 100 pontos de vida, e caminha por diversas salas até chegar na ultima (sala numero 20) OU alcançar 500 pontos. O seu objetivo não é fazer com que o herói ganhe (mas bonus para quem tentar fazer a melhor jogada), mas sim fazer com que a aventura seja possivel, ou seja, que o cliente consiga se comunicar completamente com o servidor.

Para cada sala que o herói caminha, pode acontecer algum desse eventos:
- Monstro escondido
- Baú de tesouro
- Chefão
- Nada

### Formato das mensagems

Toda mensagem do servidor segue o formato `MENSAGEM;ARGUMENTO;VIDA;PONTUAÇÃO`, onde `MENSAGEM` é o código do event atual, `ARGUMENTO` é o argumento desse evento (se tiver, normalmente é um numero), `VIDA` é a vida atual do herói e `PONTUAÇÃO` é a pontuação atual do herói. Perceba que tudo é separado por `;`.

Exemplos de mensagem do servidor:

- `MONSTER_ATTACK;5;100;0` -- Tem um argumento, no caso o 5
- `MONSTER_KILLED;60;200`
- `NOTHING_HAPPENED;50;10`
- `CHEST_VALUE;1000;50;10` -- Tem argument, no caso 1000
- `ESCAPED;90;44`

### Monstro Escondido

Neste evento, o servidor vai enviar `MONSTER_ATTACK;N`, onde `N` é o numero de portas que apareceram, que vai de 2 a 5. A sua missão é adivinhar alguma porta para atacar o monstro, enviando pro servidor um número entre 0 e `N`.
Se acertar, o herói ataca o monstro e ganha pontos. Se perder, perde vida. O servidor envia `MONSTER_KILLED` ou `MONSTER_ATTACKED` para cada evento, respectivamente.

### Baú encontrado

Quando encontrar o baú,, evento `TAKE_CHEST`, o herói pode pegar ou ignorar. Se pegar, enviando `YES` pro servidor, é possível que tenha algo legal ou algo ruim, aumentando ou perdendo pontuação. O servidor envia `CHEST_VALUE;N` sendo `N` a quantidade de pontos que o herói ganhou ou perdeu.
Se o herói decidir ignorar o baú, enviando `NO`, nada acontece e o servidor envia `SKIPPING_CHEST`.

### Chefão

As vezes é possível aparecer um chefão com a mensagem `BOSS_EVENT`. Esse você tem duas opções, lutar ou fugir.
Para fugir é só enviar `RUN`, mas você vai perder um pouco de vida por isso, e o servidor envia `ESCAPED`.
Se decidir lutar, enviando `FIGHT`, o herói vai enfrentar o chefão. Quanto mais vida o herói tiver, maior é a chance dele vencer. Se vencer, o servidor retorna `BOSS_DEFEATED`, o herói ganha pontos e pode perder um pouco de vida.
Se perder, o servidor envia `FAILED_BOSS_FIGHT` e o herói perde bastante vida!

### Nada


Não acontece nada, com a mensagem `NOTHING_HAPPENED`.


## Execução

Quando o jogo iniciar, o herói precisa enviar `START` para que o servidor saiba que o herói está pronto.
Também é necessário que o nosso herói envie `WALK` sempre que passou por uma sala para sinalizar ele está pronto para a proxima.

## Final de Jogo

Em vez de enviar algum evento como os descritos anteriormente, o servidor pode enviar `WIN` ou `GAME_OVER`, para quando o herói ganhou ou perdeu o jogo, respectivamente.

O formato é o seguinte:
`WIN ou GAME_OVER;SALAS;VIDA;PONTUACAO`, onde `SALAS` é quantas salas o herói conseguiu alcançar.

## Requerimentos do projeto

1. O cliente precisa processar todas as possíveis mensagens do servidor, sem dar problemas
2. O cliente precisa mostrar os eventos que acontecem de alguma forma, seja apenas mostrando linhas como "Apareceu um Tesouro!!!" ou algo mais interessante
3. O cliente não precisa ser bom no jogo, apenas suportar. Mas vamos considerar quem tentou fazer algo inteligente ;)
4. Pode ser totalmente automatico ou manual, mas se for manual deve ter mensagens amigáveis pro usuário entender o que está acontecendo.


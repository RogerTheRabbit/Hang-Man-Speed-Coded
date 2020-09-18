import socket

# Hangman - Coded in 1 hour 33 mins
# Notes:
#   - Only guess one letter at a time
#   - Can only play locally even though I use sockets because
#       I didn't want to use my public IP for anything.

HOST = "127.0.0.1"
PORT = 65432
BUFFER_SIZE = 4096
GAME_OVER = "Game Over!"

def validPlayerType(input):
    return input.lower() == "m" or input.lower()  == "g"

def checkGuess(wordToGuess, guess, currentGuesses):

    output = ""

    for x in range(len(wordToGuess)):
        if(wordToGuess[x] == guess):
            output += guess
        else:
            output += currentGuesses[x]
    if(output == wordToGuess):
        return GAME_OVER
    return output

def guesser(ip, port, name):
    print("You are now a gusser")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    data = s.recv(BUFFER_SIZE).decode("utf-8")
    while data != GAME_OVER or not data:
        print(data)
        s.sendall(input("Guess: ").encode("utf-8"))
        data = s.recv(BUFFER_SIZE).decode('utf-8')
    print("Game over!")
    s.sendall("Done playing".encode("utf-8"))
    s.close()
    print('Shutting down...')

def manHanger(wordToGuess):
    print("You are now a Man Hanger")
    # print("Tell players to connect to ", HOST + ":" + PORT)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    data = ""
    with conn:
        print('Connected by', addr)
        currentGuesses = "-" * len(wordToGuess)
        conn.sendall(currentGuesses.encode('utf-8'))
        while currentGuesses != GAME_OVER or not data:
            data = conn.recv(BUFFER_SIZE).decode('utf-8')
            currentGuesses = checkGuess(wordToGuess, data, currentGuesses)
            conn.sendall(currentGuesses.encode("utf-8"))
    s.close()
    print("Shutting down...")

if __name__ == "__main__":
    playerType = ""
    while not validPlayerType(playerType):
        playerType = input("Man Hanger or Guesser?(m|G): ")
    if(playerType == "m"):
        wordToGuess = input("Make word to guess: ").lower()
        manHanger(wordToGuess)
    elif (playerType == "g"):
        name = "Jeff Bezos"
        guesser(HOST, PORT, name)

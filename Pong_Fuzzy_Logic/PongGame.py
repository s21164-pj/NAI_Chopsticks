import pygame
import random

# Klatki na sekunde
FPS = 60

# Określ wysokość i szerokość okienka
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 400

# Rozmiar rakietki pong-a
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 20  # co by miał trudniej
# Dystans od krawędzi okna
PADDLE_BUFFER = 15

# Wielkość piłki
BALL_WIDTH = 10
BALL_HEIGHT = 10

# Szybkość rakietki i piłki
PADDLE_SPEED = 3
BALL_X_SPEED = 3
BALL_Y_SPEED = 2

# Kolory piłki i rakietki w formacie RGB
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
# Inicjalizacjia okna gry
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))


# Paddle 1 - Chłopak(AI) się uczy
# paddle 2 - Przeciwnik AI

# Inicjalizacja piłki
def drawBall(ballXPos, ballYPos, BallCol):
    # Utwórz mały kwadrat i go narysuj
    ball = pygame.Rect(ballXPos, ballYPos, BALL_WIDTH, BALL_HEIGHT)
    pygame.draw.rect(screen, BallCol, ball)


def drawPaddle1(paddle1YPos):
    # Stworzenie bytu samej rakietki
    paddle1 = pygame.Rect(PADDLE_BUFFER, paddle1YPos, PADDLE_WIDTH, PADDLE_HEIGHT)
    # Wyświetlenie jej
    pygame.draw.rect(screen, YELLOW, paddle1)


def drawPaddle2(paddle2YPos):
    # Stworzenie bytu samej rakietki
    paddle2 = pygame.Rect(WINDOW_WIDTH - PADDLE_BUFFER - PADDLE_WIDTH, paddle2YPos, PADDLE_WIDTH, PADDLE_HEIGHT)
    # Wyświetlenie jej
    pygame.draw.rect(screen, WHITE, paddle2)


# Aktualizacja pozycji piłki, za pomocą poniższych zmiennych takich jak:
# > pozycja rakietek
# > pozycja piłki X i Y
# > kierunek toru piłki
def updateBall(paddle1YPos, paddle2YPos, ballXPos, ballYPos, ballXDirection, ballYDirection, dft, BallColour):
    dft = 7.5
    ballXPos = ballXPos + ballXDirection * BALL_X_SPEED * dft
    ballYPos = ballYPos + ballYDirection * BALL_Y_SPEED * dft
    Missed = False
    NewBallColor = BallColour;
    # Checker kolizji
    if (
            ballXPos <= PADDLE_BUFFER + PADDLE_WIDTH and ballYPos + BALL_HEIGHT >= paddle1YPos and ballYPos - BALL_HEIGHT <= paddle1YPos + PADDLE_HEIGHT and ballXDirection == -1):
        ballXDirection = 1
        NewBallColor = BLUE
    # Kolejny cheker - Sprawdza, czy piłka wymineła rakietke przeciwnika
    elif (ballXPos <= 0):
        ballXDirection = 1
        # Jeśli player 1 lub player 2 minie piłkę dostaje minusowy score
        Missed = True
        NewBallColor = RED
        return [Missed, ballXPos, ballYPos, ballXDirection, ballYDirection, NewBallColor]

    if (
            ballXPos >= WINDOW_WIDTH - PADDLE_WIDTH - PADDLE_BUFFER and ballYPos + BALL_HEIGHT >= paddle2YPos and ballYPos - BALL_HEIGHT <= paddle2YPos + PADDLE_HEIGHT):
        ballXDirection = -1
        NewBallColor = WHITE
    elif (ballXPos >= WINDOW_WIDTH - BALL_WIDTH):
        ballXDirection = -1
        NewBallColor = WHITE
        return [Missed, ballXPos, ballYPos, ballXDirection, ballYDirection, NewBallColor]

    if (ballYPos <= 0):
        ballYPos = 0;
        ballYDirection = 1;
    elif (ballYPos >= WINDOW_HEIGHT - BALL_HEIGHT):
        ballYPos = WINDOW_HEIGHT - BALL_HEIGHT
        ballYDirection = -1
    return [Missed, ballXPos, ballYPos, ballXDirection, ballYDirection, NewBallColor]


# Aktualizowanie pozycji rakietki
def updatePaddle1(action, paddle1YPos, dft):
    # Zastosuj akcje:  'S':stój, 'U':góra, 'D':dół
    dft = 7.5
    if (action == 'U'):
        paddle1YPos = paddle1YPos - PADDLE_SPEED * dft
    if (action == 'D'):
        paddle1YPos = paddle1YPos + PADDLE_SPEED * dft

    if (paddle1YPos < 0):
        paddle1YPos = 0
    if (paddle1YPos > WINDOW_HEIGHT - PADDLE_HEIGHT):
        paddle1YPos = WINDOW_HEIGHT - PADDLE_HEIGHT
    return paddle1YPos


def updatePaddle2(paddle2YPos, ballYPos, dft):
    dft = 7.5
    # Przesuń rakietkę w dół, jeśli piłka jest, niżej niż rakietka przeciwnika
    if (paddle2YPos + PADDLE_HEIGHT / 2 < ballYPos + BALL_HEIGHT / 2):
        paddle2YPos = paddle2YPos + PADDLE_SPEED * dft
    # Przesuń rakietkę w górę, jeśli piłka jest, wyżej niż rakietka przeciwnika
    if (paddle2YPos + PADDLE_HEIGHT / 2 > ballYPos + BALL_HEIGHT / 2):
        paddle2YPos = paddle2YPos - PADDLE_SPEED * dft
    if (paddle2YPos < 0):
        paddle2YPos = 0
    if (paddle2YPos > WINDOW_HEIGHT - PADDLE_HEIGHT):
        paddle2YPos = WINDOW_HEIGHT - PADDLE_HEIGHT
    return paddle2YPos


# Główna klasa gry Pong :)
class PongGame:
    def __init__(self):

        # Inicjalizacja pygame
        pygame.init()
        pygame.display.set_caption('Pong DQN Experiment')

        num = random.randint(0, 9)

        # inicjalizacja położenia rakietek
        self.paddle1YPos = WINDOW_HEIGHT / 2 - PADDLE_HEIGHT / 2
        self.paddle2YPos = WINDOW_HEIGHT / 2 - PADDLE_HEIGHT / 2
        # inicjalizacja położenia piłki
        self.ballXDirection = 1
        self.ballYDirection = 1

        # punk startowy
        self.ballXPos = WINDOW_WIDTH / 2 - BALL_WIDTH / 2

        self.clock = pygame.time.Clock()
        self.BallColor = WHITE
        self.FrameCount = 0
        self.GScore = -10.0
        self.GEpsilonDisplay = 1.0

        self.font = pygame.font.SysFont("calibri", 20)
        # Randomowo decyduj, w którą stronę piłka ma lecieć
        if (0 < num < 3):
            self.ballXDirection = 1
            self.ballYDirection = 1
        if (3 <= num < 5):
            self.ballXDirection = -1
            self.ballYDirection = 1
        if (5 <= num < 8):
            self.ballXDirection = 1
            self.ballYDirection = -1
        if (8 <= num < 10):
            self.ballXDirection = -1
            self.ballYDirection = -1
        num = random.randint(0, 9)
        self.ballYPos = num * (WINDOW_HEIGHT - BALL_HEIGHT) / 9

    # Inicjalizuj gre
    def InitialDisplay(self):
        pygame.event.pump()
        screen.fill(BLACK)
        drawPaddle1(self.paddle1YPos)
        drawPaddle2(self.paddle2YPos)
        drawBall(self.ballXPos, self.ballYPos, WHITE)

        pygame.display.flip()

    def PlayNextMove(self, action):
        DeltaFrameTime = self.clock.tick(FPS)
        self.FrameCount = self.FrameCount + 1

        Quit = False
        KeyPressed = pygame.key.get_pressed()
        if (KeyPressed[pygame.K_ESCAPE]):
            print("Esc pressed")
            Quit = True
        if (KeyPressed[pygame.K_q]):
            print("Esc pressed")
            Quit = True
        pygame.event.pump()

        PlayerMissed = False
        screen.fill(BLACK)

        self.paddle1YPos = updatePaddle1(action, self.paddle1YPos, DeltaFrameTime)
        drawPaddle1(self.paddle1YPos)

        self.paddle2YPos = updatePaddle2(self.paddle2YPos, self.ballYPos, DeltaFrameTime)
        drawPaddle2(self.paddle2YPos)

        [PlayerMissed, self.ballXPos, self.ballYPos, self.ballXDirection, self.ballYDirection,
         self.BallColor] = updateBall(self.paddle1YPos, self.paddle2YPos, self.ballXPos, self.ballYPos,
                                      self.ballXDirection, self.ballYDirection, DeltaFrameTime, self.BallColor)
        drawBall(self.ballXPos, self.ballYPos, self.BallColor)

        TimeDisplay = self.font.render("Frame: " + str(self.FrameCount), True, (255, 255, 255))
        screen.blit(TimeDisplay, (50., 40.))

        pygame.display.flip()

        return self.FrameCount, PlayerMissed, Quit

    def ReturnCurrentState(self):

        return [self.paddle1YPos, self.ballXPos, self.ballYPos, self.ballXDirection, self.ballYDirection]


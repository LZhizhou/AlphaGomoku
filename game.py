import pygame

from board import Board, Color

"""
drawing the ui and handle the game process using pygame
"""
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
class Game:
    def __init__(self, width=800, height=800, edge_length=50, board_size = 7,wait_click = True):
        self.screen_width = width
        self.screen_height = height
        self.screen_edge_length = edge_length
        self.tile_length = (min(width, height) - 2 * edge_length) // (board_size-1)
        self.board = None
        self.wait_click = wait_click
        if self.wait_click:
            self.board = Board(board_size)
        self.screen = None

    def draw(self):
        pygame.init()
        screen = pygame.display.set_mode(
            (self.screen_width, self.screen_height))
        screen.fill(COLOR_WHITE)
        width = min(self.screen_height, self.screen_width)
        pygame.display.set_caption("GOMOKU")
        for x in range(self.screen_edge_length, width, self.tile_length):
            pygame.draw.line(screen, COLOR_BLACK, (x, self.screen_edge_length),
                             (x, width - self.screen_edge_length))
            pygame.draw.line(screen, COLOR_BLACK, (self.screen_edge_length,
                                                   x), (width - self.screen_edge_length, x))
        pygame.display.update()
        self.screen = screen

    def wait_event(self,toggle_wait=False):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if self.wait_click and event.type == pygame.MOUSEBUTTONDOWN:
                if not self.board.end:
                    if self.legal_pos(event.pos):
                        coord = self.pos_to_coord(event.pos)
                        player = self.board.play_stone(coord)
                        self.draw_stone(self.coord_to_pos(coord), player)
                        if self.board.end:
                            self.show_result(self.board.winner)
                        elif toggle_wait:
                            self.wait_click = False
                else:
                    self.board.reset()
                    self.draw()
            return True

    def legal_pos(self, pos):
        # x in bound
        constrains = [pos[0], self.screen_width -
                      pos[0], pos[1], self.screen_height - pos[1]]
        if min(constrains) > 0.5 * self.screen_edge_length:
            return True
        return False

    def pos_to_coord(self, pos):
        x = int((pos[0] - self.screen_edge_length) / self.tile_length + 0.5)
        y = int((pos[1] - self.screen_edge_length) / self.tile_length + 0.5)
        return x, y

    def coord_to_pos(self, coord):
        x = (coord[0]) * self.tile_length + self.screen_edge_length
        y = (coord[1]) * self.tile_length + self.screen_edge_length
        return x, y

    def draw_stone(self, pos, player):
        if player == Color.BLACK:
            pygame.draw.circle(self.screen, COLOR_BLACK,
                               pos, self.tile_length // 2 - 2)
        elif player == Color.WHITE:
            pygame.draw.circle(self.screen, COLOR_BLACK, pos,
                               self.tile_length // 2 - 2, 2)
        pygame.display.update()

    def show_result(self, winner):
        self.screen.fill(COLOR_WHITE)
        font = pygame.font.Font('freesansbold.ttf', 32)
        if winner == None:
            text = font.render("draw", True, COLOR_BLACK)
        else:
            text = font.render(winner.name + " wins", True, COLOR_BLACK)
        text_rect = text.get_rect()
        text_rect.center = (self.screen_width // 2, self.screen_height // 2)
        self.screen.blit(text, text_rect)
        pygame.display.update()


if __name__ == '__main__':
    game = Game(wait_click=True)
    game.draw()
    while True:
        game.wait_event()

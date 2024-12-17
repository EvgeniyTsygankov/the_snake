from random import choice, randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject():
    """Родительский класс объектов игры."""

    def __init__(self) -> None:
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT) // 2)
        self.body_color = None

    def draw(self):
        """
        Рисует объект на экране.

        Args: None
        Returns: None
        """
        pass


class Apple(GameObject):
    """Класс для создания яблок"""

    def __init__(self):
        super().__init__()
        self.body_color = APPLE_COLOR
        self.randomize_position()

    def randomize_position(self, snake_positions=None):
        """
        Генерирует случайное положение для объекта, избегая позиций змей.

        Args:
            snake_positions (list): Список позиций змей.

        Returns: None
        """
        for position in self.position:
            position_x = randint(0, GRID_WIDTH - 1)
            position_y = randint(0, GRID_HEIGHT - 1)
            position = (
                position_x * GRID_SIZE,
                position_y * GRID_SIZE
            )
            if snake_positions is None or position not in snake_positions:
                self.position = position

    def draw(self):
        """
        Рисует яблоко на игровой поверхности.

        Args: None
        Returns: None
        """
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс для создания змейки."""

    def __init__(self):
        super().__init__()
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT) // 2)]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None
        self.reset()

    def update_direction(self):
        """
        Обновляет направление движения змейки.

        Args: None
        Returns: None
        """
        if self.next_direction:
            self.direction = self.next_direction

    def move(self):
        """
        Обновляет положение змейки в игре.

        Args: None
        Returns: None
        """
        # Получение текущей позиции головы.
        current_head_position = self.get_head_position()
        x_1, y_1 = current_head_position

        # Вычисление новой позиции головы.
        direction_x, direction_y = self.direction
        new_head_position = (
            x_1 + GRID_SIZE * direction_x,
            y_1 + GRID_SIZE * direction_y,
        )
        # Проверка на выход за пределы экрана.
        x_2, y_2 = new_head_position
        new_head_position = (
            x_2 % SCREEN_WIDTH,
            y_2 % SCREEN_HEIGHT
        )
        # Добавление новой позиции головы в список.
        self.positions.insert(0, new_head_position)

        # Удаление последней позиции змейки, если длина не изменилась
        if len(self.positions) > self.length + 1:
            self.last = self.positions.pop()
        else:
            self.last = None

    def reset(self):
        """
        Сбрасывает игру в начальное состояние.

        Args: None
        Returns: None
        """
        self.length = 1
        self.positions = [self.position]
        self.direction = choice([RIGHT, LEFT, DOWN, UP])
        self.body_color = SNAKE_COLOR

    def get_head_position(self):
        """
        Возвращает позицию головы змейки.

        Args: None
        Returns: None
        """
        return self.positions[0]

    def draw(self):
        """
        Рисует змейку на игровой поверхности.

        Args: None
        Returns: None
        """
        # Отрисовка змейки на экране, кроме последнего сегмента.
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки.
        head_rect = pygame.Rect(
            self.get_head_position(),
            (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента.
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


def handle_keys(game_object):
    """
    Обрабатывает действия пользователя, связанные с направлениями движения.

    Args:
        game_object (тип данных): Игровой объект, для которого обрабатываются
        события.

    Returns: None
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Основной цикл игры."""
    # Инициализация PyGame.
    pygame.init()

    # Создание объектов игры.
    apple = Apple()
    snake = Snake()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        pygame.display.flip()

        # Проверка поедания яблока.
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)

        # Проверка столкновения змеи со своим телом.
        elif snake.get_head_position() in snake.positions[1:]:
            snake.reset()

        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        snake.draw()
        pygame.display.update()


if __name__ == "__main__":
    main()

import random
import curses


def create_food(snake, sh, sw):
    food = None
    while food is None:
        new_food = (random.randint(1, sh - 2), random.randint(1, sw - 2))
        food = new_food if new_food not in snake else None
    return food


def main(screen):
    curses.curs_set(0)

    form_food = curses.ACS_DIAMOND
    part_snake = curses.ACS_CKBOARD

    height, width = screen.getmaxyx()
    window = curses.newwin(height, width, 0, 0)
    window.keypad(1)
    window.timeout(100)

    snake_x = width // 4
    snake_y = height // 2
    snake = [
        (snake_y, snake_x),
        (snake_y, snake_x - 1),
        (snake_y, snake_x - 2)
    ]

    food = create_food(snake, height, width)
    window.addch(food[0], food[1], form_food)

    key = curses.KEY_RIGHT

    while True:
        next_key = window.getch()
        if next_key != -1 and (
                (next_key == 27) or
                (next_key == curses.KEY_DOWN and key != curses.KEY_UP) or
                (next_key == curses.KEY_UP and key != curses.KEY_DOWN) or
                (next_key == curses.KEY_LEFT and key != curses.KEY_RIGHT) or
                (next_key == curses.KEY_RIGHT and key != curses.KEY_LEFT)
        ):
            key = next_key

        if snake[0] in snake[1:]:
            curses.endwin()
            quit()

        new_head = [snake[0][0], snake[0][1]]

        if key == curses.KEY_DOWN:
            new_head = ((new_head[0] + 1) % height, new_head[1])
        if key == curses.KEY_UP:
            new_head = ((new_head[0] - 1) % height, new_head[1])
        if key == curses.KEY_LEFT:
            new_head = (new_head[0], (new_head[1] - 1) % width)
        if key == curses.KEY_RIGHT:
            new_head = (new_head[0], (new_head[1] + 1) % width)

        snake.insert(0, new_head)

        if snake[0] == food:
            food = create_food(snake, height, width)
            window.addch(food[0], food[1], form_food)
        else:
            tail = snake.pop()
            window.addch(tail[0], tail[1], ' ')

        window.addch(snake[0][0], snake[0][1], part_snake)


curses.wrapper(main)

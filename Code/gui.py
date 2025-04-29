import pygame
import settings


def draw_grid(screen, grid, start, end, offset_x=10):
    for row in grid:
        for node in row:
            color = settings.OBSTACLE_COLOR if node.obstacle else settings.EMPTY_COLOR
            if node == start:
                color = settings.START_COLOR
            elif node == end:
                color = settings.END_COLOR
            pygame.draw.rect(
                screen,
                color,
                (
                    node.x * settings.BLOCK_SIZE + offset_x,
                    node.y * settings.BLOCK_SIZE + 30,
                    settings.BLOCK_SIZE,
                    settings.BLOCK_SIZE,
                ),
                border_radius=2
            )


def draw_path(
    screen,
    path,
    path_color,
    start,
    end,
    offset_x=10,
    algo_name="",
    visited_grid_num=0,
    time_used=0,
    display_info=False,
):
    font = pygame.font.Font(None, 25)
    font_color = (255, 255, 255)
    position_y = settings.SCREEN_HEIGHT - 40

    algo_text = font.render(f"{algo_name}", True, font_color)
    screen.blit(algo_text, (10 + offset_x, 5))

    for node in path:
        if node != start and node != end:
            color = path_color
            pygame.draw.rect(
                screen,
                color,
                (
                    node.x * settings.BLOCK_SIZE + offset_x,
                    node.y * settings.BLOCK_SIZE + 30,
                    settings.BLOCK_SIZE,
                    settings.BLOCK_SIZE,
                ),
                border_radius=2
            )

    if display_info:
        path_length_text = font.render(
            f"Path Length: {len(path) - 2}", True, font_color
        )
        screen.blit(path_length_text, (10 + offset_x, position_y))
        visited_grid_text = font.render(
            f"Visited Grid: {visited_grid_num}", True, font_color
        )
        screen.blit(visited_grid_text, (170 + offset_x, position_y))
        time_used_text = font.render(
            f"Time Used: {round(time_used, 4)}s", True, font_color
        )
        screen.blit(time_used_text, (340 + offset_x, position_y))

    # pygame.display.update()


def clear_screen(screen, offset_x=0, width=settings.SCREEN_WIDTH):
    rect = pygame.Rect(offset_x, 0, width, settings.SCREEN_HEIGHT)
    screen.fill(settings.BACKGROUND_COLOR, rect)
    # pygame.display.update(rect)

def reset_button(screen, rect, label, font, bg_color, text_color):
    """
    Draws a button on the screen.

    Args:
        screen: The pygame screen object.
        rect: A pygame.Rect object defining the button's position and size.
        label: The text to display on the button.
        font: The pygame font object.
        bg_color: The background color of the button.
        text_color: The color of the text.
    """
    pygame.draw.rect(screen, bg_color, rect, border_radius=10)  # Add rounded corners
    text_surface = font.render(label, True, text_color)
    text_rect = text_surface.get_rect(center=rect.center)  # Center the text
    screen.blit(text_surface, text_rect)
    pygame.display.update(rect)




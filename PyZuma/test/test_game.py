import pygame


pygame.init()
pygame.display.set_mode([800, 600])

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()  # sys.exit() if sys is imported
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                print("Su")
            if event.key == pygame.K_DOWN:
                print("Giù")
            if event.key == pygame.K_LEFT:
                print("Sinistra")
            if event.key == pygame.K_RIGHT:
                print("Destra")
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                print("Fine Su")
            if event.key == pygame.K_DOWN:
                print("Fine Giù")
            if event.key == pygame.K_LEFT:
                print("Fine Sinistra")
            if event.key == pygame.K_RIGHT:
                print("Fine Destra")

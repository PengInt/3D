import GameEngine

running = True
while running:
	for e in GameEngine.Events.get():
		if e.type == GameEngine.pygame.QUIT:
			GameEngine.pygame.quit()

exit()
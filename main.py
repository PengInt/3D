import GameEngine

GameEngine.GameObject((
	GameEngine.Vector3(-1, -1, -1),
	GameEngine.Vector3(1, -1, -1),
	GameEngine.Vector3(-1, 1, -1),
	GameEngine.Vector3(-1, -1, 1),
	GameEngine.Vector3(1, 1, -1),
	GameEngine.Vector3(1, -1, 1),
	GameEngine.Vector3(-1, 1, 1),
	GameEngine.Vector3(1, 1, 1)),
	((0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 0)), GameEngine.Vector3(0, 0, 0)
)

running = True
while running:
	for e in GameEngine.system.event.get():
		if e.type == GameEngine.system.QUIT:
			GameEngine.system.quit()
			exit()

	GameEngine.Renderer.renderers['Renderer'].render()
	print('update')

exit()
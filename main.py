import pygame

import GameEngine, math, random, pathlib


'''arr = []
for i in range(7):
	for j in range(i+1, 8):
		arr.append([i, j])

GameEngine.GameObject((
	GameEngine.Vector3(-1, -1, -1),
	GameEngine.Vector3(1, -1, -1),
	GameEngine.Vector3(-1, 1, -1),
	GameEngine.Vector3(-1, -1, 1),
	GameEngine.Vector3(1, 1, -1),
	GameEngine.Vector3(1, -1, 1),
	GameEngine.Vector3(-1, 1, 1),
	GameEngine.Vector3(1, 1, 1)),
	arr, (), GameEngine.Vector3(0, 0, 0)
)'''

GameEngine.GameObject.fromJSON(pathlib.Path.cwd()/'model_data.json')


axis = GameEngine.Vector3(random.randint(-10, 10), random.randint(-10, 10), random.randint(-10, 10))

running = True

GameEngine.GameObject.heierarchy['Suzanne'] >>= GameEngine.Quaternion(0.5 * math.pi, GameEngine.Vector3(1, 0, 0))
GameEngine.GameObject.heierarchy['Suzanne'] >>= GameEngine.Quaternion(1 * math.pi, GameEngine.Vector3(0, 1, 0))

while running:
	for e in GameEngine.system.event.get():
		if e.type == GameEngine.system.QUIT:
			GameEngine.system.quit()
			exit()
		elif e.type == GameEngine.system.MOUSEBUTTONDOWN:
			axis = GameEngine.Vector3(random.randint(-10, 10), random.randint(-10, 10), random.randint(-10, 10))


	GameEngine.GameObject.heierarchy['Suzanne'] >>= GameEngine.Quaternion(0.0125*math.pi, axis)

	GameEngine.Renderer.renderers['Renderer'].render()

exit()
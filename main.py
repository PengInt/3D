import GameEngine, math, random


arr = []
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
)


axis = GameEngine.Vector3(random.randint(-10, 10), random.randint(-10, 10), random.randint(-10, 10))

running = True
while running:
	for e in GameEngine.system.event.get():
		if e.type == GameEngine.system.QUIT:
			GameEngine.system.quit()
			exit()


	GameEngine.GameObject.heierarchy['GameObject'] > GameEngine.Quaternion(0.00025*math.pi, axis)

	GameEngine.Renderer.renderers['Renderer'].render()

exit()
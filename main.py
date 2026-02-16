import pygame

import GameEngine, math, random, pathlib



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
		elif e.type == GameEngine.system.KEYDOWN:
			if e.key == GameEngine.system.K_w:
				GameEngine.Renderer.renderers['Renderer'].camera.pos.z += 1
			if e.key == GameEngine.system.K_a:
				GameEngine.Renderer.renderers['Renderer'].camera.pos.x += -1
			if e.key == GameEngine.system.K_s:
				GameEngine.Renderer.renderers['Renderer'].camera.pos.z += -1
			if e.key == GameEngine.system.K_d:
				GameEngine.Renderer.renderers['Renderer'].camera.pos.x += 1
			if e.key == GameEngine.system.K_e:
				GameEngine.Renderer.renderers['Renderer'].camera.pos.y += 1
			if e.key == GameEngine.system.K_q:
				GameEngine.Renderer.renderers['Renderer'].camera.pos.y += -1
		#elif e.type == GameEngine.system.MOUSEBUTTONDOWN:
		#	axis = GameEngine.Vector3(random.randint(-10, 10), random.randint(-10, 10), random.randint(-10, 10))


	GameEngine.GameObject.heierarchy['Suzanne'] >>= GameEngine.Quaternion(0.0125*math.pi, axis)

	GameEngine.Renderer.renderers['Renderer'].render()

exit()
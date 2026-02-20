import GameEngine, math, random, pathlib


renderer = GameEngine.Renderer.renderers['Renderer']

GameEngine.GameObject.fromJSON(pathlib.Path.cwd()/'Model JSONs'/'panavia_tornado_ids_model_data.json')

panavia_tornado_ids = GameEngine.GameObject.heierarchy['Panavia Tornado IDS']

axis = GameEngine.Vector3(random.randint(-10, 10), random.randint(-10, 10), random.randint(-10, 10))

running = True

#GameEngine.GameObject.heierarchy['Suzanne'] >>= GameEngine.Quaternion(0.5 * math.pi, GameEngine.Vector3(1, 0, 0))
panavia_tornado_ids >>= GameEngine.Quaternion(1 * math.pi, GameEngine.Vector3(0, 1, 0))

print()
while running:
	for e in GameEngine.system.event.get():
		if e.type == GameEngine.system.QUIT:
			GameEngine.system.quit()
			exit()
		elif e.type == GameEngine.system.KEYDOWN:
			if e.key == GameEngine.system.K_w:
				renderer.camera.pos.z += 1
			if e.key == GameEngine.system.K_a:
				renderer.camera.pos.x += -1
			if e.key == GameEngine.system.K_s:
				renderer.camera.pos.z += -1
			if e.key == GameEngine.system.K_d:
				renderer.camera.pos.x += 1
			if e.key == GameEngine.system.K_e:
				renderer.camera.pos.y += 1
			if e.key == GameEngine.system.K_q:
				renderer.camera.pos.y += -1
			if e.key == GameEngine.system.K_UP:
				renderer.camera.rot.x += 1
			if e.key == GameEngine.system.K_LEFT:
				renderer.camera.rot.y += -1
			if e.key == GameEngine.system.K_DOWN:
				renderer.camera.rot.x += -1
			if e.key == GameEngine.system.K_RIGHT:
				renderer.camera.rot.y += 1

		#elif e.type == GameEngine.system.MOUSEBUTTONDOWN:
		#	axis = GameEngine.Vector3(random.randint(-10, 10), random.randint(-10, 10), random.randint(-10, 10))


	panavia_tornado_ids >>= GameEngine.Quaternion(0.0125*math.pi, axis)

	renderer.render()
	print(f'\r{round(1/renderer.dt,2)} fps ', end='\r', flush=True)

exit()
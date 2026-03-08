import pygame

import GameEngine, math, random, pathlib



R = GameEngine.Renderer.renderers['Renderer']

#GameEngine.GameObject.fromJSON(pathlib.Path.cwd()/'panavia_tornado_ids_model_data.json', colour=(255, 102, 0), name='IDS')
#IDS = GameEngine.GameObject.heierarchy['IDS']
GameEngine.GameObject.fromJSON(pathlib.Path.cwd()/'benchy.json', colour=(255, 102, 0), name='Benchy')
Benchy = GameEngine.GameObject.heierarchy['Benchy']

axis = GameEngine.Vector3(random.randint(-10, 10), random.randint(-10, 10), random.randint(-10, 10))

running = True

#IDS >>= GameEngine.Quaternion(0.5 * math.pi, GameEngine.Vector3(1, 0, 0))
#IDS >>= GameEngine.Quaternion(1 * math.pi, GameEngine.Vector3(0, 1, 0))
Benchy >>= GameEngine.Quaternion(0.5 * math.pi, GameEngine.Vector3(1, 0, 0))

spd = 10
while running:
	dt = GameEngine.dt()
	for e in GameEngine.system.event.get():
		if e.type == GameEngine.system.QUIT:
			GameEngine.system.quit()
			exit()

		#elif e.type == GameEngine.system.MOUSEBUTTONDOWN:
		#	axis = GameEngine.Vector3(random.randint(-10, 10), random.randint(-10, 10), random.randint(-10, 10))

	keys = pygame.key.get_pressed()
	if keys[GameEngine.system.K_w]:
		R.camera.pos.z += spd * dt
	if keys[GameEngine.system.K_a]:
		R.camera.pos.x += -spd * dt
	if keys[GameEngine.system.K_s]:
		R.camera.pos.z += -spd * dt
	if keys[GameEngine.system.K_d]:
		R.camera.pos.x += spd * dt
	if keys[GameEngine.system.K_e]:
		R.camera.pos.y += spd * dt
	if keys[GameEngine.system.K_q]:
		R.camera.pos.y += -spd * dt
	if keys[GameEngine.system.K_UP]:
		R.camera.rot.x += 0.1
	if keys[GameEngine.system.K_LEFT]:
		R.camera.rot.y += -0.1
	if keys[GameEngine.system.K_DOWN]:
		R.camera.rot.x += -0.1
	if keys[GameEngine.system.K_RIGHT]:
		R.camera.rot.y += 0.1


	#IDS >>= GameEngine.Quaternion(0.0125*math.pi, axis)

	R.render()

exit()
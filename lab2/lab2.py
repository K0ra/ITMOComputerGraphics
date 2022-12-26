from Lumicept import OpenScene, LoadScene

dir = r"C:\Users\Public\Documents\Integra\Lumicept 11.31 x64\scenes\lab2"
scene_file = dir + "\initial.iof"
scene_output_file = dir + "\cornel_box0_sphere.iof"

def main():
	# Load scene
	scene = OpenScene(scene_file)
	notebook = scene.Notebook()

	camera = Camera(view_angle=55, targ_dist=3300)
	camera.targ_dist = 3300
	# set origin
	# set target
	camera.Translate(-910.77, -2915.73, 1248.6)
	
	camera.Apply()
	#notebook.AddCamera(camera)

	obs = PlaneObserver(name="plane_2D_luminance")
	obs.res = (640, 480)
	obs.thresh_ang = 1
	obs.phenom = LUM
	obs.ortho = False
	obs.focal_dist = 3300
	obs.org = (-0.5, 0.5, 0.0)
	obs.x_side = (1, 0, 0)
	obs.y_side = (0, -1, 0)
	obs.glob_attached = True
	obs.occlusion = True

	obsNode = ObserverNode(obs, name="plane_2D_luminance")
	
	scene.AddNode(obsNode)
	#scene_output_file = dir + '\Test.iof'
	#scene.Save(scene_output_file)
	LoadScene(scene)


if __name__ == "__main__":
	main()


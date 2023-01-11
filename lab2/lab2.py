from Lumicept import OpenScene, LoadScene

dir = r"C:\Users\Public\Documents\Integra\Lumicept 11.31 x64\scenes\lab2"
scene_file = dir + "\initial.iof"
scene_output_file = dir + "\cornel_box0_sphere.iof"

def set_imap_params(imap):
	imap.SetObserverAsAccSource(obsNode, calc_imap=False)
	imap.req_acc = 0.01
	imap.time_limit = 3600

def run_mcrt(kernel, scene):
	kernel.LoadScene(scene)
	print("run MCRT simulation...")
	kernel.CalculateIMaps()

def modify_luminance(scene, node_name: str, lum_value: float):
	node = scene.GetNode(node_name)
	node.shape.parts[0].surf_attrs.self_lum = lum_value

def get_plane_observer(name="plane_2D_luminance", angle=1.0):
	obs = PlaneObserver(name=name)
	obs.res = (640, 480)
	obs.thresh_ang = angle
	obs.phenom = LUM
	obs.ortho = False
	obs.focal_dist = 3300
	obs.org = (-0.5, 0.5, 0.0)
	obs.x_side = (1, 0, 0)
	obs.y_side = (0, -1, 0)
	obs.glob_attached = True
	obs.occlusion = True

	return obs

def get_lens_observer(name="lens_2D_luminance"):
	obs = LensObserver(name=name)
	obs.res = (640, 480)
	obs.view_angle = 42.65386
	obs.pupil_diam = 50
	obs.focal_length = 100
	obs.focusing_dist = 3300
	obs.image_dist = 103.125

	return obs

def main():
	scene = OpenScene(scene_file)
	notebook = scene.Notebook()

	""" Add and set camera """
	camera = Camera(view_angle=55, targ_dist=3300)
	camera.Translate(-910.77, -2915.73, 1248.6)
	camera.Rotate(67.768, 0, -17.347)
	### set the target coordinates ???
	### "keep target point" flag ???
	### set the twist angle ???
	camera.Apply()
	scene.camera = camera
	#notebook.AddCamera(camera)
	
	""" Add and set the Plane Observers for angles 
		(deg): 1, 10, 30, 60, 90 """

	for angle in [1, 10, 30, 60, 90]:
		name = "plane_2D_luminance_{}deg".format(angle)
		plane_obs = get_plane_observer(name=name, angle=angle)
		obsNode = ObserverNode(plane_obs, name=name)
		obsNode.tr.pos = (0, 0, 0)
		obsNode.Rotate(67.768, 0, -17.347)
		obsNode.tr.scale = (3435.743, 2576.807, 1)
		
		scene.AddNode(obsNode)

	""" Add and set the Lens Observer """
	lens_obs = get_lens_observer()
	obsNode = ObserverNode(lens_obs, name="lens_2D_luminance")
	obsNode.tr.pos = (-910.77, -2915.73, 1248.6)
	obsNode.Rotate(67.768, 0, -17.347)
	
	node_names = ["floor shape node", "100nit", "75nit", "50nit"]
	lum_values = [35, 55, 125, 350]
	
	for i in range(4):
		modify_luminance(scene, node_names[i], lum_values[i])

	scene.AddNode(obsNode)

	LoadScene(scene)

	#scene_output_file = dir + '\intial_set_observers.iof'
	#scene.Save(scene_output_file)

	imap = scene.IMapsParams()
	set_imap_params(imap)
	
	kernel = Kernel()
	run_mcrt(kernel, imap)
	

if __name__ == "__main__":
	main()


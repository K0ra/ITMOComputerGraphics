from Lumicept import OpenScene, LoadScene

dir = r"C:\Users\Public\Documents\Integra\Lumicept 11.31 x64\scenes\cornell_box"
scene_file = dir + "\cornel_box0.iof"
scene_output_file = dir + "\cornel_box0_sphere.iof"

# Load scene
scene = OpenScene(scene_file)
# Initialize kernel
kernel = Kernel()

# Set some rendering options
def set_render_params(suffix: str, do_imap: Bool =False):
	render = scene.RenderParams()
	render.indirect = do_imap			# use imaps during rendering
	render.path = dir + "\output\\"
	render.suffix = suffix

# Set some path-traced rendering options
def set_pt_render_params(suffix: str):
	pt_params = scene.PTRenderParams()
	pt_params.path = dir + "\output\\"
	pt_params.suffix = suffix
	pt_params.store_illum = False
	pt_params.res = Vect2i(500, 300) # image resolution
	pt_params.acc_limit = 0.1
	pt_params.store_lum = True # enable saving a .nit file

def modify_geom_attrs(node_name: str, ind: int):
	brs_node = scene.GetNode(node_name)
	#brs_part = brs_node.shape.GetPart("pbrs_{}_2".format(ind))

	gr_attrs = StdSurfAttrs()

	gr_attrs.front_side.gr_val = 1
	gr_attrs.front_side.gr_ang = 5

	gr_attrs.back_side.gr_val = 1
	gr_attrs.back_side.gr_ang = 5
				
	gr_attrs.SetKd(0)

	gr_attrs.kd_color = brs_node.shape.parts[0].surf_attrs.kd_color
	gr_attrs.col_link = 1

	brs_node.shape.ReplaceSurfAttrs(brs_node.shape.parts[0].surf_attrs, gr_attrs)


def calc_imap(time: int=60, accuracy: float=0.05):
	# reset imaps
	kernel.ResetIMaps()

	print("run MCRT simulation...")
	kernel.CalcIndirect(time=time, accuracy=accuracy)

def main():
	""" Modify light """
	lnode = scene.GetNode("F000001")
	lnode.Translate(278000,-279500,548700)
	lnode.name = "LNode0"
	#lnode.targ_dist = Vec3(548700,0,0).Length()
	lnode.light.name = "Point"
	lnode.light.kind = 0 # make a point light

	""" Adding a Sphere to the scene """
	lib = GetLibrary(Shape)
	sphere_shape = lib.GetItem("Sphere")
	sphere_node = MeshNode(sphere_shape, name="Sphere0")
	sphere_node.shape.radius = 700
	sphere_node.Translate(278000,-279500,548700)
	
	# Set material attributes of Sphere
	surf_attrs = StdSurfAttrs(name="Sphere")
	surf_attrs.SetKd(0, BWSurfColor(1.0))
	surf_attrs.SetKtd(1)
	sphere_node.shape.GetPart("Sphere").surf_attrs = surf_attrs
	
	""" Set Gauss Reflection to 1 and Kd to 0 """
	#geom_nodes = ["brs_{}".format(n) for n in range(5)]
	#for ind, node in enumerate(geom_nodes):
		#modify_geom_attrs(node, ind)

	""" Split the scene into more triangles """
	scene.SetSubdivision(use_subd = True, rel_step = 0.01)
	
	scene.AddNode(sphere_node)
	scene_output_file = dir + '\cornel_box0_sphere_subdiv.iof'
	scene.Save(scene_output_file)
	LoadScene(scene)

	#kernel.LoadScene(scene)

	""" Simple rendering """
	#set_render_params("cornell_box0_sphere_no_imap")
	#print("run rendering without IMap...")
	#kernel.Render()

	""" Rendering with imap """
	#set_render_params("cornell_box0_sphere_imap", True)
	#calc_imap(time=60, accuracy=0.05)
	#print("run rendering with IMap...")
	#kernel.Render()

	""" Path-trace render """
	#set_pt_render_params("cornell_box0_gauss_pt")
	#print("run Path-tracer rendering with subdivision...")
	#kernel.PTRender()


if __name__ == "__main__":
	main()


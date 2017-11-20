import xml.etree.ElementTree as ET
from lxml import etree








ROBOT_NAMESPACE = "http://www.ros.org/wiki/xacro"
ROBOT = "{%s}" % ROBOT_NAMESPACE

NSMAP = {"xacro" : ROBOT_NAMESPACE} # the default namespace prefix xacro

robot = etree.Element( "robot", nsmap=NSMAP, name="myrobot") # lxml only!


m =  None

while m is None:
	length = raw_input("Unesite zeljenu duljinu spage u metrima: ")
	try:

		m=float(length)
		length=float(length)

	except ValueError:
		print("Pogresan unos, unesite pozitivni decimalni ili cijeli broj")

m = None

while m is None:
	n = raw_input("Unesite zeljeni broj clanaka: ")
	
	try:

		m=int(n)
		n=int(n)

	except ValueError:
		print("Pogresan unos, unesite pozitivan cijeli broj")

m = None

while m is None:
	load_mass = raw_input("Unesite zeljeni masu tereta u kilogramima: ")
	try:

		m=float(load_mass)
		load_mass=float(load_mass)

	except ValueError:
		print("Pogresan unos, unesite pozitivan decimalni ili cijeli broj")

m = None

while m is None:
	spawn_point = raw_input("Unesite zeljeni visinu prihvatista spage: ")
	try:

		m=float(spawn_point)
		spawn_point=float(spawn_point)

	except ValueError:
		print("Pogresan unos, unesite pozitivan decimalni ili cijeli broj")



body_len = length/n
width_1 = length/300
mass_rope = 0.1 #ukloniti ovisnost o broju clanaka 
mass_link=0.01

#inertia_rope1=(1/12)*mass_rope*body_len**2+(1/4)*mass_rope*width_1**2"""
#inertia_rope2=(1/2)*mass_rope*width_1**2
inertia_rope1 = 0.01
inertia_rope2 = 0.02

load_inertia = (2/5)*load_mass*(load_mass/100)*(load_mass/100)

global property_list_names, property_list_values, base_list, rope_list

base_list = ["base_link","load"]


property_list_names = ["width_1", "body_len", "box_param", "box_param1", "spawn_point", 
						"radius", "small", "load_mass", "friction", "damping1",
						 "effort_joint", "large", "inertia_rope1", "inertia_rope2", "mass_rope", 
						 "mass_link", "inertia_link", "velocity_joint", "load_inertia"]
property_list_values = [length/250, length/n, 0.5, 0.25, spawn_point,
 						0.1+load_mass/2000, 0.005, load_mass, 0.02, 0.5,
 						 1000, 100, inertia_rope1, inertia_rope2, mass_rope, 
 						 load_mass/4000*(n/5), (load_mass/400)*(n/5), 300, load_inertia] #podesiti inertia_link i mass_link da nema nikakvih rupa


#print len(property_list_names)
#rint len(property_list_values)
def property_generator(property_list_names, property_list_values):

    for i in range(0, len(property_list_values)):
        print "{0}={1}".format(property_list_names[i],property_list_values[i])
        etree.SubElement(robot, "{http://www.ros.org/wiki/xacro}property", name="{0}".format(property_list_names[i]), value="{0}".format(property_list_values[i]))
        
    




def link_generator(n): #tocno odrediti koje argumente ce primati funkcija

    global rope_list
    rope_list = []
    link = []
    visual_link = []
    geometry_link = []
    cylinder = []
    origin = []
    collision_link = []
    geometry_col_link = []
    cylinder_col = []
    origin_col = []
    inertial_link = []
    mass_link = []
    inertia_link = []
    inertia_origin = []
    load_inertia="${(2/5)*load_mass*radius*radius}"


    for i in range(0,n+2):
        
        if i == 0:
            # world_link
            world_link = etree.SubElement(robot, "link", name="world")

            # base_link
            base_link = etree.SubElement(robot, "link", name="base_link")
            leg1_link = etree.SubElement(robot, "link", name="leg1")
            leg2_link = etree.SubElement(robot, "link", name="leg2")

            # visual_tag
            visual_base = etree.SubElement(base_link, "visual")
            visual_leg1 = etree.SubElement(leg1_link,"visual")
            visual_leg2 = etree.SubElement(leg2_link, "visual")
            geometry_base = etree.SubElement(visual_base, "geometry")
            geometry_leg1 = etree.SubElement(visual_leg1, "geometry")
            geometry_leg2 = etree.SubElement(visual_leg2, "geometry")
            etree.SubElement(geometry_base, "box", size="${box_param} ${3*box_param} ${box_param}")
            etree.SubElement(geometry_leg1, "box", size="${box_param} ${box_param1}  ${spawn_point+box_param/2}")
            etree.SubElement(geometry_leg2, "box", size="${box_param} ${-box_param1}  ${spawn_point+box_param/2}") 
            etree.SubElement(visual_leg1, "origin", xyz="0 0 ${-spawn_point/2}", rpy="0 0 0")
            etree.SubElement(visual_leg2, "origin",xyz="0 0 ${-spawn_point/2}", rpy="0 0 0")

            #collision_tag
            collision_base = etree.SubElement(base_link,"collision")
            geometry_base_c = etree.SubElement(collision_base, "geometry")
            etree.SubElement(geometry_base_c, "box", size="${box_param} ${3*box_param} ${box_param}")
            collision_leg1 = etree.SubElement(leg1_link, "collision")
            collision_leg2 = etree.SubElement(leg2_link, "collision")
            geometry_leg1_c = etree.SubElement(collision_leg1, "geometry")
            geometry_leg2_c = etree.SubElement(collision_leg2, "geometry")
            etree.SubElement(geometry_leg1_c, "box", size="${box_param} ${box_param1}  ${spawn_point+box_param/2}")
            etree.SubElement(geometry_leg2_c, "box", size="${box_param} ${-box_param1} ${spawn_point+box_param/2}")
            etree.SubElement(collision_leg1, "origin", xyz="0 0 ${-spawn_point/2}", rpy="0 0 0")
            etree.SubElement(collision_leg2, "origin", xyz="0 0 ${spawn_point/2}", rpy="0 0 0")
            etree.SubElement(collision_base, "origin", xyz="0 0 ${spawn_point}", rpy="0 0 0")


            #inertial_tag
            inertial_base = etree.SubElement(base_link,"inertial")
            inertial_leg1 = etree.SubElement(leg1_link, "inertial")
            inertial_leg2 = etree.SubElement(leg2_link, "inertial")
            etree.SubElement(inertial_base, "mass", value="${small}")
            etree.SubElement(inertial_leg1, "mass", value="${large}")
            etree.SubElement(inertial_leg2, "mass", value="${large}")
            etree.SubElement(inertial_base,"inertia", ixx="${small}", iyy="${small}", izz="${small}", ixy="0.0", ixz="0.0",   iyz="0.0")
            etree.SubElement(inertial_leg1, "inertia", ixx="${large}", iyy="${large}", izz="${large}", ixy = "0.0", ixz="0.0", iyz="0.0")
            etree.SubElement(inertial_leg2, "inertia", ixx="${large}", iyy="${large}", izz="${large}", ixy = "0.0", ixz="0.0", iyz="0.0")
            etree.SubElement(inertial_base,"origin", xyz="0 0 ${spawn_point}", rpy="0 0 0")
            etree.SubElement(inertial_leg1, "origin", xyz="0 ${3*box_param} ${-spawn_point/2}" ,rpy="0 0 0")
            etree.SubElement(inertial_leg2, "origin", xyz="0 ${-3*box_param} ${-spawn_point/2}", rpy="0 0 0")



        elif i<=n:

            rope_list.append("rope_{0}".format(i))       #generiranje liste imena

            link.append(etree.SubElement(robot,"link", name="{0}".format(rope_list[i-1])))
            visual_link.append(etree.SubElement(link[i-1], "visual"))
            geometry_link.append(etree.SubElement(visual_link[i-1],"geometry"))
            cylinder.append(etree.SubElement(geometry_link[i-1], "cylinder", length="${body_len}", radius="${width_1}"))
            origin.append(etree. SubElement(visual_link[i-1], "origin", xyz="0 0 ${-body_len/2}", rpy="0.0 0.0 0.0"))
            collision_link.append(etree.SubElement(link[i-1], "collision"))
            geometry_col_link.append(etree.SubElement(collision_link[i-1], "geometry"))
            cylinder_col.append(etree.SubElement(geometry_col_link[i-1], "cylinder", length="${body_len}", radius="${width_1}" ))
            origin_col.append(etree.SubElement(collision_link[i-1], "origin", xyz="0 0 ${-body_len/2}", rpy = "0.0 0.0 0.0"))
            inertial_link.append(etree.SubElement(link[i-1],"inertial"))
            mass_link.append(etree.SubElement(inertial_link[i-1], "mass",value="${mass_rope}"))
            inertia_link.append(etree.SubElement(inertial_link[i-1],"inertia", ixx="${inertia_rope1}", iyy="${inertia_rope1}", izz="${inertia_rope2}", ixy="0.0", ixz="0.0", iyz="0.0"))
            inertia_origin.append(etree.SubElement(inertial_link[i-1], "origin",  xyz="0 0 ${-body_len/2}", rpy="0.0 0.0 0.0"))
        
        else:

            link.append(etree.SubElement(robot,"link", name="load"))
            visual_link.append(etree.SubElement(link[-1],"visual"))
            geometry_link.append(etree.SubElement(visual_link[-1],"geometry"))
            cylinder.append(etree.SubElement(geometry_link[-1],"sphere", radius="${radius}"))
            origin.append(etree.SubElement(visual_link[-1],"origin", xyz="0 0 ${-radius}", rpy="0.0 0.0 0.0" ))
            collision_link.append(etree.SubElement(link[-1],"collision"))
            geometry_col_link.append(etree.SubElement(collision_link[-1],"geometry"))
            cylinder_col.append(etree.SubElement(geometry_col_link[-1],"sphere", radius="${radius}"))
            origin_col.append(etree.SubElement(collision_link[-1], "origin", xyz="0 0 ${-radius}", rpy="0.0 0.0 0.0"))
            inertial_link.append(etree.SubElement(link[-1],"inertial"))
            mass_link.append(etree.SubElement(inertial_link[-1],"mass", value="${load_mass}"))
            inertia_link.append(etree.SubElement(inertial_link[-1],"inertia", ixx="${load_inertia}", iyy="${load_inertia}", izz="${load_inertia}", ixy="0.0", ixz="0.0", iyz="0.0"))
            inertia_origin.append(etree.SubElement(inertial_link[-1],"origin", xyz="0 0 ${-radius}", rpy="0.0 0.0 0.0"))

    #print rope_list

    return link, visual_link, geometry_link, cylinder, origin, collision_link, geometry_col_link, cylinder_col, origin_col, inertial_link, mass_link, inertia_link, inertia_origin, rope_list


def joint_generator(n,rope_list,base_list):

    rope_Theta_links = []
    rope_Psi_links = []
    imaginary_inertiaTheta = []
    imaginary_inertiaPsi = []
    joints=[]
    joints1=[]
    joints2=[]
    joints3=[]

    joint = etree.SubElement(robot,"joint",name="world_base_link", type="fixed")
    etree.SubElement(joint, "parent", link="world")
    etree.SubElement(joint, "child", link="base_link")
    etree.SubElement(joint, "origin", xyz="0 0 ${spawn_point}", rpy="0.0 0.0 0.0")

    jointleg1 = etree.SubElement(robot,"joint",name="leg1_base_link", type="fixed")
    etree.SubElement(jointleg1, "parent", link="base_link")
    etree.SubElement(jointleg1, "child", link="leg1")
    etree.SubElement(jointleg1, "origin", xyz="0 ${3*box_param/2+box_param1/2} ${box_param/4}")

    jointleg2 = etree.SubElement(robot,"joint",name="leg2_base_link", type="fixed")
    etree.SubElement(jointleg2, "parent", link="base_link")
    etree.SubElement(jointleg2, "child", link="leg2")
    etree.SubElement(jointleg2, "origin", xyz="0 ${-(3*box_param/2+box_param1/2)} ${box_param/4}")

    for i in range(0, n+1):


        rope_Theta.append("rope{0}Theta".format(int(i+1)))
        rope_Psi.append("rope{0}Psi".format(int(i+1)))

        rope_Theta_links.append(etree.SubElement(robot, "link", name="{0}".format(rope_Theta[i])))
        imaginary_inertiaTheta.append(etree.SubElement(rope_Theta_links[i],"inertial"))
        etree.SubElement(imaginary_inertiaTheta[i],"mass", value="${mass_link}")
        etree.SubElement(imaginary_inertiaTheta[i],"inertia", ixx="${inertia_link}", iyy="${inertia_link}", izz="${inertia_link}", ixy="0.0", ixz="0.0", iyz="0.0")
        rope_Psi_links.append(etree.SubElement(robot,"link", name="{0}".format(rope_Psi[i])))
        imaginary_inertiaPsi.append(etree.SubElement(rope_Psi_links[i], "inertial"))
        etree.SubElement(imaginary_inertiaPsi[i], "mass", value="${mass_link}")
        etree.SubElement(imaginary_inertiaPsi[i], "inertia", ixx="${inertia_link}", iyy="${inertia_link}",
                      izz="${inertia_link}", ixy="0.0", ixz="0.0", iyz="0.0")
        #print rope_Theta
        #print rope_Psi
        #print rope_list

        if i == 0:

            joints.append(etree.SubElement(robot,"joint", name="{0}_to_{1}".format(base_list[i],rope_Psi[i]),type="revolute"))
            etree.SubElement(joints[i],"parent", link="base_link", )
            etree.SubElement(joints[i],"child", link="{0}".format(rope_Psi[i]))
            etree.SubElement(joints[i],"origin", xyz="0 0 ${-box_param/2}", rpy="0.0 0.0 0.0")
            etree.SubElement(joints[i],"axis", xyz="0 0 1" )
            etree.SubElement(joints[i],"dynamics", damping="${damping1}", friction="${friction}")
            etree.SubElement(joints[i],"limit", lower="${-pi/2}", upper="${pi/2}", effort="${effort_joint}", velocity="${velocity_joint}")

            joints.append(etree.SubElement(robot,"joint",name="{0}_to_{1}".format(rope_Psi[i],rope_Theta[i]),type="revolute"))
            etree.SubElement(joints[i+1], "parent", link="{0}".format(rope_Psi[i-1]) )
            etree.SubElement(joints[i+1], "child", link="{0}".format(rope_Theta[i-1]))
            etree.SubElement(joints[i+1], "axis", xyz="0 1 0")
            etree.SubElement(joints[i+1], "dynamics", damping="${damping1}", friction="${friction}")
            etree.SubElement(joints[i+1], "limit", lower="${-pi/2}", upper="${pi/2}", effort="${effort_joint}",velocity="${velocity_joint}")

            joints.append(etree.SubElement(robot, "joint", name = "{0}_to_{1}".format(rope_Theta[i],rope_list[i]), type = "revolute"))
            etree.SubElement(joints[i+2], "parent", link="{0}".format(rope_Theta[i]))
            etree.SubElement(joints[i+2], "child", link="{0}".format(rope_list[i]))
            etree.SubElement(joints[i+2], "axis", xyz="1 0 0")
            etree.SubElement(joints[i+2], "dynamics", damping="${damping1}", friction="${friction}")
            etree.SubElement(joints[i+2], "limit", lower="${-pi/16}", upper="${pi/16}", effort="${effort_joint}", velocity="${velocity_joint}")

        elif i<n:


            #print i - koristeno iskljucivo tokom debuggiranja

            joints1.append(etree.SubElement(robot, "joint", name="{0}_to_{1}".format(rope_list[i - 1], rope_Psi[i]),type="revolute"))
            etree.SubElement(joints1[i - 1], "parent", link="{0}".format(rope_list[i-1]), )
            etree.SubElement(joints1[i - 1], "child", link="{0}".format(rope_Psi[i]))
            etree.SubElement(joints1[i - 1], "origin", xyz="0 0 ${-body_len}", rpy="0.0 0.0 0.0")
            etree.SubElement(joints1[i - 1 ], "axis", xyz="0 0 1")
            etree.SubElement(joints1[i - 1], "dynamics", damping="${damping1}", friction="${friction}")
            etree.SubElement(joints1[i - 1], "limit", lower="${-pi/2}", upper="${pi/2}", effort="${effort_joint}",velocity="${velocity_joint}")

            joints2.append(etree.SubElement(robot, "joint", name="{0}_to_{1}".format(rope_Psi[i], rope_Theta[i]), type = "revolute"))
            etree.SubElement(joints2[i - 1], "parent", link="{0}".format(rope_Psi[i]))
            etree.SubElement(joints2[i - 1], "child", link="{0}".format(rope_Theta[i]))
            etree.SubElement(joints2[i - 1], "axis", xyz="0 1 0")
            etree.SubElement(joints2[i - 1], "dynamics", damping="${damping1}", friction="${friction}")
            etree.SubElement(joints2[i - 1], "limit", lower="${-pi/2}", upper="${pi/2}", effort="${effort_joint}", velocity="${velocity_joint}")

            joints3.append(etree.SubElement(robot, "joint", name="{0}_to_{1}".format(rope_Theta[i], rope_list[i]),type="revolute"))
            etree.SubElement(joints3[i - 1], "parent", link="{0}".format(rope_Theta[i]))
            etree.SubElement(joints3[i - 1], "child", link="{0}".format(rope_list[i]))
            etree.SubElement(joints3[i - 1], "axis", xyz="1 0 0")
            etree.SubElement(joints3[i - 1], "dynamics", damping="${damping1}", friction="${friction}")
            etree.SubElement(joints3[i - 1], "limit", lower="${-pi/16}", upper="${pi/16}", effort="${effort_joint}", velocity="${velocity_joint}")

        else:

            joints1.append(etree.SubElement(robot, "joint", name="{0}_to_{1}".format(rope_list[i - 1], rope_Psi[i]), type="revolute"))
            etree.SubElement(joints1[i - 1], "parent", link="{0}".format(rope_list[i - 1]), )
            etree.SubElement(joints1[i - 1], "child", link="{0}".format(rope_Psi[i]))
            etree.SubElement(joints1[i - 1], "origin", xyz="0 0 ${-body_len}", rpy="0.0 0.0 0.0")
            etree.SubElement(joints1[i - 1], "axis", xyz="0 0 1")
            etree.SubElement(joints1[i - 1], "dynamics", damping="${damping1}", friction="${friction}")
            etree.SubElement(joints1[i - 1], "limit", lower="${-pi/2}", upper="${pi/2}", effort="${effort_joint}", velocity="${velocity_joint}")

            joints2.append(etree.SubElement(robot, "joint", name="{0}_to_{1}".format(rope_Psi[i], rope_Theta[i]), type="revolute"))
            etree.SubElement(joints2[i - 1], "parent", link="{0}".format(rope_Psi[i]))
            etree.SubElement(joints2[i - 1], "child", link="{0}".format(rope_Theta[i]))
            etree.SubElement(joints2[i - 1], "axis", xyz="0 1 0")
            etree.SubElement(joints2[i - 1], "dynamics", damping="${damping1}", friction="${friction}")
            etree.SubElement(joints2[i - 1], "limit", lower="${-pi/2}", upper="${pi/2}", effort="${effort_joint}", velocity="${velocity_joint}")

            joints3.append(etree.SubElement(robot, "joint", name="{0}_to_{1}".format(rope_Theta[i], base_list[-1]), type="revolute"))
            etree.SubElement(joints3[i - 1], "parent", link="{0}".format(rope_Theta[i]))
            etree.SubElement(joints3[i - 1], "child", link="{0}".format(base_list[-1]))
            etree.SubElement(joints3[i - 1], "axis", xyz="1 0 0")
            etree.SubElement(joints3[i - 1], "dynamics", damping="${damping1}", friction="${friction}")
            etree.SubElement(joints3[i - 1], "limit", lower="${-pi/16}", upper="${pi/16}", effort="${effort_joint}",velocity="${velocity_joint}")



    return rope_Theta, rope_Psi,rope_Theta_links, rope_Psi_links, joints, joints1, joints2, joints3





def gazebo_reference(rope_list, base_link):
    for i in  range(0, len(rope_list)+1):

        if i<len(rope_list):
            gazebo = etree.SubElement(robot, "gazebo", reference="{0}".format(rope_list[i]))
            color = ["Blue", "Green", "Red"]
            material = etree.SubElement(gazebo, "material")
            material.text = "Gazebo/{0}".format(color[i%2])
        else:
            gazebo = etree.SubElement(robot, "gazebo", reference="{0}".format(base_link[-1]))
            material = etree.SubElement(gazebo, "material")
            material.text = "Gazebo/{0}".format(color[-1])






rope_Theta = []
rope_Psi = []

property_generator(property_list_names,property_list_values)
link_generator(n)
joint_generator(n,rope_list,base_list )
gazebo_reference(rope_list,base_list)
tree = etree.tostring(robot, pretty_print=True, encoding="utf-8", xml_declaration=True)
print property_list_values
"""
tree1=""
tree1.write("filename.xml", xml_declaration=True, encoding='utf-8',method="xml")"""
f = open("myrobot1.xacro",'w')
f.write(tree)










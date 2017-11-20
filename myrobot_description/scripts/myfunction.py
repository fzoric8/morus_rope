def link_generator(n,body_len,width_1):
	for i in range(n):
		print (<link name="rope_1">
			<visual>
				<geometry>	
					<cylinder radius="${width_1}" length="${body_len}"/>						
				</geometry>
				<origin xyz="0 0 ${-body_len/2}" rpy="0 0 0"/>
			</visual>
			<collision>
				<geometry>
					<cylinder radius="${width_1}" length="${body_len}"/>
				</geometry>
				<origin xyz="0  0 ${-body_len/2}" rpy="0 0 0"/>
			</collision>
				
			<inertial>
				<mass value="${mass_rope}"/>
				<inertia 
					ixx="${inertia_rope}" ixy="0.0" ixz="0.0"
        			iyy="${inertia_rope}" iyz="0.0"
        			izz="${inertia_rope}"/>
        		<origin xyz="0 0 ${-body_len/2}" rpy="0 0 0"/>
			</inertial>

		</link>) 
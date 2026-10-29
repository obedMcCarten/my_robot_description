import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch.substitutions import Command
from launch_ros.parameter_descriptions import ParameterValue

def generate_launch_description():
    pkg_name = 'my_robot_description'
    pkg_share = get_package_share_directory(pkg_name)
    urdf_file = os.path.join(pkg_share, 'urdf', 'my_robot.urdf.xacro')

    # Procesar el archivo Xacro a formato XML
    robot_desc_content = ParameterValue(Command(['xacro ', urdf_file]), value_type=str)

    # Nodo 1: Publica el estado del robot
    rsp_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_desc_content}]
    )

    # Nodo 2: Inicia Gazebo Sim (ros_gz_sim) con un mundo vacío
    pkg_ros_gz_sim = get_package_share_directory('ros_gz_sim')
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_ros_gz_sim, 'launch', 'gz_sim.launch.py')
        ),
        launch_arguments={'gz_args': 'empty.sdf -r'}.items()
    )

    # Nodo 3: Spawner para insertar el robot en Gazebo desde el topic
    spawn_node = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-name', 'mi_brazo_5gdl',
            '-topic', 'robot_description',
            '-z', '0.0'  # Altura inicial
        ],
        output='screen'
    )

    return LaunchDescription([
        rsp_node,
        gazebo,
        spawn_node
    ])

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():
    rplidar_ros_pkg = get_package_share_directory('rplidar_ros')
    slam_toolbox_pkg = get_package_share_directory('slam_toolbox')

    return LaunchDescription([
        # Include the RPLIDAR A1 launch file
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(rplidar_ros_pkg, 'launch', 'rplidar_a1_launch.py')
            ),
            launch_arguments={'frame_id': 'laser_frame'}.items()
        ),

        # Node for the slam_toolbox
        Node(
            package='slam_toolbox',
            executable='sync_slam_toolbox_node',
            name='slam_toolbox',
            output='screen',
            parameters=[
                os.path.join(slam_toolbox_pkg, 'config', 'mapper_params_online_sync.yaml')
            ],
            remappings=[
                ('scan', 'scan')  # Ensure the topic names match
            ]
        )
    ])

if __name__ == '__main__':
    generate_launch_description()

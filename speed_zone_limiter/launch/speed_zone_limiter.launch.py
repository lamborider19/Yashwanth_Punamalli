from launch import LaunchDescription
from launch_ros.actions import Node
import os


def generate_launch_description():

    config = os.path.join(
        os.path.dirname(__file__),
        '../config/slow_zone.yaml'
    )

    return LaunchDescription([

        Node(
            package='speed_zone_limiter',
            executable='speed_zone_limiter',
            name='speed_zone_limiter',
            output='screen',
            parameters=[config]
        )

    ])
    

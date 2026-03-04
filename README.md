# Zone-Based Speed Limiter

## Overview

This package implements a ROS node called `speed_zone_limiter` which reduces the robot’s forward speed when it enters a predefined slow zone on the map. The node listens to velocity commands from the navigation stack (`/cmd_vel`) and the robot pose from `/amcl_pose`. When the robot is detected inside the configured polygon zone, the node limits the forward velocity (`linear.x`) to a specified maximum value and republishes the modified command on `/cmd_vel_safe`. This approach is commonly used in mobile robots operating in warehouses or shared environments where robots should slow down near loading areas or high-traffic regions.

---

## Where the Node Fits in the Navigation Pipeline

The node acts as a small safety layer between the navigation stack and the robot controller. The navigation system generates velocity commands on `/cmd_vel`. The `speed_zone_limiter` node subscribes to this topic and also listens to `/amcl_pose` to determine the robot’s current position. If the robot is inside the configured polygon zone, the node caps the forward velocity before sending the command out again. The modified command is then published on `/cmd_vel_safe`, which can be forwarded to the robot base controller. This way the navigation system can operate normally while the limiter enforces safe speeds in specific areas.

---

## Environment

This implementation was developed and tested on:

* Ubuntu 22.04
* ROS2 Humble
* TurtleBot3 Gazebo simulation

The original instructions referenced **ROS Noetic**, but since ROS Noetic is designed for Ubuntu 20.04 and my system runs Ubuntu 22.04, the implementation was adapted to **ROS2 Humble** while keeping the same functionality and topic interfaces.

---

## Zone Configuration

The slow zone is defined in a YAML file that is loaded when the node starts.

Example:

```
max_speed: 0.10
polygon: [1.2, 0.5, 3.4, 0.5, 3.4, 2.1, 1.2, 2.1]
```

* **max_speed** – maximum forward speed allowed inside the zone
* **polygon** – coordinates defining the slow zone in the map frame

---

## Dependencies

The package uses:

* ROS2 Humble
* `rclpy`
* `geometry_msgs`
* `shapely` (used for point-in-polygon checking)

Install shapely if needed:

```
pip3 install shapely
```

---

## Build Instructions (Fresh Setup)

Create a ROS2 workspace and clone the repository:

```
mkdir -p ~/speed_ws/src
cd ~/speed_ws/src
git clone <repository_url>
```

Build the workspace:

```
cd ~/speed_ws
colcon build
```

Source the workspace:

```
source install/setup.bash
```

---

## Running the Node

Start the speed limiter node:

```
ros2 launch speed_zone_limiter speed_zone_limiter.launch.py
```

This launch file loads the zone configuration and runs the limiter node.

---

## Verifying in Simulation

The node was tested using the TurtleBot3 Gazebo simulation together with the Nav2 navigation stack.

To check that the limiter is working:

Check the original velocity from the navigation stack:

```
ros2 topic echo /cmd_vel
```

Check the velocity after the limiter:

```
ros2 topic echo /cmd_vel_safe
```

When the robot enters the configured slow zone, the forward velocity in `/cmd_vel_safe` should be capped to the configured `max_speed`.

During testing, navigation goals were sent through the slow zone in simulation and the difference between `/cmd_vel` and `/cmd_vel_safe` confirmed that the limiter was applied correctly.

---

## Tools / Resources

During development I referred to ROS2 documentation for node creation and parameter handling, and used the `shapely` Python library to perform the point-in-polygon check for determining whether the robot is inside the defined zone.

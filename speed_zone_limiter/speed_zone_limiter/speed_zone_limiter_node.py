import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist
from geometry_msgs.msg import PoseWithCovarianceStamped

from shapely.geometry import Point, Polygon


class SpeedZoneLimiter(Node):

    def __init__(self):
        super().__init__('speed_zone_limiter')

        # Declare parameters
        self.declare_parameter('max_speed', 0.1)
        self.declare_parameter('polygon', [1.2, 0.5, 3.4, 0.5, 3.4, 2.1, 1.2, 2.1])

        self.max_speed = self.get_parameter('max_speed').value
        poly_list = self.get_parameter('polygon').value

        # Convert flat list -> polygon points
        polygon_points = []
        for i in range(0, len(poly_list), 2):
            polygon_points.append((poly_list[i], poly_list[i + 1]))

        self.zone_polygon = Polygon(polygon_points)

        # Robot position
        self.current_x = None
        self.current_y = None

        # Subscribers
        self.cmd_sub = self.create_subscription(
            Twist,
            '/cmd_vel',
            self.cmd_callback,
            10
        )

        self.pose_sub = self.create_subscription(
            PoseWithCovarianceStamped,
            '/amcl_pose',
            self.pose_callback,
            10
        )

        # Publisher
        self.cmd_pub = self.create_publisher(
            Twist,
            '/cmd_vel_safe',
            10
        )

        self.get_logger().info("Speed Zone Limiter Node Started")

    def pose_callback(self, msg):
        self.current_x = msg.pose.pose.position.x
        self.current_y = msg.pose.pose.position.y

    def cmd_callback(self, msg):

        # If pose not yet received
        if self.current_x is None or self.current_y is None:
            self.cmd_pub.publish(msg)
            return

        point = Point(self.current_x, self.current_y)

        inside_zone = self.zone_polygon.contains(point)

        new_msg = Twist()
        new_msg.linear = msg.linear
        new_msg.angular = msg.angular

        if inside_zone:
            if new_msg.linear.x > self.max_speed:
                new_msg.linear.x = self.max_speed
                self.get_logger().info("Inside slow zone. Speed limited.")

        self.cmd_pub.publish(new_msg)


def main(args=None):

    rclpy.init(args=args)

    node = SpeedZoneLimiter()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

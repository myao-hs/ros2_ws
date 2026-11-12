
import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist


class SwarmNode(Node):

    def __init__(self):
        super().__init__('swarm_node')

        self.poses = {}
        self.cmd_publishers = []
        self.subscribers = []

        for i in range(1, 4):
            topic_name = f'/turtle{i}/pose'
            cmd_topic = f'/turtle{i}/cmd_vel'

            # Position information subscriber
            subscriber = self.create_subscription(
                Pose,
                topic_name,
                lambda msg, n=i: self.pose_callback(msg, n),
                10
            )
            self.subscribers.append(subscriber)

            # Velocity command publisher
            publisher = self.create_publisher(
                Twist,
                cmd_topic,
                10
            )
            self.cmd_publishers.append(publisher)

        # Publish velocity commands every 0.1 seconds
        self.timer = self.create_timer(0.1, self.control_loop)

        self.get_logger().info('Mini Swarm Node started!')

    def pose_callback(self, msg, turtle_number):
        self.poses[turtle_number] = msg

    def control_loop(self):

        for i, publisher in enumerate(self.cmd_publishers, start=1):

            msg = Twist()

            # Constant forward and turning velocity
            msg.linear.x = 0.5
            msg.angular.z = 0.5

            publisher.publish(msg)

        if len(self.poses) == 3:
            for i in range(1, 4):
                pose = self.poses[i]
                self.get_logger().info(
                    f'Turtle{i}: x={pose.x:.2f}, y={pose.y:.2f}'
                )


def main(args=None):
    rclpy.init(args=args)

    node = SwarmNode()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

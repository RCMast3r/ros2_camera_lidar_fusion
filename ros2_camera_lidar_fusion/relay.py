import rclpy
from rclpy.node import Node
from sensor_msgs.msg import PointCloud2, Image
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy

class ImageRelay(Node):
    def __init__(self):
        super().__init__('relay_depth10')

        points_qos_input = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            history=HistoryPolicy.KEEP_LAST,
            depth=5  # Match the original QoS of /image_raw
        )

        img_qos_input = QoSProfile(
            reliability=ReliabilityPolicy.RELIABLE,
            history=HistoryPolicy.KEEP_LAST,
            depth=10  # Match the original QoS of /image_raw
        )

        qos_output = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            history=HistoryPolicy.KEEP_ALL,
            depth=10  # This is the desired reduced depth
        )

        self.sub_points = self.create_subscription(
            PointCloud2,
            '/points',
            self.callback_points,
            points_qos_input
        )

        self.pub_points = self.create_publisher(
            PointCloud2,
            '/points_relay',
            qos_output
        )


        self.sub_img = self.create_subscription(
            Image,
            '/image_raw',
            self.callback_img,
            img_qos_input
        )

        self.pub_img = self.create_publisher(
            Image,
            '/image_relay',
            qos_output
        )

    def callback_points(self, msg):
        self.pub_points.publish(msg)
    def callback_img(self, msg):
        self.pub_img.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = ImageRelay()
    rclpy.spin(node)
    rclpy.shutdown()

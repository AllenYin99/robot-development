# 导入ROS2 Python库
import rclpy

# 导入Node基类，我们的机器人控制类需要继承它
from rclpy.node import Node

# Twist消息类型，用来发布速度（线速度、角速度）
from geometry_msgs.msg import Twist

# Pose消息类型，包含小乌龟的位置和方向
from turtlesim.msg import Pose

# 数学库，用于计算距离、角度
import math


# 创建一个控制小乌龟移动的节点
class MoveTurtle(Node):

    def __init__(self):
        # 初始化Node，名字叫 move_turtle
        super().__init__('move_turtle')


        # 创建速度发布器
        # 发布到 /turtle1/cmd_vel
        # 小乌龟通过这个topic接收运动指令
        self.publisher_ = self.create_publisher(
            Twist,
            '/turtle1/cmd_vel',
            10
        )


        # 创建定时器
        # 每0.5秒执行一次move函数
        # move函数负责计算速度并发送
        self.timer = self.create_timer(
            0.5,
            self.move
        )


        # 创建订阅器
        # 订阅小乌龟当前的位置和方向
        # 收到数据后调用pose_callback函数
        self.subscription = self.create_subscription(
            Pose,
            '/turtle1/pose',
            self.pose_callback,
            10
        )


        # 当前小乌龟的位置
        self.current_x = 0.0
        self.current_y = 0.0

        # 当前小乌龟朝向角度
        self.current_theta = 0.0


        # 设置目标位置
        # 小乌龟最终要移动到这里
        self.target_x = 1.0
        self.target_y = 1.0


        # 比例控制参数
        # 影响转向速度
        self.Kp = 2.0


        # 判断是否已经到达目标
        # 防止重复打印Goal reached
        self.goal_reached = False



    # 接收到/turtle1/pose数据时执行
    def pose_callback(self, pose):

        # 更新当前位置
        self.current_x = pose.x
        self.current_y = pose.y

        # 更新当前朝向
        self.current_theta = pose.theta



    # 处理角度范围
    # 将角度限制在 -pi 到 pi之间
    def normalize_angle(self, angle):

        # 如果角度超过180度，减去360度
        while angle > math.pi:
            angle -= 2 * math.pi


        # 如果角度小于-180度，加360度
        while angle < -math.pi:
            angle += 2 * math.pi


        return angle



    # 控制移动的主要函数
    def move(self):

        # 创建一个速度消息
        msg = Twist()


        # 计算当前位置到目标点的距离
        distance = math.sqrt(
            (self.target_x - self.current_x) ** 2 +
            (self.target_y - self.current_y) ** 2
        )


        # 计算目标方向角度
        # atan2可以根据目标坐标计算方向
        target_angle = math.atan2(
            self.target_y - self.current_y,
            self.target_x - self.current_x
        )


        # 计算需要转动的角度
        # 目标方向 - 当前方向
        angle_error = self.normalize_angle(
            target_angle - self.current_theta
        )


        # 如果距离目标还比较远
        if distance > 0.5:

            # 设置向前速度
            msg.linear.x = 2.0


            # 设置旋转速度
            # Kp越大，转向越快
            # 限制最大角速度为1.5
            msg.angular.z = max(
                min(self.Kp * angle_error, 1.5),
                -1.5
            )


        # 已经接近目标
        else:

            # 停止移动
            msg.linear.x = 0.0
            msg.angular.z = 0.0


            # 只打印一次到达信息
            if not self.goal_reached:

                self.get_logger().info(
                    "Goal reached!"
                )

                self.goal_reached = True



        # 打印当前距离
        self.get_logger().info(
            f'distance={distance}'
        )


        # 发布速度消息
        self.publisher_.publish(msg)




# 主函数
def main(args=None):

    # 初始化ROS2
    rclpy.init(args=args)


    # 创建节点对象
    node = MoveTurtle()


    # 保持节点运行
    rclpy.spin(node)


    # 关闭节点
    node.destroy_node()


    # 关闭ROS2
    rclpy.shutdown()



# Python直接运行这个文件时执行main
if __name__ == '__main__':
    main()
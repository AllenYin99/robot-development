# ROS2 Turtle Autonomous Navigation Controller

## 项目简介

基于 ROS2 和 Python 实现的移动机器人自主导航控制节点。

机器人通过订阅自身位姿信息，根据目标点位置计算距离和方向误差，
使用比例控制算法生成速度指令，实现自动移动到指定位置。

---

## 技术栈

- ROS2 Humble
- Python
- rclpy
- turtlesim
- geometry_msgs
- Publisher / Subscriber

---

## 实现功能

### 1. 位姿反馈

订阅：


/turtle1/pose


获取：

- x坐标
- y坐标
- 朝向theta


### 2. 目标点导航

设置目标位置：


(target_x, target_y)


计算：

- 当前距离
- 目标方向


### 3. 运动控制

采用比例控制：


angular.z = Kp * angle_error


实现方向调整。


### 4. 控制优化

加入：

- Kp比例控制
- 最大角速度限制
- 角度归一化
- 到达目标状态判断


---

## 运行效果

机器人能够自动移动到指定目标点：


start position
|
|
↓
target position


到达后输出：


Goal reached!


---

## 后续计划

- 使用URDF创建机器人模型
- Gazebo物理仿真
- 差速轮机器人控制
- SLAM地图构建

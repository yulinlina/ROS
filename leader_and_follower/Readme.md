# Basic requirement
1. 运行`$ rosmsg show HitBoundary` ，显示已定义的 HitBoundary.msg 中的内容, 我们新增了 x 和 y,用于实现 additional features 中的功能。
![image](https://user-images.githubusercontent.com/77262518/178401851-9f0721cc-69f6-4341-9995-456c712fa7d0.png)  


2. 运行以下命令，查看 ServicePID.srv 中已定义的服务类型。 运行`$ rosservice list`   
![image](https://user-images.githubusercontent.com/77262518/178401920-e212a66f-f0b6-4653-936c-9ff06983597c.png)        
3. 运行`$ rosservice info /service_pid`   
![image](https://user-images.githubusercontent.com/77262518/178401969-88792787-19a6-4e3f-8119-3a9c4be0552a.png)  
4. 生成四只小乌龟的初始位置  
![image](https://user-images.githubusercontent.com/77262518/178402020-98a162b4-a03c-4fb3-ab3f-8479bd7f3a20.png)  
5. leader 随机方向移动，三个 follower 以所需的相对距离跟随 leader
![image](https://user-images.githubusercontent.com/77262518/178402085-4d1a8467-88f8-4dae-9f82-064e9c5e72b1.png)    
6. 当 leader 接近边界并发送指示时，3 个 follower 回到初始位置，leader 返回中心位置。  
# 文件说明
• launch folder: contains launch files  
• scripts folder: contains your python code  
• srv folder: contains your custom ROS services  
• msg folder: contains your custom ROS messages  
• CMakeLists.txt: list of cmake rules for compilation  
Package.xml: Package information and dependencies
# 演示效果
[如何使用Turtlesim 实现 leader and follower](https://www.bilibili.com/video/BV1TW4y167iw)







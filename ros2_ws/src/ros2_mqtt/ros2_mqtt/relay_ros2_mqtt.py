#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_system_default
from sensor_msgs.msg import Joy

import paho.mqtt.client as mqtt
import json

class RelayRos2Mqtt(Node):
    def __init__(self):
        super().__init__('relay_ros2_mqtt')
        
        self.sleep_rate = 0.025
        self.latest_joy_msg = None
        self.rate = 10
        self.r = self.create_rate(self.rate)
        self.broker_address= self.declare_parameter("~broker_ip_address", '192.168.1.123').value
        self.MQTT_PUB_TOPIC = self.declare_parameter("~mqtt_pub_topic", 'esp32/cmd_vel').value
        self.MQTT_SUB_TOPIC = self.declare_parameter("~mqtt_sub_topic", 'esp32/feedback').value
        self.ROS_TWIST_SUB_TOPIC = self.declare_parameter("~twist_sub_topic", '/joy').value


        self.mqttclient = mqtt.Client()
        self.mqttclient.connect(self.broker_address) 
        self.mqttclient.subscribe(self.MQTT_SUB_TOPIC)
        self.mqttclient.on_message = self.on_message
        self.mqttclient.loop_start()


        self.get_logger().info('relay_ros2_mqtt:: started...')
        self.get_logger().info(f'relay_ros2_mqtt:: broker_address = {self.broker_address}')
        self.get_logger().info(f'relay_ros2_mqtt:: MQTT_PUB_TOPIC = {self.MQTT_PUB_TOPIC}')
        self.get_logger().info(f'relay_ros2_mqtt:: ROS_TWIST_SUB_TOPIC = {self.ROS_TWIST_SUB_TOPIC}')


        self.create_subscription(
            Joy,
            self.ROS_TWIST_SUB_TOPIC,
            self.joy_callback,
            qos_profile=qos_profile_system_default)
        
        # Timer que envia a cada 0.1s (2 Hz)
        self.timer = self.create_timer(0.1, self.publish_to_mqtt)

    def state_to_string(self,state):
        estados = {
            0: "robotOFF",
            1: "turnON",
            2: "robotON",
            3: "turnLeft",
            4: "turnRight",
            5: "goFoward",
            6: "turnOff"
        }
        return estados.get(state, "Estado desconhecido")
        

    def joy_callback(self, tmsg):
        self.latest_joy_msg = tmsg  # só salva a última


    def remap(self,value, in_min, in_max, out_min, out_max):
        return int((value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)
        
        

    def publish_to_mqtt(self):
        if self.latest_joy_msg is None:
            return

        tmsg = self.latest_joy_msg
        tmsg.axes[0] = self.remap(tmsg.axes[0], 1, -1, -1023, 1023)
        tmsg.axes[5] = self.remap(tmsg.axes[5], 1, -1, 0, 1023)
        Dictionary ={'start': tmsg.buttons[9],'stop' : tmsg.buttons[8] , 'robot_vel': int(tmsg.axes[5]), 'robot_yaw': int(tmsg.axes[0])}
        # self.get_logger().info('dict:: {0}'.format(json.dumps(Dictionary).encode()))
        
        self.mqttclient.publish(self.MQTT_PUB_TOPIC,json.dumps(Dictionary).encode(),qos=0, retain=False)


    # Callback when a message is received
    def on_message(self,client, userdata, msg):
        state_str = self.state_to_string(int(msg.payload.decode()))
        self.get_logger().info(f"FSM State: {state_str} ({msg.payload.decode()})")
        # self.get_logger().info(f"Message received on topic {msg.topic}: {msg.payload.decode()}")


def main(args=None):
    

    rclpy.init(args=args)
    try:
        relay_ros2_mqtt = RelayRos2Mqtt()
        rclpy.spin(relay_ros2_mqtt)
    except rclpy.exceptions.ROSInterruptException:
        pass

    relay_ros2_mqtt.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
---
sidebar_label: 'ROS 2 Fundamentals'
sidebar_position: 3
---

# ROS 2 Fundamentals

## ROS 2 Architecture

ROS 2 (Robot Operating System 2) is a flexible framework for writing robot software. It's a collection of tools, libraries, and conventions that aim to simplify the task of creating complex and robust robot behavior across a wide variety of robotic platforms.

## Nodes, Topics, and Services

### Nodes
A node is an executable that uses ROS 2 to communicate with other nodes. Nodes are organized in a graph architecture and can publish or subscribe to messages.

### Topics
Topics are named buses over which nodes exchange messages. Publishers send messages to topics, and subscribers receive messages from topics.

### Services
Services provide a request/response communication pattern. A service client sends a request to a service server and waits for a response.

## Package Management

ROS 2 uses packages to organize code. A package contains:
- Source code
- Build instructions
- Dependencies
- Documentation

## Basic Programming Concepts

ROS 2 applications are typically written in C++ or Python. The framework provides client libraries (rclcpp for C++, rclpy for Python) that handle the underlying communication infrastructure.
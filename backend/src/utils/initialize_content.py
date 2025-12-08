import asyncio
from sqlalchemy import select
from src.models.chapter import Chapter
from src.core.database import AsyncSessionLocal
from src.services.chapter_service import ChapterService


async def initialize_textbook_content():
    """
    Initialize the textbook with 6 chapters of content
    """
    print("Initializing textbook content...")

    # Define the 6 textbook chapters
    chapters_data = [
        {
            "title": "Introduction to Physical AI",
            "order": 1,
            "content": """# Introduction to Physical AI

## What is Physical AI?

Physical AI is an emerging field that combines artificial intelligence with physical systems and robotics. It represents the intersection of machine learning, robotics, and embodied intelligence, where AI agents learn and interact with the physical world.

## Historical Context

The concept of Physical AI has evolved from early work in robotics and machine learning. Unlike traditional AI that operates primarily in digital spaces, Physical AI must deal with the complexities of the real world including uncertainty, dynamics, and physical constraints.

## Key Principles

1. Embodied Cognition: Intelligence emerges from the interaction between an agent and its environment
2. Real-world Learning: Agents learn through physical interaction rather than just data
3. Multi-modal Perception: Combining visual, auditory, tactile and other sensory inputs
4. Adaptive Behavior: Systems that can adapt to changing physical conditions

## Applications and Impact

Physical AI has applications in robotics, autonomous vehicles, smart manufacturing, and human-computer interaction. It promises to revolutionize how we interact with technology in physical spaces.
"""
        },
        {
            "title": "Basics of Humanoid Robotics",
            "order": 2,
            "content": """# Basics of Humanoid Robotics

## Anatomy and Design Principles

Humanoid robots are designed to resemble and mimic human behavior. They typically feature a head, torso, two arms, and two legs, though some variations exist. The design aims to enable human-like interaction and navigation in human environments.

## Actuators and Sensors

Humanoid robots use various types of actuators to move their joints:
- Servo motors for precise control
- Pneumatic actuators for human-like compliance
- Series elastic actuators for safe human interaction

Sensors include:
- IMUs for balance and orientation
- Force/torque sensors for interaction
- Vision systems for perception
- Tactile sensors for touch feedback

## Locomotion and Balance

Maintaining balance is one of the greatest challenges in humanoid robotics. Techniques include:
- Zero Moment Point (ZMP) control
- Capture Point methods
- Whole-body control approaches

## Control Systems

Humanoid robots require sophisticated control systems that coordinate multiple degrees of freedom while maintaining stability and achieving tasks.
"""
        },
        {
            "title": "ROS 2 Fundamentals",
            "order": 3,
            "content": """# ROS 2 Fundamentals

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
"""
        },
        {
            "title": "Digital Twin Simulation (Gazebo + Isaac)",
            "order": 4,
            "content": """# Digital Twin Simulation (Gazebo + Isaac)

## Simulation Environments

Simulation is crucial for robotics development as it allows for safe, cost-effective testing and development. Digital twins provide virtual replicas of physical systems.

## Gazebo Integration

Gazebo is a robot simulation environment that provides:
- High-fidelity physics simulation
- Realistic sensor simulation
- Multiple robot models
- Environment and world creation tools

### Key Features:
- Dynamic simulation with multiple physics engines
- Sensor simulation including cameras, LIDAR, and IMUs
- Plugin system for custom functionality
- Integration with ROS/ROS 2

## Isaac Simulation Tools

Isaac Gym and Isaac Sim provide NVIDIA's simulation platforms for robotics and AI:
- GPU-accelerated physics simulation
- RL environment support
- Synthetic data generation
- PhysX physics engine integration

## Physics Modeling

Accurate physics modeling is essential for effective simulation:
- Rigid body dynamics
- Contact and collision detection
- Friction and material properties
- Fluid dynamics (for advanced applications)
"""
        },
        {
            "title": "Vision-Language-Action Systems",
            "order": 5,
            "content": """# Vision-Language-Action Systems

## Computer Vision Integration

Modern robotics increasingly relies on computer vision for perception. Vision-language-action systems combine visual understanding with language processing to enable complex robot behaviors.

## Language Understanding

Language understanding in robotics involves:
- Natural language processing
- Command interpretation
- Context awareness
- Dialogue management

## Action Planning

Action planning bridges perception and language with physical action:
- Task planning
- Motion planning
- Execution monitoring
- Error recovery

## Multimodal AI

Multimodal AI systems process multiple types of input simultaneously:
- Visual information
- Language input
- Tactile feedback
- Audio cues

These systems enable robots to understand and respond to complex, real-world scenarios that require integration of multiple sensory modalities.
"""
        },
        {
            "title": "Capstone: Simple AI-Robot Pipeline",
            "order": 6,
            "content": """# Capstone: Simple AI-Robot Pipeline

## Integration of All Concepts

This capstone chapter brings together all the concepts learned throughout the textbook to create a complete AI-robot pipeline.

## Project Overview

We'll implement a simple system that:
1. Takes a natural language command
2. Processes it using AI
3. Plans appropriate robot actions
4. Executes those actions in simulation
5. Provides feedback to the user

## Implementation Steps

### Step 1: Natural Language Processing
- Parse user commands
- Extract intent and parameters
- Validate command feasibility

### Step 2: Action Planning
- Generate robot action sequence
- Check for safety constraints
- Optimize execution path

### Step 3: Execution and Monitoring
- Execute planned actions
- Monitor execution status
- Handle exceptions and errors

### Step 4: Feedback and Learning
- Provide execution feedback
- Learn from execution results
- Improve future performance

## Assessment and Evaluation

The system will be evaluated based on:
- Command interpretation accuracy
- Action execution success rate
- Response time
- User satisfaction
"""
        }
    ]

    async with AsyncSessionLocal() as session:
        # Check if chapters already exist
        result = await session.execute(select(Chapter))
        existing_chapters = result.scalars().all()

        if existing_chapters:
            print(f"Found {len(existing_chapters)} existing chapters. Skipping initialization.")
            return

    # Create chapters if none exist
    for chapter_data in chapters_data:
        word_count = len(chapter_data["content"].split())
        await ChapterService.create_chapter(
            title=chapter_data["title"],
            content=chapter_data["content"],
            order=chapter_data["order"],
            word_count=word_count
        )
        print(f"Created chapter: {chapter_data['title']}")

    print("Textbook content initialization completed!")


if __name__ == "__main__":
    asyncio.run(initialize_textbook_content())
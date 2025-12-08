import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.
 */
const sidebars: SidebarsConfig = {
  // Textbook sidebar with structured chapters
  textbookSidebar: [
    {
      type: 'category',
      label: 'Textbook',
      items: [
        'intro',
        {
          type: 'doc',
          id: 'chapters/introduction-to-physical-ai',
          label: 'Introduction to Physical AI',
        },
        {
          type: 'doc',
          id: 'chapters/basics-of-humanoid-robotics',
          label: 'Basics of Humanoid Robotics',
        },
        {
          type: 'doc',
          id: 'chapters/ros-2-fundamentals',
          label: 'ROS 2 Fundamentals',
        },
        {
          type: 'doc',
          id: 'chapters/digital-twin-simulation',
          label: 'Digital Twin Simulation (Gazebo + Isaac)',
        },
        {
          type: 'doc',
          id: 'chapters/vision-language-action-systems',
          label: 'Vision-Language-Action Systems',
        },
        {
          type: 'doc',
          id: 'chapters/capstone-ai-robot-pipeline',
          label: 'Capstone: Simple AI-Robot Pipeline',
        },
      ],
    },
  ],
};

export default sidebars;

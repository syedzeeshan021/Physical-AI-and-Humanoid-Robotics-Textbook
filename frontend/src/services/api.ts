// API service to connect frontend to backend
// The environment variable is replaced by webpack DefinePlugin during build
declare const process: {
  env: {
    REACT_APP_BACKEND_API_URL: string;
  };
};

const BACKEND_API_URL = process.env.REACT_APP_BACKEND_API_URL || 'http://localhost:8000/api/v1';

class ApiService {
  async getChapters() {
    try {
      const response = await fetch(`${BACKEND_API_URL}/chapters`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      console.error('Error fetching chapters:', error);
      // Return mock data if API is not available
      return [
        { id: '1', title: 'Introduction to Physical AI', order: 1, word_count: 1500 },
        { id: '2', title: 'Basics of Humanoid Robotics', order: 2, word_count: 1800 },
        { id: '3', title: 'ROS 2 Fundamentals', order: 3, word_count: 1700 },
        { id: '4', title: 'Digital Twin Simulation (Gazebo + Isaac)', order: 4, word_count: 1900 },
        { id: '5', title: 'Vision-Language-Action Systems', order: 5, word_count: 1600 },
        { id: '6', title: 'Capstone: Simple AI-Robot Pipeline', order: 6, word_count: 2000 }
      ];
    }
  }

  async getChapterById(id: string) {
    try {
      const response = await fetch(`${BACKEND_API_URL}/chapters/${id}`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      console.error(`Error fetching chapter ${id}:`, error);
      // Return mock data if API is not available
      return {
        id,
        title: `Chapter ${id}`,
        content: `# Chapter ${id}\n\nThis is placeholder content for chapter ${id}. The actual content would come from the backend API when connected.`,
        order: parseInt(id)
      };
    }
  }

  async queryRag(query: string, sessionId?: string) {
    try {
      const response = await fetch(`${BACKEND_API_URL}/rag/query`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query, session_id: sessionId }),
      });
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      console.error('Error querying RAG:', error);
      // Return mock response if API is not available
      return {
        response: `This is a simulated response to your query: "${query}". The actual RAG response would come from the backend API when connected.`,
        sources: ['Simulated Response'],
        session_id: sessionId || 'mock-session-id'
      };
    }
  }
}

export default new ApiService();
import React, { createContext, useContext, useState, useEffect } from 'react';

// Get the backend API URL from webpack DefinePlugin
const BACKEND_API_URL = typeof process !== 'undefined' ?
  (process.env.REACT_APP_BACKEND_API_URL || 'http://localhost:8000/api/v1') :
  'http://localhost:8000/api/v1';

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check if user is logged in on component mount
    const token = localStorage.getItem('access_token');
    if (token) {
      // Decode token to get user info (simplified - in real app you might decode JWT)
      const storedUser = localStorage.getItem('user');
      if (storedUser) {
        try {
          const userData = JSON.parse(storedUser);
          setUser(userData);
          setIsAuthenticated(true);
        } catch (error) {
          console.error('Error parsing user data:', error);
        }
      }
    }
    setLoading(false);
  }, []);

  const login = async (email, password) => {
    try {
      const response = await fetch(`${BACKEND_API_URL}/auth/token`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
          username: email,
          password: password,
        }),
      });

      if (response.ok) {
        const data = await response.json();
        localStorage.setItem('access_token', data.access_token);

        // Get user details
        const userResponse = await fetch(`${BACKEND_API_URL}/users/me`, {
          headers: {
            'Authorization': `Bearer ${data.access_token}`
          }
        });

        if (userResponse.ok) {
          const userData = await userResponse.json();
          localStorage.setItem('user', JSON.stringify(userData));
          setUser(userData);
          setIsAuthenticated(true);
          return { success: true };
        } else {
          // Even if /users/me fails, we still have the token, so login was technically successful
          // We'll set basic user info from the token response
          const basicUserData = {
            email,
            id: null // We don't have the ID if /users/me failed
          };
          localStorage.setItem('user', JSON.stringify(basicUserData));
          setUser(basicUserData);
          setIsAuthenticated(true);
          return { success: true };
        }
      } else {
        const errorData = await response.json();
        return { success: false, error: errorData.detail || 'Login failed' };
      }
    } catch (error) {
      console.error('Login error:', error);
      return { success: false, error: 'Network error' };
    }
  };

  const register = async (email, password, softwareBackground, hardwareBackground) => {
    try {
      const response = await fetch(`${BACKEND_API_URL}/auth/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email,
          password,
          software_background: softwareBackground,
          hardware_background: hardwareBackground
        }),
      });

      if (response.ok) {
        const data = await response.json();
        localStorage.setItem('access_token', data.access_token);

        // Get user details
        const userResponse = await fetch(`${BACKEND_API_URL}/users/me`, {
          headers: {
            'Authorization': `Bearer ${data.access_token}`
          }
        });

        if (userResponse.ok) {
          const userData = await userResponse.json();
          localStorage.setItem('user', JSON.stringify(userData));
          setUser(userData);
          setIsAuthenticated(true);
          return { success: true };
        } else {
          // Even if /users/me fails, we still have the token, so registration was technically successful
          // We'll set basic user info from the token response
          const basicUserData = {
            email,
            id: null // We don't have the ID if /users/me failed
          };
          localStorage.setItem('user', JSON.stringify(basicUserData));
          setUser(basicUserData);
          setIsAuthenticated(true);
          return { success: true };
        }
      } else {
        const errorData = await response.json();
        return { success: false, error: errorData.detail || 'Registration failed' };
      }
    } catch (error) {
      console.error('Registration error:', error);
      return { success: false, error: 'Network error' };
    }
  };

  const logout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
    setUser(null);
    setIsAuthenticated(false);
  };

  const value = {
    user,
    isAuthenticated,
    loading,
    login,
    register,
    logout
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};
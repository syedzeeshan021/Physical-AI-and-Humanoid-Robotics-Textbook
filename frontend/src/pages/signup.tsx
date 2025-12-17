import React, { useState } from 'react';
import Layout from '@theme/Layout';
import { useAuth } from '../components/Auth/AuthContext';
import { useHistory, Redirect } from '@docusaurus/router';

const SignupPage = () => {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    confirmPassword: '',
    softwareBackground: '',
    hardwareBackground: ''
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { isAuthenticated, register } = useAuth();
  const history = useHistory();

  if (isAuthenticated) {
    return <Redirect to="/" />;
  }

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (formData.password !== formData.confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    setLoading(true);
    setError('');

    const result = await register(
      formData.email,
      formData.password,
      formData.softwareBackground,
      formData.hardwareBackground
    );

    if (result.success) {
      history.push('/');
    } else {
      setError(result.error);
      setLoading(false);
    }
  };

  return (
    <Layout title="Sign Up" description="Create an account for the Physical AI & Humanoid Robotics platform">
      <div style={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        minHeight: '80vh',
        padding: '20px'
      }}>
        <div style={{
          width: '100%',
          maxWidth: '500px',
          padding: '30px',
          border: '1px solid #ddd',
          borderRadius: '8px',
          backgroundColor: '#fff',
          boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)'
        }}>
          <h1 style={{ textAlign: 'center', marginBottom: '20px' }}>Create Account</h1>
          <p style={{ textAlign: 'center', marginBottom: '20px', color: '#666' }}>
            Tell us about your background to personalize your learning experience
          </p>

          {error && (
            <div style={{
              backgroundColor: '#ffebee',
              color: '#c62828',
              padding: '10px',
              borderRadius: '4px',
              marginBottom: '15px'
            }}>
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit}>
            <div style={{ marginBottom: '15px' }}>
              <label htmlFor="email" style={{ display: 'block', marginBottom: '5px' }}>Email</label>
              <input
                type="email"
                id="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                required
                style={{
                  width: '100%',
                  padding: '10px',
                  border: '1px solid #ddd',
                  borderRadius: '4px',
                  fontSize: '16px'
                }}
              />
            </div>

            <div style={{ marginBottom: '15px' }}>
              <label htmlFor="password" style={{ display: 'block', marginBottom: '5px' }}>Password</label>
              <input
                type="password"
                id="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                required
                minLength={6}
                style={{
                  width: '100%',
                  padding: '10px',
                  border: '1px solid #ddd',
                  borderRadius: '4px',
                  fontSize: '16px'
                }}
              />
            </div>

            <div style={{ marginBottom: '15px' }}>
              <label htmlFor="confirmPassword" style={{ display: 'block', marginBottom: '5px' }}>Confirm Password</label>
              <input
                type="password"
                id="confirmPassword"
                name="confirmPassword"
                value={formData.confirmPassword}
                onChange={handleChange}
                required
                style={{
                  width: '100%',
                  padding: '10px',
                  border: '1px solid #ddd',
                  borderRadius: '4px',
                  fontSize: '16px'
                }}
              />
            </div>

            <div style={{ marginBottom: '15px' }}>
              <label htmlFor="softwareBackground" style={{ display: 'block', marginBottom: '5px' }}>
                Your Software Background
              </label>
              <select
                id="softwareBackground"
                name="softwareBackground"
                value={formData.softwareBackground}
                onChange={handleChange}
                required
                style={{
                  width: '100%',
                  padding: '10px',
                  border: '1px solid #ddd',
                  borderRadius: '4px',
                  fontSize: '16px'
                }}
              >
                <option value="">Select your background</option>
                <option value="beginner">Beginner (Just starting)</option>
                <option value="intermediate">Intermediate (Some experience)</option>
                <option value="advanced">Advanced (Professional experience)</option>
                <option value="expert">Expert (Deep technical knowledge)</option>
              </select>
            </div>

            <div style={{ marginBottom: '20px' }}>
              <label htmlFor="hardwareBackground" style={{ display: 'block', marginBottom: '5px' }}>
                Your Hardware Background
              </label>
              <select
                id="hardwareBackground"
                name="hardwareBackground"
                value={formData.hardwareBackground}
                onChange={handleChange}
                required
                style={{
                  width: '100%',
                  padding: '10px',
                  border: '1px solid #ddd',
                  borderRadius: '4px',
                  fontSize: '16px'
                }}
              >
                <option value="">Select your background</option>
                <option value="beginner">Beginner (Just starting)</option>
                <option value="intermediate">Intermediate (Some experience)</option>
                <option value="advanced">Advanced (Professional experience)</option>
                <option value="expert">Expert (Deep technical knowledge)</option>
              </select>
            </div>

            <button
              type="submit"
              disabled={loading}
              style={{
                width: '100%',
                padding: '12px',
                backgroundColor: '#4CAF50',
                color: 'white',
                border: 'none',
                borderRadius: '4px',
                fontSize: '16px',
                cursor: loading ? 'not-allowed' : 'pointer',
                opacity: loading ? 0.6 : 1
              }}
            >
              {loading ? 'Creating Account...' : 'Sign Up'}
            </button>
          </form>

          <div style={{ textAlign: 'center', marginTop: '15px' }}>
            <p>
              Already have an account?{' '}
              <a href="/login" style={{ color: '#2196F3' }}>Sign in here</a>
            </p>
          </div>
        </div>
      </div>
    </Layout>
  );
};

export default SignupPage;
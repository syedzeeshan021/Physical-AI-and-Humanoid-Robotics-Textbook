import React from 'react';
import { AuthProvider } from '../components/Auth/AuthContext';
import ChatWidget from '../components/ChatWidget';
import TextSelectionPopup from '../components/TextSelectionPopup';

// Root component that wraps the entire application
// This allows us to add global components like the chat widget and auth context
const Root = ({ children }: { children: React.ReactNode }) => {
  return (
    <AuthProvider>
      {children}
      <ChatWidget />
      <TextSelectionPopup />
    </AuthProvider>
  );
};

export default Root;
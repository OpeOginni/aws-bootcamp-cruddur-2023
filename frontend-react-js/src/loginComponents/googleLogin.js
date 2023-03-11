import React, { useEffect } from 'react';
import jwt from 'jwt-decode';
import { Auth } from 'aws-amplify';

// Got code from https://docs.amplify.aws/lib/auth/advanced/q/platform/js/#facebook-sign-in-react-native---expo

export default function SignInWithGoogle() {
  useEffect(() => {
  // Check for an existing Google client initialization
    if (!window.google && !window.google?.accounts) createScript();
  }, []);

  // Load the Google client
  const createScript = () => {
    const script = document.createElement('script');
    script.src = 'https://accounts.google.com/gsi/client';
    script.async = true;
    script.defer = true;
    script.onload = initGsi;
    document.body.appendChild(script);
  }

  // Initialize Google client and render Google button
  const initGsi = () => {
    if (window.google && window.google?.accounts) {
      window.google.accounts.id.initialize({
        // Need a userPoolDomain to get a GOOGLE_CLIENT_ID
        client_id: process.env.GOOGLE_CLIENT_ID,
        callback: (response) => {
          getAWSCredentials(response.credential)
        },
      });
      window.google.accounts.id.renderButton(
        document.getElementById("googleSignInButton"),
        { theme: "outline", size: "large" }
      );
    }
  }

  // Exchange Google token for temporary AWS credentials
  const getAWSCredentials = async (credential) => {
    const token = jwt(credential);
    const user = {
      email: token.email,
      name: token.name
    };      
    await Auth.federatedSignIn(
      'google',
      { token: credential, expires_at: token.exp },
      user
    );
  }

  return (
    <div>
      <button id="googleSignInButton"/>
    </div>
  );
}
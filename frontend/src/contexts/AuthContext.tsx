// import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
// import { useNavigate } from 'react-router-dom';

// interface Profile {
//   id: string;
//   user_id: string;
//   full_name: string;
//   email: string;
//   contact_number: string | null;
//   college_name: string | null;
//   college_id: string | null;
//   college_email: string | null;
//   course_name?: string | null;
//   course_mode?: 'online' | 'offline' | null;
//   course_duration?: 'long' | 'short' | null;
//   username: string | null;
//   avatar_url: string | null;
//   status: 'pending' | 'active' | 'suspended';
//   created_at: string;
//   updated_at: string;
// }

// interface AuthUser {
//   id: string;
//   email: string;
//   profile: Profile | null;
//   role: 'student' | 'admin' | null;
// }

// interface AuthContextType {
//   user: AuthUser | null;
//   isLoading: boolean;
//   isAuthenticated: boolean;
//   signUp: (email: string, password: string, metadata: Record<string, string>) => Promise<{ success: boolean; message: string }>;
//   signIn: (username: string, password: string) => Promise<{ success: boolean; message: string; role?: string }>;
//   signOut: () => Promise<void>;
//   refreshProfile: () => Promise<void>;
// }

// const AuthContext = createContext<AuthContextType | undefined>(undefined);

// const INACTIVITY_TIMEOUT = 15 * 60 * 1000; // 15 minutes

// const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5001';

// export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
//   const [user, setUser] = useState<AuthUser | null>(null);
//   const [isLoading, setIsLoading] = useState(true);

//   const fetchUserData = useCallback(async (): Promise<AuthUser | null> => {
//     const token = localStorage.getItem('access_token');
//     if (!token) return null;
    
//     try {
//       const res = await fetch(`${API_URL}/auth/me`, { headers: { Authorization: `Bearer ${token}` } });
//       if (!res.ok) {
//         // token invalid
//         localStorage.removeItem('access_token');
//         localStorage.removeItem('refresh_token');
//         return null;
//       }
      
//       let data;
//       try {
//         data = await res.json();
//       } catch (jsonError) {
//         console.error('Failed to parse user data response:', jsonError);
//         return null;
//       }
      
//       if (data?.success) {
//         const u = data.user;
//         const role = (u.role || 'student').toLowerCase();
//         return {
//           id: u.id,
//           email: u.email,
//           profile: (u.profile || null) as Profile | null,
//           role: role === 'admin' ? 'admin' : 'student',
//         };
//       }
//       return null;
//     } catch (error) {
//       console.error('Error fetching user data:', error);
//       return null;
//     }
//   }, []);

//   useEffect(() => {
//     (async () => {
//       setIsLoading(true);
//       const userData = await fetchUserData();
//       if (userData) {
//         setUser(userData);
//       }
//       setIsLoading(false);
//     })();
//   }, [fetchUserData]);

//   // Auto logout on inactivity
//   useEffect(() => {
//     if (!user) return;

//     let inactivityTimer: NodeJS.Timeout;

//     const resetTimer = () => {
//       clearTimeout(inactivityTimer);
//       inactivityTimer = setTimeout(async () => {
//         // clear tokens and redirect
//         localStorage.removeItem('access_token');
//         localStorage.removeItem('refresh_token');
//         setUser(null);
//         window.location.href = '/auth/login?reason=inactivity';
//       }, INACTIVITY_TIMEOUT);
//     };

//     const events = ['mousedown', 'keydown', 'scroll', 'touchstart'];
//     events.forEach(event => document.addEventListener(event, resetTimer));
//     resetTimer();

//     return () => {
//       clearTimeout(inactivityTimer);
//       events.forEach(event => document.removeEventListener(event, resetTimer));
//     };
//   }, [user]);

//   const signUp = useCallback(async (email: string, password: string, metadata: Record<string, string>) => {
//     const res = await fetch(`${API_URL}/auth/signup`, {
//       method: 'POST',
//       headers: { 'Content-Type': 'application/json' },
//       body: JSON.stringify({ email, password, ...metadata }),
//     });
//     const data = await res.json();
//     if (!res.ok) return { success: false, message: data?.message || 'Signup failed' };
//     return { success: true, message: data?.message || 'Signup successful' };
//   }, []);

//   const signIn = useCallback(async (username: string, password: string) => {
//     try {
//       // If the user entered an email in the username field, send it as `email`
//       const payload: Record<string, string> = username.includes('@')
//         ? { email: username, password }
//         : { username, password };

//       const res = await fetch(`${API_URL}/auth/login`, {
//         method: 'POST',
//         headers: { 'Content-Type': 'application/json' },
//         body: JSON.stringify(payload),
//       });
      
//       // Check if response is ok before parsing JSON
//       let data;
//       try {
//         data = await res.json();
//       } catch (jsonError) {
//         return { success: false, message: 'Invalid response from server. Please check if backend is running.' };
//       }
      
//       if (!res.ok) {
//         return { success: false, message: data?.message || 'Login failed' };
//       }

//       // Validate response has required fields
//       if (!data.access_token) {
//         return { success: false, message: 'Server response missing authentication token' };
//       }

//       // store tokens
//       localStorage.setItem('access_token', data.access_token);
//       localStorage.setItem('refresh_token', data.refresh_token || '');

//       // Get role from login response first (faster than fetching user data)
//       const loginRole = data?.user?.role || 'student';
      
//       // Try to fetch user data, but don't fail if it doesn't work
//       try {
//         const userData = await fetchUserData();
//         if (userData) {
//           // Ensure role is set correctly
//           const finalUserData = { ...userData, role: userData.role || loginRole };
//           setUser(finalUserData);
//           return { success: true, message: 'Login successful!', role: finalUserData.role || 'student' };
//         }
//       } catch (fetchError) {
//         console.error('Failed to fetch user data:', fetchError);
//         // Continue with login role if fetch fails
//       }

//       // If fetchUserData fails, use login response data
//       const userFromLogin = {
//         id: data.user?.id || '',
//         email: data.user?.email || '',
//         profile: null,
//         role: loginRole,
//       };
//       setUser(userFromLogin);
      
//       return { success: true, message: 'Login successful!', role: loginRole };
//     } catch (error) {
//       console.error('Login error:', error);
//       const errorMessage = error instanceof Error ? error.message : 'Network error. Please check your connection.';
//       return { success: false, message: errorMessage };
//     }
//   }, [fetchUserData]);

//   const signOut = useCallback(async () => {
//     localStorage.removeItem('access_token');
//     localStorage.removeItem('refresh_token');
//     setUser(null);
//   }, []);

//   const refreshProfile = useCallback(async () => {
//     const userData = await fetchUserData();
//     if (userData) setUser(userData);
//   }, [fetchUserData]);

//   return (
//     <AuthContext.Provider
//       value={{
//         user,
//         isLoading,
//         isAuthenticated: !!user,
//         signUp,
//         signIn,
//         signOut,
//         refreshProfile,
//       }}
//     >
//       {children}
//     </AuthContext.Provider>
//   );
// };

// export const useAuth = () => {
//   const context = useContext(AuthContext);
//   if (context === undefined) {
//     throw new Error('useAuth must be used within an AuthProvider');
//   }
//   return context;
// };





import React, {
  createContext,
  useContext,
  useState,
  useEffect,
  useCallback,
} from 'react';
import { useNavigate } from 'react-router-dom';

/* =======================
   Types
======================= */

interface Profile {
  id: string;
  user_id: string;
  full_name: string;
  email: string;
  contact_number: string | null;
  college_name: string | null;
  college_id: string | null;
  college_email: string | null;
  course_name?: string | null;
  course_mode?: 'online' | 'offline' | null;
  course_duration?: 'long' | 'short' | null;
  username: string | null;
  avatar_url: string | null;
  status: 'pending' | 'active' | 'suspended';
  created_at: string;
  updated_at: string;
}

interface AuthUser {
  id: string;
  email: string;
  profile: Profile | null;
  role: 'student' | 'admin' | null;
}

interface AuthContextType {
  user: AuthUser | null;
  isLoading: boolean;
  isAuthenticated: boolean;

  /* Existing */
  signUp: (
    email: string,
    password: string,
    metadata: Record<string, string>
  ) => Promise<{ success: boolean; message: string }>;

  signIn: (
    username: string,
    password: string
  ) => Promise<{ success: boolean; message: string; role?: string }>;

  signOut: () => Promise<void>;
  refreshProfile: () => Promise<void>;

  /* NEW (non-breaking) */
  verifySignupOtp: (
    email: string,
    otp: string
  ) => Promise<{ success: boolean; message: string }>;
}

/* =======================
   Setup
======================= */

const AuthContext = createContext<AuthContextType | undefined>(undefined);

const INACTIVITY_TIMEOUT = 15 * 60 * 1000; // 15 minutes
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5001';

/* =======================
   Provider
======================= */

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  const [user, setUser] = useState<AuthUser | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const navigate = useNavigate();

  /* =======================
     Fetch Logged-in User
  ======================= */

  const fetchUserData = useCallback(async (): Promise<AuthUser | null> => {
    const token = localStorage.getItem('access_token');
    if (!token) return null;

    try {
      const res = await fetch(`${API_URL}/auth/me`, {
        headers: { Authorization: `Bearer ${token}` },
      });

      if (!res.ok) {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        return null;
      }

      const data = await res.json();
      if (!data?.success) return null;

      const u = data.user;
      const role = (u.role || 'student').toLowerCase();

      return {
        id: u.id,
        email: u.email,
        profile: (u.profile || null) as Profile | null,
        role: role === 'admin' ? 'admin' : 'student',
      };
    } catch (error) {
      console.error('Error fetching user data:', error);
      return null;
    }
  }, []);

  /* =======================
     Init Auth
  ======================= */

  useEffect(() => {
    (async () => {
      setIsLoading(true);
      const userData = await fetchUserData();
      if (userData) setUser(userData);
      setIsLoading(false);
    })();
  }, [fetchUserData]);

  /* =======================
     Auto Logout (Inactivity)
  ======================= */

  useEffect(() => {
    if (!user) return;

    let inactivityTimer: NodeJS.Timeout;

    const resetTimer = () => {
      clearTimeout(inactivityTimer);
      inactivityTimer = setTimeout(() => {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        setUser(null);
        navigate('/auth/login?reason=inactivity');
      }, INACTIVITY_TIMEOUT);
    };

    ['mousedown', 'keydown', 'scroll', 'touchstart'].forEach(event =>
      document.addEventListener(event, resetTimer)
    );

    resetTimer();

    return () => {
      clearTimeout(inactivityTimer);
      ['mousedown', 'keydown', 'scroll', 'touchstart'].forEach(event =>
        document.removeEventListener(event, resetTimer)
      );
    };
  }, [user, navigate]);

  /* =======================
     NEW: Verify Signup OTP
  ======================= */

  const verifySignupOtp = useCallback(
    async (email: string, otp: string) => {
      try {
        const res = await fetch(`${API_URL}/auth/verify-signup-otp`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email, otp }),
        });

        const data = await res.json();
        if (!res.ok) {
          return {
            success: false,
            message: data?.message || 'Invalid or expired OTP',
          };
        }

        return { success: true, message: 'OTP verified' };
      } catch (error) {
        return {
          success: false,
          message: 'Unable to verify OTP. Please try again.',
        };
      }
    },
    []
  );

  /* =======================
     Signup (OTP-aware)
  ======================= */

  const signUp = useCallback(
    async (email: string, password: string, metadata: Record<string, string>) => {
      try {
        const res = await fetch(`${API_URL}/auth/signup`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email, password, ...metadata }),
        });

        const data = await res.json();

        if (!res.ok) {
          return {
            success: false,
            message: data?.message || 'Signup failed',
          };
        }

        return {
          success: true,
          message: data?.message || 'Signup successful',
        };
      } catch (error) {
        return {
          success: false,
          message: 'Network error during signup',
        };
      }
    },
    []
  );

  /* =======================
     Login
  ======================= */

  const signIn = useCallback(
    async (username: string, password: string) => {
      try {
        const payload = username.includes('@')
          ? { email: username, password }
          : { username, password };

        const res = await fetch(`${API_URL}/auth/login`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload),
        });

        const data = await res.json();
        if (!res.ok) {
          return {
            success: false,
            message: data?.message || 'Login failed',
          };
        }

        if (!data.access_token) {
          return {
            success: false,
            message: 'Invalid login response',
          };
        }

        localStorage.setItem('access_token', data.access_token);
        localStorage.setItem('refresh_token', data.refresh_token || '');

        const userData = await fetchUserData();
        if (userData) setUser(userData);

        return {
          success: true,
          message: 'Login successful',
          role: userData?.role || 'student',
        };
      } catch (error) {
        return {
          success: false,
          message: 'Network error during login',
        };
      }
    },
    [fetchUserData]
  );

  /* =======================
     Logout
  ======================= */

  const signOut = useCallback(async () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    setUser(null);
    navigate('/auth/login');
  }, [navigate]);

  /* =======================
     Refresh Profile
  ======================= */

  const refreshProfile = useCallback(async () => {
    const userData = await fetchUserData();
    if (userData) setUser(userData);
  }, [fetchUserData]);

  /* =======================
     Provider
  ======================= */

  return (
    <AuthContext.Provider
      value={{
        user,
        isLoading,
        isAuthenticated: !!user,
        signUp,
        signIn,
        signOut,
        refreshProfile,
        verifySignupOtp, // NEW (safe)
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

/* =======================
   Hook
======================= */

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

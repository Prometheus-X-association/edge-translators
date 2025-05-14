import { AuthProvider } from "react-admin";
import { API_URL } from "./constants"
import { jwtDecode } from "jwt-decode";

interface AuthResponse {
  access_token: string,
  expires_in: number,
  token_type: "bearer"
}

interface JwtPayload {
  role: string; // you can adjust if your JWT payload has a different structure
  [key: string]: any; // other fields
}

export const authProvider: AuthProvider = {
  async login({username, password})  {

    const headers = new Headers();
    headers.append("Accept", "application/json");
    headers.append("Content-Type", 'application/x-www-form-urlencoded');
    
    const payload = new URLSearchParams();
    payload.append("grant_type", "password");
    payload.append("username", username);
    payload.append("password", password);
    
    const request = new Request(`${API_URL}/auth/token`, {
      method: 'POST',
      body: payload,
      headers: headers,
    });
    let response;
    try {
      response = await fetch(request);
    } catch (e) {
      throw new Error(`Network error ${e}`);
    }

    if (response.status < 200 || response.status >= 300) {
      throw new Error(response.statusText);
    }

    const auth_response: AuthResponse = await response.json();

     const decoded: JwtPayload = jwtDecode(auth_response.access_token);
     console.log(decoded)

     if (decoded["mindmatcher::role"] !== "ROLE_ADMIN") {
       throw new Error("Unauthorized"); // Stop login if not admin
     }

    localStorage.setItem('auth', JSON.stringify(auth_response));
  },
  logout: () => {
    localStorage.removeItem("auth");
    return Promise.resolve();
  },
  checkError: () => Promise.resolve(),
  checkAuth: () =>
    localStorage.getItem("auth") ? Promise.resolve() : Promise.reject(),
  getPermissions: () => {
    return Promise.resolve(undefined);
  },
  getIdentity: () => {
    const persistedUser = localStorage.getItem("auth");
    const user = persistedUser ? JSON.parse(persistedUser) : null;

    return Promise.resolve(user);
  },
};

export default authProvider;

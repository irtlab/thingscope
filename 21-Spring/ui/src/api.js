import axios from 'axios';


export const backendURL =  process.env.NODE_ENV === 'development' ?
  'https://thingscope.cs.columbia.edu' : window.location.origin;

export const apiURL = `${backendURL}/api`;
export const api = axios.create({baseURL: apiURL, withCredentials: true});

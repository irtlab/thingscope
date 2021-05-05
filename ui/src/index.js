import React, { useState } from 'react';
import ReactDOM from 'react-dom';
import socketIOClient from 'socket.io-client';
import CssBaseline from '@material-ui/core/CssBaseline';
import { BrowserRouter } from 'react-router-dom';
import { SnackbarProvider } from 'notistack';
import './index.css';
import App from './app';
import { apiURL } from './api';
import * as serviceWorker from './serviceWorker';


/*
 * This component is the main entry point to the entire React application. We
 * perform initialization here and setup various middlewares and contexts that
 * need to be available across the entire application.
 */
function Main() {
  const UserContext = React.createContext();
  const [socket, setSocket] = useState(null/*socketIOClient(apiURL)*/);

  return (
    <>
      <CssBaseline />
      <BrowserRouter>
        <SnackbarProvider maxSnack={5}>
          <UserContext.Provider value={{socket: null}}>
            <App />
          </UserContext.Provider>
        </SnackbarProvider>
      </BrowserRouter>
    </>
  );
}

ReactDOM.render(<Main />, document.getElementById('root'));

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();

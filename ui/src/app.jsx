import React, { useState, useContext } from 'react';
import { Switch, Route } from 'react-router-dom';
import { makeStyles } from '@material-ui/core';
import AppBarComponent from './components/app_bar';
import ListDrawer from './components/list_drawer';
import DeviceView from './device';

// const UserContext = React.createContext();

const useStyles = makeStyles((theme) => ({
  root: {
    display: 'flex'
  },
  toolbar: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'flex-end',
    padding: theme.spacing(0, 1),
    // necessary for content to be below app bar
    ...theme.mixins.toolbar
  },
  content: {
    flexGrow: 1,
    padding: theme.spacing(0.5),
    paddingTop: '90px',
    background: '#eef4f9'
  }
}));


// TODO not finished
function NotFoundPage() {
  return (
    <div>
      Page Not Found
    </div>
  );
}


export default function App() {
  const classes = useStyles();
  const [open, setOpen] = useState(false);
  const [selectedListItem, setSelectedListItem] = useState('');

  return (
    <div className={classes.root}>
      <AppBarComponent
        selectedItem={selectedListItem}
        open={open}
        setOpen={setOpen}
      />
      <ListDrawer
        open={open}
        setOpen={setOpen}
        selectedListItem={selectedListItem}
        setSelectedListItem={setSelectedListItem}
      />
      <Switch>
        <PrivateRoute exact path="/" component={DeviceView} />
        <PrivateRoute exact path="/devices" component={DeviceView} />
        <Route exact component={NotFoundPage} />
      </Switch>
    </div>
  );
}


function PrivateRoute({ component: Component, ...rest }) {
  const classes = useStyles();
  // const { socket } = useContext(UserContext);

  return (
    <Route
      {...rest}
      render={(props) => (
        <main className={classes.content}>
          <div className={classes.toolbar} >
            <Component {...props} socket={null} />
          </div>
        </main>
      )}
    />
  );
}

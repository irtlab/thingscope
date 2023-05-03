import React from 'react';
import clsx from 'clsx';
import PropTypes from 'prop-types';
import MenuIcon from '@material-ui/icons/Menu';
import {
  AppBar,
  Button,
  Toolbar,
  Typography,
  makeStyles,
  IconButton
} from '@material-ui/core';
import { listTabText } from '../utils';

const drawerWidth = 240;

const useStyles = makeStyles((theme) => ({
  appBar: {
    zIndex: theme.zIndex.drawer + 1,
    transition: theme.transitions.create(['width', 'margin'], {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.leavingScreen
    }),
    backgroundColor: '#2da9d8'
  },
  appBarShift: {
    marginLeft: drawerWidth,
    width: `calc(100% - ${drawerWidth}px)`,
    transition: theme.transitions.create(['width', 'margin'], {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.enteringScreen
    })
  },
  menuButton: {
    marginRight: 36
  },
  profile: {
    paddingLeft: '12px',
    paddingRight: '12px',
    minWidth: '160px'
  }
}));


export default function AppBarComponent(props) {
  const { selectedItem, open, setOpen } = props;
  const classes = useStyles();
  const logoURL = 'https://thingscope.cs.columbia.edu/public/irt_logo.svg';
  const cuURL = 'https://thingscope.cs.columbia.edu/public/cs_cu.svg';

  return (
    <>
      <AppBar
        position="fixed"
        className={clsx(classes.appBar, {
          [classes.appBarShift]: open
        })}
      >
        <Toolbar>
          <IconButton
            color="inherit"
            aria-label="open drawer"
            onClick={() => setOpen(true)}
            edge="start"
            className={clsx(classes.menuButton, {
              [classes.hide]: open
            })}
          >
            <MenuIcon />
          </IconButton>
          <Typography variant="h6" noWrap>
            { listTabText(selectedItem) }
          </Typography>
          <div style={{marginLeft: 'auto'}}>
            <img src={cuURL} alt="logo" style={{ marginRight: '15px', width: 55, borderRadius: '12%', float: 'left' }}/>
            <img src={logoURL} alt="logo" style={{ width: 55, borderRadius: '12%', float: 'left' }}/>
            <Typography variant="h5" gutterBottom style={{minWidth: 440, marginTop: '10px'}}>
                  &nbsp;
              {'IRT Lab Columbia University'}
                  &nbsp;
            </Typography>
          </div>
        </Toolbar>
      </AppBar>
    </>
  );
}

AppBarComponent.propTypes = {
  selectedItem: PropTypes.string.isRequired,
  open: PropTypes.bool.isRequired,
  setOpen: PropTypes.func.isRequired
};

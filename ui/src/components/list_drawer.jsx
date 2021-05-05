import React, { useEffect } from 'react';
import clsx from 'clsx';
import PropTypes from 'prop-types';
import { useHistory, useLocation } from 'react-router-dom';
import {
  Drawer,
  Link,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Typography,
  Tooltip,
  Divider,
  IconButton,
  makeStyles,
  useTheme
} from '@material-ui/core';
import ChevronLeftIcon from '@material-ui/icons/ChevronLeft';
import ChevronRightIcon from '@material-ui/icons/ChevronRight';
import MonetizationOnIcon from '@material-ui/icons/MonetizationOn';
import DevicesIcon from '@material-ui/icons/Devices';
import ShareIcon from '@material-ui/icons/Share';
import { listTabText } from '../utils';

const drawerWidth = 240;

const useStyles = makeStyles((theme) => ({
  hide: {
    display: 'none'
  },
  drawer: {
    width: drawerWidth,
    flexShrink: 0,
    whiteSpace: 'nowrap'
  },
  drawerOpen: {
    width: drawerWidth,
    transition: theme.transitions.create('width', {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.enteringScreen
    })
  },
  drawerClose: {
    transition: theme.transitions.create('width', {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.leavingScreen
    }),
    overflowX: 'hidden',
    width: theme.spacing(7) + 1,
    [theme.breakpoints.up('sm')]: {
      width: theme.spacing(9) + 1
    }
  },
  toolbar: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'flex-end',
    padding: theme.spacing(0, 1),
    // necessary for content to be below app bar
    ...theme.mixins.toolbar
  }
}));


function listTabIcon(idx) {
  return idx === 0 ? <DevicesIcon /> : idx === 1 ? <MonetizationOnIcon /> : <ShareIcon />;
}


export default function ListDrawer(props) {
  const classes = useStyles();
  const theme = useTheme();
  const location = useLocation();
  const history = useHistory();
  const {
    open, setOpen, selectedListItem, setSelectedListItem
  } = props;

  const setPath = (pathname) => {
    switch (pathname) {
    case '/':
      setSelectedListItem('devices');
      history.push('devices');
      break;
    case '/devices':
      setSelectedListItem('devices');
      break;
    default:
        // TODO what to do?
    }
  };

  useEffect(() => {
    setPath(`/${location.pathname.split('/')[1]}`);
  }, [location.pathname]);

  return (
    <Drawer
      variant="permanent"
      className={clsx(classes.drawer, {
        [classes.drawerOpen]: open,
        [classes.drawerClose]: !open
      })}
      classes={{
        paper: clsx({
          [classes.drawerOpen]: open,
          [classes.drawerClose]: !open
        })
      }}
    >
      <div className={classes.toolbar}>
        <Typography variant="h5">
        ThingScope
        </Typography>
        <IconButton onClick={() => setOpen(false)}>
          {theme.direction === 'rtl' ? <ChevronRightIcon /> : <ChevronLeftIcon />}
        </IconButton>
      </div>
      <Divider />
      <List>
        {['devices'].map((text, index) => (
          <ListItem
            hover={text}
            button
            key={text}
            component={Link}
            to={`/${text}`}
            selected={selectedListItem === text}
            onClick={() => {
              setSelectedListItem(text);
              history.push(`/${text}`);
            }}
          >
            <Tooltip title={listTabText(text)}>
              <ListItemIcon >
                { listTabIcon(index) }
              </ListItemIcon>
            </Tooltip>
            <ListItemText primary={listTabText(text)} />
          </ListItem>
        ))}
      </List>
    </Drawer>
  );
}

ListDrawer.defaultProps = {
  selectedListItem: ''
};

ListDrawer.propTypes = {
  open: PropTypes.bool.isRequired,
  setOpen: PropTypes.func.isRequired,
  selectedListItem: PropTypes.string,
  setSelectedListItem: PropTypes.func.isRequired
};

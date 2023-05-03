import React from 'react';
import PropTypes from 'prop-types';
import KeyboardArrowUpIcon from '@material-ui/icons/KeyboardArrowUp';
import { Zoom, makeStyles, useScrollTrigger, Fab } from '@material-ui/core';


const useStyles = makeStyles((theme) => ({
  root: {
    position: 'fixed',
    bottom: theme.spacing(2),
    right: theme.spacing(2)
  }
}));


// A floating action buttons appears on scroll to make it easy to get back to the top of the page.
function ScrollTopMain(props) {
  const { children } = props;
  const classes = useStyles();

  const trigger = useScrollTrigger({
    disableHysteresis: true,
    threshold: 100
  });

  const handleClick = (event) => {
    const anchor = (event.target.ownerDocument || document).querySelector('#back-to-top-anchor');
    if (anchor) anchor.scrollIntoView({ behavior: 'smooth', block: 'center' });
  };

  return (
    <Zoom in={trigger}>
      <div onClick={handleClick} role="presentation" className={classes.root}>
        {children}
      </div>
    </Zoom>
  );
}

ScrollTopMain.propTypes = {
  children: PropTypes.element.isRequired
};


export default function ScrollTop(props) {
  return (
    <ScrollTopMain {...props}>
      <Fab color="primary" size="medium" aria-label="scroll back to top">
        <KeyboardArrowUpIcon />
      </Fab>
    </ScrollTopMain>
  );
}

ScrollTop.propTypes = {
  children: PropTypes.element
};

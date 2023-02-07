import React from 'react';
import PropTypes from 'prop-types';
import ErrorOutlineIcon from '@material-ui/icons/ErrorOutline';
import { CircularProgress, Grid, Typography } from '@material-ui/core';

export default function SpinnerPage(props) {
  const { text } = props;

  return (
    <div>
      <Grid
        container
        spacing={0}
        direction="column"
        alignItems="center"
        justify="center"
        style={{ minHeight: '100vh' }}
      >
        <Grid item xs={3}>
          {
            text === 'Something went wrong. Please try again.' ? (
              <ErrorOutlineIcon style={{color: 'red', fontSize: '100px'}} />
            ) : (
              <CircularProgress />
            )
          }
        </Grid>
        <Grid item xs={3}>
          <Typography variant="subtitle1" gutterBottom>
            {text}
          </Typography>
        </Grid>
      </Grid>
    </div>
  );
}

SpinnerPage.defaultProps = {
  text: undefined
};

SpinnerPage.propTypes = {
  text: PropTypes.string
};

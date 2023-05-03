import React from 'react';
import PropTypes from 'prop-types';
import {
  Divider,
  Grid,
  Typography,
  Link,
  List,
  ListItem,
  ListItemText,
  makeStyles
} from '@material-ui/core';


const useStyles = makeStyles((theme) => ({
  root: {
    flexGrow: 1
  },
  section1: {
    margin: theme.spacing(2)
  },
  section2: {
    margin: theme.spacing(0, 2)
  },
  section3: {
    margin: theme.spacing(0, 2)
  }
}));


function SecurityPrivacyPolicies(props) {
  const { classes, row } = props;

  return (
    <div className={classes.section2}>
      Here is going to be the Security and Privacy Policies information
    </div>
  );
}

SecurityPrivacyPolicies.defaultProps = {
  row: undefined
};

SecurityPrivacyPolicies.propTypes = {
  classes: PropTypes.object.isRequired,
  row: PropTypes.object
};


function NetworkDataList(props) {
  const { classes, text, data, type } = props;

  return (
    <div className={classes.section3}>
      <Typography display="inline" gutterBottom variant="subtitle2" style={{fontWeight: 'bold'}}>
        {
          `${text}: (${data.length})`
        }
      </Typography>
      <List component="nav" ria-label="contacts" style={{backgroundColor: '#F8F8FF', maxHeight: 210, overflow: 'auto'}}>
        {
          data.map((item, idx) => (
            <ListItem
              button
              key={idx}
            >
              <ListItemText primary={ type === 'protocols' ? item : item.name } />
            </ListItem>
          ))
        }
      </List>
    </div>
  );
}

NetworkDataList.defaultProps = {
  text: '',
  data: []
};

NetworkDataList.propTypes = {
  classes: PropTypes.object.isRequired,
  text: PropTypes.string,
  data: PropTypes.array
};


function ShowProtocols(props) {
  const { classes, row } = props;
  return (
    <>
      {
        row ? (
          <NetworkDataList
            classes={classes}
            text='List of protocols the device uses'
            data={row.protocols}
            type='protocols'
          />
        ) : null
      }
    </>
  );
}

ShowProtocols.defaultProps = {
  row: undefined
};

ShowProtocols.propTypes = {
  classes: PropTypes.object.isRequired,
  row: PropTypes.object
};


function ShowDomains(props) {
  const { classes, row } = props;
  return (
    <>
      {
        row ? (
          <NetworkDataList
            classes={classes}
            text='List of domains the device connects to'
            data={row.domains}
            type='domains'
          />
        ) : null
      }
    </>
  );
}

ShowDomains.defaultProps = {
  row: undefined
};

ShowDomains.propTypes = {
  classes: PropTypes.object.isRequired,
  row: PropTypes.object
};


function ShowDeviceData(props) {
  const { classes, row } = props;

  return (
    <div className={classes.section2}>
      <Typography display="inline" gutterBottom variant="subtitle2" style={{fontWeight: 'bold'}}>
      Name:
      </Typography>
      {' '}
      {row.device}
      <br />
      <br />
      <Typography display="inline" gutterBottom variant="subtitle2" style={{fontWeight: 'bold'}}>
      Model:
      </Typography>
      {' '}
      {row.device_model}
      <br />
      <br />
      <Typography display="inline" gutterBottom variant="subtitle2" style={{fontWeight: 'bold'}}>
      Manufacturer:
      </Typography>
      {' '}
      {row.manufacturer.name}
      <br />
      <br />
      <Typography display="inline" gutterBottom variant="subtitle2" style={{fontWeight: 'bold'}}>
      Manufacturer website:
        <Link href="#" onClick={(event) => window.open(row.manufacturer.website, '_blank')}>
          { ` ${row.manufacturer.website}` }
        </Link>
      </Typography>
    </div>
  );
}

ShowDeviceData.defaultProps = {
  row: undefined
};

ShowDeviceData.propTypes = {
  classes: PropTypes.object.isRequired,
  row: PropTypes.object
};


export function DetailDevicePanelData({row}) {
  const classes = useStyles();

  return (
    <div className={classes.root}>
      <div className={classes.section1}>
        <Grid container>
          <Grid item xs={6}>
            <Typography gutterBottom variant="h6" style={{fontSize: '1rem', fontWeight: 'bold'}}>
              Device
            </Typography>
          </Grid>
        </Grid>
        <Divider />
      </div>
      <Grid container>
        <Grid item xs={6}>
          <ShowDeviceData classes={classes} row={row} />
          <br />
        </Grid>
      </Grid>
      <div className={classes.section1}>
        <Grid container>
          <Grid item xs={6}>
            <Typography gutterBottom variant="h6" style={{fontSize: '1rem', fontWeight: 'bold'}}>
              Network Data
            </Typography>
          </Grid>
        </Grid>
        <Divider />
      </div>
      <Grid container>
        <Grid item xs={6}>
          <ShowDomains classes={classes} row={row} />
          <br />
        </Grid>
        <Grid item xs={6}>
          <ShowProtocols classes={classes} row={row} />
          <br />
        </Grid>
      </Grid>
      <div className={classes.section1}>
        <Grid container>
          <Grid item xs={6}>
            <Typography gutterBottom variant="h6" style={{fontSize: '1rem', fontWeight: 'bold'}}>
              Security and Privacy Policies
            </Typography>
          </Grid>
        </Grid>
        <Divider />
      </div>
      <Grid container>
        <Grid item xs={6}>
          <SecurityPrivacyPolicies classes={classes} row={row} />
          <br />
        </Grid>
      </Grid>
    </div>
  );
}

DetailDevicePanelData.defaultProps = {
  row: undefined
};

DetailDevicePanelData.propTypes = {
  row: PropTypes.object
};

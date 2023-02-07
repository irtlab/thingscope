import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import MaterialTable from 'material-table';
import { useSnackbar } from 'notistack';
import {
  Grid,
  Typography,
  Link,
  makeStyles,
  withStyles,
  InputBase,
  Paper,
  FormControl,
  Select
} from '@material-ui/core';
import IconButton from '@material-ui/core/IconButton';
import SearchIcon from '@material-ui/icons/Search';
import ClearIcon from '@material-ui/icons/Clear';
import { DetailDevicePanelData } from './components/device_detail';
import { api } from './api';
import SpinnerPage from './components/spinner_page';
import ScrollTop from './components/scroll_top';
import { tableIcons } from './table_icons';
import { createAlert  } from './utils';

const useStyles = makeStyles((theme) => ({
  root: {
    display: 'flex',
    height: '85%'
  },
  input: {
    marginLeft: theme.spacing(1)
  },
  searchButton: {
    float: 'left',
    padding: 10
  },
  searchTypeDev: {
    minWidth: '10px'
  },
  searchTypeDevProp: {
    minWidth: '180px'
  }
}));

const BootstrapInput = withStyles((theme) => ({
  root: {
    'label + &': {
      marginTop: theme.spacing(3)
    }
  },
  input: {
    borderRadius: 4,
    position: 'relative',
    border: '1px solid #ced4da',
    fontSize: 16,
    padding: '12px 26px 10px 12px',
    backgroundColor: '#F5F5F5'
  }
}))(InputBase);


function stringMatching(string, value) {
  if (!value || !string) return false;

  const regex = new RegExp(value.toLowerCase(), 'g');
  const found = (string.toLowerCase()).match(regex);
  if (found) return true;
  return false;
}


// This is designed to make a material-table search custom in order to find
// data in the device schema.
function customSearch(search_obj, search_value) {
  if (!search_obj || !search_value) return null;

  if (typeof (search_obj) !== 'object' && !Array.isArray(search_obj)) {
    const found = stringMatching(JSON.stringify(search_obj), search_value);
    if (found) return search_obj;
  }

  if (Array.isArray(search_obj)) {
    for (let i = 0; i < search_obj.length; i++) {
      const rv = customSearch(search_obj[i], search_value);
      if (rv) return rv;
    }
  }

  const object_values = Object.values(search_obj);
  for (let i = 0; i < object_values.length; i++) {
    const value = object_values[i];

    if (typeof (value) === 'object' || Array.isArray(value)) {
      if (typeof (value) === 'object') {
        const rv = customSearch(value, search_value);
        if (rv) return rv;
      } else {
        for (let j = 0; j < value.length; j++) {
          const rv = customSearch(value[j], search_value);
          if (rv) return rv;
        }
      }
    }

    const found = stringMatching(JSON.stringify(value), search_value);
    if (found) return value;
  }

  return null;
}


function SearchTypeComponent(props) {
  const { type, setType } = props;
  const styleWidth = type === 'Device' ? '100px' : '180px';

  return (
    <FormControl
      variant="filled"
      style={{minWidth: styleWidth, maxWidth: styleWidth}}
    >
      <Select
        style={{height: '100%', backgroundColor: '#F5F5F5'}}
        native
        value={type}
        onChange={(event) => setType(event.target.value)}
        input={<BootstrapInput />}
      >
        <option value={'Device'}>
        Device
        </option>
        <option value={'Device Properties'}>
        Device Properties
        </option>
      </Select>
    </FormControl>
  );
}

SearchTypeComponent.propTypes = {
  type: PropTypes.string.isRequired,
  setType: PropTypes.func.isRequired
};


function SearchComponent(props) {
  const classes = useStyles();
  const { data, setData } = props;
  const [originalData, setOriginalData] = useState([]);
  const [searchType, setSearchType] = useState('Device');
  const [text, setText] = useState('');

  const handleSearchTyping = (event) => {
    const value = event.target.value.trim();
    setText(value);
    if (value) {
      let result = [];
      if (searchType === 'Device') {
        result = data.filter((dev) => customSearch(dev.device, value) !== null ||
          customSearch(dev.device_model, value) !== null ||
          customSearch(dev.manufacturer.name, value) !== null);
      } else {
        result = data.filter((dev) => customSearch(dev, value) !== null);
      }
      setData(result);
    } else {
      setData(originalData);
    }
  };

  useEffect(() => {
    setOriginalData(props.data);
  }, []);

  return (
    <Paper component="form" className={classes.root}>
      <SearchTypeComponent
        type={searchType}
        setType={setSearchType}
      />
      <div className={classes.searchButton} aria-label="search">
        <SearchIcon />
      </div>
      <InputBase
        value={text}
        fullWidth
        className={classes.input}
        placeholder="Search"
        onChange={(event) => handleSearchTyping(event)}
        onBlur={(event) => setText(event.target.value.trim())}
      />
      <IconButton
        color="primary"
        className={classes.iconButton}
        aria-label="directions"
        onClick={() => {
          setText('');
          setData(originalData);
        }}
      >
        <ClearIcon />
      </IconButton>
    </Paper>
  );
}

SearchComponent.defaultProps = {
  data: []
};

SearchComponent.propTypes = {
  data: PropTypes.array,
  setData: PropTypes.func.isRequired
};


export default function DeviceView({ socket, props }) {
  const [devices, setDevices] = useState([]);
  const [runSpinningPage, setRunSpinningPage] = useState(false);
  const alert = createAlert(useSnackbar().enqueueSnackbar);

  async function fetchDevices() {
    try {
      const rv = await api.get('/device');
      setDevices(rv.data);
    } catch (error) {
      alert('Error while fetching devices', error);
    }
  }


  useEffect(() => {
    (async () => {
      setRunSpinningPage(true);
      await fetchDevices();
      setRunSpinningPage(false);
    })();
  }, []);


  useEffect(() => {
    if (socket) {
      socket.on('ws_devices', (data) => {
        if (data) setDevices(data);
      });
    }

    // Cleanup.
    return () => { if (socket) socket.off('ws_devices'); };
  }, [socket]);


  return (
    <div style={{flexGrow: 1}}>
      {
        runSpinningPage ? (
          <SpinnerPage />
        ) : (
          <>
            <div id="back-to-top-anchor" />
            <Grid container id="back-to-top-anchor" spacing={2}>
              <Grid item xs={12}>
                <SearchComponent data={devices} setData={setDevices} />
              </Grid>
              <Grid item xs={12}>
                <MaterialTable
                  style={{ borderRadius: '10px' }}
                  icons={tableIcons}
                  title=''
                  data={devices}
                  options={{
                    search: false,
                    sorting: true,
                    paging: false,
                    headerStyle: {
                      borderWidth: '1px',
                      borderColor: 'black',
                      color: '#848484'
                    }
                  }}
                  components={{
                    Toolbar: () => (
                      <div style={{padding: '5px'}}>
                      </div>
                    )
                  }}
                  columns={[
                    {
                      title: 'Device',
                      field: 'device',
                      render: (row) => (
                        <div>
                          <Typography>
                            {row.device}
                          </Typography>
                        </div>
                      )
                    }, {
                      title: 'Model',
                      field: 'device_model',
                      render: (row) => (
                        <div>
                          <Typography>
                            {row.device_model}
                          </Typography>
                        </div>
                      )
                    }, {
                      title: 'Manufacturer',
                      field: 'manufacturer.name',
                      render: (row) => (
                        <div>
                          <Typography>
                            <Link href="#" onClick={() => window.open(row.manufacturer.website, '_blank')}>
                              {row.manufacturer.name}
                            </Link>
                          </Typography>
                        </div>
                      )
                    }
                  ]}
                  onRowClick={(event, row, togglePanel) => togglePanel()}
                  detailPanel={(row) => <DetailDevicePanelData row={row} />}
                />
                <br />
              </Grid>
            </Grid>
            <ScrollTop {...props} />
          </>
        )
      }
    </div>
  );
}

DeviceView.defaultProps = {
  socket: null
};

DeviceView.propTypes = {
  socket: PropTypes.object
};

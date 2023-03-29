import React, { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { DataGrid } from '@mui/x-data-grid';
import Snackbar from '@mui/material/Snackbar';
import Alert from '@mui/material/Alert';
import Button from '@mui/material/Button';
import { UUID } from "bson";   
 

const useUpdateRow = () => {

  return React.useCallback(
    async (row) => {
      console.log("row", row);
      const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ row: row })
      }
      const response = await fetch(`/device/${row._id}`, requestOptions);
      console.log("response", response)
      const data = await response.json();
      console.log("data", data);
     // this.setState({ postId: data.id });
    },
    [],
  );
};


const Devices = () => {
  
  const navigate = useNavigate();
 

  const [rows, setData] = React.useState([]);

  const mutateRow = useUpdateRow();

  const [snackbar, setSnackbar] = React.useState(null);

  const handleCloseSnackbar = () => setSnackbar(null);

  const processRowUpdate = React.useCallback(
    async (newRow) => {
      // Make the HTTP request to save in the backend
      console.log('newrow ', newRow)
      const response = await mutateRow(newRow);
      setSnackbar({ children: 'successfully saved!', severity: 'success' });
      return response;
    },
    [mutateRow],
  );

  const handleProcessRowUpdateError = React.useCallback((error) => {
    console.log("error", error);
    setSnackbar({ children: error.message, severity: 'error' });
  }, []);

  const navigateToEndpoint = (params) => {
    navigate(`/endpoints/${params.row._id}`, { state: {
      mac: params.row._id
    } });
  }

  useEffect(() => {
    fetch("/devices")
      .then((res) => res.json())
      .then((data) => setData(data));
  }, [processRowUpdate]);


  const columns = [
    { field: '_id',
      headerName: 'id',
      width: 330,
      renderCell: (params) => (
      <strong>
        <Button
          variant="contained"
          size="small"
          style={{ marginRight: 16 }}
          tabIndex={params.hasFocus ? 0 : -1}
          onClick={() => navigateToEndpoint(params)}
        >
          Open
        </Button>
        {params.row._id}

      </strong>
    ),},
    { field: 'ip', headerName: 'ip', width: 330},
    { field: 'name', headerName: 'Name', width: 330, editable: true },
    { field: 'mfgr', headerName: 'Manufacturer', width: 330, editable: true },
    { field: 'open_ports', headerName: 'Open Ports', width: 330, editable: true },
    {
      field: 'device_type',
      headerName: 'Device',
      width: 330,
      editable: true,
    }
  ];

  return (
    <div style={{ height: 800, width: '100%' }}>
    <DataGrid
      rows={rows}
      columns={columns}
      experimentalFeatures={{ newEditingApi: true }}
      processRowUpdate={processRowUpdate}
      onProcessRowUpdateError={handleProcessRowUpdateError}
      getRowId={(row) => row  ? row._id + row.name : UUID }
    />
     {!!snackbar && (
        <Snackbar
          open
          anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
          onClose={handleCloseSnackbar}
          autoHideDuration={6000}
        >
          <Alert {...snackbar} onClose={handleCloseSnackbar} />
        </Snackbar>
      )}
  </div>
  );
};
export default Devices;

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


const Domainips = () => {
  
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

  
  useEffect(() => {
    fetch("/domainips")
      .then((res) => res.json())
      .then((data) => setData(data));
  }, [processRowUpdate]);


  const columns = [
    { field: 'domain_name', headerName: 'domain name', width: 330},
    { field: 'ips', headerName: 'ip addresses', width: 330, editable: true },
    { field: 'ip_count', headerName: 'ip count', width: 330, editable: true }
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
export default Domainips;

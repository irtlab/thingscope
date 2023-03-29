import React, { useEffect, useState } from "react";
import { DataGrid } from '@mui/x-data-grid';
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableContainer from "@mui/material/TableContainer";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
import Paper from "@mui/material/Paper";
import { useLocation } from 'react-router-dom';
import { UUID } from "bson"; 

const Endpoints = () => {
 // const mac = "1";
  const {state} = useLocation();
  const {mac} = state
  
  const [rows, setData] = useState([]);

  useEffect(() => {
    fetch(`/endpoints/${mac}`)
      .then((res) => res.json())
      .then((data) => setData(data));
  }, []);

  const columns = [
    { field: '_id',
      headerName: 'id',
      width: 330,
    },
    { field: 'port', headerName: 'Port', width: 330},
    { field: 'protocol', headerName: 'Protocol', width: 330 },
    { field: 'ip', headerName: 'ip', width: 330 },
    {
      field: 'domain_name',
      headerName: 'domain_name',
      width: 330
    },
    {
      field: 'security_posture',
      headerName: 'security_posture',
      width: 330
    },
    {
      field: 'cert_tls_version',
      headerName: 'tls_version',
      width: 330
    },
    {
      field: 'self_signed',
      headerName: 'self_signed',
      width: 330
    },
    {
      field: 'kex_algorithm',
      headerName: 'key_exchange',
      width: 330
    },
    {
      field: 'openssl_name',
      headerName: 'openssl_name',
      width: 330
    },
    {
      field: 'enc_algorithm',
      headerName: 'encryption_algo',
      width: 330
    },
    {
      field: 'auth_algorithm',
      headerName: 'auth_algo',
      width: 330
    },
    {
      field: 'hash_algorithm',
      headerName: 'hashing_algo',
      width: 330
    },
    {
      field: 'cert_details',
      headerName: 'cert_details',
      width: 330,
      valueFormatter: (params) => {
        return params?.value && params.value.join();
      }
    },
    {
      field: 'city',
      headerName: 'city',
      width: 330
    },
    {
      field: 'region',
      headerName: 'region',
      width: 330
    },
    {
      field: 'country',
      headerName: 'country',
      width: 330
    },
    {
      field: 'ip_org',
      headerName: 'ip_org',
      width: 330
    },
    {
      field: 'coordinates',
      headerName: 'coordinates',
      width: 330
    },
    {
      field: 'ip_version',
      headerName: 'ip_version',
      width: 330
    }
  ];

  return (
    <div style={{ height: 800, width: '100%' }}>
    <DataGrid
      rows={rows}
      columns={columns}
      getRowId={(row) => row  ? row._id + row.ip : UUID }
    />
  </div>
  );
  // return (
  //   <TableContainer component={Paper}>
  //     <Table sx={{ minWidth: 650 }} size="small" aria-label="a dense table">
  //       <TableHead>
  //         <TableRow>
  //           <TableCell>_id</TableCell>
  //           <TableCell align="right">port&nbsp;</TableCell>
  //           <TableCell align="right">protocol&nbsp;</TableCell>
  //           <TableCell align="right">ip&nbsp;</TableCell>
  //           <TableCell align="right">security_posture&nbsp;</TableCell>
  //           <TableCell align="right">security_protocol&nbsp;</TableCell>
  //           <TableCell align="right">cert_details&nbsp;</TableCell>
  //           <TableCell align="right">domain_name&nbsp;</TableCell>
  //           <TableCell align="right">city&nbsp;</TableCell>
  //           <TableCell align="right">region&nbsp;</TableCell>
  //           <TableCell align="right">country&nbsp;</TableCell>
  //           {/* <TableCell align="right">device_mac&nbsp;</TableCell>  */}
  //         </TableRow>
  //       </TableHead>
  //       <TableBody>
  //         {rows.map((row) => (
  //           <TableRow
  //             key={row._id.$oid}
  //             sx={{ "&:last-child td, &:last-child th": { border: 0 } }}
  //           >
  //             <TableCell component="th" scope="row">
  //               {row._id.$oid}
  //             </TableCell>
  //             <TableCell align="right">{row.port}</TableCell>
  //             <TableCell align="right">{row.protocol}</TableCell>
  //             <TableCell align="right">{row.ip}</TableCell>
  //             <TableCell align="right">{row.security_posture}</TableCell>
  //             <TableCell align="right">{row?.tls_info?.tls_version && `TLS ${row?.tls_info?.tls_version}` }</TableCell>
  //             <TableCell align="right">{row?.security_details && row.security_details.join()}</TableCell>
  //             <TableCell align="right">{row.domain_name}</TableCell>
  //             <TableCell align="right">{row.location.city}</TableCell>
  //             <TableCell align="right">{row.location.region}</TableCell>
  //             <TableCell align="right">{row.location.country}</TableCell>
  //             {/* <TableCell align="right">{row.device_mac}</TableCell> */}
  //           </TableRow>
  //         ))}
  //       </TableBody>
  //     </Table>
  //   </TableContainer>
  // );
};
export default Endpoints;

import React from "react";
import Stack from "@mui/material/Stack";
import Button from "@mui/material/Button";
import Paper from "@mui/material/Paper";
import { useNavigate } from "react-router-dom";

const Home = () => {
  const navigate = useNavigate();

  const devicesPage = () => {
    navigate("/devices");
  };

  const endpointsPage = () => {
    navigate("/endpoints");
  };
  const domainipsPage = () => {
    navigate("/domainips");
  };
  return (
    <div>
      <Paper elevation={3}>
        <Stack spacing={2} direction="row">
          <Button variant="contained" onClick={() => devicesPage()}>
            Devices
          </Button>
          <Button variant="outlined" onClick={() => endpointsPage()}>
            Analytics
          </Button>
          <Button variant="outlined" onClick={() => domainipsPage()}>
            Domain IP Mapping
          </Button>
        </Stack>
      </Paper>
    </div>
  );
};
export default Home;

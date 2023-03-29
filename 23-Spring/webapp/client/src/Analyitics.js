import React, { useEffect, useState, PureComponent } from "react";
import CssBaseline from '@mui/material/CssBaseline';
import Box from '@mui/material/Box';
import Container from '@mui/material/Container';
import { experimentalStyled as styled } from '@mui/material/styles';
import Paper from '@mui/material/Paper';
import Grid from '@mui/material/Unstable_Grid2';
import Chart from "./Chart";
import { formatData } from "./helpers";


const Item = styled(Paper)(({ theme }) => ({
    backgroundColor: theme.palette.mode === 'dark' ? '#1A2027' : '#fff',
    ...theme.typography.body2,
    padding: theme.spacing(2),
    textAlign: 'center',
    color: theme.palette.text.secondary,
}));
const properties = ["protocol", "ip_org", "cert_tls_version", "enc_algorithm", "country"];
const colors = ['#2f7ed8', '#0d233a', '#8bbc21', '#910000', '#1aadce',
        '#492970', '#f28f43', '#77a1e5', '#c42525', '#a6c96a'];
const Analytics = () => {
    const [data, setData] = useState([]);

    useEffect(() => {
        fetch("/endpoints")
            .then((res) => res.json())
            .then((data) => {
             const formattedData = formatData(data, properties);
             console.log("formattedData", formattedData);
             setData(formattedData);
            });
    }, [])

    class CustomizedLabel extends PureComponent {
        render() {
          const { x, y, stroke, value } = this.props;
      
          return (
            <text x={x} y={y} dy={-4} fill={stroke} fontSize={10} textAnchor="middle">
              {value}
            </text>
          );
        }
      }

    return (
        <React.Fragment>
            
            <CssBaseline />
                <Grid container spacing={{ xs: 2, md: 3 }} columns={{ xs: 4, sm: 8, md: 12 }}>
                    {data.length > 0 && data.map((val, index) => (
                        <Grid xs="auto" key={index}>
                            <Item>
                              { val && 
                              <Chart data={val} color={colors[index]} label={<CustomizedLabel />} >


                              </Chart>  }
                            </Item>
                        </Grid>
                    ))}
                </Grid>
        </React.Fragment>
    );
}

export default Analytics;

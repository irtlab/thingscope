import React from "react";
import { BarChart, Bar, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const data = [
    {
        name: 'TCP',
        uv: 4000,
    },
    {
        name: 'UDP',
        uv: 3000,
    },
];

const Chart = ({data, color}) => {
    return (
        <div style={{width: "1500px", height:"1200px"}} >
            <BarChart
                width={1500}
                height={1200}
                data={data}
                margin={{
                    top: 5,
                    right: 30,
                    left: 20,
                    bottom: 5,
                }}
                layout="vertical" barCategoryGap="20%"
            >
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis type="number"/>
                <YAxis width={440}  dataKey="name" interval={0} type="category"/>
                <Tooltip />
                <Legend name="name"/>
                <Bar dataKey="count" fill={color} barSize={30} />
            </BarChart>
        </div>
    );

}
export default Chart;


# ThingScope Backend API

### Introduction
The backend server of the `ThingScope` project is implemented in TypeScript and based on ExpressJS web fremawork, and as a database it uses MongoDB.

### How to Install?
Before installing the project make sure you already installed minimum requirements: `Node.js (>= 14.0.0)` and
did set up NGINX web server.

Go to `/var/www/` directory and download the source code:
```bash
git clone git@github.com:irtlab/thingscope.git
```

It may ask `sudo` permission. If yes, then do it it with `sudo` and then run the following command to change permission:
```bash
sudo chown -R <username>:<username> thingscope
```

Now, change to the `thingscope/backend` directory and install requirements
```bash
cd thingscope/backend
npm install
```

You must setup environment variables by creating `.env` file in the root directory and providing the following variables:
```bash
MONGODB_URL=<MongoDB URL>
```


**NOTE**  
Currently, the backend running on the AWS Cloud and you would need to download a CA file. Download the RDS CA file
(`rds-combined-ca-bundle.pem`) from the AWS and put in the `/var/www/thingscope/backend` directory. This is needed to connect Amazon DocumentDB (MongoDB).


### How to Run API?
If installation went well, you can run the project in development mode or in production mode (recommended to use
[PM2](https://pm2.keymetrics.io/)).

Run development mode:
```
npm run api_dev
```

Before running the production mode make sure you build the source code by running `npm run build` command.

Run production mode:
```
npm run build
pm2 start npm --name "thingscope-api" -- run api_start
```

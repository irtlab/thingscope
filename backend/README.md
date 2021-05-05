# ThingScope

### Introduction
The backend server of the ThingScope project. Implemented in TypeScript and based on ExpressJS web fremawork.  
The project is designed to run on AWS Cloud and it uses Amazon DocumentDB as a database.

### How to Install?
Go to `/var/www/` directory run the following command:
```bash
git clone https://github.com/baloian/thingscope-backend.git
```

It may ask `sudo` permission. If yes, then do it it with `sudo` and then run the following command to change permission:
```bash
sudo chown -R <username>:<username> thingscope-backend
```

Now, change to the `thingscope-backend` directory and install requirements
```bash
cd thingscope-backend
npm install
```

Download RDS CA file (`rds-combined-ca-bundle.pem`) from the AWS and put in the `/var/www/thingscope-backend` directory.
This is needed to connect Amazon DocumentDB.

### How to Run API?
If installation went well, you can run the project in development mode or in production mode (recommended to use
[PM2](https://pm2.keymetrics.io/)).

Run development mode:
```
npm run api_dev
```

Before running the production mode make sure you buld the source code by running `npm run build` command.

Run production mode:
```
npm run build
pm2 start npm --name "thingscope-backend-api" -- run api_start
```

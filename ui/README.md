# ThingScope User Interface (UI)

The user interface of the `ThingScope` project is based on [React](https://reactjs.org/) and [Material-UI](https://material-ui.com/).

### How to Develope?

Download the source code, install requirements by running the following commands:
```bash
git clone git@github.com:irtlab/thingscope.git
cd cd thingscope/ui/
npm install
```

and then in the project directory, you can run:
```bash
npm start
```

Runs the app in the development mode. Open [http://localhost:3000](http://localhost:3000) to view it in the browser. The page will reload if you make edits.
You will also see any lint errors in the console.


### How to Build Production?

Download the source code:
```bash
git clone git@github.com:irtlab/thingscope.git
cd cd thingscope/ui/
```

Make the `install_thingscope_ui.sh` executable by running the following command:
```bash
chmod a+x install_thingscope_ui.sh 
```

and the run the script
```
./install_thingscope_ui.sh 
```
**NOTE:** the script assumes that the backend code is in the `/var/www/thingscope/backend` directory.

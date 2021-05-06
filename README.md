# ThingScope
**ThingScope** is a set of tools that complement each other to analyze home network for informing consumers about the privacy-related behavior of home
internet of things (IoT) devices, such as security cameras, thermostats, smart TV and smart
speakers, both pre-purchase and when the device is installed in their home.

### Directory Structure
```
├── agent              : Network monitoring agent.
├── backend            : Back-end server and MongoDB database.
├── ui                 : Front-end (web interface).
├── browser-extension  : Google Chrome browser extension.
├── LICENSE
├── README
├── .gitignore
```

### Build & Run
Every component must be build and run separately.

To build and run the agent, see: [agent/README.md](https://github.com/irtlab/thingscope/tree/master/agent#readme).<br/>
To build and run the backend server, see: [backend/README.md](https://github.com/irtlab/thingscope/tree/master/backend#readme)<br/>
To build and run the ui (web interface), see: [ui/README.md](https://github.com/irtlab/thingscope/tree/master/ui#readme)<br/>
To build and run the browser extension, see: [browser-extension/README.md](https://github.com/irtlab/thingscope/tree/master/browser-extension#readme)<br/>

### Contributions
Contributions are welcome and can be made by submitting GitHub pull requests
to this repository.  
In general, the `ThingScope` Javascript/TypeScript source code follows [Airbnb JavaScript Style Guide](https://github.com/airbnb/javascript), and the Python code follows [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html).


### License
This source code is available to everyone under the standard
[MIT LICENSE](https://github.com/irtlab/thingscope/blob/master/LICENSE).

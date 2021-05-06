# ThingScope Agent
The Agent is the main part of the project which scans home network.

### How to Build & Run?
Create a Python virtual environment, activate it, `git clone` the project and install requirements.
```sh
python3 -m venv agent
source agent/bin/activate
cd agent
git clone git@github.com:irtlab/thingscope.git
pip3 install -r thingscope/agent/requirements.txt
```

To start the Agent justg run the `sniffer_no_db.py` script
```bash
python3 sniffer_no_db.py
```

### How to Communicate with Cloud Server?
Please read [Communication Between ThingScope Agent & Cloud Server](https://docs.google.com/document/d/1TThC9Q1P5zryRwRAtvh7wKxE5ofZnwi6K96TXp9HAlI/edit?usp=sharing)
document and check out the [api_example.py](https://github.com/irtlab/thingscope/blob/master/agent/api_example.py) file.

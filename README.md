# amoba
Simple remotely playable gomoku board

The `amoba_server.ipynb` is a simple notebook that is listening on a port for stepping suggestions from players, performs the step and checkes if someone won. The state of the game is encoded in an integer `numpy` array. 
The motor behind all this is a simple gomoku board class found in `amoba.py`. 
A simple client script is also provided in `amoba_client.py` that plays a brainless random game. 

Visualization relies on [bqplot](https://github.com/bloomberg/bqplot). 

# mebot

An AIML and semantic network based chatbot with a react based web client which also uses Machine Learning to dynamically learn Node types at neo4j graph creation time.

Demo Video Link: https://drive.google.com/file/d/1W_qBV-xfT3rM-itHCTV4vHNmB-aCIGLX/view

## How to run?

**Backend**

To run the backend server, perform these operations: 

  - Create a virtualenv and activate it.
  - Install all the packages in requirements.txt with pip
  - run `python -m spacy download en_core_web_sm`
  - Export these variables (UNIX).
    - `export MEBOT_ENV="PROD"` (you can choose PROD or DEV)
    - `export FLASK_APP=server.py` (for flask)

  - Make sure a valid neo4j instance is running
  - Configure its credentials in the graph.py file
  - Configure its credentials in the client/src/components/Graph.jsx file
  - Finally, run the server with `flask run`

  
**Frontend**

Make sure you have `node` (the latest version) installed
To run the frontend server, perform these operations: 

  - `cd client`
  - `npm install`
  - `npm start`

That's it!


# Credits

This was a group collaboration between:

  - Haider Ali Khichi (SP17-BCS-038)
  - Muhammad Hassan Mustafa (SP17-BCS-065)
  - Muhammad Rafay Khalid (SP17-BCS-044)

of B section from COMSATS Lahore, Pakistan

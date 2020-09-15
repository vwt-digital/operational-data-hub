# ODH Architecture diagrams

This function is created to generate architecture diagrams for the Operational Data Hub documentation. The generation
of these diagrams is done by the [Diagrams as code](https://diagrams.mingrammer.com/) package.

## Usage
To use this function, follow the following steps:
1.  Create a virtual environment and install all required packages
    ~~~
    virtualenv -p python3 venv
    source venv/bin/activate
    pip3 install -r requirements.txt
    ~~~
2.  Generate the diagrams
    ~~~
    python3 diagram.py
    ~~~

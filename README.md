# Network Enablement API demo

This demo shows how to use and integrate the Network Enablement API along with the [Number Verification API](https://developer.vonage.com/en/number-verification/overview).

## Prerequisites

* A [Vonage developer account](https://developer.vonage.com/)
* Node.js and npm
* Python (>= 3.10)

## Setting up the Environment

Clone the repository, go to the `server` folder and copy the `.env.example` file to `.env`. Edit the new `.env` and change the environment variables:

```
JWT = your_jwt_token

REDIRECT_URI=https://your-server.com/callback
```

Tips:

* Use the Virtual CSP: Create a new application with the Network Registry capability enabled, and select "Sandbox" as access type. Use the fake phone number `+99012345678` when running the client.
* You can generate a new JWT using the [Vonage JWT Generator tool](https://developer.vonage.com/en/jwt).

## Run the Server 

Install the dependencies:

```bash
cd server
npm install
```

Run the application:

```bash
node server.js
```

## Run the Client 

Open a new terminal and go to the `client` folder. We'll install the Python dependencies using a virtual environment:

```bash
cd client
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run the client:

```bash
python client.py +99012345678
```


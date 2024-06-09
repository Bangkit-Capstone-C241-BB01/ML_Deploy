# ML - Flask for Deployment

## Prerequisites

Before running the application, ensure you have the following installed on your machine:

- Docker
- Python 3.x
- Pip

## Setup Instructions

### 1. Clone the repository

## Enable with Docker
To enable it with docker, you can enable it with

```bash
git clone https://github.com/Bangkit-Capstone-C241-BB01/ML_Deploy.git
cd ML_Deploy
```

or if you're using mac
```bash
git clone git@github.com:Bangkit-Capstone-C241-BB01/ML_Deploy.git
cd ML_Deploy
```

### 2. Set up the environment

Create a file with name ".env"
Ensure you have a .env file with the following content:
Replace the `<SECRET_KEY>` with anything you want. Make sure you remember it, and make it unique!

```
SECRET_KEY=<SECRET_KEY>
```


### 3. Install dependencies

Create a virtual environment and install the dependencies listed in requirements.txt.

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 4. Run the application
#### Running with Flask

Replace the `<SECRET_KEY>` with the one that you have set it up in your .env

```bash
export FLASK_APP=app.py
export SECRET_KEY=<SECRET_KEY>  
flask run --host=0.0.0.0 --port=5000
```

#### Running with Docker
Build the Docker image:
```bash
docker build -t flask_ml .
```
Replace [any port] with other port other than 5000
Note: Secret Key is being set through the .env

Run the Docker container:
```bash
docker run -p [any port]:5000 -e SECRET_KEY=SECRET_KEY flask_ml
```

Afterward, this can be accessed in your local http://127.0.0.1:[any port]

## API Endpoints

### 1. Index

**URL:** `/`

**Method:** `GET`

**Headers:**
- Authorization: Bearer `<SECRET_KEY>`

**Response:**

```json
{
  "status": {
    "code": 200,
    "message": "Success fetching the API"
  },
  "data": null
}
```

### 2. Prediction

**URL:** `/prediction`

**Method:** `POST`

**Headers:**
- Authorization: Bearer `<SECRET_KEY>`

**Body:**
- Form-data or JSON:
  - image: Image file (optional if using image_url)
  - image_url: URL of the image (optional if using image file)

**Response:**

```json
{
  "status": {
    "code": 200,
    "message": "Success fetching the API"
  },
  "data": {
    "predicted_class": "Blur/Bokeh/Normal",
    "confidence_scores": {
      "Blur": 0.5,
      "Bokeh": 0.3,
      "Normal": 0.2,
    },
    "accepted": true/false
  }
}
```

### Error Responses

**400 Bad Request**

```json
{
  "status": {
    "code": 400,
    "message": "Client side error: ..."
  },
  "data": null
}
```

**401 Bad Request**

```json
{
  "status": {
    "code": 401,
    "message": "Unauthorized Access!"
  },
  "data": null
}
```

**404 Not Found**

```json
{
  "status": {
    "code": 404,
    "message": "URL not found!"
  },
  "data": null
}

```

**405 Method Not Allowed**

```json
{
  "status": {
    "code": 405,
    "message": "Request method not allowed!"
  },
  "data": null
}

```

**429 Rate Limit Exceeded**

```json
{
  "status": {
    "code": 429,
    "message": "Rate limit exceeded. Please try again later."
  },
  "data": null
}

```

**500 Internal Server Error**

```json
{
  "status": {
    "code": 500,
    "message": "Server error!"
  },
  "data": null
}

```



## Testing with Postman

### 1. Setup Authorization

- Open Postman and create a new request.
- Go to the "Authorization" tab.
- Select "Bearer Token" as the type.
- Enter the `<SECRET_KEY>` as the token.

### 2. Test Prediction Endpoint

#### Using JSON

- Set the request type to `POST`.
- Set the URL to `http://127.0.0.1:[any port you defined]/prediction`.
- Go to the "Body" tab and select "raw" and "JSON".
- Enter the following JSON:

```json
{
  "image_url": "http://example.com/image.jpg"
}
```

#### Using Form-data (Unused)

- Set the request type to `POST`.
- Set the URL to `http://127.0.0.1:[any port you defined]/prediction`.
- Go to the "Body" tab and select "form-data".
- Add a key `image` and select a file to upload.
- Click "Send".
- You should receive a `200 OK` response with prediction data.
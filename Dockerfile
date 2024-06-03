FROM python:3.9

# Install dependencies
RUN apt-get update && apt-get install -y \
    pkg-config \
    libhdf5-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED True
ENV APP_HOME /app
WORKDIR $APP_HOME

# Copy application code
COPY . ./

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install setuptools==59.6.0 Cython==0.29.16
RUN pip install --no-binary=h5py h5py==2.10.0
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port
EXPOSE 5000

# Set the Flask app environment variable
ENV FLASK_APP=app.py

# Run the application
CMD ["python", "app.py"]

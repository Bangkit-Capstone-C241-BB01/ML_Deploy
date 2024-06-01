FROM python:3.9

# Install pkg-config
RUN apt-get update && apt-get install -y pkg-config

ENV PYTHONUNBUFFERED True
# ENV APP_HOME /app
ENV PORT 5001

# WORKDIR $APP_HOME

COPY . ./

RUN apt install -y libhdf5-dev
RUN pip install setuptools==59.6.0
RUN pip install Cython==0.29.16
RUN pip install --no-binary=h5py h5py==2.10.0

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5001
ENV FLASK_APP=app.py

CMD flask run -h 0.0.0.0 -p 5001
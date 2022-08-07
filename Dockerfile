FROM python:3.7.3-stretch

# Working Directory
WORKDIR /live_travel_advisor

# Copy source code to working directory
COPY . app.py /live_travel_advisor/

# Install packages from requirements.txt
# hadolint ignore=DL3013
RUN apt-get -y update

RUN apt-get install -y libsndfile1

RUN pip install --upgrade pip &&\
    pip install --trusted-host pypi.python.org -r requirements.txt


# Expose port 8080
EXPOSE 8080

# Run app.py at container launch
CMD ["python", "app.py"]

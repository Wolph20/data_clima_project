# Pull python 3 image
FROM python:3-alpine
# Create a work dir
WORKDIR /app
# Copy requirements.txt into workdir created above
COPY ./requirements.txt .
# Install all requirements
RUN pip install -r requirements.txt

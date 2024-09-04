FROM python:3.10-slim-buster

WORKDIR /AHB

COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

# Expose the port that the application will run on
EXPOSE 8080

# Command to run the application
CMD ["python3", "run.py"]

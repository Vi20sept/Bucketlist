# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed dependencies specified in requirements.txt
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \	
    unixodbc-dev \
    && rm -rf /var/lib/apt/lists/*




# Install Microsoft ODBC Driver for SQL Server

RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -

RUN curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list



RUN apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql17




# Install additional dependencies if needed
# RUN apt-get install -y <additional-package>

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 8070


# Define environment variable
ENV SQL_SERVER_HOST python-web-app1-server.database.windows.net
ENV SQL_SERVER_USER python-web-app1-server-admin
ENV SQL_SERVER_PASSWORD S65TWW48QC147WR4$
ENV SQL_SERVER_DATABASE BucketList

# Run app.py when the container launches
CMD ["python", "app.py"]




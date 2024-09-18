# Base image with Python and Jupyter
FROM python:3.8-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    sudo \
    curl \
    bash \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Jupyter
RUN pip install --no-cache-dir jupyter

# Install Apache Beam
RUN pip install apache-beam[gcp]
RUN pip install pandas

# Create a user with no password
ARG username=jovyan
ARG password=jovyan
RUN useradd -ms /bin/bash $username && echo "$username:$password" | chpasswd && adduser $username sudo

# Set work directory and permissions
WORKDIR /home/$username

# Grant permissions to user jovyan
RUN chown -R $username:$username /home/$username

# Set user to jovyan from now on
USER $username

# Expose Jupyter Notebook port
EXPOSE 8888

# Start Jupyter
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root", "--NotebookApp.token=''", "--NotebookApp.password=''"]

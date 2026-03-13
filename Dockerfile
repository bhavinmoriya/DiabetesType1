# Use a lightweight Python base image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Install uv for dependency management
RUN pip install uv

# Copy only the necessary files for dependency installation
COPY pyproject.toml uv.lock ./

# Install dependencies using uv
RUN uv sync
# RUN uv pip install --system

# Copy the rest of the application
COPY . .

# Expose the Streamlit port
EXPOSE 8501

# Run the Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]

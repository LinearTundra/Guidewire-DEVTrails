# -------- Base Image --------
FROM python:3.10-slim

# -------- Set Working Directory --------
WORKDIR /app

# -------- Copy Files --------
COPY . /app

# -------- Install Dependencies --------
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# -------- Expose Port --------
EXPOSE 10000

# -------- Start Server --------
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "10000"]
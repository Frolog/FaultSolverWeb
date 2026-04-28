FROM python:3.11-slim
WORKDIR /app

# העתקת ה-wheels
COPY ./wheels /wheels
COPY requirements.txt .

# התקנה אופליין
RUN pip install --no-cache-dir --no-index --find-links=/wheels -r requirements.txt

COPY . .
EXPOSE 5000
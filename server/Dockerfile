FROM python:3.11

LABEL authors="Jianlong.Lei"

WORKDIR ./src

COPY . .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

RUN pip install "uvicorn[standard]"
RUN pip install pydantic[email]

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
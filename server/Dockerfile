FROM python:3.11

LABEL authors="Jianlong.Lei"

WORKDIR .

COPY ../requirements.txt ./requirements.txt

RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

RUN pip install "uvicorn[standard]"

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
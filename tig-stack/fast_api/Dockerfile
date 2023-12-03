FROM python:3.9
WORKDIR .
COPY ./requirenments.txt /fast_api/requirenments.txt
RUN pip install --no-cache-dir --upgrade -r /fast_api/requirenments.txt
COPY main.py /fast_api/
CMD ["uvicorn", "fast_api.main:app", "--host", "0.0.0.0", "--port", "5000"]

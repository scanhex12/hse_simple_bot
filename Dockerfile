FROM python:3.9-alpine
WORKDIR /bot
ADD . .
RUN pip3 install -r requirements.txt
CMD ["python3", "bot.py"]
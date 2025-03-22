FROM python as base
WORKDIR /usr/src/app
COPY src/ ./
RUN pip install --no-cache-dir -r requirements.txt

FROM python
COPY --from=base /usr/src/app /usr/src/app
WORKDIR /usr/src/app

CMD [ "python", "app.py" ]
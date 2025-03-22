FROM python as base
WORKDIR /usr/src/app
COPY src/ ./
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install gunicorn flask

FROM python
COPY --from=base /usr /usr
WORKDIR /usr/src/app
ENV FLASK_APP=app.py
CMD [ "/usr/src/app/fotbal/bin/gunicorn", "--workers=4", "--bind=0.0.0.0:8080", "-m 007", "wsgi" ]
FROM python as base
WORKDIR /usr/src/app
COPY src/ ./
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install gunicorn flask pipenv \
    && pipenv fotbal \
    && . fotbal/bin/activate

FROM python
COPY --from=base /usr /usr
WORKDIR /usr/src/app
ENV FLASK_APP=app.py
ENV PATH="PATH=/usr/src/app/fotbal/bin"
RUN virtualenv fotbal \
    && . fotbal/bin/activate 
CMD [ "/usr/src/app/fotbal/bin/gunicorn", "--workers=4", "--bind=0.0.0.0:8080", "-m 007", "wsgi" ]
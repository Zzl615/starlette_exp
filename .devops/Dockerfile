FROM python:3.11.2-slim as builder-image

ENV TZ=Asia/Shanghai

# RUN export LANG=zh_CN.UTF-8 \
#     && echo "" >> /etc/apt/sources.list

COPY requirements.txt /requirements.txt

RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --upgrade pip setuptools  && \
    pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r /requirements.txt && \
    rm -rf /var/cache/debconf/*  /var/lib/apt/lists/*  /var/log/*  /tmp/*  ~/.cache

FROM python:3.11.2-slim

COPY --from=builder-image /usr/local/bin /usr/local/bin
COPY --from=builder-image /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

ADD . /app
RUN groupadd -g 2022 -r app \
    && useradd -m -u 2022 -r -g app app \
    && mkdir -p /logs \
    && chown -R app:app /logs /app

RUN apt-get -y autoremove

USER app



WORKDIR /app
ENV PYTHONPATH=/app

CMD ["uvicorn", "--factory", "main:create_app", "--host", "0.0.0.0", "--port", "8080"]
# CMD ["python", "main.py"]
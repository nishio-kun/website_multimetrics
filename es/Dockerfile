FROM docker.elastic.co/elasticsearch/elasticsearch:6.3.2

RUN elasticsearch-plugin install analysis-kuromoji && \
    elasticsearch-plugin install analysis-icu && \
    elasticsearch-plugin install org.codelibs:elasticsearch-analysis-kuromoji-neologd:6.3.1 -b && \
    elasticsearch-plugin remove ingest-geoip

ADD config/jvm.options /usr/share/elasticsearch/config/

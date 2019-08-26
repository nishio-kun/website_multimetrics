FROM elasticsearch:5.1

RUN elasticsearch-plugin  install --batch x-pack && \
    elasticsearch-plugin  install analysis-kuromoji && \
    elasticsearch-plugin install org.codelibs:elasticsearch-analysis-kuromoji-neologd:5.1.0

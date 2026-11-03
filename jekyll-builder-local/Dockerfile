FROM ruby:3.2.2-alpine

ENV PLANTUML_VERSION=1.2023.6
ENV LANG=en_US.UTF-8
ENV BUNDLE_FORCE_RUBY_PLATFORM=1

WORKDIR /srv/jekyll
COPY Gemfile .

# construct a Jekyll builder that comes pre-installed with plantuml runnable as a binary
RUN \
  apk add --no-cache graphviz wget ca-certificates ttf-dejavu fontconfig build-base openjdk11 && \
  wget "http://downloads.sourceforge.net/project/plantuml/${PLANTUML_VERSION}/plantuml.${PLANTUML_VERSION}.jar" -O /usr/bin/plantuml.jar

EXPOSE 8444/tcp

#gem update --system 3.4.13 \

COPY plantuml /usr/bin

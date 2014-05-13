#!/usr/bin/env python

import os
import shutil
import subprocess
from urlparse import urlparse

from bs4 import BeautifulSoup
from django.template import Context
from django.template.loader import get_template
from django.conf import settings
from pyatom import AtomFeed
import yaml


BASE_PATH = os.path.dirname(__file__)
BUILD_PATH = os.path.join(BASE_PATH, '_build')
ARTICLES_PATH = os.path.join(BASE_PATH, 'articles')

settings.configure(
    TEMPLATE_DIRS=[os.path.join(BASE_PATH, 'templates')],
)


class Article(object):
    def __init__(self, slug):
        self.slug = slug
        self.path = os.path.join(ARTICLES_PATH, self.slug)
        self.markdown_path = os.path.join(self.path, 'article.markdown')
        self.read_markdown()

        self.meta = self.get_metadata()

    def read_markdown(self):
        raw_html = subprocess.check_output(['markdown', self.markdown_path])
        soup = BeautifulSoup(raw_html)
        title_element = soup.select('h1')[0]
        self.title = title_element.text
        title_element.decompose()
        self.html = unicode(soup)

        for attribute in ['src', 'href']:
            for element in soup.select('[{0}]'.format(attribute)):
                url = urlparse(element[attribute])

                if url.netloc or url.path.startswith('/'):
                    continue

                element[attribute] = '/'.join([self.slug, url.path])

        self.index_html = unicode(soup)

    def get_metadata(self):
        with open(os.path.join(self.path, 'meta.yaml')) as yaml_file:
            return yaml.load(yaml_file)

    def render(self):
        context = Context({'article': self})
        return get_template('article.html').render(context)

    def bounce(self):
        build_directory = os.path.join(BUILD_PATH, self.slug)
        shutil.copytree(self.path, build_directory)
        html_path = os.path.join(build_directory, 'index.html')

        rendered = self.render()

        with open(html_path, 'w') as html_file:
            html_file.write(rendered.encode('utf-8'))


def render_index(articles):
    context = Context({'articles': articles})
    return get_template('index.html').render(context)


def render_feed(articles):
    feed = AtomFeed(
        title='words from a colons',
        feed_url='https://colons.co/words/feed.xml',
        url='https://colons.co/words/',
        author='Iain Dawson',
    )

    for article in articles:
        feed.add(
            title=article.title,
            content=article.index_html,
            content_type='text/html',
            author='Iain Dawson',
            url='https://colons.co/words/{0.slug}/'.format(article),
            updated=article.meta['date'],
        )

    return feed.to_string()


def build():
    if os.path.isdir(BUILD_PATH):
        shutil.rmtree(BUILD_PATH)

    os.mkdir(BUILD_PATH)

    articles = []

    for slug in os.listdir(ARTICLES_PATH):
        article = Article(slug)
        article.bounce()
        articles.append(article)

    articles.sort(key=lambda a: a.meta['date'], reverse=True)

    with open(os.path.join(BUILD_PATH, 'index.html'), 'w') as index_file:
        index_file.write(render_index(articles).encode('utf-8'))

    with open(os.path.join(BUILD_PATH, 'feed.xml'), 'w') as feed_file:
        feed_file.write(render_feed(articles).encode('utf-8'))


if __name__ == "__main__":
    build()

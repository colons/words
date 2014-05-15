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

DOMAIN = 'https://colons.co'
ROOT = '/words/'
FEED_FILENAME = 'feed.xml'
FEED_URL = ROOT + FEED_FILENAME

settings.configure(
    TEMPLATE_DIRS=[os.path.join(BASE_PATH, 'templates')],
    DATE_FORMAT='M jS, Y',
    USE_TZ=True,
    TIME_ZONE='Europe/London',
)


class Article(object):
    def __init__(self, slug):
        self.slug = slug
        self.absolute_url = ROOT + self.slug
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

        for attribute in ['src', 'href']:
            for element in soup.select('[{0}]'.format(attribute)):
                url = urlparse(element[attribute])

                if not (url.netloc or url.path.startswith('/')):
                    element[attribute] = '/'.join([self.absolute_url, url.path])

        self.html = unicode(soup)

    def get_metadata(self):
        with open(os.path.join(self.path, 'meta.yaml')) as yaml_file:
            return yaml.load(yaml_file)

    def render(self):
        context = Context({'globals': globals(), 'article': self})
        return get_template('article.html').render(context)

    def bounce(self):
        build_directory = os.path.join(BUILD_PATH, self.slug)
        shutil.copytree(self.path, build_directory)
        html_path = os.path.join(build_directory, 'index.html')

        rendered = self.render()

        with open(html_path, 'w') as html_file:
            html_file.write(rendered.encode('utf-8'))


def render_index(articles):
    context = Context({'globals': globals(), 'articles': articles})
    return get_template('index.html').render(context)


def render_feed(articles):
    feed = AtomFeed(
        title='words from a colons',
        feed_url=DOMAIN + FEED_URL,
        url=DOMAIN + ROOT,
        author='Iain Dawson',
    )

    feed_item_template = get_template('feed_item.html')

    for article in articles:
        context = Context({'article': article})

        feed.add(
            title=article.title,
            content=feed_item_template.render(context),
            content_type='html',
            author='Iain Dawson',
            url=DOMAIN + article.absolute_url,
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

    with open(os.path.join(BUILD_PATH, FEED_FILENAME), 'w') as feed_file:
        feed_file.write(render_feed(articles).encode('utf-8'))


if __name__ == "__main__":
    build()

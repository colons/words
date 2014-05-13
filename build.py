#!/usr/bin/env python

import os
import shutil
import subprocess

from django.template import Context
from django.template.loader import get_template
from django.conf import settings
from bs4 import BeautifulSoup


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

    def get_html(self):
        return subprocess.check_output(['markdown', self.markdown_path])

    def get_title(self):
        return BeautifulSoup(self.get_html()).select('h1')[0].text

    def get_context(self):
        return {
            'content': self.get_html(),
            'title': self.get_title(),
        }

    def render(self):
        context = Context(self.get_context())

        return get_template('article.html').render(context)

    def bounce(self):
        build_directory = os.path.join(BUILD_PATH, self.slug)
        shutil.copytree(self.path, build_directory)
        html_path = os.path.join(build_directory, 'index.html')

        rendered = self.render()

        with open(html_path, 'w') as html_file:
            html_file.write(rendered.encode('utf-8'))


def build():
    if os.path.isdir(BUILD_PATH):
        shutil.rmtree(BUILD_PATH)

    os.mkdir(BUILD_PATH)

    for slug in os.listdir(ARTICLES_PATH):
        article = Article(slug)
        article.bounce()


if __name__ == "__main__":
    build()

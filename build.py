#!/usr/bin/env python

import hashlib
import os
import shutil
import subprocess
from urllib.parse import urlparse

from bs4 import BeautifulSoup
import django
from django.conf import settings
from django.template.loader import get_template
from feedgen.feed import FeedGenerator
import yaml


BASE_PATH = os.path.dirname(__file__)
BUILD_PATH = os.path.join(BASE_PATH, '_build')
ARTICLES_PATH = os.path.join(BASE_PATH, 'articles')

DOMAIN = 'https://colons.co'
TWITTER_SCREEN_NAME = 'mftb'
AUTHOR = 'colons'
ROOT = '/words/'
FEED_FILENAME = 'feed.xml'
FEED_URL = ROOT + FEED_FILENAME

FILE_HASHES = {}

settings.configure(
    TEMPLATES=[{
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_PATH, 'templates')],
        'APP_DIRS': False,
    }],
    DATE_FORMAT='M jS, Y',
    USE_TZ=True,
    TIME_ZONE='Europe/London',
)

django.setup()


class Article(object):
    def __init__(self, slug):
        self.slug = slug
        self.absolute_url = ROOT + self.slug
        self.path = os.path.join(ARTICLES_PATH, self.slug)
        self.markdown_path = os.path.join(self.path, 'article.markdown')
        self.read_markdown()

        self.meta = self.get_metadata()

    def __str__(self):
        return '{title} ({slug})'.format(**self.__dict__)

    def fix_internal_links(self, soup):
        for attribute in ['src', 'href']:
            for element in soup.select('[{0}]'.format(attribute)):
                url = urlparse(element[attribute])

                if not (url.netloc or url.path.startswith('/')):
                    element[attribute] = '/'.join([self.absolute_url,
                                                   url.path])

    def make_external_links_target_blank(self, soup):
        for link in soup.select('a[href]'):
            url = urlparse(link['href'])
            if url.netloc:
                link['target'] = '_blank'

    def annotate_image_only_paragraphs(self, soup):
        """
        Add a 'figure' class to <p>s that contain no text and an <img>.
        """

        for paragraph in soup.select('p'):
            if (
                not paragraph.text and
                'img' in [e.name for e in paragraph.select('*')]
            ):
                paragraph.attrs['class'] = 'figure'

    def find_featured_image(self, soup):
        featured_substring = ' (featured)'
        self.featured_image = None

        for image in soup.select('img[alt]'):
            if image['alt'].endswith(featured_substring):
                image['alt'] = image['alt'][0:-len(featured_substring)]

                if self.featured_image is None:
                    self.featured_image = image['src']
                else:
                    raise ValueError("{} has more than one featured image"
                                     .format(self))

    def read_markdown(self):
        raw_html = subprocess.check_output(['markdown', self.markdown_path])
        soup = BeautifulSoup(raw_html, features='lxml')
        title_element = soup.select('h1')[0]
        self.title = title_element.text
        title_element.decompose()

        self.find_featured_image(soup)
        self.fix_internal_links(soup)
        self.make_external_links_target_blank(soup)
        self.annotate_image_only_paragraphs(soup)

        self.html = str(soup)

    def get_metadata(self):
        with open(os.path.join(self.path, 'meta.yaml')) as yaml_file:
            return yaml.safe_load(yaml_file)

    def render(self):
        context = {'globals': globals(), 'article': self}
        return get_template('article.html').render(context)

    def bounce(self):
        build_directory = os.path.join(BUILD_PATH, self.slug)
        shutil.copytree(self.path, build_directory)
        html_path = os.path.join(build_directory, 'index.html')

        rendered = self.render()

        with open(html_path, 'w') as html_file:
            html_file.write(rendered)

    def history_url(self):
        return (
            'https://github.com/colons/words/commits/master/articles/'
            '{slug}/article.markdown'.format(slug=self.slug)
        )

    def get_absolute_url(self):
        return '{}{}{}/'.format(DOMAIN, ROOT, self.slug)

    def get_summary(self):
        return [p.text for p in BeautifulSoup(self.html, features='lxml')
                .select('p') if p.text][0]


def render_index(articles):
    context = {
        'is_index': True,
        'globals': globals(),
        'articles': articles,
    }
    return get_template('index.html').render(context)


class EntryBaseExtension:
    def extend_atom(self, entry):
        entry.set('base', DOMAIN + FEED_URL)


def render_feed(articles):
    feed = FeedGenerator()
    feed.id(DOMAIN + FEED_URL)
    feed.title('words from a colons')
    feed.author({'name': AUTHOR})
    feed.link(href=DOMAIN + ROOT)
    feed.link(href=(DOMAIN + FEED_URL), rel='self')

    feed_item_template = get_template('feed_item.html')

    for article in articles:
        context = {'article': article}

        entry = feed.add_entry(order='append')
        url = DOMAIN + article.absolute_url
        entry.id(url)
        entry.link(href=url)
        entry.title(article.title)
        entry.author({'name': AUTHOR})
        entry.updated(article.meta['date'])
        entry.content(feed_item_template.render(context), type='html')
        entry.register_extension('entry_base', EntryBaseExtension,
                                 atom=True, rss=False)

    return feed.atom_str(pretty=True)


def build():
    if os.path.isdir(BUILD_PATH):
        shutil.rmtree(BUILD_PATH)

    os.mkdir(BUILD_PATH)

    with open(os.path.join(BUILD_PATH, 'style.css'), 'bw') as css_file:
        css = subprocess.check_output(['lessc', 'style.less'])
        FILE_HASHES['css'] = hashlib.sha256(css).hexdigest()[:16]
        css_file.write(css)

    articles = []

    for slug in [d for d in os.listdir(ARTICLES_PATH)
                 if not d.startswith('.')]:
        article = Article(slug)
        article.bounce()
        articles.append(article)

    articles.sort(key=lambda a: a.meta['date'], reverse=True)

    with open(os.path.join(BUILD_PATH, 'index.html'), 'w') as index_file:
        index_file.write(render_index(articles))

    with open(os.path.join(BUILD_PATH, FEED_FILENAME), 'wb') as feed_file:
        feed_file.write(render_feed(articles))


if __name__ == "__main__":
    build()

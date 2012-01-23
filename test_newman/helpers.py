# -*- coding: utf-8 -*-
from datetime import datetime
from django.test import TestCase
from django.contrib.sites.models import Site
from django.contrib.auth.models import User

from ella.core.models import Author, Category, Publishable

from django.conf import settings

# choose Article as an example publishable
from ella.articles.models import Article


class NewmanTestCase(TestCase):

    def setUp(self):
        super(NewmanTestCase, self).setUp()

        self.site = Site.objects.get(name='example.com')
        self.site_second = Site.objects.create(domain='test.net', name='test.net')

        self.user = User.objects.create(
            username='newman',
            first_name='Paul',
            last_name='Newman',
            email='',
            is_active=True,
            is_staff=True,
            is_superuser=False
        )

        self.author = Author.objects.create(name='igorko', slug='igorko')

        self.create_categories()

    def create_categories(self):
        site = self.site
        # Categories on site 1
        self.category_top_level = Category.objects.create(slug='a0-top', title='a0 top', description='A top category', site=site)
        self.nested_first_level = Category.objects.create(
            tree_parent=self.category_top_level,
            slug='a1-first-nested-level',
            title='a1 first nested level',
            description='nested',
            site=site
        )
        self.nested_first_level_two = Category.objects.create(
            tree_parent=self.category_top_level,
            slug='a2-first-nested-level',
            title='a2 first nested level',
            description='nested',
            site=site
        )
        self.nested_second_level = Category.objects.create(
            tree_parent=self.nested_first_level,
            slug='a4-second-nested-level',
            title='a4 second nested level',
            description='nested',
            site=site
        )
        self.nested_second_level_two = Category.objects.create(
            tree_parent=self.nested_first_level_two,
            slug='a5-second-nested-level',
            title='a5 second nested level',
            description='nested',
            site=site
        )

        # Categories on site 2
        self.category_top_level_b = Category.objects.create(slug='a0-top', title='a0 top', description='A top category', site=self.site_second)
        self.nested_first_level_b = Category.objects.create(
            tree_parent=self.category_top_level_b,
            slug='a1-first-nested-level',
            title='a1 first nested level',
            description='nested',
            site=self.site_second
        )
        self.nested_first_level_two_b = Category.objects.create(
            tree_parent=self.category_top_level_b,
            slug='a2-first-nested-level',
            title='a2 first nested level',
            description='nested',
            site=self.site_second
        )
        self.nested_second_level_b = Category.objects.create(
            tree_parent=self.nested_first_level_b,
            slug='a4-second-nested-level',
            title='a4 second nested level',
            description='nested',
            site=self.site_second
        )
        self.nested_second_level_two_b = Category.objects.create(
            tree_parent=self.nested_first_level_two_b,
            slug='a5-second-nested-level',
            title='a5 second nested level',
            description='nested',
            site=self.site_second
        )

        self.categories = [
            self.category_top_level, self.nested_first_level, self.nested_first_level_two, self.nested_second_level, self.nested_second_level_two,
            self.category_top_level_b, self.nested_first_level_b, self.nested_first_level_two_b, self.nested_second_level_b, self.nested_second_level_two_b,
        ]

def create_basic_categories(case):
    case.site_id = getattr(settings, "SITE_ID", 1)

    case.category = Category.objects.create(
        title=u"你好 category",
        description=u"exmple testing category",
        site_id = case.site_id,
        slug=u"ni-hao-category",
    )

    case.category_nested = Category.objects.create(
        title=u"nested category",
        description=u"category nested in case.category",
        tree_parent=case.category,
        site_id = case.site_id,
        slug=u"nested-category",
    )

    case.category_nested_second = Category.objects.create(
        title=u" second nested category",
        description=u"category nested in case.category_nested",
        tree_parent=case.category_nested,
        site_id = case.site_id,
        slug=u"second-nested-category",
    )

def create_and_place_a_publishable(case):
    case.publishable = Article.objects.create(
        title=u'First Article',
        slug=u'first-article',
        description=u'Some\nlonger\ntext',
        category=case.category_nested,
        publish_from=datetime(2008,1,10),
        published=True
    )
    case.only_publishable = Publishable.objects.get(pk=case.publishable.pk)


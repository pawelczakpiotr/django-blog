from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from blog.models import Post


class LatestPostsFeed(Feed):
    title = 'Mój blog'
    link = '/blog/'
    description = 'Nowe posty na moim blogu.'

    def items(self):
        return Post.published.all()[:5]

    def item_title(self, item: Post):
        return item.title

    def item_description(self, item: Post):
        return truncatewords(item.body, 30)


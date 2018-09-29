# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import Article, Catagory, Tag

from django.views.generic.base import View
from django.http import HttpResponse
from operation.models import UserFavArticle
from article.models import Article

# Create your views here.


class ArticleListView(View):
    """
    文章列表页
    """
    def get(self, request):
        all_article = Article.objects.all().order_by("-date_publish")
        # 对文章进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_article, 3, request=request)

        all_article = p.page(page)


        return render(request, 'all_Article_list.html', locals())



class ArticleCategoryListView(View):
    """
    文章列表页 按类别列表
    """
    def get(self, request, category):

        all_article = Article.objects.filter(category__name=category)
        print(all_article)

        # 对文章进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_article, 3, request=request)

        all_article = p.page(page)

        return render(request, 'Article_list.html', {
            "all_article": all_article,
            "category": category,
        })


# class ArticleDetailView(View):
#     """
#     文章详情页
#     """
#     def get(self, request, category, article_id):
#
#         article = Article.objects.get(id=int(article_id))
#
#         return render(request, 'Article.html', {
#             "article": article,
#             "category": category,
#         })

class ArticleDetailView(View):
    """
    文章详情页
    """
    def get(self, request, article_id):

        article = Article.objects.get(id=int(article_id))
        article.click_count += 1
        article.save()



        # 是否收藏文章
        has_fav_article = False

        if request.user.is_authenticated():
            if UserFavArticle.objects.filter(user=request.user, article_id=article.id):
                has_fav_article = True


        return render(request, 'Article.html', locals())


class AddFavView(View):
    """
    用户收藏，用户取消收藏
    """
    def post(self, request):
        article_id = request.POST.get('article_id', 0)


        if not request.user.is_authenticated():
            #判断用户登录状态
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')

        exist_records = UserFavArticle.objects.filter(user=request.user, article_id=int(article_id))
        if exist_records:
            #如果记录已经存在， 则表示用户取消收藏
            exist_records.delete()
            article = Article.objects.get(id=int(article_id))
            article.fav_num -= 1
            if article.fav_num < 0:
                article.fav_num = 0
            article.save()
            return HttpResponse('{"status":"success", "msg":"收藏"}', content_type='application/json')
        else:
            user_fav = UserFavArticle()
            if int(article_id) > 0 :
                user_fav.user = request.user
                user_fav.article_id = int(article_id)
                user_fav.save()
                article = Article.objects.get(id=int(article_id))
                article.fav_num += 1
                article.save()
                return HttpResponse('{"status":"success", "msg":"已收藏"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail", "msg":"收藏出错"}', content_type='application/json')
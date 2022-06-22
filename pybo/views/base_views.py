from typing import Counter
from unicodedata import category
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Count

from ..models import Answer, Question, QuestionCount, Category


def index(request):
    """
    pybo 목록 출력
    """
    page = request.GET.get('page', '1')     # 페이지
    kw = request.GET.get('kw', '')          # 검색어
    so = request.GET.get('so', 'recent')    # question 정렬 기준
    category = request.GET.get('category', 'qna')

    category_obj = get_object_or_404(Category, name=category)
    question_list = Question.objects.filter(category=category_obj)

    #question 정렬
    if so == 'recommend':
        question_list = question_list.annotate(
            num_voter=Count('voter')).order_by('-num_voter', '-create_date')
    elif so == 'popular':
        question_list = question_list.annotate(
            num_answer=Count('answer')).order_by('-num_answer', '-create_date')
    else:   # recent
        question_list = question_list.order_by('-create_date')
    
    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |
            Q(content__icontains=kw) |
            Q(author__username__icontains=kw) |
            Q(answer__author__username__icontains=kw)
        ).distinct()
    
    # 페이징 처리
    paginator = Paginator(question_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)

    category_list = Category.objects.all()

    print(category_list)

    context = {'question_list': page_obj, 'page':page, 'kw':kw, 'category': category, 'category_list': category_list}

    return render(request, 'pybo/question_list.html', context)
    

def detail(request, question_id):
    """
    pybo 내용 출력
    """
    question = Question.objects.get(pk=question_id)
    
    # 조회수
    ip = get_client_ip(request)
    cnt = QuestionCount.objects.filter(ip=ip, question=question).count()
    if cnt == 0:
        qc = QuestionCount(ip=ip, question=question)
        qc.save()

    context = {'question': question}
    return render(request, 'pybo/question_detail.html', context)
    
    

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
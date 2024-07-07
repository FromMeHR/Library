from django.db.models import Q
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, SearchHeadline

from books.models import Books

def q_search(query):
    if query.isdigit() and len(query) <= 5:
        return Books.objects.filter(id=int(query)) # need queryset (not object using .get())
    
    vector = SearchVector("name", "description")
    query = SearchQuery(query)
    result = Books.objects.annotate(rank=SearchRank(vector, query)).order_by('-rank').filter(rank__gt=0)
    result = result.annotate(
        headline=SearchHeadline(
            "name",
            query,
            start_sel='<span style="background-color: yellow;">',
            stop_sel="</span>",
        )
    )
    result = result.annotate(
        bodyline=SearchHeadline(
            "description",
            query,
            start_sel='<span style="background-color: yellow;">',
            stop_sel="</span>",
        )
    )
    return result
    # return Books.objects.annotate(search=SearchVector("name", "description")).filter(search=query)

    # keywords = [word for word in query.split() if len(word) > 2]
    # q_objects = Q()
    # for token in keywords:
    #     q_objects |= Q(description__icontains=token)
    #     q_objects |= Q(name__icontains=token)
    # return Books.objects.filter(q_objects)
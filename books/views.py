# Create your views here.
from django.shortcuts import render_to_response, Http404, render
from django.template import RequestContext
from django.shortcuts import get_object_or_404
from books.models import Book
from django.http import HttpResponse, HttpResponseRedirect
import urllib, urllib2
import json 

def incr_reads(request, book_id):
    if request.POST:
        try:
            readers = Book.objects.get(id=book_id).incr_reads()
            return HttpResponse(readers)
        except Book.DoesNotExist:
            pass
    return HttpResponse('FAILED')

def index(request):
    '''
    No processing, should use direct to template.
    '''
    return render_to_response('index.html', {}, context_instance=RequestContext(request))

def search(request):
    if request.GET and 'q' in request.GET:
        b = Book.search.query(request.GET['q'])
    return render_to_response('books/book_list.html', {'object_list':b}, context_instance=RequestContext(request))

def suggest_image(request, *args, **kwargs):
    '''
    So this is a helper view for staff to update the picture.
    '''
    if kwargs:
        book_id = kwargs.get('book_id')
    b = Book.objects.get(id=book_id)
    _img = b.get_image_suggestions(first=False)
    return render_to_response('books/image_suggestor.html', {'images':_img, 'book':b}, context_instance=RequestContext(request))

def select_image(request, book_id):
    '''
    This view selects the image for a book and saves it in the database.
    '''
    if request.POST:
        book = get_object_or_404(Book, pk=book_id)
        image = request.POST['img-src']
        book.image = image
        book.save()

    return HttpResponse('success')

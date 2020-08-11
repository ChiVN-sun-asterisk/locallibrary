from django.shortcuts import render, get_object_or_404
from catalog.models import Book, Author, BookInstance, Genre
from django.views import generic

def index(request):
  """View function for home page of site."""

  # Generate counts of some of the main objects
  num_books = Book.objects.all().count()
  num_instances = BookInstance.objects.all().count()
    
  # Available books (status = 'a')
  num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    
  # The 'all()' is implied by default.    
  num_authors = Author.objects.count()
  
  num_genres=Genre.objects.all().count()

  num_books_available = Book.objects.filter(title__exact='b').count()

  context = {
    'num_books': num_books,
    'num_instances': num_instances,
    'num_instances_available': num_instances_available,
    'num_authors': num_authors,
    'num_genres': num_genres,
    'num_books_available': num_books_available,
  }

  # Render the HTML template index.html with the data in the context variable
  return render(request, 'index.html', context=context)

class BookListView(generic.ListView):
  model = Book
  paginate_by = 10

  def get_context_data(self, **kwargs):
    # Call the base implementation first to get the context
    context = super(BookListView, self).get_context_data(**kwargs)
    # Create any data and add it to the context
    context['some_data'] = 'This is just some data'
    return context

class BookDetailView(generic.DetailView):
  model = Book

  def book_detail_view(request, primary_key):
    book = get_object_or_404(Book, pk=primary_key)
    return render(request, 'catalog/book_detail.html', context={'book': book})

class AuthorListView(generic.ListView):
  model = Author
  paginate_by = 10

  def get_context_data(self, **kwargs):
    # Call the base implementation first to get the context
    context = super(AuthorListView, self).get_context_data(**kwargs)
    # Create any data and add it to the context
    context['some_data'] = 'This is just some data'
    return context

class AuthorDetailView(generic.DetailView):
  model = Author

  def author_detail_view(request, primary_key):
    author = get_object_or_404(Author, pk=primary_key)
    return render(request, 'catalog/author_detail.html', context={'author': author})

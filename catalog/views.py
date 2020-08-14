import datetime

from django.shortcuts import render, get_object_or_404
from catalog.models import Book, Author, BookInstance, Genre
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from catalog.forms import RenewBookForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView

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

  num_visits = request.session.get('num_visits', 0)
  request.session['num_visits'] = num_visits + 1

  context = {
    'num_books': num_books,
    'num_instances': num_instances,
    'num_instances_available': num_instances_available,
    'num_authors': num_authors,
    'num_genres': num_genres,
    'num_books_available': num_books_available,
    'num_visits': num_visits,
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

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
  """Generic class-based view listing books on loan to current user."""
  model = BookInstance
  template_name ='catalog/bookinstance_list_borrowed_user.html'
  paginate_by = 10
  
  def get_queryset(self):
    return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

class AllBorrowedBooksListView(LoginRequiredMixin,generic.ListView):
  model = BookInstance
  permission_required = 'catalog.can_mark_returned'
  template_name ='catalog/all_bookinstance_list_borrowed.html'
  paginate_by = 10
    
  def get_queryset(self):
    return BookInstance.objects.filter(status__exact='o').order_by('due_back')

@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
  book_instance = get_object_or_404(BookInstance, pk = pk)

  if request.method == 'POST':
    form = RenewBookForm(request.POST)
    if form.is_valid():
      book_instance.due_back = form.cleaned_data['renewal_date']
      book_instance.save()

      return HttpResponseRedirect(reverse('all-borrowed'))
  else:
    proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
    form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})
  
  context = {
    'form': form,
    'book_instance': book_instance,
  }

  return render(request, 'catalog/book_renew_librarian.html', context)

class AuthorCreate(CreateView):
  model = Author
  fields = '__all__'
  initial = {'date_of_death': '05/01/2018'}

class AuthorUpdate(UpdateView):
  model = Author
  fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']

class AuthorDelete(DeleteView):
  model = Author
  success_url = reverse_lazy('authors')

class BookCreate(CreateView):
  model = Book
  fields = '__all__'

class BookUpdate(UpdateView):
  model = Book
  fields = '__all__'

class BookDelete(DeleteView):
  model = Book
  success_url = reverse_lazy('books')

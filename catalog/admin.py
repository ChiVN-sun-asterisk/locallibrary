from django.contrib import admin
from .models import Author, Genre, Book, BookInstance, Language

# admin.site.register(Book)
# admin.site.register(Author)
# admin.site.register(Genre)
# admin.site.register(BookInstance)

class BooksInline(admin.TabularInline):
  model = Book

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
  list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
  exclude = ['date_of_death', 'last_name' ]
  inlines = [BooksInline]
  
class BooksInstanceInline(admin.TabularInline):
  model = BookInstance

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
  list_display = ('title', 'author', 'display_genre')
  inlines = [BooksInstanceInline]

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
  list_display = ('book', 'imprint', 'borrower', 'due_back', 'status', 'id')
  list_filter = ('status', 'due_back')
  fieldsets = (
    (None, {
      'fields': ('book', 'imprint', 'id')
    }),
    ('Availability', {
      'fields': ('status', 'due_back', 'borrower')
    }),
  )

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
  pass

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
  pass

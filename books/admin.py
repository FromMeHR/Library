from django.contrib import admin
from books.models import Categories, Books, WatchedLinks

@admin.register(Categories)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('name','slug')
    list_display = ('name','slug')
    
@admin.register(Books)
class BookAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('name','quantity','author','category','publication_year','date_of_issue')
    list_display = ('name','quantity','description','author','publication_year','date_of_issue')
    search_fields = ['name','description']
    filter_horizontal = ['category']
    
@admin.register(WatchedLinks)
class WatchedLinksAdmin(admin.ModelAdmin):
    list_display = ('user','book',)
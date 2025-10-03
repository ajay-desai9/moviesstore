from django.contrib import admin
from .models import Movie, Review, MovieRequest, Petition, PetitionVote

class MovieAdmin(admin.ModelAdmin):
    ordering = ['name']
    search_fields = ['name']

class MovieRequestAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'date']
    list_filter = ['date', 'user']
    search_fields = ['name', 'description']
    ordering = ['-date']

class PetitionVoteInline(admin.TabularInline):
    model = PetitionVote
    extra = 0
    readonly_fields = ['created_at']

class PetitionAdmin(admin.ModelAdmin):
    list_display = ['title', 'movie_title', 'created_by', 'vote_count', 'total_votes', 'created_at', 'is_active']
    list_filter = ['created_at', 'is_active', 'created_by']
    search_fields = ['title', 'movie_title', 'description']
    ordering = ['-created_at']
    inlines = [PetitionVoteInline]

class PetitionVoteAdmin(admin.ModelAdmin):
    list_display = ['petition', 'user', 'vote_type', 'created_at']
    list_filter = ['vote_type', 'created_at']
    search_fields = ['petition__title', 'user__username']

admin.site.register(Movie, MovieAdmin)
admin.site.register(Review)
admin.site.register(MovieRequest, MovieRequestAdmin)
admin.site.register(Petition, PetitionAdmin)
admin.site.register(PetitionVote, PetitionVoteAdmin)
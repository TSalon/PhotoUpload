from django.contrib import admin
from .models import Competition, Competitor, Entry

class CompetitorAdmin(admin.ModelAdmin):
    readonly_fields=('last_upload', 'first_upload',)
    list_display = ['__unicode__', 'member_number','enabled','last_upload']
    
class CompetitionAdmin(admin.ModelAdmin):
    list_display = ['judge_date', 'name', 'level', 'download_url', ]
    
class EntryAdmin(admin.ModelAdmin):
    list_display = ['owner', 'position', 'title', 'competition', ]
    list_filter = ('competition', 'owner', )
    search_fields = ('title',)

admin.site.register(Competition, CompetitionAdmin)
admin.site.register(Competitor, CompetitorAdmin)
admin.site.register(Entry, EntryAdmin)


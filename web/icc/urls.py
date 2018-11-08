from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

from competition import views
from photohunt import views as photohuntviews

urlpatterns = [
    # standard competition upload stuff
    url(r'^$', views.login, name='login'),
    url(r'^entries/(?P<pHash>[a-z0-9]+)/(?P<pMemberNumber>[0-9]+)/(?P<pSurname>[A-Za-z]+)/$', views.entries, name='entries'),
    url(r'^competition/(?P<pCompetitionSerial>[0-9]+)/(?P<pHash>[a-z0-9]+)/(?P<pMemberNumber>[0-9]+)/(?P<pSurname>[A-Za-z]+)/$', views.competition, name='competition'),
    url(r'^competition/delete/(?P<pHash>[a-z0-9]+)/(?P<pMemberNumber>[0-9]+)/(?P<pSurname>[A-Za-z]+)/(?P<pCompetitionSerial>[0-9]+)/$', views.competition_delete_entries, name='competition_delete_entries'),
    url(r'^competition/addentry/(?P<pCompetitionSerial>[0-9]+)/(?P<pHash>[a-z0-9]+)/(?P<pMemberNumber>[0-9]+)/(?P<pSurname>[A-Za-z]+)/$', views.competition_add_entry, name='competition_add_entry'),
    url(r'^download/(?P<pCompetitionSerial>[0-9]+)/(?P<pDownloadHash>[a-zA-Z0-9]+)/$', views.download, name='download'),
    url(r'^download/(?P<pCompetitionSerial>[0-9]+)/(?P<pDownloadHash>[a-zA-Z0-9]+)/No3/$', views.download_no_third, name='download-no-third'),
    url(r'^download/$', views.completed_entries, name='completed_entries'),
    url(r'^all_entries_list/$', views.all_entries_list, name='all_entries_list'),
    
    # photo hunt upload form
    url(r'^photohunt/$', photohuntviews.homepage, name='photohunt_home'),
    url(r'^photohunt/submit/$', photohuntviews.submit, name='photohunt_submit'),
    url(r'^photohunt/thanks/$', photohuntviews.thanks, name='photohunt_thanks'),
    url(r'^photohunt/DownloadAllEntries/$', photohuntviews.download, name='photohunt_download'),
    
    # admin site
    url(r'^admin/', include(admin.site.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

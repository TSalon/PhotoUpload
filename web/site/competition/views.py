from datetime import datetime
import hashlib, os, shutil, StringIO, zipfile

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .forms import EntryForm
from .models import Competitor, Competition, Entry


def login(request):
  """
  Show login form (surname/member number/club password) and allow login to the user page
  """
  lErrorMessage = None
  if request.POST:
    if request.POST['password'] == 'hotel':
      lMemberNumber = request.POST['member_number'].strip()
      lSurname = request.POST['surname'].strip()
      try:
	lCompetitor = Competitor.objects.filter(member_number=lMemberNumber, surname__iexact=lSurname)[0]
	lStringToHash = "%s%s%s" % (lCompetitor.id, lCompetitor.first_name, lCompetitor.surname,)
	lHash = hashlib.sha1(lStringToHash).hexdigest()
	return HttpResponseRedirect('/entries/%s/%s/%s/' % (lHash, lCompetitor.member_number, lCompetitor.surname))
      except IndexError:
        # No user found
        lErrorMessage = "Sorry, that combination of member number and surname is not correct"
  
    else:
      lErrorMessage = "Password incorrect"
      
  context = {
    'error_message' : lErrorMessage,
	     }
  return render(request, 'competition/login.html', context)



def _fetch_competitor(pHash, pMemberNumber, pSurname):
  """
  Check integrity of url information and return it
  """
  try:
    lCompetitor = Competitor.objects.filter(member_number=pMemberNumber, surname__iexact=pSurname)[0]
    lStringToHash = "%s%s%s" % (lCompetitor.id, lCompetitor.first_name, lCompetitor.surname,)
    lHash = hashlib.sha1(lStringToHash).hexdigest()
    if pHash != lHash:
      return None
    return lCompetitor
  except IndexError:
    return None


def entries(request, pHash, pMemberNumber, pSurname):
  """
  Show available contests
  """
  lCompetitor = _fetch_competitor(pHash, pMemberNumber, pSurname)
  if lCompetitor == None:
    raise Http404
  
  lNow = datetime.today()
     
  # closed competitions
  lClosedCompetitions = Competition.objects.filter(end_date__lt=lNow).order_by('-end_date')
  for competition in lClosedCompetitions:
    competition.Entries = competition.entry_set.filter(owner=lCompetitor)
    
  # paged competitions
  lPagedCompetitions = Competition.objects.filter(start_date__lte=lNow, end_date__gte=lNow) 
      
  lClubCompetitions = lPagedCompetitions.filter(level='club')
  for competition in lClubCompetitions:
    competition.Entries = competition.entry_set.filter(owner=lCompetitor)
    competition.EntryCount = competition.Entries.count()
    
  lExternalCompetitions = lPagedCompetitions.filter(level='external')
  for competition in lExternalCompetitions:
    competition.Entries = competition.entry_set.filter(owner=lCompetitor)
    competition.EntryCount = competition.Entries.count()
  
  lContext = {
    'ClosedCompetitions' : lClosedCompetitions,
    'ClubCompetitions' : lClubCompetitions,
    'ExternalCompetitions' : lExternalCompetitions,
    'Competitor' : lCompetitor,
    'Hash' : pHash,
    }
  
  return render(request, 'competition/entries.html', lContext)


def competition(request, pCompetitionSerial, pHash, pMemberNumber, pSurname, pFormWithErrors=None):
  """
  Show a single competition and allow entries to be added
  """
  lCompetitor = _fetch_competitor(pHash, pMemberNumber, pSurname)
  if lCompetitor == None:
    raise Http404

  lNow = datetime.today() 
  try:
    lCompetition = Competition.objects.filter(id=pCompetitionSerial, start_date__lte=lNow, end_date__gte=lNow)[0]
  except IndexError:
    raise Http404
  
  lCompetition.Entries = lCompetition.entry_set.filter(owner=lCompetitor)
  if lCompetition.Entries.count() >= lCompetition.max_photos:
    lCompetition.UploadMorePhotos = False
  else:
    lCompetition.UploadMorePhotos = True
      
  if pFormWithErrors:
    lEntryForm = pFormWithErrors
  else:
    lEntry = Entry()
    lEntry.competition = lCompetition
    lEntryForm = EntryForm(instance=lEntry)
  
  lContext = {
    'Competition' : lCompetition,
    'Competitor' : lCompetitor,
    'EntryForm' : lEntryForm,
    'Hash' : pHash,
    }
  
  return render(request, 'competition/competition.html', lContext)



def competition_delete_entries(request, pHash, pMemberNumber, pSurname, pCompetitionSerial):
    """
    Delete an entry from a single competition page
    """
    lCompetitor = _fetch_competitor(pHash, pMemberNumber, pSurname)
    if lCompetitor == None:
      raise Http404
  
    try:
      lCompetition = Competition.objects.filter(id=pCompetitionSerial)[0]
    except IndexError:
        raise Http404
    
    try:
      Entry.objects.filter(owner=lCompetitor,competition=lCompetition).delete()
    except IndexError:
      raise Http404
    
    return HttpResponseRedirect('/competition/%d/%s/%s/%s/' % (lCompetition.id, pHash, lCompetitor.member_number, lCompetitor.surname))  
    
    
    
    
@csrf_exempt     
def competition_add_entry(request, pCompetitionSerial, pHash, pMemberNumber, pSurname):
  """
  Add a new entry for a competition
  """
  lCompetitor = _fetch_competitor(pHash, pMemberNumber, pSurname)
  if lCompetitor == None:
    raise Http404
  
  try:
    lCompetition = Competition.objects.filter(id=pCompetitionSerial)[0]
  except IndexError:
    raise Http404
  
  lEntry = Entry()
  lEntry.competition = lCompetition
  lForm = EntryForm(request.POST, request.FILES, instance=lEntry)
  
  if lForm.is_valid() == False:
    return competition(request, pCompetitionSerial, pHash, pMemberNumber, pSurname, lForm)
  
  lEntry = lForm.save(commit=False)
  lEntry.owner = lCompetitor
  lEntry.competition = lCompetition
  lEntry.save()
  
  lCompetitor.last_upload = datetime.now()
  if lCompetitor.first_upload == None:
    lCompetitor.first_upload = datetime.now()
  lCompetitor.save()
  
  return HttpResponseRedirect('/competition/%d/%s/%s/%s/' % (lCompetition.id, pHash, lCompetitor.member_number, lCompetitor.surname))  
    

def download_no_third(request, pCompetitionSerial, pDownloadHash):
    """
    Download competition entries, but don't include thirds
    """ 
    return download(request, pCompetitionSerial, pDownloadHash, False)
  
@login_required
def download(request, pCompetitionSerial, pDownloadHash, pIncludeThirds=True):
  """
  Download competition entries as a zip file
  """
  try:
    lCompetition = Competition.objects.filter(id=pCompetitionSerial)[0]
  except IndexError:
    raise Http404

  if lCompetition.download_hash() != pDownloadHash:
    raise Http404
  
  lPath = '/home/tjs/web/icc/site_media/zip/%d' % (lCompetition.id)
  if os.path.exists(lPath):
    shutil.rmtree(lPath)
  os.makedirs(lPath)
  
  
  ### TODO need to exclude any entries that don't meet the min_photos criteria
  
  lEntries = lCompetition.entry_set.all().order_by('id')
  if not pIncludeThirds:
      lEntries = lEntries.exclude(position=3)
  for entry in lEntries:
    entry.save_entry_for_judge(lPath)
    
  lMinimumEntries = lCompetition.min_photos
  
  lZipFileName = "%s.zip" % lCompetition.filename()
  s = StringIO.StringIO()
  zf = zipfile.ZipFile(s, "w")
  for membername in os.listdir(lPath):
      for filename in os.listdir(lPath + "/" + membername):
          filepath = "%s/%s/%s" % (lPath, membername, filename)
          zippath = "%s/%s" % (membername, filename)
          zf.write(filepath, zippath)
  zf.close()
  
  resp = HttpResponse(s.getvalue(), content_type = "application/x-zip-compressed")
  resp['content-disposition'] = 'attachment; filename="%s"' % lZipFileName
  
  return resp
  
  
  
@login_required
def completed_entries(request):
    lCompetitions = Competition.objects.all().order_by('-judge_date')
    
    lContext = {
      'Competitions' : lCompetitions,
    }
    
    return render(request, 'competition/download.html', lContext) 

@login_required
def all_entries_list(request):
    """
    Provide a list and thumbnails of all entries, ordered by title
    """
    lEntries = Entry.objects.all().order_by('title')

    lContext = {
      'Entries' : lEntries,
    }
    
    
    return render(request, 'competition/all_entries_list.html', lContext) 
    

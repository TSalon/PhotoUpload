from datetime import date
from django.db import models
from django.utils.dateformat import format
import hashlib
import os
import shutil


class Competition(models.Model):
  """
  A photographic competition 
  """
  start_date = models.DateField(help_text='Date the competition opens')
  end_date = models.DateField(help_text='Last date for entries into the competition')
  judge_date= models.DateField(help_text='The date that the competition will be judged')
  name = models.CharField(max_length=200, help_text='Name of the competition')
  description = models.TextField(help_text='Judging criteria for the competition')
  min_photos = models.IntegerField(default=1, help_text='The minimum number of photos that can be entered for this competition')
  max_photos = models.IntegerField(default=3, help_text='The maximum number of photos that can be entered for this competition')
  LEVEL_CHOICES = (
            ('club','Club Competition'),
            ('external','External Competition'),
      )
  level = models.CharField(max_length=20, default='club', choices=LEVEL_CHOICES, help_text='Type of competition')
  DIMENSION_CHOICES = (
            ('1050x1400', '1050 x 1400'),
            ('1200x1600', '1200 x 1600')
    )
  upload_dimensions = models.CharField(max_length=12, default='1050x1400', choices=DIMENSION_CHOICES, help_text='dimensions of PDI required')
  
  def __unicode__(self):
    return "%s %s" % (self.judge_date, self.name)

  def horizontal(self):
      return int(self.upload_dimensions[5:9])

  def vertical(self):
      return int(self.upload_dimensions[0:4])


  def width(self):
      lTotal = 100.0
      lMaxPhotos = self.max_photos
      lWidth = lTotal / lMaxPhotos
      return lWidth

  @property
  def download_url(self):
    """
    Return the download url for downloading entries
    """
    return "http://icc.hotmandarins.co.uk/download/%s/%s/" % (self.id, self.download_hash())

  def download_url_no_third(self):
    """
    Return the download url for downloading entries
    """
    return "http://icc.hotmandarins.co.uk/download/%s/%s/No3/" % (self.id, self.download_hash())

  def download_hash(self):
    """
    Return the unique download hash for this competition
    """
    lStringToHash = "%s_%s_%s_%s" % (self.start_date, self.end_date, self.judge_date, self.name)
    lHash = hashlib.sha1(lStringToHash).hexdigest()
    return lHash

  def entrycount(self):
      """
      Return the number of entries for this competition
      """
      return self.entry_set.count()
  
  def entrycount_no_thirds(self):
      """
      Return the number of entries for this competition, excluding third images
      """
      return self.entry_set.exclude(position=3).count() 
  
  def filename(self):
    lDate = format(self.judge_date, 'Y-m-d')
    return "%s %s" % (lDate, self.name)
  
  def entrycountdescription(self):
    if self.max_photos == self.min_photos:
      return "To enter this competition you need to upload %d pictures" % self.max_photos
    elif self.min_photos == 1:
      return "You may enter up to %d pictures for this competition" % self.max_photos
    else:
      return "You must enter a minimum of %d images, and a maximum of %d images for this competition" % (self.min_photos, self.max_photos)
  
  def status_class(self):
      lToday = date.today()
      if self.end_date >= lToday:
          return "danger"
      elif self.judge_date > lToday:
          return "success"
      return ""
  
  class Meta:
    ordering = ['judge_date', 'name']
  
  
class Competitor(models.Model):
  """
  A person who takes part in a photographic competition
  """
  first_name = models.CharField(max_length=100, help_text='Competitor first name')
  surname = models.CharField(max_length=50, help_text='Competitor surname for login')
  member_number = models.CharField(max_length=5, help_text='The icc unique member number')
  last_upload = models.DateTimeField(blank=True, null=True, help_text='The last time this person uploaded anything')
  first_upload = models.DateTimeField(blank=True, null=True, help_text='The first time this person uploaded anything')
  enabled = models.BooleanField(default=True, help_text='Whether this person is allowed to enter contests or not')
  
  def __unicode__(self):
    return "%s, %s %s" % (self.surname, self.first_name, self.member_number)

  class Meta:
    ordering = ['member_number', ]
  
class Entry(models.Model):
  """
  A photograph entered into a competition
  """
  competition = models.ForeignKey(Competition, help_text='The competition this photograph is entered into')
  owner = models.ForeignKey(Competitor, help_text='The person entering this competition')
  photo = models.ImageField(upload_to='photos/%Y/%m/%d', help_text='Click "Choose File" to select your .JPG file to enter')
  title = models.CharField(max_length=50, help_text='A short title for your image')
  position = models.IntegerField(blank=True, help_text='The position of the image, last choice images will be dropped if too many entries')
  
  def __unicode__(self):
    return "%s - %s - %s" % (self.owner, self.competition, self.title)

  def save(self, *args, **kwargs):
    if not self.position:
      lEntryCount = self.competition.entry_set.filter(owner=self.owner).count()
      self.position = lEntryCount + 1
    self.title = self.title.replace('_', ' ')
    super(Entry, self).save(*args, **kwargs)
    
  def processFilename(self, pTitle):
    lReturn = ""
    lValid = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890, -_"
    for eachChar in pTitle:
        if eachChar in lValid:
            lReturn += eachChar
    return lReturn
    
  def save_entry_for_judge(self, pPath):
    lSourcePath = self.photo.path
    lMemberName = "%s %s" % (self.owner.first_name, self.owner.surname)
    lDestinationPath = "%s/%s" % (pPath, lMemberName)
    if not os.path.exists(lDestinationPath):
        os.mkdir(lDestinationPath)
    lTitleForFilename = self.processFilename(self.title)
    lDestinationFile = "%s/%s_%s_%s.jpg" % (lDestinationPath, self.owner.member_number, self.position, lTitleForFilename)
    shutil.copyfile(lSourcePath, lDestinationFile)
    
  class Meta:
    ordering = ['position', ]
			    

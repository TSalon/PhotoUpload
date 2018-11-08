from django.forms import ModelForm, ValidationError
from .models import Entry
from django.core.files.images import get_image_dimensions

def get_image_colourspace(file_or_path, close=False):
    """
    Return the colorspace of an image
    """
    from PIL import ImageFile as PillowImageFile

    p = PillowImageFile.Parser()
    if hasattr(file_or_path, 'read'):
        file = file_or_path
        file_pos = file.tell()
        file.seek(0)
    else:
        file = open(file_or_path, 'rb')
        close = True
    try:
        # Most of the time Pillow only needs a small chunk to parse the image
        # and get the dimensions, but with some TIFF files Pillow needs to
        # parse the whole file.
        chunk_size = 1024
        while 1:
            data = file.read(chunk_size)
            if not data:
                break
            try:
                p.feed(data)
            except zlib.error as e:
                # ignore zlib complaining on truncated stream, just feed more
                # data to parser (ticket #19457).
                if e.args[0].startswith("Error -5"):
                    pass
                else:
                    raise
            if p.image:
                return p.image.info.get('icc_profile')
            chunk_size *= 2
        return None
    finally:
        if close:
            file.close()
        else:
            file.seek(file_pos)


class EntryForm(ModelForm):
  """
  Form representing an image file upload
  """
  class Meta:
    model = Entry
    fields = ['photo','title',]
    
  def clean_photo(self):
      photo = self.cleaned_data.get("photo")
      if not photo:
        raise ValidationError("No image uploaded!")
      else:
        w, h = get_image_dimensions(photo)
        if w > h:
          lLandscape = True
          lPortrait = False
          lSquare = False
        elif h > w:
          lLandscape = False
          lPortrait = True
          lSquare = False
        else:
          lLandscape = False
          lPortrait = False
          lSquare = True

        lVertical = self.instance.competition.vertical()
        lHorizontal = self.instance.competition.horizontal()

        if lLandscape:
          if w > lHorizontal or h > lVertical:
            raise ValidationError("Images must not exceed %i pixels wide by %i pixels high whether you are using landscape or portrait format.  Scale your original image proportionately so it fills either the maximum width (%ipx) or maximum height (%ipx) or both.  This image is %i wide x %i high." % (lHorizontal, lVertical, lHorizontal, lVertical, w,h) )
           
          if w < lHorizontal and h < lVertical - 10:
            raise ValidationError("Images must not exceed %i pixels wide by %i pixels high whether you are using landscape or portrait format.  Scale your original image proportionately so it fills either the maximum width (%ipx) or maximum height (%ipx) or both.  This image is %i wide x %i high." % (lHorizontal, lVertical, lHorizontal, lVertical, w,h) )
	     
        if lPortrait:
          if h < lVertical - 50 or h > lVertical:
            raise ValidationError("Images must not exceed %i pixels wide by %i pixels high whether you are using landscape or portrait format.  Scale your original image proportionately so it fills either the maximum width (%ipx) or maximum height (%ipx) or both.  This image is %i wide x %i high." % (lHorizontal, lVertical, lHorizontal, lVertical, w,h) )
	     
        if lSquare:
          if h > lVertical or h < lVertical - 50:
            raise ValidationError("The maximum allowed height and width of a square image is %ipx.  This image is %i on each side. Scale your original image proportionately so it has a height and width of %ipx. " % (lVertical, h, lVertical))
           
        return photo

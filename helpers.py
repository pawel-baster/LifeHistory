from PIL import Image
from PIL.ExifTags import TAGS

class ExifHelper:
    
    @staticmethod
    def get_exif_data(fname):
        """Get embedded EXIF data from image file."""
        ret = {}
        img = Image.open(fname)
        if hasattr( img, '_getexif' ):
            exifinfo = img._getexif()
            if exifinfo != None:
                for tag, value in exifinfo.items():
                    decoded = TAGS.get(tag, tag)
                    ret[decoded] = value
        return ret

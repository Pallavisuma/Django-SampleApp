from django.contrib import admin
from .models import EmployeeRefer, Position,PDFFile

  
admin.site.register(EmployeeRefer)
admin.site.register(Position)

from .models import OTP

# Register the OTP model with the admin site
admin.site.register(OTP)
admin.site.register(PDFFile)

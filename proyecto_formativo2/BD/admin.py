from django.contrib import admin
from .models import Instructor

# Register your models here.
class InstructorAdmin(admin.ModelAdmin):
    list_display = ("nomb_instr", "corr_instr","ciud_instr", "tele_instr", "resu_instr", "carg_instr", "cent_instr", "foto_instr")
admin.site.register(Instructor, InstructorAdmin)
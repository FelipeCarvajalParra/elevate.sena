from django.contrib.auth.models import User
from django.db import models


class Aspirante(models.Model):
    docu_aspir = models.CharField(max_length=45, primary_key=True)
    tdoc_aspir = models.CharField(max_length=45)
    pnom_aspir = models.CharField(max_length=45)
    snom_aspir = models.CharField(max_length=45, blank=True, null=True)
    pape_aspir = models.CharField(max_length=45)
    sape_aspir = models.CharField(max_length=45)
    gene_aspir = models.CharField(max_length=45)
    pais_aspir = models.CharField(max_length=80)
    fech_aspir = models.DateField()
    corr_aspir = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'aspirante'

class Ficha(models.Model):
    nume_ficha = models.IntegerField(primary_key=True)
    curs_ficha = models.IntegerField()
    inic_ficha = models.DateField()
    fina_ficha = models.DateField()
    luga_ficha = models.CharField(max_length=60)
    nota_ficha = models.CharField(max_length=300)
    ficha_activa = models.IntegerField(default=1)
    iden_instr2 = models.ForeignKey('Instructor', models.DO_NOTHING, db_column='iden_instr2')

    class Meta:
        managed = False
        db_table = 'ficha'


class FichaAspirante(models.Model):
    iden_ficha_aspirante = models.AutoField(primary_key=True)
    nume_ficha1 = models.ForeignKey(Ficha, models.DO_NOTHING, db_column='nume_ficha1')
    docu_aspir1 = models.ForeignKey(Aspirante, models.DO_NOTHING, db_column='docu_aspir1')
    nive_aspir = models.CharField(max_length=100)
    area_aspir = models.CharField(max_length=100)
    carg_aspir = models.CharField(max_length=100)
    empl_aspir = models.CharField(max_length=100)
    arl_aspir = models.CharField(max_length=100)
    sect_aspir = models.CharField(max_length=100)
    fech_regis = models.DateField(auto_now=True)
    doc0 = models.FileField(upload_to='requisitos-previos/', blank=True, null=True) #formato requisitos previos
    doc1 = models.FileField(upload_to='documentos/', blank=True, null=True)
    doc2 = models.FileField(upload_to='documentos/', blank=True, null=True)
    doc3 = models.FileField(upload_to='documentos/', blank=True, null=True)
    doc4 = models.FileField(upload_to='documentos/', blank=True, null=True)
    doc5 = models.FileField(upload_to='documentos/', blank=True, null=True)
    doc6 = models.FileField(upload_to='documentos/', blank=True, null=True)
    doc7 = models.FileField(upload_to='documentos/', blank=True, null=True)
    doc8 = models.FileField(upload_to='documentos/', blank=True, null=True)
    doc9 = models.FileField(upload_to='documentos/', blank=True, null=True)
    doc10 = models.FileField(upload_to='documentos/', blank=True, null=True)
    doc11 = models.FileField(upload_to='documentos/', blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'ficha_aspirante'

class Instructor(models.Model):
    iden_instr = models.IntegerField(primary_key=True)
    nomb_instr = models.CharField(max_length=60)
    corr_instr = models.CharField(max_length=65)
    ciud_instr = models.CharField(max_length=45, blank=True, null=True)
    tele_instr = models.CharField(max_length=45, blank=True, null=True)
    resu_instr = models.CharField(max_length=500, blank=True, null=True)
    carg_instr = models.CharField(max_length=45, blank=True, null=True)
    cent_instr = models.CharField(max_length=100, blank=True, null=True)
    foto_instr = models.ImageField(upload_to='instructor/')

    class Meta:
        managed = False
        db_table = 'instructor'


class Mensaje(models.Model):
    iden_mensa = models.AutoField(primary_key=True)
    nomb_mensa = models.CharField(max_length=60)
    apel_mensa = models.CharField(max_length=60)
    corr_mensa = models.CharField(max_length=60)
    mens_mensa = models.CharField(max_length=500)
    fech_mensa = models.DateField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'mensaje'



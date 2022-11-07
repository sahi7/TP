from django.db import models
from django.core.validators import RegexValidator
import math, random


class academicSession(models.Model):
	session_start_year = models.DateField()	#%Y-%m-%d
	session_end_year = models.DateField()

	class Meta:
		ordering = ('session_start_year',)

	def __str__(self):
		return self.session_start_year


class Level(models.Model):
	name = models.CharField(max_length=7)

	class Meta:
		ordering = ('name',)

	def __str__(self):
		return self.name


class Department(models.Model):
	name = models.CharField(max_length=100, editable=True)
	code = models.CharField(max_length=15, editable=True)
	level = models.ForeignKey(Level, on_delete=models.CASCADE)

	class Meta:
		ordering = ('name',)

	def __str__(self):
		return self.name


class Option(models.Model):
	name = models.CharField(max_length=150)
	code = models.CharField(max_length=10)
	department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="departments")

	class Meta:
		ordering = ('name',)

	def __str__(self):
		return self.name 


class Town(models.Model):
	name = models.CharField(max_length=75)

	class Meta:
		ordering = ('name',)

	def __str__(self):
		return self.name


class School(models.Model):
	name = models.CharField(max_length=150)
	num_of_sudent = models.IntegerField(default=1)
	town = models.ForeignKey(Town, null=True, on_delete=models.CASCADE)
	

	class Meta:
		ordering = ('name',)

	def __str__(self):
		return self.name


class SchoolDept(models.Model):
	name = models.CharField(max_length=100)
	school = models.ForeignKey(School, on_delete=models.CASCADE)

	class Meta:
		ordering = ('name',)

	def __str__(self):
		return self.name


class Student(models.Model):
	telephone_regex = RegexValidator(
        regex="^[0-9]{9,13}$", message="Entered mobile number isn't in a right format!"
    )
	name = models.CharField(max_length=500)
	matricule = models.CharField(max_length=10, unique=True)
	tp_code =  models.CharField(max_length=8, unique=True)
	telephone = models.CharField(validators=[telephone_regex], max_length=9)
	level = models.ForeignKey(Level, null=True, on_delete=models.SET_NULL)
	department = models.ForeignKey(Department, null=True, on_delete=models.CASCADE)
	option = models.ForeignKey(Option, null=True, on_delete=models.DO_NOTHING, related_name="options")
	school = models.ForeignKey(School, null=True, on_delete=models.CASCADE)
	school_dept = models.ForeignKey(SchoolDept, null=True, on_delete=models.CASCADE)
	academic_session = models.ForeignKey(academicSession, null=True, on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ('-created_at',)

	def save(self, *args, **kwargs):
		if self.pk is None:
			self.tp_code = self.genTpCode()
		self.matricule = self.matricule.upper()
		super(Student, self).save(*args, **kwargs)

	def genTpCode(self):
		uniqueOBJ = self.matricule + self.telephone
		TpCode = ""
		length = len(uniqueOBJ)
		for i in range(8):
			TpCode += uniqueOBJ[math.floor(random.random() * length)]
		return TpCode.upper()

	def __str__(self):
		return self.name or ''
		







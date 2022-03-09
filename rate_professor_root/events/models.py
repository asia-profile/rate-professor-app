from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
#from djangoratings.fields import RatingField

# Create your models here.
# is the order correct? to create module we need student and professor, but for student we need module and same of professor...
# okay now tried sth like this
class Student(models.Model):
    username = models.CharField('Student Username', max_length=30)
    email = models.EmailField('Student Email', unique=True)
    password = models.CharField('Student Password', max_length=120)
    # modules = models.ManyToManyField(Module, blank=True) #modules taken by the student

    def __str__(self):
        return self.username


class Professor(models.Model):
    professor_id = models.CharField('Identifier of Professor', max_length=30, null=True)
    firstname = models.CharField('First Name of Professor', max_length=30,  null=True)
    lastname = models.CharField('Lastname of Professor', max_length=30,  null=True)
    # rating = models.IntegerField() #it is going to be calculated from all modules an
    # idk if I need this, or if I can just calculate this stuff and display it then
    #modules = models.ManyToManyField(Module, blank=True) # professor can be in multiple modules
    rating = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(5)])
    ratings_count = models.IntegerField(default=0) #amount of times professor was rated
    # rating = models.RatingField(range=5)  # 5 possible rating values, 1-5

    def __str__(self):
        return self.firstname + " " + self.lastname

    #def average_rating(self):
    #    if self.ratings_count!=0:
    #        average = self.rating/self.ratings_count
    #    else:
    #        average = 0
    #    return average


    #def average_module_rating(self):





class Module(models.Model):
    module_code = models.CharField('Module Code', max_length=120)
    name = models.CharField('Module Name', max_length=120)
    year = models.IntegerField()
    semester = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(2)])
    professors = models.ManyToManyField(Professor, blank=True)  # what professors teach the module
    students = models.ManyToManyField(Student, blank=True)  # students taking the module

    def get_professors(self):
        p = ' '
        for professor in self.professors.all():
            p = p + professor.professor_id + ' ' + professor.firstname + ' ' + professor.lastname + '\n'

        # remove the last '\n' and return the value.
        return p[:-1]

    def __str__(self):
        return self.code + " " + self.name



# need? a Rating model? with name of person who gave it, name of professor and a module name
# I guess this is good? tho is it too manu foreignkeys...?


class Rating (models.Model):
    #student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    module = models.ForeignKey(Module,  on_delete=models.CASCADE)
    professor_id = models.CharField('Identifier of Professor', max_length=30, null=True)
    #professor_id = models.ForeignKey(Professor,  on_delete=models.CASCADE)
    # professor_id = models.ForeignKey(Professor, on_delete=models.CASCADE)
    # possible change needed? will see
    #add the year and the semester? no, I think it's good as it is
    rating = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(5)])


    def __str__(self):
        return self.rating_num

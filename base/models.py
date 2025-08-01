from django.db import models

class Birthday(models.Model):
    emp_name = models.CharField(max_length=50)
    emp_code = models.IntegerField(unique=True)
    dob = models.DateField()
    img = models.ImageField(upload_to='photos')

    def __str__(self):
        return self.emp_name
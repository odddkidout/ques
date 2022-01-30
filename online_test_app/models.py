from django.db import models

# Create your models here.
class FileObject(models.Model):
    file = models.FileField(upload_to='files/')
   
    def __str__(self):
        return str(self.file)

class QuestionAnswerModel(models.Model):
    user_name = models.CharField(max_length=30,blank=True)
    qNum = models.IntegerField()
    mainQ = models.TextField()
    subQuestion1 = models.CharField(max_length=2000,blank=True)
    subQuestion2 = models.CharField(max_length=2000,blank=True)
    subQuestion3 = models.CharField(max_length=2000,blank=True)
    subQuestion4 = models.CharField(max_length=2000,blank=True)
    ans1 = models.CharField(max_length=2000,blank=True)
    ans2 = models.CharField(max_length=2000,blank=True)
    ans3 = models.CharField(max_length=2000,blank=True)
    ans4 = models.CharField(max_length=2000,blank=True)
    selected_answer = models.CharField(max_length=2000,blank=True)

class AnswerModel(models.Model):
    qNum = models.IntegerField(blank=True)
    answer = models.CharField(max_length=6,blank=True)
    
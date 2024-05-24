from django.db import models

# Create your models here.


class studentInfo(models.Model):
    studID = models.IntegerField(primary_key=True)
    lrn = models.CharField(max_length = 12)
    lastname = models.CharField(max_length = 100)
    firstname = models.CharField( max_length = 100)
    middlename = models.CharField(max_length = 50)
    degree = models.CharField(max_length = 150)
    yearlvl = models.CharField(max_length = 10)
    sex = models.CharField(max_length = 10)
    emailadd = models.EmailField()
    contact = models.CharField(max_length = 11)

    def __str__(self):
        return f"{self.studID} {self.lastname} {self.firstname}"
    
    class Meta:
        ordering = ['lastname']  # Specify the default ordering herea


class RequestedGMC(models.Model):
    student = models.ForeignKey(studentInfo, on_delete=models.CASCADE)
    reason = models.TextField()
    or_num = models.CharField(max_length=100, null=True, blank=True)
    request_date = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)  # Add this field
    
    def __str__(self):
        return f"GMC Request for {self.student} - {self.reason}"
        
class Schedule(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()

    def __str__(self):
        return self.title

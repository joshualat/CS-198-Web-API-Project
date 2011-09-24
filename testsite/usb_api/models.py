from django.db import models

GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
)

class USBUser(models.Model):
    #required fields
    usb_code = models.CharField(max_length=1000)
    username = models.CharField(max_length=100)
    password_code = models.CharField(max_length=1000)
    shared_key = models.CharField(max_length=1000)
    public_key = models.CharField(max_length=1000)
    salt = models.CharField(max_length=100)
    one_time_password = models.CharField(max_length=1000)

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    sex = models.CharField(max_length=1, choices=GENDER_CHOICES)
    birthdate = models.DateTimeField()

    #optional fields
    address = models.CharField(max_length=200)
    contact_number = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    #automatic fields
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    last_login = models.DateTimeField(auto_now_add=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    def is_registered(self):
        if self.username == "":
            return False
        return True

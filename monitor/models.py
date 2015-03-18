from django.db import models

class Beer(models.Model):
    
    beer_text = models.CharField('Beer',max_length=30)
    brew_date = models.DateField('Brew Date',blank=True,null=True)
    bottle_date = models.DateField('Bottle Date',blank=True,null=True)
    
    def __str__(self):
        return self.beer_text
    
class Reading(models.Model):

    temp_choices = (
        ('F', 'Fahrenheit'),
        ('C', 'Celcius'),
    )

    beer = models.ForeignKey(Beer)
    instant = models.DateTimeField('Instant',auto_now_add=True)
    instant_override = models.DateTimeField('Instant Override',blank=True,
                                            null=True,default=None)
    instant_actual = models.DateTimeField('Instant Actual',blank=True,
                                            null=True,default=None)
    light_amb = models.DecimalField('Ambient Light', max_digits=5,
                                    decimal_places=2,blank=True,null=False,
                                    default=0)
    temp_amb = models.DecimalField('Ambient Temp',max_digits=5,
                                   decimal_places=2,blank=True,null=False,
                                    default=0)
    temp_beer = models.DecimalField('Beer Temp',max_digits=5,
                                    decimal_places=2,blank=True,null=False,
                                    default=0)
    temp_unit = models.CharField('Temp Unit',max_length=1,
                                 choices=temp_choices,default='F')
                                 
    error_flag = models.NullBooleanField('Error?')
    error_details = models.CharField('Error Details',blank=True,max_length=150)
    
	#Defunct after references removed from views.chart
    def func_instant_actual(self):
        if self.instant_override is not None:
            return self.instant_override
        else:
            return self.instant
            
	#Break out conversion into a new function, combine with get_temp_beer
    def get_temp_amb(self):
        if self.temp_unit is 'F' or self.temp_unit is None:
            return float(self.temp_amb)
        else:
            return float(self.temp_amb*9/5+32)
    
	#Break out conversion into a new function, combine with get_temp_amb
    def get_temp_beer(self):
        if self.temp_unit is 'F' or self.temp_unit is None:
            return float(self.temp_beer)
        else:
            return float(self.temp_beer*9/5+32)
    
	#Remove if/else once no legacy data without instant_actual exists
    def __str__(self):
        value = str(self.beer) + ': '
        if bool(self.instant_actual):        
            value = value + str(self.instant_actual.strftime("%Y-%m-%d %H:%M:%S"))
        else:
            value = value + str(self.instant.strftime("%Y-%m-%d %H:%M:%S"))
        return value
        
    def save(self, *args, **kwargs):
        
        super(Reading, self).save(*args, **kwargs)
        
        #Set instant_actual before each save            
        if bool(self.instant_override):
            self.instant_actual = self.instant_override
        else:
            self.instant_actual = self.instant

        super(Reading, self).save(*args, **kwargs)

class Config(models.Model):
    
    beer = models.ForeignKey(Beer)
    temp_amb_base = models.DecimalField('Ambient Temp Baseline', max_digits=5,
                                        decimal_places=2,blank=True,null=True,
                                        default=None)
    temp_amb_dev = models.DecimalField('Ambient Temp Deviation', max_digits=5,
                                       decimal_places=2,blank=True,null=True,
                                       default=None)
    temp_beer_base = models.DecimalField('Beer Temp Baseline', max_digits=5,
                                         decimal_places=2,blank=True,null=True,
                                         default=None)
    temp_beer_dev = models.DecimalField('Ambient Temp Deviation', max_digits=5,
                                        decimal_places=2,blank=True,null=True,
                                        default=None)
                                        
    read_missing = models.PositiveIntegerField('Missing Reading Warning (minutes)',
                                               default=0)
    read_last_instant = models.DateTimeField('Last Reading Instant',blank=True,
                                null=True,default=None)
                                        
    email_enable = models.BooleanField('Enable Email?',default=False)
    email_timeout = models.PositiveIntegerField('Email Timeout (minutes)',
                                                default=60)
    email_api_key = models.CharField("API Key",default='',blank=True,
                                     max_length=50)    
    email_sender = models.CharField("From",default='',blank=True,max_length=50)
    email_to = models.CharField("To",default='',blank=True,max_length=150)
    email_subject = models.CharField("Subject",default='',blank=True,
                                     max_length=150)
    email_last_instant = models.DateTimeField('Last Email Instant',blank=True,
                                null=True,default=None)
        
    def __str__(self):
        return 'Config' + ': ' + str(self.pk)
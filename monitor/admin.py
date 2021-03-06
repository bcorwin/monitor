from django.contrib import admin
from monitor.models import Beer, Reading, Config, Archive, Event

class ReadingInLine(admin.TabularInline):
    model = Reading
    extra = 1

    fields = ('instant', 'instant_override','instant_actual','light_amb', 'pres_beer',
              'temp_amb', 'temp_beer', 'temp_unit', 'error_flag', 'error_details')
    readonly_fields = ('instant','instant_actual')

class BeerAdmin(admin.ModelAdmin):
    fieldsets = [
        ('General Information', {'fields': [('beer_text','beer_type'),'brewer']}),
        ('Brew Details', {'fields': [('brew_date','brew_sg','brew_temp'),'brew_notes']}),
        ('Bottle Details', {'fields': [('bottle_date','bottle_sg','bottle_temp'),('sugar_amount','bottle_count'),'bottle_notes']}),
        ('Other Details', {'fields': [('pull_date','max_abv'),'other_notes']}),
        ('Sensor Modifiers',    {'fields': [('temp_amb_mod','light_amb_mod'),('temp_beer_mod','pres_beer_mod')]})
    ]
    #inlines = [ReadingInLine]
    readonly_fields = ('max_abv',)

class ReadingAdmin(admin.ModelAdmin):
    fieldsets = [
    ('Instant',    {'fields': ['instant','instant_override','instant_actual','version']}),
    ('Data',       {'fields': ['beer',('temp_amb','light_amb'),('temp_beer','pres_beer'),
                               'temp_unit']}),
    ('Errors',     {'fields': ['error_flag','error_details']}),
    ]

    readonly_fields = ('instant','instant_actual','version')

class ArchiveAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Archive Info', {'fields': ['beer','reading_date','count','update_instant']}),
        ('Data', {'fields': ['instant_actual','light_amb','pres_beer','temp_amb','temp_beer','event_temp_amb','event_temp_beer']})
    ]

    readonly_fields = ('beer','reading_date','count','instant_actual',
                       'light_amb','pres_beer','temp_amb','temp_beer',
                       'event_temp_amb','event_temp_beer','update_instant')

class ConfigAdmin(admin.ModelAdmin):
    fields = ('beer','temp_amb_base','temp_amb_dev','temp_beer_base','temp_beer_dev',
              'read_missing','read_last_instant','email_enable','email_timeout',
              'email_api_key','email_sender','email_to','email_subject',
              'email_last_instant','api_server_url','api_prod_key','api_test_key',)

    readonly_fields = ('read_last_instant','reading_key','archive_key')

admin.site.register(Beer, BeerAdmin)
admin.site.register(Config, ConfigAdmin)
admin.site.register(Reading,ReadingAdmin)
admin.site.register(Archive,ArchiveAdmin)
admin.site.register(Event)
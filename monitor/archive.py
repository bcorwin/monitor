from monitor.models import Archive

import matplotlib.dates as mpld

def getAllArchives(active_beer):
    all_archives = None
    try:
        all_archives = Archive.objects.filter(beer=active_beer)
    finally:
        return all_archives

def getArchive(active_beer, day):
    active_archive = None    
    try:
        active_archive = Archive.objects.get(beer=active_beer, reading_date=day)
    finally:
        return active_archive

def createArchive(active_beer, day):
    archive = None
    try:
        if not bool(getArchive(active_beer, day)):
            archive = Archive(beer=active_beer, reading_date=day)
            archive.save()
    finally:
        return archive
    
def updateArchive(archive, reading):
    result = None
    try:
        archive.instant_actual += str(mpld.date2num(reading.instant_actual)) + '^'
        archive.light_amb += str(reading.get_light_amb()) + '^'
        archive.pres_beer += str(reading.get_pres_beer()) + '^'
        archive.temp_amb += str(reading.get_temp_amb()) + '^'
        archive.temp_beer += str(reading.get_temp_beer()) + '^'
        archive.count += 1
        archive.save()
        reading.delete()
        result = True
    finally:
        return result

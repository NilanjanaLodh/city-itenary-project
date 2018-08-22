##python 3
import os,system

bad_sites = [
    'ChIJBw12GwJZwokRCoPEwRCi3G0',
    'ChIJs6UWAT1awokRQopDDN7vSwo',
    'ChIJJ7AvWDhDXz4RgtxWx69mLkk',
    'ChIJIQ98ZdRCXz4RM1n-zZxl7CA',
    'ChIJRcbZaklDXz4RYlEphFBu5r0',
    'ChIJk0n7n6zAwoARDT89ZsTyZvw',
    'ChIJY-otQbHHwoARFLxG5thhkC4',
    'ChIJg6_eOxHsC0ER6zlGwyHtcFk',
    'ChIJlTr0NSVu5kcR-Zf_HVedVq8',
    'ChIJUeiI4P9x5kcRqEwHl6V32GQ',
    'ChIJ-xLGm-OZ4jAR9ybBn23dTtc',
    'ChIJM2HqLK-f4jARj_xwApEvCok',
    'ChIJI6YDVQOZ4jARjo2Hah2dwYE',
    'ChIJWXlWGearQjQRNEj80OdQoVw',
    'ChIJmX9y62OpQjQRufPZ_fJir5k',
    'ChIJwz8uNM4adkgRpTiaG4dntQA',
    'ChIJk0n7n6zAwoARDT89ZsTyZvw',
    'ChIJITjJkkzGwoAR35tUi0GRxKA',
    'ChIJg6_eOxHsC0ER6zlGwyHtcFk',
    'ChIJDZwOpjgGBDQR9_QB80jKj6s'
]

for site in bad_sites:
    os.system("find . -name '{}' | xargs -I '$' cat '$'/info.json".format(site))
    opt = input('\ny/n? ');
    if opt == 'y':
        os.system("find . -name '{}' | xargs -I '$' rm -r '$'".format(site))

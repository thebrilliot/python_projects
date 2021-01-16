# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 10:40:17 2020

Used Car Part Price Scraper

@author: lando
"""

import re
from datetime import date
from urllib.request import urlopen
from bs4 import BeautifulSoup as soup

# 2010 Jeep Wrangler - Fuel Pump
#sample_url = 'https://www.car-part.com/cgi-bin/search.cgi?userSearch=int&userPID=1000&userLocation=USA&userIMS=&userInterchange=EA%3F&userSide=&userDate=2010&userDate2=2010&dbModel=37.14.1.1&userModel=Jeep%20Wrangler&dbPart=323.1&userPart=Fuel%20Pump&sessionID=13000000084163931&sURL=www.car-part.com&userPreference=year&userIntSelect=2540939&userUID=0&userBroker=&iKey=&userPage=55'

# 2010 Toyota Corolla - Fuel Pump
#sample_url = 'https://www.car-part.com/cgi-bin/search.cgi?userSearch=int&userPID=1000&userLocation=USA&userIMS=&userInterchange=B%3DAA%40&userSide=&userDate=2010&userDate2=2010&dbModel=73.7.1.1&userModel=Toyota%20Corolla&dbPart=323.1&sessionID=13000000084292690&sURL=www.car-part.com&userPreference=year&userIntSelect=601547&userUID=0&userBroker=&iKey=&userPage=88'

# 2010 Mazda Miata - Fuel Pump
#sample_url = 'https://www.car-part.com/cgi-bin/search.cgi?userSearch=int&userPID=1000&userLocation=USA&userIMS=&userInterchange=B%3D%3EAF&userSide=&userDate=2010&userDate2=2010&dbModel=48.12.1.1&userModel=Mazda%20Miata%20MX5&dbPart=323.1&userPart=Fuel%20Pump&sessionID=14000000073810189&sURL=www.car-part.com&userPreference=year&userIntSelect=1499122&userUID=0&userBroker=&iKey=&userPage=13'

# 2010 Nissan Frontier - Fuel Pump
#sample_url = 'https://www.car-part.com/cgi-bin/search.cgi?userSearch=int&userPID=1000&userLocation=USA&userIMS=&userInterchange=BFA%3DC&userSide=&userDate=2010&userDate2=2010&dbModel=54.23.1.1&userModel=Nissan%20Frontier&dbPart=323.1&userPart=Fuel%20Pump&sessionID=14000000073810982&sURL=www.car-part.com&userPreference=year&userIntSelect=1041205&userUID=0&userBroker=&iKey=&userPage=146'

# 2010 Volkwagen Bug - Fuel Pump
#sample_url = 'https://www.car-part.com/cgi-bin/search.cgi?userSearch=int&userPID=1000&userLocation=USA&userIMS=&userInterchange=%3E%3D%3D%3D%3E&userSide=&userDate=2010&userDate2=2010&dbModel=75.3.1.1&userModel=Volkswagen%20Beetle%2FBug&dbPart=323.1&userPart=Fuel%20Pump&sessionID=13000000084308412&sURL=www.car-part.com&userPreference=year&userIntSelect=200759&userUID=0&userBroker=&iKey=&userPage=8'

# 2010 Chevy Truck-Silverado 2500 - Fuel Pump (gas, 6' 6")
#sample_url = 'https://www.car-part.com/cgi-bin/search.cgi?userSearch=int&userPID=1000&userLocation=USA&userIMS=&userInterchange=CEA&userSide=&userDate=2010&userDate2=2010&dbModel=15.28.35.35&userModel=Chevy%20Truck-Silverado%202500%20(1999%20Up)&dbPart=323.1&userPart=Fuel%20Pump&sessionID=13000000084312119&sURL=www.car-part.com&userPreference=year&userIntSelect=2211691&userUID=0&userBroker=&iKey=&userPage=12'
# 2010 Chevy Truck-Silverado 2500 - Fuel Pump (gas, 8')
#sample_url = 'https://www.car-part.com/cgi-bin/search.cgi?userSearch=int&userPID=1000&userLocation=USA&userIMS=&userInterchange=CEC&userSide=&userDate=2010&userDate2=2010&dbModel=15.28.35.35&userModel=Chevy%20Truck-Silverado%202500%20(1999%20Up)&dbPart=323.1&userPart=Fuel%20Pump&sessionID=13000000084312517&sURL=www.car-part.com&userPreference=year&userIntSelect=2211692&userUID=0&userBroker=&iKey=&userPage=17'

# 2010 Ford Crown Victoria - Fuel Pump
#sample_url = 'https://www.car-part.com/cgi-bin/search.cgi?userSearch=int&userPID=1000&userLocation=USA&userIMS=&userInterchange=%3EC%3FB&userSide=&userDate=2010&userDate2=2010&dbModel=27.1.3.3&userModel=Ford%20Crown%20Vic%20(1983%20Up)&dbPart=323.1&userPart=Fuel%20Pump&sessionID=14000000073816159&sURL=www.car-part.com&userPreference=year&userIntSelect=640085&userUID=0&userBroker=&iKey=&userPage=15'

# 2010 Honda Accord - Fuel Pump (3.5L, California)
#sample_url = 'https://www.car-part.com/cgi-bin/search.cgi?userSearch=int&userPID=1000&userLocation=USA&userIMS=&userInterchange=B%3D%40C%3F&userSide=&userDate=2010&userDate2=2010&dbModel=30.3.1.1&userModel=Honda%20Accord&dbPart=323.1&userPart=Fuel%20Pump&sessionID=14000000073818005&sURL=www.car-part.com&userPreference=year&userIntSelect=54874&userUID=0&userBroker=&iKey=&userPage=9'

# 2010 Hyundai Elantra - Fuel Pump
#sample_url = 'https://www.car-part.com/cgi-bin/search.cgi?userSearch=int&userPID=1000&userLocation=USA&userIMS=&userInterchange=B%3D%3FD%3D&userSide=&userDate=2010&userDate2=2010&dbModel=32.3.1.1&userModel=Hyundai%20Elantra&dbPart=323.1&userPart=Fuel%20Pump&sessionID=14000000073818562&sURL=www.car-part.com&userPreference=year&userIntSelect=785472&userUID=0&userBroker=&iKey=&userPage=62'

# 2010 Jeep Wrangler - A/C Compressor Assembly
#sample_url = 'https://www.car-part.com/cgi-bin/search.cgi?userSearch=int&userPID=1000&userLocation=USA&userIMS=&userInterchange=%3F%3EE&userSide=&userDate=2010&userDate2=2010&dbModel=37.14.1.1&userModel=Jeep%20Wrangler&dbPart=682.1&userPart=A%2FC%20Compressor&sessionID=14000000074168524&sURL=www.car-part.com&userPreference=year&userIntSelect=2543985&userUID=0&userBroker=&iKey=&userPage=35'

# 2010 Toyota Corolla - A/C Compressor Assembly
#sample_url = 'https://www.car-part.com/cgi-bin/search.cgi?userSearch=int&userPID=1000&userLocation=USA&userIMS=&userInterchange=B%3D%3FFA&userSide=&userDate=2010&userDate2=2010&dbModel=73.7.1.1&userModel=Toyota%20Corolla&dbPart=682.1&userPart=A%2FC%20Compressor&sessionID=14000000074158893&sURL=www.car-part.com&userPreference=year&userIntSelect=607588&userUID=0&userBroker=&iKey=&userPage=26'

# 2010 Mazda Miata = A/C Compressor Assembly
#sample_url = 'https://www.car-part.com/cgi-bin/search.cgi?userSearch=int&userPID=1000&userLocation=USA&userIMS=&userInterchange=B%3D%3E%3EF&userSide=&userDate=2010&userDate2=2010&dbModel=48.12.1.1&userModel=Mazda%20Miata%20MX5&dbPart=682.1&userPart=A%2FC%20Compressor&sessionID=14000000074168910&sURL=www.car-part.com&userPreference=year&userIntSelect=1501087&userUID=0&userBroker=&iKey=&userPage=12'

# 2010 Nissan Frontier - A/C Compressor Assembly (6 cyl)
#sample_url = 'https://www.car-part.com/cgi-bin/search.cgi?userSearch=int&userPID=1000&userLocation=USA&userIMS=&userInterchange=BF%3DFA&userSide=&userDate=2010&userDate2=2010&dbModel=54.23.1.1&userModel=Nissan%20Frontier&dbPart=682.1&userPart=A%2FC%20Compressor&sessionID=14000000074169326&sURL=www.car-part.com&userPreference=year&userIntSelect=1044363&userUID=0&userBroker=&iKey=&userPage=86'

# 2010 Volkwagen Bug - A/C Compressor Assembly
#sample_url = 'https://www.car-part.com/cgi-bin/search.cgi?userSearch=int&userPID=1000&userLocation=USA&userIMS=&userInterchange=B%3D%3EB%3D&userSide=&userDate=2010&userDate2=2010&dbModel=75.3.1.1&userModel=Volkswagen%20Beetle%2FBug&dbPart=682.1&userPart=A%2FC%20Compressor&sessionID=14000000074169943&sURL=www.car-part.com&userPreference=year&userIntSelect=204191&userUID=0&userBroker=&iKey=&userPage=17'

# 2010 Chevrolet Silverado - A/C Compressor Assembly (the 2500, diesel)
#sample_url = 'https://www.car-part.com/cgi-bin/search.cgi?userSearch=int&userPID=1000&userLocation=USA&userIMS=&userInterchange=CAB&userSide=&userDate=2010&userDate2=2010&dbModel=15.28.35.35&userModel=Chevy%20Truck-Silverado%202500%20(1999%20Up)&dbPart=682.1&userPart=A%2FC%20Compressor&sessionID=14000000074170369&sURL=www.car-part.com&userPreference=year&userIntSelect=2215806&userUID=0&userBroker=&iKey=&userPage=182'

# 2002 Ford Explorer - A/C Compressor Assembly (6 cyl, 4 dr, Sport Trac)
#sample_url = 'https://www.car-part.com/cgi-bin/search.cgi?userSearch=int&userPID=1000&userLocation=USA&userIMS=&userInterchange=CA%3D&userSide=&userDate=2002&userDate2=2002&dbModel=27.15.1.1&userModel=Ford%20Explorer&dbPart=682.1&userPart=A%2FC%20Compressor&sessionID=14000000074171421&sURL=www.car-part.com&userPreference=year&userIntSelect=859725&userUID=0&userBroker=&iKey=&userPage=268'

# 2002 Ford Crown Victoria - A/C Compressor Assembly
#sample_url = 'https://www.car-part.com/cgi-bin/search.cgi?userSearch=int&userPID=1000&userLocation=USA&userIMS=&userInterchange=B%3F%40&userSide=&userDate=2002&userDate2=2002&dbModel=27.1.3.3&userModel=Ford%20Crown%20Vic%20(1983%20Up)&dbPart=682.1&userPart=A%2FC%20Compressor&sessionID=13000000084672981&sURL=www.car-part.com&userPreference=year&userIntSelect=642724&userUID=0&userBroker=&iKey=&userPage=101'

# 2002 Honda Accord - A/C Compressor Assembly
#sample_url = 'https://www.car-part.com/cgi-bin/search.cgi?userSearch=int&userPID=1000&userLocation=USA&userIMS=&userInterchange=BEDEA&userSide=&userDate=2002&userDate2=2002&dbModel=30.3.1.1&userModel=Honda%20Accord&dbPart=682.1&userPart=A%2FC%20Compressor&sessionID=14000000074176116&sURL=www.car-part.com&userPreference=year&userIntSelect=62592&userUID=0&userBroker=&iKey=&userPage=112'

# 2010 Honda Accord - A/C Compressor Assembly
#sample_url = 'https://www.car-part.com/cgi-bin/search.cgi?userSearch=int&userPID=1000&userLocation=USA&userIMS=&userInterchange=B%3D%3FB%40N&userSide=&userDate=2010&userDate2=2010&dbModel=30.3.1.1&userModel=Honda%20Accord&dbPart=682.1&userPart=A%2FC%20Compressor&sessionID=14000000074181245&sURL=www.car-part.com&userPreference=year&userIntSelect=62598&userUID=0&userBroker=&iKey=&userPage=39'

# 2010 Hyundai Elantra - A/C Compressor Assembly
#sample_url = 'https://www.car-part.com/cgi-bin/search.cgi?userSearch=int&userPID=1000&userLocation=USA&userIMS=&userInterchange=B%3D%40%3E%3F&userSide=&userDate=2010&userDate2=2010&dbModel=32.3.1.1&userModel=Hyundai%20Elantra&dbPart=682.1&userPart=A%2FC%20Compressor&sessionID=14000000074181618&sURL=www.car-part.com&userPreference=year&userIntSelect=789563&userUID=0&userBroker=&iKey=&userPage=56'

# 2010 Ford Explorer - A/C Compressor Assembly (w/aux heat, 6 cyl)
#sample_url = 'https://www.car-part.com/cgi-bin/search.cgi?userSearch=int&userPID=1000&userLocation=USA&userIMS=&userInterchange=%3E%40C&userSide=&userDate=2010&userDate2=2010&dbModel=27.15.1.1&userModel=Ford%20Explorer&dbPart=682.1&userPart=A%2FC%20Compressor&sessionID=13000000085313943&sURL=www.car-part.com&userPreference=year&userIntSelect=859730&userUID=0&userBroker=&iKey=&userPage=37'

# 2010 Ford Explorer - Fuel Pump
#sample_url = 'https://www.car-part.com/cgi-bin/search.cgi?userSearch=int&userPID=1000&userLocation=USA&userIMS=&userInterchange=F%3DE&userSide=&userDate=2010&userDate2=2010&dbModel=27.15.1.1&userModel=Ford%20Explorer&dbPart=323.1&userPart=Fuel%20Pump&sessionID=13000000085314813&sURL=www.car-part.com&userPreference=year&userIntSelect=853474&userUID=0&userBroker=&iKey=&userPage=19'

urls = ['https://www.car-part.com/cgi-bin/search.cgi?userSearch=int&userPID=1000&userLocation=USA&userIMS=&userInterchange=EA%3F&userSide=&userDate=2010&userDate2=2010&dbModel=37.14.1.1&userModel=Jeep%20Wrangler&dbPart=323.1&userPart=Fuel%20Pump&sessionID=13000000084163931&sURL=www.car-part.com&userPreference=year&userIntSelect=2540939&userUID=0&userBroker=&iKey=&userPage=55',
        'https://www.car-part.com/cgi-bin/search.cgi?userSearch=int&userPID=1000&userLocation=USA&userIMS=&userInterchange=B%3DAA%40&userSide=&userDate=2010&userDate2=2010&dbModel=73.7.1.1&userModel=Toyota%20Corolla&dbPart=323.1&sessionID=13000000084292690&sURL=www.car-part.com&userPreference=year&userIntSelect=601547&userUID=0&userBroker=&iKey=&userPage=88',
        'https://www.car-part.com/cgi-bin/search.cgi?userSearch=int&userPID=1000&userLocation=USA&userIMS=&userInterchange=B%3D%3EAF&userSide=&userDate=2010&userDate2=2010&dbModel=48.12.1.1&userModel=Mazda%20Miata%20MX5&dbPart=323.1&userPart=Fuel%20Pump&sessionID=14000000073810189&sURL=www.car-part.com&userPreference=year&userIntSelect=1499122&userUID=0&userBroker=&iKey=&userPage=13',
        'https://www.car-part.com/cgi-bin/search.cgi?userSearch=int&userPID=1000&userLocation=USA&userIMS=&userInterchange=BFA%3DC&userSide=&userDate=2010&userDate2=2010&dbModel=54.23.1.1&userModel=Nissan%20Frontier&dbPart=323.1&userPart=Fuel%20Pump&sessionID=14000000073810982&sURL=www.car-part.com&userPreference=year&userIntSelect=1041205&userUID=0&userBroker=&iKey=&userPage=146',
        'https://www.car-part.com/cgi-bin/search.cgi?userSearch=int&userPID=1000&userLocation=USA&userIMS=&userInterchange=%3E%3D%3D%3D%3E&userSide=&userDate=2010&userDate2=2010&dbModel=75.3.1.1&userModel=Volkswagen%20Beetle%2FBug&dbPart=323.1&userPart=Fuel%20Pump&sessionID=13000000084308412&sURL=www.car-part.com&userPreference=year&userIntSelect=200759&userUID=0&userBroker=&iKey=&userPage=8',
        'https://www.car-part.com/cgi-bin/search.cgi?userSearch=int&userPID=1000&userLocation=USA&userIMS=&userInterchange=CEA&userSide=&userDate=2010&userDate2=2010&dbModel=15.28.35.35&userModel=Chevy%20Truck-Silverado%202500%20(1999%20Up)&dbPart=323.1&userPart=Fuel%20Pump&sessionID=13000000084312119&sURL=www.car-part.com&userPreference=year&userIntSelect=2211691&userUID=0&userBroker=&iKey=&userPage=12',
        'https://www.car-part.com/cgi-bin/search.cgi?userSearch=int&userPID=1000&userLocation=USA&userIMS=&userInterchange=CEC&userSide=&userDate=2010&userDate2=2010&dbModel=15.28.35.35&userModel=Chevy%20Truck-Silverado%202500%20(1999%20Up)&dbPart=323.1&userPart=Fuel%20Pump&sessionID=13000000084312517&sURL=www.car-part.com&userPreference=year&userIntSelect=2211692&userUID=0&userBroker=&iKey=&userPage=17',
        'https://www.car-part.com/cgi-bin/search.cgi?userSearch=int&userPID=1000&userLocation=USA&userIMS=&userInterchange=%3EC%3FB&userSide=&userDate=2010&userDate2=2010&dbModel=27.1.3.3&userModel=Ford%20Crown%20Vic%20(1983%20Up)&dbPart=323.1&userPart=Fuel%20Pump&sessionID=14000000073816159&sURL=www.car-part.com&userPreference=year&userIntSelect=640085&userUID=0&userBroker=&iKey=&userPage=15',
        'https://www.car-part.com/cgi-bin/search.cgi?userSearch=int&userPID=1000&userLocation=USA&userIMS=&userInterchange=B%3D%40C%3F&userSide=&userDate=2010&userDate2=2010&dbModel=30.3.1.1&userModel=Honda%20Accord&dbPart=323.1&userPart=Fuel%20Pump&sessionID=14000000073818005&sURL=www.car-part.com&userPreference=year&userIntSelect=54874&userUID=0&userBroker=&iKey=&userPage=9',
        'https://www.car-part.com/cgi-bin/search.cgi?userSearch=int&userPID=1000&userLocation=USA&userIMS=&userInterchange=B%3D%3FD%3D&userSide=&userDate=2010&userDate2=2010&dbModel=32.3.1.1&userModel=Hyundai%20Elantra&dbPart=323.1&userPart=Fuel%20Pump&sessionID=14000000073818562&sURL=www.car-part.com&userPreference=year&userIntSelect=785472&userUID=0&userBroker=&iKey=&userPage=62',
        'https://www.car-part.com/cgi-bin/search.cgi?userSearch=int&userPID=1000&userLocation=USA&userIMS=&userInterchange=%3F%3EE&userSide=&userDate=2010&userDate2=2010&dbModel=37.14.1.1&userModel=Jeep%20Wrangler&dbPart=682.1&userPart=A%2FC%20Compressor&sessionID=14000000074168524&sURL=www.car-part.com&userPreference=year&userIntSelect=2543985&userUID=0&userBroker=&iKey=&userPage=35',
        'https://www.car-part.com/cgi-bin/search.cgi?userSearch=int&userPID=1000&userLocation=USA&userIMS=&userInterchange=B%3D%3FFA&userSide=&userDate=2010&userDate2=2010&dbModel=73.7.1.1&userModel=Toyota%20Corolla&dbPart=682.1&userPart=A%2FC%20Compressor&sessionID=14000000074158893&sURL=www.car-part.com&userPreference=year&userIntSelect=607588&userUID=0&userBroker=&iKey=&userPage=26',
        'https://www.car-part.com/cgi-bin/search.cgi?userSearch=int&userPID=1000&userLocation=USA&userIMS=&userInterchange=B%3D%3E%3EF&userSide=&userDate=2010&userDate2=2010&dbModel=48.12.1.1&userModel=Mazda%20Miata%20MX5&dbPart=682.1&userPart=A%2FC%20Compressor&sessionID=14000000074168910&sURL=www.car-part.com&userPreference=year&userIntSelect=1501087&userUID=0&userBroker=&iKey=&userPage=12',
        'https://www.car-part.com/cgi-bin/search.cgi?userSearch=int&userPID=1000&userLocation=USA&userIMS=&userInterchange=BF%3DFA&userSide=&userDate=2010&userDate2=2010&dbModel=54.23.1.1&userModel=Nissan%20Frontier&dbPart=682.1&userPart=A%2FC%20Compressor&sessionID=14000000074169326&sURL=www.car-part.com&userPreference=year&userIntSelect=1044363&userUID=0&userBroker=&iKey=&userPage=86',
        'https://www.car-part.com/cgi-bin/search.cgi?userSearch=int&userPID=1000&userLocation=USA&userIMS=&userInterchange=B%3D%3EB%3D&userSide=&userDate=2010&userDate2=2010&dbModel=75.3.1.1&userModel=Volkswagen%20Beetle%2FBug&dbPart=682.1&userPart=A%2FC%20Compressor&sessionID=14000000074169943&sURL=www.car-part.com&userPreference=year&userIntSelect=204191&userUID=0&userBroker=&iKey=&userPage=17',
        'https://www.car-part.com/cgi-bin/search.cgi?userSearch=int&userPID=1000&userLocation=USA&userIMS=&userInterchange=CAB&userSide=&userDate=2010&userDate2=2010&dbModel=15.28.35.35&userModel=Chevy%20Truck-Silverado%202500%20(1999%20Up)&dbPart=682.1&userPart=A%2FC%20Compressor&sessionID=14000000074170369&sURL=www.car-part.com&userPreference=year&userIntSelect=2215806&userUID=0&userBroker=&iKey=&userPage=182',
        'https://www.car-part.com/cgi-bin/search.cgi?userSearch=int&userPID=1000&userLocation=USA&userIMS=&userInterchange=CA%3D&userSide=&userDate=2002&userDate2=2002&dbModel=27.15.1.1&userModel=Ford%20Explorer&dbPart=682.1&userPart=A%2FC%20Compressor&sessionID=14000000074171421&sURL=www.car-part.com&userPreference=year&userIntSelect=859725&userUID=0&userBroker=&iKey=&userPage=268',
        'https://www.car-part.com/cgi-bin/search.cgi?userSearch=int&userPID=1000&userLocation=USA&userIMS=&userInterchange=B%3F%40&userSide=&userDate=2002&userDate2=2002&dbModel=27.1.3.3&userModel=Ford%20Crown%20Vic%20(1983%20Up)&dbPart=682.1&userPart=A%2FC%20Compressor&sessionID=13000000084672981&sURL=www.car-part.com&userPreference=year&userIntSelect=642724&userUID=0&userBroker=&iKey=&userPage=101',
        'https://www.car-part.com/cgi-bin/search.cgi?userSearch=int&userPID=1000&userLocation=USA&userIMS=&userInterchange=BEDEA&userSide=&userDate=2002&userDate2=2002&dbModel=30.3.1.1&userModel=Honda%20Accord&dbPart=682.1&userPart=A%2FC%20Compressor&sessionID=14000000074176116&sURL=www.car-part.com&userPreference=year&userIntSelect=62592&userUID=0&userBroker=&iKey=&userPage=112',
        'https://www.car-part.com/cgi-bin/search.cgi?userSearch=int&userPID=1000&userLocation=USA&userIMS=&userInterchange=B%3D%3FB%40N&userSide=&userDate=2010&userDate2=2010&dbModel=30.3.1.1&userModel=Honda%20Accord&dbPart=682.1&userPart=A%2FC%20Compressor&sessionID=14000000074181245&sURL=www.car-part.com&userPreference=year&userIntSelect=62598&userUID=0&userBroker=&iKey=&userPage=39',
        'https://www.car-part.com/cgi-bin/search.cgi?userSearch=int&userPID=1000&userLocation=USA&userIMS=&userInterchange=B%3D%40%3E%3F&userSide=&userDate=2010&userDate2=2010&dbModel=32.3.1.1&userModel=Hyundai%20Elantra&dbPart=682.1&userPart=A%2FC%20Compressor&sessionID=14000000074181618&sURL=www.car-part.com&userPreference=year&userIntSelect=789563&userUID=0&userBroker=&iKey=&userPage=56',
        'https://www.car-part.com/cgi-bin/search.cgi?userSearch=int&userPID=1000&userLocation=USA&userIMS=&userInterchange=%3E%40C&userSide=&userDate=2010&userDate2=2010&dbModel=27.15.1.1&userModel=Ford%20Explorer&dbPart=682.1&userPart=A%2FC%20Compressor&sessionID=13000000085313943&sURL=www.car-part.com&userPreference=year&userIntSelect=859730&userUID=0&userBroker=&iKey=&userPage=37',
        'https://www.car-part.com/cgi-bin/search.cgi?userSearch=int&userPID=1000&userLocation=USA&userIMS=&userInterchange=F%3DE&userSide=&userDate=2010&userDate2=2010&dbModel=27.15.1.1&userModel=Ford%20Explorer&dbPart=323.1&userPart=Fuel%20Pump&sessionID=13000000085314813&sURL=www.car-part.com&userPreference=year&userIntSelect=853474&userUID=0&userBroker=&iKey=&userPage=19']

#model = 'Jeep Wrangler'
#model = 'Toyota Corolla'
#model = 'Mazda Miata'
#model = 'Nissan Frontier'
#model = 'Volkswagen Bug'
#model = 'Chevrolet Silverado'
#model = 'Ford Explorer'
#model = 'Ford Crown Victoria'
#model = 'Honda Accord'
#model = 'Hyundai Elantra'
models = ['Jeep Wrangler',
         'Mazda Miata MX5',
         'Nissan Frontier',
         'Ford Explorer']

#part = 'Fuel Pump / Fuel Injector'
#part = 'A/C Compressor Assembly'
part = ''

#url =  'https://www.car-part.com/cgi-bin/search.cgi?'
#url += '&userLocation=USA'
#url += '&userDate=' + years[0]
#url += '&userDate2=' + years[0]
#url += '&userModel=' + re.compile('\s').sub('%20',models[1])
#url += '&dbPart=' + part_nums[0]
#url += '&userPreference=year'
#url += '&userPage='
#print(url)

csv = 'used_part_prices.csv'
write_update = open(csv,'a',encoding='utf-8')

car = 1
for sample_url in urls:
    
    print('Car #'+str(car)+'\n')    
    userPage = 1
    findEndPage = re.compile('userPage=(?P<endPage>\d+)$')
    endPage = findEndPage.search(sample_url).group('endPage')
    while (userPage <= int(endPage)):
    
        full_url = sample_url[:-len(endPage)] + str(userPage)
        print('Page', userPage)
        
        open_site = urlopen(full_url)
        site_html = open_site.read()
        open_site.close()
        
        site_soup = soup(site_html, 'html.parser')
        table_soup = site_soup.findAll('tr',{})
#        i = 0
#        for tag in table_soup:
#            print('\n\nPosition: ',i,'\n')
#            print(tag)
#            i += 1

        table = []
        record = 0
        for row in table_soup:
            table_row = []
            i = 1
            for cell in row.findAll('td',{}):
                if (cell.text == "YearPartModel"):
                    record += 1
                if ((record == 1) & ((i==1) | (i==5))):
                    table_row.append(cell.text)
                i += 1
            if (record == 1):
                 table.append(table_row)
        table.pop(0) #Getting rid of the column titles
        #print(table)
        
        #Creating a writer to append the new data
        today = date.today()
        line = ''
        findMakeModel = re.compile('(?P<year>(\d{4}))?(?P<part>.+?[a-z])?(?P<makeModel>([A-Z][a-z]+[\-\s]?)+)$')
        for row in table:
            i = 1
            for cell in row:
                if (i == 1):
                    makeModel = findMakeModel.match(cell)
                    if (isinstance(makeModel,re.Match)):
                        year = '' if str(makeModel.group('year')) == 'None' else makeModel.group('year')
                        partName = '' if str(makeModel.group('part')) == 'None' else makeModel.group('part')
                        makeModel = '' if str(makeModel.group('makeModel')) == 'None' else makeModel.group('makeModel')
                        line += year + ',' + partName + ',' + makeModel + ','
                    else:
                        line += cell[0:4] + ',' + part + ',' + model + ','
                else:
                    line += cell + ','
                i += 1
            line += str(today.month)+'-'+str(today.day)+'-'+str(today.year)+'\n'
        #print(line)
        write_update.write(line)
        
        userPage += 1
    
write_update.close()
#
#year = '2010'
#part = 'Fuel Pump'
#car = ''
#phrase = year + part + car
#findMakeModel = re.compile('(?P<year>(\d{4}))?(?P<part>.+?[a-z])?(?P<makeModel>([A-Z][a-z]+[\-\s]?)+(\d*)?)$')
#makeModel = findMakeModel.match(phrase)
#year = '' if str(makeModel.group('year')) == 'None' else makeModel.group('year')
#partName = '' if str(makeModel.group('part')) == 'None' else makeModel.group('part')
#makeModel = '' if str(makeModel.group('makeModel')) == 'None' else makeModel.group('makeModel')
#
#string = year + ',' + partName + ',' + makeModel
#print(string)

url =  'https://www.car-part.com/cgi-bin/search.cgi?'
#url += 'userSearch=int'
#url += '&userPID=1000'
url += '&userLocation=USA'
#url += '&userInterchange=B%3DAA%40'
url += '&userDate=2010'
url += '&userDate2=2010'
#url += '&dbModel=73.7.1.1'
url += re.compile('\s').sub('%20','&userModel='+models[4])
#url += '&userModel=Ford%20Explorer'
url += '&dbPart=323.1'
#url += '&userPart=Fuel%20Pump'
#url += '&sessionID=13000000084292690'
#url += '&userIntSelect=601547'
url += '&userPreference=year'
url += '&userPage=2'
print(url)

#I have got to figure out the different parts between models
https://www.car-part.com/cgi-bin/search.cgi?userSearch=int&userPID=1000&userLocation=USA&userIMS=&userInterchange=B%3D%40C%3F&userSide=&userDate=2010&userDate2=2010&dbModel=30.3.1.1&userModel=Honda%20Accord&dbPart=323.1&sessionID=14000000076647652&sURL=www.car-part.com&userPreference=year&userIntSelect=54874&userUID=0&userBroker=&iKey=&userPage=2
https://www.car-part.com/cgi-bin/search.cgi?userSearch=int&userPID=1000&userLocation=USA&userIMS=&userInterchange=B%3DADE&userSide=&userDate=2010&userDate2=2010&dbModel=30.3.1.1&userModel=Honda%20Accord&dbPart=323.1&sessionID=14000000076647748&sURL=www.car-part.com&userPreference=year&userIntSelect=54875&userUID=0&userBroker=&iKey=&userPage=2
https://www.car-part.com/cgi-bin/search.cgi?userSearch=int&userPID=1000&userLocation=USA&userIMS=&userInterchange=B%3DADE&userSide=&userDate=2010&userDate2=2010&dbModel=30.3.1.1&userModel=Honda%20Accord&dbPart=323.1&sessionID=14000000076647792&sURL=www.car-part.com&userPreference=year&userIntSelect=54876&userUID=0&userBroker=&iKey=&userPage=2
https://www.car-part.com/cgi-bin/search.cgi?userSearch=int&userPID=1000&userLocation=USA&userIMS=&userInterchange=B%3D%40C%3D&userSide=&userDate=2010&userDate2=2010&dbModel=30.3.1.1&userModel=Honda%20Accord&dbPart=323.1&userPart=Fuel%20Pump&sessionID=14000000076648200&sURL=www.car-part.com&userPreference=year&userIntSelect=54877&userUID=0&userBroker=&iKey=&userPage=2
https://www.car-part.com/cgi-bin/search.cgi?userSearch=int&userPID=1000&userLocation=USA&userIMS=&userInterchange=B%3D%40BF&userSide=&userDate=2010&userDate2=2010&dbModel=30.3.1.1&userModel=Honda%20Accord&dbPart=323.1&userPart=Fuel%20Pump&sessionID=14000000076648245&sURL=www.car-part.com&userPreference=year&userIntSelect=54878&userUID=0&userBroker=&iKey=&userPage=2
https://www.car-part.com/cgi-bin/search.cgi?userSearch=int&userPID=1000&userLocation=USA&userIMS=&userInterchange=B%3D%40BF&userSide=&userDate=2010&userDate2=2010&dbModel=30.3.1.1&userModel=Honda%20Accord&dbPart=323.1&userPart=Fuel%20Pump&sessionID=14000000076648280&sURL=www.car-part.com&userPreference=year&userIntSelect=54879&userUID=0&userBroker=&iKey=&userPage=2
https://www.car-part.com/cgi-bin/search.cgi?userSearch=int&userPID=1000&userLocation=USA&userIMS=&userInterchange=B%3D%40BF&userSide=&userDate=2010&userDate2=2010&dbModel=30.3.1.1&userModel=Honda%20Accord&dbPart=323.1&userPart=Fuel%20Pump&sessionID=14000000076648389&sURL=www.car-part.com&userPreference=year&userIntSelect=54880&userUID=0&userBroker=&iKey=&userPage=2
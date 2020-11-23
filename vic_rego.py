import time
import requests
from bs4 import BeautifulSoup


def get_vic_rego(vehicle_type='car/truck',identifier_type='registration number',search_codes=['1DF5BI']):
    #start a session
    s=requests.Session()
    #get viewstate and view state generator
    res=s.get('https://www.vicroads.vic.gov.au/registration/buy-sell-or-transfer-a-vehicle/check-vehicle-registration/vehicle-registration-enquiry')
    soup=BeautifulSoup(res.text,'html.parser')
    view_generator=soup.find('input',{"id":'__VIEWSTATEGENERATOR'})['value']
    view_state=soup.find('input',{"id":'__VIEWSTATE'})['value']
    #have to leave 1 second time interval between 2 requests. Otherwise access will be denied.
    time.sleep(1)

    output=[]
    for search_code in search_codes:
        #request form content:
        data={'__EVENTTARGET': '',
        '__EVENTARGUMENT': '',
        '__VIEWSTATE': view_state,
        '__VIEWSTATEGENERATOR': view_generator,
        '__VIEWSTATEENCRYPTED': '',
        'site-search-head': '',
        'ph_pagebody_0$phheader_0$_FlyoutLogin$PersonalEmail$EmailAddress': '',
        'ph_pagebody_0$phheader_0$_FlyoutLogin$PersonalPassword$SingleLine_CtrlHolderDivShown': '',
        'ph_pagebody_0$phheader_0$_FlyoutLogin$OrganisationEmail$EmailAddress': '',
        'ph_pagebody_0$phheader_0$_FlyoutLogin$OrganisationPassword$SingleLine_CtrlHolderDivShown': '',
        'ph_pagebody_0$phheader_0$_FlyoutLogin$PartnerEmail$EmailAddress': '',
        'ph_pagebody_0$phheader_0$_FlyoutLogin$PartnerPassword$SingleLine_CtrlHolderDivShown': '',
        'ph_pagebody_0$phthreecolumnmaincontent_1$panel$VehicleSearch$vehicle-type': vehicle_type,
        'ph_pagebody_0$phthreecolumnmaincontent_1$panel$VehicleSearch$vehicle-identifier-type': identifier_type,
        'ph_pagebody_0$phthreecolumnmaincontent_1$panel$VehicleSearch$RegistrationNumberCar$RegistrationNumber_CtrlHolderDivShown': search_code,
        'honeypot': '',
        'ph_pagebody_0$phthreecolumnmaincontent_1$panel$btnSearch': 'Search'}

        #request data

        headers={'origin': 'https://www.vicroads.vic.gov.au',
        'referer': 'https://www.vicroads.vic.gov.au/registration/buy-sell-or-transfer-a-vehicle/check-vehicle-registration/vehicle-registration-enquiry',
        'user-agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'}
        re=s.post('https://www.vicroads.vic.gov.au/registration/buy-sell-or-transfer-a-vehicle/check-vehicle-registration/vehicle-registration-enquiry',data=data,headers=headers)
        soup=BeautifulSoup(re.text,'html.parser')

        #parse data
        
        details=soup.find('div',class_="detail-module")
        if details:
            record={}
            labels=details.find_all("label", class_="label")
            answers=details.find_all("div", class_="display")
            i=0
            for label in labels:
                record[label.text]=answers[i].text.strip()
                i=i+1
            output.append(record)
    
    return output




a=get_vic_rego(vehicle_type='car/truck',identifier_type='registration number',search_codes=['88888','ZJZ399','1DF4BI','1DF6NI'])
print(a)
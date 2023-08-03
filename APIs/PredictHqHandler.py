import requests
import json
from ..database.SQLiteHandler import insertEvent

API_KEY = "EqpJf87ypBIW6cbbhkXRj_HOyxkNezMRw66NdI86"
defaultID = "5uRg7CqGu7DTtu4Rfk"
iso_3166_1 =  ['AD','AE','AF','AG','AI','AL','AM','AO','AQ','AR','AS','AT','AU','AW','AX','AZ','BA','BB','BD','BE','BF','BG','BH','BI','BJ','BL','BM','BN','BO','BQ','BR','BS','BT','BV','BW','BY','BZ','CA','CC','CD','CF','CG','CH','CI','CK','CL','CM','CN','CO','CR','CU','CV','CW','CX','CY','CZ','DE','DJ','DK','DM','DO','DZ','EC','EE','EG','EH','ER','ES','ET','FI','FJ','FK','FM','FO','FR','GA','GB','GD','GE','GF','GG','GH','GI','GL','GM','GN','GP','GQ','GR','GS','GT','GU','GW','GY','HK','HM','HN','HR','HT','HU','ID','IE','IL','IM','IN','IO','IQ','IR','IS','IT','JE','JM','JO','JP','KE','KG','KH','KI','KM','KN','KP','KR','KW','KY','KZ','LA','LB','LC','LI','LK','LR','LS','LT','LU','LV','LY','MA','MC','MD','ME','MF','MG','MH','MK','ML','MM','MN','MO','MP','MQ','MR','MS','MT','MU','MV','MW','MX','MY','MZ','NA','NC','NE','NF','NG','NI','NL','NO','NP','NR','NU','NZ','OM','PA','PE','PF','PG','PH','PK','PL','PM','PN','PR','PS','PT','PW','PY','QA','RE','RO','RS','RU','RW','SA','SB','SC','SD','SE','SG','SH','SI','SJ','SK','SL','SM','SN','SO','SR','SS','ST','SV','SX','SY','SZ','TC','TD','TF','TG','TH','TJ','TK','TL','TM','TN','TO','TR','TT','TV','TW','TZ','UA','UG','UM','US','UY','UZ','VA','VC','VE','VG','VI','VN','VU','WF','WS','YE','YT','ZA','ZM','ZW']


def sendToDatabase(dataDict):
    resultsList = dataDict['results']
    for resDict in resultsList:
        id = resDict['id']
        country = resDict['country']
        insertEvent(id, country, resDict)

def getFullList(countryIsoCode):    
    response = requests.get(
        url=f"https://api.predicthq.com/v1/events",
        headers={
            "Authorization": f'Bearer {API_KEY}',
            "Accept": "application/json"
        },
        params={
            'country':countryIsoCode.upper(),
            "sort":"rank",
            "limit":"10"

        }
    )
    sendToDatabase(response.json())
    return response.json()


def getEventById(eventId):
    response = requests.get(
        url=f"https://api.predicthq.com/v1/events?id={eventId}",
        headers={
            "Authorization": f'Bearer {API_KEY}',
            "Accept": "application/json"
        },
        params={
            "id": eventId
        }
    )
    sendToDatabase(response.json())
    return response.json()


def isIsoCountryCode(countryCode):
    return countryCode.upper() in iso_3166_1
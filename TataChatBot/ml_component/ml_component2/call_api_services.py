import json
import requests
class CallApiServices(object):
    def __init__(self):
        pass


    def call_api(self):
        data = {'company code2': 455, 'month year3':
            {'month': "December", 'year': 2018}}
        companyId = data["company code2"]
        month = data["month year3"]["month"]
        years = data["month year3"]["year"]

        service1 = "http://192.168.0.116:8080/BillTrack/botBilltrack/subReceivableForecast?companyId="+str(companyId)+"&month="+str(month)+"&Year="+str(years)
        print(service1)
        # service2 = "http: // 192.168.0.116: 8080 / BillTrack / botBilltrack / topOutstandingByCustomer?companyId = "+companyId
        service3 = "http: // 192.168.0.116: 8080 / BillTrack / botBilltrack / sendMailForInvoice / Post"
        get_response = requests.get(service1)

if __name__ == '__main__':
    obj =  CallApiServices()
    obj.call_api()

# data = {'sender':   'Alice',
#     'receiver': 'Bob',
#     'message':  'We did it!'}
# data_json = simplejson.dumps(data)
# payload = {'json_payload': data_json}
# r = requests.post("http://localhost:8080", data=payload)
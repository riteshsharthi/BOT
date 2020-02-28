from .extractors.City_final import CityFinder
# from extractors.City_final import CityFinder
from .extractors.getNo_people.get_people import GetPeople
from dateutil.parser import parse
from .extractors.email_extractor import Email_extrator
from .extractors.Date_Extractor_Month_name_Final import DateMonthYear
# from .extractors.Company_invoice import invoice
# from .extractors.Company_name_Extractor import company_name
from .extractors.Company_next import CompanyNameExtractor
class Operations(object):

    def __init__(self):
       self.obj_findcity = CityFinder()
       self.no_of_people_finder = GetPeople()
       self.obj_sub_company = CompanyNameExtractor()
       self.obj_datemonth = DateMonthYear()
       self.obj_email = Email_extrator()

    def city_extrctr(self, text, context_data):
        try:
            city_extrctr = self.obj_findcity.findcity(text)
        except Exception as e:
            print("Exception in city_extrctr", e)
        return city_extrctr, context_data
    
    def people_count(self, text, context_data):
        try:
            people_count = self.no_of_people_finder.no_people(text)
        except Exception as e:
            print("Exception in people_count" , e)

        return people_count, context_data


    def extrator_email(self ,text, context_data):
        try:
            email = self.obj_email.email_extractor(text)
        except Exception as e :
            print("Exception in people_count", e)

        return email, context_data

    def invoice(self,text, context_data):

        return self.people_count(text, context_data)

    def month_year(self, text, context_data):
        try:
            d = self.obj_datemonth.date_extractor(text)
        except Exception as e:
            print("Exception in month_year", e)

        return d, context_data

    def company_name(self,text, context_data):
        try:
            data = self.obj_sub_company.company_code_extract(text)
        except Exception as e:
            print("Exception in company_name", e)
        return data,context_data

    def email_message(self,text, context_data):

        return text, context_data

    def yes_no(self, text, context_data):
        extracted_val = ""
        if text in ["yes", "y", "n", "no"]:
            if text == "y":
                text = "yes"
            if text == "n":
                text = "no"
        extracted_val=text
        return extracted_val, context_data

    def sub_company(self,text, context_data):
        try:
           sub_data =self.obj_sub_company.company_code_extract(text)
        except Exception as e:
            print("Exception in sub_company", e)
        return sub_data,context_data


if __name__ == "__main__":
    val = Operations()
    print(val.invoice("my email id is " ,{}))

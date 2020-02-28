import json
from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017')
db = client['bot']
collection = db['f_a_q']
# for obj in collection.find():
#     print (obj)





# with open('currencies.json') as f:
#     file_data = json.load(f)
#
file_data =[{
	"_id": 1,
	"question": "I want to understand my current bill.",
	"answer": " You can check your current bill details by logging on to vodafone.in \u003e\u003e Bills and Payments \u003e\u003e View Bills.  You may also download the MyVodafone App and view bill details by going to Main menu \u003e\u003e Bills and Payments",
	"audio": "",
	"video": "",
	"image": "",
	"doc": ""
},
{
	"_id": 2,
	"question": "I want to know my current outstanding amount.",
	"answer": "You can check your outstanding amount by logging on to vodafone.in or click here",
	"audio": "",
	"video": "",
	"image": "",
	"doc": ""
},
{
	"_id": 3,
	"question": "I want to view my current bill.",
	"answer": "You can view your current bill details by logging on to vodafone.in .  You may also download the MyVodafone App and view current bill details by going to Main menu \u003e\u003e Bills and Payments.",
	"audio": "",
	"video": "",
	"image": "",
	"doc": ""
},
{
	"_id": 4,
	"question": "I want to know my unbilled amount.",
	"answer": "  You can check your unbilled amount by logging on to vodafone.in .  You may also download the MyVodafone App and view unbilled amount on the homepage.",
	"audio": "",
	"video": "",
	"image": "",
	"doc": ""
},
{
	"_id": 5,
	"question": "I have not received my bill.",
	"answer": "You can check your current bill details by logging in to vodafone.in \u003e\u003e Bills and Payments \u003e\u003e View Bills.  You may also download the MyVodafone App and view bill details by going to Main menu \u003e\u003e Bills and Payments.",
	"audio": "",
	"video": "",
	"image": "",
	"doc": ""
},
{
	"_id": 6,
	"question": "I want a duplicate bill.",
	"answer": "You can view/download/Email your bills by logging on to vodafone.in and clicking the Bills and payments section. Your previous bills are available under View Bills section.  You may also download the MyVodafone App and view/downlioad/email your bills by going to Main Menu \u003e\u003e Bills and Payments.",
	"audio": "",
	"video": "",
	"image": "",
	"doc": ""
},
{
	"_id": 7,
	"question": "I want to switch to Bill on Email (E-bill) facility.",
	"answer": " You can check your current bill delivery mode and switch to bill on Email by logging on to vodafone.in and clicking Bills and Payments \u003e\u003e Bill Preferences.  You may also download the MyVodafone App and switch to bill on Email by clicking on Main Menu \u003e\u003e Bills and Payments \u003e\u003e Manage your Bill preferences",
	"audio": "",
	"video": "",
	"image": "",
	"doc": ""
},
{
	"_id": 8,
	"question": "I want to pay my bill.",
	"answer": " You can pay your Vodafone bills via any of the below mentioned modes:      My Vodafone App- Download here. Easy 2 steps journey for bill payment.     Vodafone.in - Pay bill in just 2 steps on the go!     Visit nearest retail store     Cheque- Drop a cheque in nearest Vodafone store     Auto- Payment- Activate standing instruction for automated monthly payments. Activate now     Net Banking and other wallets - Any bank app or other payment apps like Paytm",
	"audio": "",
	"video": "",
	"image": "",
	"doc": ""
},
{
	"_id": 9,
	"question": "I want to know my due date for bill payment.",
	"answer": "You can check your bill due date by logging on to vodafone.in  You may also download the MyVodafone App and view bill due date on the homepage.",
	"audio": "",
	"video": "",
	"image": "",
	"doc": ""
},
{
	"_id": 10,
	"question": "Money was deducted, but the bill payment is not updated.",
	"answer": " It may take up to 24 hours to update your payment in your respective account.  In case the money was deducted from your account and the payment was unsuccessful, the amount will be refunded in your respective account within 7 working days.  You can check your payment status by logging on to vodafone.in \u003e\u003e Bill payment \u003e\u003e Payment history.  You can also download the MyVodafone App and check your payment status by clicking on Bills and Payments \u003e\u003e Past payments",
	"audio": "",
	"video": "",
	"image": "",
	"doc": ""
},
{
	"_id": 11,
	"question": "How to get the payment receipt for my payment?",
	"answer": "You can download your previous payment receipt by logging on to vodafone.in and clicking the Bills and payments \u003e\u003e Payment History. ",
	"audio": "",
	"video": "",
	"image": "",
	"doc": ""
},
{
	"_id": 12,
	"question": "What are late payment charges?",
	"answer": " Late payment fee is charged when bill payment is not made within the due date. Request to make your payment in time to avoid late payment charges.  For hassle free experience, you can activate standing instruction (Auto payment by Credit card) on your number.To activate Click here.",
	"audio": "",
	"video": "",
	"image": "",
	"doc": ""
},
{
	"_id": 13,
	"question": "I want to activate auto payments of bill (standing instruction).",
	"answer": "To avoid the hassle of remembering bill due date every month, activate Standing instruction (SI on Credit card). Click here to activate.",
	"audio": "",
	"video": "",
	"image": "",
	"doc": ""
},
{
	"_id": 14,
	"question": "I want to know my current plan and packs",
	"answer": " You can view your plan and packs details by logging on to vodafone.in and clicking on Plans and usage.  You may also download the MyVodafone App and view your plan and packs by going to Main Menu \u003e\u003e Active plans and packs.",
	"audio": "",
	"video": "",
	"image": "",
	"doc": ""
},
{
	"_id": 15,
	"question": "I want to know the impact of GST on my bill.",
	"answer": "As per government directive, from 1st July 2017, Goods and Services Tax (GST) is applicable on all services. You will be charged GST of 18% in your Vodafone Mobile bill.",
	"audio": "",
	"video": "",
	"image": "",
	"doc": ""
},
{
	"_id": 16,
	"question": "I want to check my balance online.",
	"answer": "You can check your balance by logging on to vodafone.in .  You may also download the MyVodafone App and view your balance on the homescreen. Also, you can dial *111# and choose the relevant option to check your balance",
	"audio": "",
	"video": "",
	"image": "",
	"doc": ""
},
{
	"_id": 17,
	"question": "I want to check my data balance online.",
	"answer": " You can check your data balance by logging on to vodafone.in  You may also download the MyVodafone App and view your data balance on the homescreen. Also, you can dial *111# and choose the relevant option to check your data balance.",
	"audio": "",
	"video": "",
	"image": "",
	"doc": ""
},
{
	"_id": 18,
	"question": "I want to check my validity.",
	"answer": "You can download the MyVodafone App and view your service validity on the homescreen. Also, you can dial *111# and choose the relevant option to know your service validity.",
	"audio": "",
	"video": "",
	"image": "",
	"doc": ""
},
{
	"_id": 19,
	"question": "I want to know my active packs and plans.",
	"answer": "You can check your active packs details by logging on to vodafone.in \u003e\u003e Plans and Usage. You may also download the MyVodafone App and view your active packs details by clicking on Main menu \u003e\u003e Active packs and services. Also, you can dial *111# and choose the relevant option to know your active plans and packs details.",
	"audio": "",
	"video": "",
	"image": "",
	"doc": ""
},
{
	"_id": 20,
	"question": "How can I do a recharge?",
	"answer": "You can do a prepaid recharge via any of the below mentioned modes:      My Vodafone App- Download here MyVodafone App. Easy 2 step journey for quick recharge.     vodafone.in - Recharge in just 2 steps, without logging in.     Visit nearest Vodafone store     Visit nearest retail store     Recharge using any third party bank app/ wallet like PayTM, Amazon Pay, Phone pe, etc.",
	"audio": "",
	"video": "",
	"image": "",
	"doc": ""
},
{
	"_id": 21,
	"question": "How can I do a recharge using my available balance?",
	"answer": "You can dial *111# and select the relevant option to activate a sata pack or any other bonus card from your available balance. You can also download the MyVodafone App and choose the relevant pack \u003e\u003e Pay by balance. This option is available only for selective packs. Please note that the charges will be deducted from your available prepaid account balance",
	"audio": "",
	"video": "",
	"image": "",
	"doc": ""
},
{
	"_id": 22,
	"question": "I cannot see my balance after the recharge",
	"answer": "Sometimes, it takes up to 30 minutes for the recharge benefits to reflect in your account.You can check your recharge status by logging on to vodafone.in \u003e\u003e Plans and Usage \u003e\u003e Recharge history  You can also download the MyVodafone App and check your recharge status by clicking on Recharge and more \u003e\u003e History",
	"audio": "",
	"video": "",
	"image": "",
	"doc": ""
},
{
	"_id": 23,
	"question": "I want to know my previous recharges.",
	"answer": " You can check your previous recharges by logging on to vodafone.in \u003e\u003e Plans and Usage \u003e\u003e Recharge history  You can also download the MyVodafone App and check your previous recharges by clicking on Recharge and more \u003e\u003e History",
	"audio": "",
	"video": "",
	"image": "",
	"doc": ""
},
{
	"_id": 24,
	"question": "I want to know my recent deductions.",
	"answer": "You can check your recent deductions by using one of the following options:      1 .Download the MyVodafone App and click on Recharge and more \u003e\u003e History     2. Dial *111# and choose the relevant option under “Balance and Usage” ",
	"audio": "",
	"video": "",
	"image": "",
	"doc": ""
},
{
	"_id": 25,
	"question": "I want to know my last call charges.",
	"answer": "You can check your recent deductions by using one of the following options:      Log on to vodafone.in \u003e\u003e Plans and Usage     Download the MyVodafone App and click on Recharge and more \u003e\u003e History     Dial *111# and choose the relevant option under “Balance and Usage” ",
	"audio": "",
	"video": "",
	"image": "",
	"doc": ""
},
{
	"_id": 26,
	"question": "I want to explore other packs and plans.",
	"answer": "You can view our exciting packs and plans in the SHOP section of the vodafone.in or download the MyVodafone App.",
	"audio": "",
	"video": "",
	"image": "",
	"doc": ""
},
{
	"_id": 27,
	"question": "I want to change my postpaid connection to Prepaid.",
	"answer": "Please visit the nearest Vodafone store with your Aadhaar number to convert the number from postpaid to prepaid.  In case you do not have Aadhaar number, don’t forget to carry your Identity and Address proof with you.",
	"audio": "",
	"video": "",
	"image": "",
	"doc": ""
},
{
	"_id": 28,
	"question": "What is Vodafone 4G ?",
	"answer": " Vodafone 4G (short for 4th Generation) is the next evolution in mobile technology. It provides significantly improved internet experience for a smartphone user.  You will enjoy almost instantaneous web page loading, faster photo viewing on Facebook and video streaming without the wait.",
	"audio": "",
	"video": "",
	"image": "",
	"doc": ""
},
{
	"_id": 29,
	"question": "How is 4G different from 3G/2G ?",
	"answer": "In one word: Speed.  Vodafone 4G provides faster internet speed, up to ten times faster than the current 3G speed.",
	"audio": "",
	"video": "",
	"image": "",
	"doc": ""
},
{
	"_id": 30,
	"question": "How is 4G different from LTE?",
	"answer": "They are both essentially the same.  4G is often referred to as LTE which stands for ‘Long Term Evolution’.",
	"audio": "",
	"video": "",
	"image": "",
	"doc": ""
},
{
	"_id": 31,
	"question": "Do I need a separate SIM to use 4G services?",
	"answer": "Yes, you will need a separate SIM to use 4G services. Visit any of our stores for a free 4G SIM upgrade.",
	"audio": "",
	"video": "",
	"image": "",
	"doc": ""
},
{
	"_id": 32,
	"question": "I want to receive internet settings.",
	"answer": "To receive internet settings, just SMS “ALL” to 199. Happy surfing!",
	"audio": "",
	"video": "",
	"image": "",
	"doc": ""
},
{
	"_id": 33,
	"question": "I want to check my data usage and available quota.",
	"answer": "  You can check your data balance by logging on to vodafone.in .  You may also download the MyVodafone App and view your data balance on the homescreen. Also, you can dial *111# and choose the relevant option to check your data balance.",
	"audio": "",
	"video": "",
	"image": "",
	"doc": ""
},
{
	"_id": 34,
	"question": "I want to know my active data pack.",
	"answer": "You can check your active data pack details by logging on to vodafone.in \u003e\u003ePlans and Usage.  You may also download the MyVodafone App and view your active data pack details by clicking on Main menu \u003e\u003e Active packs and services.  Also, you can dial *111# and choose the relevant option to know your active data pack details.",
	"audio": "",
	"video": "",
	"image": "",
	"doc": ""
},
{
	"_id": 35,
	"question": "I want to explore data packs and plans",
	"answer": "You can view our exciting data packs and plans in the SHOP section of the vodafone.in or Simply download the MyVodafone App.",
	"audio": "",
	"video": "",
	"image": "",
	"doc": ""
},
{
	"_id": 36,
	"question": "I want to buy a new Vodafone connection.",
	"answer": "Great choice!  You can buy a new Vodafone connection online and get it delivered to your doorstep by simply sharing your details here. Order Now!  Also, you can visit the Vodafone store or Retail store to buy a new connection. Please do carry your Aadhaar card with you.",
	"audio": "",
	"video": "",
	"image": "",
	"doc": ""
},
{
	"_id": 37,
	"question": "I want to know convert my Prepaid to Postpaid connection.",
	"answer": "Great choice!  You can convert your Prepaid connection to Postpaid online and get the new SIM delivered to your doorstep by sharing your details here. Switch now!  Also, you can visit the Vodafone store to switch from Prepaid to Postpaid connection. Please do carry your Aadhaar card with you.",
	"audio": "",
	"video": "",
	"image": "",
	"doc": ""
},
{
	"_id": 38,
	"question": "I want to port my number to Vodafone.",
	"answer": "Great choice!  Please generate a UPC code by sending PORT to 1900 from your existing network provider. Kindly clear all your dues before porting. You can then order a new Vodafone connection online and get it delivered to your doorstep by simply sharing your details here. Port now!  Also, you can visit the Vodafone store or Retail store to port your existing connection to Vodafone. Please do carry your Aadhaar card with you",
	"audio": "",
	"video": "",
	"image": "",
	"doc": ""
},
{
	"_id": 39,
	"question": "I want to know my existing plan and packs.",
	"answer": " You can view your plan and packs details by logging on to Vodafone.in. Click here  You may also download the MyVodafone App Here and view your plan and packs by going to Main Menu \u003e\u003e Active plans and packs.",
	"audio": "",
	"video": "",
	"image": "",
	"doc": ""
},
{
	"_id": 40,
	"question": "I want to activate roaming pack for travel within India.",
	"answer": "To activate a national roamig pack, please visit Homepage and select shop \u003e\u003e Roaming packs. OR Prepaid customers can click here.. Postpaid customers can click here.",
	"audio": "",
	"video": "",
	"image": "",
	"doc": ""
},
{
	"_id": 41,
	"question": "I want to activate International roaming service.",
	"answer": "If you are a Prepaid customer Prepaid users can SMS ACT IR to 144 (toll free) (Applicable for Ori, Bhr, Kol, ROB) For rest of the country, IR service is preactivated \u0026 you will be charged a monthly rental of Rs. 99 when any of the following chargeable events are performed while on International Roaming:  Making an Outgoing call- USSD Callback* or Direct dial Answering an incoming call Sending Messages Using GPRS  If you are a postpaid customer,you can follow any of the below mentioned option: Download MyVodafone App and navigate to Main menu \u003e Roaming \u003e International Roaming Via Website : Go to Discover \u003e\u003e International Roaming Call 199 from your Vodafone mobile phone SMS ACT IR to 199 (toll free) International Roaming service will get activated Within 30 minutes post SMS. International roaming deposit can also be paid online. The option of paying applicable deposits is also available at any of our Vodafone stores. TAT for payment updation – maximum 24 Hours.  Disclaimer: Based on the discretion of Vodafone Credit services, additional deposits may or may not be payable. On request from the user, deposit will be adjusted in the upcoming bills post the deactivation of International Roaming services.",
	"audio": "",
	"video": "",
	"image": "",
	"doc": ""
},
{
	"_id": 42,
	"question": "I want to activate International roaming pack.",
	"answer": "To activate your international roaming pack, you can follow any of these options: 1. Visit Homepage and select shop \u003e\u003e Roaming packs 2. Download the MyVodafone App and activate the same by going to Main Menu \u003e\u003e Roaming \u003e\u003e Country name \u003e\u003e Select pack 3. Call the customer care on 199 4. Dial *111# and choose the relevant option TAT for pack activation: 30 mins",
	"audio": "",
	"video": "",
	"image": "",
	"doc": ""
},
{
	"_id": 43,
	"question": "What data usage rate will I be charged?",
	"answer": "Standard data usage rate of Rs.5.50 (country specific) per 10KB will be charged while roaming internationally. Free usage given in your local data plan is not applicable while roaming internationally. Some operators may charge for PDP sessions as well. Do check country applicability and activate a pack for discounted benefits.",
	"audio": "",
	"video": "",
	"image": "",
	"doc": ""
},
{
	"_id": 44,
	"question": "What are the data roaming charges on International roaming?",
	"answer": "On International Roaming, data charges are country specific. To know the rates for your choosen country, you can do the following: 1.Go to Discover \u003e\u003e International roaming. 2. Download MyVodafone App and clicking on Main Menu \u003e\u003e Roaming \u003e\u003e Enter country. 3. SMS ROAM country name to 199(toll free in home network). ",
	"audio": "",
	"video": "",
	"image": "",
	"doc": ""
},
{
	"_id": 45,
	"question": "What is a PDP session?",
	"answer": "PDP is Packet Data protocol. When you want to use GPRS, your mobile will first attach to a GPRS enabled network in the country you are roaming and then your mobile will automatically activate a “PDP context”. PDP context is essential for the visited network to authenticate you as a valid GPRS user. Some operators may charge for PDP context. We recommend that you switch off GPRS after you have finished to avoid any additional charges.",
	"audio": "",
	"video": "",
	"image": "",
	"doc": ""
},
{
	"_id": 46,
	"question": "I want to know my active roaming packs and services.",
	"answer": "You can check your active packs and services by logging on to vodafone.in \u003e\u003e My Services. You may also download the MyVodafone App and check your active packs and plans by going to Main menu \u003e\u003e Active packs and services.",
	"audio": "",
	"video": "",
	"image": "",
	"doc": ""
},
{
	"_id": 47,
	"question": "I want to contact customer care while travelling within India.",
	"answer": "You can call the customer care on 199 from your Vodafone number.",
	"audio": "",
	"video": "",
	"image": "",
	"doc": ""
},
{
	"_id": 48,
	"question": "I want to contact customer care while travelling outside India",
	"answer": "You can call the customer care on 199 from your Vodafone number. Also, you can call your state's Vodafone customer care number for any assistance on International roaming. These calls are free of cost. To get the list of customer care number for your state, click here.",
	"audio": "",
	"video": "",
	"image": "",
	"doc": ""
},
{
	"_id": 49,
	"question": "I want to deactivate international roaming service/packs",
	"answer": "To deactivate your international roaming service/pack, you can do the following: 1. Download the MyVodafone App and deactivate the same by going to Main Menu \u003e\u003e Active packs and services \u003e\u003e Packs/Services. 2. SMS CAN IR to 199 (Toll free). Service will be deactivated within 30 mins post SMS. 3. Visit the nearesr Vodafone store.",
	"audio": "",
	"video": "",
	"image": "",
	"doc": ""
},
{
	"_id": 50,
	"question": "I am not able to use my national roaming. What should I do ?",
	"answer": "If you have national roaming active on your mobile, pls try and select the network manually. If you still face this problem, you can call up at 199.",
	"audio": "",
	"video": "",
	"image": "",
	"doc": ""
},
{
	"_id": 51,
	"question": "I want to use my free data quota on international roaming. Is it possible ?",
	"answer": "Any in built free data usage will NOT be applicable while on International roaming. Usage is charged as per applicable rates except for special roaming packages (subject to availability).",
	"audio": "",
	"video": "",
	"image": "",
	"doc": ""
},
{
	"_id": 52,
	"question": "Why am I billed for roaming even when I have not visited any roaming location in the last billing period?",
	"answer": "Roaming usages are billed as per data received from the destination Roaming Operator. In case of delay in receiving of such data files, usages made in a particular bill period may reflect in succeeding bill period.",
	"audio": "",
	"video": "",
	"image": "",
	"doc": ""
},
{
	"_id": 53,
	"question": "Tips on optimizing your mobile internet usage?",
	"answer": "If you have online applications on your device, remember that data usage occurs throughout the day; hence usage will be billed accordingly.  Smart devices have a tendency to continuously access data network and automatically download some updates for certain applications like Weather, Stock/News alerts, social networking sites (Twitter, Facebook) and emails. Hence it is recommended, you disable data from your handset itself to avoid unnecessary charges by Switching off the settings.  Or alternatively check your handset menu to switch off data settings or auto updates It is advisable to log-out properly before terminating a surfing session thus ensuring unnecessary data transfer is avoided.",
	"audio": "",
	"video": "",
	"image": "",
	"doc": ""
},
{
	"_id": 54,
	"question": "Caller Tunes",
	"answer": " Activation - Send CT \u003cSMS Code\u003e to 56789 to set the Callertune. For example to set the Vodafone Tune as Callertunes then send CT 130030 to 56789 Charges– Rs. 5 / SMS.  Charges      If you have already subscribed to the Callertune service – Rs. 15 per Callertune For 90 days     If you have not subscribed to the Callertune service – Rs. 36 rental per month     And Rs. 15 per Callertune for 90 days  Deactivate      If you're a Postpaid customer, SMS CAN CT to 199 (toll free)     If you're a Prepaid customer, SMS CAN CT to 144 (toll free)     Your caller tune will get Deactivated in the next 4 hours  Activation / deactivation Caller tune service will be activated / deactivated within 30 mins and a confirmation SMS will be sent on your Vodafone mobile number.",
	"audio": "",
	"video": "",
	"image": "",
	"doc": ""
},
{
	"_id": 55,
	"question": "Vodafone Alert",
	"answer": " Vodafone Alert is a bundled package with wide range of services ranging from Sports, Entertainment, Devotional, Infotainment, Rural, Finance, Health and Education segment. Along with daily in and out around you it also provides several entertaining packages which keeps you engaged through-out the day. To Avail Vodafone Alerts Service of your choice, dial *123# (Tollfree). Below are few Vodafone Alerts Service types:      Sports- Get regular updates from the ground of Cricket, Football, Hockey, Tennis and Formuala-1.     Entertainment- Follow your celebrities, movie reviews and filmy gossips and play competition and win prizes.     Devotional- Stay in touch with your faith, wherever you are.     Finance- Get latest update from the stock market for a wise investment.     Infotainment- Be updated with news from all the happenings around you.     Lifestyle- Make the most of your free time by having some fun.",
	"audio": "",
	"video": "",
	"image": "",
	"doc": ""
},
{
	"_id": 56,
	"question": "Ringtones",
	"answer": "      Send RT \u003csong or movie name\u003e as an SMS to 56789 or to get the list of top 10 tunes, just send RT TOP as SMS to 56789     After choosing the song, send RT \u003csong number\u003e to 56789     You will then receive a reply asking you to save the sound     Selected Ringtone gets saved in the Tones option of your phone.     Downloading a Ringtone takes a few minutes.  Charges- you will be charged Rs. 5 / SMS and an additional Rs. 7 for downloading a Ringtone.",
	"audio": "",
	"video": "",
	"image": "",
	"doc": ""
},
{
	"_id": 57,
	"question": "How do I change/modify my account details?",
	"answer": "    All you need to do is simply visit any of our Vodafone Stores.     Fill in a Service Request Form, along with your latest (not older than 3 months) Proof Of Address (POA) and Proof Of Identity (POI). On submission of correct and complete documents, your address will be changed within 3 days.     You will receive your latest bill at the new address if the address change request with complete documents has been submitted at least 4 days prior to your bill date.     Do carry originals for verification purpose. To know acceptable POA/POI click here  How do I update my Date of Birth?  Submit your Proof of Identity (POI) showing the Date of Birth, on receipt of correct documents this shall be rectified within 30 mins. For list of acceptable POI documents, click here   How do I update/change my alternate number?  Send an sms as ALT Your Alternate Number to 199 (toll free), the number will be updated in your Vodafone account within 30 mins. You can also update it using the myVodafone app.",
	"audio": "",
	"video": "",
	"image": "",
	"doc": ""
},
{
	"_id": 58,
	"question": "How can I change the SIM / What do I do if I have lost the SIM?",
	"answer": " Please visit nearest Vodafone store or Vodafone Mini Store with a copy of your Proof of Identity for SIM Change.   You can collect replacement of SIM card at your nearest Vodafone store or Vodafone Mini Store by submitting the damaged SIM along with a copy of photo id proof.   In case of loss of SIM. The customer is requiered to visit the nearest Vodafone Store/Vodafone Mini Store and submit FIR/Missing report along with a copy of their identity proof.      Bring an original photo ID proof with you when visiting a store to collect your replacement SIM card.     TAT of SIM replacement 2 hrs and Roaming SIM replacement - 48 hrs ",
	"audio": "",
	"video": "",
	"image": "",
	"doc": ""
},
{
	"_id": 59,
	"question": "Documents required for SIM Exchange?",
	"answer": " Documents required for SIM Change      SIM Exchange Form will be provided at the Vodafone Store / Mini Store     Carry a copy of your Proof of Identity with you         Indian Nationals         Foreign Nationals",
	"audio": "",
	"video": "",
	"image": "",
	"doc": ""
},
{
	"_id": 60,
	"question": "What is a Postpaid connection?",
	"answer": "A Postpaid connection is one where you are charged for the services that you use on a monthly basis. This is calculated keeping in mind the cost of your selected tariff plan as well as any additional packs or plans that you buy. You can view a break-up of the charges in your monthly bill. ",
	"audio": "",
	"video": "",
	"image": "",
	"doc": ""
},
{
	"_id": 61,
	"question": "Why should I choose Idea as my Postpaid service provider?",
	"answer": "• You can enjoy complete flexibility with Idea Postpaid, without worrying about your balance or recharges • You only have to pay a monthly bill to make use of Idea Postpaid services • Enjoy customized tariff plans, economical roaming charges, excellent data services and stay connected with coverage that you can count on • Besides, making bill payments is also easy • Select from multiple payment options available to you. ",
	"audio": "",
	"video": "",
	"image": "",
	"doc": ""
},
{
	"_id": 62,
	"question": "How do I get an Idea Cellular Postpaid connection?",
	"answer": "To get a new Idea Postpaid connection, submit your details here and an Idea executive will get in touch with you shortly. You can even avail of doorstep delivery of your choice of number.  Alternatively, you can visit the Idea service centre closest to you. Our executives will help you choose a Postpaid plan according to your usage. To locate the nearest Idea service centre, click here.  To get an Idea Postpaid connection, you must have the following documents:      A self-attested photograph     Filled Customer Application Form     Self-attested copy of address proof. Click here for list of documents that you can submit as address proof.     Self-attested copy of identity proof. Click here for list of documents that you can submit as identity proof.  You can get a Customer Application Form from an Idea service centre, or request a sales executive to give you one.  Once you have completed the application process, carry out tele-verification by calling 59059 from your new Idea Postpaid connection. ",
	"audio": "",
	"video": "",
	"image": "",
	"doc": ""
},
{
	"_id": 63,
	"question": "Do I need to make a payment while taking a new Postpaid connection? Is this amount refundable?",
	"answer": "When you apply for a new Postpaid connection, you will have to pay a one-time activation fee and a security deposit. While the one-time activation fee is non-refundable, the security deposit will be returned to you when you surrender your Idea Postpaid connection. ",
	"audio": "",
	"video": "",
	"image": "",
	"doc": ""
},
{
	"_id": 64,
	"question": "Will I get STD, ISD and roaming facilities with my Idea Postpaid connection?",
	"answer": "STD and national roaming are default services that you can enjoy with your new Idea Postpaid connection. If you need ISD and international roaming services, you can request it to be activated at the nearest Idea service centre. Or, you can visit www.ideacellular.com, click on ‘Self-care’, select my ‘Postpaid’ and choose the ‘My Plans \u0026 Services’ option. From the list of services, select ‘International Roaming’ and click on ‘Activate’. Do note you might have to undergo additional billing address verification and/or make a deposit to activate these services.  While there is no additional rental for STD, ISD and national roaming services, for international roaming, you will have to pay monthly rental of Rs.149, which will be added to your Postpaid bill.",
	"audio": "",
	"video": "",
	"image": "",
	"doc": ""
},
{
	"_id": 65,
	"question": "Can I block my Idea connection if I’ve lost the SIM card?",
	"answer": "You can get your SIM card replaced by simply visiting the nearest Idea Service Centre. You will need to present your original Photo Id proof \u0026 submit its photocopy. Charges for SIM replacement are circle-dependant.  1.In case if third party is visiting on your behalf then additional documents required are: I.Authorization letter with reason for sim replacement, details of the person who is visiting on your behalf \u0026 your signature on it. II.Photocopy of valid, self-attested Photo ID proof of third party.  2.Documents required if you are corporate customer I.Photocopy of valid, self attested photo ID proof of authorized signatory II.Request to be given on company letterhead, signed \u0026 stamped by authorized signatory",
	"audio": "",
	"video": "",
	"image": "",
	"doc": ""
},
{
	"_id": 66,
	"question": "Will all my old services be retained on my new SIM card?",
	"answer": "Yes, all your existing services will be retained \u0026 continued on the new SIM card.",
	"audio": "",
	"video": "",
	"image": "",
	"doc": ""
},
{
	"_id": 67,
	"question": "What is a Prepaid subscription?",
	"answer": "A pre-paid connection is a ‘pay \u0026 use’ subscription service. With this subscription, you need to pay in advance to use the services by way of recharge, which provides you talk-time/ balance for usage. Pre-paid services allow you to control your usage as per your need.",
	"audio": "",
	"video": "",
	"image": "",
	"doc": ""
},
{
	"_id": 68,
	"question": "How do I get an Idea Cellular Prepaid connection?",
	"answer": "To get an Idea Prepaid connection, you can call Idea customer care and request a new connection. An Idea executive will get in touch with you shortly with details of latest offers and promotions. For Idea customer care contact details, click here. You can also make a request for a new connection by clicking here.  You can also visit the nearest Idea service centre or Idea retailer. Here you have to: 1.If Aadhaar is available :      Carry your Aadhaar card to the point of sale.     Foreign national customers are not eligible for eKYC activation process.   2.If Aadhaar is not available :      Fill up a Customer Application Form.     Provide one passport size photograph.     Provide a copy of valid address proof. Click here for list of documents that you can submit as address proof.     Provide a copy of valid identity proof. Click here for list of documents that you can submit as identity proof.  Note: You will have to carry your original address proof and ID proof documents for verification.  For Idea Stores, click here ",
	"audio": "",
	"video": "",
	"image": "",
	"doc": ""
},
{
	"_id": 69,
	"question": "How can I recharge my Prepaid connection?",
	"answer": "Visit www.ideacellular.com, log in with your credentials and click on ‘Overview’. Then, click on ‘Recharge Now’. Alternatively, you can simply click here.  You can also recharge your Idea Prepaid connection through the following modes:      Purchase a recharge coupon from the nearest Idea service centre or any Idea retailer. Then, follow the instructions on the coupon to complete the recharge.     Pay cash at any Idea service centre or Idea retailer and complete a recharge.     You can also recharge your Idea Prepaid connection at an ATM of the following banks: Axis Bank, Citibank Corporation Bank, Dena Bank, Development Credit Bank, Deutsche Bank, Greater Bank, HDFC Bank, ICICI Bank, IDBI Bank, ING Vysya Bank, SBI, Standard Chartered and Yes Bank.",
	"audio": "",
	"video": "",
	"image": "",
	"doc": ""
},
{
	"_id": 70,
	"question": "How long is my Prepaid connection valid for?",
	"answer": "For pre-paid connections with lifetime validity (not applicable for Assam, NESA, Jammu \u0026 Kashmir), the connection will continue as long as you maintain the usage as per the product conditions. Pre-paid connections wherein there is no usage for a continuous period of 90 days are likely to get disconnected. You can avoid this by ensuring continuous usage on your Pre-paid connection.  In case of non-usage for a continuous period of 90 days, the validity can be further extended if you maintain a balance more than or equal to Rs 20. In this case, Idea will debit Rs. 20 from the Pre-paid account and extend the validity period by 30 days and the process will continue till the account balance is more or equal to Rs. 20.",
	"audio": "",
	"video": "",
	"image": "",
	"doc": ""
},
{
	"_id": 71,
	"question": "What is grace period? (Applicable only to Prepaid customers from Assam, NESA and J\u0026K)",
	"answer": "On expiry of validity, if you do not recharge your Prepaid account, the number remains valid for a grace period of 60 days.  If you don’t recharge your account within the first 15 days of this period, your balance, if any, is forfeited.  If you don’t recharge your account with validity within 60 days, then your Prepaid number will be permanently disconnected. ",
	"audio": "",
	"video": "",
	"image": "",
	"doc": ""
},
{
	"_id": 72,
	"question": "Can I recharge my Prepaid account once the grace period expires?",
	"answer": "Once the grace period of 60 days has expired, your Prepaid connection will be permanently deactivated. In this case, you will need to buy a new Prepaid SIM card. The old number can’t be re-activated or re-allocated. ",
	"audio": "",
	"video": "",
	"image": "",
	"doc": ""
},
{
	"_id": 73,
	"question": "Do I need to pay extra to avail STD and ISD services on my Prepaid connection?",
	"answer": " STD and ISD services come with your Idea Prepaid connection. You don’t have to pay an extra charge to activate STD or ISD services.  STD and ISD call charges are applicable as per your plan/recharge.",
	"audio": "",
	"video": "",
	"image": "",
	"doc": ""
},
{
	"_id": 74,
	"question": "How do I avail the roaming feature on my Idea Prepaid connection?",
	"answer": "Roaming services are also pre-activated on all Pre-paid connections. There are no additional charges for activation of roaming. While using your pre-paid connection in International Roaming, a monthly rental will be deducted from your pre-paid account balance.  With a Pre-paid connection, you will be able to use the roaming service across India, except for Jammu and Kashmir. For Pre-paid cards activated in Jammu and Kashmir, roaming services are not available.  To view the national and International roaming tie-ups click here. ",
	"audio": "",
	"video": "",
	"image": "",
	"doc": ""
},
{
	"_id": 75,
	"question": "Can I block my Idea connection if I have lost the SIM card ?",
	"answer": "Yes, call our Idea customer care and we will block your connection. You can also visit the nearest Service Centre. Carry your original photo ID for verification. We recommend that you also get a replacement SIM card through the Idea Service Centre. ",
	"audio": "",
	"video": "",
	"image": "",
	"doc": ""
},
{
	"_id": 76,
	"question": "Will all my old services be retained on my new SIM card?",
	"answer": "Yes, all your existing services will be retained \u0026 continued on the new SIM card. ",
	"audio": "",
	"video": "",
	"image": "",
	"doc": ""
},
{
	"_id": 77,
	"question": "How can I use the GPRS service on my Idea connection?",
	"answer": "GPRS services are usually already proactive on your Idea Postpaid and Prepaid connection. However, if you have deactivated it, there are multiple ways in which you can make your GPRS activation request.Click here for more information on GPRS and data services on your Prepaid connection, Click here for information for your Postpaid connection.  Note that GPRS will work on compatible handsets. Additionally, in order to use 3G services, your device should be 3G compatible as well. Click here to find out how you can check whether your device is 3G compatible and visit the 'Must-haves' section.  Once the service is activated, there are certain settings that your handset must have. Click here for detailed information on GPRS settings.  Based on your data usage, you can select the most suitable plan for your Idea number and activate it. Click here to see data plans for Prepaid connections, and here to view data plans for Postpaid connections.  Happy surfing ! ",
	"audio": "",
	"video": "",
	"image": "",
	"doc": ""
}]


collection.insert(file_data)
client.close()

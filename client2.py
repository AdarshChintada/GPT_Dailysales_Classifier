import requests
import streamlit as st
import pandas as pd
import json  # Import the json module


# Sample data dictionary
data_dict = {'Candlewood Cupboard': 'miscellaneous income', 'AR Ledger Payments': 'payments received towards city ledger', 'Discount - D': 'transient discount', 'Parking': 'parking income', 'Corp-Global - G': 'group corporate', 'Corp-Negotiated Accts - L': 'transient corporate negotiate', 'Corp-Key Accts and BTA - P': 'transient corporate marketing programs', 'Package-Leisure - K': 'package exchange', 'City Tax 9%': 'rooms city tax', 'State Tax 6%': 'rooms sales tax', 'Sales Tax 8.25%': 'rooms sales tax', 'Gov/Dipl/Military - M': 'group government', 'Wholesale/FIT - W': 'transient wholesale', 'American Express': 'amex rooms', 'Cash': 'cash', 'Discover': 'discover rooms', 'Pet Fee': 'pet fees', 'House Use - H': 'house use rooms', 'Visa': 'visamc rooms', 'MasterCard': 'visamc rooms', 'Deposit Ledger Deposits Transfered at Check-In': 'advances transferred out', 'Deposit Ledger Payments': 'new advances recevied', 'AR Ledger Charges and Transfers': 'transfers to direct billing from guest ledger', 'Direct Billing/City Ledger': 'transfers to direct billing from guest ledger', 'Guest Ledger Deposits Transfered at Check-In': 'advances transferred out', 'No Show': 'guaranteed no show rooms', 'Accommodation Upsell': 'transient retail', 'No Show - Adj.': 'guaranteed no show rooms', 'City Tax 9% -Adj': 'rooms city tax', 'State Tax 6% -Adj': 'rooms sales tax', 'JCB': 'misc. credit card payment', 'Late Checkout': 'late checkout fees', 'Mamacitas Brkfst - Food': 'restaurant one food sales breakfast', 'Mamacitas Brkfst - Bar': 'restaurant one beverage sales other', 'Mamacitas Lunch - Food': 'restaurant one food sales lunch', 'Mamacitas Lunch - Bar': 'restaurant one beverage sales other', 'Mamacitas- Non Alcohol Bev': 'restaurant one beverage sales other', 'Mamacitas Dinner - Food': 'restaurant one food sales dinner', 'Mamacitas Dinner - Bar': 'restaurant one beverage sales other', 'Circa 1963 Dinner Food': 'restaurant one food sales dinner', 'Grab and Go': 'grab and go tax', 'Mamacitas Alcohol Tax': 'f and b sales tax', 'Mamacitas - Gratuity': 'f and b tips', 'Mamacitas - Food Tax  ': 'f and b sales tax', 'Circa 1963 Alcohol Tax': 'f and b sales tax', 'Circa Non Alcoholic Beverage': 'restaurant one beverage sales other', 'Circa 1963 Gratuity': 'f and b tips', 'Circa 1963 Food Tax': 'f and b sales tax', 'City Venue Tax 2%': 'rooms city tax', 'County Tax 2.5%': 'rooms county occupancy tax', 'POS - Cash': 'POS - Cash', 'POS- American Express': 'POS- American Express', 'POS - Visa': 'POS - Visa', 'POS - MasterCard': 'POS - MasterCard', 'POS - Discover': 'POS - Discover', 'POS -Gift Cert': 'POS -Gift Cert', 'State Tax 6%-Adj': 'rooms sales tax', 'City Tax 7%-Adj ': 'rooms city tax exemptions', 'City Venue Tax 2%-Adj': 'rooms city tax exemptions', ' County Tax 2.5%-Adj': 'rooms county occupancy tax exemptions', 'Corporate Marketing Programs': 'transient corporate marketing programs', 'Corporate Negotiated': 'transient corporate negotiate', 'Other Discounts': 'transient other discounts', 'Trans Suite Medium-Term': 'transient retail', 'Trans Suite Short-Term': 'transient retail', 'Trans Suite Long-Term': 'transient retail', 'Other Beverage Revenue': 'restaurant one beverage sales other', 'Other Revenue': 'miscellaneous income', 'BAR': 'transient best available rate', 'Consortia': 'transient consortia', 'AR Credit Card AMEX': 'amex rooms', 'Sales Tax Payable State': 'rooms sales tax', 'Room Occ Tax Payable - State': 'rooms county occupancy tax', 'AR Credit Card MC Visa': 'visamc rooms', 'Day Guest Charges': 'transient retail', 'Guaranteed No Show': 'guaranteed no show rooms', 'Government / Oth. Bus. Disc': 'group government', 'Telephone Local': 'telephone income local long distance', 'Telephone Long Dista': 'telephone income local long distance', 'Long Distance - Inte': 'telephone income local long distance', 'Attrition': 'attrition fees', 'Currency Exchange': 'miscellaneous income', 'Attrition F&B': 'attrition fees', 'Cxl/Attrition': 'attrition fees', 'Gift Certificate Pur': 'gift certificate 23140', 'AR CCard JCB Discover Diners': 'misc. credit card payment', 'Retail Sundries Non-Tax': 'miscellaneous income', 'Breakfast Covers': 'restaurant one food sales breakfast', 'SMERF Room Revenue': 'group smerf', 'Food & Beverage Tax Pay - City': 'f and b sales tax', 'Corp Negotiated Room Revenue': 'transient corporate negotiate', 'Dinner Covers': 'restaurant one food sales dinner', 'Honors Food Contra Revenue': 'miscellaneous income', 'Waiter Fees & Tips Payable': 'f and b tips', 'Trans.Suite/Room Rev.ShortTerm': 'transient retail', 'Local Negotiated Room Revenue': 'transient local negotiated', 'Dinner Food Revenue': 'restaurant one food sales dinner', 'Beer Revenue': 'restaurant one beverage sales beer', 'Discounts Room Rev': 'transient discount', 'Liquor Revenue': 'restaurant one beverage sales liquor', 'Best Available Rate Room Rev': 'transient best available rate', 'Food & Beverage Tax Pay -State': 'f and b sales tax', 'Meeting Room Revenue': 'meeting rooms', 'AR F&B Credit Card AMEX': 'amex f and b', 'Breakfast Food Revenue': 'restaurant one food sales breakfast', 'AR F&B Credit Card MC Visa': 'visamc f and b', 'Corp Mktg Program Room Revenue': 'transient corporate marketing programs', 'Wine Revenue': 'restaurant one beverage sales wine', 'Individual Tour Wholesale Room': 'transient wholesale', 'Service Charge Revenue': 'room service service charge', 'Sales Tax Payable City': 'rooms city tax', 'Service Charge Employee': 'room service service charge', 'TRANSIENT ROOM REV ': 'transient retail', 'BISTREAUX METAIRIE ': 'restaurant one restaurant other revenue', 'SUNDRIES TAX  ': 'grab and go tax', 'SUNDRY': 'miscellaneous income', 'VALET PARKING': 'parking income', 'PERKS': 'miscellaneous income', 'ROOM TAX': 'rooms sales tax', 'SALES TAX ': 'rooms sales tax', 'TAX EXEMPT ROOM REV': 'transient retail', 'VALET PARKING ADJ': 'parking income', 'RACK/BAR ': 'restaurant one beverage sales other', 'CORP NEGOTIATED ': 'transient corporate negotiate', 'CORP MARKET': 'transient corporate marketing programs', 'OTHER DISC': 'transient other discounts', 'GOVERNMENT': 'group government', 'INTERNET-NOP ': 'internet income', 'MERF ': 'group smerf', 'REST 1 DISCOUNTS': 'cash discounts earned', 'WIRED FOR BUS-FEE': 'eftwire payments', 'AMEX CLEARING': 'amex rooms', 'VISA/MASTER CARD': 'visamc rooms', 'DISCOVER CLEARING': 'discover rooms', 'GROUP BANQUETS': 'group associationconvention', 'IN ROOM DINING ': 'room service service charge', 'PACKAGE ROOM': 'transient retail', 'CATERING ROOM RENTAL': 'banquet room rental', 'BQT/CARTERING TAX': 'rooms sales tax', 'LAUNDRY': 'guest laundrydry cleaning', 'FACILITY FEE ': 'miscellaneous income', 'HEALTH CLUB': 'miscellaneous income', 'FRONT DESK CASH': 'cash', 'ROOM REVENUE': 'transient retail', 'EARLY DEPT FEE ': 'early departure fees', 'INTERNET': 'internet income', 'Room Rent ': 'transient retail', 'Rollaways': 'rollawayscribs', 'PETS': 'pet fees', 'Cancellation Charge': 'cancellation fees', 'No Show Charge': 'guaranteed no show rooms', 'Room Correction': 'miscellaneous income', 'FX2 Only': 'miscellaneous income', 'Late Check Out': 'late checkout fees', 'Early Check In': 'miscellaneous income', 'Check': 'checks', 'Innkeepers Tax': 'rooms sales tax', 'State Sales Tax': 'state tax', 'Sale Tax': 'rooms sales tax', 'County Tax ': 'rooms city tax', 'Discover(VB)': 'discover rooms', 'Discover / Novus /': 'discover rooms', 'Mastercard ': 'visamc rooms', 'Visa (S4)': 'visamc rooms', 'Misc Non-Taxable': 'miscellaneous income', 'Gift Shop': 'gift shop sales', 'Smoking': 'smoking fees', 'Pet Fees': 'pet fees', 'BW Free Night': 'complimentary rooms', 'Travelcards BW': 'misc. credit card payment', 'Complimentary Per': 'complimentary rooms', 'EFT PAYMENT': 'eftwire payments', 'Property Damage': 'miscellaneous income', 'CONNECTING ROOM': 'transient retail', 'Miscellaneous Tax': 'rooms city tax', 'Miscellaneous No Tax': 'miscellaneous income', 'Soap': 'miscellaneous income', 'Soda-bottle': 'miscellaneous income', 'Candy': 'miscellaneous income', 'Chips': 'miscellaneous income', 'Energy Drink': 'miscellaneous income', 'Soda-can': 'miscellaneous income', 'Softener': 'miscellaneous income', 'GUEST ROOM': 'transient retail', 'EXTRA ADULT': 'transient retail', 'EXTRA NO SHOW ROOM REVENUE ': 'transient retail', 'GUEST ROOM HONORS': 'transient retail', 'PREPAID EARLY CHECKOUT': 'early departure fees', 'ROOM UPGRADE': 'transient retail', 'ADVANCE PURCHASE 3.5% DISCOUNT': 'advance purchase 3.5% discount', 'ADVANCE PURCHASE 3.5%': 'advance purchase 3.5% discount', 'DISCOUNT': 'discount', 'ADVANCE PURCHASE CHANGE FEE ': 'advance purchase change fee', 'BALANCE TRANSFER ': 'balance transfer', 'CANCELLATION CHARGE ': 'cancellation fees', 'CHARGE-BACKS ': 'charge-backs', 'CLEANING FEE': 'cleaning fee', 'COFFEE BREAK': 'coffee break', 'COMMISSION REVENUE ': 'commission charge', 'COPIES': 'copies', 'EARLY ARRIVAL': 'early arrival', 'FAX': 'fax', 'GUEST CERTIFICATE': 'guest certificate', 'GUEST EQUIPMENT RENTAL ': 'guest equipment', 'HOME2MKT': 'home2mkt', 'INTERNET ACCESS': 'internet income', 'LATE CANCEL ROOM REVENUE': 'late cancel room revenue', 'LATE DEPARTURE': 'late departure', 'MEETING ROOM': 'meeting room', 'MISC REVENUE': 'miscellaneous income', 'MISC REVENUE NON-TAXABLE': 'misc revenue non-taxable', 'NO SHOW ROOM REVENUE ': 'guaranteed no show rooms', 'PET FEE': 'pet fees', 'PET FEE 1 TO 4 NIGHTS': 'pet fees', 'PET FEE 5 OR MORE NIGHTS ': 'pet fees', 'PET FEE ALLOW': 'pet fees', 'PET FEE MANUAL': 'pet fees', 'PREMIUM INTERNET ACCESS': 'internet income', 'PREPAID LATE CANCEL ROOM ': 'cancellation fees', 'RETURNED CHECKS': 'miscellaneous income', 'SERVICE ANIMAL': 'miscellaneous income', 'SMOKING FEE': 'smoking fees', 'TELEPHONE COMMISSIONS ': 'commission income', 'TELEPHONE-LD (FOREIGN) ': 'telephone income local long distance', 'TELEPHONE-LD (INTERSTATE) ': 'telephone income local long distance', 'TELEPHONE-LOCAL': 'telephone income local long distance', 'VALET LAUNDRY': 'guest laundrydry cleaning', 'VENDING MACHINE REVENUE': 'miscellaneous income', 'MISC COUNTY TAX ': 'rooms sales tax', 'MISC STATE TAX': 'rooms sales tax', 'RM COUNTY TAX': 'rooms county occupancy tax', 'RM HOTEL MOTEL FEE ': 'miscellaneous income', 'RM OCCUPANCY TAX': 'rooms county occupancy tax', 'RM STATE TAX': 'rooms sales tax', 'CASH': 'cash', 'CHECK': 'checks', 'AMEX ': 'amex rooms', 'MASTER': 'visamc rooms', 'VISA': 'visamc rooms', 'DISCOVER ': 'discover rooms', 'TELEPHONE-LD (INTRASTATE)': 'telephone income local long distance'}

#OPENAI response
def get_openai_response(input_text):
    response = requests.post(
        "http://localhost:8000/line_item/invoke",
        json={'input': {'data_dict': json.dumps(data_dict), 'line_items': input_text}}  
    )
    if response.status_code == 200:
        response_json = response.json()
        if 'output' in response_json and 'content' in response_json['output']:
            content_str = response_json['output']['content']
            # Convert the content string into a JSON object
            content_json = json.loads(content_str)
            st.text("GPT 3.5 response:")
            # Display JSON content
            st.json(content_json)
            # Add download button for JSON
            st.download_button(
                label="Download JSON",
                data=content_str,
                file_name="openai_response.json",
                mime="application/json"
            )
            return ""
        else:
            return st.error("No content found in response")
    else:
        return st.error(f"Error: {response.text}")
        
#llama2 response      
def get_ollama_response(input_text1):
    response = requests.post(
        "http://localhost:8000/opensource/invoke",
        json={'input': {'data_dict': json.dumps(data_dict), 'line_items': input_text1}}  
    )
    if response.status_code == 200:
        response_json = response.json()
        if 'output' in response_json and 'content' in response_json['output']:
            content_str = response_json['output']['content']
            # Convert the content string into a JSON object
            content_json = json.loads(content_str)
            st.text("Llama2 response:")
            # Display JSON content
            st.json(content_json)
            # Add download button for JSON
            st.download_button(
                label="llama2 JSON",
                data=content_str,
                file_name="Llama2_response.json",
                mime="application/json"
            )
            return ""
        else:
            return st.error("No content found in response")
    else:
        return st.error(f"Error: {response.text}")

# Line items from dataframe

#csv
'''df = pd.read_csv('dataframe.csv')

for index, row in df.iterrows():
    line_item = row['line_item_column_name']  
    get_openai_response(line_item)'''
 
 #text   
'''def read_line_items_from_text_file(text_file):
    with open(text_file, 'r') as file:
        line_items = file.readlines()
    return line_items'''
    
    
## streamlit framework

st.title('DAILY SALES CLASSIFIER')
input_text = st.text_area("GPT asking you line items")

input_text1 = st.text_area("Llama2 waiting for line items")

if input_text:
    # st.write('OpenAI response:')
    st.write(get_openai_response(input_text))

if input_text1:
    # st.write('Llama2 response:')
    st.write(get_ollama_response(input_text1))


from adcb_uae_test.items import Product
import scrapy
from lxml import html
import os
from datetime import date

def clean(text):
    if not text:
        return None
    return ' '.join(''.join(text).split()).strip()

class Adcb_uae_testSpider(scrapy.Spider):
    name = "adcb_uae_test"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.adcb_uae_list = []       # For main files
        self.adcb_uae_sub_list = []   # For sub files
        self.total_requests = 0       # Track total files to process
        self.processed_responses = 0  # Track responses received

    def start_requests(self):
        # folder_path = os.path.dirname(os.path.abspath(__file__))
        folder_path = os.path.join(os.path.expanduser("~"), "Documents")
        for file_name in os.listdir(folder_path):
            if file_name.endswith(".mhtml"):
                self.total_requests += 1
                meta = {
                    'file_name': file_name
                }
                file_path = f"file://{os.path.abspath(os.path.join(folder_path, file_name))}"
                yield scrapy.Request(
                    url=file_path,
                    callback=self.parse,
                    meta=meta
                )
                # return
        print(f'Request count : {self.total_requests}')

    def parse(self, response):
        file_name = response.meta.get('file_name', '')
        # print(file_name)
        adcb_uae_list, adcb_uae_sub_list = [], []
        if file_name:
            
            if '-' not in file_name:
                adcb_uae = self.parse1(response)
                if adcb_uae:
                    self.adcb_uae_list.append(adcb_uae)
                # return Product(**adcb_uae)
            else:
                adcb_uae_sub = self.parse2(response)
                # return Product2(**adcb_uae_sub)
                if adcb_uae_sub:
                    self.adcb_uae_sub_list.append(adcb_uae_sub)
        self.processed_responses += 1
        if self.processed_responses == self.total_requests:
            # Only proceed if there is data to compare
            if self.adcb_uae_list and self.adcb_uae_sub_list:
                for item in self.generate_items():
                    # print(item)
                    yield Product(**item)
            else:
                print("No data found in one or both lists")

    def generate_items(self):
        items = []
        if self.adcb_uae_list and self.adcb_uae_sub_list:
            for main in self.adcb_uae_list:
                for sub in self.adcb_uae_sub_list:
                    if main.get('cid_no') == sub.get('cid_no'):
                        combined = {**main, **sub}
                        items.append(combined)
        return items  # Always returns an empty list if no matches

    def parse2(self, response):
        # return
        parser = html.fromstring(response.text)
        # xpath_address2 = "//td[contains(text(), 'Address')]//parent::tr//following-sibling::tr[1]/td[2]//text()"
        # xpath_address3 = "//td[contains(text(), 'Address')]//parent::tr//following-sibling::tr[2]/td[2]//text()"
        xpath_data = "//td[contains(text(), 'CID No.')]//parent::tr//parent::tbody//tr"
        cleaned_text = response.text.replace("=3D", "=").replace("\n", "").replace("\r", "").replace("\t", "").replace("&nbsp;", " ").strip()
        # print(cleaned_text)
        # return
        try:
            Issue_date  = [
                item for item in cleaned_text.replace('&=nbsp;', '').split('Issue date')[-1].strip().split('</td>') if item.strip()
                ][0].split('nowrap="">')[-1].strip().replace('=', '').strip().split('"data">')[-1].replace('&nbsp;', '')
        except Exception as e:
            print(e)
            Issue_date = ''

        if Issue_date and '</td>' in Issue_date:
            Issue_date = Issue_date.split('</td>')[0].strip()

        try:
            Next_due_date  = [
                item for item in cleaned_text.replace('&=nbsp;', '').split('Next due date')[-1].strip().split('</td>') if item.strip()
                ][0].split('nowrap="">')[-1].strip().replace('=', '').strip().split('"data">')[-1].replace('&nbsp;', '')
        except Exception as e:
            print(e)
            Next_due_date = ''

        if Next_due_date and '</td>' in Next_due_date:
            Next_due_date = Next_due_date.split('</td>')[0].strip()

        try:
            Total_Overdue_amount  = [
                item for item in cleaned_text.replace('&=nbsp;', '').split('Total Overdue amount')[-1].strip().split('</td>') if item.strip()
                ][0].split('nowrap="">')[-1].strip().replace('=', '').strip().split('"data">')[-1].replace('&nbsp;', '')
        except Exception as e:
            print(e)
            Total_Overdue_amount = ''

        if Total_Overdue_amount and '</td>' in Total_Overdue_amount:
            Total_Overdue_amount = Total_Overdue_amount.split('</td>')[0].strip()

        try:
            Credit_Shield_Flag_or_Uniq_acno  = [
                item for item in cleaned_text.replace('&=nbsp;', '').split('Credit Shield Flag / Uniq=_acno')[-1].strip().split('</td>') if item.strip()
                ][0].split('nowrap="">')[-1].strip().replace('=', '').strip().split('"data">')[-1].replace('&nbsp;', '')
        except Exception as e:
            print(e)
            Credit_Shield_Flag_or_Uniq_acno = ''

        if Credit_Shield_Flag_or_Uniq_acno and '</td>' in Credit_Shield_Flag_or_Uniq_acno:
            Credit_Shield_Flag_or_Uniq_acno = Credit_Shield_Flag_or_Uniq_acno.split('</td>')[0].strip()

        try:
            Outstanding  = [
                item for item in cleaned_text.replace('&=nbsp;', '').split('Outstanding')[-1].strip().split('</td>') if item.strip()
                ][0].split('nowrap="">')[-1].strip().replace('=', '').strip().split('"data">')[-1].replace('&nbsp;', '')
        except Exception as e:
            print(e)
            Outstanding = ''

        if Outstanding and '</td>' in Outstanding:
            Outstanding = Outstanding.split('</td>')[0].strip()

        try:
            Principal_OS  = [
                item for item in cleaned_text.replace('&=nbsp;', '').split('Principal OS')[-1].strip().split('</td>') if item.strip()
                ][0].split('nowrap="">')[-1].strip().replace('=', '').strip().split('"data">')[-1].replace('&nbsp;', '')
        except Exception as e:
            print(e)
            Principal_OS = ''

        if Principal_OS and '</td>' in Principal_OS:
            Principal_OS = Principal_OS.split('</td>')[0].strip()

        try:
            Interest_Profit_OS  = [
                item for item in cleaned_text.replace('&=nbsp;', '').split('Interest / Profit OS')[-1].strip().split('</td>') if item.strip()
                ][0].split('nowrap="">')[-1].strip().replace('=', '').strip().split('"data">')[-1].replace('&nbsp;', '')
        except Exception as e:
            print(e)
            Interest_Profit_OS = ''

        if Interest_Profit_OS and '</td>' in Interest_Profit_OS:
            Interest_Profit_OS = Interest_Profit_OS.split('</td>')[0].strip()
            	
        try:
            Last_payment_date  = [
                item for item in cleaned_text.replace('&=nbsp;', '').split('Last payment date')[-1].strip().split('</td>') if item.strip()
                ][0].split('nowrap="">')[-1].strip().replace('=', '').strip().split('"data">')[-1].replace('&nbsp;', '')
        except Exception as e:
            print(e)
            Last_payment_date = ''

        if Last_payment_date and '</td>' in Last_payment_date:
            Last_payment_date = Last_payment_date.split('</td>')[0].strip()
        
        try:
            Last_payment_amount  = [
                item for item in cleaned_text.replace('&=nbsp;', '').split('Last payment amount')[-1].strip().split('</td>') if item.strip()
                ][0].split('nowrap="">')[-1].strip().replace('=', '').strip().split('"data">')[-1].replace('&nbsp;', '')
        except Exception as e:
            print(e)
            Last_payment_amount = ''

        if Last_payment_amount and '</td>' in Last_payment_amount:
            Last_payment_amount = Last_payment_amount.split('</td>')[0].strip()
        
        try:
            Card_status  = [
                item for item in cleaned_text.replace('&=nbsp;', '').split('Card status')[-1].strip().split('</td>') if item.strip()
                ][0].split('nowrap="">')[-1].strip().replace('=', '').strip().split('"data">')[-1].replace('&nbsp;', '')
        except Exception as e:
            print(e)
            Card_status = ''

        if Card_status and '</td>' in Card_status:
            Card_status = Card_status.split('</td>')[0].strip()

        try:
            PROD_STATUS  = [
                item for item in cleaned_text.replace('&=nbsp;', '').split('PROD')[-1].strip().split('</td>') if item.strip()
                ][0].split('nowrap="">')[-1].strip().replace('=', '').strip().split('"data">')[-1].replace('&nbsp;', '')
        except Exception as e:
            print(e)
            PROD_STATUS = ''

        if PROD_STATUS and '</td>' in PROD_STATUS:
            PROD_STATUS = PROD_STATUS.split('</td>')[0].strip()

        try:
            Product_Code  = [
                item for item in cleaned_text.replace('&=nbsp;', '').split('Product Code')[-1].strip().split('</td>') if item.strip()
                ][0].split('nowrap="">')[-1].strip().replace('=', '').strip().split('"data">')[-1].replace('&nbsp;', '')
        except Exception as e:
            print(e)
            Product_Code = ''

        if Product_Code and '</td>' in Product_Code:
            Product_Code = Product_Code.split('</td>')[0].strip()
        
        try:
            Product_Desc  = [
                item for item in cleaned_text.replace('&=nbsp;', '').split('Product Desc')[-1].strip().split('</td>') if item.strip()
                ][0].split('nowrap="">')[-1].strip().replace('=', '').strip().split('"data">')[-1].replace('&nbsp;', '')
        except Exception as e:
            print(e)
            Product_Desc = ''

        if Product_Desc and '</td>' in Product_Desc:
            Product_Desc = Product_Desc.split('</td>')[0].strip()
        
        try:
            Queue_Agent  = [
                item for item in cleaned_text.replace('&=nbsp;', '').split('Queue / Agent')[-1].strip().split('</td>') if item.strip()
                ][0].split('nowrap="">')[-1].strip().replace('=', '').strip().split('"data">')[-1].replace('&nbsp;', '')
        except Exception as e:
            print(e)
            Queue_Agent = ''

        if Queue_Agent and '</td>' in Queue_Agent:
            Queue_Agent = Queue_Agent.split('</td>')[0].strip()

        try:
            OD_Limit_Set_Date  = cleaned_text.split('OD Limit Set Date')[-1].strip().split('</td>')[1].strip().split('class="data">')[-1].replace('&=nbsp;', '')
        except Exception as e:
            print(e)
            OD_Limit_Set_Date = ''

        if OD_Limit_Set_Date and '</td>' in OD_Limit_Set_Date:
            OD_Limit_Set_Date = OD_Limit_Set_Date.split('</td>')[0].strip()
        
        try:
            OD_Limit_End_Date  = cleaned_text.split('OD Limit End Date')[-1].strip().split('</td>')[1].strip().split('class="data">')[-1].replace('&=nbsp;', '').replace('=', '')
        except Exception as e:
            print(e)
            OD_Limit_End_Date = ''

        if OD_Limit_End_Date and '</td>' in OD_Limit_End_Date:
            OD_Limit_End_Date = OD_Limit_End_Date.split('</td>')[0].strip()
        
        
        # try:
        #     Days_Past_Due  = [
        #         item for item in cleaned_text.replace('&=nbsp;', '').split('Days Past Due')[-1].strip().split('</td>') if item.strip()
        #         ][0].split('nowrap="">')[-1].strip().replace('=', '').strip().split('"data">')[-1].replace('&nbsp;', '')
        # except Exception as e:
        #     print(e)
        #     Days_Past_Due = ''

        # if Days_Past_Due and '</td>' in Days_Past_Due:
        #     Days_Past_Due = Days_Past_Due.split('</td>')[0].strip()
        
        # print(Days_Past_Due)
        # return
        
        try:
            Current_Balance  = [
                item for item in cleaned_text.replace('&=nbsp;', '').split('Current Balance')[-1].strip().split('</td>') if item.strip()
                ][0].split('nowrap="">')[-1].strip().replace('=', '').strip().split('"data">')[-1].replace('&nbsp;', '')
        except Exception as e:
            print(e)
            Current_Balance = ''

        if Current_Balance and '</td>' in Current_Balance:
            Current_Balance = Current_Balance.split('</td>')[0].strip()


        try:
            Interest_Amount  = [
                item for item in cleaned_text.replace('&=nbsp;', '').split('Interest Amount')[-1].strip().split('</td>') if item.strip()
                ][0].split('nowrap="">')[-1].strip().replace('=', '').strip().split('"data">')[-1].replace('&nbsp;', '')
        except Exception as e:
            print(e)
            Interest_Amount = ''

        if Interest_Amount and '</td>' in Interest_Amount:
            Interest_Amount = Interest_Amount.split('</td>')[0].strip()

        try:
            Utilisation  = [
                item for item in cleaned_text.replace('&=nbsp;', '').split('Utilisation')[-1].strip().split('</td>') if item.strip()
                ][0].split('nowrap="">')[-1].strip().replace('=', '').strip().split('"data">')[-1].replace('&nbsp;', '')
        except Exception as e:
            print(e)
            Utilisation = ''

        if Utilisation and '</td>' in Utilisation:
            Utilisation = Utilisation.split('</td>')[0].strip()
        
        try:
            Interest_In_Suspense  = [
                item for item in cleaned_text.replace('&=nbsp;', '').split('Interest In Suspense')[-1].strip().split('</td>') if item.strip()
                ][0].split('nowrap="">')[-1].strip().replace('=', '').strip().split('"data">')[-1].replace('&nbsp;', '')
        except Exception as e:
            print(e)
            Interest_In_Suspense = ''

        if Interest_In_Suspense and '</td>' in Interest_In_Suspense:
            Interest_In_Suspense = Interest_In_Suspense.split('</td>')[0].strip()

        try:
            Total_Due  = [
                item for item in cleaned_text.replace('&=nbsp;', '').split('Total Due')[-1].strip().split('</td>') if item.strip()
                ][0].split('nowrap="">')[-1].strip().replace('=', '').strip().split('"data">')[-1].replace('&nbsp;', '')
        except Exception as e:
            print(e)
            Total_Due = ''

        if Total_Due and '</td>' in Total_Due:
            Total_Due = Total_Due.split('</td>')[0].strip()

        try:
            Expiry_flag  = [
                item for item in cleaned_text.replace('&=nbsp;', '').split('Expiry flag')[-1].strip().split('</td>') if item.strip()
                ][0].split('nowrap="">')[-1].strip().replace('=', '').strip().split('"data">')[-1].replace('&nbsp;', '')
        except Exception as e:
            print(e)
            Expiry_flag = ''

        if Expiry_flag and '</td>' in Expiry_flag:
            Expiry_flag = Expiry_flag.split('</td>')[0].strip()

        
        try:
            Current_Bucket_amount  = [
                item for item in cleaned_text.replace('&=nbsp;', '').split('Current Bucket amount')[-1].strip().split('</td>') if item.strip()
                ][0].split('nowrap="">')[-1].strip().replace('=', '').strip().split('"data">')[-1].replace('&nbsp;', '')
        except Exception as e:
            print(e)
            Current_Bucket_amount = ''

        if Current_Bucket_amount and '</td>' in Current_Bucket_amount:
            Current_Bucket_amount = Current_Bucket_amount.split('</td>')[0].strip()
        
        try:
            Bucket_1_amount  = [
                item for item in cleaned_text.replace('&=nbsp;', '').split('Bucket 1 amount')[-1].strip().split('</td>') if item.strip()
                ][0].split('nowrap="">')[-1].strip().replace('=', '').strip().split('"data">')[-1].replace('&nbsp;', '')
        except Exception as e:
            print(e)
            Bucket_1_amount = ''

        if Bucket_1_amount and '</td>' in Bucket_1_amount:
            Bucket_1_amount = Bucket_1_amount.split('</td>')[0].strip()
        
        try:
            Bucket_2_amount  = [
                item for item in cleaned_text.replace('&=nbsp;', '').split('Bucket 2 amount')[-1].strip().split('</td>') if item.strip()
                ][0].split('nowrap="">')[-1].strip().replace('=', '').strip().split('"data">')[-1].replace('&nbsp;', '')
        except Exception as e:
            print(e)
            Bucket_2_amount = ''

        if Bucket_2_amount and '</td>' in Bucket_2_amount:
            Bucket_2_amount = Bucket_2_amount.split('</td>')[0].strip()
        
        try:
            Bucket_3_amount  = [
                item for item in cleaned_text.replace('&=nbsp;', '').split('Bucket 3 amount')[-1].strip().split('</td>') if item.strip()
                ][0].split('nowrap="">')[-1].strip().replace('=', '').strip().split('"data">')[-1].replace('&nbsp;', '')
        except Exception as e:
            print(e)
            Bucket_3_amount = ''

        if Bucket_3_amount and '</td>' in Bucket_3_amount:
            Bucket_3_amount = Bucket_3_amount.split('</td>')[0].strip()
        
        try:
            Bucket_4_amount  = [
                item for item in cleaned_text.replace('&=nbsp;', '').split('Bucket 4 amount')[-1].strip().split('</td>') if item.strip()
                ][0].split('nowrap="">')[-1].strip().replace('=', '').strip().split('"data">')[-1].replace('&nbsp;', '')
        except Exception as e:
            print(e)
            Bucket_4_amount = ''

        if Bucket_4_amount and '</td>' in Bucket_4_amount:
            Bucket_4_amount = Bucket_4_amount.split('</td>')[0].strip()
        
        try:
            Bucket_5_amount  = [
                item for item in cleaned_text.replace('&=nbsp;', '').split('Bucket 5 amount')[-1].strip().split('</td>') if item.strip()
                ][0].split('nowrap="">')[-1].strip().replace('=', '').strip().split('"data">')[-1].replace('&nbsp;', '')
        except Exception as e:
            print(e)
            Bucket_5_amount = ''

        if Bucket_5_amount and '</td>' in Bucket_5_amount:
            Bucket_5_amount = Bucket_5_amount.split('</td>')[0].strip()
        
        try:
            Bucket_6_amount  = [
                item for item in cleaned_text.replace('&=nbsp;', '').split('Bucket 6 amount')[-1].strip().split('</td>') if item.strip()
                ][0].split('nowrap="">')[-1].strip().replace('=', '').strip().split('"data">')[-1].replace('&nbsp;', '')
        except Exception as e:
            print(e)
            Bucket_6_amount = ''

        if Bucket_6_amount and '</td>' in Bucket_6_amount:
            Bucket_6_amount = Bucket_6_amount.split('</td>')[0].strip()
        
        try:
            Bucket_greater_6_amount  = [
                item for item in cleaned_text.replace('&=nbsp;', '').split('Bucket greater 6 amount')[-1].strip().split('</td>') if item.strip()
                ][0].split('nowrap="">')[-1].strip().replace('=', '').strip().split('"data">')[-1].replace('&nbsp;', '')
        except Exception as e:
            print(e)
            Bucket_greater_6_amount = ''

        if Bucket_greater_6_amount and '</td>' in Bucket_greater_6_amount:
            Bucket_greater_6_amount = Bucket_greater_6_amount.split('</td>')[0].strip()

        scrape_date = date.today()
        # scrape_date = '2025-04-13'
        items = parser.xpath(xpath_data)
        data = {}
        for item in items:
            items1 = item.xpath('.//td[contains(@class, "ez1")]//text()')
            items2 = item.xpath('.//td[contains(@class, "data")]//text()')
            data1 = [
                i.strip().replace('\r\n', '').replace('&nbs=p;', '').replace('&=nbsp;', '').replace('&nbsp=;', '').replace('=', '').replace('&nbsp;', '') for i in items1 if i.strip().replace('\r\n', '').replace('&nbs=p;', '')
            ]
            data2 = [
                i.strip().replace('\r\n', '').replace('&nbs=p;', '').replace('&=nbsp;', '').replace('&nbsp=;', '').replace('=', '').replace('&nbsp;', '') for i in items2 if i.strip().replace('\r\n', '').replace('&nbs=p;', '')
            ]
            data_items = dict(zip(data1, data2))

            if 'PROD' in data_items:
                PROD = clean(''.join(data_items.get('PROD', '')).strip())
                data['PROD'] = PROD if PROD else ''
            if 'CID No.' in data_items:
                cid_no = clean(''.join(data_items.get('CID No.', '')).strip())
                Card_type = clean(''.join(data_items.get('Card type', '')).strip())
                MinimumPayment_Amount = clean(data_items.get('MinimumPayment Amount', ''))
                if MinimumPayment_Amount and '</td>' in MinimumPayment_Amount:
                    MinimumPayment_Amount = MinimumPayment_Amount.split('</td>')[0].strip()

                data['cid_no'] = str(cid_no).replace('&nbsp;', '') if cid_no else ''
                data['Card_type'] = str(Card_type).replace('&nbsp;', '') if Card_type else ''
                data['MinimumPayment_Amount'] = str(MinimumPayment_Amount).replace('&nbsp;', '') if MinimumPayment_Amount else ''

            elif 'A/C No.' in data_items:
                A_C_no = data_items.get('A/C No.', '')
                Credit_card_limit = clean(data_items.get('Credit card limit', ''))
                Last_statement_date = clean(data_items.get('Last statement date', ''))
                # Card_Days_past_due = clean(data_items.get('Days past due', ''))
                # if Card_Days_past_due and '</td>' in Card_Days_past_due:
                #     Card_Days_past_due = Card_Days_past_due.split('</td>')[0].strip()
                if A_C_no and 'td>' in A_C_no:
                    A_C_no = A_C_no.split('td>')[0].strip()
                try:
                    A_C_no = [part.strip() for part in A_C_no.replace('\xa0', '').split('\t') if part.strip()][0]
                except Exception as e:
                    print(e)
                    A_C_no = ''
                data['A_C_no'] = str(A_C_no).replace('&nbsp;', '').replace('&nbsp;', '') if A_C_no  and len(A_C_no) < 50 else ''
                data['Last_statement_date'] = str(Last_statement_date).replace('&nbsp;', '') if Last_statement_date and len(Last_statement_date) < 30 else ''
                data['Credit_card_limit'] = str(Credit_card_limit).replace('&nbsp;', '') if Credit_card_limit and len(Credit_card_limit) < 30 else ''
                # data['Card_Days_past_due'] = str(Card_Days_past_due).replace('&nbsp;', '') if Card_Days_past_due and len(Card_Days_past_due) < 30 else ''

        data['Issue_date'] = clean(Issue_date).replace('&nbsp;', '') if Issue_date and len(Issue_date) < 10 else ''
        data['Next_due_date'] = clean(Next_due_date).replace('&nbsp;', '') if Next_due_date and len(Next_due_date) < 10 else ''
        data['Total_Overdue_amount'] = clean(Total_Overdue_amount).replace('&nbsp;', '') if Total_Overdue_amount and len(Total_Overdue_amount) < 10 else ''
        data['Credit_Shield_Flag_or_Uniq_acno'] = clean(Credit_Shield_Flag_or_Uniq_acno).replace('&nbsp;', '') if Credit_Shield_Flag_or_Uniq_acno and len(Credit_Shield_Flag_or_Uniq_acno) < 25 else ''
        data['Outstanding'] = clean(Outstanding).replace('&nbsp;', '') if Outstanding and len(Outstanding) < 25 else ''
        data['Principal_OS'] = clean(Principal_OS).replace('&nbsp;', '') if Principal_OS and len(Principal_OS) < 25 else ''
        data['Interest_Profit_OS'] = clean(Interest_Profit_OS).replace('&nbsp;', '') if Interest_Profit_OS and len(Interest_Profit_OS) < 25 else ''
        data['Last_payment_date'] = clean(Last_payment_date).replace('&nbsp;', '') if Last_payment_date and len(Last_payment_date) < 25 else ''
        data['Last_payment_amount'] = clean(Last_payment_amount).replace('&nbsp;', '') if Last_payment_amount and len(Last_payment_amount) < 25 else ''
        data['scrape_date'] = str(scrape_date).replace('&nbsp;', '') if scrape_date else ''
        data['Product_Code'] = str(Product_Code).replace('&nbsp;', '') if Product_Code and len(Product_Code) < 30 else ''
        data['OD_Limit_Set_Date'] = str(OD_Limit_Set_Date).replace('&nbsp;', '') if OD_Limit_Set_Date and len(OD_Limit_Set_Date) < 20 else ''
        data['OD_Limit_End_Date'] = str(OD_Limit_End_Date).replace('&nbsp;', '') if OD_Limit_End_Date and len(OD_Limit_End_Date) < 20 else ''
        # data['Days_Past_Due'] = str(Days_Past_Due).replace('&nbsp;', '') if Days_Past_Due and len(Days_Past_Due) < 20 else ''
        data['Current_Balance'] = str(Current_Balance).replace('&nbsp;', '') if Current_Balance and len(Current_Balance) < 20 else ''
        data['Interest_Amount'] = str(Interest_Amount).replace('&nbsp;', '') if Interest_Amount and len(Interest_Amount) < 20 else ''
        data['Utilisation'] = str(Utilisation).replace('&nbsp;', '') if Utilisation and len(Utilisation) < 20 else ''
        data['Interest_In_Suspense'] = str(Interest_In_Suspense).replace('&nbsp;', '') if Interest_In_Suspense and len(Interest_In_Suspense) < 20 else ''
        data['Total_Due'] = str(Total_Due).replace('&nbsp;', '') if Total_Due and len(Total_Due) < 20 else ''
        data['Expiry_flag'] = str(Expiry_flag).replace('&nbsp;', '') if Expiry_flag and len(Expiry_flag) < 20 else ''

        data['Current_Bucket_amount'] = str(Current_Bucket_amount).replace('&nbsp;', '') if Current_Bucket_amount and len(Current_Bucket_amount) < 20 else ''
        data['Bucket_1_amount'] = str(Bucket_1_amount).replace('&nbsp;', '') if Bucket_1_amount and len(Bucket_1_amount) < 20 else ''
        data['Bucket_2_amount'] = str(Bucket_2_amount).replace('&nbsp;', '') if Bucket_2_amount and len(Bucket_2_amount) < 20 else ''
        data['Bucket_3_amount'] = str(Bucket_3_amount).replace('&nbsp;', '') if Bucket_3_amount and len(Bucket_3_amount) < 20 else ''
        data['Bucket_4_amount'] = str(Bucket_4_amount).replace('&nbsp;', '') if Bucket_4_amount and len(Bucket_4_amount) < 20 else ''
        data['Bucket_5_amount'] = str(Bucket_5_amount).replace('&nbsp;', '') if Bucket_5_amount and len(Bucket_5_amount) < 20 else ''
        data['Bucket_6_amount'] = str(Bucket_6_amount).replace('&nbsp;', '') if Bucket_6_amount and len(Bucket_6_amount) < 20 else ''
        data['Bucket_greater_6_amount'] = str(Bucket_greater_6_amount).replace('&nbsp;', '') if Bucket_greater_6_amount and len(Bucket_greater_6_amount) < 20 else ''
        # yield Product(**data)
        return data

    def parse1(self, response):
        parser = html.fromstring(response.text)

        xpath_address2 = "//td[contains(text(), 'Address')]//parent::tr//following-sibling::tr[1]/td[2]//text()"
        xpath_address3 = "//td[contains(text(), 'Address')]//parent::tr//following-sibling::tr[2]/td[2]//text()"
        xpath_data = "//td[contains(text(), 'CID No.')]//parent::tr//parent::tbody//tr"

        cleaned_text = response.text.replace("=3D", "=").replace("\n", "").replace("\r", "").replace("\t", "").replace("&nbsp;", " ").strip()

        address2 = ''.join(parser.xpath(xpath_address2)).strip().replace('=', '')
        address3 = ''.join(parser.xpath(xpath_address3)).strip().replace('=', '').replace('&nbs', '').replace('p;', '')
        try:
            total_os_elements = [
                item for item in cleaned_text.split('Total OS', 1)[-1].strip().split('</td>') if item.strip()
                ][0].split('nowrap="">')[-1].strip().replace('=', '').strip()
        except Exception as e:
            print(e)
            total_os_elements = ''
        if '</td>' in total_os_elements:
            total_os_elements = total_os_elements.split('</td>')[0].strip()
        try:
            employer_name = [
                item for item in cleaned_text.replace('&=nbsp;', '').split('Employer Name', 1)[-1].strip().split('</td>') if item.strip()
                ][0].split('nowrap="">')[-1].strip().replace('=', '').strip().split('"data">')[-1]
        except Exception as e:
            print(e)
            employer_name = ''
        if '</td>' in employer_name:
            employer_name = employer_name.split('</td>')[0].strip()
        try:
            Mobile_Number = [
                item for item in cleaned_text.replace('&=nbsp;', '').split('Mobile Number', 1)[-1].strip().split('</td>') if item.strip()
                ][0].split('nowrap="">')[-1].strip().replace('=', '').strip().split('"data">')[-1].replace('&nbsp;', '')
        except Exception as e:
            print(e)
            Mobile_Number = ''
        if '</td>' in Mobile_Number:
            Mobile_Number = Mobile_Number.split('</td>')[0].strip()
        try:
            Office_Numbers  = [
                item for item in cleaned_text.replace('&=nbsp;', '').split('Office1  /  Of=fice 2 Number')[-1].strip().split('</td>') if item.strip()
                ][0].split('nowrap="">')[-1].strip().replace('=', '').strip().split('"data">')[-1].replace('&nbsp;', '')
        except Exception as e:
            print(e)
            Office_Numbers = ''
        if '</td>' in Office_Numbers:
            Office_Numbers = Office_Numbers.split('</td>')[0].strip()
        try:
            Ref_name_mobile  = [
                item for item in cleaned_text.replace('&=nbsp;', '').split('Ref Name  /  R=ef Mob')[-1].strip().split('</td>') if item.strip()
                ][0].split('nowrap="">')[-1].strip().replace('=', '').strip().split('"data">')[-1].replace('&nbsp;', '')
        except Exception as e:
            print(e)
            Ref_name_mobile = ''
        if '</td>' in Ref_name_mobile:
            Ref_name_mobile = Ref_name_mobile.split('</td>')[0].strip()
        try:
            Email_ID  = [
                item for item in cleaned_text.replace('&=nbsp;', '').split('Email ID =')[-1].strip().split('</td>') if item.strip()
                ][0].split('nowrap="">')[-1].strip().replace('=', '').strip().split('"data">')[-1].replace('&nbsp;', '')
        except Exception as e:
            print(e)
            Email_ID = ''
        try:
            Home_Country_Number  = [
                item for item in cleaned_text.replace('&=nbsp;', '').split('Home Country N=umber')[-1].strip().split('</td>') if item.strip()
                ][0].split('nowrap="">')[-1].strip().replace('=', '').strip().split('"data">')[-1].replace('&nbsp;', '')
        except Exception as e:
            print(e)
            Home_Country_Number = ''
        if '</td>' in Home_Country_Number:
            Home_Country_Number = Home_Country_Number.split('</td>')[0].strip()
        try:
            Designation_Occupation = [
                item for item in cleaned_text.replace('&=nbsp;', '').split('Designation  /=  Occupation')[-1].strip().split('</td>') if item.strip()
                ][0].split('nowrap="">')[-1].strip().replace('=', '').strip().split('"data">')[-1].replace('&nbsp;', '')
        except Exception as e:
            print(e)
            Designation_Occupation = ''

        if '</td>' in Designation_Occupation:
            Designation_Occupation = Designation_Occupation.split('</td>')[0].strip()

        try:
            Emirates_id = [
                item for item in str(cleaned_text).replace('&nb=sp;', '').split('Emirates ID')[-1].strip().split('</td>') if item.strip()
                ][0].split('nowrap="">')[-1].strip().replace('=', '').strip().split('"data">')[-1].replace('&nbsp;', '')
        except Exception as e:
            print(e)
            Emirates_id = ''
        if '</td>' in Emirates_id:
            Emirates_id = Emirates_id.split('</td>')[0].strip()
        try:
            address1 = [
                item for item in str(cleaned_text).split('class="ez1">Address')[-1].strip().split('</td>') if item.strip()
                ][0].split('nowrap="">')[-1].strip().replace('=', '').strip().split('"data">')[-1].replace('&nbsp;', '')
        except Exception as e:
            print(e)
            address1 = ''
        try:
            Residence_number = [
                item for item in str(cleaned_text).split('Residence1  / = Residence 2 Number')[-1].strip().split('</td>') if item.strip()
                ][0].split('nowrap="">')[-1].strip().replace('=', '').strip().split('"data">')[-1].replace('&nbsp;', '')
        except Exception as e:
            print(e)
            Residence_number = ''
        if '</td>' in Residence_number:
            Residence_number = Residence_number.split('</td>')[0].strip()
        
        try:
            Region = [
                item for item in str(cleaned_text).split('Region')[-1].strip().split('</td>') if item.strip()
                ][0].split('nowrap="">')[-1].strip().replace('=', '').strip().split('"data">')[-1].replace('&nbsp;', '')
        except Exception as e:
            print(e)
            Region = ''
        if '</td>' in Region:
            Region = Region.split('</td>')[0].strip()

        address1 = address1.split('</td>')[0].strip() if '</td>' in address1 else address1
        address = clean(', '.join(list(filter(None, [address1,address2,address3]))))
        # scrape_date = date.today()
        scrape_date = '2025-04-13'
        items = parser.xpath(xpath_data)
        data = {}
        for item in items:
            items1 = item.xpath('.//td[contains(@class, "ez1")]//text()')
            items2 = item.xpath('.//td[contains(@class, "data")]//text()')
            data1 = [
                i.strip().replace('\r\n', '').replace('&nbs=p;', '').replace('&=nbsp;', '').replace('&nbsp=;', '').replace('=', '').replace('&nbsp;', '') for i in items1 if i.strip().replace('\r\n', '').replace('&nbs=p;', '')
            ]
            data2 = [
                i.strip().replace('\r\n', '').replace('&nbs=p;', '').replace('&=nbsp;', '').replace('&nbsp=;', '').replace('=', '').replace('&nbsp;', '') for i in items2 if i.strip().replace('\r\n', '').replace('&nbs=p;', '')
            ]
            data_items = dict(zip(data1, data2))
            if 'CID No.' in data_items:
                cid_no = clean(''.join(data_items.get('CID No.', '')).strip())
                nationality_passport = data_items.get('Nationality  /  Passport', '').split('/')
                nationality, passport_no = clean(''.join(nationality_passport[0]).strip()), clean(''.join(nationality_passport[-1]).strip())
                data['cid_no'] = cid_no.replace('&nbsp;', '') if cid_no else ''
                data['nationality'] = nationality.replace('&nbsp;', '') if nationality else ''
                data['passport_no'] = passport_no.replace('&nbsp;', '') if passport_no else ''
            elif 'Name' in data_items:
                gender_date_of_birth = data_items.get('Gender  /  Date Of Birth', '').split('/')
                gender, date_of_birth = gender_date_of_birth[0].strip(), gender_date_of_birth[-1].strip()
                # office_number = data_items.get('Office1  /  Office 2 Number', '').replace('/', '').strip()
                data['name'] = clean(data_items.get('Name', '')).replace('&nbsp;', '')
                data['gender'] = clean(gender).replace('&nbsp;', '')
                data['date_of_birth'] = clean(date_of_birth).replace('&nbsp;', '')
        data['total_os'] = clean(total_os_elements).replace('&nbsp;', '') if total_os_elements else None
        data['employer_name'] = clean(employer_name).replace('&nbsp;', '') if employer_name else None
        data['Mobile_Number'] = clean(Mobile_Number).replace('&nbsp;', '') if Mobile_Number else None
        data['Office_Numbers'] = clean(Office_Numbers).replace('&nbsp;', '') if Office_Numbers else None
        data['Reference_name_mobile'] = clean(Ref_name_mobile).replace('&nbsp;', '') if Ref_name_mobile else None
        data['Email_ID'] = clean(Email_ID).replace('&nbsp;', '') if Email_ID else None
        data['Home_Country_Number'] = clean(Home_Country_Number).replace('&nbsp;', '') if Home_Country_Number else None
        data['Designation_Occupation'] = clean(Designation_Occupation).replace('&nbsp;', '') if Designation_Occupation else None
        data['Emirates_id'] = clean(Emirates_id).replace('&nbsp;', '') if Emirates_id else None
        data['address'] = clean(address).replace('&nbsp;', '') if address else None
        data['Residence_number'] = clean(Residence_number).replace('&nbsp;', '') if Residence_number else None
        data['scrape_date'] = str(scrape_date).replace('&nbsp;', '') if scrape_date else ''
        data['Region'] = str(Region).replace('&nbsp;', '') if Region else ''
        # yield Product(**data)
        return data
        # print(data)

import requests, re
from bs4 import BeautifulSoup
import sys
import os

def bls_base(n):
    try:
        bls_category_dict = {}
        url = 'http://www.bls.gov/oes/2016/may/oes151131.htm'
        try:
            req = requests.get(url)
        except Exception as e:
            bls_category_dict = None
            return bls_category_dict
        soup = BeautifulSoup(req.content, 'lxml')
        data = []
        if req.status_code == 200:
            keys_table = []
            values_tab = []
            try:
                card = soup.find('div', id='bodytext').find_all('table')[n]
            except:
                card = []
            try:
                trs = card.find_all('tr')
            except:
                trs = None
            for i,tr in enumerate(trs):
                regex_brackets =re.compile(r"\((\d+)\)")
                if i==0:
                    try:
                        key_th = tr.find_all('th')
                    except:
                        key_th = None
                    for j in key_th:
                        key_name = j.text.strip()
                        key_desc_check = bool(regex_brackets.search(key_name))
                        regex_word_check = re.compile(r"%\((\w+)\)")
                        word_check = bool(regex_word_check.search(key_name))
                        if word_check is True:
                            key_name = regex_word_check.sub('',key_name)
                            key_name = '{0}%'.format(key_name)
                        else:
                            if key_desc_check is True:
                                key_name = regex_brackets.sub('',key_name).strip()
                                key_name = key_name.replace(' ','_').lower()
                            else:
                                key_name = key_name.replace(' ','_').replace('(','_').replace(')','').lower()
                        keys_table.append(key_name)
                else:
                    try:
                        value_tr = tr.find_all('td')
                    except:
                        value_tr = None
                    range_keys = len(keys_table)
                    for k in range(range_keys):
                        try:
                            value = value_tr[k].text.strip()
                        except:
                            value = None
                        regex_row_check = re.compile(r"\w+\s\((\d+)\)")
                        row_check = bool(regex_row_check.findall(value))
                        if row_check is True:
                            value = regex_brackets.sub('',value).strip()
                        else:
                            value_check = bool(regex_brackets.search(value))
                            if value_check is True:
                                value = None
                            else:
                                value = value
                        values_tab.append(value)
            values_table = []
            for i in range(0,len(values_tab),len(keys_table)):
                values_table.append(values_tab[i:i+len(keys_table)])
            for val in values_table:
                obj = {}
                for index,ele in enumerate(val):
                    obj[keys_table[index]] = ele
                data.append(obj)
            bls_category_dict['data'] = data
            return bls_category_dict
    except Exception as e:
        print(str(e))
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return None


def bls_category():
    try:
        blsDict = {}
        blsDict['success'] = True
        try:
            national_estimates_Dict = {}
            national_estimates_Dict['employment_mean_wage_estimates'] = bls_base(n=0)
            national_estimates_Dict['percentile_wage_estimates'] = bls_base(n=1)
            industry_profile_Dict = {}
            industry_profile_Dict['industry_high_levels_employments'] = bls_base(n=2)
            industry_profile_Dict['industry_high_concentration_employments'] = bls_base(n=3)
            industry_profile_Dict['industry_top_paying_industries'] = bls_base(n=4)
            geography_profile_Dict = {}
            geography_profile_Dict['highest_employment_level_state'] = bls_base(n=5)
            geography_profile_Dict['highest_conc_job_loc_quotient_state'] = bls_base(n=6)
            geography_profile_Dict['top_paying_states'] = bls_base(n=7)
            geography_profile_Dict['highest_employment_level_metropolitan_areas'] = bls_base(n=8)
            geography_profile_Dict['highest_conc_job_loc_quotient_metropolitan_areas'] = bls_base(n=9)
            geography_profile_Dict['top_paying_metropolitan_areas'] = bls_base(n=10)
            geography_profile_Dict['highest_employment_non_metropolitan_areas'] = bls_base(n=11)
            geography_profile_Dict['highest_conc_job_loc_quotient_non_metropolitan_areas'] = bls_base(n=12)
            geography_profile_Dict['top_paying_non_metropolitan_areas'] = bls_base(n=13)
            blsDict['national_estimates'] = national_estimates_Dict
            blsDict['industry_profile_Dict'] = industry_profile_Dict
            blsDict['geography_profile'] = geography_profile_Dict
            return blsDict
        except Exception as e:
            blsDict['success'] = False
            return blsDict
    except Exception as e:
        print(str(e))
        return None


print(bls_category())
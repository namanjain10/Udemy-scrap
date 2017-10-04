import requests
import json
import pandas as pd

base_url = 'https://www.udemy.com'
mid_url = '/api-2.0/channels/'
change_url = '/courses?is_angular_app=true&is_topic_filters_enabled=true&p=1'

code = 1624
url = base_url + mid_url + str(code) + change_url
list_courses = []

while code <= 1652 :
    print ('code', code)
    
    url = base_url + mid_url + str(code) + change_url
    
    while 1 :
        
        r = requests.get(url)
        e = json.loads(r.text)
        
        n = len(e['results'])
        
        for i in range (0,n) :
            
            dic = {}
            
            #cat_id = e['results'][i]['id']
            cat_title = e['results'][i]['title']
            cat_url = e['results'][i]['url']
            
            try :
                cat_net_price = e['results'][i]['discount']['list_price']['amount']
            except :
                cat_net_price = 0
            
            try :   
                cat_price = e['results'][i]['discount']['price']['amount']
                
            except :
                cat_price = 0
            
            try :    
            	cat_subs = e['results'][i]['num_subscribers']
            except :
            	cat_subs = 0
            	
            try :
            	cat_rating = e['results'][i]['avg_rating_recent']
            	
            except :
            	cat_rating = 0
            
            try :	
            	cat_caption = e['results'][i]['caption_languages']
            
            except :
            	cat_caption = '-'
            	
            try :
            	cat_last_updated = e['results'][i]['published_time']
			
			except :
            	cat_last_updated = '-'
            	
			try :
            	cat_lang = e['results'][i]['locale']['english_title']
            
            except :
            	cat_lang = '-'
            	
            	
            cat_inst_name = []
            cat_inst_job = []
            
            number = len(e['results'][i]['visible_instructors'])
            
            for k in range (0,number) :
            
            	try :
                	cat_inst_name.append(e['results'][i]['visible_instructors'][k]['display_name'])
                
                except :
                	cat_inst_name.append('-')
                	
                try :
                	cat_inst_job.append(e['results'][i]['visible_instructors'][k]['job_title'])
                
                except :
                	cat_inst_job.append('-')
                	
            try :    	
            	cat_descr = e['results'][i]['headline']
            
            except :
            	cat_descr = '-'
            	
            re = BeautifulSoup (requests.get(base_url + cat_url).text)
            
            try :
            	cat_inst_desc = re.find("div",{"class" : "instructor__description"}).p.text.strip()
            
            except :
            	cat_inst_desc = '-'
            	
            q = re.find_all("ul",{"class" : "what-you-get__items"})
            num = len(re.find_all('span', {'class':"what-you-get__text"}))
            
            learn = []
            
            for j in range (0,num) :
            	
            	try :
                	learn.append(re.find_all('span', {'class':"what-you-get__text"})[j].text.strip())
        		
            	except :
            		learn.append ('-')
            		
            dic['What Will You Learn'] = learn
            dic['Course Name'] = cat_title
            dic['Brief Description'] = cat_descr
            dic['Rating'] = cat_rating
            dic['Students Enrolled'] = cat_subs
            dic['Last Updated'] = cat_last_updated
            dic['Language'] = cat_lang
            dic['Captions Language'] = cat_caption
            dic['Today Price'] = cat_price
            dic['Normal Price'] = cat_net_price
            dic['Instructor Name'] = cat_inst_name
            dic['Instructor Job'] = cat_inst_job
            dic['Instructor Description'] = cat_inst_desc
            
            list_courses.append(dic)
        
        print ('current', e['pagination']['current_page'] , 'last ', e['pagination']['total_page'] )
        
        if e['pagination']['current_page'] == e['pagination']['total_page'] :
            break
        
        url = base_url + e['pagination']['next']['url']

    code += 2
    
pd.DataFrame (list_courses).to_csv('myfile.csv',header = True, index = False)

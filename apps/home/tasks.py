
from io import StringIO
from pytrends.request import TrendReq
import pandas as pd
import time
from celery import shared_task
from celery_progress.backend import ProgressRecorder

@shared_task(bind=True)
def extract_trends(self, keywords, timeframe): # added timeframe as per Dunc's request
    s = StringIO()
    progress_recorder = ProgressRecorder(self)
    total_kws = len(keywords)
    headers = {
    # 'sec-ch-ua': '"Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"',
    # 'Referer': 'https://trends.google.com/',
    # 'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
    # 'sec-ch-ua-platform': '"Windows"',
    }
    
    # Instantiate pytrends
    pytrend = TrendReq(retries=3,backoff_factor=3, requests_args={'headers': headers})
    # Create final dictionary to save
    kw_dict = {}
    for i,keyword in enumerate(keywords):
        pytrend.build_payload(kw_list=[keyword], geo = 'GB', timeframe = timeframe, cat = 0)
        related_queries= pytrend.related_queries()
        keys = list(related_queries)
        ## Perhaps i can take the keys out and substitute for keyword there
        related_queries ={ 'top': pd.DataFrame.from_dict(related_queries[keys[0]]['top']), 
                        'rising': pd.DataFrame.from_dict(related_queries[keys[0]]['rising'])}
        
        top_rising = pd.concat(related_queries.values(), axis=1 , keys=related_queries.keys()) # axis was changed from 1 to 0
        print(f'hi {i}')
        kw_dict[keyword] = top_rising
        joined = pd.concat(kw_dict.values(), axis=0, keys=kw_dict.keys())
        time.sleep(1)
        progress_recorder.set_progress(i, total_kws, description="Working")

    #rising_df = joined.drop(['top'], axis = 1)
    joined.to_html(s)
    my_html = s.getvalue()
    # we return the In memory item
    
    return my_html
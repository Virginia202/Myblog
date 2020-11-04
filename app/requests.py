import urllib.request,json
from .models import Quote


#Getting URL
base_url = None

def configure_request(app):
    global base_url
    base_url = app.config['QUOTE_API_BASE_URL']
   
  
def get_quotes():
    '''
    Function that gets the json response to our url request
    '''
    with urllib.request.urlopen(base_url) as url:
        get_quotes_data = url.read()
        get_quotes_response = json.loads(get_quotes_data)
        
        quote_results = None
        
        if get_quotes_response:
            quote_results_list = get_quotes_response
            quote_results = process_results(quote_results_list)
    
    return quote_results 

def process_results(quote_results_list):
    '''
    Function that processes the movie result and transform them to a list Objects
    
    Args:
        quote_list: A list of dictionaries that contain movie details
        
    Returns:
        quote_results: A list of quote objects    
    '''
    quote_results = []
    
    id = quote_results_list.get('id')
    author = quote_results_list.get('author')
    quote= quote_results_list.get('quote')
            
    if quote:
        quote_object = Quote(id,author,quote)
        quote_results.append(quote_object)
        
    return quote_results              
        
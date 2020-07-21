from requests import get, post

# Module variables to connect to moodle api:
## Insert token and URL for your site here. 
## Mind that the endpoint can start with "/moodle" depending on your installation.
KEY = "" 
URL = "https://your.moodle.site"
ENDPOINT="/webservice/rest/server.php"

def rest_api_parameters(in_args, prefix='', out_dict=None):
    """Transform dictionary/array structure to a flat dictionary, with key names
    defining the structure.
    Example usage:
    >>> rest_api_parameters({'courses':[{'id':1,'name': 'course1'}]})
    {'courses[0][id]':1,
     'courses[0][name]':'course1'}
    """
    if out_dict==None:
        out_dict = {}
    if not type(in_args) in (list,dict):
        out_dict[prefix] = in_args
        return out_dict
    if prefix == '':
        prefix = prefix + '{0}'
    else:
        prefix = prefix + '[{0}]'
    if type(in_args)==list:
        for idx, item in enumerate(in_args):
            rest_api_parameters(item, prefix.format(idx), out_dict)
    elif type(in_args)==dict:
        for key, item in in_args.items():
            rest_api_parameters(item, prefix.format(key), out_dict)
    return out_dict

def call(fname, **kwargs):
    """Calls moodle API function with function name fname and keyword arguments.
    Example:
    >>> call_mdl_function('core_course_update_courses',
                           courses = [{'id': 1, 'fullname': 'My favorite course'}])
    """
    parameters = rest_api_parameters(kwargs)
    parameters.update({"wstoken": KEY, 'moodlewsrestformat': 'json', "wsfunction": fname})
    #print(parameters)
    response = post(URL+ENDPOINT, data=parameters).json()
    if type(response) == dict and response.get('exception'):
        raise SystemError("Error calling Moodle API\n", response)
    return response

################################################
# Rest-Api classes
################################################

class LocalUpdateSectionformatoptions(object):
    """Updates section format options: Requires courseid and an array with sectionformatoptions"""
    def __init__(self, cid, secformat):
        self.updatesectionformatoptions = call('local_wsmanagesections_update_sectionformatoptions', courseid = cid, sections = secformat)
        
################################################
# Example
################################################

# Update section format options.
courseid = "881" # Exchange with a valid courseid.
# Example for courseformat onetopic.
secformopts = [{'sectionnumber': 4, 'sectionformatoptions': [{'name': 'level', 'value': '1'}]},\
               {'sectionnumber': 3, 'sectionformatoptions': [{'name': 'firsttabtext', 'value': 'General'}]},\
               {'sectionnumber': 5, 'sectionformatoptions': [{'name': 'level', 'value': '1'},\
                                                             {'name': 'firsttabtext', 'value': 'General'}]},\
               {'sectionnumber': 2, 'sectionformatoptions': [{'name': 'firsttabtext', 'value': 'General'}]}]
sec = LocalUpdateSectionformatoptions(courseid, secformopts)
print(sec.updatesectionformatoptions)


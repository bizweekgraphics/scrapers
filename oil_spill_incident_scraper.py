#need loop to grab materials page for a given incident
#going to tell it to count up incident ids, not use an external list of IDs
#you segregate your functions and then stick them together under "main". the reason we chunk it up like this is to add structure in a human-readable form. by chunking it up, we know what the program is doing exactly. 
#we're making a chain of operations that get stuck together at the end. the hard work is figuring out where to break things up and then how to stick them together. "the smallest unit of work we can do"
#next up: soup the materials pages, and find out how to slot them into rows and columns 
#the cookie thing? you do it in a browser, see what gets sent, then find out how to emulate that so it doesnt reject you
#want to end up with, concerning 2013-2014 something akin to the sheets in teh other csvs.  spill details, each in a discrete row that has an incident_ID colum
#once that works, then we just feed it the 1/1/2013 and 2/XX/15 IDs into the xrange section, bada bing, it'll iterate, yank all those rows, then its just a databse nightmare.

#homework: write in what you think needs to happen here
import requests
import sys 
import csv
import pprint
from bs4 import BeautifulSoup


def get_html_for_id(incident_id): #define the function named x, with parameters (y). (y) is just a placeholder so we know what we're referring to. the names of your vars can change once they enter functions. functions create new namers for the variables you feed into them. functions help you segregate the chunks of your program, and to help you generalize. dont have to pass it the same var name each time you want to use it
	base_url = "http://www.nrc.uscg.mil/pls/apex/f?p=109:3:0::NO::P3_SEQNOS:"
	full_url = base_url + str(incident_id) #just sticks two strings together, so you cant stick a string + an integer. gotta turn it into a string
	cookie_dictionary = {"WWV_CUSTOM-F_996331400518796_109":"6CECBECFC19CD455446106C07BBD90BA"} #a dict, formatted like {"key": value, "key": value}, like a json
	response = requests.get(full_url,cookies=cookie_dictionary, stream=False)
        return response.text
	#two types of paramaters/arguments: positional and keyword. incident_id is positional. keywords give default values. def get_html_for_id(material_id, cookie=None), cookie= is the named parameter. 
	#pass 

	#def get(url, cookies=None, headers=None, form_data=None) since you dont have to add parameters, they have default values of none. this helps you load paramaters in by name, and not by order, and whether or not they're required. cookie_dictionary in our case is an optional argument. what you pass to a function is an argument; what it takes is a parameter. it depends on your perspective, the function or what's outside.

def extract_material_data(material_page_html):
    def has_headers(element):
        return hasattr(element, 'headers')
	#here's where the soup happens.
    souped_material_page = BeautifulSoup(material_page_html)
    table = souped_material_page.find('table', class_='t16Standard')
    if not table:
        return [], []
    rows = table.find_all('tr')
    headers = []
    for th in rows[0].find_all('th'):
        headers.append(th.text)
    materials = []
    for row in rows[1:]:
        material_info = []
        for td in row.find_all('td'):
            if td.text == u'\xa0':
                material_info.append(0)
            else:
                material_info.append(td.text)

        materials.append(material_info)
    return headers, materials

def write_to_csv(dataset, headers, write_headers):
    with open('dataset.csv', 'a') as file_handle:
        writer = csv.writer(file_handle, delimiter='\t')
        if write_headers:
            writer.writerow(headers)
        writer.writerows(dataset)


def main(): #this will call all subordinate functions. this is our scaffold that holds our building materials. think of it as a pipeline of stuff to execute. we could nest them all, the outputs and inputs and start points and such, but thits makes it way easier to navigate
	""""where we start our script"""
	material_list = []
        for index, incident_id in enumerate(range(1034564,1073821)): #looping over each number that this generates. always use colons after for loops start
            try:
		html = get_html_for_id(incident_id) #reaches back to the above function, defines the output as html
		headers, material_data = extract_material_data(html)
                for element in material_data:
                    element.append(incident_id)
                headers.append('incident_id')
		material_list += material_data #.append can only happen to a list, and you have to pass it something. what are you passing? material data, which you just defined above
                if index % 10 == 0:
                    write_to_csv(material_list, headers, write_headers=index == 0)
                    material_list = []
                    print index
            except:
                print 'Error with id [{}]'.format(incident_id)
	write_to_csv(material_list, headers) #now this summons the write_to_csv function and tells it to act on material_list, which we just generated
	
if __name__ == "__main__":
    main() #this is what's on top of your stack. its where the program starts.

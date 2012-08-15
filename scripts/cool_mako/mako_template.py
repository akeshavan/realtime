from mako.template import Template
import time

json = {"subject_id":"pilot17","time":time.ctime(),"Protocol":[{"name":"Localizer"},{"name":"Visit 1"},{"name":"Visit 2"}]}
foo = Template(filename='subreg.html',encoding_errors='replace')


print foo.render(**json)





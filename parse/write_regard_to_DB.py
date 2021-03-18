import os
from glob import glob
import re
from webapp import create_app
from webapp.model import db, GPU
from pprint import pprint
from datetime import datetime



pattern = '\d{4}-\d{2}-\d{2}\s\d{2}-\d{2}'


basedir = os.path.abspath(os.path.dirname(__file__))
print(basedir)
files = os.listdir(os.path.join(basedir, 'data'))
files.sort()

latest = []
for each in glob('data/*.csv'):
    # print(type(each), each)
    # tmp1 = each.split('.')
    tmp1 = re.findall(pattern, each)[0]
    latest.append(datetime.strptime(tmp1, '%Y-%m-%d %H-%M'))
filename = 'regard_' + str(max(latest)) + '.csv'
print(filename)
print(files[-1])


# app = create_app()
# with app.app_context():

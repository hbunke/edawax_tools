# Hendrik Bunke <h.bunke@zbw.eu>, 10/2015

from __future__ import print_function
from config import api_key, url_base, pkg_name
import requests
import json
from time import time
import random
import os
from toolz.functoolz import compose, juxt

# you can start this with python -i, then call mass_upload(number)

pydir = os.path.dirname(os.path.abspath(__file__))
res_name = 'Mass Upload File'


def mass_upload(number):
    data = {'package_id': pkg_name,
            'url': 'http://zbw.eu/bla',  # why do we need this...?
            'name': res_name,
            }
    headers = {'Authorization': api_key}
    
    fn = ['1.pdf', '2.pdf', '3.pdf']
    fnames = map(lambda name: os.path.join(pydir, 'example_files', name), fn)
    
    # we try to keep the actual upload method as clean as possible (only the
    # request) to guarantee comparable timer values. So this function declares
    # the random variables and then calls upload()
    def para(n):
        f = data['description'] = random.choice(fnames)
        files = [('upload', file(f))]
        print('upload #{} {}'.format(n, f))
        return upload(files)

    @timer
    def upload(files):
        req = requests.post(
                url('resource_create'),
                data=data,
                files=files,
                headers=headers)
        assert req.status_code == 200

    start = time()
    times = map(lambda n: para(n), xrange(1, number + 1))
    end = time()

    data = dict(
        number=number,
        mini=min(times),
        maxi=max(times),
        avg=sum(times) / float(number),
        sumi=int(end - start)
        )

    print("""
Uploaded {number} resources in {sumi} seconds.
Min: {mini} sec
Max: {maxi} sec
Avg: {avg} sec
""".format(**data))


def mass_delete():
    """
    deletes resources with default name (res_name) within the given package
    """
    pkg = _package_show(pkg_name)
    resources = filter(lambda res: res['name'] == res_name, pkg['resources'])
    
    @timer
    def del_res():
        printi = lambda i: print('deleted resource {}'.format(i))
        map(lambda res: juxt(_resource_delete, printi)(res['id']), resources)
    
    print("{} resources deleted in {} seconds".format(len(resources),
        int(del_res())))


def timer(func):
    def wrapper(*args):
        start = time()
        func(*args)
        end = time()
        return end - start
    return wrapper


def url(cmd):
    return "{}/api/action/{}".format(url_base, cmd) 


def _resource_delete(res_id):
    headers = {'Authorization': api_key,
               'content-type': 'application/json; charset=UTF-8'}
    params = json.dumps({'id': res_id})
    req = requests.post(url('resource_delete'), data=params, headers=headers)
    assert req.status_code == 200


def _package_show(pkg_id):
    headers = {'Authorization': api_key, 'content-type':
               'application/json; charset=UTF-8'}
    data = json.dumps({'id': pkg_id})
    req = requests.post(url('package_show'), data=data, headers=headers)
    assert req.status_code == 200
    content = json.loads(req.content)
    return content['result']



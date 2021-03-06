import uuid

import hyperchamber.io as io

import random

store = {}
results = []

def set(key, value):
    """Sets a hyperparameter.  Can be used to set an array of hyperparameters."""
    store[key]=value
    return store

def count_configs():
    count = 1

    for key in store:
        value = store[key]
        if(isinstance(value,list)):
            count *= len(value)

    return count

def get_config_value(k, i):
    """Gets the ith config value for k.  e.g. get_config_value('x', 1)"""
    if(not isinstance(store[k], list)):
        return store[k]
    else:
        return store[k][i]

def configs(max_configs=1, offset=None, serial=False, create_uuid=True):
    """Generate max configs, each one a dictionary.  e.g. [{'x': 1}] 
      
      Will also add a config UUID, useful for tracking configs.  
      You can turn this off by passing create_uuid=False.
    """
    if len(store)==0:
        return []

    configs = []

    if(offset is None):
        offset = max(0, random.randint(0, count_configs()))
    for i in range(max_configs):
        # get an element to index over

        config = config_at(offset)
        if(create_uuid):
          config["uuid"]=uuid.uuid4().hex
        configs.append(config)
        if(serial):
            offset+=1
        else:
            offset = max(0, random.randint(0, count_configs()))
    return configs

def config_at(i):
  """Gets the ith config"""
  selections = {}
  for key in store:
    value = store[key]
    if isinstance(value, list):
        selected = i % len(value)
        i = i // len(value)
        selections[key]= value[selected]
    else:
        selections[key]= value

  return selections

def random_config():
  offset = max(0, random.randint(0, count_configs()))
  return config_at(offset)

def reset():
    """Reset the hyperchamber variables"""
    global store
    global results
    store = {}
    results = []
    return

def top(sort_by):
    """Get the best results according to your custom sort method."""
    sort = sorted(results, key=sort_by)
    return sort

def record(config, result):
    """Record the results of a config."""
    results.append((config, result))

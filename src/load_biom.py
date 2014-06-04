#!/usr/bin/env python 
import json 
import numpy

def load_biom(fname):
  """
  load a biom file and return a dense matrix 
  :fname - string containing the path to the biom file
  :data - numpy array containing the OTU matrix
  :samples - list containing the sample IDs (important for knowing 
    the labels in the data matrix)
  :features - list containing the feature names
  """
  o = json.loads(open(fname,"U").read())
  if o["matrix_type"] == "sparse":
    data = load_sparse(o)
  else:
    data = load_dense(o)

  samples = []
  for sid in o["columns"]:
    samples.append(sid["id"])
  features = []
  for sid in o["rows"]:
    # check to see if the taxonomy is listed, this will generally lead to more 
    # descriptive names for the taxonomies. 
    if sid.has_key("metadata") and sid["metadata"] != None:
      if sid["metadata"].has_key("taxonomy"):
        features.append(json.dumps(sid["metadata"]["taxonomy"]))
      else:
        features.append(sid["id"])
    else:
      features.append(sid["id"])
  return data, samples, features 


def load_dense(obj):
  """
  load a biom file in dense format
  :obj - json dictionary from biom file
  :data - dense data matrix
  """
  n_feat,n_sample = obj["shape"]
  data = np.array(obj["data"])
  return data.transpose()

def load_sparse(obj):
  """
  load a biom file in sparse format
  :obj - json dictionary from biom file
  :data - dense data matrix
  """
  n_feat,n_sample = obj["shape"] 
  data = numpy.zeros((n_feat, n_sample))
  for val in obj["data"]:
    data[val[0], val[1]] = val[2]
  data = data.transpose() 
  return data


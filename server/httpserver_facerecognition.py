#coding=utf-8

import json
from flask import Flask, request
from collections import OrderedDict
from elasticsearch import Elasticsearch
from facerecognition.elasticsearch_driver import SignatureES
import socket

hostname = socket.gethostname()

app = Flask(__name__)

port = '3006'
es_index = "facerecognition"

es = Elasticsearch("0.0.0.0", port=9200)

if not es.indices.exists(es_index):
	# index settings
	settings = {
		"settings" : {
			"analysis": {
					"analyzer": {
					   "payload_analyzer": {
						  "type": "custom",
						  "tokenizer":"whitespace",
						  "filter":"delimited_payload_filter"
						}
			  }
			}
		 },
		 "mappings": {
			"face" : {
			  "properties" : {
				  "signature": {
							  "type": "text",
							  "term_vector": "with_positions_offsets_payloads",
							  "analyzer" : "payload_analyzer"
						   }
			  }
		  }
		 }
	}
	try:
		# create index
		es.indices.create(index=es_index, body=settings)
	except Exception, e:
		pass

ses = SignatureES(es, index=es_index)

@app.route('/query',methods=['GET', 'POST'])
def message_for_image_search():
	if request.method == 'GET':
		return '200'

	search_dict = {}
	search_dict["tag"] = {}
	search_dict["result"] = "ok"
	search_dict["error_message"] = "no error"
	re = request.form['files']
	print re

	try:
		result = json.loads(re)
		print result
	except :
		search_dict["result"] = "error"
		search_dict["error_message"] = "can not catch picture"

	else:
		message_query = OrderedDict()
		if 'pics' in result.keys() and (result['pics'] is not None) and (len(result['pics']) > 0):
			for each_pic in result['pics']:
				path = each_pic['path']
				# path_aligned = each_pic['path_aligned']
				pic_id = each_pic['id']
				if 'consume_history' in each_pic and each_pic['consume_history'] == 'True':
					is_consume = True
				else:
					is_consume =False
				print path

				try:
					result = ses.query(path, is_consume)
					message_query[pic_id] = result
				except Exception, e:
					message_query[pic_id] = []
					search_dict["result"] = "error"
					search_dict["error_message"] = str(e)


		search_dict['tag'] = message_query
	# print "detection_dict: ", detection_dict
	tag_json = json.dumps(search_dict)
	print tag_json
	return tag_json

if __name__ == '__main__':
	app.run(debug=False, host='0.0.0.0', port=port)

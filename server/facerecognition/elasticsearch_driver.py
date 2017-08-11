import os
from datetime import datetime
from image_signature import generate_signature

class SignatureES(object):
    """Elasticsearch driver for image-match

    """

    def __init__(self, es, index='face', doc_type='face', timeout='10s', size=1, distance_low=0.5, distance_high = 0.8):
        """Extra setup for Elasticsearch

        Args:
            es (elasticsearch): an instance of the elasticsearch python driver
            index (Optional[string]): a name for the Elasticsearch index (default 'images')
            doc_type (Optional[string]): a name for the document time (default 'image')
            timeout (Optional[int]): how long to wait on an Elasticsearch query, in seconds (default 10)
            size (Optional[int]): maximum number of Elasticsearch results (default 100)
            *args (Optional): Variable length argument list to pass to base constructor
            **kwargs (Optional): Arbitrary keyword arguments to pass to base constructor

        Examples:
            >>> from elasticsearch import Elasticsearch
            >>> from image_match.elasticsearch_driver import SignatureES
            >>> es = Elasticsearch()
            >>> ses = SignatureES(es)
            >>> ses.add_image('https://upload.wikimedia.org/wikipedia/commons/thumb/e/ec/Mona_Lisa,_by_Leonardo_da_Vinci,_from_C2RMF_retouched.jpg/687px-Mona_Lisa,_by_Leonardo_da_Vinci,_from_C2RMF_retouched.jpg')
            >>> ses.search_image('https://upload.wikimedia.org/wikipedia/commons/thumb/e/ec/Mona_Lisa,_by_Leonardo_da_Vinci,_from_C2RMF_retouched.jpg/687px-Mona_Lisa,_by_Leonardo_da_Vinci,_from_C2RMF_retouched.jpg')
            [
             {'dist': 0.0,
              'id': u'AVM37nMg0osmmAxpPvx6',
              'path': u'https://upload.wikimedia.org/wikipedia/commons/thumb/e/ec/Mona_Lisa,_by_Leonardo_da_Vinci,_from_C2RMF_retouched.jpg/687px-Mona_Lisa,_by_Leonardo_da_Vinci,_from_C2RMF_retouched.jpg',
              'score': 0.28797293}
            ]

        """
        self.es = es
        self.index = index
        self.doc_type = doc_type
        self.timeout = timeout
        self.size = size
        self.distance_low = distance_low
        self.distance_high = distance_high

    def make_record(self, img_path, signature, is_consume, username, facename):
        """Makes a record suitable for database insertion.

        Note:
            This non-class version of make_record is provided for
            CPU pooling. Functions passed to worker processes must
            be picklable.

        Args:
            path (string): path or image data. If bytestream=False, then path is assumed to be
                a URL or filesystem path. Otherwise, it's assumed to be raw image data

        Returns:
            An image record.

            For example:

            {'path': 'https://pixabay.com/static/uploads/photo/2012/11/28/08/56/mona-lisa-67506_960_720.jpg',
             'signature': [0.123456, 0.234567, ... ]
             'metadata': {...}
             }

        """

        cur_time = datetime.now()

        record = dict()
        # convert it to http format
        record['path'] = img_path

        sig_list = signature.tolist()

        sig_res = ''
        for i, val in enumerate(sig_list):
            if i != (len(sig_list) - 1):
                sig_res += '%d|%f ' % (i, val)
            else:
                sig_res += '%d|%f' % (i, val)
        record['signature'] = sig_res

        if is_consume:
            record['consume_history'] = 1
        else:
            record['consume_history'] = 0

        record['username'] = username
        record['facename'] = facename

        record['timestamp'] = cur_time

        return record

    def search_img(self, signature, username):
        sig_list = signature.tolist()
        result = self.search_single_record(sig_list, username)

        return result

    def add_img(self, img_path, signature, is_consume, username, facename):
        rec = self.make_record(img_path, signature, is_consume, username, facename)
        self.insert_single_record(rec)

    def update_img(self, id):
        self.update_single_record(id)

    def query(self, img_path, is_consume=False, username='unknown', facename='unknown'):
        signature = generate_signature(img_path)
        search_result = self.search_img(signature, username)
        if len(search_result) != 0:
            result = search_result[0]['_source']['path']
            score = search_result[0]['_score']
            if is_consume and score > self.distance_high:
                self.update_img(search_result[0]['_id'])
        else:
            self.add_img(img_path, signature, is_consume, username, facename)
            result = 'add'

        return result

    def search_single_record(self, signature, username):
        # a common query DSL
        body={
        "query": {
        "function_score": {
             "query" : {
                "match": {
                    "username": username
                    }
           },
            "script_score": {
                "script": {
                    "inline": "payload_vector_score",
                    "lang": "native",
                    "params": {
                        "field": "signature",
                        "vector": signature,
                        "cosine": True
                    }
                }
            },
            "min_score" : self.distance_low,
            "boost_mode":"replace"
        }
        }
        }

        es_res = self.es.search(index=self.index,
                             doc_type=self.doc_type,
                             body=body,
                             size=self.size,
                             _source_exclude=['signature', 'timestamp', 'facename'],
                             timeout=self.timeout)
        res = es_res['hits']['hits']

        return res

    def insert_single_record(self, rec, refresh_after=False):
        self.es.index(index=self.index, doc_type=self.doc_type, body=rec, refresh=refresh_after)

    def update_single_record(self, id):
        self.es.update(index=self.index,doc_type=self.doc_type,id=id,
                body={"doc": {"consume_history": 1}})

    def delete_duplicates(self, path):
        """Delete all but one entries in elasticsearch whose `path` value is equivalent to that of path.
           need to modify!!!
        Args:
            path (string): path value to compare to those in the elastic search
        """
        result = self.es.search(body={'query':
                                 {'match':
                                      {'path': path}
                                  }
                             },
                       index=self.index)['hits']['hits']

        matching_paths = []
        matching_thumbnail = []
        for item in result:
            if item['_source']['path'] == path:
                matching_paths.append(item['_id'])
                matching_thumbnail.append(item['_source']['thumbnail'])

        if len(matching_paths) > 0:
            for i, id_tag in enumerate(matching_paths[1:]):
                self.es.delete(index=self.index, doc_type=self.doc_type, id=id_tag)
                if os.path.isfile(matching_thumbnail[i]):
                    os.remove(matching_thumbnail[i])

from unittest.mock import MagicMock
from datetime import datetime

brokerage_note_dummy = {'pdf_link': 'https://brokerage-note-and-bank-statement.s3.amazonaws.com/14/Region.BR/'
                            'broker_note/2022/4/19.pdf?AWSAccessKeyId=AKIATZVFXI25USQWCS5O&Signature='
                            'U0fZ7EtnQr5c2HStRgLowD8H22w%3D&Expires=1651258518'}

file_link_brokerage_dummy = 'https://brokerage-note-and-bank-statement.s3.amazonaws.com/109/?AWSAccessKeyId=5243792748DGHDJDH' \
                            '&signature=FHDGKFU6356489nfhjd65243&expires=875342628946'


broker_note_link_dummy = 'https://brokerage-note-and-bank-statement.s3.amazonaws.com/14/Region.BR/broker_note/2022/4/19.pdf?AWSAccessKeyId=AKIATZVFXI25USQWCS5O&Signature=U0fZ7EtnQr5c2HStRgLowD8H22w%3D&Expires=1651258518'

broker_note_link_all_dummy = 'https://brokerage-note-and-bank-statement.s3.amazonaws.com/14/Region.ALL/broker_note/2022/4/19.pdf?AWSAccessKeyId=AKIATZVFXI25USQWCS5O&Signature=U0fZ7EtnQr5c2HStRgLowD8H22w%3D&Expires=1651258518'

broker_note_us_link_dummy = "https://brokerage-note-and-bank-statement.s3.amazonaws.com/14/Region.US/broker_note/2022/4/19.pdf?AWSAccessKeyId=AKIATZVFXI25USQWCS5O&Signature=qk787uKUGTTYEFiUomCAZuC0z6w%3D&Expires=1651261099"

list_broker_note_dummy = [{'broker_note_link': 'https://brokerage-note-and-bank-statement.s3.amazonaws.com/'
                                               '14/BR/broker_note/2022/4/5.pdf?AWSAccessKeyId='
                                               'AKIATZVFXI25USQWCS5O&Signature='
                                               'd9vYYouHGiwtQptZIBZQCOpszj4%3D&Expires='
                                               '1651608773',
                                              'day': 5,
                                              'market': 'bmf',
                                              'region': 'BR'}]

list_broker_note_response_dummy = [{'market': 'us',
                                    'region': 'US',
                                    'day': 5,
                                    'broker_note_link': 'https://brokerage-note-and-bank-statement.s3.amazonaws.com/'
                                                        '14/US/broker_note/2022/4/5.pdf?AWSAccessKeyId='
                                                        'AKIATZVFXI25USQWCS5O&Signature='
                                                        'd9vYYouHGiwtQptZIBZQCOpszj4%3D&Expires=1651608773'}]


month_broker_notes_dirs_bmf_br = {'ResponseMetadata': {'RequestId': 'XR6HMV9M30YVDS2Q', 'HostId': 'PXZYLrTWpywLF56MwUy2Y25uPx0MwvxMYCUBoFN05AqPH96TQuK9WCBtlwNz+RXoTCJjstWyoDs=', 'HTTPStatusCode': 200, 'HTTPHeaders': {'x-amz-id-2': 'PXZYLrTWpywLF56MwUy2Y25uPx0MwvxMYCUBoFN05AqPH96TQuK9WCBtlwNz+RXoTCJjstWyoDs=', 'x-amz-request-id': 'XR6HMV9M30YVDS2Q', 'date': 'Wed, 04 May 2022 13:43:12 GMT', 'x-amz-bucket-region': 'sa-east-1', 'content-type': 'application/xml', 'transfer-encoding': 'chunked', 'server': 'AmazonS3'}, 'RetryAttempts': 0}, 'IsTruncated': False, 'Marker': '', 'Contents': [{'Key': '14/BR/broker_note/2022/4/5.pdf', 'LastModified': datetime(2022, 5, 2, 18, 25, 29, tzinfo=None), 'ETag': '"ff275b543b941d1da1de55bbb5517681-1"', 'Size': 37874, 'StorageClass': 'STANDARD', 'Owner': {'DisplayName': 'billing', 'ID': 'ddadb26827b39dff7bf757ada428f98b7a1f69409bd241069e1db04bf4aefd19'}}], 'Name': 'brokerage-note-and-bank-statement', 'Prefix': '14/BR/broker_note/2022/4/', 'Delimiter': '/', 'MaxKeys': 1000, 'EncodingType': 'url'}

month_broker_note_dummy = [{'market': 'bovespa', 'region': 'BR', 'day': 5, 'broker_note_link': 'https://brokerage-note-and-bank-statement.s3.amazonaws.com/14/BR/broker_note/2022/4/5.pdf?AWSAccessKeyId=AKIATZVFXI25USQWCS5O&Signature=d9vYYouHGiwtQptZIBZQCOpszj4%3D&Expires=1651608773'}]

month_broker_note_us_dummy = [{'market': 'us', 'region': 'US', 'day': 5, 'broker_note_link': 'https://brokerage-note-and-bank-statement.s3.amazonaws.com/14/US/broker_note/2022/4/5.pdf?AWSAccessKeyId=AKIATZVFXI25USQWCS5O&Signature=d9vYYouHGiwtQptZIBZQCOpszj4%3D&Expires=1651608773'}]

month_broker_note_bmf_dummy = [{'market': 'bmf', 'region': 'BR', 'day': 5, 'broker_note_link': 'https://brokerage-note-and-bank-statement.s3.amazonaws.com/14/BR/broker_note/2022/4/5.pdf?AWSAccessKeyId=AKIATZVFXI25USQWCS5O&Signature=d9vYYouHGiwtQptZIBZQCOpszj4%3D&Expires=1651608773'}]

month_response_stub = [{'broker_note_link': 'https://brokerage-note-and-bank-statement.s3.amazonaws.com/14/Region.BR/broker_note/2022/4/19.pdf?AWSAccessKeyId=AKIATZVFXI25USQWCS5O&Signature=U0fZ7EtnQr5c2HStRgLowD8H22w%3D&Expires=1651258518',
  'day': 5,
  'market': 'bmf',
  'region': 'BR'}]

month_broker_note_all_dummy = [{'market': 'all', 'region': 'ALL', 'day': 5, 'broker_note_link': 'https://brokerage-note-and-bank-statement.s3.amazonaws.com/14/BR/broker_note/2022/4/5.pdf?AWSAccessKeyId=AKIATZVFXI25USQWCS5O&Signature=d9vYYouHGiwtQptZIBZQCOpszj4%3D&Expires=1651608773'}]

month_broker_note_all_br_dummy = [{'market': 'all', 'region': 'BR', 'day': 5, 'broker_note_link': 'https://brokerage-note-and-bank-statement.s3.amazonaws.com/14/BR/broker_note/2022/4/5.pdf?AWSAccessKeyId=AKIATZVFXI25USQWCS5O&Signature=d9vYYouHGiwtQptZIBZQCOpszj4%3D&Expires=1651608773'}]

directories_stub = {'Key': '14/BR/broker_note/2022/4/5.pdf', 'ETag': '"ff275b543b941d1da1de55bbb5517681-1"', 'Size': 37874, 'StorageClass': 'STANDARD', 'Owner': {'DisplayName': 'billing', 'ID': 'ddadb26827b39dff7bf757ada428f98b7a1f69409bd241069e1db04bf4aefd19'}}

directories = MagicMock()

all_broker_note_from_all_markets_dummy = [{'broker_note_link': 'https://brokerage-note-and-bank-statement.s3.amazonaws.com/14/US/broker_note/2022/4/5.pdf?AWSAccessKeyId=AKIATZVFXI25USQWCS5O&Signature=d9vYYouHGiwtQptZIBZQCOpszj4%3D&Expires=1651608773',
                          'day': 5,
                          'market': 'us',
                          'region': 'US'},
                         {'broker_note_link': 'https://brokerage-note-and-bank-statement.s3.amazonaws.com/14/US/broker_note/2022/4/5.pdf?AWSAccessKeyId=AKIATZVFXI25USQWCS5O&Signature=d9vYYouHGiwtQptZIBZQCOpszj4%3D&Expires=1651608773',
                          'day': 5,
                          'market': 'us',
                          'region': 'US'},
                         {'broker_note_link': 'https://brokerage-note-and-bank-statement.s3.amazonaws.com/14/US/broker_note/2022/4/5.pdf?AWSAccessKeyId=AKIATZVFXI25USQWCS5O&Signature=d9vYYouHGiwtQptZIBZQCOpszj4%3D&Expires=1651608773',
                          'day': 5,
                          'market': 'us',
                          'region': 'US'}]

broker_note_from_br_markets_dummy = [{'broker_note_link': 'https://brokerage-note-and-bank-statement.s3.amazonaws.com/14/BR/broker_note/2022/4/5.pdf?AWSAccessKeyId=AKIATZVFXI25USQWCS5O&Signature=d9vYYouHGiwtQptZIBZQCOpszj4%3D&Expires=1651608773',
                                      'day': 5,
                                      'market': 'all',
                                      'region': 'BR'},
                                     {'broker_note_link': 'https://brokerage-note-and-bank-statement.s3.amazonaws.com/14/BR/broker_note/2022/4/5.pdf?AWSAccessKeyId=AKIATZVFXI25USQWCS5O&Signature=d9vYYouHGiwtQptZIBZQCOpszj4%3D&Expires=1651608773',
                                      'day': 5,
                                      'market': 'all',
                                      'region': 'BR'}]
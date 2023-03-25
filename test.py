import json

from PROcalc import DO_t

def my_handler(event, context):
    print(event)

    for msg in event['Records']:
        params = json.loads(msg['body'])
        DO_t.do_by_id(params)
    
    return {
        'statusCode': 200,
    }

[![Falkonry Logo](http://static1.squarespace.com/static/55a7df64e4b09f03368a7a78/t/569c6441ab281050fe32c18a/1453089858079/15-logo-transparent-h.png?format=500w)](http://falkonry.com/)

[![Build status](https://img.shields.io/travis/Falkonry/falkonry-python-client.svg?style=flat-square)](https://travis-ci.org/Falkonry/falkonry-python-client)

Falkonry Python Client to access [Falkonry Condition Prediction](http://falkonry.com) APIs

[Releases](https://github.com/Falkonry/falkonry-python-client/releases)

## Installation

```bash
$ pip install falkonryclient
```

## Features

    * Create Eventbuffer
    * Retrieve Eventbuffers
    * Create Pipeline
    * Retrieve Pipelines
    * Add data to Eventbuffer (csv/json, stream)
    * Retrieve output of Pipeline
    * Create subscription for Eventbuffer
    * Create publication for Pipeline
    
## Quick Start

    * To create Eventbuffer for single thing
    
```python
from falkonryclient import client as Falkonry
from falkonryclient import schemas as Schemas

falkonry   = Falkonry('https://service.falkonry.io', 'auth-token')

eventbuffer = Schemas.Eventbuffer()
eventbuffer.set_name('Motor Health')
eventbuffer.set_time_identifier('time')
eventbuffer.set_time_format('iso_8601')
        
createdEventbuffer = falkonry.create_eventbuffer(eventbuffer)
```

    * To create Eventbuffer with multiple things
    
```python
from falkonryclient import client as Falkonry
from falkonryclient import schemas as Schemas

falkonry   = Falkonry('https://service.falkonry.io', 'auth-token')

eventbuffer = Schemas.Eventbuffer()
eventbuffer.set_name('Motor Health')
eventbuffer.set_time_identifier('time')
eventbuffer.set_time_format('iso_8601')
eventbuffer.set_thing_identifier('motor')
        
createdEventbuffer = falkonry.create_eventbuffer(eventbuffer)
```

    * To create Eventbuffer for narrow format data
    
```python
from falkonryclient import client as Falkonry
from falkonryclient import schemas as Schemas

falkonry   = Falkonry('https://service.falkonry.io', 'auth-token')

eventbuffer = Schemas.Eventbuffer()
eventbuffer.set_name('Motor Health' + str(random.random()))
eventbuffer.set_time_identifier('time')
eventbuffer.set_time_format('iso_8601')
eventbuffer.set_signals_tag_field('tag')
eventbuffer.set_signals_delimiter('_')
eventbuffer.set_signals_location('prefix')
eventbuffer.set_value_column('value')
        
createdEventbuffer = falkonry.create_eventbuffer(eventbuffer)
```

    * To get all Eventbuffers
    
```python
from falkonryclient import client as Falkonry
from falkonryclient import schemas as Schemas

falkonry   = Falkonry('https://service.falkonry.io', 'auth-token')
        
eventbuffers = falkonry.get_eventbuffers()
```


    * To create Pipeline
    
```python
from falkonryclient import client as Falkonry
from falkonryclient import schemas as Schemas

falkonry   = Falkonry('https://service.falkonry.io', 'auth-token')

eventbuffer.set_name('Motor Health')
eventbuffer.set_time_identifier('time')
eventbuffer.set_time_format('iso_8601')
eventbuffer.set_thing_identifier('motor')
        
createdEventbuffer = falkonry.create_eventbuffer(eventbuffer)

assessment = Schemas.Assessment()
                .set_name('Health')
                .set_input_signals(['current', 'vibration'])
                        
pipeline   = Schemas.Pipeline()
                .set_name('Motor Health')
                .set_eventbuffer(createdEventbuffer.get_id())
                .set_input_signals({'current' : 'Numeric', 'vibration' : 'Numeric'})
                .set_assessment(assessment)
        
createdPipeline = falkonry.createPipeline(pipeline)
```

    * To get all Pipelines
    
```python
from falkonryclient import client as Falkonry
from falkonryclient import schemas as Schemas

falkonry   = Falkonry('https://service.falkonry.io', 'auth-token')
pipelines  = falkonry.getPipelines()
```

    * To add data
    
```python
from falkonryclient import client as Falkonry
from falkonryclient import schemas as Schemas

falkonry      = Falkonry('https://service.falkonry.io', 'auth-token')
data          = '{"time" :"2016-03-01 01:01:01", "current" : 12.4, "vibration" : 3.4, "state" : "On"}'
inputResponse = falkonry.add_input_data('eventbuffer_id', 'json', {}, data)
```

    * To add data from a stream
    
```python
import os, sys
from falkonryclient import client as Falkonry
from falkonryclient import schemas as Schemas

falkonry = Falkonry('https://service.falkonry.io', 'auth-token')
stream   = io.open('./data.json')

response = falkonry.add_input_stream('eventbuffer_id', 'json', {}, stream)
```

    * To add verification data
    
```python
from falkonryclient import client as Falkonry
from falkonryclient import schemas as Schemas

falkonry      = Falkonry('https://service.falkonry.io', 'auth-token')
data          = '{"time" : "2011-03-26T12:00:00Z", "car" : "HI3821", "end" : "2012-06-01T00:00:00Z", "Health" : "Normal"}'
inputResponse = falkonry.add_verification('pipeline_id', 'json', {}, data)
```

    * To add verification data from a stream
    
```python
import os, sys
from falkonryclient import client as Falkonry
from falkonryclient import schemas as Schemas

falkonry = Falkonry('https://service.falkonry.io', 'auth-token')
stream   = io.open('./data.json')

response = falkonry.add_verification_stream('pipeline_id', 'json', {}, stream)

```

    * To get output of a Pipeline
    
```python
import os, sys
from falkonryclient import client as Falkonry
from falkonryclient import schemas as Schemas

falkonry     = Falkonry('https://service.falkonry.io', 'auth-token')
stream       = open('/tmp/sample.json', 'r')
startTime    = '1457018017' #seconds since unix epoch 
endTime      = '1457028017' #seconds since unix epoch
outputStream = falkonry.getOutput('pipeline_id', startTime, endTime)
with open('/tmp/pipelineOutput.json', 'w') as outputFile:
    for line in outputStream:
        outputFile.write(line + '\n')
```

    * To create eventbuffer subscription
    
```python
from falkonryclient import client as Falkonry
from falkonryclient import schemas as Schemas

falkonry      = Falkonry('https://service.falkonry.io', 'auth-token')
subscription  = Schemas.Subscription()
subscription.set_type('MQTT') \
            .set_path('mqtt://test.mosquito.com') \
            .set_topic('falkonry-eb-1-test') \
            .set_username('test-user') \
            .set_password('test') \
            .set_time_format('YYYY-MM-DD HH:mm:ss') \
            .set_time_identifier('time')
subscription  = falkonry.create_subscription('eventbuffer_id', subscription)
```

    * To create pipeline publication
    
```python
from falkonryclient import client as Falkonry
from falkonryclient import schemas as Schemas

falkonry      = Falkonry('https://service.falkonry.io', 'auth-token')
publication   = Schemas.Publication() \
                .set_type('WEBHOOK') \
                .set_path('https://test.example.com/getFalkonryData') \
                .set_headers({
                    'Authorization': 'Token 1234567890'
                })
publication   = falkonry.create_publication('pipeline_id', publication)
```

## Docs

   [Falkonry APIs](https://service.falkonry.io/api)
     
## Tests

  To run the test suite, first install the dependencies, then run `Test.sh`:
  
```bash
$ pip install -r requirements.txt
$ python test/*.py
```

## License

  Available under [MIT License](LICENSE)

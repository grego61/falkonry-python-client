"""
Falkonry Client

Client to access Condition Prediction APIs

:copyright: (c) 2016 by Falkonry Inc.
:license: MIT, see LICENSE for more details.

"""

import jsonpickle
from falkonryclient.helper.models.Publication import Publication
from falkonryclient.helper.models.Assessment import Assessment
from falkonryclient.helper.models.Signal import Signal


class Pipeline:
    """Pipeline schema class"""

    def __init__(self, **kwargs):
        if 'pipeline' in kwargs:
            self.raw = kwargs.get('pipeline')
        else:
            self.raw = {}

        if 'inputList' in self.raw:
            if isinstance(self.raw['inputList'], list):
                inputs = []
                for input_signal in self.raw['inputList']:
                    inputs.append(Signal(signal=input_signal))
                self.raw['inputList'] = inputs

        if 'assessmentList' in self.raw:
            if isinstance(self.raw['assessmentList'], list):
                assessments = []
                for assessment in self.raw['assessmentList']:
                    assessments.append(Assessment(assessment=assessment))
                self.raw['assessmentList'] = assessments

        if 'publicationList' in self.raw:
            if isinstance(self.raw['publicationList'], list):
                publications = []
                for publication in self.raw['publicationList']:
                    publications.append(Publication(publication=publication))
                self.raw['publicationList'] = publications

    def get_id(self):
        return self.raw['id']

    def set_source_id(self, source_id):
        self.raw['sourceId'] = source_id
        return self

    def get_source_id(self):
        return self.raw['sourceId']

    def set_name(self, name):
        self.raw['name'] = name
        return self

    def get_name(self):
        return self.raw['name']

    def get_account(self):
        return self.raw['tenant']

    def get_create_time(self):
        return self.raw['createTime']

    def get_created_by(self):
        return self.raw['createdBy']

    def get_update_time(self):
        return self.raw['updateTime']

    def get_updated_by(self):
        return self.raw['updatedBy']

    def set_eventbuffer(self, eventbuffer):
        self.raw['input'] = eventbuffer
        return self

    def get_eventbuffer(self):
        return self.raw['input']

    def set_thing_identifier(self, identifier):
        self.raw['thingIdentifier'] = identifier
        return self

    def get_thing_identifier(self):
        return self.raw['thingIdentifier']

    def set_thing_name(self, name):
        self.raw['singleThingID'] = name
        return self

    def get_thing_name(self):
        return self.raw['singleThingID']

    def set_input_signal(self, signal, stype):
        if stype is not 'Numeric' and stype is not 'Categorical':
            return self

        signals = self.raw['inputList'] if self.raw['inputList'] is not None else []
        new_signal = Signal(signal={
          'name': signal,
          'valueType': {
            'type': stype
          }
        })
        signals.append(new_signal)
        self.raw['inputList'] = signals
        return self

    def set_input_signals(self, input_list):
        inputs = []
        for signal in input_list:
            new_signal = Signal(signal={
              'name': signal,
              'valueType': {
                'type': input_list[signal]
              }
            })
            inputs.append(new_signal)
        self.raw['inputList'] = inputs
        return self

    def get_input_signals(self):
        return self.raw['inputList']

    def set_assessment(self, assessment):
        if not isinstance(assessment, Assessment):
            return self

        assessments = self.raw['assessmentList'] if 'assessmentList' in self.raw else []
        assessments.append(assessment)
        self.raw['assessmentList'] = assessments
        return self

    def set_assessments(self, assessments):
        assessment_list = self.raw['assessmentList'] if 'assessmentList' in self.raw else []
        for assessment in assessments:
            if isinstance(assessment, Assessment):
                assessment_list.append(assessment)

        self.raw['assessmentList'] = assessment_list
        return self

    def get_assessments(self):
        return self.raw['assessmentList']

    def set_publications(self, publications):
        publication_list = self.raw['publicationList'] if 'publicationList' in self.raw else []
        for publication in publications:
            if isinstance(publication, Publication):
                publication_list.append(publication)

        self.raw['publicationList'] = publication_list
        return self

    def get_publications(self):
        return self.raw['publicationList']

    def get_status(self):
        return self.raw['status']

    def get_outflow_status(self):
        return self.raw['outflowStatus']

    def set_interval(self, signal=None, duration=None):
        self.raw['interval'] = {
          'field': signal,
          'duration': duration
        }
        return self

    def get_interval(self):
        return self.raw['interval']

    def get_earliest_data_time(self):
        return self.raw['earliestDataPoint']

    def get_latest_data_time(self):
        return self.raw['latestDataPoint']

    def set_data_format(self, dformat):
        self.raw['dataFormat'] = dformat
        return self

    def get_data_format(self):
        return self.raw['dataFormat']

    def get_model_revisions(self):
        return self.raw['modelRevisionList']

    def get_outflow_history(self):
        return self.raw['outflowHistory']

    def to_json(self):
        inputs = []
        assessments = []
        publications = []
        for inputSignal in self.raw['inputList']:
            inputs.append(jsonpickle.unpickler.decode(inputSignal.to_json()))

        for assessment in self.raw['assessmentList']:
            assessments.append(jsonpickle.unpickler.decode(assessment.to_json()))

        for publication in self.raw['publicationList']:
            publications.append(jsonpickle.unpickler.decode(publication.to_json()))

        pipeline = self.raw
        pipeline['inputList'] = inputs
        pipeline['assessmentList'] = assessments
        pipeline['publicationList'] = publications
        return jsonpickle.pickler.encode(pipeline)

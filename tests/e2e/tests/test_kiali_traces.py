import pytest
import tests.conftest as conftest
import calendar
import time

gmt = time.gmtime

bookinfo_namespace = conftest.get_bookinfo_namespace()

def test_service_traces_endpoint(kiali_client):
    response = kiali_client.request (method_name='serviceTraces',  path={'namespace': bookinfo_namespace, 'service':'details'}, params={'startMicros': calendar.timegm(gmt())})
    if response.status_code in [404, 500]:
        pytest.skip()
    elif response.status_code == 200:
        data = response.json().get('data')
        assert data != None, f"Data not found in json: {response.json()}"
        assert len(data) != 0, f"Data not found in json: {response.json()}"
        traceID = data[0].get('traceID')
        assert traceID != None, f"TraceID not found in json: {response.json()}"
        spans_list = response.json().get('data')[0].get('spans')
        assert spans_list != None
        for traceID in spans_list:
            assert traceID not in [None, '']
    else:
        assert False

def test_workload_traces_endpoint(kiali_client):
    response = kiali_client.request (method_name='workloadTraces',  path={'namespace': bookinfo_namespace, 'workload':'details-v1'}, params={'startMicros': calendar.timegm(gmt())})
    if response.status_code in [404, 500]:
        pytest.skip()
    elif response.status_code == 200:
        data = response.json().get('data')
        assert data != None, f"Data not found in json: {response.json()}"
        assert len(data) != 0, f"Data not found in json: {response.json()}"
        traceID = data[0].get('traceID')
        assert traceID != None, f"TraceID not found in json: {response.json()}"
        spans_list = response.json().get('data')[0].get('spans')
        assert spans_list != None
        for traceID in spans_list:
            assert traceID not in [None, '']
    else:
        assert False
        
def test_app_traces_endpoint(kiali_client):
    response = kiali_client.request (method_name='appTraces',  path={'namespace': bookinfo_namespace, 'app':'details'}, params={'startMicros': calendar.timegm(gmt())})
    if response.status_code in [404, 500]:
        pytest.skip()
    elif response.status_code == 200:
        data = response.json().get('data')
        assert data != None, f"Data not found in json: {response.json()}"
        assert len(data) != 0, f"Data not found in json: {response.json()}"
        traceID = data[0].get('traceID')
        assert traceID != None, f"TraceID not found in json: {response.json()}"
        spans_list = response.json().get('data')[0].get('spans')
        assert spans_list != None
        for traceID in spans_list:
            assert traceID not in [None, '']
    else:
        assert False    

def test_workload_spans_endpoint(kiali_client):
    response = kiali_client.request (method_name='workloadSpans',  path={'namespace': bookinfo_namespace, 'workload':'details-v1'}, params={'startMicros': calendar.timegm(gmt())})
    if response.status_code == 500:
        pytest.skip()
    elif response.status_code == 200:
        traceID = response.json()[0]['traceID']
        assert traceID != None
        references_traceID = response.json()[0]['references'][0]['traceID']
        assert references_traceID not in [None, '']
    else:
        assert False


def test_service_spans_endpoint(kiali_client):
    response = kiali_client.request (method_name='serviceSpans',  path={'namespace': bookinfo_namespace, 'service':'details'}, params={'startMicros': calendar.timegm(gmt())})
    if response.status_code == 500:
        pytest.skip()
    elif response.status_code == 200:
        traceID = response.json()[0]['traceID']
        assert traceID != None
        references_traceID = response.json()[0]['references'][0]['traceID']
        assert references_traceID not in [None, '']
    else:
        assert False

def test_app_spans_endpoint(kiali_client):
    response = kiali_client.request(method_name='appSpans', path={'namespace': bookinfo_namespace, 'app': 'details'}, params={'startMicros': calendar.timegm(gmt())})
    if response.status_code == 500:
        pytest.skip()
    elif response.status_code == 200:
        traceID = response.json()[0]['traceID']
        assert traceID != None
        references_traceID = response.json()[0]['references'][0]['traceID']
        assert references_traceID not in [None, '']
    else:
        assert False

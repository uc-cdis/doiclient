
def test_get_bloodpac():
    from doiclient.client import DOIClient
    
    signpost = DOIClient(baseurl="https://dx.doi.org/")
    
    res = signpost.get("10.25638/BLOODPAC.0001")
    assert res.status_code == 200
    print(res.json())


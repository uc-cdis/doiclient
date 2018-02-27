
def test_get_bloodpac():
    from doiclient.client import DOIClient
    
    signpost = DOIClient(baseurl="https://dx.doi.org/")
    
    res = signpost.get("10.1007/s41060-017-0052-3")
    print(res.to_json())


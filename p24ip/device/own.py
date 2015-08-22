def control(request, site_name):
    from p24ip.manage import get_struct    
    return get_struct(request).web.__dict__[site_name](request)
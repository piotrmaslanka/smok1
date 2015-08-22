def get_struct(request):
    from patelnia.p24 import Device
    struc = Device(request.session['Device.dev_number']).structure
    return eval("__import__('p24ip.structures."+struc+"\').structures."+struc)
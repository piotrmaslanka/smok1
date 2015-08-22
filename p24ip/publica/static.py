from djangomako.shortcuts import render_to_response


def about(request):
    return render_to_response('publica/about.html', {})

def index(request):
    return render_to_response('publica/index.html', {})

def sitemap(request):
    return render_to_response('sitemap.xml', {})
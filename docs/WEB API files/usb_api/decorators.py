from django.http import HttpResponse

def usb_login_required(function=None):      
    def _dec(view_func):
        def _view(request, *args, **kwargs):
            if request.session.get('usb_code',None) == None:                
                return HttpResponse("You are not logged in")
            else:
                return view_func(request, *args, **kwargs)

        _view.__name__ = view_func.__name__
        _view.__dict__ = view_func.__dict__
        _view.__doc__ = view_func.__doc__

        return _view

    if function is None:
        return _dec
    else:
        return _dec(function)

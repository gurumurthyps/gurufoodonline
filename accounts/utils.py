

def detectUser(user):
    print(user.role)
    if user.role==1:
        redirecturl='custDashboard'
    elif user.role==2:
        redirecturl='restDashboard'
    elif user.role is None and user.is_superadmin:
        redirecturl='admin/'  
    return redirecturl      

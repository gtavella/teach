# How to build a Web Server - routing & middleware
# Design patterns and proven ideas for building the higher level code of an application built on a web server.
# Giuseppe Tavella



class App:

    def __init__(self) -> None:
        # not to be called directly, because are not wrapped by middleware
        self.route_handlers = {}
        
        self.request = {}
        
        self.session = {
            "is_login": False,
            "magic_token": None
        }


    def register_route(self, route):

        def outer(route_handler):

            def inner(*args, **kwargs):
                # home_handler -> route_handler
                
                # before the route handler is called
                self.before_every_route_handler(*args, **kwargs)
                # call route handler
                route_handler(*args, **kwargs)
                # after the route handler is called
                self.after_every_route_handler(*args, **kwargs)
    
            self.route_handlers[route] = inner

            return inner

        return outer


    def require_login(self, next_func):
        
        def inner(*args, **kwargs):
            # if user is logged in, continue to next func
            if self.session["is_login"]:
                
                self.before_login_success(*args, **kwargs)
                
                return next_func(*args, **kwargs)
            # else stop here, user cannot access resource
            else:
                
                print("You are not logged in - access denied")
                
                return self.when_not_login(*args, **kwargs)
            
        return inner
    
    
    def require_magic_token(self, token):
        
        def outer(next_func):
                    
            def inner(*args, **kwargs):
                
                is_token_valid = (token == self.session.get("magic_token"))
                
                if is_token_valid:
                    
                    print("magic token is valid - congrats")                    
   
                    return next_func(*args, **kwargs)
                
                else:
                    
                    print("magic token is not valid - sorry")
                    
                    return ""
                
            return inner
            
        return outer
        

    def before_every_route_handler(self, *args, **kwargs):
        print("this func is called before any route handler")

    def after_every_route_handler(self, *args, **kwargs):
        print("this func is called after any route handler")
    
    def when_not_login(self, *args, **kwargs):
        print("this func is called when user is not logged in")
    
    
    def before_login_success(self):
        print("this func is called right before successful login")


    def set_login(self, is_login):
        self.session["is_login"] = is_login

    def set_magic_token(self, token):
        self.session["magic_token"] = token



def open_database_connection():
    print("qui dentro gestisco tutto quello che ha a che fare con il database")


# classe e decoratori


app = App()
# montare, registrare
# mount, register


@app.require_login
@app.register_route("/home")
def home_handler():
    print("qui dentro va il codice specifico che gestisco /home")
    print("connessione database aperta")
    
    open_database_connection()
    
    print("connessione database chiusa")
    
    print("a questo punto, la funzione che gestisce /home e' finita")
    return "Welcome to Home Page"




@app.require_magic_token(12345)
@app.register_route("/chi-siamo")
def chi_siamo_handler():
    # qui dentro gestisco tutto quello che riguarda 
    # /chi-siamo
    print("welcome to chi siamo")
    return "Welcome to Chi Siamo"



@app.require_login
@app.require_magic_token(12345)
@app.register_route("/dashboard")
def dashboard_handler():
    
    print("welcome - you are now in dashboard")
    return "Welcome to Dashboard"



app.set_magic_token(12345)
app.set_login(False)
# app.set_login(False)


# dashboard_handler()

home_handler()



# chi_siamo_handler()



# ROUTING
# giuseppetavella.it

# path = route

# URL path/route

# URL
# https://negozio.giuseppetavella.it/chi-siamo


# ROUTES (ROUTING)
"""
URL path         | route handler     
----------------------------------------
/home            |  home_handler    
/chi-siamo       |  chi_siamo_handler
/contatti        |  contatti_handler
/dashboard       |  dashboard_handler
------------------------------------
"""



# MIDDLEWARE
# il middleware sono funzioni che stanno tra la richiesta in arrivo
# e la risposta a quella richiesta

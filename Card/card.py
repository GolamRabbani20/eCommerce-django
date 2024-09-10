from store.models import Product, Profile
class Card:
    def __init__(self, request):
        self.session = request.session

        #Get request
        self.request = request

        #Get the current session key if exists
        card = self.session.get('session_key')

        #If the user is new, no session key! Create one!
        if 'session_key' not in request.session:
            card = self.session['session_key'] = {}

        self.card = card

    def add(self, product, quantity):
        product_id = str(product.id) #{'4': 3, '2': 5}
    
        if product_id not in self.card:
            self.card[product_id] = quantity
   
        self.session.modified = True

        #Deal with logged in user
        if self.request.user.is_authenticated:
            #Get the current user profile
            current_user = Profile.objects.filter(user__id = self.request.user.id)
            #Convert python dictonary to string ==> {'3':2, '4':10} -> "{'3':2, '4':10}"
            cart_str = str(self.card)
            #Convert the string to json formate ==> {'3':2, '4':10} -> {"3":2, "4":10}
            cart_str = cart_str.replace("\'", "\"") 
            current_user.update(old_card = str(cart_str))


    def db_add(self, product_id, quantity):
        if product_id not in self.card:
            self.card[product_id] = quantity
   
        self.session.modified = True

        #Deal with logged in user
        if self.request.user.is_authenticated:
            #Get the current user profile
            current_user = Profile.objects.filter(user__id = self.request.user.id)
            #Convert python dictonary to string ==> {'3':2, '4':10} -> "{'3':2, '4':10}"
            cart_str = str(self.card)
            #Convert the string to json formate ==> {'3':2, '4':10} -> {"3":2, "4":10}
            cart_str = cart_str.replace("\'", "\"") 
            current_user.update(old_card = str(cart_str))

    def __len__(self):
        return len(self.card) 
    
    def get_products(self):
        #Get ids from card
        product_ids = self.card.keys()

        #Use ids to lookup products in database model
        products = Product.objects.filter(id__in=product_ids)
        return products
    
    def get_quantity(self):
        return self.card
    
    def update(self, product, quantity):
        product_id = str(product) #{'4': 3, '2': 5}

        #Update Dictonary of card
        self.card[product_id]=quantity

         #Deal with logged in user
        if self.request.user.is_authenticated:
            #Get the current user profile
            current_user = Profile.objects.filter(user__id = self.request.user.id)
            #Convert python dictonary to string ==> {'3':2, '4':10} -> "{'3':2, '4':10}"
            cart_str = str(self.card)
            #Convert the string to json formate ==> {'3':2, '4':10} -> {"3":2, "4":10}
            cart_str = cart_str.replace("\'", "\"") 
            current_user.update(old_card = str(cart_str))

        self.session.modified = True
        return self.card
    
    def delete(self, product):
        if product in self.card:
            del self.card[product]

        #Deal with logged in user
        if self.request.user.is_authenticated:
            #Get the current user profile
            current_user = Profile.objects.filter(user__id = self.request.user.id)
            #Convert python dictonary to string ==> {'3':2, '4':10} -> "{'3':2, '4':10}"
            cart_str = str(self.card)
            #Convert the string to json formate ==> {'3':2, '4':10} -> {"3":2, "4":10}
            cart_str = cart_str.replace("\'", "\"") 
            current_user.update(old_card = str(cart_str))

        self.session.modified = True
        return self.card
    
    def cardTotal(self):
        product_ids = self.card.keys()
       
        #Lookup those keys in our Products database model
        products = Product.objects.filter(id__in=product_ids)#When you use id__in, you are providing a list of IDs
  
        total_price = 0
        total_product = 0
        for key, val in self.card.items(): #{'4': 3, '2': 5}
            for product in products:
                if product.id == int(key):
                    if product.is_sale:
                        total_price += product.sale_price * val
                    else:
                        total_price += product.price * val
            total_product += val

        total_price = float(total_price)
        if total_price>=2000:
            discount = (20/100)*total_price
            discount_price = total_price - discount
            return {'total_price':total_price, 'total_product':total_product, 'discount':discount, 'discount_price':discount_price}
        return {'total_price':total_price, 'total_product':total_product}         


        


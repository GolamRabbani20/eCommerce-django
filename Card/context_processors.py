from .card import Card

#Create context processor so that our card can work on all pages of the site.
def card(request):
    #Return the default data from our Card
    return {'card': Card(request)}
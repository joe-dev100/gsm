from datetime import datetime
from vente.models import Facture, NumFacture, Session, Vente


def formatNumFacture(num):
    """
    Format a number with commas as thousands separators.
    """
    number_size=len(str(num))
   
    if number_size == 1:
        return f"000{num}"
    elif number_size == 2:
        return f"00{num}"
    elif number_size == 3:
        return f"0{num}"
    
    
def numFacture(user):
    """
    Generate a formatted invoice number.
    """
    vente=Vente.objects.filter().last()
    # Get the last invoice number from the database
    last_invoice = NumFacture.objects.filter(date=datetime.now().date()).last()
    new_invoice_number = 0
    session=Session.objects.get(login=user)
    if last_invoice:
        # Increment the last invoice number by 1
        new_invoice_number = int(last_invoice.lastNum) + 1
        year= str(datetime.now().year)[2:]  
        month= str(datetime.now().month)
        day= str(datetime.now().day)
        if len(day) == 1:
            day=f'0{day}'
        if len(month) == 1:
            month=f'0{month}'
        # Format the new invoice number with leading zeros
        
        last_invoice.lastNum = new_invoice_number
        last_invoice.save()
        formatted_invoice_number = f"{year}{month}{day}{formatNumFacture(new_invoice_number)}"
        Facture.objects.create(numFacture=formatted_invoice_number, utilisateur=session,vente=vente)
    else:
        # If no invoices exist, start with 1
        new_invoice_number = 1
        NumFacture.objects.create(lastNum=new_invoice_number,date=datetime.now().date())
        year= str(datetime.now().year)[2:]  
        month= str(datetime.now().month)
        day= str(datetime.now().day)
        formatted_invoice_number = f"{year}{month}{day}{formatNumFacture(new_invoice_number)}"
        Facture.objects.create(numFacture=formatted_invoice_number, utilisateur=session,vente=vente)
    return formatted_invoice_number
   
    

def resetNumFacture():
    """
    Reset the invoice number to 1.
    """
    # Get the last invoice number from the database
    last_invoice = NumFacture.objects.last()
    if last_invoice:
        # Reset the last invoice number to 1
        last_invoice.lastNum = 0
        last_invoice.save()
    else:
        # If no invoices exist, create a new one with number 1
        NumFacture.objects.create(lastNum=0)
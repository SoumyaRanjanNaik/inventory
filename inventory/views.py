from django.shortcuts import render, redirect, get_object_or_404
import datetime
from django.http import HttpResponse

# Create your views here.

from inventory.models import Product, Sale, Stock, Bill, Restock

context = {'product': Product.objects.all(),
           'sale': Sale.objects.all(),
           'stock': Stock.objects.all(),
           }


def dashboard(request):
    """
    dashboard renderer
    """
    context = {'restock': Restock.objects.all().order_by('r_id').reverse(),
               'field': ['date', 'id', 'gst', 'amount'],
               'sale': Sale.objects.all().order_by('sale_id').reverse(),
               }
    return render(request, 'dashboard.html', context)


def restock_page(request):
    """
    restock page form renderer
    """
    context = {'stock': Stock.objects.all(),
               'product': Product.objects.all(),
               'range': range(1, 30),
               'field': [f.name for f in Stock._meta.get_fields()][2:4]}
    return render(request, 'restock.html', context)


def sale_page(request):
    """
    sale page form renderer
    """
    context = {'bill': Bill.objects.all(),
               'product': Product.objects.all(),
               'range': range(1, 30),
               'field': [f.name for f in Bill._meta.get_fields()][2:5]}
    return render(request, 'sale.html', context)


def manager(request):
    """
    restock and stock database entry
    """
    if request.method == "POST":
        products = cleaner(request.POST.getlist('product'))
        in_stock = cleaner(request.POST.getlist('in_stock'))
        gst = request.POST.get('gst')
        r = Restock(date=datetime.datetime.now(), gst=float(gst), amount=0)
        r.save()
        gst = float(gst)/100
        amt = []
        for i in range(len(products)):
            s = Stock(restock_id=r,
                      product=Product.objects.get(p_name=products[i]),
                      in_stock=int(in_stock[i]),
                      amount=int(
                          in_stock[i]) * Product.objects.get(p_name=products[i]).p_price
                      )
            amt.append(s.amount)
            inv = Product.objects.get(p_id=s.product.p_id)
            st = inv.stocks
            inv.stocks = st+s.in_stock
            inv.save()
            s.save()
        r.amount = sum(amt)+(sum(amt)*gst)
        r.save(force_update=True)
        context = {'type': 'sale',
                   'total': sum(amt),
                   'total_gst': sum(amt)+(sum(amt)*gst),
                   'datax': zip(products,
                                in_stock,
                                range(len(products)),
                                amt,
                                ),
                   'field': ['product', 'quantity', 'amount'],
                   }
    else:
        return HttpResponse("failed")
    return render(request, "stockconfirmation.html", context)


def sale(request):
    """
    sale and bill database entry
    """
    if request.method == "POST":
        products = cleaner(request.POST.getlist('product'))
        quantity = cleaner(request.POST.getlist('quantity'))
        discount = cleaner(request.POST.getlist('discount'))
        gst = request.POST.get('gst')
        s = Sale(date=datetime.datetime.now(), gst=float(gst), amount=0)
        gst = float(gst)/100
        s.save()
        for i in range(len(products)):
            b = Bill(bill_id=s,
                     product=Product.objects.get(p_name=products[i]),
                     quantity=int(quantity[i]),
                     discount=int(discount[i]),
                     amount=(int(
                         quantity[i])*Product.objects.get(p_name=products[i]).p_price)-int(discount[i])
                     )
            b.save()
            inv = Product.objects.get(p_id=b.product.p_id)
            st = inv.stocks
            inv.stocks = st-b.quantity
            inv.save()
        ls = Bill.objects.filter(bill_id=s).values_list('amount')
        l = [i[0] for i in ls]
        s.amount = sum(l)+(sum(l)*gst)
        s.save(force_update=True)
        context = {'type': 'sale',
                   'data': zip(products,
                               quantity,
                               discount,
                               range(len(products)),
                               l),
                   'field': ['product', 'quantity', 'discount', 'amount'],
                   'total': sum(l),
                   'total_gst': s.amount
                   }
    else:
        return HttpResponse("failed")
    return render(request, "confirmation.html", context)


def cleaner(l):
    """
    list cleaner for empty entries (used in functions above)
    """
    i = -1
    while(l[i] == ''):
        l.remove('')
    return l


def newproduct(request):
    """
    new product addition form page renderer
    """
    context = {'range': range(1, 30),
               'field': ['product name', 'price per unit']}
    return render(request, 'add_product.html', context)


def newproductadd(request):
    """
    new product addition into database
    """
    if request.method == "POST":
        products = cleaner(request.POST.getlist('product'))
        price = cleaner(request.POST.getlist('price'))
        for i in range(len(products)):
            p = Product(p_name=products[i],
                        p_price=price[i],
                        stocks=0)
            p.save()
    else:
        return HttpResponse("failed")
    return render(request, 'addconfirmation.html')


def stockview(request):
    """
    current stocks viewer with latest element at first
    """
    context = {'stocks': Product.objects.all().order_by('p_id').reverse(),
               'field': ['id', 'name', 'price', 'stocks']}
    return render(request, 'stocksviewer.html', context)


def report_req(request):
    '''
    report generation and request handeling
    '''
    if request.method == "POST":
        start = request.POST.get('start')
        end = request.POST.get('end')
        if request.POST.get('type').lower() == 'sale':
            context = {'type': 'sale',
                       'start': start,
                       'end': end,
                       'report': Sale.objects.filter(date__range=(start, end)),
                       'fields': ['date', 'id', 'gst', 'amount']
                       }
        elif request.POST.get('type').lower() == 'restock':
            context = {'type': 'restock',
                       'start': start,
                       'end': end,
                       'report': Sale.objects.filter(date__range=(start, end)),
                       'fields': ['date', 'id', 'gst', 'amount']
                       }
        return render(request, 'report.html', context)
# include bugfix messages framework
    else:
        return render(request, 'reportgen.html', {})

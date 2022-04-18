from django.shortcuts import render, reverse ,get_object_or_404
from django.views import generic
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse

from .forms import CreateMoneyForm, CreateShoppingForm
from .models import Week, Shopping, Money, Hesab, MainHesab, LastHesab



class WeekList(generic.ListView):
    model = Week
    template_name = 'hesab/week_list.html'
    context_object_name = 'week_list'


def refresh(request, pk):
    week = Week.objects.get(id=pk)
    all_money = Money.objects.filter(week=week).order_by('money')
    shopping = Shopping.objects.filter(week=week).order_by('name')
    moneys = Money.objects.filter(week=week)
    chosen_shopping = Shopping.objects.filter(week=week)
    m = 0
    for money in moneys:
        m+=1
        my_money = 0
        chosen_shopping_buyer = Shopping.objects.filter(week=week, buyer=money.user)

        for shop in chosen_shopping_buyer:
            my_money += int(shop.amount)
        for shop in chosen_shopping:
            numbers = shop.consumer.all().count()
            if money.user in shop.consumer.all():
                my_money -= int(shop.amount / numbers)
            Money.objects.filter(user=money.user, week=week).update(money=my_money)
    sum = 0
    for s in shopping:
        sum += s.amount
    Week.objects.filter(id=pk).update(sum=sum)
    try:
        return render(request, 'hesab/week_details.html', {'week': week, 'sum': week.sum, 'shopping': shopping,'all_money':all_money})

    except:
        return render(request, 'hesab/week_details.html', {'week': week, 'sum': week.sum, 'shopping': shopping})

def week_details(request, pk):
    week = Week.objects.get(id=pk)
    all_money = Money.objects.filter(week=week).order_by('money')
    shopping = Shopping.objects.filter(week=week).order_by('name')

    week_money = 0
    # for shop in shopping:
    #     week_money +=shop.amount
    # Week.objects.filter(id=pk).update(sum=week_money)
    context = {
        'week': week,
        'sum': week.sum,
        'shopping': shopping,
        'all_money': all_money
    }
    return render(request, 'hesab/week_details.html', context)


def money_create_view(request, pk):
    week = Week.objects.get(id=pk)
    if request.method == 'POST':
        money_form = CreateMoneyForm(request.POST)
        if money_form.is_valid():
            money = Money(user=money_form.cleaned_data['user'], week=week)
            money.save()
            return HttpResponseRedirect(f'/{pk}/refresh/')

    else:
        money_form = CreateMoneyForm()
        context = {
            'form': money_form
        }
        return render(request, 'hesab/create_money.html',context )

def shopping_create_view(request, pk):
    week = Week.objects.get(id=pk)
    week_sum = week.sum
    if request.method == 'POST':
        shop_form = CreateShoppingForm(request.POST)
        if shop_form.is_valid():
            shop = Shopping(
                             week=week,
                             name=shop_form.cleaned_data['name'],
                             goods=shop_form.cleaned_data['goods'],
                             buyer=shop_form.cleaned_data['buyer'],
                             amount=shop_form.cleaned_data['amount'],
                             )
            shop.save()
            for n in shop_form.cleaned_data['consumer']:
                shop.consumer.add(n)
            numbers = shop.consumer.all().count()
            week_sum += shop.amount
            for con in shop.consumer.all():
                try:
                    money = Money.objects.get(week=week, user=con)

                except:
                    shop.delete()
                    return HttpResponse('چنین مصرف کننده ای برای این هفته تعریف نشده است')
                my_money = money.money
                my_money -= int(shop.amount / numbers)
                Money.objects.filter(user=money.user, week=week).update(money=my_money)
            Week.objects.filter(id=pk).update(sum=week_sum)
            return HttpResponseRedirect(f'/{pk}/weekdetails/')
        else:
            return HttpResponse('حداقل یک مورد را برای مصرف کنندگان انتخاب کنید !')

    else:
        shop_form = CreateShoppingForm()
        context = {
            'form': shop_form,
            "week": week
        }
        return render(request, 'hesab/create_shopping.html',context )

def hesab_view(request, pk):
    week = Week.objects.get(id=pk)
    hesab = Hesab.objects.filter(week_id=pk)
    for hes in hesab :
        hes.delete()
    chosen_money_negative = Money.objects.filter(week_id=pk, money__lte=-1)
    for n in chosen_money_negative:
        chosen_money_plus = Money.objects.filter(week_id=pk, money__gte=1)
        while n.money < 0:
            print('---------------')
            print(chosen_money_negative)
            print(n.money)
            print(chosen_money_plus)
            for p in chosen_money_plus:
                print('=============')
                p_user = p.user
                n_user = n.user
                x = p.money
                y = n.money
                if x >= -1*y:
                    x += y
                    n = Money.objects.get(id=n.id)
                    n.money = 0
                    p=Money.objects.get(id=p.id)
                    p.money = x
                    p.save()
                elif x < -1*y:
                    y += x
                    nn=Money.objects.get(id=n.id)
                    print('first :',nn.money)
                    nn.money = y
                    nn.save()
                    print('second :',nn.money)

                    pp = Money.objects.get(id=p.id)
                    pp.money = 0
                    pp.save()
                    # Hesab.objects.create(plus=p_user,negative=n_user,amount=x)
    hesabs = Hesab.objects.filter(week_id=pk)
    return render(request, 'hesab/all_hesab.html', {'hesabs': hesabs})

#
def hesab_view3(request, pk):
    week = Week.objects.get(id=pk)
    hesab = Hesab.objects.filter(week_id=pk)
    for hes in hesab:
        hes.delete()
    moneys = Money.objects.filter(week_id=pk)
    money_dict_p = {}
    money_dict_n = {}
    for money in moneys:
        if money.money > 0:
            money_dict_p.update({money.id: money.money})
        elif money.money < 0:
            money_dict_n.update({money.id: money.money})
    key_n_list = []
    key_p_list = []
    for key, zero in money_dict_p.items():
        if zero == 0:
            list.append(key)
    print(list)
    for key_n, negative in money_dict_n.items():
        for key_p, positive in money_dict_p.items():
            if negative < positive:
                positive += negative
                print(key_n)
                print(money_dict_p)
                print(money_dict_n)
                money_dict_n.pop(key_n)
                break
            elif negative > positive:
                negative += positive
                money_dict_p.pop(key_p)
                break
            elif negative == positive:
                money_dict_p.pop(key_p)
                money_dict_n.pop(key_n)
                break


def hesab(request, pk):
    week = Week.objects.get(id=pk)
    shopping = Shopping.objects.filter(week=week).order_by('name')
    hesabs = Hesab.objects.filter(week=week).delete()
    for shop in shopping:
        for con in shop.consumer.all():
            if con != shop.buyer:
                Hesab.objects.create(plus=shop.buyer, negative=con, amount=shop.amount/shop.consumer.all().count(), week=week)
    hesabs = Hesab.objects.filter(week=week)
    print(hesabs)
    for hesab in hesabs:
        money = 0
        chosen_hesab = Hesab.objects.filter(week=week, plus=hesab.plus, negative=hesab.negative)
        for hesab2 in chosen_hesab:
            money += hesab.amount
            print(hesab.amount)
            try:
                hesab_2 = MainHesab.objects.get(week=week, plus=hesab.plus, negative=hesab.negative)
                hesab_2.amount = money
            except:
                hesab_2 = MainHesab.objects.create(week=week, plus=hesab.plus, negative=hesab.negative, amount=money)
    # for hesab in hesabs:
        chosen_hesab_2 = Hesab.objects.filter(week=week, plus=hesab.negative, negative=hesab.plus)
        for hesab2 in chosen_hesab_2:
            money -= hesab.amount
        print('last money :', hesab.amount)
        try:
            hesab_2 = MainHesab.objects.get(week=week, plus=hesab.plus, negative=hesab.negative)
            hesab_2.amount = money
        except:
            hesab_2 = MainHesab.objects.create(week=week, plus=hesab.plus, negative=hesab.negative,amount=money)

    hesabs_3 = MainHesab.objects.filter(week=pk)
    return render(request, 'hesab/all_hesab.html', {'hesabs': hesabs_3})

def last_hesab_refresh(request, pk):
    week = Week.objects.get(id=pk)
    shopping = Shopping.objects.filter(week=week).order_by('name')
    main_heasbs = MainHesab.objects.filter(week=week).order_by('amount')      #important
    LastHesab.objects.filter(week=week).delete()
    for main_hesab in main_heasbs:
        try:
            try:
                last_hesab = LastHesab.objects.get(week=week, plus=main_hesab.plus, negative=main_hesab.negative)
                last_hesab.amount += main_hesab.amoun
                print('-------')
            except:
                pass
            try:
                last_hesab = LastHesab.objects.get(week=week, plus=main_hesab.negative, negative=main_hesab.plus)
                last_hesab.amount -= main_hesab.amoun
                print('++++++++')

            except:
                pass
        except:
            last_hesab = LastHesab.objects.create(week=week, plus=main_hesab.plus, negative=main_hesab.negative, amount=main_hesab.amount)

    last_hesabs = LastHesab.objects.filter(week=pk)
    return render(request, 'hesab/all_hesab.html', {'hesabs': last_hesabs})







    # for money_p in chosen_money_plus:
    #     p_mon = money_p.money
    #     for money_n in chosen_money_negative:
    #         if p_mon != 0 and p_mon >= -1*(money_n.money):
    #             Hesab.objects.create(plus=money_p.user, negative=money_n.user, amount=int(money_n.money))
    #             p_mon +=money_n.money
    #         elif p_mon != 0 and p_mon < -1*(money_n.money):
    #             Hesab.objects.create(plus=money_p.user, negative=money_n.user, amount=int(money_n.money))
    #             money_n.money +=p_mon
    #             money_n._do_update(money=money_n.money)



















# class WeekDetails(generic.DetailView):
#     model = Week
#     template_name = 'hesab/week_details.html'
#     context_object_name = 'week'
#
#
# def refresh2(request, pk):
#     week = Week.objects.get(id=pk)
#     shopping = Shopping.objects.filter(week=week)
#     moneys = Money.objects.filter(week=week)
#     for shop in shopping:
#         numbers = shop.consumer.all().count()
#         for con in shop.consumer.all():
#             print(con)
#             my_money = 0
#             my_money -= int(shop.amount/numbers)
#             print('money : ' ,my_money , )
#             if shop.buyer == con:
#                 print(con)
#                 print(shop.buyer == con)
#                 my_money += int(shop.amount)
#             me = Money.objects.filter(user=con, week=week).update(money=my_money)
#             print('me money :',me,'000')
#             # my_con =con
#             print('-------------------------------------------')
#     print('=====================================================')
#             # me_2 = Money.objects.update_or_create(user=my_con
#             #                                       ,week=week,money=10)
#             # money_form = MoneyForm()
#             # print(me_2)
#             # me2 = me.objects.update(money=my_money)
#     return render(request, 'hesab/week_details.html', {'week': week})

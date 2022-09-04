
import logging
from azbankgateways import bankfactories, models as bank_models, default_settings as settings
from azbankgateways.exceptions import AZBankGatewaysException
from django.http import HttpResponse, Http404
from order_module.models import Order
from django.shortcuts import render

from utils import bankfactories

# go to bank
def go_to_gateway_view(request , orderid):

    #get order info based order id
    order = Order.objects.get(id=orderid)

    # خواندن مبلغ از هر جایی که مد نظر است
    amount = order.total_price
    # تنظیم شماره موبایل کاربر از هر جایی که مد نظر است
    user_mobile_number = '+989980000000'  # اختیاری

    factory = bankfactories.MyBankFactory()

    try:
        bank = factory.create() # or factory.create(bank_models.BankType.BMI) or set identifier
        bank.set_request(request)
        bank.set_amount(amount)
        bank.set_orderId(orderid)
        # یو آر ال بازگشت به نرم افزار برای ادامه فرآیند
        bank.set_client_callback_url('/callback-gateway/')
        bank.set_mobile_number(user_mobile_number)  # اختیاری
    
        # در صورت تمایل اتصال این رکورد به رکورد فاکتور یا هر چیزی که بعدا بتوانید ارتباط بین محصول یا خدمات را با این
        # پرداخت برقرار کنید. 
        bank_record = bank.ready()
        
        # هدایت کاربر به درگاه بانک
        return bank.redirect_gateway()

    except AZBankGatewaysException as e:
        logging.critical(e)
        # TODO: redirect to failed page.
        return render(request, 'apppayment/process.html', {'message': 'خطا در اتصال به درگاه بانکی دوباره امتحان کنید' , 'type' : 'danger'})
        #raise e



#callback from bank
def callback_gateway_view(request):
    tracking_code = request.GET.get(settings.TRACKING_CODE_QUERY_PARAM, None)
    if not tracking_code:
        logging.debug("این لینک معتبر نیست.")
        return render(request, 'apppayment/process.html', {'message': 'این لینک معتبر نیست.' , 'type' : 'warning'})
        #raise Http404

    try:
        bank_record = bank_models.Bank.objects.get(tracking_code=tracking_code)
    except bank_models.Bank.DoesNotExist:
        logging.debug("این لینک معتبر نیست.")
        return render(request, 'apppayment/process.html', {'message': 'این لینک معتبر نیست.' , 'type' : 'warning'})
        #raise Http404

    # در این قسمت باید از طریق داده هایی که در بانک رکورد وجود دارد، رکورد متناظر یا هر اقدام مقتضی دیگر را انجام دهیم
    if bank_record.is_success:
        # پرداخت با موفقیت انجام پذیرفته است و بانک تایید کرده است.
        # می توانید کاربر را به صفحه نتیجه هدایت کنید یا نتیجه را نمایش دهید.
        #return HttpResponse("پرداخت با موفقیت انجام شد.")
        print( " order_id => " + str(bank_record.order_id))
        target_order = Order.objects.get(id=bank_record.order_id)
        target_order.paid = 1
        target_order.save()
        return render(request, 'apppayment/process.html', {'message': 'پرداخت با موفقیت انجام شد.' , 'type' : 'success'})

    # پرداخت موفق نبوده است. اگر پول کم شده است ظرف مدت ۴۸ ساعت پول به حساب شما بازخواهد گشت.
    #return HttpResponse("پرداخت با شکست مواجه شده است. اگر پول کم شده است ظرف مدت ۴۸ ساعت پول به حساب شما بازخواهد گشت.")
    return render(request, 'apppayment/process.html', {'message': 'پرداخت با شکست مواجه شده است. اگر پول کم شده است ظرف مدت ۴۸ ساعت پول به حساب شما بازخواهد گشت.' , 'type' : 'info'})

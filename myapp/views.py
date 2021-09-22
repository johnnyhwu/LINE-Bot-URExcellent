from django.conf import settings
from django.http.response import HttpResponseNotFound
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest, JsonResponse
from django.views .decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage

from .modules import func

import json


# line_bot_api = LineBotApi(settings.CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.CHANNEL_SECRET)

@csrf_exempt
def callback(request):
    
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
        
        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()
        
        for event in events:
            if isinstance(event, MessageEvent):
                # line_bot_api.reply_message(event.reply_token, TextSendMessage(text=event.message.text))
                
                mtext = event.message.text
                
                if mtext == '@文字的力量':
                    func.send_text(event)
        
        
        return HttpResponse()

    else:
        return HttpResponseBadRequest()
    
    
def manage(request):
    result = func.read_record_sql()
    if result == None:
        return HttpResponseNotFound()
    else:
        return render(request, 'manage.html', {'data': result})


def delete_record(request):
    if request.method == 'POST':
        result = func.delete_record_sql(json.loads(request.body.decode())['id'])
        return JsonResponse({'status':result})
    
def add_record(request):
    if request.method == 'POST':
        result = func.add_record_sql(json.loads(request.body.decode())['text'])
        return JsonResponse({'status':result[0], 'id':result[1]})

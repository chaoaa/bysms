import traceback

from django.http import JsonResponse
import json
from django.core.paginator import Paginator, EmptyPage

from common.models import Customer

def listcustomers(request):
    try:
        pagenum  = request.params['pagenum']
        pagesize = request.params['pagesize']
        #返回一个QuerySet对象，包含所有的表记录
        qs = Customer.objects.values()

        pgnt = Paginator(qs,pagesize)
        page = pgnt.page(pagenum)
        #将QuerySet对象转化为list类型
        #否则不能被转化为JSON字符串
        retlist = list(page)

        # total指定了 一共有多少数据
        return JsonResponse({'ret': 0, 'retlist': retlist, 'total': pgnt.count})

    except EmptyPage:
        return JsonResponse({'ret': 0, 'retlist': [], 'total': 0})

    except:
        return JsonResponse({'ret': 2, 'msg': f'未知错误\n{traceback.format_exc()}'})

def addcustomer(request):
    info = request.params['data']
    #从请求消息中，获取要添加客户的信息
    #并且插入到数据库中
    record = Customer.objects.create(name=info['name'],
                            phonenumber=info['phonenumber'],
                            address=info['address'],)
    return JsonResponse({'ret':0,'id':record.id})

def modifycustomer(request):
    # 从请求消息中 获取修改客户的信息
    # 找到该客户，并且进行修改操作
    customerid = request.params['id']
    newdata    = request.params['newdata']

    try:
        # 根据 id 从数据库中找到相应的客户记录
        customer = Customer.objects.get(id=customerid)
    except Customer.DoesNotExist:
        return  {
                'ret': 1,
                'msg': f'id 为`{customerid}`的客户不存在'
        }
    if 'name' in  newdata:
        customer.name = newdata['name']
    if 'phonenumber' in  newdata:
        customer.phonenumber = newdata['phonenumber']
    if 'address' in  newdata:
        customer.address = newdata['address']

    # 注意，一定要执行save才能将修改信息保存到数据库
    customer.save()

    return JsonResponse({'ret': 0})

def deletecustomer(request):

    customerid = request.params['id']

    try:
        # 根据 id 从数据库中找到相应的客户记录
        customer = Customer.objects.get(id=customerid)
    except Customer.DoesNotExist:
        return  {
                'ret': 1,
                'msg': f'id 为`{customerid}`的客户不存在'
        }

    # delete 方法就将该记录从数据库中删除了
    customer.delete()

    return JsonResponse({'ret': 0})

from lib.handler import dispatcherBase

Action2Handler = {
    'list_customer': listcustomers,
    'add_customer': addcustomer,
    'modify_customer': modifycustomer,
    'del_customer': deletecustomer,
}

def dispatcher(request):
    return dispatcherBase(request, Action2Handler)
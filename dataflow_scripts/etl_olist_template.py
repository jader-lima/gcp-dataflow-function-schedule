import apache_beam as beam
import re
import itertools 
# for datetime manipulation
from datetime import datetime,date
from apache_beam.options.pipeline_options import PipelineOptions, StandardOptions
from apache_beam.runners.runner import PipelineState

import argparse

class Etl_olist_template(PipelineOptions):
    @classmethod
    def _add_argparse_args(cls, parser):
        parser.add_value_provider_argument(
            '--input_itens',
            #dest='input_itens', 
            help='Input itens file to process.')
        
        parser.add_value_provider_argument(
            '--input_seller',
            #dest='input_seller', 
            help='Input seller file to process.')
        
        parser.add_value_provider_argument(
            '--input_products',
            #dest='input_products', 
            help='Input products file to process.')
        
        parser.add_value_provider_argument(
            '--input_order',
            #dest='input_order', 
            help='Input order file to process.')
        
        parser.add_value_provider_argument(
            '--input_reviews',
            #dest='input_reviews', 
            help='Input reviews file to process.')
        
        parser.add_value_provider_argument(
            '--input_payments',
            #dest='input_payments', 
            help='Input payments file to process.')
        
        parser.add_value_provider_argument(
            '--input_customer',
            #dest='input_customer', 
            help='Input customer file to process.')
        
        parser.add_value_provider_argument(
            '--output',
            #dest='output',
            help='Output table to write results to.')

        parser.add_value_provider_argument(
            '--partition_date',
            #dest='partition_date',
            help='partition date for big query ingestion.')

def ListtoStr( values):    
        return ','.join(f"{value}" for value in values)
    
def cleandata( element):
    element = re.sub(r"[\"\'\(\)\[\]]", '', element)
    return element.split(',')

def dict_toList( element):
    item = element[0].split(',')
    for key, value in element[1].items():
        for v in value:
            if isinstance(v, dict):
                for key, value in v.items():
                    item += [str(value[0])]
            else:
                item += [str(v)]
    return item

def retReview( element):
    if element is not None and len(element) >= 3 and len(element[1]) == 32:
        return element[1], element[2]

def retSeller( element):
    return element[0], element[2], element[3]

def retCustomer( element):
    return element[0], element[3], element[4]

def retProd( element):
    return element[0], element[1]

def format_Prod( element):
    return f"{element[0]},{element[1]}"

def retOrderItems( element):
    return element[0], element[0],element[3], element[4],element[5], element[6], element[7],element[8]

def returnFieldsJoin7Join4( element,current_date):
    return element[3],element[4],element[5],element[6],element[7],element[10] ,element[11],element[12],element[13],element[14],element[15],element[16], element[20], element[21], element[22], element[23], element[24], element[25], element[26], element[27], element[28], element[0], element[1], element[2], current_date


def reTupless( element):
    l = list(element[1].keys())
    for i in range(len(l) - 1):
        item = element[1].get(l[i])
        for x in item:
            for y in element[1].get(l[-1]):
                if isinstance(y, list):
                    yield list(x) + list(y)
                else:
                    yield list(x) + [y]

def CompleteCleanDate( element):
    date_fields = [3, 4, 5, 6, 7, 17]
    for idx in date_fields:
        if element[idx] == '':
            element[idx] = '2099-12-31'
    return element

def list_to_dict( element, cols):
    return dict(zip(cols, element))

            
def run(argv=None):

    parser = argparse.ArgumentParser()  

    path_args, pipeline_args = parser.parse_known_args()
                
    pipeline_options = PipelineOptions(pipeline_args)

    p1 = beam.Pipeline(options=pipeline_options)

    global opts

    opts = pipeline_options.view_as(Etl_olist_template)  

    
    output_header = 'order_id,payment_sequential,payment_type,payment_installments,payment_value,order_status,order_purchase_timestamp,order_approved_at,order_delivered_carrier_date,\
    order_delivered_customer_date,order_estimated_delivery_date,review_score,shipping_limit_date,itens_count,price,freight_value,seller_id,seller_city,seller_state,product_id,\
    product_category_name,customer_id,customer_city,customer_state,load_date'
    

    current_date = str(date.today())


    cols_itens = [
                    "order_id","order_item_id","product_id","seller_id","shipping_limit_date","price","freight_value"]
        
    input_itens_orders = ( 
                p1 
                | 'Read itens_orders data' >> beam.io.ReadFromText(opts.input_itens,skip_header_lines=1)
                | 'Clean data itens_orders' >> beam.Map(cleandata) 
                | 'dict for itens_orders' >> beam.Map(list_to_dict, cols_itens)    
            )


    itens_sum_price = (
            input_itens_orders  
                | 'dict for sum prices' >> beam.Map(lambda element: (element['order_id']+','+element['product_id'] +','+element['seller_id']+','+element['shipping_limit_date'], float(element['price'])) ) 
                | 'Group sum prices' >> beam.CombinePerKey(sum)
    )

    itens_count = (
            input_itens_orders 
                | 'dict for count itens' >> beam.Map(lambda element: (element['order_id']+','+element['product_id'] +','+element['seller_id']+','+element['shipping_limit_date'], int(element['order_item_id']))) 
                | 'count itens' >> beam.combiners.Count.PerKey()
    )

    freight_value = (
            input_itens_orders 
                | 'dict for sum freight_value' >> beam.Map(lambda element: (element['order_id']+','+element['product_id'] +','+element['seller_id']+','+element['shipping_limit_date'], float(element['freight_value'])) ) 
                | 'Group sum freight_value' >> beam.CombinePerKey(sum)
    )


    join1 = ({'itens_count': itens_count, 'itens_sum_price': itens_sum_price} 
                | 'itens_count + itens_sum_price' >> beam.CoGroupByKey()                                                               
    )


    join2 = ({'join1': join1, 'freight_value': freight_value} 
                | 'join1 + freight_value' >> beam.CoGroupByKey()
                | 'dict to list ' >> beam.Map(dict_toList) 
                | 'create dict join2 ' >> beam.Map(lambda element: (element[2], element))
    )


    sellers = (
        p1
            | 'Read seller data' >> beam.io.ReadFromText(opts.input_seller,skip_header_lines=1)
            | 'Clean data seller' >> beam.Map(cleandata) 
            | 'return seller data except geo id' >> beam.Map(retSeller)
            | 'create dict from seller' >> beam.Map(lambda sellers: (sellers[0], sellers))
    )


    join3 = ({'join2': join2, 'sellers': sellers} 
                | 'join2 + sellers' >> beam.CoGroupByKey()
                | 'dict to list sellers' >> beam.FlatMap(reTupless) 
                | 'create dict join3 ' >> beam.Map(lambda itens: (itens[1], itens))#verificar essa linha

    )


    products = (
            p1
                | 'Read prod data' >> beam.io.ReadFromText(opts.input_products,skip_header_lines=1)
                | 'Clean data prod' >> beam.Map(cleandata) 
                | 'return prod data ' >> beam.Map(retProd)
                | 'create dict from prod' >> beam.Map(lambda prod: (prod[0], prod))
    )



    join4 = ({'join3': join3, 'products': products} 
                | 'join3 + products' >> beam.CoGroupByKey()
                | 'dict to list join4' >> beam.FlatMap(reTupless) 
                | 'Removing undisired caracters after join' >> beam.Map(ListtoStr)
                | 'Clean data and preparing list' >> beam.Map(cleandata) 
                | 'dict order id key join 4 ' >> beam.Map(lambda itens: (itens[0], itens))

    )  


        
    order = (
            p1
                | 'Read orders data' >> beam.io.ReadFromText(opts.input_order,skip_header_lines=1)
                | 'Clean data orders' >> beam.Map(cleandata) 
                | 'create dict from orders' >> beam.Map(lambda order: (order[0], order))
    )


    reviews = (
            p1
                | 'Read reviews data' >> beam.io.ReadFromText(opts.input_reviews,skip_header_lines=1)
                | 'Clean reviews order' >> beam.Map(cleandata) 
                | 'return order id and review score' >> beam.Map(retReview)
                | 'Check reviews only with id' >> beam.Filter(lambda rev: rev is not None )
                | 'create dict from reviews' >> beam.Map(lambda reviews: (reviews[0], reviews[1]))         
    )

    join5 = ({'order': order, 'reviews': reviews} 
                | 'orders + reviews' >> beam.CoGroupByKey()
                | 'dict to list join5' >> beam.FlatMap(reTupless) 
                | 'create dict join 5 ' >> beam.Map(lambda itens: (itens[0], itens))
    )

    
    payments = (
        p1
            | 'Read payments data' >> beam.io.ReadFromText(opts.input_payments,skip_header_lines=1)
            | 'Clean payments order' >> beam.Map(cleandata) 
            | 'create dict from payments' >> beam.Map(lambda itens: (itens[0], itens))   
    )

    join6 = ({ 'payments': payments,'join5': join5} 
                | ' payments + join5 ' >> beam.CoGroupByKey()
                | 'dict to list join6' >> beam.FlatMap(reTupless) 
                | 'create dict join 6' >> beam.Map(lambda itens: (itens[6], itens))
    )
    
    customer = (
        p1
            | 'Read customer data' >> beam.io.ReadFromText(opts.input_customer,skip_header_lines=1)
            | 'Clean customer order' >> beam.Map(cleandata) 
            | 'return customer id ,state and City' >> beam.Map(retCustomer)
            | 'create dict from customer' >> beam.Map(lambda itens: (itens[0], itens))        
    )

    join7 = ({ 'customer': customer, 'join6': join6} 
            | 'customer + join6' >> beam.CoGroupByKey()
            | 'dict to list join7' >> beam.FlatMap(reTupless) 
            | 'dict order id key join 7  ' >> beam.Map(lambda itens: (itens[8], itens))
    )


    join8 = ({ 'join7': join7, 'join4': join4} 
                | 'join7 + join4' >> beam.CoGroupByKey()
                | 'dict to list join8' >> beam.FlatMap(reTupless) 
                | 'selection field in desired order' >> beam.Map(returnFieldsJoin7Join4,current_date)  
                | 'List to string' >> beam.Map(ListtoStr)             
                | 'Write results join 8' >> beam.io.WriteToText(opts.output, file_name_suffix='.csv',header=output_header)
        )


    p1.run()

if __name__ == '__main__':
    run()
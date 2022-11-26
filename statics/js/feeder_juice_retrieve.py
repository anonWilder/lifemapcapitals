import psycopg2
import pandas as pd
import psycopg2.extras
import requests
import numpy as np

connection = psycopg2.connect(user = "postgres",
    password = "EedcOsita@123",
    host = "localhost",
    port = "5432",
    database = "EEDCLIVE")
cr = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)


# cr = self._cr
cr.execute("SELECT feeder_id as id,f.name from res_partner c left join feeder_feeder f on f.id = c.feeder_id where  juice_acc_no is not null and metering_type = 'prepaid' and feeder_id is not null group by feeder_id,f.name")
feeders = cr.fetchall()


#   print(sms)
count_ = 0  
# print(len(feeders))
# exit()
feeders = []
file = "juice_tariff21.csv"
loads = pd.read_csv('/data/%s' % (file),dtype=str).dropna()
for da,v in loads.iterrows():
    data = {"feeder_id":"0","name":"Dummy"} 
    feeders.append(data)

for d in feeders:
    # cr.execute("SELECT meter_no,locid,tariff.name as tariff from res_partner cus LEFT JOIN feeder_cluster feed on feed.feeder_cluster = cus.feeder_id LEFT JOIN customer_class cl on cl.id = cus.customer_class LEFT JOIN tariff_extention tariff on tariff.new_tariff = cus.customer_class and service_clusters = feed.service_cluster_id where meter_no is not null and locid is not null and feeder_id = %s and juice_acc_no is not null and metering_type = 'prepaid'" % (d['id']))
    # cr.execute("SELECT juice.cus_name as meter_no,juice.market as locid,tariff.name as tariff from mike_test juice LEFT JOIN res_partner cus on cus.juice_acc_no = juice.consume LEFT JOIN feeder_cluster feed on feed.feeder_cluster = cus.feeder_id LEFT JOIN customer_class cl on cl.id = cus.customer_class LEFT JOIN tariff_extention tariff on tariff.new_tariff = cus.customer_class and service_clusters = feed.service_cluster_id where cus.acc_no is not null and tariff.name is not null")
    # juice_data = cr.fetchall()
    juice_data = []
    file = "juice_tariff21.csv"
    loads = pd.read_csv('/data/%s' % (file),dtype=str).dropna()
    for da,v in loads.iterrows():
        data = {"meter_no":v['meter_no'],"locid":v['locid'],"tariff":v['tariff']} 
        juice_data.append(data)
    print("Sending %s .........................." % (d['name']))
    if len(juice_data) > 1000:
        feeder_data = list(np.array_split(juice_data,round(len(juice_data)/1000)))
    else:
        feeder_data = [juice_data]
    count = 0

    for dt in feeder_data:
        
        meters = []
        count = count + 1
        count_ = count_ + 1
        # print(d)
        print("%s feeder name : %s %s " % (str(count_),str(d['name']),str(len(dt))))
        # continue
        for j in dt:
            # print(count_)
            # print("%s%s" % (d['name'],count))

            load = {}
            load['serialnumber'] = "'%s'" % (j['meter_no'])
            load['tariff'] = "'%s'" % (j['tariff'])
            meters.append(load)
        if len(meters) > 0:
            pd.DataFrame(meters).to_csv('/data/feeder_uploads/%s%s_meter.csv' % (d['name'],count),columns=['serialnumber','tariff'], index=False)
        location = []
        for j in dt:
            load = {}
            load['locid'] = "'%s'" % (j['locid'])
            load['tariff'] = "'%s'" % (j['tariff'])
            location.append(load)
        if len(location) > 0:
            pd.DataFrame(location).to_csv('/data/feeder_uploads/%s%s_locid.csv' % (d['name'],count),columns=['locid','tariff'], index=False)
        # if len(dt):
            # continue
            url = "http://74.208.145.137:5000/juice/update/tariff/feeder"

            payload = "{\"params\":[{\"m_filename\":\"%s%s_meter.csv\",\"l_filename\":\"%s%s_locid.csv\"}]}" % (d['name'],count,d['name'],count)
            headers = {
              'Content-Type': 'application/json',
              'Cookie': 'PHPSESSID=652aa11cd624ee873a771204467c8fc6; frontend_lang=en_US; session_id=9b3879e49ac2bbe065d67c289df2ff645bb940dc'
            }

            response = requests.request("POST", url, headers=headers, data = payload)

            print(response.text.encode('utf8'))
        


    
    
    # print(d)

# -*- coding: utf-8 -*-
import pandas as pd
from flask import Flask, render_template, request
import sqlite3
import pygal
from pygal_maps_world.maps import World
from pygal.maps.world import COUNTRIES
from pygal_maps_world import i18n
from nltk import pos_tag, word_tokenize
import nltk
import re
from autocorrect import spell
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')


app = Flask(__name__)

column_dict = {'invoice':'invoiceno','invoiceno':'invoiceno','invc':'invoiceno','stockcode':'stockcode',
               'stck':'stockcode','description':'description','desc':'description','quantity':'quantity',
               'quantities':'quantity','2010':'year','year':'year','month':'month','months':'month',
               '2011':'year','december':'month','january':'month','february':'month','march':'month',
               'april':'month','may':'month','june':'month','july':'month','august':'month',
               'September':'month','october':'month','november':'month','wednesday':'weekday', 
               'thursday':'weekday', 'friday':'weekday', 'sunday':'weekday', 'monday':'weekday',
               'tuesday':'weekday','revenue':'revenue','earning':'revenue','earnings':'revenue',
               'income':'revenue','sales':'quantity','sale':'quantity','rev':'revenue','amount':'revenue',
               'countries':'country','country':'country','unit':'quantity','units':'quantity'}

def spell_check(x):
    
    k= ''
    
    num_list = re.sub("[^0-9\s]", "", x).strip().split(" ")
    
    for i in x.split():
        if i not in num_list:
            i = spell(i)
            k = k + ' ' + str(i)
        else:
            k = k + ' ' + i
    return k

def text2int(textnum, numwords={}):
    if not numwords:
        units = ["zero", "one", "two", "three", "four",
                 "five", "six", "seven", "eight", "nine", "ten", "eleven",
                 "twelve", "thirteen", "fourteen", "fifteen", "sixteen",
                 "seventeen", "eighteen", "nineteen"]
        
        tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", 
                "seventy", "eighty", "ninety"]
        
        scales = ["hundred", "thousand", "million", "billion", "trillion"]
        
        numwords["and"] = (1,0)
        
        for idx, word in enumerate(units): numwords[word] = (1, idx)
        for idx, word in enumerate(tens): numwords[word] = (1, idx * 10)
        for idx, word in enumerate(scales): numwords[word] = (10 ** (idx * 3 or 2), 0)
        
    ordinal_words = {'first':1, 'second':2, 'third':3,'fourth':4, 'fifth':5, 'eighth':8, 
                     'ninth':9, 'twelfth':12}
    ordinal_endings = [('ieth', 'y'), ('th', '')]
    
    textnum = textnum.replace('-', ' ')
    
    current = result = 0
    curstring = ""
    onnumber = False
    for word in textnum.split():
        if word in ordinal_words:
            scale, increment = (1, ordinal_words[word])
            current = current * scale + increment
            if scale > 100:
                result += current
                current = 0
            onnumber = True
        else:
            for ending, replacement in ordinal_endings:
                if word.endswith(ending):
                    word = "%s%s" % (word[:-len(ending)], replacement)
            if word not in numwords:
                if onnumber:
                    curstring += repr(result + current) + " "
                curstring += word + " "
                result = current = 0
            else:
                scale, increment = numwords[word]
                
                current = current * scale + increment
                if scale > 100:
                    result += current
                    current = 0
                onnumber = True
    if onnumber:
        curstring += repr(result + current)
        
    return curstring

def numeric_extract(x):
    
    k = re.sub("[^0-9\s]", "", x).strip().split(" ")
    op = []
    for i in k:
        if i!='':
            op.append(i)
    return op

def high_low(x):
    
    k = 0
    for i in x:
        if i in ['top','most','first','upper']:
            k = 1
        
        elif i in ['lowest','least','bottom','last']:
            k = 2
    return k

def qu_op(inp):
    a = inp.lower()
    b = spell_check(a)
    c = text2int(b)
    #d = word_tokenize(c)
    e = pos_tag(word_tokenize(c))
    
    limit_words = []
    num = []
    imp_words = []
    where_word = []
    cols = []
    for i in range(len(e)):
        if e[i][1] in ['JJ','JJS']:
            limit_words.append(e[i][0])
        elif e[i][1] == 'CD':
            num.append(e[i][0])
            #num.append(column_dict.get(e[i][0],''))
        elif e[i][1] in ['NN','NNS']:
            imp_words.append(e[i][0])
            cols.append(column_dict.get(e[i][0],''))
        elif e[i][0].lower()=='in' and str(e[i+1][0]).isdigit():
            where_word.append(e[i+1][0])
        elif e[i][0].lower()=='in' and str(e[i+2][0]).isdigit():
            where_word.append(e[i+2][0])
    for i in limit_words:
        if 'year' in i:
            cols.append('year')
        elif 'month' in i:
            cols.append('month')
    if '2010' in where_word:
        where_df = ' where ' + column_dict[where_word[0]] + '=' + '2010' + ' '
    else:
        where_df = ' where ' + column_dict[where_word[0]] + '=' + '2011' + ' '
    
    group_df = ' group by '        
    
    if 'monthly' in limit_words or 'yearly' in limit_words:
        select_df = "select '2' as graph,"
        from_df = ' from Price_History '
        
        if 'monthly' in limit_words:

            try:
                cols.remove('year')
            except:
                cols = cols
            for i in cols:
                if len(i)>0 and i not in ['quantity','revenue']:
                    select_df += i + ','
                if i in ['quantity','revenue']:
                    select_df += 'sum(' + i + ') as ' + i + ','
                if i == 'date':
                    group_df += 'year,month,day'
                if i == 'country':
                    group_df += i + ','
                if i == 'month':
                    group_df += i + ','
        else:
            where_df = ''
            try:
                cols.remove('month')
            except:
                cols = cols
            for i in cols:
                if len(i)>0 and i not in ['quantity','revenue']:
                    select_df += i + ','
                if i in ['quantity','revenue']:
                    select_df += 'sum(' + i + ') as ' + i + ','
                if i == 'date':
                    group_df += 'year,month,day'
                if i == 'country':
                    group_df += i + ','
                if i == 'year':
                    group_df += i + ','
#        for i in num:
#                if len(i) in [1,2] and i not in ['',' ']:
#                    limit_df += str(i)
        query =   select_df[0:len(select_df)-1] + from_df + where_df + group_df[0:len(group_df)-1]
    #            elif len(i) not in [1,2] and i not in ['',' ']:
    #                query =   select_df[0:len(select_df)-1] + from_df + where_df + group_df[0:len(group_df)-1]
        #select_df[range(len(select_df))] + from_df + where_df + group_df[range(len(group_df))]       
        
    else:
        select_df = "select '1' as graph,"
        from_df = ' from Price_History '
        order_df = ' order by '
        limit_df = ' limit '
        if '2010' in where_word:
            where_df = ' where ' + column_dict[where_word[0]] + '=' + '2010' + ' '
        else:
            where_df = ' where ' + column_dict[where_word[0]] + '=' + '2011' + ' '
        group_df = ' group by '
        for i in cols:
            if len(i)>0 and i not in ['quantity','revenue']:
                select_df += i + ','
            if i in ['quantity','revenue']:
                select_df += 'sum(' + i + ') as ' + i + ','
                order_df += i
            if i == 'date':
                group_df += 'year,month,day'
            if i == 'country':
                group_df += i + ','
            if i == 'month':
                group_df += i + ','
                #where_df = ''
    #        if i == 'year':
    #            group_df += i + ','
    #            #where_df = ''
        for i in num:
                if len(i) in [1,2] and i not in ['',' ']:
                    limit_df += str(i)
                    query =   select_df[0:len(select_df)-1] + from_df + where_df + group_df[0:len(group_df)-1] + order_df + limit_df
#                elif len(i) not in [1,2] and i not in ['',' ']:
#                    query =   select_df[0:len(select_df)-1] + from_df + where_df + group_df[0:len(group_df)-1]
#        select_df[range(len(select_df))] + from_df + where_df + group_df[range(len(group_df))]
    return query




@app.route('/')
def student():
   return render_template('landingpage.html')

@app.route('/result',methods = ['POST','GET'])
def result():
    if request.method == 'POST' or request.method == 'GET':
        engine = sqlite3.connect('csv_test10.db')
        result = request.form['q']  
        query = qu_op(result)
        b = query.split(' ')
        yr = []
        for i in b:
            if 'year' in i:
                yr.append(i[5:len(i)])
        df = pd.read_sql_query(query , engine)   
        print(df)
        
        if df.loc[0,'graph'] == '2':            
            bar_chart = pygal.Bar(width=800, height=600,
                     legend_at_bottom=True, human_readable=True,background = 'white',
                     title= df.columns.values[1].capitalize()+ ' across months in ' + yr[0] ,x_title='Months',y_title = df.columns.values[1].capitalize())
            for index, row in df.iterrows():
                bar_chart.add(row[2], row[1])            
            final = bar_chart.render_data_uri()
            
        #df = df.sort_values('sales',ascending=False)
        
        elif df.loc[0,'graph'] == '1':            
            country_dict = {}
            wm=World(show_legend=False)
            wm.title= df.columns.values[2].capitalize() +" across Top Countries in "+ yr[0]
            for i in range(len(df)):
                for code, name in COUNTRIES.items():        
                    if name.lower() == df.iloc[i,1].lower():
                        country_dict[code] = df.iloc[i,2]
            wm.add("Country:",country_dict)            
            final = wm.render_data_uri()
            
        return render_template('result.html',result = final)
      
if __name__ == '__main__':
   app.run(debug = True)


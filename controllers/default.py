# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------
import json as json

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    response.flash = T("Hello World")
    return dict(message=T('Welcome to web2py!'))


def load_data():
    import pandas as pd
    import os
    import ujson
    wd = os.getcwd()
    privateDir = wd + '/applications/gamerstats1/private/'
    df = pd.read_csv(privateDir+'data/dataset_1/Video_Games_Sales_as_at_22_Dec_2016.csv')
    #print df
    #genres = df.transpose().groupby('Global_Sales')[['Action','Adventure','Fighting','Misc','Platform','Puzzle','Racing','Role-Playing','Shooter','Simulation','Sports','Strategy']].sum()
    regions = df.groupby('Genre')[['NA_Sales','EU_Sales','JP_Sales','Other_Sales']].sum()
    systems = df.groupby('Platform')[['NA_Sales','EU_Sales','JP_Sales','Other_Sales']].sum()
    publishers = df.groupby('Publisher')[['NA_Sales','EU_Sales','JP_Sales','Other_Sales']].sum()
    years = df.groupby('Year_of_Release')[['NA_Sales','EU_Sales','JP_Sales','Other_Sales','Global_Sales']].sum()
    names = df.groupby('Name')[['NA_Sales','EU_Sales','JP_Sales','Other_Sales','Global_Sales']].sum()
    #print years  

    output = {}
    output['regions'] = regions.to_dict()
    output['genres'] = regions.transpose().to_dict()
    output['systems'] = systems.transpose().to_dict()
    output['publishers'] = publishers.transpose().to_dict()
    #output['genres'] = genres.to_dict()
    output['years'] = years.to_dict()
    output['names'] = names.to_dict()
    nameKeys = output['names']['Global_Sales'].keys()
    #output['namesearchlist'] = [n + ' | ' + ','.join(df[df['Name'].isin([n])].dropna()['Platform'].unique()) + ' | ' + ','.join(df[df['Name'].isin([n])].dropna()['Publisher'].unique()) + ' | ' + ','.join(df[df['Name'].isin([n])].dropna()['Genre'].unique()) for n in nameKeys]
    output['namelist'] = nameKeys
    output['genrelist'] = output['genres'].keys()
    output['publisherlist'] = output['publishers'].keys()
    output['systemlist'] = output['systems'].keys()
    
    #ourput['name_list'] = output['names']['Global_Sales'].keys()


    return ujson.dumps(output)

def update_data(req):
    import pandas as pd
    import os
    import ujson

    wd = os.getcwd()
    privateDir = wd + '/applications/gamerstats1/private/'
    df = pd.read_csv(privateDir+'data/dataset_1/Video_Games_Sales_as_at_22_Dec_2016.csv')

    # genre = existsOrEmptyList(req.args.get('genre'),req.args.get('splitter'))
    # system = existsOrEmptyList(req.args.get('system'),req.args.get('splitter'))
    # publisher = existsOrEmptyList(req.args.get('publisher'),req.args.get('splitter'))
    # game = existsOrEmptyList(req.args.get('game'),req.args.get('splitter'))

    genre = existsOrEmptyList(req.vars['genre'],req.vars['splitter'])
    system = existsOrEmptyList(req.vars['system'],req.vars['splitter'])
    publisher = existsOrEmptyList(req.vars['publisher'],req.vars['splitter'])
    game = existsOrEmptyList(req.vars['game'],req.vars['splitter'])

    udf = df

    tag_total = len(genre) + len(system) + len(publisher) + len(game)

    if tag_total > 0:
        udf = df[df['Genre'].isin(genre) | df['Platform'].isin(system) | df['Publisher'].isin(publisher) | df['Name'].isin(game)]
    
    sdf = udf.fillna(0)
    sales = {n : sdf[sdf['Genre'].isin([n])][['Global_Sales']].sum() for n in [g for g in sdf['Genre'].unique() if str(g) != '0']}
    

    #sales = udf[['NA_Sales','EU_Sales','JP_Sales','Other_Sales']].sum().to_dict()

    years = udf.groupby('Year_of_Release')[['NA_Sales','EU_Sales','JP_Sales','Other_Sales']].sum()

    output = {}
    output['subset'] = {}
    output['ratings'] = {}

    if tag_total > 0:
        for g in genre:
            output['subset'][g] = udf[udf['Genre'].isin([g])][['NA_Sales','EU_Sales','JP_Sales','Other_Sales']].sum().to_dict()
            output['ratings'][g] = udf[udf['Genre'].isin([g])][['Critic_Score','User_Score']].mean().dropna().to_dict()
        
        for g in system:
            output['subset'][g] = udf[udf['Platform'].isin([g])][['NA_Sales','EU_Sales','JP_Sales','Other_Sales']].sum().to_dict()
            output['ratings'][g] = udf[udf['Platform'].isin([g])][['Critic_Score','User_Score']].mean().dropna().to_dict()

        for g in publisher:
            output['subset'][g] = udf[udf['Publisher'].isin([g])][['NA_Sales','EU_Sales','JP_Sales','Other_Sales']].sum().to_dict()
            output['ratings'][g] = udf[udf['Publisher'].isin([g])][['Critic_Score','User_Score']].mean().dropna().to_dict()

        for g in game:
            output['subset'][g] = udf[udf['Name'].isin([g])][['NA_Sales','EU_Sales','JP_Sales','Other_Sales']].sum().to_dict()
            output['ratings'][g] = udf[udf['Name'].isin([g])][['Critic_Score','User_Score']].mean().dropna().to_dict()
    else:
        output['subset']['Total'] = udf[['NA_Sales','EU_Sales','JP_Sales','Other_Sales']].sum().to_dict()
        for o in output['subset']['Total']:
            output['subset']['Total'][o] = round(output['subset']['Total'][o],2)

    output['sales'] = sales

    output['years'] = years.to_dict()

    #print udf[['Critic_Score']].dropna().sum()

    #print output
    
    return ujson.dumps(output)

def existsOrEmptyList(v,d):
    output = []
    if v is not None:
        output = str(v).split(d)
    return output

def data():
    return load_data()

def update():
    return update_data(request)

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()



# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html


from scrapy import Item, Field


class FileResponseItem(Item):
    ''' File downloaded after each link opened
    
    This item meant to save the response for further analysis, and also acts as attachment for `EnvEnforcementRecordItem` and `EnvEnforcementFileItem`.    
    Notes:

    Args:

    Attributes:
        collections(str): default collections saved in MongoDB
        uuid(str): unique id of the entry
        createdAt(str): date string of when the item is created 
        updatedAt(str): date string of the last time the item is updated 
        sourceLink(str): URL string of the response source URL
        linkType(str): whether the sourceLink is an `EnvEnforcementFile` or an `EnvEnforcementRecord` item.
        relatedItemId(str): the response related envenforcement id 
        fileType(str): type of the content file type// ['json', 'html', 'xls','xlsx', 'doc', 'docx', 'png', 'jpg', 'csv']
        responseContent(str): content of the string

    Functions:
        None


    '''
    collections = 'fileResponse'

    # General #################################################################
    uuid = Field()
    createdAt = Field()
    updatedAt = Field()
    sourceLink = Field()
    linkType = Field()
    relatedItemId = Field()
    fileType = Field() # ['json', 'html', 'xls','xlsx', 'doc', 'docx', 'png', 'jpg', 'csv']
    responseContent = Field()
 

class EnvEnforcementFileItem(Item):
    ''' Environment Protection Enforcement Annoucement File on Website

    This item is collected for further record extraction. One Annoucement may contain multiple records.

    Notes:

    Args:

    Attributes:
        collections(str): default collections saved in MongoDB
        
        createdAt(str): date string of when the item is created
        updatedAt(str): date string of the last time the item is updated 
        pageLink(str): URL string of the response source URL
        pageTitle(str): title of the page
        pageType(str): page type for further analysis, 

see `settings.FILE_RESPONSE_TYPE`
        keywordHit(list): keywords hit in the file keywords
        pageResponse(list): list of related file response document id
        pageResponseType(list): list of files #TODO 
        pageTable(list): parsed table from html tables
        pageAppendix(list): list of parsed file response id

    Functions:
        None

    '''
    collections = 'enforcementFile'
    # General #################################################################

    createdAt = Field()
    updatedAt = Field()
    pageLink = Field()
    pageTitle = Field()
    pageType = Field()

    # Content #################################################################
    keywordHit = Field()
    pageResponse = Field()
    pageResponseType = Field() # ['xhr', 'html', 'xls','xlsx', 'doc', 'docx', 'png', 'jpg', 'csv']
    pageTable = Field()
    pageAppendix = Field()
    

class EnvEnforcementRecordItem(Item):
    ''' Environment Protection Enforcement Record

    This item meant records an entry of an enforcement
    
    Notes:
    
    Args:

    Attributes:
        collections(str): default collections saved in MongoDB
        
        annouceDate(str): date string of announcement date
        province(str): province where the enforcement record issued
        city(str): city, county or district of where the enforcement record issued
        pageTitle(list): list of titles related to this record
        pageLink(list): list of links related to this record
        pageSourceWebsite(list): list of links origin website
        pageType(list): list of page type related to this record, please see `settings.EPER_RECORD_PAGE_TYPE` 
        createdAt(str): date string of when the item is created
        updatedAt(str): date string of the last time the item is updated 
        
        entity(str): entity name
        entityType(str): entity type, person or an organization like company or institution, see `settings.EPER_ENTITY_TYPE` for definition
        entityCode(str): entity identification code
        entityCodeType(str): type of entity identification code , see `settings.EPER_ENTITY_CODE_TYPE` for definition
        entityAddress(str): address of entity

        
        punishmentSourceStorage(list): list of file response ids
        punishmentFiles(list): list of file response ids
        punishmentParsedText(list): list of parsed text for the record
        punishment(list): list of punishment strings
        punishmentMoneyAmount(list): list of float punishment
        punishmentCurrency(list): list of currency type, see `settings.
        punishmentReason(list): list of punishment reasons(str)
        outlawFact(list): list of break law facts(str)
        legalBasis(list): list of law items(str)


        punisher(list): list of punisher names
        punishmentFilingCode(list): list of punishment filing codes
        
        legalRepresentative(list): list of legal representative names who in charge of the entity
        entityOperator(list): list of operator names who operate the entity



    '''
    # define the fields for your item here like:
    # name = scrapy.Field()
    collections = 'enforcementRecord'


    # General #################################################################
    annouceDate = Field()
    province = Field()
    city = Field()
    pageTitle = Field()
    pageLink = Field()
    pageSourceWebsite = Field()
    pageType = Field() # [htmlTable, text, pdf, png, jpg, xls, doc]
    createdAt = Field()
    updatedAt = Field()
    
    # Entity Info #############################################################
    entity = Field()
    entityType = Field()
    entityCode = Field()
    entityCodeType = Field() # [统一社会信用代码，营业执照]
    entityAddress = Field()
    
    # Adminstrative Punishment ################################################

    punishmentSourceStorage = Field()    
    punishmentFiles = Field()
    punishmentParsedText = Field()
    punishment = Field()
    punishmentMoneyAmount = Field()
    punishmentCurrency = Field()
    punishmentReason = Field()
    outlawFact = Field()
    legalBasis = Field()

    # Punisher ################################################################
    punisher = Field()
    punishmentFilingCode = Field()
    

    
    # Entity Related Person ###################################################
    legalRepresentative = Field()
    entityOperator = Field()


import requests
import json 

def parse_katalog(search_phrase):
    search_phrase = '%20'.join(search_phrase.lower().split())
    # proxies = {3.71.239.218
    #     "http": "http://127.0.0.1:3128",
    #     "https": "http://127.0.0.1:3128" # раскомментируйте если ваш прокси поддерживает https, а  socat или netcat настроены для работы с https.
    # }
    proxies = {
        "http": "http://10.5.30.126:9999",
        "https": "http://10.5.30.126:9999" # раскомментируйте если ваш прокси поддерживает https, а  socat или netcat настроены для работы с https.
    }
    url = f"https://n-katalog.ru/api/service/search?keyword={search_phrase}"
    response = requests.get(url, proxies=proxies, timeout=10).text
    print(response)
    response_json = json.loads(response)
    if(not response_json.get("products")):
        return None
    if(len(response_json["products"]) <= 0):
        return None
    product_url = response_json["products"][0]["link"]
    return "https://n-katalog.ru" + product_url


def parse(search_phrase):
    #search_phrase = '%20'.join(search_phrase.lower().split())
    url = f"https://www.citilink.ru/graphql/"
    headers = {
        "content-type": "application/json",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    }
    payload = '''
        {"query":"query GetFullSearchProductsFilter($fullSearchProductsFilterInput:CatalogFilter_FullSearchFilterInput!){fullSearchFilter(filter:$fullSearchProductsFilterInput){record{...FullSearchProductsFilter},error{... on CatalogFilter_ProductsFilterInternalError{__typename,message},... on CatalogFilter_ProductsFilterIncorrectArgumentsError{__typename,message}}}}fragment FullSearchProductsFilter on CatalogFilter_ProductsFilter{__typename,products{...ProductSnippetFull},sortings{id,name,slug,directions{id,isSelected,name,slug,isDefault}},groups{...SubcategoryProductsFilterGroup},categories{...FilterCategoryInfo},pageInfo{...Pagination},searchStrategy}fragment ProductSnippetFull on Catalog_Product{...ProductSnippetShort,propertiesShort{...ProductProperty},rating,counters{opinions,reviews}}fragment ProductSnippetShort on Catalog_Product{...ProductSnippetBase,labels{...ProductLabel},delivery{__typename,self{__typename,availabilityByDays{__typename,deliveryTime,storeCount},availableInFavoriteStores{store{id,shortName},productsCount}}},stock{countInStores,maxCountInStock},yandexPay{withYandexSplit}}fragment ProductSnippetBase on Catalog_Product{id,name,shortName,slug,isAvailable,images{citilink{...Image}},price{...ProductPrice},category{id,name},brand{name},multiplicity,quantityInPackageFromSupplier}fragment Image on Image{sources{url,size}}fragment ProductPrice on Catalog_ProductPrice{current,old,club,clubPriceViewType,discount{percent}}fragment ProductLabel on Catalog_Label{id,type,title,description,target{...Target},textColor,backgroundColor,expirationTime}fragment Target on Catalog_Target{action{...TargetAction},url,inNewWindow}fragment TargetAction on Catalog_TargetAction{id}fragment ProductProperty on Catalog_Property{name,value}fragment SubcategoryProductsFilterGroup on CatalogFilter_FilterGroup{id,isCollapsed,isDisabled,name,filter{... on CatalogFilter_ListFilter{__typename,isSearchable,logic,filters{id,isDisabled,isInShortList,isInTagList,isSelected,name,total,childGroups{id,isCollapsed,isDisabled,name,filter{... on CatalogFilter_ListFilter{__typename,isSearchable,logic,filters{id,isDisabled,isInShortList,isInTagList,name,isSelected,total}},... on CatalogFilter_RangeFilter{__typename,fromValue,isInTagList,maxValue,minValue,serifValues,scaleStep,toValue,unit}}}}},... on CatalogFilter_RangeFilter{__typename,fromValue,isInTagList,maxValue,minValue,serifValues,scaleStep,toValue,unit}}}fragment FilterCategoryInfo on CatalogFilter_CategoryInfo{category{...Category},isSelected,productsCount}fragment Category on Catalog_Category{__typename,id,name,slug}fragment Pagination on PageInfo{hasNextPage,hasPreviousPage,perPage,page,totalItems,totalPages}","variables":{"fullSearchProductsFilterInput":{"categoryId":"0","pagination":{"page":1,"perPage":5},"conditions":[],"sorting":{"id":"","direction":"SORT_DIRECTION_DESC"},"searchText":"''' + search_phrase + '''","popularitySegmentId":"THREE"}}}
    '''
    response = requests.post(url, headers=headers, data=payload).text
    response_json = json.loads(response)
    if(not response_json.get("data")):
        return None
    response_json = response_json["data"]["fullSearchFilter"]["record"]
    if(not response_json.get("products")):
        return None
    if(len(response_json["products"]) <= 0):
        return None
    product_id = response_json["products"][0]["id"]
    return f"https://www.citilink.ru/product/{product_id}" 



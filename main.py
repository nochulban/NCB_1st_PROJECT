import crawler
import gpt_report


if __name__=="__main__":
    print("키워드를 입력하세요 : ")
    keyword = input()

    print(keyword)
    print(type(keyword))

    #1차    
    if keyword == '':
        crawler.pageSelenium(keyword)
    else:
        crawler.grayhatApi(keyword)
        crawler.pageSelenium(keyword)

    crawler.crawledPageDataInsert()
    gpt_report.run_pipeline(keyword)

    #2차
    

    #3차


    #최종

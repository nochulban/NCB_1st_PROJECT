import crawler
import crawledDataDownload
import virusTotalHash
import gpt_report


if __name__=="__main__":
    mainroot = '/opt/isolation'
    print("키워드를 입력하세요 : ")

    keyword = input()

    print(keyword)
    print(type(keyword))

    # #1차    
    if keyword == '':
        crawler.pageSelenium(keyword)
    else:
        crawler.grayhatApi(keyword)
        crawler.pageSelenium(keyword)

    crawler.crawledPageDataInsert()

    # #2차
    crawledDataDownload.main(mainroot)
    virusTotalHash.scan_all_files_in_directory(mainroot)
    gpt_report.run_pipeline(keyword)

    #3차


    #최종

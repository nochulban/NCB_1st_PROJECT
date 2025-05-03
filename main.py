import crawler
import connectDatabase



if __name__=="__main__":
    print("키워드를 입력하세요 : ")
    keyword = input()

    print(keyword)
    print(type(keyword))



    #1차
    #crawler.pageSelenium(keyword)
    crawler.grayhatApi(keyword)

    #2차

    #3차nn

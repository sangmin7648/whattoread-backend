from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import csv
import time
import re


def openLoveReadingPage(book, driver):
    """입력된 book의 LoveReading페이지를 driver에서 열기
    :param String book: 책 이름
    :param webdriver driver: selenium webdriver 객체
    """
    url = "https://www.lovereading.co.uk/"
    driver.get(url)
    search_input = driver.find_element_by_class_name("books-search-box")
    search_input.send_keys(book)
    search_input.send_keys(Keys.RETURN)
    time.sleep(4)
    book_result = driver.find_element_by_xpath("//a[@data-show='book-results']")
    book_result.click()
    book_link = driver.find_element_by_class_name("category-item-image")
    book_link.click()


def openGoodReadsPage(book, driver):
    """입력된 book의 GoodReads페이지를 driver에서 열기
    :param String book: 책 이름
    :param webdriver driver: selenium webdriver 객체
    """
    url = "https://www.goodreads.com/book/"
    driver.get(url)
    search_input = driver.find_element_by_id("explore_search_query")
    search_button = driver.find_element_by_class_name("searchBox__button")
    search_input.send_keys(book)
    search_button.click()
    try:
        book_cover = driver.find_element_by_class_name("bookCover")
        book_cover.click()
    except Exception:
        close_button = driver.find_element_by_xpath("//img[@src='//s.gr-assets.com/assets/gr/icons/icon_close-63734f04e7baaa77fbad796225e5724c.svg']")
        close_button.click()
        book_cover = driver.find_element_by_class_name("bookCover")
        book_cover.click()


def scrapeLoveReadingMetaData(soup):
    """LoveReading의 soup에서 책의 저자, 장르, 설명 데이터 스크랩해서 반환
    :param BeautifulSoup soup: BeautifulSoup으로 파싱된 html

    :return: author, genres_list, description
    :rtype: author(str), genres_list(list), description(str)
    """
    valid_genres = ["Action Adventure / Spy", "Adult Fiction", "Book Club Recommendations", "Children's Fiction",
        "Classics", "Crime / Mystery", "Debuts", "Diverse Voices", "Dystopian Fiction", "Family Drama",
        "Feel-Good Fiction", "Historical Fiction", "Humour", "Literary Fiction", "Modern and Contemporary Fiction",
        "NewGen - YA Fiction", "Poetry", "Political Thrillers", "Reader Reviewed Books", "Relationship Stories",
        "Sagas and Romance", "Sci-Fi and Fantasy", "Shorter Reads", "Spine-Chilling Fiction", "Star Books",
        "Thriller / Suspense", "Translated Fiction"
    ]
    meta_table = soup.find('table', class_="book-info")
    author = meta_table.find('strong', text=re.compile("Author")).parent.parent.find('a').text.strip()
    genre_list = []
    try :
        # valid_genres에 있는 장르만 append
        genres = meta_table.find('strong', text=re.compile("Genres")).parent.parent.find_all('a')
        for genre in genres:
            genre = genre.text.strip()
            if genre in valid_genres:
                genre_list.append(genre)
    except Exception:
        pass
    description = soup.find('div', class_="book-section-wrapper").find('p').text.strip()
    return author, genre_list, description


def scrapeGoodReadsMetaData(soup):
    """GoodReads의 soup에서 책의 저자, 장르, 설명 데이터 스크랩해서 반환
    :param BeautifulSoup soup: BeautifulSoup으로 파싱된 html

    :return: author, genres_list, description
    :rtype: author(str), genres_list(list), description(str)
    """
    author = soup.find('a', class_="authorName").text.strip()
    genres_div = soup.find('div', class_="rightContainer").find('a', text=re.compile("Genres")).parent.parent.parent
    genres_list = []
    genres = genres_div.find_all('div', class_="elementList")
    for genre in genres:
        genre_name = genre.find('div', class_="left").text.replace("\n       ", '').strip()
        n_genre_vote = genre.find('div', class_="right").text.strip()[:-6]
        genres_list.append((genre_name, n_genre_vote))
    description_div = soup.find('div', id="description")
    if "...more" in description_div.text:
        description = description_div.find('span', style="display:none").text.strip()
    else:
        description = description_div.text.strip()
    return author, genres_list, description


def scrapeGoodReadsReviewData(book, driver, soup):
    """GoodReads의 책 페이지에서 리뷰 데이터 스크랩해서 (book, review)반환
    :param String book: 책 이름
    :param webdriver driver: selenium webdriver 객체    
    :param BeautifulSoup soup: BeautifulSoup으로 파싱된 html

    :return: review_data
    :rtype: List review_data: (book, user, rating, review) 튜플들을 담은 리스트
    """
    review_data = []
    rating_system = {
        'did not like it': 1,
        'it was ok': 2,
        'liked it': 3,
        'really liked it': 4,
        'it was amazing': 5
    }
    n_review_page = 10
    for i in range(n_review_page):
        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        reviews = soup.find_all('div', class_="friendReviews")
        for review in reviews:
            user = review.find('a', class_="user").text.strip()
            rating = rating_system[review.find('span', class_=" staticStars").text.strip()]
            if ("...more" in review.text):
                review = review.find('span', style="display:none")
            else:
                review = review.find('span')
            review = review.get_text(separator=" ").replace("[\"br\"]>", "").replace('\n', ' ').strip()
            if (len(review) > 50):
                    review_data.append((book, user, rating, review))
        next_button = driver.find_element_by_class_name("next_page")
        next_button.click()
        time.sleep(5)
    return review_data


def writeMetaData(file_name, meta_data):
    """책 이름, 저자, 장르, 설명 데이터를 file_name.csv 파일에 작성
    :param String file_name: csv 파일 이름
    :param tuple meta_data: book, author, genres_list, description을 담은 튜플
    """
    file = open(f"{file_name}.csv", 'a')
    writer = csv.writer(file)
    book, author, genres_list, description = meta_data
    writer.writerow([book, author, genres_list, description])
    file.close()


def writeReviewData(file_name, review_data):
    """책 이름, 리뷰 데이터를 file_name.csv 파일에 작성
    :param String file_name: csv 파일 이름
    :param List review_data: (book, review) 튜플들을 담은 리스트
    """
    file = open(f"{file_name}.csv", 'a')
    writer = csv.writer(file)
    for review in review_data:
        book, review = review
        writer.writerow([book, review])
    file.close()


def main():
    driver = webdriver.Firefox(executable_path='/home/sangmin/vscode/mhrisecsv/geckodriver')
    # Time's List of the 100 Best Novels: novels published in the English language between 1923 and 2005. 
    books = [
        "All the King’s Men",
        "American Pastoral",
        "An American Tragedy",
        "Animal Farm",
        "Appointment in Samarra",
        "Are You There God? It's Me",
        "The Assistant",
        "At Swim-Two-Birds",
        "Atonement",
        "Beloved",
        "The Berlin Stories",
        "The Big Sleep",
        "The Blind Assassin",
        "Blood Meridian",
        "Brideshead Revisited",
        "The Bridge of San Luis Rey",
        "Call It Sleep",
        "Catch-22",
        "The Catcher in the Rye",
        "A Clockwork Orange",
        "The Confessions of Nat Turner",
        "The Corrections",
        "The Crying of Lot 49",
        "A Dance to the Music of Time",
        "The Day of the Locust",
        "Death Comes for the Archbishop",
        "A Death in the Family",
        "The Death of the Heart",
        "Deliverance",
        "Dog Soldiers",
        "Falconer",
        "The French Lieutenant's Woman",
        "The Golden Notebook",
        "Go Tell It on the Mountain",
        "Gone with the Wind",
        "The Grapes of Wrath",
        "Gravity's Rainbow",
        "The Great Gatsby",
        "A Handful of Dust",
        "The Heart Is a Lonely Hunter",
        "The Heart of the Matter",
        "Herzog",
        "Housekeeping",
        "A House for Mr. Biswas",
        "Infinite Jest",
        "Invisible Man",
        "Light in August",
        "The Lion",
        "Lolita",
        "Lord of the Flies",
        "The Lord of the Rings",
        "Loving",
        "Lucky Jim",
        "The Man Who Loved Children",
        "Midnight's Children",
        "Money",
        "The Moviegoer",
        "Mrs. Dalloway",
        "Naked Lunch",
        "Native Son",
        "Neuromancer",
        "Never Let Me Go",
        "1984",
        "On the Road",
        "One Flew Over the Cuckoo's Nest",
        "The Painted Bird",
        "Pale Fire",
        "A Passage to India",
        "Play It as It Lays",
        "Portnoy's Complaint",
        "Possession",
        "The Power and the Glory",
        "The Prime of Miss Jean Brodie",
        "Rabbit",
        "Ragtime",
        "The Recognitions",
        "Red Harvest",
        "Revolutionary Road",
        "The Sheltering Sky",
        "Slaughterhouse-Five",
        "Snow Crash",
        "The Sot-Weed Factor",
        "The Sound and the Fury",
        "The Sportswriter",
        "The Spy Who Came in from the Cold",
        "The Sun Also Rises",
        "Their Eyes Were Watching God",
        "Things Fall Apart",
        "To Kill a Mockingbird",
        "To the Lighthouse",
        "Tropic of Cancer",
        "Ubik",
        "Under the Net",
        "Under the Volcano",
        "Watchmen",
        "White Noise",
        "White Teeth",
        "Wide Sargasso Sea",
        "The Adventures of Augie March"
    ]
    meta_file_name = "meta.csv"
    meta_file = open(meta_file_name, 'w')
    for book in books:
        openGoodReadsPage(book, driver)
        html = driver.page_source
        soup = BeautifulSoup(html, "lxml")
        author, genres_list, description = scrapeGoodReadsMetaData(soup)
        meta_data = (book, author, genres_list, description)
        writeMetaData(meta_file_name, meta_data)
        time.sleep(5)
    meta_file.close()

if (__name__ == "__main__"):
    main()

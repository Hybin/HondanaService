from bs4 import BeautifulSoup
from urllib.request import urlopen


class Worker(object):
    def __init__(self, conf):
        self.conf = conf
        self.rank = "ranking_block_{}"

    def load(self):
        """
        Load the index of WeRead
        :return: BeautifulSoup Object - soup
        """
        doc = urlopen(self.conf.url)
        soup = BeautifulSoup(doc, "html.parser")
        return soup

    def get_rank_header(self, block):
        """
        Get the header of the ranking block
        :param block: HTMLElement
        :return: string - header
        """
        header = block.find('h2', class_=self.rank.format("header_title"))
        return header.text

    def get_rank_body(self, block):
        """
        Get the body of the ranking block
        :param block: HTMLElement
        :return: list<HTMLElement> - body
        """
        positions = ["body_left", "body_right"]
        body = [block.find('div', class_=self.rank.format(position)) for position in positions]
        return body

    def get_book_info(self, element):
        """
        Get the information of the book
        :param element: HTMLElement
        :return: dict - book
        """
        book = {
            "title": element["title"],
            "cover": element.find("div", class_=self.rank.format("book_cover")).find("img")["src"],
            "link": element.find("a", class_=self.rank.format("book_link"))["href"],
            "rank": element.find('span', class_=self.rank.format("book_index")).text,
            "author": {
                "name": element.find('a', class_=self.rank.format("book_author")).text,
                "link": element.find('a', class_=self.rank.format("book_author"))["href"]
            }
        }
        return book

    def get_top_list(self):
        """
        Get the content of the top list
        :return: dict - top_list
        """
        soup = self.load()

        top_list, blocks = dict(), soup.find_all("div", class_=self.rank.format("container"))
        for block in blocks:
            books = list()
            header, body = self.get_rank_header(block), self.get_rank_body(block)

            for component in body:
                content = component.find_all("div", class_=self.rank.format("book"))
                for element in content:
                    book = self.get_book_info(element)
                    books.append(book)

            top_list[header] = books

        return top_list

from unittest import TestCase, main
from ant.worker import Worker
from utility.config import Config


class TestWorker(TestCase):
    def setUp(self):
        self.conf = Config()
        self.worker = Worker(self.conf)
        self.soup = self.worker.load()

    def test_rank(self):
        self.assertEqual(self.worker.rank, "ranking_block_{}")

    def test_load(self):
        self.assertEqual(self.soup.title.text, "微信读书-正版书籍小说免费阅读")

    def test_get_rank_header(self):
        block = self.soup.find_all("div", class_=self.worker.rank.format("container"))[0]
        self.assertEqual(self.worker.get_rank_header(block), "总榜")

    def test_get_rank_body(self):
        block = self.soup.find_all("div", class_=self.worker.rank.format("container"))[0]
        self.assertEqual(len(self.worker.get_rank_body(block)), 2)

    def test_get_book_info(self):
        target = {
            'title': '围城',
            'rank': '1',
            'link': '/web/reader/54c32520715e229954c8b8a',
            'cover': 'https://rescdn.qqmail.com/weread/cover/457/22946457/t6_22946457.jpg',
            'author': {
                'link': '/web/search/books?author=%E9%92%B1%E9%94%BA%E4%B9%A6',
                'name': '钱锺书'
            }
        }
        block = self.soup.find_all("div", class_=self.worker.rank.format("container"))[0]
        content = self.worker.get_rank_body(block)[0]
        element = content.find_all("div", class_=self.worker.rank.format("book"))[0]
        book = self.worker.get_book_info(element)
        self.assertDictEqual(book, target)


if __name__ == "__main__":
    main()

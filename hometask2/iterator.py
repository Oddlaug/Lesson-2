# -*- coding:utf-8 -*-
import optparse
import json
from json.decoder import JSONDecodeError
import wikipedia
from wikipedia.exceptions import PageError, DisambiguationError
from hometask2.generator import is_exists


class CountryFinder:
    def __init__(self, countries_file):
        if is_exists(countries_file):
            self.__countries_file = countries_file
            self.__countries = None
            self.__start = -1
            self.__get_countries()

        else:
            raise FileNotFoundError('Invalid input file!')

    def __iter__(self):
        return self

    def __next__(self):
        if len(self.__countries):
            self.__start += 1
            if self.__start != len(self.__countries):
                country = self.__countries[self.__start]
                user_data = {}
                try:
                    url = wikipedia.page(country).url
                    user_data['name'] = country
                    user_data['url'] = url
                except (PageError, DisambiguationError, KeyError) as e:
                    print(e)
                return user_data
            else:
                raise StopIteration
        else:
            raise TypeError('Invalid country list!')

    def __get_countries(self):
        with open(self.__countries_file, encoding='utf-8') as f:
            try:
                self.__countries = [key['name']['official'] for key in json.load(f)]
            except JSONDecodeError as e:
                print(f'JSON Error => "{e}"')


def main():
    parser = optparse.OptionParser()
    parser.add_option("-s", "--source",
                      dest="source",
                      default=False,
                      action="store_true",
                      help="path to countries file"
                      )
    parser.add_option("-d", "--dest",
                      dest="destination",
                      default=False,
                      action="store_true",
                      help="path to export file"
                      )

    (_, args) = parser.parse_args()
    try:
        source_file = rf'{args[0]}'
        destination_file = rf'{args[1]}'
        countries = {}

        for country in CountryFinder(source_file):
            try:
                countries[country['name']] = country
            except KeyError:
                pass

        with open(destination_file, 'w', encoding='utf-8') as f:
            json.dump(countries, f, indent=4, ensure_ascii=False)

    except IndexError:
        print('Usage: python iterator.py -s <json file> -d <export_file.json>')


if __name__ == '__main__':
    main()

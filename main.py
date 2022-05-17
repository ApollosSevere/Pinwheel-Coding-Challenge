import json
import requests
from pathlib import Path
from loguru import logger
from bs4 import BeautifulSoup

recorded_forms = {}
MIN_YEAR = 2018
MAX_YEAR = 2020


def get_form_info(rows):
    for form in rows:
        try:
            # split form_name to check for english versions
            form_name = form.find(name='td', class_='LeftCellSpacer').text.split(' (', 1)
            form_title = form.find(name='td', class_='MiddleCellSpacer').text.strip()
            form_year = int(form.find(name='td', class_='EndCellSpacer').text.strip())

            if len(form_name) < 2:  # if length > 1, then we don't have an english version
                form_number = form_name[0].strip()

                if recorded_forms.get(form_number):  # if record exits, update it accordingly
                    form_item = recorded_forms[form_number]
                    if form_item['min_year'] > form_year:
                        form_item['min_year'] = form_year
                    elif form_item['max_year'] < form_year:
                        form_item['max_year'] = form_year
                else:
                    recorded_forms[form_number] = {
                        "form_number": form_number,
                        "form_title": form_title,
                        "min_year": form_year,
                        "max_year": form_year
                    }
        except Exception as e:
            logger.error(f'Can not parse form info, error: {e}')


def save_form_pdf(rows):
    for row in rows:
        try:
            form_year = int(row.find(name='td', class_='EndCellSpacer').text.strip())
            form_element = row.findChild(['LeftCellSpacer', 'a'])
            form_name = form_element.string.split(' (', 1)  # split to check for english versions

            if MIN_YEAR <= form_year <= MAX_YEAR and len(form_name) < 2:
                form_number = form_name[0].strip()
                link_url = form_element.attrs['href']
                resp = requests.get(link_url, stream=True)

                # creates file path and skips If file exits
                Path("Downloaded_PDFs" + "/" + form_number).mkdir(parents=True, exist_ok=True)

                filename = "Downloaded_PDFs/{}/{} - {}.pdf".format(form_number, form_number, form_year)
                with open(filename, 'wb') as pdf:
                    for chunk in resp.iter_content(chunk_size=1024):
                        """ We must write one chunk at a time for large PDF files"""
                        pdf.write(chunk)
        except Exception as e:
            logger.error(f'Can not save file, error: {e}')


def main():
    try:
        print("Loading ... ")
        print("Retrieving form data ...")
        print("Downloading PDFs ...")

        pagination = 0
        more_rows = True

        while more_rows:
            url = (f'https://apps.irs.gov/app/picklist/list/priorFormPublication.html?'
                   f'indexOfFirstRow={pagination}&'
                   f'sortColumn=sortOrder&'
                   f'value=&criteria=&'
                   f'resultsPerPage=200&'
                   f'isDescending=false')
            html_text = requests.get(url).text
            soup = BeautifulSoup(html_text, 'lxml')
            table = soup.find('table', attrs={'class': 'picklist-dataTable'})
            rows = table.find_all('tr')[1:]  # Must omit header

            if rows:
                pagination += 200
                get_form_info(rows)
                save_form_pdf(rows)
            else:
                more_rows = False

    except Exception as e:
        logger.error(f'Cannot connect to website, error: {e}')

    form_data = list(recorded_forms.values())
    json_object = json.dumps(form_data, indent=4)

    return json_object


if __name__ == '__main__':
    # Added a logging system to record if something goes wrong
    logger.add('errors.txt', level='ERROR', rotation="30 days", backtrace=True)

    Path("FormData_Results").mkdir(parents=True, exist_ok=True)
    with open('FormData_Results/data.json', 'w') as outfile:
        outfile.write(main())

    print("Done!")

from selenium import webdriver
import pandas as pd

chromedriver_path = './chromedriver'
url = 'http://www.statiz.co.kr'
play_list_path = './player_list.csv'

problem_list = []

def main():

    driver = webdriver.Chrome(chromedriver_path)
    driver.get(url)
     
    player_list = pd.read_csv(play_list_path, encoding = "cp949")
     
    col_names = ['date', 'vs', 'result', 'list_number', 'postion','start', 'ab', 'run', 'hit', 'hit2', 'hit3', 'hr', 'tb', 'rbi', 
    'sb', 'cs', 'bb', 'hbp', 'ibb', 'so', 'gdp', 'hst', 'hsf', 'avg','obp', 'slg', 'ops', 'pitch', 'avli', 're24', 'wpa']

    output = pd.DataFrame(columns=col_names)

    odd_evens = ['oddrow_stz0', 'evenrow_stz0']

    for index, row in player_list.iterrows():
        batter_name = row['batter_name']
        birth = row['birth']
        season = row['season']

        print('=' * 20)
        print("batter name: ", batter_name)
        print("batter name: ", batter_name)
        print("birth: ", birth)
        print("season: ", season)
        print('=' * 20)

        driver.find_element_by_name('name').send_keys('{}'.format(batter_name))
        driver.find_element_by_css_selector('.input-group-btn').click()

        player_first_page_url = driver.current_url
        player_first_page_url = player_first_page_url.replace('search=', '')
        player_first_page_url = player_first_page_url + 'birth={}'.format(birth)

        day_by_day_url = player_first_page_url[:35] + 'opt=3&' + player_first_page_url[35:]

        season_day_by_day_url = day_by_day_url + '&re=0&se=&da=&year={}&cv='.format(season)
        driver.get(season_day_by_day_url)

        results = []

        try: 
            for odd_even in odd_evens:
                for row in driver.find_elements_by_css_selector("tr.{}".format(odd_even)):

                    day_by_day_result = []    
                    for i in range(0,31):   
                        value = row.find_elements_by_tag_name("td")[i].text
                        day_by_day_result.append(value)

                    print(day_by_day_result)
                    results.append(day_by_day_result)

            results_df = pd.DataFrame(results)
            results_df.columns = col_names
            results_df['batter_name'] = batter_name
            results_df['season'] = season

            results_df_sort = results_df.sort_values(["date"])
            results_df_sort = results_df_sort.reset_index(drop=True)

            output = output.append(results_df_sort, ignore_index=True, sort=False)
            output.to_csv('./output.csv', index=False,encoding = "cp949")

        except Exception as e:
            print('이선수 문제 있다.')
            problem_list.append((batter_name, season))
            continue            
    

if __name__ == '__main__':
    main()

